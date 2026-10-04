"""Record installed distribution license metadata and notice hashes."""
import hashlib
import json
from importlib import metadata
from pathlib import Path

names = [line.split('==')[0] for line in Path('requirements-lock.txt').read_text(encoding='utf-8-sig').splitlines() if '==' in line]
inventory = []
for name in names:
    dist = metadata.distribution(name)
    notices = []
    for file in dist.files or []:
        if any(word in str(file).upper() for word in ('LICENSE', 'LICENCE', 'COPYING', 'NOTICE')):
            path = dist.locate_file(file)
            if path.is_file():
                notices.append({'file': str(file), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()})
    declared = dist.metadata.get('License-Expression') or dist.metadata.get('License') or ''
    classifiers = [v for v in dist.metadata.get_all('Classifier', []) if v.startswith('License ::')]
    inventory.append({'name': name, 'version': dist.version,
                       'declared_license': declared.splitlines()[0] if declared else classifiers,
                       'notice_files': notices, 'project_urls': dist.metadata.get_all('Project-URL', [])})
Path('evidence/dependency-licenses.json').write_text(json.dumps(inventory, indent=2) + '\n')
print(f'Recorded license metadata and notice hashes for {len(inventory)} distributions')
