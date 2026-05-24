from typing import Optional

from Datatypes.Abstract_ARC_Task import AbstractObjectMatrix
from Datatypes.Primitive_Datatypes import Axis
from Transformations.Transformation import Transformation, FeatureParameter
from Transformations.Primitive_Transformations import mirror

class MirrorParameter(FeatureParameter):

    def __init__(self, axis: Axis):
        self.axis = axis

    @classmethod
    def possible_values(cls) -> list['MirrorParameter']:
        return [cls(c) for c in Axis]

    def __repr__(self):
        return f"MirrorParameter({self.axis.name})"

class Mirror(Transformation):
    parameters = MirrorParameter.possible_values()

    def __init__(self, parameter_axis: MirrorParameter = None):
        super().__init__(parameter_axis)

    def from_parameter(self, parameter: Optional[MirrorParameter] = None) -> 'Mirror':
        return Mirror(parameter)

    def transform(self, abstract_matrix: AbstractObjectMatrix, parameter_axis: Optional[MirrorParameter] = None):
        if parameter_axis is None:
            if self.fixed_parameter is None:
                raise ValueError("Either axis or fixed_parameter must be specified")
            else:
                parameter_axis = self.fixed_parameter

        for abstract_object in abstract_matrix.abstract_objects:
            mirror(abstract_object, parameter_axis.axis)

