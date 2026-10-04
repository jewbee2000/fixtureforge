"""Render reimported STEP meshes to a local PNG without executing HTML."""
import sys
from pathlib import Path

import cadquery as cq
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

folder = Path(sys.argv[1])
target = Path(sys.argv[2])
fig = plt.figure(figsize=(12, 8), facecolor='#f0f3f2')
ax = fig.add_subplot(111, projection='3d')
ax.set_facecolor('#f0f3f2')
all_points = []
all_triangles = []
all_colors = []
for name, color in [('base', '#447e94'), ('clamp', '#d99043')]:
    shape = cq.importers.importStep(str(folder / f'{name}.step')).val()
    vertices, triangles = shape.tessellate(0.08, 0.1)
    points = np.array([v.toTuple() for v in vertices])
    all_points.extend(points)
    all_triangles.extend(points[np.array(triangles)])
    all_colors.extend([color] * len(triangles))
poly = Poly3DCollection(all_triangles, facecolors=all_colors, shade=True, linewidth=0, alpha=1)
ax.add_collection3d(poly)
coords = np.array(all_points)
low, high = coords.min(axis=0), coords.max(axis=0)
ax.set(xlim=(low[0]-4, high[0]+4), ylim=(low[1]-4, high[1]+4), zlim=(0, high[2]+5),
       xlabel='X / mm', ylabel='Y / mm', zlabel='Z / mm')
ax.set_box_aspect(high-low)
ax.view_init(elev=28, azim=-48)
fig.suptitle('FixtureForge · 24 mm synthetic sensor clamp', fontsize=20, color='#203440')
fig.text(0.5, 0.04, 'Reimported STEP geometry · base blue / clamp amber · 1 mm split gap\nNominal CAD only; no physical fit or strength measurements.',
         ha='center', fontsize=12, color='#203440')
target.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(target, dpi=160, bbox_inches='tight')
plt.close(fig)
