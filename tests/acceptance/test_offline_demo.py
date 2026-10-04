import json
import os
import subprocess
import sys


def test_demo_with_python_egress_denied(tmp_path):
    guard = tmp_path / 'guard'
    guard.mkdir()
    (guard / 'sitecustomize.py').write_text('''import sys
def deny_network(event, args):
    if event in ('socket.__new__', 'socket.connect', 'socket.getaddrinfo'):
        raise PermissionError('offline acceptance: Python socket egress denied')
sys.addaudithook(deny_network)
''')
    env = {k: v for k, v in os.environ.items() if not any(s in k.upper() for s in ('API_KEY', 'TOKEN', 'SECRET'))}
    env['PYTHONPATH'] = str(guard)
    probe = subprocess.run([sys.executable, '-c', "import socket; socket.create_connection(('example.com',443))"], env=env, capture_output=True, timeout=10)
    assert probe.returncode != 0 and b'egress denied' in probe.stderr
    out = tmp_path / 'offline'
    completed = subprocess.run([sys.executable, '-m', 'fixtureforge', 'demo', '--offline',
                                '--output', str(out)], env=env, capture_output=True, timeout=130)
    assert completed.returncode == 0, completed.stdout + completed.stderr
    assert json.loads((out / 'rejected/inspection.json').read_text())['status'] == 'fail'
    assert json.loads((out / 'corrected/inspection.json').read_text())['status'] == 'pass'
    report = json.loads((out / 'inspection.json').read_text())
    assert report['mode'] == 'REPLAY'
    assert report['live_model_evaluation'] == 'not_run'
