import hashlib
import json
from pathlib import Path

JSON_LIMIT = 256 * 1024
STEP_LIMIT = 10 * 1024 * 1024


def digest(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def read_json(path):
    path = Path(path)
    if path.stat().st_size > JSON_LIMIT:
        raise ValueError('JSON exceeds 256 KiB limit')

    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f'duplicate JSON key: {key}')
            result[key] = value
        return result

    return json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=unique)


def write_json(path, data):
    Path(path).write_text(json.dumps(data, indent=2, allow_nan=False) + '\n', encoding='utf-8')


def import_parts(spec, root):
    import re

    import cadquery as cq

    root = Path(root).resolve()
    result = {}
    face_count = 0
    for entry in spec.parts:
        path = (root / entry.file).resolve()
        if not path.is_relative_to(root):
            raise ValueError('STEP resolved outside input directory')
        if path.stat().st_size > STEP_LIMIT:
            raise ValueError('STEP exceeds 10 MiB limit')
        if digest(path) != entry.sha256:
            raise ValueError(f'{entry.id}: STEP hash does not match explicit selector')
        source = path.read_text(encoding='ascii', errors='replace')
        units = re.findall(r'SI_UNIT\s*\(\s*([^,]*),\s*\.METRE\.\s*\)', source)
        if not units or any(u.strip() != '.MILLI.' for u in units) or 'CONVERSION_BASED_UNIT' in source:
            raise ValueError(f'{entry.id}: STEP length units must be explicitly millimeters')
        roots = cq.importers.importStep(str(path)).vals()
        if not all(isinstance(s, cq.Shape) for s in roots):
            raise ValueError('STEP contains a non-shape root')
        obj = cq.Compound.makeCompound([s for s in roots if isinstance(s, cq.Shape)])
        solids = obj.Solids()
        if (len(solids) != 1 or not obj.isValid() or obj.Volume() <= 0
                or len(obj.Faces()) != len(solids[0].Faces())
                or len(obj.Edges()) != len(solids[0].Edges())):
            raise ValueError(f'{entry.id}: expected exactly one valid positive-volume solid')
        face_count += len(obj.Faces())
        if face_count > 2000:
            raise ValueError('assembly exceeds 2000 face limit')
        placed = solids[0].translate(entry.translation_mm)
        bb = placed.BoundingBox()
        if max(abs(getattr(bb, f'{a}{edge}')) for a in 'xyz' for edge in ('min', 'max')) > 1000:
            raise ValueError('placed geometry exceeds 1000 mm coordinate limit')
        result[entry.id] = placed
    return result
