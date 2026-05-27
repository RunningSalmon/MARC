import copy
import heapq

from Datatypes.Abstract_ARC_Task import AbstractObjectMatrixPair
from Transformations.Transformation import *
from Evaluation.Matrix_Pair_Evaluation import *
from Datatypes.Primitive_Datatypes import *
from Evaluation.Feature_Color import *
from Evaluation.Feature_Position import *
from Evaluation.Feature_Shape import *

class FeatureHeapItem:
    def __init__(self, score: float, feature: Feature, feature_mapping: dict):
        self.score = score
        self.feature = feature
        self.feature_mapping = feature_mapping

    def __lt__(self, other):
        return self.score < other.score

def check_paring_ambiguity(pairing: dict):
    """returns true if every object from the output matrix appears only once in the pairing"""
    paired_objects_indices = []
    for idx, paired_idx in pairing.items():
        if paired_idx in paired_objects_indices:
            return False
        paired_objects_indices.append(paired_idx)
    return True

def create_object_mapping(abstract_matrix_pair: AbstractObjectMatrixPair, eval_features: list[Feature], transforms: list[Transformation]):
    input_matrix = abstract_matrix_pair.input
    output_matrix = abstract_matrix_pair.output
    input_objects = input_matrix.abstract_objects
    output_objects = output_matrix.abstract_objects
    matrix_shape = input_matrix.height, input_matrix.width
    feature_heap = []

    #debug
    #print(f"input objects: {len(input_objects)}, output objects: {len(output_objects)}")

    # 1 to 1 mapping (pairing)
    if len(input_objects) == len(output_objects):
        feature_heap = []
        counter = 0
        for feature in eval_features:
            feature_pairing = {}
            for idx1 in range(len(input_objects)):
                highest_score = 0
                best_fit_idx2 = 0
                for idx2 in range(len(output_objects)):
                    score = evaluate_abstract_object_pair(input_objects[idx1], output_objects[idx2], [feature], matrix_shape)
                    if score > highest_score:
                        highest_score = score
                        best_fit_idx2 = idx2
                feature_pairing[idx1] = [best_fit_idx2]

            if check_paring_ambiguity(feature_pairing):
                mapped_matrix_pair = copy.deepcopy(abstract_matrix_pair)
                mapped_matrix_pair.pairing = feature_pairing
                overall_score = evaluate_abstract_matrix_pair(mapped_matrix_pair, eval_features)
                heapq.heappush(feature_heap, FeatureHeapItem(overall_score, feature, feature_pairing))
                counter += 1

    # 1 to x mapping
    #elif len(input_objects) > len(output_objects):
    #    feature_heap = []
    #    counter = 0
    #    for feature in eval_features:
    #        feature_pairing = {}
    #        for idx2 in range(len(output_objects)):
    #            highest_score = 0
    #            best_fit_idx1 = 0
    #            for idx1 in range(len(input_objects)):
    #                score = evaluate_abstract_object_pair(input_objects[idx1],
    #                                                      output_objects[idx2],
    #                                                      [feature],
    #                                                      matrix_shape)
    #                if score > highest_score:
    #                    highest_score = score
    #                    best_fit_idx1 = idx1
    #            feature_pairing[best_fit_idx1].append(idx2)
    #
    #        if check_paring_ambiguity(feature_pairing):
    #            mapped_matrix_pair = copy.deepcopy(abstract_matrix_pair)
    #            mapped_matrix_pair.pairing = feature_pairing
    #            overall_score = evaluate_abstract_matrix_pair(mapped_matrix_pair, eval_features)
    #            heapq.heappush(feature_heap,  FeatureHeapItem(overall_score, feature, feature_pairing))
    #            counter += 1
    #
    if feature_heap:
        feature_heap_item: FeatureHeapItem = heapq.heappop(feature_heap)
        feature_score = feature_heap_item.score
        feature = feature_heap_item.feature
        mapping = feature_heap_item.feature_mapping
        return mapping

    return {}



