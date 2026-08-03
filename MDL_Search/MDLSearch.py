import copy
import heapq

from Evaluation.Object_Mapping import create_object_mapping
from Transformations.Transformation import *
from Evaluation.Matrix_Pair_Evaluation import *
from Datatypes.ARC_Task import *
from Evaluation.Feature import *

beam_width = 30


class HeapItem:
    def __init__(self, mdl: float, nll: float, transforms: list[Transformation],
                 transformed_matrices: list[AbstractObjectMatrix]):
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
    """
    sets up the heap for the MDL search and the list of primitive transformations
    :arg abstract_arc_task: the task to be solved
    :arg transformations: the list of transformation algorithms to be considered
    :arg eval_features: the list of evaluation features for object based evaluation
    :arg statistics: the list of summary statistics for statistics based evaluation
    :arg conditions: the list of conditions to be considered in the search
    :returns: a list of primitive transformations and the heap containing all initial transformation series
    """
    training_pairs = abstract_arc_task.train
    heap = []
    primitive_transformations = []

    for transformation in transformations:  # iterate over transformations
        params = transformation.possible_parameters
        nll = transformation.get_nll(len(transformations), len(conditions))
        for param in params:  # iterate over all possible parameters for transformation
            possible_conditions = set()
            transform_param_scores = []
            transformed_matrices = []
            for abstract_matrix_pair in training_pairs:  # iterate over trials
                if conditions:
                    transform_param_results = transform_eval_matrix_pair_conditioned(abstract_matrix_pair,
                                                                                     transformation,
                                                                                     param,
                                                                                     eval_features,
                                                                                     statistics,
                                                                                     conditions)
                    transform_param_possible_conditions, score, transformed_matrix = transform_param_results
                    possible_conditions.update(transform_param_possible_conditions)
                else:
                    transform_param_results = transform_eval_matrix_pair(abstract_matrix_pair,
                                                                         transformation,
                                                                         param,
                                                                         eval_features,
                                                                         statistics, )
                    score, transformed_matrix = transform_param_results

                transform_param_scores.append(score)
                transformed_matrices.append(transformed_matrix)

            mean_transform_param_score = float(np.mean(transform_param_scores))
            mdl = nll * (1 - mean_transform_param_score)
            # print(transformation, param, mean_transform_param_score, nll, mdl)
            heapq.heappush(heap,
                           HeapItem(mdl, nll, [transformation.from_parameter_condition(param)], transformed_matrices))
            primitive_transformations.append(transformation.from_parameter_condition(param))

            if possible_conditions:
                for condition in possible_conditions:
                    transform = copy.deepcopy(transformation)
                    transform.condition = condition
                    scores = []
                    transformed_matrices = []
                    for abstract_matrix_pair in training_pairs:  # iterate over trials
                        transform_param_results = transform_eval_matrix_pair(abstract_matrix_pair,
                                                                             transform,
                                                                             param,
                                                                             eval_features,
                                                                             statistics, )
                        score, transformed_matrix = transform_param_results
                        scores.append(score)
                        transformed_matrices.append(transformed_matrix)
                    mean_score = float(np.mean(scores))
                    if mean_score > mean_transform_param_score:
                        mdl = nll * (1 - mean_score)
                        heapq.heappush(heap,
                                       HeapItem(mdl, nll, [transform.from_parameter_condition(param, condition)],
                                                transformed_matrices))

    return heap, primitive_transformations


