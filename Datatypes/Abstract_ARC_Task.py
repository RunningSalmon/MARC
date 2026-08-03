from matplotlib.patches import FancyArrowPatch, Rectangle

from Datatypes.Abstract_Object import *
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from Datatypes.Abstract_Object import ArcColor


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
        """
        converts the abstract matrix into a regular color matrix by pasting all abstract objects
        at their stored position with their stored shape and color into it.

        :return: color matrix in the form of an nd-array
        """
        color_matrix = np.zeros((self.height, self.width))
        for obj in self.abstract_objects:
            obj_height, obj_width = obj.Shape_Matrix.shape
            x, y = obj.Position_X, obj.Position_Y
            for i in range(obj_height):
                for j in range(obj_width):
                    px, py = j + x, i + y
                    if obj.Shape_Matrix[i][j] == 1 and 0 <= px < self.width and 0 <= py < self.height:
                        color_matrix[py][px] = obj.Color.value
        return color_matrix

    # matplot visualization
    def to_matplot(self, ax=None, title=None, show_grid=True):
        """
        plots the abstract matrix as a color matrix
        """
        matrix = self.to_matrix()
        own_fig = ax is None
        if own_fig:
            fig, ax = plt.subplots(figsize=(self.width / 2, self.height / 2))

        for (row, col), value in np.ndenumerate(matrix):
            color = ArcColor(int(value)).to_hex()
            ax.add_patch(Rectangle((col, row), 1, 1, facecolor=color, edgecolor='none'))

        ax.set_xlim(0, self.width)
        ax.set_ylim(self.height, 0)  # invertiert, damit (0,0) oben links bleibt
        ax.set_aspect('equal')

        if show_grid:
            ax.set_xticks(np.arange(0, self.width + 1, 1), minor=False)
            ax.set_yticks(np.arange(0, self.height + 1, 1), minor=False)
            ax.grid(which='major', color='gray', linewidth=0.5)
        ax.tick_params(which='both', bottom=False, left=False,
                       labelbottom=False, labelleft=False)

        for spine in ax.spines.values():
            spine.set_visible(False)

        if title:
            ax.set_title(title)

        if own_fig:
            plt.tight_layout()
            plt.show()

        return ax


class AbstractMatrixPair:
    input: AbstractObjectMatrix
    output: AbstractObjectMatrix
    mapping = {}

    def __init__(self, abstract_input: AbstractObjectMatrix, abstract_output: AbstractObjectMatrix,
                 object_pairing=None):
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

    def to_matplot(self, ax_input=None, ax_output=None, label=""):
        """
        visualizes input and output matrices side by side.
        """
        own_fig = ax_input is None or ax_output is None
        if own_fig:
            fig, (ax_input, ax_output) = plt.subplots(1, 2, figsize=(
                (self.input.width + self.output.width) / 2 + 1,
                max(self.input.height, self.output.height) / 2 + 1
            ))
        else:
            fig = ax_input.figure

        prefix = f"{label} – " if label else ""
        self.input.to_matplot(ax=ax_input, title=f"{prefix}Input")
        self.output.to_matplot(ax=ax_output, title=f"{prefix}Target")

        if own_fig:
            plt.tight_layout()

        if own_fig:
            plt.show()

        return (ax_input, ax_output)


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

    def to_matplot(self):
        """
        visualizes all pairs of the task in one plot.
        """
        all_pairs = [(f"Train {i}", pair) for i, pair in enumerate(self.train)] + \
                    [(f"Test {i}", pair) for i, pair in enumerate(self.test)]

        n_rows = len(all_pairs)
        fig, axes = plt.subplots(n_rows, 2, figsize=(6, 3 * n_rows))

        if n_rows == 1:
            axes = axes.reshape(1, 2)

        for row, (label, pair) in enumerate(all_pairs):
            pair.to_matplot(ax_input=axes[row][0], ax_output=axes[row][1], label=label)

        plt.tight_layout()
        plt.show()

        return fig, axes
