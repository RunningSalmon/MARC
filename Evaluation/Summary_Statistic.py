from abc import ABC, abstractmethod

from Datatypes.Abstract_ARC_Task import AbstractMatrixPair


class SummaryStatistic(ABC):
    @abstractmethod
    def get_fitness(self, abstract_matrix_pair: AbstractMatrixPair) -> float:
        pass