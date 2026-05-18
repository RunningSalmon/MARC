from Datatypes.Abstract_ARC_Task import AbstractObjectMatrix, AbstractObjectMatrixPair
from Datatypes.Primitive_Datatypes import Axis
from Features.Feature import Feature
from Transformations.Primitive_Transformations import mirror
from Evaluation.Eval_Features import eval_mirrored_shape


class Color(Feature):
    axis: Axis
    def transform(self, abstract_matrix: AbstractObjectMatrix):
        for abstract_object in abstract_matrix.abstract_objects:
            mirror(abstract_object, self.axis)

    def get_fitness(self, abstract_matrix_pair: AbstractObjectMatrixPair):
        input_matrix = abstract_matrix_pair.input
        output_matrix = abstract_matrix_pair.output
        input_objects = input_matrix.abstract_objects
        output_objects = output_matrix.abstract_objects
        score = 0
        for (input_id, output_id) in abstract_matrix_pair.pairing:
            score += (eval_mirrored_shape(input_objects[input_id], output_objects[output_id]))

        return score/len(abstract_matrix_pair.pairing)