import json
import subprocess
import sys

import pytest

from fixtureforge.models import AccessSpec


@pytest.mark.parametrize('payload', [
    {}, {'schema_version': '99'}, {'units': 'inch'},
    {'schema_version': '1.0', 'units': 'mm', 'parts': [], 'paths': []},
])
def test_incomplete_contract_never_clear(payload):
    with pytest.raises(ValueError):
        AccessSpec.model_validate(payload)


def test_cli_invalid_is_two(tmp_path):
    inp = tmp_path / 'invalid.json'
    inp.write_text('{"units":"inch"}')
    out = tmp_path / 'result'
    result = subprocess.run([sys.executable, '-m', 'fixtureforge', 'build', str(inp),
                             '--output', str(out)], capture_output=True, timeout=130)
    assert result.returncode == 2
    report = json.loads((out / 'inspection.json').read_text())
    assert report['status'] == 'inconclusive'


def test_result_schema(built):
    from pathlib import Path

    import jsonschema
    report = json.loads((built / 'inspection.json').read_text())
    schema = json.loads(Path('schemas/result-1.0.json').read_text())
    jsonschema.validate(report, schema)
    assert report['status'] == 'pass'
    assert all(c['status'] in ('pass', 'not_applicable') for c in report['checks'])
