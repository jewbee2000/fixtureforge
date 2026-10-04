import json

import pytest

from fixtureforge.models import FixtureSpec


def test_input_is_data_not_python(tmp_path):
    target = tmp_path / 'executed'
    payload = {'sensor_diameter_mm': f'__import__("pathlib").Path({str(target)!r}).touch()'}
    with pytest.raises(ValueError):
        FixtureSpec.model_validate_json(json.dumps(payload))
    assert not target.exists()
