from Evaluation.Feature import *

class FeatureShape(Feature):
    def evaluate_objects(self, abstract_object_1: AbstractObject, abstract_object_2: AbstractObject) -> float:
        obj_1_shape_matrix = abstract_object_1.Shape_Matrix
        obj_2_shape_matrix = abstract_object_2.Shape_Matrix
        return eval_shape_matrix(obj_1_shape_matrix, obj_2_shape_matrix)




def eval_shape_matrix(matrix_1: np.ndarray, matrix_2: np.ndarray):
    matrix_1_shape = matrix_1.shape
    matrix_2_shape = matrix_2.shape
    min_height = min(matrix_1_shape[0], matrix_2_shape[0])
    min_width = min(matrix_1_shape[1], matrix_2_shape[1])
    max_height = max(matrix_1_shape[0], matrix_2_shape[0])
    max_width = max(matrix_1_shape[1], matrix_2_shape[1])

    similarity_count = 0
    for i in range(min_height):
        for j in range(min_width):
            if matrix_1[i][j] == matrix_2[i][j]:
                similarity_count += 1

    return similarity_count / (max_height * max_width)