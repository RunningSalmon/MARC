import numpy as np
import copy
from Datatypes.ARC_Task import *
from Datatypes.Abstract_Object import *


def extract_objects(color_matrix: ColorMatrix):
    matrix = copy.copy(color_matrix.matrix)
    matrix_height, matrix_width = color_matrix.shape
    objects = []
    for (r, c), val in np.ndenumerate(matrix):
        if val != 0:
            to_visit = [(r,c)]
            obj_coordinates = []
            obj_color = val
            row_min = r
            row_max = r
            col_min = c
            col_max = c
            while len(to_visit) > 0:
                current = to_visit.pop(0)
                current_row, current_col = current
                if current not in obj_coordinates and matrix[current_row][current_col] == obj_color:
                    obj_coordinates.append(current)
                    matrix[current_row][current_col] = 0

                    row_min = min(row_min, current_row)
                    row_max = max(row_max, current_row)
                    col_min = min(col_min, current_col)
                    col_max = max(col_max, current_col)

                    if current_row > 0:
                        to_visit.append((current_row - 1, current_col))
                    if current_row < matrix_height:
                        to_visit.append((current_row + 1, current_col))
                    if current_col > 0:
                        to_visit.append((current_row, current_col - 1))
                    if current_col < matrix_width:
                        to_visit.append((current_row, current_col + 1))
            object_shape = np.zeros((row_max-row_min, col_max-col_min))
            for x, y in obj_coordinates:
                object_shape[x][y] = 1
            abstract_object = AbstractObject((row_min, col_min), object_shape, obj_color)
            objects.append(abstract_object)

    return objects