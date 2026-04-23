from dataclasses import dataclass
import numpy as np

ARC_COLORS = {
    0: "\033[48;2;0;0;0m",        # Black (background)
    1: "\033[48;2;0;116;217m",    # Blue
    2: "\033[48;2;255;65;54m",    # Red
    3: "\033[48;2;46;204;64m",    # Green
    4: "\033[48;2;255;220;0m",    # Yellow
    5: "\033[48;2;170;170;170m",  # Grey
    6: "\033[48;2;240;18;190m",   # Pink
    7: "\033[48;2;255;133;27m",   # Orange
    8: "\033[48;2;127;219;255m",  # Azure
    9: "\033[48;2;135;12;37m",    # Maroon
}
Reset_Color = "\033[0m"

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
                row_string += f"{ARC_COLORS[value]}   {Reset_Color}"
            string += row_string + "\n"
        return string

    def __repr__(self):
        return f"Matrix:\n{self.__str__}"

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

