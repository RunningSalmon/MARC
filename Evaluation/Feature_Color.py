from Evaluation.Feature import *

class FeatureColor(Feature):
    def evaluate_objects(self, abstract_object_1: AbstractObject, abstract_object_2: AbstractObject) -> float:
        return 1 if abstract_object_1.Color == abstract_object_2.Color else 0