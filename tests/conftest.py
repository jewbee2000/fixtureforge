import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(scope='session')
def built(tmp_path_factory):
    out = tmp_path_factory.mktemp('reference')
    result = subprocess.run([sys.executable, '-m', 'fixtureforge', 'build',
                             str(ROOT / 'examples/sensor_24mm.json'), '--output', str(out)],
                            capture_output=True, text=True, timeout=130)
    assert result.returncode == 0, result.stdout + result.stderr
    return out


@pytest.fixture(scope='session')
def oracle():
    return json.loads((ROOT / 'tests/oracle/reference.json').read_text())
