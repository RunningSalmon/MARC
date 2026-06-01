from abc import ABC, abstractmethod
from math import log
from typing import Optional

from Datatypes.Abstract_ARC_Task import *
from Conditionals.Condition import *


class TransformationParameter(ABC):
    @classmethod
    @abstractmethod
    def possible_values(cls) -> list:
        pass

class Transformation(ABC):
    parameters: list[TransformationParameter] = []

    @abstractmethod
    def __init__(self, parameter: Optional[TransformationParameter] = None, condition: Condition = None):
        self.fixed_parameter = parameter
        if condition:
            self.condition = condition
        else:
            self.condition = None

    def __repr__(self):
        return f"Transformation '{type(self).__name__}' with fixed parameter: {self.fixed_parameter} and condition: {self.condition}"

    @abstractmethod
    def from_parameter_condition(self, parameter: Optional[TransformationParameter] = None, condition: Optional[Condition] = None) -> 'Transformation':
        pass

    @abstractmethod
    def transform_abstract_matrix(self, abstract_matrix: AbstractObjectMatrix, parameter: Optional[TransformationParameter] = None):
        pass

    @abstractmethod
    def transform_abstract_object(self, abstract_object: AbstractObject, parameter: Optional[TransformationParameter] = None):
        pass

    def get_nll(self, nr_of_algos: int) -> float:
        if not self.parameters:
            raise ValueError("parameters are not specified")

        class_nll = -log(1/nr_of_algos)
        if self.fixed_parameter:
            parameter_nll = 0
        else:
            parameter_nll = -log(1/len(self.parameters))

        return class_nll #+ parameter_nll