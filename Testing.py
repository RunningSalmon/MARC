from Evaluation.Matrix_Pair_Evaluation import *
from Evaluation.Feature_Color import *
from Evaluation.Feature_Position import *
from Evaluation.Feature_Shape import *
from Task_Generation.Matrix_Transformation import manipulate_arc_task, abstract_task_to_arc_task, \
    abstract_pair_to_matrix_pair, manipulate_abstract_matrix

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

    #task = load_arc_task_from_json("Rotate90+DuplicateDown.json", "ARC_Generator_JSONs")
    #abstracted_task = task.to_abstract_task()
    #print(task)
    #print(abstracted_task)
    #first_input_color_matrix = task.test[0].input
    #print(first_input_color_matrix)
    #
    #transformations = [Recolor(),
    #                   Translate(),
    #                   Duplicate(),
    #                   Mirror(),
    #                   Rotate()]


    #train = abstracted_task.train
    #for matrix_pair in train:
    #    matrix_pair.pairing = create_object_mapping(matrix_pair, eval_features, transformations)
    #    Rotate().transform(matrix_pair.input, RotationParameter(Degree.Deg90))
    #    print(matrix_pair)
    #    score_shape = evaluate_abstract_matrix_pair(matrix_pair, [FeatureShape()])
    #    print(score_shape)

    template_task_1 = load_arc_task_from_json("Template_Task_1.json", "ARC_Generator_JSONs")
    #print(template_task_1)
    template_task_1 = template_task_1.to_abstract_task()
    manipulations = [Rotate(RotationParameter(Degree.Deg90))]
    eval_features = [FeatureColor(),
                    FeaturePosition(),
                    FeatureShape()]
    transformations = [Duplicate(),
                       Mirror(),
                       Recolor(),
                       Rotate(),
                       Translate(),]
    manipulate_arc_task(template_task_1, manipulations)
    #print(abstract_task_to_arc_task(template_task_1))

    #test_matrix_pair = template_task_1.train[0]
    #test_matrix_pair.pairing = create_object_mapping(test_matrix_pair, eval_features, transformations)
    #print(abstract_pair_to_matrix_pair(test_matrix_pair))
    #score = FeatureShape().evaluate_abstract_matrix_pair(test_matrix_pair)
    #print(score)
    ##manipulate_abstract_matrix(test_matrix_pair.input, [Rotate(RotationParameter(Degree.Deg90))])
    #manipulate_abstract_matrix(test_matrix_pair.input, [Mirror(MirrorParameter(Axis.Horizontal))])
    #score = evaluate_abstract_matrix_pair(test_matrix_pair, eval_features)
    #print(score)



    solution, visited = mdl_search(template_task_1, transformations, eval_features)
    print(f"found solution: {solution}. visited:\n{visited}")


    #print(first_input)
    #print(ColorMatrix(first_input.to_matrix()))

    #transformation = Mirror()

    #transformation.transform(first_input, MirrorParameter(Axis.Vertical))
    #print(first_input)
    #print(ColorMatrix(first_input.to_matrix()))
