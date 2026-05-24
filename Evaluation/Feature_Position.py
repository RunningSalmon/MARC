from Evaluation.Feature import *

class FeaturePosition(Feature):
    matrix_shape: tuple[int,int]

    def __init__(self, matrix_shape: tuple[int, int]):
        self.matrix_shape = matrix_shape

    def evaluate_objects(self, abstract_object_1: AbstractObject, abstract_object_2: AbstractObject) -> float:
        distance_vec = (abstract_object_2.Position_Y - abstract_object_1.Position_Y, abstract_object_2.Position_X - abstract_object_1.Position_X)
        relative_distance_vec = (distance_vec[0] / self.matrix_shape[0], distance_vec[1] / self.matrix_shape[1])
        relative_distance = np.linalg.norm(relative_distance_vec)
        return float(1 - relative_distance)
