"""Measurements of reimported solids, independent of construction helpers."""
import math

import cadquery as cq
from OCP.BRepAdaptor import BRepAdaptor_Surface
from OCP.GeomAbs import GeomAbs_Cylinder, GeomAbs_Plane

from .access import bounds, overlap


def check(identity, requirement, passed, message, **data):
    return dict(id=identity, requirement=requirement, status='pass' if passed else 'fail',
                message=message, **data)


def inspect_fixture(parts, spec):
    checks = []
    valid = set(parts) == {'base', 'clamp'} and all(
        len(p.Solids()) == 1 and p.isValid() and p.Volume() > 0 for p in parts.values())
    checks.append(check('solid-count', 'FF-02', valid, 'Exactly two valid positive-volume single solids'))
    if not valid:
        return checks
    base, clamp = parts['base'], parts['clamp']
    checks.append(check('separate-halves', 'FF-02', overlap(base, clamp) <= 1e-7,
                        'Base and clamp remain separate'))
    measured = {}
    r = (spec.sensor_diameter_mm + spec.clearance_mm) / 2
    z_expected = spec.base_mm + r + spec.wall_mm
    for name, shape in parts.items():
        cylinders, planes = [], []
        for face in shape.Faces():
            adapter = BRepAdaptor_Surface(face.wrapped)
            if adapter.GetType() == GeomAbs_Cylinder:
                c = adapter.Cylinder()
                d, p = c.Axis().Direction(), c.Location()
                cylinders.append({'radius': c.Radius(), 'axis': [d.X(), d.Y(), d.Z()],
                                  'origin': [p.X(), p.Y(), p.Z()]})
            if adapter.GetType() == GeomAbs_Plane:
                p = adapter.Plane()
                if abs(p.Axis().Direction().Z()) > 0.999:
                    planes.append(p.Location().Z())
        bores = [c for c in cylinders if abs(c['axis'][0]) > 0.999]
        bore_ok = bool(bores) and all(abs(c['radius'] - r) * 2 <= 0.05
                    and abs(c['origin'][1]) <= 0.05 and abs(c['origin'][2] - z_expected) <= 0.05
                    for c in bores)
        checks.append(check(f'{name}-bore', 'FF-03', bore_ok, 'Bore cylinder radius and axis from STEP', cylinders=bores))
        bb = shape.BoundingBox()
        limits = [bb.xlen, bb.ylen, bb.zlen]
        checks.append(check(f'{name}-build-volume', 'FF-06', max(limits) <= 180.05,
                            'Per-part 180 mm build envelope', measured_mm=limits))
        # Full minimum annular band containment, not sampled wall rays.
        outer = cq.Solid.makeCylinder(r + 2.4, 20, cq.Vector(-10, 0, z_expected), cq.Vector(1, 0, 0))
        inner = cq.Solid.makeCylinder(r, 20, cq.Vector(-10, 0, z_expected), cq.Vector(1, 0, 0))
        shell = outer.cut(inner)
        half = cq.Workplane('XY').box(22, 200, 100).translate(
            (0, 0, z_expected - 50.5 if name == 'base' else z_expected + 50.5)).findSolid()
        required = shell.intersect(half)
        missing = required.cut(shape).Volume()
        checks.append(check(f'{name}-wall', 'FF-06', missing <= 1e-5,
                            'Minimum 2.4 mm radial material band over 20 mm support length',
                            missing_material_mm3=missing))
        downward = []
        for face in shape.Faces():
            if face.geomType() == 'PLANE':
                normal = face.normalAt()
                if normal.z < -0.7:
                    downward.append({'center_mm': face.Center().toTuple(), 'area_mm2': face.Area()})
        measured[name] = {'bounds_mm': bounds(shape), 'volume_mm3': shape.Volume(),
                          'downward_faces': downward,
                          'bed_face': 'Z=0 mounting face' if name == 'base' else 'split face; translate its minimum Z to 0 without rotation',
                          'overhang_warning': 'Downward faces and curved bore need slicer review in the stated orientation.'}
        if name == 'base':
            holes = [c for c in cylinders if abs(c['axis'][2]) > 0.999 and abs(c['origin'][0]) > 1]
            expected = [(x, y) for x in (-spec.mount_pitch_x_mm / 2, spec.mount_pitch_x_mm / 2)
                        for y in (-spec.mount_pitch_y_mm / 2, spec.mount_pitch_y_mm / 2)]
            holes_ok = len(holes) == 4 and all(any(
                math.dist(c['origin'][:2], pos) <= 0.05 and abs(c['radius'] - 2.25) <= 0.025
                for c in holes) for pos in expected)
            checks.append(check('mount-pattern', 'FF-03', holes_ok, 'Four measured mounting hole axes', holes=holes))
            thickness = any(abs(p - spec.base_mm) <= 0.05 for p in planes)
            checks.append(check('base-thickness-datums', 'FF-03', thickness and abs(bb.zmin) <= 0.05
                                and abs(bb.xmin + bb.xmax) <= 0.05 and abs(bb.ymin + bb.ymax) <= 0.05,
                                'Base planes and centered X/Y datums', horizontal_planes_mm=planes))
            # Independent continuous witness strip, away from intentional through holes.
            strip = cq.Workplane('XY').box(spec.mount_pitch_x_mm + 10, 1, 5,
                                           centered=(True, True, False)).findSolid()
            missing_base = strip.cut(base).Volume()
            checks.append(check('base-minimum', 'FF-06', missing_base <= 1e-5,
                                '5 mm continuous base witness along Y=0', missing_material_mm3=missing_base))
    checks.append(check('measured-geometry', 'FF-03', True, 'STEP geometry observations', parts=measured))
    return checks
