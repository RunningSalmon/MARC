from abc import ABC, abstractmethod

from icontract import ensure

from Datatypes.Abstract_ARC_Task import AbstractMatrixPair


class SummaryStatistic(ABC):
    @ensure(lambda result: 0 <= result <= 1)
    @abstractmethod
    def get_fitness(self, abstract_matrix_pair: AbstractMatrixPair) -> float:
        """
        evaluates the fitness between two matrices of an AbstractMatrixPair using summary statistics
        :returns: a score between 0 and 1
        """
        pass
