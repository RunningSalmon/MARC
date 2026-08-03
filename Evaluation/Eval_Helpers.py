from Transformations.Primitive_Transformations import *


def eval_shape_matrix(matrix_1: np.ndarray, matrix_2: np.ndarray):
    """
    compares two shape matrices
    :returns: the number of identical values at identical coordinates divided by the total number of values
    """
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


def eval_shape_duplicated(obj_1: AbstractObject, obj_2: AbstractObject):
    """evaluates two shapes by duplicating them and comparing the resulting shape matrices"""
    obj_1_shape_matrix = obj_1.Shape_Matrix
    obj_2_shape_matrix = obj_2.Shape_Matrix
    fitness = []

    # duplicate up
    obj_1_transformed_matrix = duplicate_matrix(obj_1_shape_matrix, Direction.Up)
    fitness.append(eval_shape_matrix(obj_1_transformed_matrix, obj_2_shape_matrix))

    # duplicate down
    obj_1_transformed_matrix = duplicate_matrix(obj_1_shape_matrix, Direction.Down)
    fitness.append(eval_shape_matrix(obj_1_transformed_matrix, obj_2_shape_matrix))

    # duplicate left
    obj_1_transformed_matrix = duplicate_matrix(obj_1_shape_matrix, Direction.Left)
    fitness.append(eval_shape_matrix(obj_1_transformed_matrix, obj_2_shape_matrix))

    # duplicate right
    obj_1_transformed_matrix = duplicate_matrix(obj_1_shape_matrix, Direction.Right)
    fitness.append(eval_shape_matrix(obj_1_transformed_matrix, obj_2_shape_matrix))

    return max(fitness)


def eval_rotated_shape(obj_1: AbstractObject, obj_2: AbstractObject):
    """evaluates two shapes by rotating them and comparing the resulting shape matrices"""
    obj_1_shape_matrix = obj_1.Shape_Matrix
    obj_2_shape_matrix = obj_2.Shape_Matrix
    fitness = []

    # 90deg
    obj_1_transformed_matrix = rotate_matrix(obj_1_shape_matrix, Degree.Deg90)
    fitness.append(eval_shape_matrix(obj_1_transformed_matrix, obj_2_shape_matrix))
    # 180deg
    obj_1_transformed_matrix = rotate_matrix(obj_1_shape_matrix, Degree.Deg180)
    fitness.append(eval_shape_matrix(obj_1_transformed_matrix, obj_2_shape_matrix))
    # 270deg
    obj_1_transformed_matrix = rotate_matrix(obj_1_shape_matrix, Degree.Deg270)
    fitness.append(eval_shape_matrix(obj_1_transformed_matrix, obj_2_shape_matrix))

    return max(fitness)


def eval_mirrored_shape(obj_1: AbstractObject, obj_2: AbstractObject):
    """evaluates two shapes by mirroring them and comparing the resulting shape matrices"""
    obj_1_shape_matrix = obj_1.Shape_Matrix
    obj_2_shape_matrix = obj_2.Shape_Matrix
    fitness = []

    # Horizontal
    obj_1_transformed_matrix = mirror_matrix(obj_1_shape_matrix, Axis.Horizontal)
    fitness.append(eval_shape_matrix(obj_1_transformed_matrix, obj_2_shape_matrix))
    # Vertical
    obj_1_transformed_matrix = mirror_matrix(obj_1_shape_matrix, Axis.Vertical)
    fitness.append(eval_shape_matrix(obj_1_transformed_matrix, obj_2_shape_matrix))
    # Both
    obj_1_transformed_matrix = mirror_matrix(obj_1_transformed_matrix, Axis.Horizontal)
    fitness.append(eval_shape_matrix(obj_1_transformed_matrix, obj_2_shape_matrix))

    return max(fitness)
