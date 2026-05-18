from Datatypes.Abstract_ARC_Task import AbstractObjectMatrix, AbstractObjectMatrixPair
from Datatypes.Primitive_Datatypes import ArcColor
from Features.Feature import Feature
from Transformations.Primitive_Transformations import recolor
from Evaluation.Eval_Features import eval_color


class Color(Feature):
    color_value: ArcColor
    def transform(self, abstract_matrix: AbstractObjectMatrix):
        for abstract_object in abstract_matrix.abstract_objects:
            recolor(abstract_object, self.color_value)

    def get_fitness(self, abstract_matrix_pair: AbstractObjectMatrixPair):
        input_matrix = abstract_matrix_pair.input
        output_matrix = abstract_matrix_pair.output
        input_objects = input_matrix.abstract_objects
        output_objects = output_matrix.abstract_objects
        score = 0
        for (input_id, output_id) in abstract_matrix_pair.pairing:
            score += (eval_color(input_objects[input_id], output_objects[output_id]))

        return score/len(abstract_matrix_pair.pairing)