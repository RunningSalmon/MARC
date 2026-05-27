from Datatypes.Abstract_ARC_Task import AbstractObjectMatrixPair, AbstractARCTask
from Summary_Statistic import *
import numpy as np


def evaluate_summary_stats(abstract_matrix_pair: AbstractObjectMatrixPair, statistics: list[SummaryStatistic]) -> float:
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