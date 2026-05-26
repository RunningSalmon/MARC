import numpy as np

from Datatypes.ARC_Task import *
from Datatypes.Abstract_ARC_Task import *
from Transformations.Transformation import *

def manipulate_abstract_matrix(abstract_matrix: AbstractObjectMatrix, transformation_series: list[Transformation]):
    for transformation in transformation_series:
        if not transformation.fixed_parameter:
            raise ValueError("Transformations need to be parameterized for matrix_manipulation.")
        transformation.transform(abstract_matrix)

def manipulate_arc_task(arc_task: AbstractARCTask, transformation_series: list[Transformation]):
    training_trials = arc_task.train
    for trial in training_trials:
        manipulate_abstract_matrix(trial.output, transformation_series)

def abstract_pair_to_matrix_pair(abstract_matrix_pair: AbstractObjectMatrixPair) -> MatrixPair:
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