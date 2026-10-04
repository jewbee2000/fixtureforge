import json
import time

import pytest

from fixtureforge.api import build, inspect
from fixtureforge.models import AccessSpec


@pytest.mark.parametrize('limit', [{'timeout': 0.001}, {'memory_mb': 1}])
def test_cad_worker_is_killable(tmp_path, limit):
    started = time.perf_counter()
    code, report = build('examples/sensor_24mm.json', tmp_path / 'limited', **limit)
    assert code == 2 and report['status'] == 'inconclusive'
    assert time.perf_counter() - started < 10
    assert report['checks'][0]['requirement'] == 'FF-20'


def test_json_limit_and_part_limit(tmp_path):
    source = tmp_path / 'huge.json'
    source.write_text(' ' * (256 * 1024 + 1))
    code, report = inspect(source, tmp_path / 'rejected')
    assert code == 2 and '256 KiB' in report['checks'][0]['message']
    part = dict(id='p', file='p.step', sha256='0' * 64)
    with pytest.raises(ValueError):
        AccessSpec(schema_version='1.0', units='mm', parts=[part] * 21, paths=[])


def test_large_step_is_rejected_before_import(tmp_path, built):
    spec = json.loads((built / 'access.json').read_text())
    source = tmp_path / 'large.step'
    with source.open('wb') as f:
        f.truncate(10 * 1024 * 1024 + 1)
    spec['parts'][0]['file'] = 'large.step'
    access = tmp_path / 'access.json'
    access.write_text(json.dumps(spec))
    code, report = inspect(access, tmp_path / 'out')
    assert code == 2 and '10 MiB' in report['checks'][0]['message']