def mdl_search_step(abstract_arc_task: AbstractARCTask,
                    heap: list,
                    primitive_transformations: list,
                    visited: set,
                    eval_features: list[Feature],
                    statistics: list[SummaryStatistic],
                    conditions: list[Condition]) -> tuple[list, set]:
    """
        pops the transformation series with the lowest MDL score from the heap and expands it with all possible transformations
        :arg abstract_arc_task: the task to be solved
        :arg heap: the heap containing up to 30 transformation series sorted by their MDL score
        :arg primitive_transformations: the list of primitive transformations established in the initialization
        :arg visited: the set of transformation series that have already been visited
        :arg eval_features: the list of evaluation features for object based evaluation
        :arg statistics: the list of summary statistics for statistics based evaluation
        :arg conditions: the list of conditions to be considered in the search
        :returns: the heap with all expanded transformation series added to it and the set of transformation series that have already been visited
        """
    training_pairs: list[AbstractMatrixPair] = abstract_arc_task.train
    item: HeapItem = heapq.heappop(heap)
    transforms: list[Transformation] = item.transforms
    # print(f"Expanded: {item.transforms} with DL: {item.mdl}")

    # check if sequence already visited else append to visited
    key = tuple(repr(transform) for transform in transforms)
    if key in visited:
        return heap, visited
    visited.add(key)

    transformed_matrices = item.transformed_matrices  # input matrices with current Transform-Series applied
    transformation_series_nll = item.nll  # accumulated nll over transforms

    for transformation in primitive_transformations:
        anticipatory_matrices = []
        transform_scores = []
        possible_conditions = set()
        for i, abstract_arc_task in enumerate(training_pairs):
            manipulatable_transformed_matrix = copy.deepcopy(
                transformed_matrices[i])  # manipulatable matrix with current series applied
            output_matrix = abstract_arc_task.output  # non-manipulatable output matrix for eval
            manipulatable_transformed_pair = AbstractMatrixPair(manipulatable_transformed_matrix, output_matrix)

            if conditions:
                transform_param_results = transform_eval_matrix_pair_conditioned(manipulatable_transformed_pair,
                                                                                 transformation,
                                                                                 None,
                                                                                 # primitive transforms have fixed parameters
                                                                                 eval_features,
                                                                                 statistics,
                                                                                 conditions)
                transform_param_possible_conditions, score, transformed_matrix = transform_param_results
                possible_conditions.update(transform_param_possible_conditions)
            else:
                transform_param_results = transform_eval_matrix_pair(manipulatable_transformed_pair,
                                                                     transformation,
                                                                     None,  # primitive transforms have fixed parameters
                                                                     eval_features,
                                                                     statistics)
                score, transformed_matrix = transform_param_results

            transform_scores.append(score)
            anticipatory_matrices.append(transformed_matrix)

        mean_transform_score = np.mean(transform_scores)
        nll = transformation.get_nll(len(primitive_transformations), len(conditions))
        new_transformation_series_nll = transformation_series_nll + nll
        new_transformation_series_mdl = (1 - mean_transform_score) * new_transformation_series_nll

        accumulated_transforms = transforms + [transformation]
        heapq.heappush(heap,
                       HeapItem(new_transformation_series_mdl,
                                new_transformation_series_nll,
                                accumulated_transforms,
                                anticipatory_matrices)
                       )

        if possible_conditions:
            for condition in possible_conditions:
                conditioned_transformation = copy.deepcopy(transformation)
                conditioned_transformation.condition = condition
                scores = []
                anticipatory_matrices = []
                for i, abstract_arc_task in enumerate(training_pairs):
                    manipulatable_transformed_matrix = copy.deepcopy(transformed_matrices[i])
                    output_matrix = abstract_arc_task.output
                    manipulatable_transformed_pair = AbstractMatrixPair(manipulatable_transformed_matrix, output_matrix)

                    transform_param_results = transform_eval_matrix_pair(manipulatable_transformed_pair,
                                                                         conditioned_transformation,
                                                                         None,
                                                                         eval_features,
                                                                         statistics)
                    score, manipulatable_transformed_matrix = transform_param_results
                    scores.append(score)
                    anticipatory_matrices.append(manipulatable_transformed_matrix)
                mean_score = float(np.mean(scores))
                if mean_score > mean_transform_score:
                    nll = conditioned_transformation.get_nll(len(primitive_transformations), len(conditions))
                    new_transformation_series_nll = transformation_series_nll + nll
                    new_transformation_series_mdl = (1 - mean_score) * new_transformation_series_nll
                    accumulated_transforms = transforms + [conditioned_transformation]
                    heapq.heappush(heap, HeapItem(new_transformation_series_mdl, new_transformation_series_nll,
                                                  accumulated_transforms, anticipatory_matrices))

    return heap, visited


def check_if_solved(abstract_arc_task: AbstractARCTask, heap_item: HeapItem):
    """returns true if the given transformation series is a solution, else false"""
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
    """
    initializes and executes the MDL search for the given task. Prunes the heap to the 30 best items after every steps and returns a solution for all training trials if found.
    :arg abstract_arc_task: the task to be solved
    :arg transformations: the list of transformation algorithms to be considered
    :arg eval_features: the list of evaluation features for object based evaluation
    :arg statistics: the list of summary statistics for statistics based evaluation
    :arg conditions: the list of conditions to be considered in the search
    :returns: a series of transformations that solves the task, the number of steps it took to find a solution and the transformation series that were visited

    """
    heap, primitive_transformations = initialize_mdl_search(abstract_arc_task, transformations, eval_features,
                                                            statistics, conditions)
    visited = set()

    max_step_nr = 100
    step = 0

    ## debug
    # print_heap = copy.deepcopy(heap)
    # while print_heap:
    #    item = heapq.heappop(print_heap)
    #    print(f"heap in step {step}: score: {item.mdl}, transforms: {item.transforms}")

    while heap and step < max_step_nr:
        ## debug
        # print_heap = copy.deepcopy(heap)
        # while print_heap:
        #    item = heapq.heappop(print_heap)
        #    print(f"heap in step {step}: mdl: {item.mdl}, nll: {item.nll}, transforms: {item.transforms}")

        # check if the currently best heap item is a solution
        heap_item: HeapItem = heap[0]
        if check_if_solved(abstract_arc_task, heap_item):
            return heap_item.transforms, visited, step

        # update the heap with one step
        heap, visited = mdl_search_step(abstract_arc_task, heap, primitive_transformations, visited, eval_features,
                                        statistics, conditions)
        step += 1
        if len(heap) > beam_width:  # limit heap to beam_width
            optima = heapq.nsmallest(beam_width, heap)
            heapq.heapify(optima)
            heap = optima

    return None, visited, step


