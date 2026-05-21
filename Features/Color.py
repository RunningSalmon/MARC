from typing import Optional

from Datatypes.Abstract_ARC_Task import AbstractObjectMatrix
from Datatypes.Abstract_Object import AbstractObject
from Datatypes.Primitive_Datatypes import ArcColor
from Features.Feature import Feature
from Transformations.Primitive_Transformations import recolor
from Evaluation.Eval_Features import eval_color
from math import log


class Color(Feature):
    color_value: Optional[ArcColor]
    nr_of_params = 9

    def __init__(self, color_value: Optional[ArcColor] = None):
        self.color_value = color_value

    def __repr__(self):
        return f"Feature 'Color' with parameter: {self.color_value}"

    def transform(self, abstract_matrix: AbstractObjectMatrix):
        if self.color_value is None:
            raise ValueError("cannot invoke transform without parameterization")
        for abstract_object in abstract_matrix.abstract_objects:
            recolor(abstract_object, self.color_value)

    def get_fitness(self, obj_1: AbstractObject, obj_2: AbstractObject) -> float:
        return eval_color(obj_1, obj_2)

