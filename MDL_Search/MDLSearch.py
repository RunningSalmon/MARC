import copy
import heapq

from Datatypes.Abstract_ARC_Task import AbstractObjectMatrixPair
from Evaluation.Object_Pairing import create_object_pairing
from Transformations.Transformation import *
from Evaluation.Matrix_Pair_Evaluation import *
from Datatypes.ARC_Task import *
from Evaluation.Feature import *

beam_width = 30

class HeapItem:
    def __init__(self, mdl: float, transforms: list[Transformation], transformed_matrices: list[AbstractObjectMatrix]):
        self.mdl = mdl
        self.transforms = transforms
        self.transformed_matrices = transformed_matrices

    def __lt__(self, other):
        return self.mdl < other.mdl

def initialize_mdl_search(abstract_arc_task: AbstractARCTask, transformations: list[Transformation], eval_features: list[Feature]):
    training_pairs = abstract_arc_task.train
    heap = []
    primitive_transformations = []

    for transformation in transformations: #iterate over transformations
        params = transformation.parameters
        nll = transformation.get_nll(len(transformations))
        for param in params: #iterate over parameterization for transformations
            transform_param_score = 0
            transformed_matrices = []
            for abstract_matrix_pair in training_pairs: #iterate over trials
                input_matrix = abstract_matrix_pair.input
                output_matrix = abstract_matrix_pair.output
                if not abstract_matrix_pair.pairing: #establish pairing if not yet existing
                    abstract_matrix_pair.pairing = create_object_pairing(abstract_matrix_pair)
                object_pairing = abstract_matrix_pair.pairing

                anticipatory_input_matrix = copy.deepcopy(input_matrix) #create manipulatable copy of the input matrix
                transformation.transform(anticipatory_input_matrix, param) #apply current transformation with current parameter
                transformed_matrices.append(anticipatory_input_matrix)
                anticipatory_pair = AbstractObjectMatrixPair(anticipatory_input_matrix, output_matrix, object_pairing)
                score = evaluate_abstract_matrix_pair(anticipatory_pair, eval_features) #compare to output matrix
                transform_param_score += score #add to the accumulated transform(param) score

            mean_transform_param_score = transform_param_score / len(params)
            mdl = nll * (1-mean_transform_param_score)
            heapq.heappush(heap, HeapItem(mdl, [transformation.from_parameter(param)], transformed_matrices))
            primitive_transformations.append(transformation.from_parameter(param))

    return heap, primitive_transformations

def mdl_search_step(abstract_matrix_pair: AbstractARCTask, heap: list, primitive_transformations: list, visited: set, eval_features: list[Feature]):
    training_pairs = abstract_matrix_pair.train
    item: HeapItem = heapq.heappop(heap)
    transforms = item.transforms

    # check if sequence already visited else append to visited
    key = tuple(repr(transform) for transform in transforms)
    if key in visited:
        return heap, visited, None
    visited.add(key)

    transformed_matrices = item.transformed_matrices
    transformation_series_mdl = item.mdl
    solved = True
    transform_score = 0

    for transformation in primitive_transformations:
        anticipatory_matrices = []
        for i, abstract_matrix_pair in enumerate(training_pairs):
            transformed_matrix = transformed_matrices[i]
            output_matrix = abstract_matrix_pair.output
            object_pairing = abstract_matrix_pair.pairing

            if transformed_matrix != output_matrix:
                solved = False

            anticipatory_matrix = copy.deepcopy(transformed_matrix)
            transformation.transform(anticipatory_matrix)
            anticipatory_pair = AbstractObjectMatrixPair(anticipatory_matrix, output_matrix, object_pairing)
            transform_score += evaluate_abstract_matrix_pair(anticipatory_pair, eval_features)
            anticipatory_matrices.append(anticipatory_matrix)

        mean_transform_score = transform_score / len(training_pairs)
        nll = transformation.get_nll(len(primitive_transformations))
        mdl = nll * (1 - mean_transform_score)
        accumulated_transforms = transforms + [transformation]
        heapq.heappush(heap, HeapItem(mdl, accumulated_transforms, anticipatory_matrices))

    if solved:
        return heap, visited, transforms

    return heap, visited, None

def mdl_search(abstract_arc_task: AbstractARCTask, transformations: list[Transformation], eval_features: list[Feature]):
    heap, primitive_transformations = initialize_mdl_search(abstract_arc_task, transformations, eval_features)
    visited = set()

    # debug
    print_heap = copy.deepcopy(heap)
    while print_heap:
        item = heapq.heappop(print_heap)
        print(f"score: {item.mdl}, transforms: {item.transforms}")

    solution = None
    while heap:
        #item = heapq.heappop(heap)
        #print(f"score: {item.mdl}, transforms: {item.transforms}")

        if solution is None:
            heap, visited, solution = mdl_search_step(abstract_arc_task, heap, primitive_transformations, visited, eval_features)
            if len(heap) > beam_width: #limit heap to beam_width
                optima = heapq.nsmallest(beam_width, heap)
                heapq.heapify(optima)
                heap = optima
        else:
            return solution, visited

    return None, visited