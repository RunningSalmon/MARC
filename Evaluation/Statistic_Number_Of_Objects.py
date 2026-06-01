from abc import ABC

from Datatypes.Abstract_ARC_Task import AbstractMatrixPair
from Evaluation.Summary_Statistic import SummaryStatistic


class NumberOfObjects(SummaryStatistic):
    def get_fitness(self, abstract_matrix_pair: AbstractMatrixPair) -> float:
        number_of_input_objects = len(abstract_matrix_pair.input.abstract_objects)
        number_of_output_objects = len(abstract_matrix_pair.output.abstract_objects)
        return min(number_of_input_objects, number_of_output_objects)/max(number_of_input_objects, number_of_output_objects)