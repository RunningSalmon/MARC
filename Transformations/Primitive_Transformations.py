
import numpy as np

from Datatypes.Abstract_Object import *
from Datatypes.Primitive_Datatypes import *

def translate(abstract_object: AbstractObject, direction: Direction):
    match direction:
        case Direction.Up:
            abstract_object.Position_Y -= 1
        case Direction.Down:
            abstract_object.Position_Y += 1
        case Direction.Left:
            abstract_object.Position_X -= 1
        case Direction.Right:
            abstract_object.Position_X += 1


def mirror_matrix(matrix: np.ndarray, axis: Axis):
    return np.flip(matrix, axis.value)

def mirror(abstract_object: AbstractObject, axis: Axis):
    shape_matrix = abstract_object.Shape_Matrix
    abstract_object.Shape_Matrix = mirror_matrix(shape_matrix, axis)

def rotate_matrix(matrix: np.ndarray, degree: Degree):
    return np.rot90(matrix, degree.value)

def rotate(abstract_object: AbstractObject, degree: Degree):
    shape_matrix = abstract_object.Shape_Matrix
    abstract_object.Shape_Matrix = rotate_matrix(shape_matrix, degree)

def duplicate_matrix(matrix: np.ndarray, direction: Direction):
    duplicate_direction = None
    if direction == Direction.Up or direction == Direction.Down:
        duplicate_direction = (2, 1)

    elif direction == Direction.Left or direction == Direction.Right:
        duplicate_direction = (1,2)

    return np.tile(matrix, duplicate_direction)

def duplicate(abstract_object: AbstractObject, direction: Direction):
    height, width = abstract_object.Shape_Matrix.shape
    if direction == Direction.Up:
        abstract_object.Position_Y -= height
    elif direction == Direction.Left:
        abstract_object.Position_X -= width

    abstract_object.Shape_Matrix = duplicate_matrix(abstract_object.Shape_Matrix, direction)

def recolor(abstract_object: AbstractObject, color: ArcColor):
    abstract_object.Color = color