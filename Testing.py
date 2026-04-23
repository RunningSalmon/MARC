import numpy as np

from Datatypes.ARC_Task import *


if __name__ == '__main__':
    basic_matrix = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    color_matrix = ColorMatrix(basic_matrix)
    print(color_matrix)