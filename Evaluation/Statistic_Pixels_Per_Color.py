from Datatypes.Primitive_Datatypes import ArcColor
from Summary_Statistic import *
import numpy as np


class PixelsPerColor(SummaryStatistic):
    def get_fitness(self, abstract_matrix_pair: AbstractObjectMatrixPair) -> float:
        input_matrix = abstract_matrix_pair.input.to_matrix()
        output_matrix = abstract_matrix_pair.output.to_matrix()
        overlapping_count = 0
        for color in ArcColor:
            input_count = np.sum(input_matrix == color.value)
            output_count = np.sum(output_matrix == color.value)
            overlapping_count += min(input_count, output_count)
        return float(overlapping_count/input_matrix.size)