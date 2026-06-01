from typing import Optional

from Datatypes.Abstract_ARC_Task import AbstractObjectMatrix
from Datatypes.Primitive_Datatypes import Degree
from Transformations.Transformation import Transformation, TransformationParameter
from Transformations.Primitive_Transformations import rotate
from Conditionals.Condition import *

class RotationParameter(TransformationParameter):

    def __init__(self, degree: Degree):
        self.degree = degree

    @classmethod
    def possible_values(cls) -> list['RotationParameter']:
        return [cls(c) for c in Degree]

    def __repr__(self):
        return self.degree.name

class Rotate(Transformation):
    parameters = RotationParameter.possible_values()

    def __init__(self, parameter_degree: RotationParameter = None, condition: Optional[Condition] = None):
        super().__init__(parameter_degree, condition)

    def from_parameter_condition(self, parameter: Optional[RotationParameter] = None, condition: Optional[Condition] = None) -> 'Rotate':
        return Rotate(parameter, condition)

    def transform_abstract_matrix(self, abstract_matrix: AbstractObjectMatrix, parameter_degree: Optional[RotationParameter] = None):
        if parameter_degree is None:
            if self.fixed_parameter is None:
                raise ValueError("Either degree or fixed_parameter must be specified")
            else:
                parameter_degree = self.fixed_parameter

        for abstract_object in abstract_matrix.abstract_objects:
            if self.condition is None or self.condition.applies_to(abstract_object):
                self.transform_abstract_object(abstract_object, parameter_degree)

    def transform_abstract_object(self, abstract_object: AbstractObject, parameter_degree: Optional[RotationParameter] = None):
        if parameter_degree is None:
            if self.fixed_parameter is None:
                raise ValueError("Either degree or fixed_parameter must be specified")
            else:
                parameter_degree = self.fixed_parameter

        if self.condition is None or self.condition.applies_to(abstract_object):
            rotate(abstract_object, parameter_degree.degree)
