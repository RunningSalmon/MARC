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