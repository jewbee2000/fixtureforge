import json
from pathlib import Path


def test_executed_comparison():
    result = json.loads(Path('evidence/baseline.json').read_text())
    assert set(result['cases']) == {'screw_tool', 'connector'}
    for case in result['cases'].values():
        assert case['endpoint_overlap_mm3'] == 0
        assert abs(case['swept_overlap_mm3'] - 4) < 1e-6
        assert case['cadclaw_static_collisions'] == 0
        assert case['cadclaw_sweep_collisions'] == 1
    assert result['roundtrip_volume_mm3'] == 1000
