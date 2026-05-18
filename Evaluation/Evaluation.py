from Datatypes.Abstract_ARC_Task import *

def evaluate_abstract_matrix_pair(abstract_matrix_pair: AbstractObjectMatrixPair, eval_features: list):
    score = 0
    for feature in eval_features:
        input_matrix = abstract_matrix_pair.input
        output_matrix = abstract_matrix_pair.output
        input_objects = input_matrix.abstract_objects
        output_objects = output_matrix.abstract_objects
        feature_score = 0
        for (input_id, output_id) in abstract_matrix_pair.pairing:
            feature_score += (feature.get_fitness(input_objects[input_id], output_objects[output_id]))

        score += feature_score/len(abstract_matrix_pair.pairing)

    score /= len(eval_features)

    return score

def evaluate_abstract_objects_pair(obj_1: AbstractObject, obj_2: AbstractObject, eval_features: list):
    score = 0
    for feature in eval_features:
        score += feature.get_fitness(obj_1,obj_2)
    return score/len(eval_features)