"""Three measured CLI-equivalent runs; no universal performance claim."""
import json
import subprocess
import sys
import time
from pathlib import Path

root = Path(__file__).resolve().parents[1]
records = []
for index in range(3):
    out = root / f'artifacts/performance-{index}'
    started = time.perf_counter()
    result = subprocess.run([sys.executable, '-m', 'fixtureforge', 'build',
                             str(root / 'examples/sensor_24mm.json'), '--output', str(out)],
                            capture_output=True, text=True, timeout=125)
    manifest = json.loads((out / 'manifest.json').read_text())
    records.append({'command': result.args, 'exit_code': result.returncode,
                    'wall_seconds': time.perf_counter() - started,
                    'peak_worker_rss_bytes': max(w['peak_rss_bytes'] for w in manifest['workers']),
                    'input_sha256': manifest['input_sha256'], 'source_commit': manifest['source_commit'],
                    'source_dirty': manifest['source_dirty'], 'lock_sha256': manifest['lock_sha256'],
                    'oracle_sha256': manifest['oracle_sha256'], 'artifacts': manifest['artifacts']})
    assert result.returncode == 0
    assert records[-1]['wall_seconds'] < 60
    assert records[-1]['peak_worker_rss_bytes'] < 2 * 1024**3
output = {'machine': 'Dell XPS 15 9510; Intel i9-11900H; 8 cores/16 threads; 64 GiB; Windows 11 x64',
          'method': '3 serial fresh-interpreter 24 mm builds including fresh STEP verification; worker RSS sampled every 20 ms',
          'target_seconds': 60, 'deadline_seconds': 120, 'memory_limit_mb': 2048,
          'runs': records}
Path('evidence/performance.json').write_text(json.dumps(output, indent=2) + '\n')
print(json.dumps([{k: r[k] for k in ('exit_code', 'wall_seconds', 'peak_worker_rss_bytes')} for r in records]))
