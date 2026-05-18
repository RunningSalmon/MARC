from abc import ABC, abstractmethod

from Datatypes import Abstract_ARC_Task
from Transformations.Primitive_Transformations import *
from Datatypes.Abstract_ARC_Task import *
from Evaluation.Eval_Features import *

class Feature(ABC):
    @abstractmethod
    def __init__(self):
        pass
    @abstractmethod
    def transform(self, abstract_matrix: AbstractObjectMatrix):
        pass
    @abstractmethod
    def get_fitness(self, obj_1: AbstractObject, obj_2: AbstractObject):
        pass