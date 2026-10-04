import json

import cadquery as cq

from fixtureforge.api import inspect
from fixtureforge.files import digest


def test_multiple_solids_and_units_rejected(tmp_path):
    shape = cq.Workplane('XY').box(1, 1, 1).val()
    step = tmp_path / 'two.step'
    cq.exporters.export(cq.Compound.makeCompound([shape, shape.translate((5, 0, 0))]), str(step))
    payload = {'schema_version': '1.0', 'units': 'mm',
               'parts': [{'id': 'part', 'file': step.name, 'sha256': digest(step)}],
               'paths': [{'id': 'tool', 'envelope': {'kind': 'box', 'size_mm': [1, 1, 1]},
                          'start_mm': [0, 0, 10], 'end_mm': [0, 0, 5], 'occupied': ['part']}]}
    access = tmp_path / 'access.json'
    access.write_text(json.dumps(payload))
    code, report = inspect(access, tmp_path / 'multi')
    assert code == 2 and 'exactly one' in report['checks'][0]['message']
    cq.exporters.export(shape, str(step))
    step.write_text(step.read_text().replace('SI_UNIT(.MILLI.,.METRE.)', 'SI_UNIT($,.METRE.)'))
    payload['parts'][0]['sha256'] = digest(step)
    access.write_text(json.dumps(payload))
    code, report = inspect(access, tmp_path / 'units')
    assert code == 2 and 'millimeters' in report['checks'][0]['message']


def test_translated_part_changes_collision(tmp_path):
    step = tmp_path / 'cube.step'
    cq.exporters.export(cq.Workplane('XY').box(1, 1, 1).val(), str(step))
    payload = {'schema_version': '1.0', 'units': 'mm',
               'parts': [{'id': 'part', 'file': step.name, 'sha256': digest(step), 'translation_mm': [0, 0, 5]}],
               'paths': [{'id': 'tool', 'envelope': {'kind': 'box', 'size_mm': [1, 1, 1]},
                          'start_mm': [0, 0, 3], 'end_mm': [0, 0, 7], 'occupied': ['part']}]}
    access = tmp_path / 'access.json'
    access.write_text(json.dumps(payload))
    code, _ = inspect(access, tmp_path / 'blocked')
    assert code == 1
    payload['parts'][0]['translation_mm'] = [5, 0, 5]
    access.write_text(json.dumps(payload))
    code, _ = inspect(access, tmp_path / 'clear')
    assert code == 0
