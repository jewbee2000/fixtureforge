"""Retain independent defects and their complete inspection results."""
import importlib.util
import json
from pathlib import Path

import cadquery as cq

from fixtureforge.access import evaluate_path
from fixtureforge.inspection import inspect_fixture
from fixtureforge.models import AccessSpec, FixtureSpec
from fixtureforge.report import result, write_report

module_spec = importlib.util.spec_from_file_location('mutations', 'tests/acceptance/test_case_inventory.py')
module = importlib.util.module_from_spec(module_spec)
module_spec.loader.exec_module(module)
built = Path('artifacts/first-24')
fixture = FixtureSpec.model_validate_json((built / 'fixture.json').read_text())
access = AccessSpec.model_validate_json((built / 'access.json').read_text())
summary = {}
for name, parts in module.seeded_cases(built).items():
    out = Path('artifacts/seeded-failures-v2') / name
    out.mkdir(parents=True, exist_ok=True)
    for part_id, part in parts.items():
        if part.Solids():
            cq.exporters.export(part, str(out / f'{part_id}.step'))
        else:
            (out / f'{part_id}-empty.json').write_text('{"defect":"empty BREP compound"}\n')
    checks = inspect_fixture(parts, fixture)
    if name not in ('empty_solid', 'merged_halves'):
        checks += [evaluate_path(p, parts) for p in access.paths]
    report = result(checks)
    write_report(out, report)
    summary[name] = {'status': report['status'], 'failed': [c['id'] for c in checks if c['status'] == 'fail'],
                     'requirements': sorted({c['requirement'] for c in checks if c['status'] == 'fail'})}
summary['impossible_pitch'] = {'status': 'rejected_input', 'requirements': ['FF-01'], 'mount_pitch_y_mm': 40}
Path('evidence/seeded-failures.json').write_text(json.dumps(summary, indent=2) + '\n')
