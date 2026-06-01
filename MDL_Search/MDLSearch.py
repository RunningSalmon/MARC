import copy
import heapq
from itertools import pairwise

from Datatypes.Abstract_ARC_Task import AbstractMatrixPair
from Evaluation.Object_Mapping import create_object_mapping
from Evaluation.Summary_Statistic import SummaryStatistic
from Task_Generation.Matrix_Transformation import manipulate_abstract_matrix
from Transformations.Transformation import *
from Evaluation.Matrix_Pair_Evaluation import *
from Datatypes.ARC_Task import *
from Evaluation.Feature import *

beam_width = 30

class HeapItem:
    def __init__(self, mdl: float, nll: float, transforms: list[Transformation], transformed_matrices: list[AbstractObjectMatrix]):
        self.mdl = mdl
        self.nll = nll
        self.transforms = transforms
        self.transformed_matrices = transformed_matrices

    def __lt__(self, other):
        return self.mdl < other.mdl

def initialize_mdl_search(abstract_arc_task: AbstractARCTask,
                          transformations: list[Transformation],
                          eval_features: list[Feature],
                          statistics: list[SummaryStatistic],
                          conditions: list[Condition]):
    training_pairs = abstract_arc_task.train
    heap = []
    primitive_transformations = []
    possible_conditions = set()

    for transformation in transformations: #iterate over transformations
        params = transformation.parameters
        nll = transformation.get_nll(len(transformations))
        for param in params: #iterate over all possible parameters for transformation
            transformation.fixed_parameter = param
            transform_param_scores = []
            transformed_matrices = []
            for abstract_matrix_pair in training_pairs: #iterate over trials
                if conditions:
                    transform_param_results = transform_eval_matrix_pair_conditioned(abstract_matrix_pair,
                                                                           transformation,
                                                                           eval_features,
                                                                           statistics,
                                                                           conditions)
                    transform_param_possible_conditions, score, transformed_matrix = transform_param_results
                    possible_conditions.update(transform_param_possible_conditions)
                else:
                    transform_param_results = transform_eval_matrix_pair(abstract_matrix_pair,
                                                                           transformation,
                                                                           eval_features,
                                                                           statistics,)
                    score, transformed_matrix = transform_param_results

                transform_param_scores.append(score)
                transformed_matrices.append(transformed_matrix)

            mean_transform_param_score = float(np.mean(transform_param_scores))
            mdl = nll * (1-mean_transform_param_score)
            #print(transformation, param, mean_transform_param_score, nll, mdl)
            heapq.heappush(heap, HeapItem(mdl, nll, [transformation.from_parameter_condition(param)], transformed_matrices))
            primitive_transformations.append(transformation.from_parameter_condition(param))

            if possible_conditions:
                for condition in possible_conditions:
                    transformation.condition = condition
                    scores = []
                    for abstract_matrix_pair in training_pairs:  # iterate over trials
                        transform_param_results = transform_eval_matrix_pair(abstract_matrix_pair,
                                                                           transformation,
                                                                           eval_features,
                                                                           statistics,)
                        score, transformed_matrix = transform_param_results
                        scores.append(score)
                    mean_score = float(np.mean(scores))
                    if mean_score > mean_transform_param_score:
                        mdl = nll * (1-mean_score)
                        heapq.heappush(heap,
                                       HeapItem(mdl, nll, [transformation.from_parameter_condition(param, condition)], transformed_matrices))


    return heap, primitive_transformations

def mdl_search_step(abstract_matrix_pair: AbstractARCTask,
                    heap: list,
                    primitive_transformations: list,
                    visited: set,
                    eval_features: list[Feature],
                    statistics: list[SummaryStatistic]) -> tuple[list, set]:
    training_pairs = abstract_matrix_pair.train
    item: HeapItem = heapq.heappop(heap)
    transforms = item.transforms

    # check if sequence already visited else append to visited
    key = tuple(repr(transform) for transform in transforms)
    if key in visited:
        return heap, visited
    visited.add(key)

    transformed_matrices = item.transformed_matrices
    transformation_series_mdl = item.mdl
    transformation_series_nll = item.nll
    solved = True


    for transformation in primitive_transformations:
        anticipatory_matrices = []
        transform_score = 0
        for i, abstract_matrix_pair in enumerate(training_pairs):
            transformed_matrix = transformed_matrices[i]
            output_matrix = abstract_matrix_pair.output
            object_pairing = abstract_matrix_pair.mapping

            if transformed_matrix != output_matrix:
                solved = False

            #manipulate matrix
            anticipatory_matrix = copy.deepcopy(transformed_matrix)
            transformation.transform_abstract_matrix(anticipatory_matrix)
            anticipatory_pair = AbstractMatrixPair(anticipatory_matrix, output_matrix, object_pairing)

            # object evaluation
            if not anticipatory_pair.mapping:  # establish pairing if not yet existing
                anticipatory_pair.mapping = create_object_mapping(anticipatory_pair, eval_features)
            if anticipatory_pair.mapping and eval_features:
                score = obj_eval_abstract_matrix_pair(anticipatory_pair, eval_features)  # compare to output matrix
                transform_score += score  # add to the accumulated transform(param) score

            # summary statistics evaluation
            elif statistics:
                transform_score = sumstat_eval_abstract_matrix_pair(anticipatory_pair, statistics)
            else:
                raise ValueError("no Summary Statistics given to the search. Failed because there were either no Features given or there was no unambiguous object mapping.")

            anticipatory_matrices.append(anticipatory_matrix)

        mean_transform_score = transform_score / len(training_pairs)
        nll = transformation.get_nll(len(primitive_transformations))
        new_transformation_series_nll = transformation_series_nll + nll
        new_transformation_series_mdl = (1-mean_transform_score) * new_transformation_series_nll

        accumulated_transforms = transforms + [transformation]
        heapq.heappush(heap, HeapItem(new_transformation_series_mdl, nll, accumulated_transforms, anticipatory_matrices))



    return heap, visited

