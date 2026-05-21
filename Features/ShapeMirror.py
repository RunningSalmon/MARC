from typing import Optional

from Datatypes.Abstract_ARC_Task import AbstractObjectMatrix, AbstractObjectMatrixPair
from Datatypes.Abstract_Object import AbstractObject
from Datatypes.Primitive_Datatypes import Axis
from Features.Feature import Feature
from Transformations.Primitive_Transformations import mirror
from Evaluation.Eval_Features import eval_mirrored_shape


class ShapeMirror(Feature):
    axis: Optional[Axis]

    nr_of_algos = 2

    def __init__(self, axis: Optional[Axis] = None):
        self.axis = axis

    def __repr__(self):
        return f"Feature 'Mirror' with parameter: {self.axis}"

    def transform(self, abstract_matrix: AbstractObjectMatrix):
        if self.axis is None:
            raise ValueError("cannot invoke transform without parameterization")

        for abstract_object in abstract_matrix.abstract_objects:
            mirror(abstract_object, self.axis)

    def get_fitness(self, obj_1: AbstractObject, obj_2: AbstractObject):
        return eval_mirrored_shape(obj_1, obj_2)