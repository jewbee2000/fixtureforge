"""Synthetic MIT-licensed baseline, independent of fixtureforge package."""
import hashlib
import importlib.metadata as metadata
import json
import time
from pathlib import Path

import build123d as bd
import cadclaw
import cadquery as cq
import psutil
from cadclaw.interference import InterferenceCheck

out = Path('artifacts/baseline')
out.mkdir(parents=True, exist_ok=True)
started = time.perf_counter()
obstacle = cq.Workplane('XY').box(1, 1, 4).translate((0, 0, 5)).val()
bd_obstacle = bd.Pos(0, 0, 5) * bd.Box(1, 1, 4)
cases = {}
for name in ('screw_tool', 'connector'):
    if name == 'screw_tool':
        endpoint = cq.Solid.makeCylinder(1, 2, cq.Vector(0, 0, -1))
        swept = cq.Solid.makeCylinder(1, 12, cq.Vector(0, 0, -1))
        bd_swept = bd.Pos(0, 0, 5) * bd.Cylinder(1, 12)
    else:
        endpoint = cq.Workplane('XY').box(2, 2, 2).val()
        swept = cq.Workplane('XY').box(2, 2, 12).translate((0, 0, 5)).val()
        bd_swept = bd.Pos(0, 0, 5) * bd.Box(2, 2, 12)
    static = InterferenceCheck([obstacle, endpoint], lambda s: str(id(s))).run()
    full = InterferenceCheck([obstacle, swept], lambda s: str(id(s))).run()
    cq.exporters.export(cq.Compound.makeCompound([obstacle, endpoint]), str(out / f'{name}-static.step'))
    cq.exporters.export(cq.Compound.makeCompound([obstacle, swept]), str(out / f'{name}-swept.step'))
    cases[name] = {
        'endpoint_overlap_mm3': obstacle.intersect(endpoint).Volume(),
        'other_endpoint_overlap_mm3': obstacle.intersect(endpoint.translate((0, 0, 10))).Volume(),
        'swept_overlap_mm3': obstacle.intersect(swept).Volume(),
        'build123d_swept_overlap_mm3': (bd_obstacle & bd_swept).volume,
        'cadclaw_static_collisions': len(static.clips),
        'cadclaw_sweep_collisions': len(full.clips),
    }
cube = cq.Workplane('XY').box(10, 10, 10)
cq.exporters.export(cube, str(out / 'cube.step'))
volume = cq.importers.importStep(str(out / 'cube.step')).val().Volume()
module_path = Path(cadclaw.__file__).parent
result = {
    'cases': cases,
    'roundtrip_volume_mm3': round(volume, 9),
    'versions': {name: metadata.version(name) for name in ['cadclaw', 'cadquery', 'build123d', 'cadquery-ocp']},
    'cadclaw_source_sha256': {name: hashlib.sha256((module_path / name).read_bytes()).hexdigest()
                             for name in ['interference.py', 'disassembly.py']},
    'elapsed_seconds': time.perf_counter() - started,
    'rss_bytes_at_end': psutil.Process().memory_info().rss,
    'artifacts': {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in out.glob('*.step')},
    'provenance': 'Independently authored synthetic solids, MIT; no physical measurements',
}
Path('evidence/baseline.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
