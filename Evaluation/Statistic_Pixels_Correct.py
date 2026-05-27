import numpy as np

from Datatypes.Abstract_ARC_Task import AbstractObjectMatrixPair
from Evaluation.Summary_Statistic import SummaryStatistic


class PixelsCorrect(SummaryStatistic):
    def get_fitness(self, abstract_matrix_pair: AbstractObjectMatrixPair) -> float:
        input_matrix = abstract_matrix_pair.input.to_matrix()
        output_matrix = abstract_matrix_pair.output.to_matrix()
        pixels_correct = int(np.sum(input_matrix == output_matrix))
        return pixels_correct/input_matrix.size