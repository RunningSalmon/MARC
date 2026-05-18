import numpy as np

from Datatypes.Primitive_Datatypes import *
class AbstractObject:
    Position_X: int
    Position_Y: int
    Shape = np.ndarray
    Color = ArcColor

    def __init__(self, position: tuple[int, int], shape: np.ndarray, color: ArcColor):
        self.Position_X = position[0]
        self.Position_Y = position[1]
        self.height = shape.shape[0]
        self.width = shape.shape[1]
        self.Shape = shape
        if color is ArcColor.Black:
            raise ValueError(f"Objects cant be colored in the background color")
        self.Color = color

    def __str__(self):
        colored_matrix = np.zeros(self.Shape.shape)
        for row, arr in enumerate(self.Shape):
            for col, val in enumerate(arr):
                if val == 1:
                    colored_matrix[row, col] = self.Color

        string = ""
        for row in colored_matrix:
            row_string = ""
            for value in row:
                row_string += f"{Printing_Colors[int(value)]}   {Printing_Colors[10]}"
            string += row_string + "\n"

        return string

    def __repr__(self):
        return f"Object:\n{self.__str__}"