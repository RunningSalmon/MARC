from typing import Optional

from Datatypes.Abstract_ARC_Task import AbstractObjectMatrix, AbstractObjectMatrixPair
from Datatypes.Abstract_Object import AbstractObject
from Datatypes.Primitive_Datatypes import Direction
from Features.Feature import Feature
from Transformations.Primitive_Transformations import duplicate
from Evaluation.Eval_Features import eval_shape_duplicated


class ShapeDuplication(Feature):
    direction: Optional[Direction]

    nr_of_algos = 4

    def __init__(self, direction: Optional[Direction] = None):
        self.direction = direction

    def __repr__(self):
        return f"Feature 'Duplicate' with parameter: {self.direction}"

    def transform(self, abstract_matrix: AbstractObjectMatrix):
        if self.direction is None:
            raise ValueError("cannot invoke transform without parameterization")
        for abstract_object in abstract_matrix.abstract_objects:
            duplicate(abstract_object, self.direction)

    def get_fitness(self, obj_1: AbstractObject, obj_2: AbstractObject):
        return eval_shape_duplicated(obj_1, obj_2)