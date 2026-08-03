from typing import Optional

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
    def __init__(self, parameter_color: Optional[ConditionColorParameter] = None):
        super().__init__(parameter_color)

    def applies_to(self, abstract_object: AbstractObject) -> bool:
        if self.fixed_parameter is None:
            raise ValueError("ConditionColor has no parameter for application")
        return abstract_object.Color == self.fixed_parameter

    def explains_grouping(self, affected_group: list[AbstractObject], unaffected_group: list[AbstractObject]) -> list[
        'ConditionColor']:
        if not affected_group or not unaffected_group:
            return []
        affected_color = affected_group[0].Color
        for obj in affected_group:
            if obj.Color != affected_color:
                return []
        for obj in unaffected_group:
            if obj.Color == affected_color:
                return []
        return [ConditionColor(ConditionColorParameter(affected_color))]
