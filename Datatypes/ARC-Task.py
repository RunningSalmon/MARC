from dataclasses import dataclass
import numpy as np

@dataclass
class ColorMatrix:
    """A Matrix consisting of the 10 ARC-Colors"""
    matrix: np.ndarray
    def __repr__(self):
        return str(f"Matrix:\n{self.matrix}")

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

