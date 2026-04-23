
import numpy as np

from Datatypes.Abstract_Object import *
from Datatypes.PrimitiveDatatypes import *

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


def mirror(abstract_object: AbstractObject, axis: Axis):
    shape_matrix = abstract_object.Shape
    abstract_object.Shape = np.flip(shape_matrix, axis.value)


def rotate(abstract_object: AbstractObject, degree: Degree):
    shape_matrix = abstract_object.Shape
    abstract_object.Shape = np.rot90(shape_matrix, degree.value)

def duplicate(abstract_object: AbstractObject, direction: Direction):
    shape_matrix = abstract_object.Shape
    duplicate_direction = None
    match direction:
        case Direction.Up:
            duplicate_direction = (2, 1)
            abstract_object.Position_Y -= abstract_object.height
        case Direction.Down:
            duplicate_direction = (2, 1)
        case Direction.Left:
            duplicate_direction = (1, 2)
            abstract_object.Position_X -= abstract_object.width
        case Direction.Right:
            duplicate_direction = (1, 2)

    abstract_object.Shape = np.tile(shape_matrix, duplicate_direction)

def recolor(abstract_object: AbstractObject, color: ArcColor):
    abstract_object.Color = color