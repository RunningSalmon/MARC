from abc import ABC, abstractmethod
from math import log

from Datatypes import Abstract_ARC_Task
from Transformations.Primitive_Transformations import *
from Datatypes.Abstract_ARC_Task import *
from Evaluation.Eval_Features import *

class Feature(ABC):
    nr_of_params: int
    @abstractmethod
    def __init__(self):
        pass
    @abstractmethod
    def transform(self, abstract_matrix: AbstractObjectMatrix):
        pass
    @abstractmethod
    def get_fitness(self, obj_1: AbstractObject, obj_2: AbstractObject) -> float:
        pass

    def get_nll(self, nr_of_algos: int) -> float:
        if not self.nr_of_params:
            raise ValueError("The number of parameters not specified")
        return -log(1 / nr_of_algos) + -log(1 / self.nr_of_params)