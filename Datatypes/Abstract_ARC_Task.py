from Abstract_Object import *

class AbstractObjectMatrix:
    height: int
    width: int
    abstract_objects: list[AbstractObject]
    def __init__(self, height: int, width: int, abstract_objects: list[AbstractObject]):
        self.height = height
        self.width = width
        self.abstract_objects = abstract_objects

    def __str__(self):
        return f"An Abstract Matrix of Height: {self.height}, Width: {self.width}, containing the abstract objects {self.abstract_objects}"

class AbstractObjectMatrixPair:
    input = AbstractObjectMatrix
    output = AbstractObjectMatrix
    pairing = {}

    def __init__(self, abstract_input: AbstractObjectMatrix, abstract_output: AbstractObjectMatrix):
        self.input = abstract_input
        self.output = abstract_output

    def __str__(self):
        return (f"AbstractObjectMatrixPair with Input:\n{self.input},\n "
                f"and Output:\n {self.output}\n")

class AbstractARCTask:
    train: list[AbstractObjectMatrixPair]
    test: list[AbstractObjectMatrixPair]

    def __init__(self, train: list[AbstractObjectMatrixPair], test: list[AbstractObjectMatrixPair]):
        self.train = train
        self.test = test

    def __repr__(self):
        return (f"AbstractObjectARCTask(\n"
                f"train:\n"
                f"{self.train},\n"
                f" test:\n"
                f"{self.test}\n)")