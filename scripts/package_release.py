"""Build an offline-installable wheel with immutable source provenance."""
import hashlib
import json
import shutil
import subprocess
import sys
from importlib import metadata
from pathlib import Path

from packaging.requirements import Requirement
from packaging.utils import canonicalize_name

root = Path(__file__).resolve().parents[1]
pending = ['cadquery', 'pydantic', 'psutil', 'trimesh']
names = set()
while pending:
    name = canonicalize_name(pending.pop())
    if name in names:
        continue
    names.add(name)
    for raw in metadata.requires(name) or []:
        req = Requirement(raw)
        if req.marker is None or req.marker.evaluate({'extra': ''}):
            pending.append(req.name)
runtime = root / 'requirements-runtime-lock.txt'
runtime.write_text(''.join(f'{name}=={metadata.version(name)}\n' for name in sorted(names)))

stage = root / 'artifacts/package-source'
stage.mkdir(parents=True, exist_ok=True)
shutil.copytree(root / 'src', stage / 'src', dirs_exist_ok=True, ignore=shutil.ignore_patterns('__pycache__', '*.egg-info'))
for file in ('pyproject.toml', 'LICENSE'):
    shutil.copy2(root / file, stage / file)
def git(*args):
    return subprocess.check_output(['git', '-c', f'safe.directory={root.as_posix()}', *args], text=True).strip()
def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()
info = dict(source_commit=git('rev-parse', 'HEAD'), source_dirty=bool(git('status', '--porcelain')),
            lock_sha256=sha(root / 'requirements-lock.txt'),
            oracle_sha256=sha(root / 'tests/oracle/reference.json'),
            source_files={p.relative_to(root).as_posix(): sha(p) for p in (root / 'src').rglob('*.py')})
(stage / 'src/fixtureforge/_provenance.json').write_text(json.dumps(info, indent=2) + '\n')
subprocess.run([sys.executable, '-m', 'build', '--wheel', '--no-isolation',
                '--outdir', str(root / 'dist'), str(stage)], check=True)
