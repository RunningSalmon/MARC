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
    def __init__(self, mdl: float, transforms: list[Transformation]):
        self.mdl = mdl
        self.transforms = transforms

    def __lt__(self, other):
        return self.mdl < other.mdl

def initialize_mdl_search(abstract_matrix_pair: AbstractObjectMatrixPair, transformations: list[Transformation], eval_features: list[Feature]):
    input_matrix = abstract_matrix_pair.input
    output_matrix = abstract_matrix_pair.output
    if not abstract_matrix_pair.pairing:
        abstract_matrix_pair.pairing = create_object_pairing(abstract_matrix_pair)
    object_pairing = abstract_matrix_pair.pairing

    heap = []
    primitive_transformations = []

    for transformation in transformations:
        params = transformation.parameters
        nll = transformation.get_nll(len(transformations))
        for param in params:
            anticipatory_input_matrix = copy.deepcopy(input_matrix)
            transformation.transform(anticipatory_input_matrix, param)
            anticipatory_pair = AbstractObjectMatrixPair(anticipatory_input_matrix, output_matrix, object_pairing)
            score = evaluate_abstract_matrix_pair(anticipatory_pair, eval_features)
            if score != 0:
                mdl = nll * (1-score)
                heapq.heappush(heap, HeapItem(mdl, [transformation.from_parameter(param)]))
                primitive_transformations.append(transformation.from_parameter(param))

    return heap, primitive_transformations

def mdl_search_step(abstract_matrix_pair: AbstractObjectMatrixPair, heap: list, primitive_transformations: list, visited: set, eval_features: list[Feature]):

    input_matrix = abstract_matrix_pair.input
    output_matrix = abstract_matrix_pair.output
    object_pairing = abstract_matrix_pair.pairing

    item = heapq.heappop(heap)
    transforms = item.transforms

    #hash sequence and check if already applied
    key = tuple(repr(t) for t in transforms)
    if key in visited:
        return heap
    visited.add(key)

    transformed_matrix = copy.deepcopy(input_matrix)
    for transformation in transforms:
        transformation.transform(transformed_matrix)

    #print(transformed_matrix,"\n", output_matrix)
    #print(transformed_matrix.to_matrix(), "\n\n", output_matrix.to_matrix)

    if transformed_matrix == output_matrix:
        return heap, visited, transforms

    for transformation in primitive_transformations:
        nll = transformation.get_nll(len(primitive_transformations))
        anticipatory_matrix = copy.deepcopy(transformed_matrix)
        transformation.transform(anticipatory_matrix)
        anticipatory_pair = AbstractObjectMatrixPair(anticipatory_matrix, output_matrix, object_pairing)
        score = evaluate_abstract_matrix_pair(anticipatory_pair, eval_features)

        if score != 0:
            mdl = nll * (1-score)
            accumulated_transforms = transforms + [transformation]
            heapq.heappush(heap, HeapItem(mdl, accumulated_transforms))

    if len(heap) > beam_width:
        optima = heapq.nsmallest(beam_width, heap)
        heapq.heapify(optima)
        heap = optima

    return heap, visited, None

def mdl_search(abstract_matrix_pair: AbstractObjectMatrixPair, transformations: list[Transformation], eval_features: list[Feature]):
    heap, primitive_transformations = initialize_mdl_search(abstract_matrix_pair, transformations, eval_features)
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
            heap, visited, solution = mdl_search_step(abstract_matrix_pair, heap, primitive_transformations, visited, eval_features)
        else:
            return solution, visited

    return None, visited