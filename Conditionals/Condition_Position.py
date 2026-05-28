from enum import Enum
from hmac import compare_digest

from Datatypes.Primitive_Datatypes import Axis, SmallerOrLarger
from .Condition import *

class ConditionPositionParameter(ConditionParameter):
    def __init__(self, threshold: int, axis: Axis, comparator: SmallerOrLarger):
        self.threshold = threshold
        self.axis = axis
        self.comparator = comparator

    def __repr__(self):
        return f"all positions {self.comparator} than {self.threshold} on the {self.axis} axis"

class ConditionPosition(Condition):
    def __init__(self, parameter_position: ConditionPositionParameter):
        self.position_parameter = parameter_position

    def applies_to(self, abstract_object: AbstractObject):
        object_position = abstract_object.Position_Y if self.position_parameter.axis == Axis.Vertical else abstract_object.Position_X
        if self.position_parameter.comparator == SmallerOrLarger.smaller:
            return object_position <= self.position_parameter.threshold
        else:
            return object_position >= self.position_parameter.threshold
