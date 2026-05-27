from abc import ABC, abstractmethod

from Datatypes.Abstract_ARC_Task import AbstractObjectMatrixPair


class SummaryStatistic(ABC):
    @abstractmethod
    def get_fitness(self, abstract_matrix_pair: AbstractObjectMatrixPair) -> float:
        pass