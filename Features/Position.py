from typing import Optional

from Datatypes.Abstract_ARC_Task import AbstractObjectMatrix, AbstractObjectMatrixPair
from Datatypes.Abstract_Object import AbstractObject
from Datatypes.Primitive_Datatypes import Direction
from Features.Feature import Feature
from Transformations.Primitive_Transformations import translate
from Evaluation.Eval_Features import eval_position


class Position(Feature):
    direction: Optional[Direction]
    matrix_height: int
    matrix_width: int

    nr_of_algos = 4

    def __init__(self, matrix_height: int, matrix_width: int, direction: Optional[Direction] = None):
        self.direction = direction
        self.matrix_height = matrix_height
        self.matrix_width = matrix_width

    def __repr__(self):
        return f"Feature 'Position' with parameter: {self.direction}"

    def transform(self, abstract_matrix: AbstractObjectMatrix):
        if self.direction is None:
            raise ValueError("cannot invoke transform without parameterization")

        for abstract_object in abstract_matrix.abstract_objects:
            translate(abstract_object, self.direction)

    def get_fitness(self, obj_1: AbstractObject, obj_2: AbstractObject):
        return eval_position(obj_1, obj_2, (self.matrix_height, self.matrix_width))
