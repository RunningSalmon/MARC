from typing import Optional

from Datatypes.Abstract_ARC_Task import AbstractObjectMatrix
from Datatypes.Primitive_Datatypes import Degree
from Transformations.Transformation import Transformation, FeatureParameter
from Transformations.Primitive_Transformations import rotate

class RotationParameter(FeatureParameter):

    def __init__(self, degree: Degree):
        self.degree = degree

    @classmethod
    def possible_values(cls) -> list['RotationParameter']:
        return [cls(c) for c in Degree]

    def __repr__(self):
        return f"RotationParameter({self.degree.name})"

class Rotate(Transformation):
    parameters = RotationParameter.possible_values()

    def __init__(self, parameter_degree: RotationParameter = None):
        super().__init__(parameter_degree)

    def from_parameter(self, parameter: Optional[RotationParameter] = None) -> 'Rotate':
        return Rotate(parameter)

    def transform(self, abstract_matrix: AbstractObjectMatrix, parameter_degree: Optional[RotationParameter] = None):
        if parameter_degree is None:
            if self.fixed_parameter is None:
                raise ValueError("Either degree or fixed_parameter must be specified")
            else:
                parameter_degree = self.fixed_parameter

        for abstract_object in abstract_matrix.abstract_objects:
            rotate(abstract_object, parameter_degree.degree)

