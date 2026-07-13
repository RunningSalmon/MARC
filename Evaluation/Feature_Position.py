from typing import override

from Evaluation.Feature import *

class FeaturePosition(Feature):
    matrix_shape: tuple[int,int]

    @ensure(lambda result: 0 <= result <= 1)
    def evaluate_objects(self, abstract_object_1: AbstractObject, abstract_object_2: AbstractObject,
                         abstract_matrix_pair: AbstractMatrixPair) -> float:
        input_matrix = abstract_matrix_pair.input
        output_matrix = abstract_matrix_pair.output
        all_objects = (input_matrix.abstract_objects + output_matrix.abstract_objects
                       + [abstract_object_1, abstract_object_2])

        max_x = max(obj.Position_X for obj in all_objects)
        max_y = max(obj.Position_Y for obj in all_objects)
        min_x = min(obj.Position_X for obj in all_objects)
        min_y = min(obj.Position_Y for obj in all_objects)

        max_possible_distance = np.linalg.norm((max_y - min_y, max_x - min_x))

        distance = np.linalg.norm((abstract_object_2.Position_Y - abstract_object_1.Position_Y,
                                   abstract_object_2.Position_X - abstract_object_1.Position_X))

        if max_possible_distance == 0:
            return 1.0

        return float(1 - distance / max_possible_distance)
