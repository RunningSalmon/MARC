from Datatypes.Abstract_ARC_Task import AbstractObjectMatrixPair, AbstractObjectMatrix
from Evaluation.Summary_Statistic import SummaryStatistic
import numpy as np


class NumberOfEdges(SummaryStatistic):
    def get_fitness(self, abstract_matrix_pair: AbstractObjectMatrixPair) -> float:
        input_matrix = abstract_matrix_pair.input.to_matrix()
        output_matrix = abstract_matrix_pair.output.to_matrix()
        input_edges = get_number_of_edges(input_matrix)
        output_edges = get_number_of_edges(output_matrix)
        if max(input_edges, output_edges) == 0:
            return 1
        return min(input_edges, output_edges)/max(input_edges, output_edges)


def get_number_of_edges(matrix: np.ndarray) -> int:
    matrix_height = matrix.shape[0]
    matrix_width = matrix.shape[1]
    count_of_edges = 0
    for i, row in enumerate(matrix):
        for j, value in enumerate(row):
            if i > 0:
                if matrix[i-1][j] != value:
                    count_of_edges += 1
            if i < matrix_height-1:
                if matrix[i+1][j] != value:
                    count_of_edges += 1
            if j > 0:
                if matrix[i][j-1] != value:
                    count_of_edges += 1
            if j < matrix_width-1:
                if matrix[i][j+1] != value:
                    count_of_edges += 1
    return count_of_edges