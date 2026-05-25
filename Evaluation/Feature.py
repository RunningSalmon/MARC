from abc import ABC, abstractmethod
from Datatypes.Abstract_ARC_Task import *

class Feature(ABC):
    @abstractmethod
    def evaluate_objects(self, abstract_object_1: AbstractObject, abstract_object_2: AbstractObject, matrix_shape: tuple[int, int]) -> float:
        pass

    def evaluate_abstract_matrix_pair(self, abstract_matrix_pair: AbstractObjectMatrixPair):
        score = 0

        input_matrix = abstract_matrix_pair.input
        output_matrix = abstract_matrix_pair.output
        input_objects = input_matrix.abstract_objects
        output_objects = output_matrix.abstract_objects

        if not abstract_matrix_pair.pairing:
            raise(NotImplementedError("evaluate_abstract_matrix_pair needs an object pairing"))

        for (input_id, output_id) in abstract_matrix_pair.pairing.items():
            score += (self.evaluate_objects(input_objects[input_id], output_objects[output_id], (input_matrix.height, input_matrix.width)))

        return score/len(input_objects)