def transform_eval_matrix_pair_conditioned(abstract_matrix_pair: AbstractMatrixPair,
                                           parameterized_transformation: Transformation,
                                           parameter: Optional[TransformationParameter],
                                           eval_features: list[Feature],
                                           statistics: list[SummaryStatistic],
                                           conditions: list[Condition]):
    manipulatable_input_matrix = copy.deepcopy(abstract_matrix_pair.input)  # manipulatable copy
    output_matrix = abstract_matrix_pair.output  # non manipulatable output for comparison
    matrix_shape = manipulatable_input_matrix.height, manipulatable_input_matrix.width
    positive_change = []
    negative_change = []
    scores = []

    if check_for_object_mapping(abstract_matrix_pair, eval_features):  # per object transformation and evaluation
        for input_obj_idx, output_obj_idx in abstract_matrix_pair.mapping.items():
            input_obj = manipulatable_input_matrix.abstract_objects[
                input_obj_idx]  # no copy for manipulatable input object since it should transform the manipulatable matrix
            output_obj = output_matrix.abstract_objects[output_obj_idx]
            current_score = evaluate_abstract_object_pair(input_obj, output_obj, eval_features,
                                                          abstract_matrix_pair)  # evaluate before transform
            parameterized_transformation.transform_abstract_object(input_obj, parameter)  # transform single object
            new_score = evaluate_abstract_object_pair(input_obj, output_obj, eval_features,
                                                      abstract_matrix_pair)  # evaluate after transform
            scores.append(new_score)
            if new_score > current_score:  # object transformation had a positive effect
                positive_change.append(input_obj)
            else:  # object transformation had a negative or no effect
                negative_change.append(input_obj)

    else:  # summary stat evaluation
        manipulatable_pair = AbstractMatrixPair(manipulatable_input_matrix, output_matrix)
        for input_obj in manipulatable_input_matrix.abstract_objects:
            current_score = sumstat_eval_abstract_matrix_pair(manipulatable_pair, statistics)  # current matrix score
            parameterized_transformation.transform_abstract_object(input_obj, parameter)  # transform single object
            new_score = sumstat_eval_abstract_matrix_pair(manipulatable_pair, statistics)  # new matrix score
            scores.append(new_score)
            if new_score > current_score:  # object manipulation had a positive effect on matrix score
                positive_change.append(input_obj)
            else:  # object manipulation had a negative or no effect on matrix score
                negative_change.append(input_obj)

    matrix_pair_score = np.mean(scores)
    possible_conditions = [
        result
        for condition in conditions
        for result in condition.explains_grouping(positive_change, negative_change)
    ]

    return possible_conditions, matrix_pair_score, manipulatable_input_matrix


def transform_eval_matrix_pair(abstract_matrix_pair: AbstractMatrixPair,
                               transformation: Transformation,
                               parameter: Optional[TransformationParameter],
                               eval_features: list[Feature],
                               statistics: list[SummaryStatistic]):
    manipulatable_input_matrix = copy.deepcopy(abstract_matrix_pair.input)  # manipulatable input matrix
    transformation.transform_abstract_matrix(manipulatable_input_matrix,
                                             parameter)  # transform manipulatable input matrix
    transformed_matrix_pair = AbstractMatrixPair(manipulatable_input_matrix, abstract_matrix_pair.output,
                                                 abstract_matrix_pair.mapping)
    if eval_features and check_for_object_mapping(transformed_matrix_pair, eval_features):  # per object evaluation
        score = obj_eval_abstract_matrix_pair(transformed_matrix_pair, eval_features)
    elif statistics:  # Summary stat evaluation
        score = sumstat_eval_abstract_matrix_pair(transformed_matrix_pair, statistics)
    else:  # no evaluation possible
        score = 0

    return score, manipulatable_input_matrix


def check_for_object_mapping(abstract_matrix_pair: AbstractMatrixPair, eval_features: list[Feature]):
    if not abstract_matrix_pair.mapping:  # no existing pairing?
        abstract_matrix_pair.mapping = create_object_mapping(abstract_matrix_pair,
                                                             eval_features)  # try to establish pairing and safe to Matrix-Pair
        if not abstract_matrix_pair.mapping:  # still not existing?
            return False
    return True
