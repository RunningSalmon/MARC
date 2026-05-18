from Datatypes.Abstract_ARC_Task import AbstractObjectMatrix, AbstractObjectMatrixPair
from Datatypes.Abstract_Object import AbstractObject
from Datatypes.Primitive_Datatypes import Direction
from Features.Feature import Feature
from Transformations.Primitive_Transformations import duplicate
from Evaluation.Eval_Features import eval_shape_duplicated


class ShapeDuplication(Feature):
    direction: Direction

    def __init__(self, direction: Direction):
        self.direction = direction

    def transform(self, abstract_matrix: AbstractObjectMatrix):
        for abstract_object in abstract_matrix.abstract_objects:
            duplicate(abstract_object, self.direction)

    def get_fitness(self, obj_1: AbstractObject, obj_2: AbstractObject):
        return eval_shape_duplicated(obj_1, obj_2)