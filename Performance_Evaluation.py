from Datatypes.ARC_Task import load_arc_task_from_json
from Evaluation.Feature_Color import FeatureColor
from Evaluation.Feature_Position import FeaturePosition
from Evaluation.Feature_Shape import FeatureShape
from Evaluation.Statistic_Number_Of_Edges import NumberOfEdges
from Evaluation.Statistic_Number_Of_Objects import NumberOfObjects
from Evaluation.Statistic_Pixels_Correct import PixelsCorrect
from Evaluation.Statistic_Pixels_Per_Color import PixelsPerColor
from Task_Generation.Matrix_Transformation import *
from MDL_Search.MDLSearch import *
from Transformations.Duplicate import Duplicate
from Transformations.Mirror import Mirror
from Transformations.Recolor import Recolor
from Transformations.Rotate import Rotate
from Transformations.Translate import Translate

template_1 = load_arc_task_from_json("T1.json", "ARC_Generator_JSONs").to_abstract_task()
template_2 = load_arc_task_from_json("T2.json", "ARC_Generator_JSONs").to_abstract_task()
template_3 = load_arc_task_from_json("T3.json", "ARC_Generator_JSONs").to_abstract_task()
template_4 = load_arc_task_from_json("T4.json", "ARC_Generator_JSONs").to_abstract_task()
template_5 = load_arc_task_from_json("T5.json", "ARC_Generator_JSONs").to_abstract_task()

eval_features = [FeatureColor(),
                 FeaturePosition(),
                 FeatureShape()]
statistics = [NumberOfEdges(),
              NumberOfObjects(),
              PixelsCorrect(),
              PixelsPerColor(), ]
transforms = [Duplicate(),
              Mirror(),
              Recolor(),
              Rotate(),
              Translate(), ]
conditions = [ConditionColor(),
              ConditionPosition(),
              ConditionShape(), ]

def run_on_test_set(test_set, transforms, eval_features, statistics, conditions):
    for task, series in test_set:
        solution, visited, steps = mdl_search(task, transforms, eval_features, statistics, conditions)
        if solution:
            correct_solution = transform_and_evaluate_test_trials(task, solution)


import matplotlib.pyplot as plt
import numpy as np


def run_configuration(test_set, transforms, eval_features, statistics, conditions):
    # results[template_idx][series_length] = (solve_rate, mean_steps)
    templates = ['T1', 'T2', 'T3', 'T4', 'T5']
    series_lengths = [1, 3, 5]

    # organize results by template and series length
    results = {t: {l: {'solved': 0, 'total': 0, 'steps': []}
                   for l in series_lengths}
               for t in templates}

    for i, (task, series) in enumerate(test_set):
        template_idx = i // (len(series_lengths) * 5)  # 5 tasks per combination
        series_length_idx = (i // 5) % len(series_lengths)
        template = templates[template_idx]
        series_length = series_lengths[series_length_idx]

        solution, visited, steps = mdl_search(task, transforms, eval_features, statistics, conditions)
        results[template][series_length]['total'] += 1

        if solution and transform_and_evaluate_test_trials(task, solution):
            results[template][series_length]['solved'] += 1
            results[template][series_length]['steps'].append(steps)
            print(f"Solved {templates[template_idx]} in {steps} steps. Iteration {i}.")
        else:
            print(f"Failed to solve {templates[template_idx]}. Iteration {i}.")

    return results


def plot_results(results, config_name):
    templates = ['T1', 'T2', 'T3', 'T4', 'T5']
    series_lengths = [1, 3, 5]
    colors = ['blue', 'orange', 'green', 'red', 'purple']
    linestyles = ['-', '--', '-.', ':', (0, (3, 1, 1, 1))]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    # Plot 1: Solve rate
    for template, color, ls in zip(templates, colors, linestyles):
        solve_rates = [
            results[template][l]['solved'] / results[template][l]['total'] * 100
            if results[template][l]['total'] > 0 else 0
            for l in series_lengths
        ]
        ax1.plot(series_lengths, solve_rates, marker='o', label=template,
                 color=color, linestyle=ls, alpha=0.85, linewidth=2)

    ax1.set_xlabel('Series Length')
    ax1.set_ylabel('Solved (%)')
    ax1.set_title(f'{config_name}: Solve Rate')
    ax1.legend()
    ax1.set_xticks(series_lengths)
    ax1.set_ylim(0, 108)
    ax1.set_yticks(range(0, 101, 20))

    # Plot 2: Mean steps
    for template, color, ls in zip(templates, colors, linestyles):
        mean_steps = [
            np.mean(results[template][l]['steps'])
            if results[template][l]['steps'] else 0
            for l in series_lengths
        ]
        ax2.plot(series_lengths, mean_steps, marker='o', label=template,
                 color=color, linestyle=ls, alpha=0.85, linewidth=2)

    ax2.set_xlabel('Series Length')
    ax2.set_ylabel('Mean Steps')
    ax2.set_title(f'{config_name}: Search Efficiency')
    ax2.legend()
    ax2.set_xticks(series_lengths)

    plt.tight_layout()
    plt.savefig(f'{config_name}.png', dpi=150)
    plt.show()

if __name__ == '__main__':
    test_set = generate_test_set([template_1, template_2, template_3, template_4, template_5], [1, 3, 5],
                                           transforms, conditions, 5)
    # Full configuration
    results_full = run_configuration(test_set, transforms, eval_features, statistics, conditions)
    plot_results(results_full, 'Full')

    # Full unconditioned
    results_unconditioned = run_configuration(test_set, transforms, eval_features, statistics, [])
    plot_results(results_unconditioned, 'Full_unconditioned')

    # Object-based only
    results_obj_based = run_configuration(test_set, transforms, eval_features, [], [])
    plot_results(results_obj_based, 'Object_based_only')

    # Statistics only
    results_stats = run_configuration(test_set, transforms, [], statistics, [])
    plot_results(results_stats, 'Statistics_only')