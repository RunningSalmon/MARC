from typing import Optional

from Datatypes.Abstract_ARC_Task import AbstractObjectMatrix
from Datatypes.Primitive_Datatypes import Direction
from Transformations.Transformation import Transformation, FeatureParameter
from Transformations.Primitive_Transformations import translate

class TranslateParameter(FeatureParameter):

    def __init__(self, direction: Direction):
        self.direction = direction

    @classmethod
    def possible_values(cls) -> list['TranslateParameter']:
        return [cls(c) for c in Direction]

    def __repr__(self):
        return f"TranslateParameter({self.direction.name})"


class Translate(Transformation):
    parameters = TranslateParameter.possible_values()

    def __init__(self, parameter_direction: TranslateParameter = None):
        super().__init__(parameter_direction)

    def from_parameter(self, parameter: Optional[TranslateParameter] = None) -> 'Translate':
        return Translate(parameter)

    def transform(self, abstract_matrix: AbstractObjectMatrix, parameter_direction: Optional[TranslateParameter] = None):
        if parameter_direction is None:
            if self.fixed_parameter is None:
                raise ValueError("Either direction or fixed_parameter must be specified")
            else:
                parameter_direction = self.fixed_parameter

        for abstract_object in abstract_matrix.abstract_objects:
            translate(abstract_object, parameter_direction.direction)