def check_if_solved(abstract_arc_task: AbstractARCTask, heap_item: HeapItem):
    transformed_matrices = heap_item.transformed_matrices
    training_pairs = abstract_arc_task.train
    for i, abstract_matrix_pair in enumerate(training_pairs):
        transformed_matrix = transformed_matrices[i]
        output_matrix = abstract_matrix_pair.output

        if transformed_matrix != output_matrix:
            return False
    return True

def mdl_search(abstract_arc_task: AbstractARCTask,
               transformations: list[Transformation],
               eval_features: list[Feature],
               statistics: list[SummaryStatistic],
               conditions: list[Condition]):
    heap, primitive_transformations = initialize_mdl_search(abstract_arc_task, transformations, eval_features, statistics, conditions)
    visited = set()

    max_step_nr = 0
    step = 0

    #debug
    print_heap = copy.deepcopy(heap)
    while print_heap:
        item = heapq.heappop(print_heap)
        print(f"heap in step {step}: score: {item.mdl}, transforms: {item.transforms}")
    
    while heap and step < max_step_nr:
        # debug
        #print_heap = copy.deepcopy(heap)
        #while print_heap:
        #    item = heapq.heappop(print_heap)
        #    print(f"heap in step {step}: score: {item.mdl}, transforms: {item.transforms}")

        # check if the currently best heap item is a solution
        heap_item: HeapItem = heap[0]
        if check_if_solved(abstract_arc_task, heap_item):
            return heap_item.transforms, visited, step

        #update the heap with one step
        heap, visited = mdl_search_step(abstract_arc_task, heap, primitive_transformations, visited, eval_features, statistics)
        step += 1
        if len(heap) > beam_width: #limit heap to beam_width
            optima = heapq.nsmallest(beam_width, heap)
            heapq.heapify(optima)
            heap = optima

    return None, visited, step

def transform_eval_matrix_pair_conditioned(abstract_matrix_pair: AbstractMatrixPair,
                                           parameterized_transformation: Transformation,
                                           eval_features: list[Feature],
                                           statistics: list[SummaryStatistic],
                                           conditions: list[Condition]):
    if parameterized_transformation.fixed_parameter is None:
        raise ValueError("check for condition needs parameterized transformation")
    input_matrix = abstract_matrix_pair.input
    output_matrix = abstract_matrix_pair.output
    matrix_shape = input_matrix.height, input_matrix.width
    positive_change = []
    negative_change = []
    scores = []
    manipulatable_input_matrix = copy.deepcopy(input_matrix)

    if abstract_matrix_pair.mapping: #per object evaluation
        for input_obj_idx, output_obj_idx in abstract_matrix_pair.mapping.items():
            input_obj = input_matrix.abstract_objects[input_obj_idx]
            output_obj = output_matrix.abstract_objects[output_obj_idx]
            current_score = evaluate_abstract_object_pair(input_obj, output_obj, eval_features, matrix_shape)
            parameterized_transformation.transform_abstract_object(input_obj)
            new_score = evaluate_abstract_object_pair(input_obj, output_obj, eval_features, matrix_shape)
            scores.append(new_score)
            if new_score > current_score:
                positive_change.append(input_obj)
            else:
                negative_change.append(input_obj)
    else: #summary stat evaluation
        manipulatable_pair = AbstractMatrixPair(manipulatable_input_matrix, output_matrix)
        for input_obj in manipulatable_input_matrix.abstract_objects:
            current_score = sumstat_eval_abstract_matrix_pair(manipulatable_pair, statistics)
            parameterized_transformation.transform_abstract_object(input_obj)
            new_score = sumstat_eval_abstract_matrix_pair(manipulatable_pair, statistics)
            scores.append(new_score)
            if new_score > current_score:
                positive_change.append(input_obj)
            else:
                negative_change.append(input_obj)

    matrix_pair_score = np.mean(scores)
    possible_conditions = [
        result
        for condition in conditions
        for result in condition.explains_grouping(positive_change, negative_change)
    ]

    return possible_conditions, matrix_pair_score, manipulatable_input_matrix

def transform_eval_matrix_pair(abstract_matrix_pair: AbstractMatrixPair,
                               parameterized_transformation: Transformation,
                               eval_features: list[Feature],
                               statistics: list[SummaryStatistic]):
    manipulatable_input_matrix = copy.deepcopy(abstract_matrix_pair.input)
    parameterized_transformation.transform_abstract_matrix(manipulatable_input_matrix)
    transformed_matrix_pair = AbstractMatrixPair(manipulatable_input_matrix, abstract_matrix_pair.output)
    if check_for_object_mapping(transformed_matrix_pair, eval_features): #per object evaluation
        score = obj_eval_abstract_matrix_pair(transformed_matrix_pair, eval_features)
    else: #Summary stat evaluation
        score = sumstat_eval_abstract_matrix_pair(transformed_matrix_pair, statistics)

    return score, manipulatable_input_matrix



def check_for_object_mapping(abstract_matrix_pair: AbstractMatrixPair, eval_features: list[Feature]):
    if not abstract_matrix_pair.mapping:
        mapping = create_object_mapping(abstract_matrix_pair, eval_features)
        if not mapping:
            return False
        abstract_matrix_pair.mapping = mapping
    return True

