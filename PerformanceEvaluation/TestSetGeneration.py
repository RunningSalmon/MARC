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
    load_arc_task_from_json expects, so it round-trips."""
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


def check_roundtrip_integrity(task, raw_arc_task, task_id):
    """Diagnostic: compares object counts (and, on mismatch, shapes/colors) between
    the abstract task straight out of generate_test_task and the same task after
    rasterizing to pixels and re-extracting objects via BFS. A mismatch here means
    the JSON round-trip is silently changing task difficulty (e.g. merging adjacent
    same-colored objects, or clipping objects at the matrix border)."""
    reextracted = raw_arc_task.to_abstract_task()

    mismatches = []
    for split_name, original_pairs, reext_pairs in [
        ("train", task.train, reextracted.train),
        ("test", task.test, reextracted.test),
    ]:
        for i, (orig_pair, reext_pair) in enumerate(zip(original_pairs, reext_pairs)):
            for side_name, orig_matrix, reext_matrix in [
                ("input", orig_pair.input, reext_pair.input),
                ("output", orig_pair.output, reext_pair.output),
            ]:
                orig_n = len(orig_matrix.abstract_objects)
                reext_n = len(reext_matrix.abstract_objects)
                if orig_n != reext_n:
                    mismatches.append(
                        f"{task_id} {split_name}[{i}].{side_name}: "
                        f"{orig_n} objects before roundtrip, {reext_n} after"
                    )
    return mismatches


def build_task_id(template_name: str, series_length: int, repetition: int) -> str:
    return f"{template_name}_L{series_length}_rep{repetition}"


def main():
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

                mismatches = check_roundtrip_integrity(task, raw_arc_task, task_id)
                all_mismatches.extend(mismatches)

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