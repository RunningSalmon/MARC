from dataclasses import dataclass
import numpy as np

from Datatypes.Primitive_Datatypes import Printing_Colors


@dataclass
class ColorMatrix:
    """A Matrix consisting of the 10 ARC-Colors"""
    valid_values = set(range(10))
    matrix: np.ndarray

    def __init__(self, matrix: np.ndarray):
        if any(val not in self.valid_values for val in matrix.flat):
            raise ValueError(f"Invalid matrix: {matrix}. Only ARC-Color Values (0-9) are allowed.")
        self.matrix = matrix

    def __str__(self):
        string = ""
        for row in self.matrix:
            row_string = ""
            for value in row:
                row_string += f"{Printing_Colors[value]}   {Printing_Colors[10]}"
            string += row_string + "\n"
        return string

    def __repr__(self):
        return f"Matrix:\n{self.__str__}"

    def shape(self):
        return self.matrix.shape

@dataclass
class MatrixPair:
    """Holds an input/output matrix pair of ColorMatrices"""
    input: ColorMatrix
    output: ColorMatrix

    def __repr__(self):
        return f"MatrixPair(\ninput=\n{self.input},\n output=\n{self.output})"


@dataclass
class ARCTask:
    """Holds the full dataset with train and test trials"""
    train: list[MatrixPair]
    test: list[MatrixPair]

    def __repr__(self):
        return (f"ARCTask(\n"
                f"train:\n"
                f"{self.train},\n"
                f" test:\n"
                f"{self.test}\n)")

