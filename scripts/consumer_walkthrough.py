"""Agent-executed cold consumer walkthrough, outside the source checkout."""
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

from fixtureforge.files import digest

root = Path(__file__).resolve().parents[1]
consumer = Path(sys.argv[1]).resolve()
consumer.mkdir(parents=True, exist_ok=False)
started = time.perf_counter()
commands = []
env = dict(os.environ)
env.pop('PYTHONPATH', None)


def run(args, expected=0, limit=600):
    begun = time.perf_counter()
    completed = subprocess.run([str(a) for a in args], cwd=consumer, env=env,
                               capture_output=True, text=True, timeout=limit)
    record = {'command': [str(a) for a in args], 'exit_code': completed.returncode,
              'elapsed_seconds': time.perf_counter() - begun}
    commands.append(record)
    (consumer / f'command-{len(commands)}.log').write_text(completed.stdout + completed.stderr, encoding='utf-8')
    if completed.returncode != expected:
        raise RuntimeError(f'Expected {expected}, got {completed.returncode}: {record}')
    return completed


run([sys.executable, '-m', 'venv', consumer / '.venv'])
python = consumer / '.venv/Scripts/python.exe'
shutil.copy2(root / 'requirements-runtime-lock.txt', consumer / 'requirements-runtime-lock.txt')
run([python, '-m', 'pip', 'install', '-r', 'requirements-runtime-lock.txt'])
wheel = root / 'dist/fixtureforge-0.1.0-py3-none-any.whl'
shutil.copy2(wheel, consumer / wheel.name)
run([python, '-m', 'pip', 'install', '--no-deps', wheel.name])
run([python, '-m', 'pip', 'check'])
installation_seconds = time.perf_counter() - started
external = root / 'artifacts/external-source'
shutil.copy2(external / 'bracket.step', consumer / 'bracket.step')
contract = {
    'schema_version': '1.0', 'units': 'mm',
    'parts': [{'id': 'my-bracket', 'file': 'bracket.step', 'sha256': digest(consumer / 'bracket.step')}],
    'paths': [{'id': 'my-connector', 'envelope': {'kind': 'box', 'size_mm': [3, 2, 2]},
               'start_mm': [-12, 0, 5], 'end_mm': [12, 0, 5], 'occupied': ['my-bracket']}],
    'assumptions': ['Agent-executed clean consumer. Non-default connector, independently authored synthetic STEP.']}
(consumer / 'blocked.json').write_text(json.dumps(contract, indent=2) + '\n')
run([python, '-m', 'fixtureforge', 'inspect', 'blocked.json', '--output', 'blocked'], expected=1)
contract['paths'][0]['start_mm'][1] = 5
contract['paths'][0]['end_mm'][1] = 5
(consumer / 'corrected.json').write_text(json.dumps(contract, indent=2) + '\n')
run([python, '-m', 'fixtureforge', 'inspect', 'corrected.json', '--output', 'corrected'])
fixture = {'schema_version': '1.0', 'units': 'mm', 'sensor_diameter_mm': 18,
           'sensor_length_mm': 35, 'mount_pitch_x_mm': 36, 'mount_pitch_y_mm': 60}
(consumer / 'sensor-18.json').write_text(json.dumps(fixture, indent=2) + '\n')
run([python, '-m', 'fixtureforge', 'build', 'sensor-18.json', '--output', 'sensor-18'])
run([python, '-m', 'fixtureforge', 'build', 'sensor-18.json', '--output', 'sensor-18-repeat'])
first = json.loads((consumer / 'sensor-18/inspection.json').read_text())
second = json.loads((consumer / 'sensor-18-repeat/inspection.json').read_text())
assert first == second, 'Semantic inspection differs between identical builds'
assert first['status'] == 'pass'
result = {
    'label': 'Agent-executed consumer walkthrough; practitioner validation unverified',
    'consumer_directory': str(consumer), 'installation_seconds': installation_seconds,
    'total_seconds': time.perf_counter() - started,
    'package_source_edited': False, 'commands': commands,
    'configuration_bytes': (consumer / 'blocked.json').stat().st_size,
    'configuration_lines': len((consumer / 'blocked.json').read_text().splitlines()),
    'consumer_code_lines': 0, 'nondefault_fixture': fixture,
    'expected_failure_exit': 1, 'corrected_exit': 0, 'semantic_reproduction_equal': True,
    'wheel_sha256': digest(wheel), 'runtime_lock_sha256': digest(consumer / 'requirements-runtime-lock.txt'),
    'report_hashes': {f: digest(consumer / f / 'inspection.json') for f in ('blocked', 'corrected', 'sensor-18', 'sensor-18-repeat')},
    'source_provenance': json.loads((consumer / 'corrected/manifest.json').read_text()),
}
(root / 'evidence/consumer.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({k: v for k, v in result.items() if k not in ('commands', 'source_provenance')}, indent=2))
