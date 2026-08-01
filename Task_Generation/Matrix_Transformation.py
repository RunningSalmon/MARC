import numpy as np

from Conditionals.ConditionShape import ConditionShape, ConditionShapeParameter
from Conditionals.Condition_Color import ConditionColor, ConditionColorParameter
from Conditionals.Condition_Position import ConditionPosition, ConditionPositionParameter
from Datatypes.ARC_Task import *
from Datatypes.Abstract_ARC_Task import *
from Transformations.Transformation import *
import random
import copy

def manipulate_abstract_matrix(abstract_matrix: AbstractObjectMatrix, transformation_series: list[Transformation]):
    for transformation in transformation_series:
        if not transformation.fixed_parameter:
            raise ValueError("Transformations need to be parameterized for matrix_manipulation.")
        transformation.transform_abstract_matrix(abstract_matrix)

def manipulate_arc_task(arc_task: AbstractARCTask, transformation_series: list[Transformation]):
    training_trials = arc_task.train
    test_trials = arc_task.test
    for trial in training_trials:
        manipulate_abstract_matrix(trial.output, transformation_series)
    for trial in test_trials:
        manipulate_abstract_matrix(trial.output, transformation_series)

def abstract_pair_to_matrix_pair(abstract_matrix_pair: AbstractMatrixPair) -> MatrixPair:
    matrix_pair = abstract_matrix_pair.to_matrix_pair()
    input_color_matrix = ColorMatrix(matrix_pair[0])
    output_color_matrix = ColorMatrix(matrix_pair[1])
    return MatrixPair(input_color_matrix, output_color_matrix)


def abstract_task_to_arc_task(abstract_task: AbstractARCTask) -> ARCTask:
    abstract_train = abstract_task.train
    abstract_test = abstract_task.test
    train = []
    test = []
    for abstract_matrix_pair in abstract_train:
        train.append(abstract_pair_to_matrix_pair(abstract_matrix_pair))
    for abstract_matrix_pair in abstract_test:
        test.append(abstract_pair_to_matrix_pair(abstract_matrix_pair))

    return ARCTask(train, test)




def generate_test_task(template: AbstractARCTask,
                       series_length: int,
                       available_transformations: list[Transformation],
                       available_conditions: list[Condition]) -> tuple[AbstractARCTask, list[Transformation]]:
    task = copy.deepcopy(template)
    series = []
    valid_conditions = []
    if available_conditions:
        valid_conditions = get_valid_conditions(template, available_conditions)

    for _ in range(series_length):
        transformation = random.choice(available_transformations)
        parameter = random.choice(transformation.possible_parameters)
        if valid_conditions and random.randint(1, 10) == 1: #10% chance
            parameterized_condition = random.choice(valid_conditions)
            parameterized = transformation.from_parameter_condition(parameter, parameterized_condition)
        else:
            parameterized = transformation.from_parameter_condition(parameter, None)
        series.append(parameterized)

    manipulate_arc_task(task, series)
    return task, series

def get_valid_conditions(template, available_conditions):
    # extract actual feature values present in the template
    valid = []
    if all(len(trial.input.abstract_objects) == 1 for trial in template.train):
        return valid
    objects = [obj for trial in template.train for obj in trial.input.abstract_objects]
    colors = set(obj.Color for obj in objects)
    shapes = set(obj.Shape_Matrix.tobytes() for obj in objects)
    positions = set((obj.Center_Y, obj.Center_X) for obj in objects)
    for condition in available_conditions:
        if isinstance(condition, ConditionColor):
            for color in colors:
                valid.append(ConditionColor(ConditionColorParameter(color)))
        elif isinstance(condition, ConditionShape):
            if len(shapes) > 1:
                for obj in objects:
                    valid.append(ConditionShape(ConditionShapeParameter(obj.Shape_Matrix)))
        elif isinstance(condition, ConditionPosition):
            for position in positions:
                valid.append(
                    ConditionPosition(ConditionPositionParameter(position[0], Axis.Vertical, SmallerOrLarger.smaller)))
                valid.append(
                    ConditionPosition(ConditionPositionParameter(position[0], Axis.Vertical, SmallerOrLarger.larger)))
                valid.append(
                    ConditionPosition(ConditionPositionParameter(position[1], Axis.Horizontal, SmallerOrLarger.smaller)))
                valid.append(
                    ConditionPosition(ConditionPositionParameter(position[1], Axis.Horizontal, SmallerOrLarger.larger)))
    return valid

def generate_test_set(templates: list[AbstractARCTask],
                      series_lengths: list[int],
                      available_transformations: list[Transformation],
                      available_conditions: list[Condition],
                      tasks_per_combination: int) -> list[tuple[AbstractARCTask, list[Transformation]]]:
    test_set = []
    for template in templates:
        for length in series_lengths:
            for _ in range(tasks_per_combination):
                task, series = generate_test_task(template, length, available_transformations, available_conditions)
                test_set.append((task, series))
    return test_set

def apply_to_test_trials(task: AbstractARCTask, series: list[Transformation]):
    test_trials = task.test
    for trial in test_trials:
        manipulate_abstract_matrix(trial.input, series)

def transform_and_evaluate_test_trials(task: AbstractARCTask, series: list[Transformation]) -> bool:
    task_copy = copy.deepcopy(task)
    apply_to_test_trials(task_copy, series)
    test_trials = task_copy.test
    for trial in test_trials:
        if not np.array_equal(trial.input.to_matrix(), trial.output.to_matrix()):
            return False
    return True