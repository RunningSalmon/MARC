from math import log
from Datatypes.Abstract_ARC_Task import *
from Conditionals.Condition import *


class TransformationParameter(ABC):
    @classmethod
    @abstractmethod
    def possible_values(cls) -> list:
        pass


class Transformation(ABC):
    possible_parameters: list[TransformationParameter] = []

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
    def from_parameter_condition(self, parameter: Optional[TransformationParameter] = None,
                                 condition: Optional[Condition] = None) -> 'Transformation':
        """allows to create a transformation from a parameter and a condition"""
        pass

    @abstractmethod
    def transform_abstract_matrix(self, abstract_matrix: AbstractObjectMatrix,
                                  parameter: Optional[TransformationParameter] = None):
        """transforms all objects in the abstract matrix by the transformation with the give parameter"""
        pass

    @abstractmethod
    def transform_abstract_object(self, abstract_object: AbstractObject,
                                  parameter: Optional[TransformationParameter] = None):
        """transforms a single object by the transformation with the give parameter"""
        pass

    def get_nll(self, nr_of_algos: int, nr_of_conditions: int = 0) -> float:
        """returns the negative log likelihood of the transformation"""
        if not self.possible_parameters:
            raise ValueError("parameters are not specified")

        if self.fixed_parameter:
            parameter_nll = 0
        else:
            parameter_nll = -log(1 / len(self.possible_parameters))

        if nr_of_conditions > 0:
            condition_nll = -log(1 / nr_of_conditions)
        else:
            condition_nll = 0

        class_nll = -log(1 / nr_of_algos)

        nll = class_nll + parameter_nll + condition_nll

        return nll
