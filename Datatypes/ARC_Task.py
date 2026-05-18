from dataclasses import dataclass
import numpy as np

from Datatypes.Abstract_ARC_Task import AbstractObjectMatrix, AbstractObjectMatrixPair, AbstractARCTask
from Object_Detection import *
import json
from dataclasses import dataclass


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

    def to_abstract_matrix(self):
        objects = extract_objects(self)
        height, width = self.shape()
        abstract_matrix = AbstractObjectMatrix(height, width, objects)
        return abstract_matrix

@dataclass
class MatrixPair:
    """Holds an input/output matrix pair of ColorMatrices"""
    input: ColorMatrix
    output: ColorMatrix

    def __init__(self, input: ColorMatrix, output: ColorMatrix):
        self.input = input
        self.output = output

    def __repr__(self):
        return f"MatrixPair(\ninput=\n{self.input},\n output=\n{self.output})"

    def to_abstract_matrix_pair(self):
        abstract_input = self.input.to_abstract_matrix()
        abstract_output = self.output.to_abstract_matrix()
        return AbstractObjectMatrixPair(abstract_input, abstract_output)


@dataclass
class ARCTask:
    """Holds the full dataset with train and test trials"""
    train: list[MatrixPair]
    test: list[MatrixPair]

    def __init__(self, train: list[MatrixPair], test: list[MatrixPair]):
        self.train = train
        self.test = test

    def __repr__(self):
        return (f"ARCTask(\n"
                f"train:\n"
                f"{self.train},\n"
                f" test:\n"
                f"{self.test}\n)")

    def to_abstract_task(self):
        train = [pair.to_abstract_matrix_pair() for pair in self.train]
        test = [pair.to_abstract_matrix_pair() for pair in self.test]

        return AbstractARCTask(train, test)


def load_arc_task_from_json(json_file: str, path = str) -> ARCTask:
    """Load a MatrixDataset from an ARC_Problem_Interface JSON file."""

    with open(f"{path}.{json_file}", "r") as f:
        data = json.load(f)

    def to_array(matrix: list[list[int]]) -> np.ndarray:
        return np.array(matrix, dtype=np.int8)

    train = [MatrixPair(input=ColorMatrix(to_array(p["input"])), output=ColorMatrix(to_array(p["output"]))) for p in
             data.get("train", [])]
    test = [MatrixPair(input=ColorMatrix(to_array(p["input"])), output=ColorMatrix(to_array(p["output"]))) for p in
            data.get("test", [])]
    return ARCTask(train, test)
