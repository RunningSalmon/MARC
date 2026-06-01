from typing import Optional

from Datatypes.Abstract_ARC_Task import AbstractObjectMatrix
from Datatypes.Primitive_Datatypes import ArcColor
from Transformations.Rotate import RotationParameter
from Transformations.Transformation import Transformation, TransformationParameter
from Transformations.Primitive_Transformations import recolor
from Conditionals.Condition import *

class RecolorParameter(TransformationParameter):

    def __init__(self, color: ArcColor):
        if color == ArcColor.Black:
            raise ValueError("Black is not a valid color for recoloring")
        self.color = color

    @classmethod
    def possible_values(cls) -> list['RecolorParameter']:
        return [cls(c) for c in ArcColor if c != ArcColor.Black]

    def __repr__(self):
        return self.color.name

class Recolor(Transformation):
    parameters = RecolorParameter.possible_values()

    def __init__(self, parameter_color: Optional[RecolorParameter] = None, condition: Optional[Condition] = None):
        super().__init__(parameter_color, condition)

    def from_parameter_condition(self, parameter: Optional[RotationParameter] = None, condition: Optional[Condition] = None) -> 'Recolor':
        return Recolor(parameter, condition)

    def transform_abstract_matrix(self, abstract_matrix: AbstractObjectMatrix, parameter_color: Optional[RecolorParameter] = None):
        if parameter_color is None:
            if self.fixed_parameter is None:
                raise ValueError("Either color or fixed_parameter must be specified")
            else:
                parameter_color = self.fixed_parameter

        for abstract_object in abstract_matrix.abstract_objects:
            self.transform_abstract_object(abstract_object, parameter_color)

    def transform_abstract_object(self, abstract_object: AbstractObject, parameter_color: Optional[RecolorParameter] = None):
        if parameter_color is None:
            if self.fixed_parameter is None:
                raise ValueError("Either color or fixed_parameter must be specified")
            else:
                parameter_color = self.fixed_parameter

        if self.condition is None or self.condition.applies_to(abstract_object):
            recolor(abstract_object, parameter_color.color)



