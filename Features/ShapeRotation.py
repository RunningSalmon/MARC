from typing import Optional

from Datatypes.Abstract_ARC_Task import AbstractObjectMatrix, AbstractObjectMatrixPair
from Datatypes.Abstract_Object import AbstractObject
from Datatypes.Primitive_Datatypes import Degree
from Features.Feature import Feature
from Transformations.Primitive_Transformations import rotate
from Evaluation.Eval_Features import eval_rotated_shape


class ShapeRotation(Feature):
    degree: Optional[Degree]

    nr_of_algos = 3

    def __init__(self, degree: Optional[Degree] = None):
        self.degree = degree

    def __repr__(self):
        return f"Feature 'Rotation' with parameter: {self.degree}"

    def transform(self, abstract_matrix: AbstractObjectMatrix):
        if self.degree is None:
            raise ValueError("cannot invoke transform without parameterization")

        for abstract_object in abstract_matrix.abstract_objects:
            rotate(abstract_object, self.degree)

    def get_fitness(self, obj_1: AbstractObject, obj_2: AbstractObject):
        return eval_rotated_shape(obj_1, obj_2)
