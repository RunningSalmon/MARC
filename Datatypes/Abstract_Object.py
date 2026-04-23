import numpy as np

from Datatypes.PrimitiveDatatypes import *
from Datatypes.ARC_Task import *

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
        base = np.zeros(self.Shape.shape)
        for row, arr in enumerate(self.Shape):
            for col, val in enumerate(arr):
                if val == 1:
                    base[row, col] = self.Color.value

        return (f"Abstract Object with Position {self.Position_X}, {self.Position_Y};\n"
                f"and Colored Shape: \n{str(ColorMatrix(base))}\n"
                f"width: {self.width}, height: {self.height}")