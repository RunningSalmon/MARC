import json
import random
from pathlib import Path

from Datatypes.ARC_Task import load_arc_task_from_json
from Task_Generation.Matrix_Transformation import generate_test_set, abstract_task_to_arc_task
from Transformations.Duplicate import Duplicate
from Transformations.Mirror import Mirror
from Transformations.Recolor import Recolor
from Transformations.Rotate import Rotate
from Transformations.Translate import Translate
from Conditionals.Condition_Color import ConditionColor
from Conditionals.Condition_Position import ConditionPosition
from Conditionals.ConditionShape import ConditionShape

TEMPLATE_NAMES = ['T1', 'T2', 'T3', 'T4', 'T5']
SERIES_LENGTHS = [1, 3, 5]
TASKS_PER_COMBINATION = 5
SEED = 12

# assumes this script lives in MARC/PerformanceEvaluation/ and ARC_Generator_JSONs
# lives in MARC/ — adjust the number of .parent calls if your layout differs
PROJECT_ROOT = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = PROJECT_ROOT / "ARC_Generator_JSONs"

TEST_SET_DIR = Path("test_sets")
TEST_SET_DIR.mkdir(exist_ok=True)


def arc_task_to_json_dict(arc_task) -> dict:
    """Convert an ARCTask (raw ColorMatrix-based) into the same dict shape
    load_arc_task_from_json expects."""
    return {
        "train": [
            {"input": pair.input.matrix.tolist(), "output": pair.output.matrix.tolist()}
            for pair in arc_task.train
        ],
        "test": [
            {"input": pair.input.matrix.tolist(), "output": pair.output.matrix.tolist()}
            for pair in arc_task.test
        ],
    }


def build_task_id(template_name: str, series_length: int, repetition: int) -> str:
    return f"{template_name}_L{series_length}_rep{repetition}"


def main():
    """generates a test-set with a given seed, and saves it to test_sets/test_set{seed}.json"""
    templates = {
        name: load_arc_task_from_json(f"{name}.json", str(TEMPLATES_DIR)).to_abstract_task()
        for name in TEMPLATE_NAMES
    }

    transforms = [Duplicate(), Mirror(), Recolor(), Rotate(), Translate()]
    conditions = [ConditionColor(), ConditionPosition(), ConditionShape()]

    entries = []
    all_mismatches = []
    for template_name in TEMPLATE_NAMES:
        template = templates[template_name]
        for length in SERIES_LENGTHS:
            single_template_set = generate_test_set(
                [template], [length], transforms, conditions, TASKS_PER_COMBINATION
            )
            for repetition, (task, series) in enumerate(single_template_set):
                task_id = build_task_id(template_name, length, repetition)
                raw_arc_task = abstract_task_to_arc_task(task)

                entries.append({
                    "task_id": task_id,
                    "template": template_name,
                    "series_length": length,
                    "repetition": repetition,
                    "ground_truth_series": [repr(t) for t in series],
                    "task": arc_task_to_json_dict(raw_arc_task),
                })

    if all_mismatches:
        print(f"\n!!! {len(all_mismatches)} object-count mismatches found during JSON round-trip:")
        for m in all_mismatches:
            print(" ", m)
    else:
        print("\nNo object-count mismatches found during JSON round-trip.")

    out_path = TEST_SET_DIR / f"test_set{SEED}.json"
    with open(out_path, "w") as f:
        json.dump(entries, f, indent=2)
    print(f"Saved {len(entries)} tasks to {out_path}")


if __name__ == '__main__':
    random.seed(SEED)
    main()
