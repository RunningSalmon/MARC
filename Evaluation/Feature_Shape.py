from typing import override

from Evaluation.Feature import *

class FeatureShape(Feature):
    @ensure(lambda result: 0 <= result <= 1)
    def evaluate_objects(self, abstract_object_1: AbstractObject, abstract_object_2: AbstractObject, abstract_matrix_pair: AbstractMatrixPair) -> float:
        matrix_shape = (abstract_matrix_pair.input.height, abstract_matrix_pair.input.width)
        obj_1_shape_matrix = abstract_object_1.Shape_Matrix
        obj_2_shape_matrix = abstract_object_2.Shape_Matrix
        obj_1_position = abstract_object_1.Position_Y, abstract_object_1.Position_X
        obj_2_position = abstract_object_2.Position_Y, abstract_object_2.Position_X

        obj_1_clipped_shape_matrix = clip_object_shape_to_matrix(obj_1_shape_matrix, obj_1_position, matrix_shape)
        obj_2_clipped_shape_matrix = clip_object_shape_to_matrix(obj_2_shape_matrix, obj_2_position, matrix_shape)
        return eval_shape_matrix(obj_1_clipped_shape_matrix, obj_2_clipped_shape_matrix)

def eval_shape_matrix(matrix_1: np.ndarray, matrix_2: np.ndarray):
    matrix_1_shape = matrix_1.shape
    matrix_2_shape = matrix_2.shape
    min_height = min(matrix_1_shape[0], matrix_2_shape[0])
    min_width = min(matrix_1_shape[1], matrix_2_shape[1])
    max_height = max(matrix_1_shape[0], matrix_2_shape[0])
    max_width = max(matrix_1_shape[1], matrix_2_shape[1])

    #both objects have no shape matrices
    if max_height == 0 or max_width == 0:
        return 1

    #one object has no shape matrix
    if min_height == 0 or min_width == 0:
        return 0


    similarity_count = 0
    for i in range(min_height):
        for j in range(min_width):
            if matrix_1[i][j] == matrix_2[i][j]:
                similarity_count += 1

    return similarity_count / (max_height * max_width)

def clip_object_shape_to_matrix(obj_shape_matrix: np.ndarray, obj_position: tuple[int, int], matrix_shape: tuple[int, int]) -> np.ndarray:
    obj_y, obj_x = obj_position
    canvas_h, canvas_w = matrix_shape
    obj_h, obj_w = obj_shape_matrix.shape

    # object shape within matrix
    row_start = max(0, -obj_y)
    col_start = max(0, -obj_x)
    row_end = min(obj_h, canvas_h - obj_y)
    col_end = min(obj_w, canvas_w - obj_x)

    # object not in matrix at all
    if row_start >= row_end or col_start >= col_end:
        return np.zeros((0, 0))

    return obj_shape_matrix[row_start:row_end, col_start:col_end]