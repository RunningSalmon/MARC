import heapq

from Datatypes.Abstract_ARC_Task import AbstractObjectMatrixPair
from Transformations.Recolor import Recolor
from Transformations.Translate import Translate
from Transformations.Duplicate import Duplicate
from Transformations.Mirror import Mirror
from Transformations.Rotate import Rotate
from Evaluation.Matrix_Pair_Evaluation import *
from Datatypes.Primitive_Datatypes import *
from Evaluation.Feature_Color import *
from Evaluation.Feature_Position import *
from Evaluation.Feature_Shape import *

def create_object_pairing(abstract_matrix_pair: AbstractObjectMatrixPair):
    input_matrix = abstract_matrix_pair.input
    output_matrix = abstract_matrix_pair.output
    matrix_height = input_matrix.height
    matrix_width = input_matrix.width
    relevant_features = [FeatureColor(),
                         FeaturePosition(),
                         FeatureShape()]
    input_objects = input_matrix.abstract_objects
    output_objects = output_matrix.abstract_objects
    input_range = range(len(input_objects))
    output_range = range(len(output_objects))
    pairing = {}
    #print(f"input objects: {len(input_objects)}, output objects: {len(output_objects)}")

    # singular pairing
    if len(input_objects) == len(output_objects):
        heap = []
        for i in input_range:
            for j in output_range:
                current_score = evaluate_abstract_object_pair(input_objects[i], output_objects[j], relevant_features, (input_matrix.height, input_matrix.width))
                heapq.heappush(heap, (-current_score, (i, j)))

        input_ids = list(input_range)
        output_ids = list(output_range)

        while len(input_ids) > 0 and len(output_ids) > 0:
            score, (i, j) = heapq.heappop(heap)
            if i in input_ids and j in output_ids:
                input_ids.remove(i)
                output_ids.remove(j)
                pairing[i] = j

        return pairing
    return {}