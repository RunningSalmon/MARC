import heapq

from Datatypes.Abstract_ARC_Task import AbstractObjectMatrixPair
from Features.Color import Color
from Features.Position import Position
from Features.ShapeDuplication import ShapeDuplication
from Features.ShapeMirror import ShapeMirror
from Features.ShapeRotation import ShapeRotation
from Evaluation.Evaluation import *
from Datatypes.Primitive_Datatypes import *

def create_object_pairing(abstract_matrix_pair: AbstractObjectMatrixPair):
    input_matrix = abstract_matrix_pair.input
    output_matrix = abstract_matrix_pair.output
    matrix_height = input_matrix.height
    matrix_width = input_matrix.width
    relevant_features = [Color(ArcColor.Black),
                         Position(Direction.Up, matrix_height, matrix_width),
                         ShapeDuplication(Direction.Up),
                         ShapeMirror(Axis.Horizontal),
                         ShapeRotation(Degree.Deg90)]
    input_objects = input_matrix.abstract_objects
    output_objects = output_matrix.abstract_objects
    input_range = range(len(input_objects))
    output_range = range(len(output_objects))
    pairing = {}

    # singular pairing
    if len(input_objects) == len(output_objects):
        heap = []
        for i in input_range:
            for j in output_range:
                current_score = evaluate_abstract_objects_pair(output_objects[i], input_objects[j], relevant_features)
                heapq.heappush(heap, (-current_score, (i, j)))

        input_ids = list(input_range)
        output_ids = list(output_range)

        while len(input_ids) > 0 and len(output_ids) > 0:
            score, (input_id, output_id) = heapq.heappop(heap)
            if input_id in input_ids and output_id in output_ids:
                input_ids.remove(input_id)
                output_ids.remove(output_id)
                pairing[input_id] = output_id
                print(score)

        return pairing
    return {}