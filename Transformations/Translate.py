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
    matrix_height: int
    matrix_width: int
    parameters = TranslateParameter.possible_values()

    def __init__(self, matrix_height: int, matrix_width: int, parameter_direction: TranslateParameter = None):
        self.matrix_height = matrix_height
        self.matrix_width = matrix_width
        super().__init__(parameter_direction)

    def from_parameter(self, parameter: Optional[TranslateParameter] = None) -> 'Translate':
        return Translate(self.matrix_height, self.matrix_width, parameter)

    def transform(self, abstract_matrix: AbstractObjectMatrix, parameter_direction: Optional[TranslateParameter] = None):
        if parameter_direction is None:
            if self.fixed_parameter is None:
                raise ValueError("Either direction or fixed_parameter must be specified")
            else:
                parameter_direction = self.fixed_parameter

        if parameter_direction not in self.parameters:
            raise ValueError(f"{parameter_direction} is not a valid direction for translate")

        for abstract_object in abstract_matrix.abstract_objects:
            translate(abstract_object, parameter_direction.direction)

