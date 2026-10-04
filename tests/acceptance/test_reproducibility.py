import json
from pathlib import Path


def test_fresh_wheel_and_semantic_repeat():
    consumer = json.loads(Path('evidence/consumer.json').read_text())
    assert consumer['semantic_reproduction_equal']
    assert consumer['report_hashes']['sensor-18'] == consumer['report_hashes']['sensor-18-repeat']
    assert len(consumer['wheel_sha256']) == 64
    assert all(c['exit_code'] == (1 if 'blocked.json' in c['command'] else 0) for c in consumer['commands'])


def test_measured_performance_bounds():
    evidence = json.loads(Path('evidence/performance.json').read_text())
    assert len(evidence['runs']) == 3
    assert all(r['wall_seconds'] < 60 and r['peak_worker_rss_bytes'] < 2 * 1024**3
               for r in evidence['runs'])
