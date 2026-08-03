from abc import ABC, abstractmethod
from Datatypes.Abstract_ARC_Task import *
from icontract import require, ensure, invariant


class Feature(ABC):
    @ensure(lambda result: 0 <= result <= 1)
    @abstractmethod
    def evaluate_objects(self, abstract_object_1: AbstractObject, abstract_object_2: AbstractObject,
                         abstract_matrix_pair: AbstractMatrixPair) -> float:
        """
        compares two objects in an abstract matrix pair
        :returns: a score between 0 and 1
        """
        pass

    @ensure(lambda result: 0 <= result <= 1)
    def evaluate_abstract_matrix_pair(self, abstract_matrix_pair: AbstractMatrixPair):
        """
        evaluates the two matrices of an abstract matrix pair by the average evaluation score of their paired objects
        :returns: a score between 0 and 1
        """
        scores = []

        input_matrix = abstract_matrix_pair.input
        output_matrix = abstract_matrix_pair.output
        input_objects = input_matrix.abstract_objects
        output_objects = output_matrix.abstract_objects

        if not abstract_matrix_pair.mapping:
            raise (NotImplementedError("evaluate_abstract_matrix_pair needs an object pairing"))

        for input_id, output_id in abstract_matrix_pair.mapping.items():  # iterate over objects
            scores.append(
                self.evaluate_objects(input_objects[input_id], output_objects[output_id], abstract_matrix_pair))
        mean_score = np.mean(scores)

        return mean_score
