from typing import Optional

from Datatypes.Abstract_ARC_Task import AbstractObjectMatrix
from Datatypes.Primitive_Datatypes import Direction
from Transformations.Transformation import Transformation, TransformationParameter
from Transformations.Primitive_Transformations import duplicate
from Conditionals.Condition import *


class DuplicationParameter(TransformationParameter):

    def __init__(self, direction: Direction):
        self.direction = direction

    @classmethod
    def possible_values(cls) -> list['DuplicationParameter']:
        return [cls(c) for c in Direction]

    def __repr__(self):
        return self.direction.name

class Duplicate(Transformation):
    possible_parameters = DuplicationParameter.possible_values()

    def __init__(self, direction: DuplicationParameter = None, condition: Optional[Condition] = None):
        super().__init__(direction, condition)

    def from_parameter_condition(self, parameter: Optional[TransformationParameter] = None, condition: Optional[Condition] = None) -> 'Duplicate':
        return Duplicate(parameter, condition)

    def transform_abstract_matrix(self, abstract_matrix: AbstractObjectMatrix, parameter_direction: Optional[DuplicationParameter] = None):
        if parameter_direction is None:
            if self.fixed_parameter is None:
                raise ValueError("Either direction or fixed_parameter must be specified")
            else:
                parameter_direction = self.fixed_parameter

        for abstract_object in abstract_matrix.abstract_objects:
                self.transform_abstract_object(abstract_object, parameter_direction)

    def transform_abstract_object(self, abstract_object: AbstractObject, parameter_direction: Optional[DuplicationParameter] = None):
        if parameter_direction is None:
            if self.fixed_parameter is None:
                raise ValueError("Either direction or fixed_parameter must be specified")
            else:
                parameter_direction = self.fixed_parameter

        if self.condition is None or self.condition.applies_to(abstract_object):
            duplicate(abstract_object, parameter_direction.direction)