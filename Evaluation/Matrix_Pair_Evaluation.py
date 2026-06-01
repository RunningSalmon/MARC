from Datatypes.Abstract_ARC_Task import *
from Evaluation.Feature import *
from Evaluation.Summary_Statistic import SummaryStatistic


def evaluate_abstract_object_pair(abstract_object_1: AbstractObject, abstract_object_2: AbstractObject, eval_features: list[Feature], matrix_shape: tuple[int, int]) -> float:
    if len(eval_features) == 0:
        return 0

    score = 0
    for feature in eval_features:
        score += feature.evaluate_objects(abstract_object_1, abstract_object_2, matrix_shape)

    return score/len(eval_features)

def obj_eval_abstract_matrix_pair(abstract_matrix_pair: AbstractMatrixPair, eval_features: list[Feature]):
    if len(eval_features) == 0:
        return 0

    score = 0
    for feature in eval_features:
        score += feature.evaluate_abstract_matrix_pair(abstract_matrix_pair)

    return score/len(eval_features)

def sumstat_eval_abstract_matrix_pair(abstract_matrix_pair: AbstractMatrixPair, statistics: list[SummaryStatistic]) -> float:
    if len(statistics) == 0:
        return 0

    scores = []
    for statistic in statistics:
        statistic_score = statistic.get_fitness(abstract_matrix_pair)
        scores.append(statistic_score)
    return float(np.mean(scores))
