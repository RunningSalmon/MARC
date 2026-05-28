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
    parameters = DuplicationParameter.possible_values()

    def __init__(self, direction: DuplicationParameter = None, condition: Optional[Condition] = None):
        super().__init__(direction, condition)

    def from_parameter(self, parameter: Optional[DuplicationParameter] = None) -> 'Duplicate':
        return Duplicate(parameter)

    def transform(self, abstract_matrix: AbstractObjectMatrix, direction: Optional[DuplicationParameter] = None):
        if direction is None:
            if self.fixed_parameter is None:
                raise ValueError("Either direction or fixed_parameter must be specified")
            else:
                direction = self.fixed_parameter

        for abstract_object in abstract_matrix.abstract_objects:
            if self.condition is None or self.condition.applies_to(abstract_object):
                duplicate(abstract_object, direction.direction)
