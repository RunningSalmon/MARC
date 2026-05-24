from Evaluation.Matrix_Pair_Evaluation import *
from Evaluation.Feature_Color import *
from Evaluation.Feature_Position import *
from Evaluation.Feature_Shape import *

from Transformations.Recolor import *
from Transformations.Translate import *
from Transformations.Duplicate import *
from Transformations.Mirror import *
from Transformations.Rotate import *
from MDL_Search.MDLSearch import *

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

    task = load_arc_task_from_json("Rotate90+DuplicateDown.json", "ARC_Generator_JSONs")
    abstracted_task = task.to_abstract_task()
    print(task)
    #print(abstracted_task)
    #first_input_color_matrix = task.test[0].input
    #print(first_input_color_matrix)

    first_pair = abstracted_task.train[0]
    first_pair.pairing = create_object_pairing(first_pair)

    # print(first_pair)
    first_pair.print_pairing()


    first_input = first_pair.input
    first_output = first_pair.output
    transformations = [Recolor(),
                       Translate(first_input.height, first_input.width),
                       Duplicate(first_input.height, first_input.width),
                       Mirror(),
                       Rotate()]
    eval_features = relevant_features = [FeatureColor(),
                         FeaturePosition((first_input.height, first_input.width)),
                         FeatureShape()]

    solution, visited = mdl_search(first_pair, transformations, eval_features)
    print(f"found solution: {solution}. visited:\n{visited}")

    #print(first_input)
    #print(ColorMatrix(first_input.to_matrix()))

    #transformation = Mirror()

    #transformation.transform(first_input, MirrorParameter(Axis.Vertical))
    #print(first_input)
    #print(ColorMatrix(first_input.to_matrix()))
