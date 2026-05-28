from idlelib.debugobj_r import remote_object_tree_item

from .Condition import *
import numpy as np

class ConditionShapeParameter(ConditionParameter):
    def __init__(self, shape: np.ndarray):
        self.shape = shape

    def __repr__(self):
        return f"\n{self.shape}\n"

class ConditionShape(Condition):
    def __init__(self, shape_parameter: ConditionShapeParameter):
        self.shape_parameter = shape_parameter

    def applies_to(self, abstract_object: AbstractObject) -> bool:
        return np.array_equal(self.shape_parameter.shape, abstract_object.Shape_Matrix)

    def explains_grouping(self, affected_group: list[AbstractObject], unaffected_group: list[AbstractObject]) -> list['ConditionShape']:
        affected_shape = affected_group[0].Shape_Matrix
        for obj in affected_group:
            if not np.array_equal(affected_shape, obj.Shape_Matrix):
                return []
        for obj in unaffected_group:
            if np.array_equal(affected_shape, obj.Shape_Matrix):
                return []

        return [ConditionShape(ConditionShapeParameter(affected_shape))]