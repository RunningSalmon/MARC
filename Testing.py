import numpy as np

from Datatypes.ARC_Task import *
from Datatypes.Abstract_Object import *
from Evaluation.Object_Pairing import create_object_pairing
from Transformations.Primitive_Transformations import *

if __name__ == '__main__':
    # basic_matrix = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    # color_matrix = ColorMatrix(basic_matrix)
    # print(color_matrix)
    #
    #
    # shape_matrix = np.array([[0, 1, 0], [1, 1, 0], [0, 0, 0]])
    # abstract_object = AbstractObject((0, 0), shape_matrix, ArcColor.Red)
    # print(abstract_object)
    # print("Translate up")
    # translate(abstract_object, Direction.Up)
    # print(abstract_object)
    # print("Mirror Vertically")
    # mirror(abstract_object, Axis.Horizontal)
    # print(abstract_object)
    # print("Rotate 180deg")
    # rotate(abstract_object, Degree.Deg180)
    # print(abstract_object)
    # print("Duplicate left")
    # duplicate(abstract_object, Direction.Left)
    # print(abstract_object)
    # print("Recolor Azure")
    # recolor(abstract_object, ArcColor.Azure)
    # print(abstract_object)

    task = load_arc_task_from_json("Duplicate_Right.json", "ARC_Generator_JSONs")
    abstracted_task = task.to_abstract_task()
    #print(task)
    #print(abstracted_task)

    first_pair = abstracted_task.test[0]
    first_pair.pairing = create_object_pairing(first_pair)

    print(first_pair)
    first_pair.print_pairing()