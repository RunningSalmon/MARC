import json
from pathlib import Path
from collections import defaultdict

import matplotlib.pyplot as plt
import numpy as np

RESULTS_DIR = Path("results")
TEMPLATES = ['T1', 'T2', 'T3', 'T4', 'T5']
SERIES_LENGTHS = [1, 3, 5]
COLORS = ['blue', 'orange', 'green', 'red', 'purple']
LINESTYLES = ['-', '--', '-.', ':', (0, (3, 1, 1, 1))]
SEED = 12


def load_results(config_name):
    path = RESULTS_DIR / f"{config_name}{SEED}.json"
    with open(path) as f:
        return json.load(f)


def aggregate(task_results):
    """Turn the flat list of per-task results back into the
    {template: {series_length: {'solved':.., 'total':.., 'steps':[...], 'failure_reasons': {...}}}}
    shape needed for plotting (failure_reasons is extra, kept for the discussion section)."""
    agg = {t: {l: {'solved': 0, 'total': 0, 'steps': [], 'failure_reasons': {}} for l in SERIES_LENGTHS}
           for t in TEMPLATES}
    for r in task_results:
        bucket = agg[r['template']][r['series_length']]
        bucket['total'] += 1
        if r['solved']:
            bucket['solved'] += 1
            bucket['steps'].append(r['steps'])
        else:
            reason = r.get('failure_reason', 'unknown')
            bucket['failure_reasons'][reason] = bucket['failure_reasons'].get(reason, 0) + 1
    return agg


def plot_results(results, config_name):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(7, 10))

    for template, color, ls in zip(TEMPLATES, COLORS, LINESTYLES):
        solve_rates = [
            results[template][l]['solved'] / results[template][l]['total'] * 100
            if results[template][l]['total'] > 0 else 0
            for l in SERIES_LENGTHS
        ]
        ax1.plot(SERIES_LENGTHS, solve_rates, marker='o', label=template,
                 color=color, linestyle=ls, alpha=0.85, linewidth=2)

    ax1.set_xlabel('Series Length')
    ax1.set_ylabel('Solved (%)')
    ax1.set_title(f'{config_name}: Solve Rate')
    ax1.legend()
    ax1.set_xticks(SERIES_LENGTHS)
    ax1.set_ylim(0, 108)
    ax1.set_yticks(range(0, 101, 20))

    for template, color, ls in zip(TEMPLATES, COLORS, LINESTYLES):
        mean_steps = [
            np.mean(results[template][l]['steps'])
            if results[template][l]['steps'] else 0
            for l in SERIES_LENGTHS
        ]
        ax2.plot(SERIES_LENGTHS, mean_steps, marker='o', label=template,
                 color=color, linestyle=ls, alpha=0.85, linewidth=2)

    ax2.set_xlabel('Series Length')
    ax2.set_ylabel('Mean Steps')
    ax2.set_title(f'{config_name}: Search Efficiency')
    ax2.legend()
    ax2.set_xticks(SERIES_LENGTHS)

    plt.tight_layout()
    plt.savefig(f'Results_{config_name}.png', dpi=150)
    plt.show()


if __name__ == '__main__':
    for config_name in ["Full", "Full_unconditioned", "Object_based_only", "Statistics_only"]:
        task_results = load_results(config_name)
        agg = aggregate(task_results)
        plot_results(agg, config_name)