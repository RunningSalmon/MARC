"""
Extract a single ARC task from a generated test set, given its template,
series length, and repetition (i.e. its task_id).

Assumes the test set was created with PerformanceEvaluation/generate_test_set.py
and is stored at test_sets/test_set{SEED}.json, with each entry shaped like:

{
    "task_id": "T2_L3_rep1",
    "template": "T2",
    "series_length": 3,
    "repetition": 1,
    "ground_truth_series": [...],
    "task": {"train": [...], "test": [...]}
}

Usage:
    # by explicit task_id
    python extract_task.py --seed 12 --task_id T2_L3_rep1

    # by components (equivalent to the task_id above)
    python extract_task.py --seed 12 --template T2 --series_length 3 --repetition 1

    # write the extracted ARC task (train/test matrices only) to its own file
    python extract_task.py --seed 12 --task_id T2_L3_rep1 --output extracted/T2_L3_rep1.json

    # also print the ground truth transformation series used to generate it
    python extract_task.py --seed 12 --task_id T2_L3_rep1 --show_series
"""

import argparse
import json
import tempfile
from pathlib import Path

TEST_SET_DIR = Path("test_sets")


def build_task_id(template_name: str, series_length: int, repetition: int) -> str:
    return f"{template_name}_L{series_length}_rep{repetition}"


def load_test_set(seed: int, test_set_dir: Path = TEST_SET_DIR) -> list[dict]:
    """loads a test set with a given seed"""
    path = test_set_dir / f"test_set{seed}.json"
    if not path.exists():
        raise FileNotFoundError(f"No test set found at {path}")
    with open(path) as f:
        return json.load(f)


def find_entry(entries: list[dict], task_id: str) -> dict:
    """finds the entry with the given task_id in the given list of entries"""
    for entry in entries:
        if entry["task_id"] == task_id:
            return entry
    available = ", ".join(e["task_id"] for e in entries)
    raise KeyError(f"task_id '{task_id}' not found in test set. Available: {available}")


def extract_task(
        seed: int,
        task_id: str | None = None,
        template: str | None = None,
        series_length: int | None = None,
        repetition: int | None = None,
        test_set_dir: Path = TEST_SET_DIR,
) -> dict:
    """
    Returns the full entry (task_id, template, series_length, repetition,
    ground_truth_series, task) for the requested task.

    Either pass task_id directly, or all three of template/series_length/repetition.
    """
    if task_id is None:
        if template is None or series_length is None or repetition is None:
            raise ValueError(
                "Provide either task_id, or all of template, series_length, and repetition."
            )
        task_id = build_task_id(template, series_length, repetition)

    entries = load_test_set(seed, test_set_dir)
    return find_entry(entries, task_id)


def extract_task_as_arc_task(
        seed: int,
        task_id: str | None = None,
        template: str | None = None,
        series_length: int | None = None,
        repetition: int | None = None,
        test_set_dir: Path = TEST_SET_DIR,
):
    """
    Same lookup as extract_task(), but returns a real ARCTask object
    """
    from Datatypes.ARC_Task import load_arc_task_from_json  # local import: only needed here

    entry = extract_task(seed, task_id, template, series_length, repetition, test_set_dir)

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir) / f"{entry['task_id']}.json"
        with open(tmp_path, "w") as f:
            json.dump(entry["task"], f)
        arc_task = load_arc_task_from_json(tmp_path.name, tmp_dir)

    return arc_task


def print_matrix(matrix: list[list[int]]) -> None:
    for row in matrix:
        print(" ".join(str(cell) for cell in row))


if __name__ == "__main__":
    arc_task = extract_task_as_arc_task(seed=128, task_id="T3_L5_rep0")
    arc_task.to_abstract_task().to_matplot()
    # print(arc_task)
