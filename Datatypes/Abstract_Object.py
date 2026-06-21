import numpy as np

from Datatypes.Primitive_Datatypes import *
class AbstractObject:
    Shape_Matrix: np.ndarray
    Color: ArcColor

    def __init__(self, position: tuple[int, int], shape: np.ndarray, color: ArcColor):
        if color is ArcColor.Black:
            raise ValueError(f"Objects cant be colored in the background color")

        top_left_y, top_left_x = position
        height, width = shape.shape

        # Geometrischer Mittelpunkt der Bounding Box (kann .5 sein bei gerader Höhe/Breite)
        self.Center_Y = top_left_y + (height - 1) / 2
        self.Center_X = top_left_x + (width - 1) / 2
        self.Shape_Matrix = shape
        self.Color = color

    @property
    def Position_X(self) -> int:
        """Top-left X, abgeleitet aus Center_X und der aktuellen Shape-Breite."""
        width = self.Shape_Matrix.shape[1]
        return round(self.Center_X - (width - 1) / 2)

    @property
    def Position_Y(self) -> int:
        """Top-left Y, abgeleitet aus Center_Y und der aktuellen Shape-Höhe."""
        height = self.Shape_Matrix.shape[0]
        return round(self.Center_Y - (height - 1) / 2)

    @Position_X.setter
    def Position_X(self, value: int):
        width = self.Shape_Matrix.shape[1]
        self.Center_X = value + (width - 1) / 2

    @Position_Y.setter
    def Position_Y(self, value: int):
        height = self.Shape_Matrix.shape[0]
        self.Center_Y = value + (height - 1) / 2

    def __str__(self):
        colored_matrix = np.zeros(self.Shape_Matrix.shape)
        for row, arr in enumerate(self.Shape_Matrix):
            for col, val in enumerate(arr):
                if val == 1:
                    colored_matrix[row, col] = self.Color.value

        string = ""
        for row in colored_matrix:
            row_string = ""
            for value in row:
                row_string += f"{Printing_Colors[int(value)]}   {Printing_Colors[10]}"
            string += row_string + "\n"

        return string + f"at {self.Position_X},{self.Position_Y}\n"

    def __repr__(self):
        return f"Object:\n{self.__str__}"