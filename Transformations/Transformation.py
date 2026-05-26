from abc import ABC, abstractmethod
from math import log
from typing import Optional

from Datatypes.Abstract_ARC_Task import *


class FeatureParameter(ABC):
    @classmethod
    @abstractmethod
    def possible_values(cls) -> list:
        pass

class Transformation(ABC):
    parameters: list[FeatureParameter] = []

    @abstractmethod
    def __init__(self, parameter: Optional[FeatureParameter] = None):
        self.fixed_parameter = parameter

    def __repr__(self):
        return f"Feature '{type(self).__name__}' with fixed parameter: {self.fixed_parameter}"

    @abstractmethod
    def from_parameter(self, parameter: Optional[FeatureParameter] = None) -> 'Transformation':
        pass

    @abstractmethod
    def transform(self, abstract_matrix: AbstractObjectMatrix, parameter: Optional[FeatureParameter] = None):
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