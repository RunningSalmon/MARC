from Evaluation.Feature import *

class FeatureColor(Feature):
    @ensure(lambda result: 0 <= result <= 1)
    def evaluate_objects(self, abstract_object_1: AbstractObject, abstract_object_2: AbstractObject, abstract_matrix_pair: AbstractMatrixPair) -> float:
        return 1 if abstract_object_1.Color == abstract_object_2.Color else 0