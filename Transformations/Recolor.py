from typing import Optional

from Datatypes.Abstract_ARC_Task import AbstractObjectMatrix
from Datatypes.Primitive_Datatypes import ArcColor
from Transformations.Transformation import Transformation, FeatureParameter
from Transformations.Primitive_Transformations import recolor


class RecolorParameter(FeatureParameter):

    def __init__(self, color: ArcColor):
        if color == ArcColor.Black:
            raise ValueError("Black is not a valid color for recoloring")
        self.color = color

    @classmethod
    def possible_values(cls) -> list['RecolorParameter']:
        return [cls(c) for c in ArcColor if c != ArcColor.Black]

    def __repr__(self):
        return f"ColorParameter({self.color.name})"

class Recolor(Transformation):
    parameters = RecolorParameter.possible_values()

    def __init__(self, parameter_color: Optional[RecolorParameter] = None):
        super().__init__(parameter_color)

    def from_parameter(self, parameter: Optional[RecolorParameter] = None) -> 'Recolor':
        return Recolor(parameter)

    def transform(self, abstract_matrix: AbstractObjectMatrix, parameter_color: Optional[RecolorParameter] = None):
        if parameter_color is None:
            if self.fixed_parameter is None:
                raise ValueError("Either color or fixed_parameter must be specified")
            else:
                parameter_color = self.fixed_parameter
        for abstract_object in abstract_matrix.abstract_objects:
            recolor(abstract_object, parameter_color.color)



