# MARC: A Minimal Description Length Approach to Transformation Series Inference

MARC is a model that infers the series of transformations connecting the input and target
matrices of an ARC-like task, guided by the Minimal Description Length (MDL)
principle. Given input/target color-matrix pairs, MARC searches for the shortest,
best-fitting sequence of object-level transformations (recolor, translate, rotate,
mirror, duplicate with optional conditions on object features) that explains the
difference between them, using a beam search over transformation series ranked by
description length.

This repository contains the full implementation of MARC, together with the
experimental pipeline used to evaluate its performance. It is the codebase
accompanying the bachelor thesis *"MARC: A Minimal Description Length Approach
to Transformation Series Inference"* (Cognitive Modeling, University of Tübingen).

## How it works

1. **Object extraction:** Color matrices are decomposed into `AbstractObjects`
   (color, position, shape mask) via connected-component search, and stored as
   an `AbstractMatrix`.
2. **Transformations:** Five primitive transformations (Recolor, Translate,
   Rotate, Mirror, Duplicate) operate on abstract objects and can optionally be
   *conditioned* on an object feature (color, position, shape), so they only
   apply to a subset of objects.
3. **Evaluation:** Transformed matrices are scored against their targets either
   by **object-based evaluation** (comparing paired objects by color, position,
   shape) or, if no unambiguous object pairing exists, by **summary statistics**
   (pixels correct, pixels per color, number of objects, number of edges).
4. **MDL search:** Starting from an empty transformation series, MARC greedily
   expands the series with the lowest description length (negative log-likelihood
   of the transformation, weighted by its residual fitness score), using a
   beam-search heap, until a series is found that solves all training trials.

## Requirements

- Python 3.10+ (uses `list[...]`/`X | Y` type-hint syntax)
- `numpy`
- `matplotlib`
- `icontract`

```bash
pip install numpy matplotlib icontract
```

## Running an experiment

The `PerformanceEvaluation/` scripts form a small pipeline and are meant to be
run from within that directory:

```bash
cd PerformanceEvaluation

# 1. Generate a randomized test set from the templates in ARC_Generator_JSONs/
python TestSetGeneration.py        # -> test_sets/test_set{SEED}.json

# 2. Run all four algorithmic configurations (Full, Full_unconditioned,
#    Object_based_only, Statistics_only) on the generated test set
python RunExperiment.py            # -> results/{config}{SEED}.json

# 3. Plot solve rate and search efficiency per template/configuration
python PlotResults.py              # -> Results_{config}.png
```

A single task can be pulled out of a generated test set for inspection with:

```bash
python TestSetTaskExtraction.py    # or import extract_task_as_arc_task(...)
```

To experiment with MARC interactively on a single task (without the full
evaluation pipeline), see `Testing.py` in the repository root.

## Status

This is a research prototype developed as part of a bachelor thesis and is not
intended for production use. See the thesis for a full discussion of the model's
design choices, experimental results, and known limitations.