"""Recompute all synthetic result summaries and one comparison chart."""
import json
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

from parity_ot.examples import run_all

ROOT = Path(__file__).resolve().parents[1]
output = ROOT / 'outputs'
(output / 'figures').mkdir(parents=True, exist_ok=True)
results = run_all()
(output / 'synthetic_bounds.json').write_text(json.dumps(results, indent=2) + '\n')

pairs = [
    ('Two dates: rally then fall', results['two_date_rally_decline']['ordinary_ot'],
     results['two_date_rally_decline']['martingale_ot']),
    ('Three dates: fall then rebound',
     results['three_date_rally_decline_rebound']['ordinary_ot'],
     results['three_date_rally_decline_rebound']['martingale_ot']),
    ('Three-date monitored upper barrier',
     results['three_date_discretely_monitored_upper_barrier_130']['ordinary_ot'],
     results['three_date_discretely_monitored_upper_barrier_130']['martingale_ot']),
]
fig, ax = plt.subplots(figsize=(10.2, 4.8))
for i,(name,ordinary,mart) in enumerate(pairs):
    y = 2.3-i
    ax.plot([100*ordinary[0],100*ordinary[1]], [y+0.14,y+0.14],
            marker='o', linewidth=3, label='Ordinary OT' if i==0 else None)
    ax.plot([100*mart[0],100*mart[1]], [y-0.14,y-0.14],
            marker='s', linewidth=3, label='Martingale OT' if i==0 else None)
ax.set_yticks([2.3,1.3,0.3], [x[0] for x in pairs])
ax.set_xlim(-1, 53)
ax.set_xlabel('Feasible normalized claim price (%)')
ax.set_title('Sharp bounds under identical synthetic marginal prices')
ax.grid(axis='x', alpha=.25)
ax.legend(loc='upper right', frameon=False)
fig.text(.08,.013,'Finite-state synthetic distributions; no observed exchange prices.\n'
        'MOT assumes a dynamically tradable, discounted martingale underlying.',fontsize=9)
fig.tight_layout(rect=(0,.08,1,1))
fig.savefig(output/'figures'/'transport_bound_comparison.png', dpi=180)
plt.close(fig)
print('Wrote', output/'synthetic_bounds.json')
print('Wrote', output/'figures'/'transport_bound_comparison.png')
