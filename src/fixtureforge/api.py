"""Public bounded API. All kernel work runs in killable fresh processes."""
import importlib.metadata
import math
import os
import platform
import subprocess
import sys
import time
from pathlib import Path

import psutil

from .files import digest, read_json, write_json
from .report import result, write_report


def prepare_output(output):
    path = Path(output)
    if '..' in path.parts:
        raise ValueError('output path traversal is not allowed')
    if any(p.is_symlink() for p in (path, *path.parents)):
        raise ValueError('output symlinks are not allowed')
    path = path.resolve()
    path.mkdir(parents=True, exist_ok=True)
    if any(path.iterdir()):
        raise ValueError('output directory must be empty; choose a new run directory')
    return path


def run_worker(action, source, out, timeout, memory_mb):
    started = time.perf_counter()
    peak = 0
    reason = None
    with (out / f'{action}.log').open('w', encoding='utf-8') as log:
        env = dict(os.environ)
        env['OMP_NUM_THREADS'] = '1'
        process = subprocess.Popen([sys.executable, '-m', 'fixtureforge.worker', action,
                                    str(source), str(out)], stdout=log, stderr=log, env=env)
        monitored = psutil.Process(process.pid)
        while process.poll() is None:
            try:
                memory = monitored.memory_info().rss
                memory += sum(c.memory_info().rss for c in monitored.children(recursive=True))
                peak = max(peak, memory)
            except psutil.Error:
                pass
            if time.perf_counter() - started > timeout:
                reason = 'elapsed-time limit exceeded; CAD worker terminated'
            elif peak > memory_mb * 1024 * 1024:
                reason = 'memory limit exceeded; CAD worker terminated'
            if reason:
                try:
                    for child in monitored.children(recursive=True):
                        try:
                            child.kill()
                        except psutil.Error:
                            pass
                    process.kill()
                except (psutil.Error, OSError):
                    pass  # Worker may exit between poll and termination.
                break
            time.sleep(0.02)
        code = process.wait()
    stats = dict(action=action, elapsed_seconds=time.perf_counter() - started,
                 peak_rss_bytes=peak, exit_code=code, deadline_seconds=timeout,
                 memory_limit_mb=memory_mb)
    if reason or code not in (0, 1, 2):
        message = reason or f'CAD worker terminated unexpectedly ({code}); see {action}.log'
        write_report(out, result([dict(id='worker-limit', requirement='FF-20', status='inconclusive', message=message)]))
        return 2, stats
    if code and not (out / 'inspection.json').exists():
        write_report(out, result([dict(id='worker-error', requirement='FF-19', status='inconclusive',
                                      message=f'Worker failed before writing result; see {action}.log')]))
        return 2, stats
    return code, stats


def provenance(source, out, stats):
    root = Path(__file__).resolve().parents[2]

    def git(*args):
        command = ['git', '-c', f'safe.directory={root.as_posix()}', '-C', str(root), *args]
        try:
            completed = subprocess.run(command, capture_output=True, text=True, timeout=5)
        except (OSError, subprocess.TimeoutExpired):
            return 'unavailable'
        return completed.stdout.strip() if completed.returncode == 0 else 'unavailable'

    lock = root / 'requirements-lock.txt'
    oracle = root / 'tests/oracle/reference.json'
    embedded = Path(__file__).with_name('_provenance.json')
    package_info = read_json(embedded) if embedded.exists() else {}
    write_json(out / 'manifest.json', {
        'schema_version': '1.0', 'input_sha256': digest(source) if Path(source).is_file() else None,
        'source_commit': package_info.get('source_commit', git('rev-parse', 'HEAD')),
        'source_dirty': package_info.get('source_dirty', git('status', '--porcelain') != ''),
        'lock_sha256': digest(lock) if lock.exists() else package_info.get('lock_sha256'),
        'oracle_sha256': digest(oracle) if oracle.exists() else package_info.get('oracle_sha256'),
        'source_files': package_info.get('source_files', {p.name: digest(p) for p in Path(__file__).parent.glob('*.py')}),
        'python': sys.version, 'platform': platform.platform(),
        'versions': {p: importlib.metadata.version(p) for p in ('fixtureforge', 'cadquery', 'cadquery-ocp', 'pydantic')},
        'workers': stats, 'assembly_transform': 'identity; mm; right handed X/Y/Z',
        'geometry_hashes': {p.name: digest(p) for p in out.glob('*.step')},
        'artifacts': {p.name: digest(p) for p in out.iterdir() if p.is_file() and p.name != 'manifest.json'},
        'telemetry': 'none', 'physical_tests': 'not_performed',
    })


def execute(action, source, output, timeout=120, memory_mb=2048):
    if not math.isfinite(timeout) or not 0 < timeout <= 120:
        raise ValueError('timeout must be finite, >0 and <=120 seconds')
    if not 1 <= memory_mb <= 2048:
        raise ValueError('memory_mb must be between 1 and 2048')
    out = prepare_output(output)
    source = Path(source).resolve()
    stats = []
    begun = time.perf_counter()
    try:
        # Reject oversized or malformed data before launching expensive kernel work.
        read_json(source)
        code, run = run_worker(action, source, out, timeout, memory_mb)
        stats.append(run)
        if action == 'build' and code == 0:
            remaining = max(0.001, timeout - (time.perf_counter() - begun))
            code, run = run_worker('verify', out / 'access.json', out, remaining, memory_mb)
            stats.append(run)
    except (ValueError, OSError) as error:
        write_report(out, result([dict(id='input', requirement='FF-19', status='inconclusive', message=str(error))]))
        code = 2
    provenance(source, out, stats)
    return code, read_json(out / 'inspection.json')


def build(spec_path, output, *, timeout=120, memory_mb=2048):
    return execute('build', spec_path, output, timeout, memory_mb)


def inspect(access_path, output, *, timeout=120, memory_mb=2048):
    return execute('inspect', access_path, output, timeout, memory_mb)
