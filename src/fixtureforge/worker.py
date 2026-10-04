"""Trusted fixed CAD operations. This resource worker is NOT a code sandbox."""
import sys
from pathlib import Path

from .files import import_parts, read_json, write_json
from .models import AccessSpec, FixtureSpec
from .report import result, write_report


def run(action, source, out):
    import cadquery as cq

    from .access import bounds, evaluate_path, swept_shape

    out = Path(out)
    if action == 'build':
        from .geometry import construct, export_fixture
        from .inspection import inspect_fixture
        spec = FixtureSpec.model_validate(read_json(source))
        parts = construct(spec)
        checks = inspect_fixture(parts, spec)
        if any(c['status'] == 'fail' for c in checks):
            write_report(out, result(checks))
            return 1
        export_fixture(parts, spec, out)
        return 0
    access = AccessSpec.model_validate(read_json(source))
    parts = import_parts(access, Path(source).parent)
    checks = []
    if action == 'verify':
        import trimesh

        from .inspection import check, inspect_fixture
        spec = FixtureSpec.model_validate(read_json(out / 'fixture.json'))
        checks.extend(inspect_fixture(parts, spec))
        assembly = cq.importers.importStep(str(out / 'assembly.step')).findSolid()
        checks.append(check('assembly-roundtrip', 'FF-08', len(assembly.Solids()) == 2
                            and assembly.isValid() and abs(assembly.Volume() - sum(p.Volume() for p in parts.values())) < 0.01,
                            'Assembly STEP preserves two solids and per-part volume'))
        for name, part in parts.items():
            mesh = trimesh.load_mesh(out / f'{name}.stl')
            import numpy as np
            ok = mesh.is_watertight and mesh.is_winding_consistent and mesh.volume > 0
            ok = ok and abs(mesh.volume - part.Volume()) / part.Volume() < 0.005
            ok = ok and np.allclose(mesh.bounds, bounds(part), atol=0.05)
            checks.append(check(f'{name}-stl', 'FF-08', bool(ok), 'STL watertight, oriented, bounds and volume within tolerance'))
    for path in access.paths:
        checks.append(evaluate_path(path, parts))
        sweep, _ = swept_shape(path, path.margin_mm)
        cq.exporters.export(sweep, str(out / f'sweep-{path.id}.step'))
    compound = cq.Compound.makeCompound(list(parts.values()))
    svg = cq.exporters.getSVG(compound, opts={'width': 950, 'height': 520, 'showAxes': True,
                                             'projectionDir': (1, -1, 0.8), 'showHidden': False})
    (out / 'dimensions.svg').write_text(svg, encoding='utf-8')
    checks.append(dict(id='physical-validation', requirement='FF-11', status='not_applicable',
                       message='Physical measurements and strength tests have not been performed.'))
    report = result(checks, assumptions=access.assumptions, datums=access.datums,
                    parts={name: {'bounds_mm': bounds(p), 'volume_mm3': p.Volume()} for name, p in parts.items()})
    write_report(out, report)
    write_json(out / 'input-access.json', access.model_dump(mode='json'))
    return 0 if report['status'] == 'pass' else 1


def main():
    action, source, out = sys.argv[1:]
    try:
        code = run(action, source, out)
    except Exception as error:
        write_report(Path(out), result([dict(id='execution', requirement='FF-19', status='inconclusive',
                                             message=f'{type(error).__name__}: {error}')]))
        code = 2
    raise SystemExit(code)


if __name__ == '__main__':
    main()
