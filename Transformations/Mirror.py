from typing import Optional

from Datatypes.Abstract_ARC_Task import AbstractObjectMatrix
from Datatypes.Primitive_Datatypes import Axis
from Transformations.Transformation import Transformation, TransformationParameter
from Transformations.Primitive_Transformations import mirror
from Conditionals.Condition import *


class MirrorParameter(TransformationParameter):

    def __init__(self, axis: Axis):
        self.axis = axis

    @classmethod
    def possible_values(cls) -> list['MirrorParameter']:
        return [cls(c) for c in Axis]

    def __repr__(self):
        return self.axis.name + " axis"


class Mirror(Transformation):
    possible_parameters = MirrorParameter.possible_values()

    def __init__(self, parameter_axis: MirrorParameter = None, condition: Optional[Condition] = None):
        super().__init__(parameter_axis, condition)

    def from_parameter_condition(self, parameter: Optional[MirrorParameter] = None,
                                 condition: Optional[Condition] = None) -> 'Mirror':
        return Mirror(parameter, condition)

    def transform_abstract_matrix(self, abstract_matrix: AbstractObjectMatrix,
                                  parameter_axis: Optional[MirrorParameter] = None):
        if parameter_axis is None:
            if self.fixed_parameter is None:
                raise ValueError("Either axis or fixed_parameter must be specified")
            else:
                parameter_axis = self.fixed_parameter

        for abstract_object in abstract_matrix.abstract_objects:
            self.transform_abstract_object(abstract_object, parameter_axis)

    def transform_abstract_object(self, abstract_object: AbstractObject,
                                  parameter_axis: Optional[MirrorParameter] = None):
        if parameter_axis is None:
            if self.fixed_parameter is None:
                raise ValueError("Either axis or fixed_parameter must be specified")
            else:
                parameter_axis = self.fixed_parameter

        if self.condition is None or self.condition.applies_to(abstract_object):
            mirror(abstract_object, parameter_axis.axis)
