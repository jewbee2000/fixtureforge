"""Observed YZ edges plus envelope bounds. Illustration never decides clearance."""
import json
from pathlib import Path

import cadquery as cq
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

root = Path('artifacts/replay')
fig, axes = plt.subplots(1, 2, figsize=(12, 7), sharex=True, sharey=True)
for ax, folder, title in zip(axes, ['rejected', 'corrected'], ['Rejected driver line', 'Corrected: driver at screw'], strict=True):
    for name, color in [('base', '#447e94'), ('clamp', '#be792e')]:
        shape = cq.importers.importStep(str(root / 'corrected' / f'{name}.step')).val()
        for edge in shape.Edges():
            points = [edge.positionAt(i / 30).toTuple() for i in range(31)]
            ax.plot([p[1] for p in points], [p[2] for p in points], color=color, linewidth=0.7)
    report = json.loads((root / folder / 'inspection.json').read_text())
    check = next(c for c in report['checks'] if c['id'] == 'tool-1')
    low, high = check['sweep_bounds_mm']
    color = '#b83631' if check['status'] == 'fail' else '#287955'
    ax.add_patch(Rectangle((low[1], low[2]), high[1]-low[1], high[2]-low[2], facecolor=color, edgecolor=color, alpha=0.22))
    ax.annotate('', xy=(check['end_mm'][1], check['end_mm'][2]), xytext=(check['start_mm'][1], check['start_mm'][2]), arrowprops=dict(arrowstyle='->', color=color, lw=2))
    ax.set_title(title + ' · ' + check['status'].upper(), color=color, fontsize=15)
    ax.set(xlabel='Y / mm', ylabel='Z / mm', xlim=(-40,40), ylim=(-3,80))
    ax.set_aspect('equal')
    ax.grid(alpha=0.2)
fig.suptitle('Full-path access check · deliberately seeded replay', fontsize=19)
fig.text(0.5, 0.025, 'Actual STEP edges, YZ projection; shaded rectangle is the swept tool envelope.\nComputed geometry only. This is not a live model trial or a physical measurement.', ha='center', fontsize=11)
fig.tight_layout(rect=(0,0.13,1,0.94))
fig.savefig('evidence/replay.png', dpi=150)
