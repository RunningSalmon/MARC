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

    def __eq__(self, other):
        return np.array_equal(self.to_matrix(), other.to_matrix())

    def to_matrix(self):
        color_matrix = np.zeros((self.height, self.width))
        for obj in self.abstract_objects:
            obj_height, obj_width = obj.Shape_Matrix.shape
            x, y = obj.Position_X, obj.Position_Y
            for i in range(0, obj_height):
                for j in range(0, obj_width):
                    if obj.Shape_Matrix[i][j] == 1 and i+y <= self.height - 1 and j+x <= self.width - 1 and x >= 0 and y >= 0:
                        color_matrix[i+y][j+x] = obj.Color.value
        return color_matrix

class AbstractMatrixPair:
    input: AbstractObjectMatrix
    output: AbstractObjectMatrix
    mapping = {}

    def __init__(self, abstract_input: AbstractObjectMatrix, abstract_output: AbstractObjectMatrix, object_pairing = None):
        self.input = abstract_input
        self.output = abstract_output
        if object_pairing:
            self.mapping = object_pairing

    def __str__(self):
        return (f"AbstractObjectMatrixPair with Input:\n{self.input},\n "
                f"and Output:\n {self.output}\n")

    def to_matrix_pair(self) -> tuple[np.ndarray, np.ndarray]:
        input_matrix = self.input.to_matrix()
        output_matrix = self.output.to_matrix()
        return input_matrix, output_matrix

    def print_pairing(self):
        if self.mapping:
            input_objects = self.input.abstract_objects
            output_objects = self.output.abstract_objects

            for id1, id2 in self.mapping.items():
                print(f"Pairing {id1}: \n{input_objects[id1]}\n {output_objects[id2]}")


class AbstractARCTask:
    train: list[AbstractMatrixPair]
    test: list[AbstractMatrixPair]

    def __init__(self, train: list[AbstractMatrixPair], test: list[AbstractMatrixPair]):
        self.train = train
        self.test = test

    def __repr__(self):
        train_str = "\n".join(str(pair) for pair in self.train)
        test_str = "\n".join(str(pair) for pair in self.test)
        return (f"AbstractObjectARCTask(\n"
                f"train:\n{train_str},\n"
                f"test:\n{test_str}\n)")
