import json
import subprocess
import sys
from pathlib import Path

import pytest

from fixtureforge.api import inspect


def test_external_bracket_and_repair(tmp_path):
    source = tmp_path / 'external'
    subprocess.run([sys.executable, 'scripts/external_example.py', str(source)], check=True, timeout=60)
    assert 'fixtureforge' not in Path('scripts/external_example.py').read_text().split('import hashlib')[1]
    code, failed = inspect(source / 'blocked.json', tmp_path / 'blocked')
    assert code == 1
    assert failed['checks'][0]['pairs'][0]['overlap_mm3'] == pytest.approx(4, abs=1e-6)
    code, passed = inspect(source / 'clear.json', tmp_path / 'clear')
    assert code == 0
    assert passed['checks'][0]['nominal_clearance_mm'] == pytest.approx(2, abs=1e-6)
    changed = json.loads((source / 'blocked.json').read_text())
    changed['parts'][0]['sha256'] = '0' * 64
    (source / 'stale.json').write_text(json.dumps(changed))
    code, stale = inspect(source / 'stale.json', tmp_path / 'stale')
    assert code == 2 and stale['status'] == 'inconclusive'
