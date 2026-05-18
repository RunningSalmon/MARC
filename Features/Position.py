from Datatypes.Abstract_ARC_Task import AbstractObjectMatrix, AbstractObjectMatrixPair
from Datatypes.Abstract_Object import AbstractObject
from Datatypes.Primitive_Datatypes import Direction
from Features.Feature import Feature
from Transformations.Primitive_Transformations import translate
from Evaluation.Eval_Features import eval_position


class Position(Feature):
    direction: Direction
    matrix_height: int
    matrix_width: int

    def __init__(self, direction: Direction, matrix_height: int, matrix_width: int):
        self.direction = direction
        self.matrix_height = matrix_height
        self.matrix_width = matrix_width

    def transform(self, abstract_matrix: AbstractObjectMatrix):
        for abstract_object in abstract_matrix.abstract_objects:
            translate(abstract_object, self.direction)

    def get_fitness(self, obj_1: AbstractObject, obj_2: AbstractObject):
        return eval_position(obj_1, obj_2, (self.matrix_height, self.matrix_width))
