from enum import Enum
from hmac import compare_digest
from typing import Optional

from Datatypes.Primitive_Datatypes import Axis, SmallerOrLarger
from .Condition import *

class ConditionPositionParameter(ConditionParameter):
    def __init__(self, threshold: int, axis: Axis, comparator: SmallerOrLarger):
        self.threshold = threshold
        self.axis = axis
        self.comparator = comparator

    def __repr__(self):
        return f"all positions {self.comparator.name} than {self.threshold} on the {self.axis.name} axis"

class ConditionPosition(Condition):
    def __init__(self, parameter_position: Optional[ConditionPositionParameter] = None):
        super().__init__(parameter_position)

    def applies_to(self, abstract_object: AbstractObject):
        if self.fixed_parameter is None:
            raise ValueError("ConditionPosition has no parameter for application")
        object_position = abstract_object.Position_Y if self.fixed_parameter.axis == Axis.Vertical else abstract_object.Position_X
        if self.fixed_parameter.comparator == SmallerOrLarger.smaller:
            return object_position <= self.fixed_parameter.threshold
        else:
            return object_position >= self.fixed_parameter.threshold

    def explains_grouping(self, affected_group: list[AbstractObject], unaffected_group: list[AbstractObject]) -> list['ConditionPosition']:
        if not affected_group or not unaffected_group:
            return []
        possible_explanations = []

        min_x_affected = min(affected_obj.Position_X for affected_obj in affected_group)
        min_y_affected = min(affected_obj.Position_Y for affected_obj in affected_group)
        max_x_affected = max(affected_obj.Position_X for affected_obj in affected_group)
        max_y_affected = max(affected_obj.Position_Y for affected_obj in affected_group)

        min_x_unaffected = min(unaffected_obj.Position_X for unaffected_obj in unaffected_group)
        min_y_unaffected = min(unaffected_obj.Position_Y for unaffected_obj in unaffected_group)
        max_x_unaffected = max(unaffected_obj.Position_X for unaffected_obj in unaffected_group)
        max_y_unaffected = max(unaffected_obj.Position_Y for unaffected_obj in unaffected_group)

        if min_x_affected > max_x_unaffected: #all objects have x_unaffected > x >= x_affected
            possible_explanations.append(
                ConditionPosition(ConditionPositionParameter(min_x_affected, Axis.Horizontal, SmallerOrLarger.larger)))

        if min_y_affected > max_y_unaffected: #all objects have y_unaffected > y >= y_affected
            possible_explanations.append(
                ConditionPosition(ConditionPositionParameter(min_y_affected, Axis.Vertical, SmallerOrLarger.larger)))

        if max_x_affected < min_x_unaffected:  # all objects have x_affected <= x < x_unaffected
            possible_explanations.append(
                ConditionPosition(ConditionPositionParameter(max_x_affected, Axis.Horizontal, SmallerOrLarger.smaller)))

        if max_y_affected < min_y_unaffected:  # all objects have y_affected <= y < y_unaffected
            possible_explanations.append(
                ConditionPosition(ConditionPositionParameter(max_y_affected, Axis.Vertical, SmallerOrLarger.smaller)))

        return possible_explanations