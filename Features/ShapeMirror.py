from Datatypes.Abstract_ARC_Task import AbstractObjectMatrix, AbstractObjectMatrixPair
from Datatypes.Abstract_Object import AbstractObject
from Datatypes.Primitive_Datatypes import Axis
from Features.Feature import Feature
from Transformations.Primitive_Transformations import mirror
from Evaluation.Eval_Features import eval_mirrored_shape


class ShapeMirror(Feature):
    axis: Axis

    def __init__(self, axis: Axis):
        self.axis = axis

    def transform(self, abstract_matrix: AbstractObjectMatrix):
        for abstract_object in abstract_matrix.abstract_objects:
            mirror(abstract_object, self.axis)

    def get_fitness(self, obj_1: AbstractObject, obj_2: AbstractObject):
        return eval_mirrored_shape(obj_1, obj_2)