import copy
from dataclasses import dataclass
import numpy as np

from Datatypes.Abstract_ARC_Task import AbstractObjectMatrix, AbstractMatrixPair, AbstractARCTask
import json

from Datatypes.Abstract_Object import AbstractObject
from Datatypes.Primitive_Datatypes import Printing_Colors, ArcColor


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

    def extract_abstract_objects(self):
        """
        Extracts all objects from the matrix and returns a list of AbstractObjects
        :returns: the objects found in the matrix
        """
        matrix = copy.deepcopy(self.matrix)
        matrix_height, matrix_width = self.shape()
        objects = []
        for (r, c), color in np.ndenumerate(matrix):
            if color != 0:
                to_visit = [(r, c)]
                obj_coordinates = []
                obj_color = color
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
                        if current_row < matrix_height - 1:
                            to_visit.append((current_row + 1, current_col))
                        if current_col > 0:
                            to_visit.append((current_row, current_col - 1))
                        if current_col < matrix_width - 1:
                            to_visit.append((current_row, current_col + 1))
                object_shape = np.zeros((row_max - row_min + 1, col_max - col_min + 1))
                for x, y in obj_coordinates:
                    object_shape[x - row_min][y - col_min] = 1
                abstract_object = AbstractObject((row_min, col_min), object_shape, ArcColor(obj_color))
                # print(f"Found object: color={obj_color}, pos=({row_min},{col_min}), shape={object_shape.shape}")
                objects.append(abstract_object)

        return objects

    def to_abstract_matrix(self):
        """
        turns the matrix into an AbstractObjectMatrix by extracting all objects from it
        :returns: An AbstractObjectMatrix with the extracted objects and the shape of the original matrix
        """
        objects = self.extract_abstract_objects()
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
        return AbstractMatrixPair(abstract_input, abstract_output)


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


def load_arc_task_from_json(json_file: str, path=str) -> ARCTask:
    """Load a MatrixDataset from an ARC_Problem_Interface JSON file."""

    with open(f"{path}/{json_file}", "r") as f:
        data = json.load(f)

    def to_array(matrix: list[list[int]]) -> np.ndarray:
        return np.array(matrix, dtype=np.int8)

    train = [MatrixPair(input=ColorMatrix(to_array(p["input"])), output=ColorMatrix(to_array(p["output"]))) for p in
             data.get("train", [])]
    test = [MatrixPair(input=ColorMatrix(to_array(p["input"])), output=ColorMatrix(to_array(p["output"]))) for p in
            data.get("test", [])]
    return ARCTask(train, test)
