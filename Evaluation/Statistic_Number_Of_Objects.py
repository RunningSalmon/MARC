from abc import ABC

from Datatypes.Abstract_ARC_Task import AbstractMatrixPair
from Evaluation.Summary_Statistic import SummaryStatistic


class NumberOfObjects(SummaryStatistic):
    def get_fitness(self, abstract_matrix_pair: AbstractMatrixPair) -> float:
        number_of_input_objects = count_visible_objects(abstract_matrix_pair.input)
        number_of_output_objects = count_visible_objects(abstract_matrix_pair.output)
        if max(number_of_input_objects, number_of_output_objects) == 0:
            return 1
        return min(number_of_input_objects, number_of_output_objects) / max(number_of_input_objects, number_of_output_objects)


def count_visible_objects(abstract_matrix) -> int:
    count = 0
    for obj in abstract_matrix.abstract_objects:
        obj_h, obj_w = obj.Shape_Matrix.shape
        x, y = obj.Position_X, obj.Position_Y
        if (x < abstract_matrix.width and y < abstract_matrix.height and
                x + obj_w > 0 and y + obj_h > 0):
            count += 1
    return count