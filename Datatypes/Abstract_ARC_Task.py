from Datatypes.Abstract_Object import *

class AbstractObjectMatrix:
    height: int
    width: int
    abstract_objects: list[AbstractObject]
    def __init__(self, height: int, width: int, abstract_objects: list[AbstractObject]):
        self.height = height
        self.width = width
        self.abstract_objects = abstract_objects

    def __str__(self):
        objects_str = ""
        for i, obj in enumerate(self.abstract_objects):
            objects_str += str(obj)
            if i < len(self.abstract_objects) - 1:
                objects_str += "and\n"
        return f"An Abstract Matrix of Height: {self.height}, Width: {self.width}, containing:\n{objects_str}"

class AbstractObjectMatrixPair:
    input: AbstractObjectMatrix
    output: AbstractObjectMatrix
    pairing = {}

    def __init__(self, abstract_input: AbstractObjectMatrix, abstract_output: AbstractObjectMatrix):
        self.input = abstract_input
        self.output = abstract_output

    def __str__(self):
        return (f"AbstractObjectMatrixPair with Input:\n{self.input},\n "
                f"and Output:\n {self.output}\n")

    def print_pairing(self):
        if self.pairing:
            for id1, id2 in self.pairing.items():
                print(f"{id1} - {id2}")


class AbstractARCTask:
    train: list[AbstractObjectMatrixPair]
    test: list[AbstractObjectMatrixPair]

    def __init__(self, train: list[AbstractObjectMatrixPair], test: list[AbstractObjectMatrixPair]):
        self.train = train
        self.test = test

    def __repr__(self):
        train_str = "\n".join(str(pair) for pair in self.train)
        test_str = "\n".join(str(pair) for pair in self.test)
        return (f"AbstractObjectARCTask(\n"
                f"train:\n{train_str},\n"
                f"test:\n{test_str}\n)")