from typing import Optional

from Datatypes.Abstract_ARC_Task import AbstractObjectMatrix
from Datatypes.Primitive_Datatypes import Direction
from Transformations.Transformation import Transformation, TransformationParameter
from Transformations.Primitive_Transformations import translate
from Conditionals.Condition import *

class TranslateParameter(TransformationParameter):

    def __init__(self, direction: Direction):
        self.direction = direction

    @classmethod
    def possible_values(cls) -> list['TranslateParameter']:
        return [cls(c) for c in Direction]

    def __repr__(self):
        return self.direction.name


class Translate(Transformation):
    parameters = TranslateParameter.possible_values()

    def __init__(self, parameter_direction: TranslateParameter = None, condition: Optional[Condition] = None):
        super().__init__(parameter_direction, condition)

    def from_parameter_condition(self, parameter: Optional[TranslateParameter] = None, condition: Optional[Condition] = None) -> 'Translate':
        return Translate(parameter, condition)

    def transform_abstract_matrix(self, abstract_matrix: AbstractObjectMatrix, parameter_direction: Optional[TranslateParameter] = None):
        if parameter_direction is None:
            if self.fixed_parameter is None:
                raise ValueError("Either direction or fixed_parameter must be specified")
            else:
                parameter_direction = self.fixed_parameter

        for abstract_object in abstract_matrix.abstract_objects:
            self.transform_abstract_object(abstract_object, parameter_direction)

    def transform_abstract_object(self, abstract_object: AbstractObject,
                                  parameter_direction: Optional[TranslateParameter] = None):
        if parameter_direction is None:
            if self.fixed_parameter is None:
                raise ValueError("Either direction or fixed_parameter must be specified")
            else:
                parameter_direction = self.fixed_parameter

        if self.condition is None or self.condition.applies_to(abstract_object):
            translate(abstract_object, parameter_direction.direction)

