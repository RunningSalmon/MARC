from Datatypes.Abstract_Object import *
from Transformations.Primitive_Transformations import *


def eval_color(obj_1: AbstractObject, obj_2: AbstractObject):
    return 1 if obj_1.Color == obj_2.Color else 0

def eval_position(obj_1: AbstractObject, obj_2: AbstractObject, matrix_shape: tuple[int, int]):
    distance_vec = (obj_2.Position_Y - obj_1.Position_Y, obj_2.Position_X - obj_1.Position_X)
    relative_distance_vec = (distance_vec[0]/matrix_shape[0], distance_vec[1]/matrix_shape[1])
    relative_distance = np.linalg.norm(relative_distance_vec)
    return 1-relative_distance


def eval_shape_matrix(matrix_1: np.ndarray, matrix_2: np.ndarray):
    if matrix_1.shape != matrix_2.shape:
        return 0.0

    intersection = np.sum((matrix_1 == 1) & (matrix_2 == 1))
    union = np.sum((matrix_1 == 1) | (matrix_2 == 1))

    if union == 0:
        return 0.0
    return intersection/union

def eval_shape_duplicated(obj_1: AbstractObject, obj_2: AbstractObject):
    obj_1_shape_matrix = obj_1.Shape
    obj_2_shape_matrix = obj_2.Shape
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
    obj_1_shape_matrix = obj_1.Shape
    obj_2_shape_matrix = obj_2.Shape
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
    obj_1_shape_matrix = obj_1.Shape
    obj_2_shape_matrix = obj_2.Shape
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
