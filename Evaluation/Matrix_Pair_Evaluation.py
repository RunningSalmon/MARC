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

def obj_eval_abstract_matrix_pair(abstract_matrix_pair: AbstractObjectMatrixPair, eval_features: list[Feature]):
    if len(eval_features) == 0:
        return 0

    score = 0
    for feature in eval_features:
        score += feature.evaluate_abstract_matrix_pair(abstract_matrix_pair)

    return score/len(eval_features)

def sumstat_eval_abstract_matrix_pair(abstract_matrix_pair: AbstractObjectMatrixPair, statistics: list[SummaryStatistic]) -> float:
    if len(statistics) == 0:
        return 0

    scores = []
    for statistic in statistics:
        statistic_score = statistic.get_fitness(abstract_matrix_pair)
        scores.append(statistic_score)
    return float(np.mean(scores))

def evaluate_task_summary_stats(abstract_arc_task: AbstractARCTask, statistics: list[SummaryStatistic]) -> float:
    #this could obviously use evaluate_summary_stats, but I want the loops to be that way for simpler debugging
    scores = []
    for statistic in statistics:
        statistic_score = []
        for abstract_matrix_pair in abstract_arc_task.train:
            statistic_score.append(statistic.get_fitness(abstract_matrix_pair))
        mean_statistic_score = np.mean(statistic_score)
        scores.append(mean_statistic_score)
    return float(np.mean(scores))