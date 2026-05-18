from Datatypes.Abstract_ARC_Task import AbstractObjectMatrix, AbstractObjectMatrixPair
from Datatypes.Abstract_Object import AbstractObject
from Datatypes.Primitive_Datatypes import ArcColor
from Features.Feature import Feature
from Transformations.Primitive_Transformations import recolor
from Evaluation.Eval_Features import eval_color


class Color(Feature):
    color_value: ArcColor

    def __init__(self, color_value: ArcColor):
        self.color_value = color_value

    def transform(self, abstract_matrix: AbstractObjectMatrix):
        for abstract_object in abstract_matrix.abstract_objects:
            recolor(abstract_object, self.color_value)

    def get_fitness(self, obj_1: AbstractObject, obj_2: AbstractObject):
        return eval_color(obj_1, obj_2)