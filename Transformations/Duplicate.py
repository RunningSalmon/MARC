from typing import Optional

from Datatypes.Abstract_ARC_Task import AbstractObjectMatrix
from Datatypes.Primitive_Datatypes import Direction
from Transformations.Transformation import Transformation, FeatureParameter
from Transformations.Primitive_Transformations import duplicate


class DuplicationParameter(FeatureParameter):

    def __init__(self, direction: Direction):
        self.direction = direction

    @classmethod
    def possible_values(cls) -> list['DuplicationParameter']:
        return [cls(c) for c in Direction]

    def __repr__(self):
        return f"DuplicationParameter({self.direction.name})"

class Duplicate(Transformation):
    parameters = DuplicationParameter.possible_values()

    def __init__(self, direction: DuplicationParameter = None):
        super().__init__(direction)

    def from_parameter(self, parameter: Optional[DuplicationParameter] = None) -> 'Duplicate':
        return Duplicate(parameter)

    def transform(self, abstract_matrix: AbstractObjectMatrix, direction: Optional[DuplicationParameter] = None):
        if direction is None:
            if self.fixed_parameter is None:
                raise ValueError("Either direction or fixed_parameter must be specified")
            else:
                direction = self.fixed_parameter

        for abstract_object in abstract_matrix.abstract_objects:
            duplicate(abstract_object, direction.direction)
