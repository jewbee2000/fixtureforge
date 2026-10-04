"""Independent mutations of exported geometry; never builder fault flags."""
import json
from pathlib import Path

import cadquery as cq
import pytest

from fixtureforge.access import evaluate_path
from fixtureforge.inspection import inspect_fixture
from fixtureforge.models import AccessSpec, FixtureSpec


@pytest.mark.parametrize('diameter', [12, 16, 20, 24, 32, 40])
def test_reference_family(diameter, tmp_path):
    from fixtureforge.api import build
    source = Path(f'examples/sensor_{diameter}mm.json')
    code, result = build(source, tmp_path / 'built')
    assert code == 0
    assert result['status'] == 'pass'


def seeded_cases(built):
    parts = {name: cq.importers.importStep(str(built / f'{name}.step')).val()
             for name in ('base', 'clamp')}

    def block(x, y, z, cx, cy, cz):
        return cq.Workplane('XY').box(x, y, z).translate((cx, cy, cz)).val()

    cases = {}
    cases['below_minimum_wall'] = dict(parts, clamp=parts['clamp'].cut(block(30, 60, 10, 0, 0, 38)))
    cases['connector_collision'] = dict(parts, base=parts['base'].fuse(block(3, 3, 20, 24, 0, 12)))
    cases['screw_head_collision'] = dict(parts, clamp=parts['clamp'].fuse(block(2, 4, 5, 3.5, 22.2, 27)))
    # A high bridge attached to the ring blocks the tool while the head seat is open.
    tower = block(0.8, 3, 22, 5.2, 14.5, 40)
    bridge = block(0.8, 12, 3, 5.2, 19.5, 49)
    cases['inaccessible_tool_path'] = dict(parts, clamp=parts['clamp'].fuse(tower).fuse(bridge))
    joined = parts['base'].fuse(parts['clamp']).fuse(block(4, 4, 4, 0, 26, 20))
    cases['merged_halves'] = {'base': joined, 'clamp': joined}
    cases['empty_solid'] = {'base': parts['base'], 'clamp': cq.Compound.makeCompound([])}
    cases['exceeds_build_volume'] = dict(parts, base=parts['base'].fuse(block(200, 4, 4, 0, 0, 2)))
    return cases


def test_all_seeded_causes(built, oracle, tmp_path):
    fixture = FixtureSpec.model_validate(json.loads((built / 'fixture.json').read_text()))
    access = AccessSpec.model_validate(json.loads((built / 'access.json').read_text()))
    cases = seeded_cases(built)
    assert set(cases) | {'impossible_pitch'} == set(oracle['invalid_cases'])
    with pytest.raises(ValueError, match='FF-01'):
        FixtureSpec(mount_pitch_y_mm=40)
    records = {}
    for name, parts in cases.items():
        checks = inspect_fixture(parts, fixture)
        if name not in ('empty_solid', 'merged_halves'):
            checks += [evaluate_path(p, parts) for p in access.paths]
        intended = oracle['invalid_cases'][name]
        assert any(c['status'] == 'fail' and c['requirement'] == intended for c in checks), (name, checks)
        if name == 'connector_collision':
            assert not any(c['requirement'] == 'FF-02' and c['status'] == 'fail' for c in checks)
        if name == 'inaccessible_tool_path':
            assert not any(c['id'].startswith('head-') and c['status'] == 'fail' for c in checks)
        records[name] = {'intended_requirement': intended, 'failed_checks': [c for c in checks if c['status'] == 'fail']}
    (tmp_path / 'seeded-failures.json').write_text(json.dumps(records, indent=2))
