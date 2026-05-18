from abc import ABC, abstractmethod

from Datatypes import Abstract_ARC_Task
from Transformations.Primitive_Transformations import *
from Datatypes.Abstract_ARC_Task import *
from Evaluation.Eval_Features import *

class Feature(ABC):
    @abstractmethod
    def transform(self, abstract_matrix: AbstractObjectMatrix):
        pass
    @abstractmethod
    def get_fitness(self, abstract_matrix_pair: AbstractObjectMatrixPair):
        pass