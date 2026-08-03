import json
from pathlib import Path

import numpy as np

from Datatypes.ARC_Task import ARCTask, MatrixPair, ColorMatrix
from Evaluation.Feature_Color import FeatureColor
from Evaluation.Feature_Position import FeaturePosition
from Evaluation.Feature_Shape import FeatureShape
from Evaluation.Statistic_Number_Of_Edges import NumberOfEdges
from Evaluation.Statistic_Number_Of_Objects import NumberOfObjects
from Evaluation.Statistic_Pixels_Correct import PixelsCorrect
from Evaluation.Statistic_Pixels_Per_Color import PixelsPerColor
from Task_Generation.Matrix_Transformation import transform_and_evaluate_test_trials
from MDL_Search.MDLSearch import mdl_search
from Transformations.Duplicate import Duplicate
from Transformations.Mirror import Mirror
from Transformations.Recolor import Recolor
from Transformations.Rotate import Rotate
from Transformations.Translate import Translate
from Conditionals.Condition_Color import ConditionColor
from Conditionals.Condition_Position import ConditionPosition
from Conditionals.ConditionShape import ConditionShape

#must match the max_step_nr constant hardcoded inside MDLSearch.mdl_search.
MAX_STEPS = 100
SEED = 128

TEST_SET_DIR = Path("test_sets")
RESULTS_DIR = Path("results")
RESULTS_DIR.mkdir(exist_ok=True)

eval_features = [FeatureColor(), FeaturePosition(), FeatureShape()]
statistics = [NumberOfEdges(), NumberOfObjects(), PixelsCorrect(), PixelsPerColor()]
transforms = [Duplicate(), Mirror(), Recolor(), Rotate(), Translate()]
conditions = [ConditionColor(), ConditionPosition(), ConditionShape()]


def load_test_set(name=f"test_set{SEED}.json"):
    """loads test_set + 'SEED' from the test_sets directory."""
    with open(TEST_SET_DIR / name) as f:
        return json.load(f)


def json_dict_to_arc_task(task_dict: dict) -> ARCTask:
    def to_array(m):
        return np.array(m, dtype=np.int8)

    train = [MatrixPair(input=ColorMatrix(to_array(p["input"])), output=ColorMatrix(to_array(p["output"])))
              for p in task_dict["train"]]
    test = [MatrixPair(input=ColorMatrix(to_array(p["input"])), output=ColorMatrix(to_array(p["output"])))
             for p in task_dict["test"]]
    return ARCTask(train, test)


def classify_failure(solution, steps, solved_on_test):
    """labels the failure reason of a solution."""
    if solution is None:
        if steps >= MAX_STEPS:
            return "step_limit_reached"
        return "heap_exhausted"
    if not solved_on_test:
        return "wrong_solution_generalization_failed"
    return None


def run_configuration(test_set_entries, transforms, eval_features, statistics, conditions, config_name):
    """runs the search for each task in the test set with the given configuration."""
    task_results = []

    for entry in test_set_entries:
        abstract_task = json_dict_to_arc_task(entry["task"]).to_abstract_task()

        solution, visited, steps = mdl_search(abstract_task, transforms, eval_features, statistics, conditions)
        solved_on_test = bool(solution) and transform_and_evaluate_test_trials(abstract_task, solution)
        solved = bool(solution) and solved_on_test
        failure_reason = classify_failure(solution, steps, solved_on_test)

        result = {
            "task_id": entry["task_id"],
            "config": config_name,
            "template": entry["template"],
            "series_length": entry["series_length"],
            "repetition": entry["repetition"],
            "ground_truth_series": entry["ground_truth_series"],
            "solved": solved,
            "steps": steps,
            "found_series": [repr(t) for t in solution] if solution else None,
            "failure_reason": failure_reason,
        }
        task_results.append(result)

        status = f"solved in {steps} steps" if solved else f"failed ({failure_reason})"
        print(f"[{config_name}] {entry['task_id']}: {status}")

    return task_results


def save_results(task_results, config_name):
    """saves the task results to a JSON file with the naming convention 'config_name' + 'SEED'."""
    path = RESULTS_DIR / f"{config_name}{SEED}.json"
    with open(path, "w") as f:
        json.dump(task_results, f, indent=2)
    print(f"Saved {len(task_results)} task results to {path}")


if __name__ == '__main__':
    test_set_entries = load_test_set()

    configs = [
        ("Full", transforms, eval_features, statistics, conditions),
        ("Full_unconditioned", transforms, eval_features, statistics, []),
        ("Object_based_only", transforms, eval_features, [], []),
        ("Statistics_only", transforms, [], statistics, []),
    ]

    for config_name, t, ef, st, co in configs:
        results = run_configuration(test_set_entries, t, ef, st, co, config_name)
        save_results(results, config_name)