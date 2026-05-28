from Datatypes.Primitive_Datatypes import ArcColor
from .Condition import *


class ConditionColorParameter(ConditionParameter):
    def __init__(self, color: ArcColor):
        if color == ArcColor.Black:
            raise ValueError("Black is not a valid color for recoloring")
        self.color = color

    def __eq__(self, other):
        return self.color == other

    def __repr__(self):
        return self.color.name

class ConditionColor(Condition):
    def __init__(self, parameter_color: ConditionColorParameter):
        self.color_parameter = parameter_color

    def applies_to(self, abstract_object: AbstractObject) -> bool:
        return abstract_object.Color == self.color_parameter



