import json
from pathlib import Path


def test_executed_consumer_evidence():
    record = json.loads(Path('evidence/consumer.json').read_text())
    assert record['package_source_edited'] is False
    assert record['expected_failure_exit'] == 1
    assert record['corrected_exit'] == 0
    assert record['semantic_reproduction_equal'] is True
    assert record['nondefault_fixture']['sensor_diameter_mm'] == 18
    assert record['consumer_code_lines'] == 0
    assert record['source_provenance']['source_commit'] != 'unavailable'
