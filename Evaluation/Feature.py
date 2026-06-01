from abc import ABC, abstractmethod
from Datatypes.Abstract_ARC_Task import *

class Feature(ABC):
    @abstractmethod
    def evaluate_objects(self, abstract_object_1: AbstractObject, abstract_object_2: AbstractObject, matrix_shape: tuple[int, int]) -> float:
        pass

    def evaluate_abstract_matrix_pair(self, abstract_matrix_pair: AbstractMatrixPair):
        score = 0

        input_matrix = abstract_matrix_pair.input
        output_matrix = abstract_matrix_pair.output
        input_objects = input_matrix.abstract_objects
        output_objects = output_matrix.abstract_objects
        mean_score = 0

        if not abstract_matrix_pair.mapping:
            raise(NotImplementedError("evaluate_abstract_matrix_pair needs an object pairing"))

        for (input_id, output_id_list) in abstract_matrix_pair.mapping.items():
            for output_id in output_id_list:
                score += (self.evaluate_objects(input_objects[input_id], output_objects[output_id], (input_matrix.height, input_matrix.width)))
            mean_score = score / len(output_id_list)

        return mean_score/len(input_objects)