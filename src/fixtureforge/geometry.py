"""One restricted synthetic clamp family. Inspection lives in a separate module."""
import cadquery as cq

from .files import digest, write_json
from .models import AccessSpec, FixtureSpec


def box(x, y, z, center):
    return cq.Workplane('XY').box(x, y, z).findSolid().translate(center)


def cylinder(radius, length, start, axis=(0, 0, 1)):
    return cq.Solid.makeCylinder(radius, length, cq.Vector(*start), cq.Vector(*axis))


def construct(spec: FixtureSpec):
    r = (spec.sensor_diameter_mm + spec.clearance_mm) / 2
    outer = r + spec.wall_mm
    z = spec.base_mm + outer
    ear = outer + 7
    lower = box(spec.mount_pitch_x_mm + 12, spec.mount_pitch_y_mm + 12,
                spec.base_mm, (0, 0, spec.base_mm / 2))
    height = z - 0.5 - spec.base_mm
    lower = lower.fuse(box(20, 2 * outer, height, (0, 0, spec.base_mm + height / 2)))
    upper = box(20, 2 * outer, outer - 0.5, (0, 0, z + (outer + 0.5) / 2))
    for sign in (-1, 1):
        # Ear overlap reaches 1 mm into the ring to make a single solid.
        lower = lower.fuse(box(20, 14, height, (0, sign * (ear - 1), spec.base_mm + height / 2)))
        upper = upper.fuse(box(20, 14, 5, (0, sign * (ear - 1), z + 3)))
    bore = cylinder(r, 22, (-11, 0, z), (1, 0, 0))
    lower, upper = lower.cut(bore), upper.cut(bore)
    for sign in (-1, 1):
        hole = cylinder(2.25, 100, (0, sign * ear, -1))
        lower, upper = lower.cut(hole), upper.cut(hole)
    for x in (-spec.mount_pitch_x_mm / 2, spec.mount_pitch_x_mm / 2):
        for y in (-spec.mount_pitch_y_mm / 2, spec.mount_pitch_y_mm / 2):
            lower = lower.cut(cylinder(2.25, spec.base_mm + 2, (x, y, -1)))
    return {'base': lower.clean(), 'clamp': upper.clean()}


def export_fixture(parts, spec, out):
    assembly = cq.Assembly(name='fixtureforge')
    for name, shape in parts.items():
        cq.exporters.export(shape, str(out / f'{name}.step'))
        cq.exporters.export(shape, str(out / f'{name}.stl'), tolerance=0.01, angularTolerance=0.05)
        assembly.add(shape, name=name)
    assembly.export(str(out / 'assembly.step'))
    write_json(out / 'fixture.json', spec.model_dump(mode='json'))
    access = fixture_access(spec, out)
    write_json(out / 'access.json', access.model_dump(mode='json'))


def fixture_access(spec, out):
    r = (spec.sensor_diameter_mm + spec.clearance_mm) / 2
    z = spec.base_mm + r + spec.wall_mm
    ear = r + spec.wall_mm + 7
    paths = []

    def path(name, envelope, start, end, requirement, occupied=None, contacts=None):
        paths.append(dict(id=name, envelope=envelope, start_mm=start, end_mm=end,
                          requirement=requirement, occupied=occupied or ['base', 'clamp'],
                          intended_end_contacts=contacts or []))

    path('sensor', dict(kind='cylinder', radius_mm=spec.sensor_diameter_mm / 2,
                        height_mm=spec.sensor_length_mm, axis='x'),
         [0, 0, z], [0, 0, z], 'FF-04')
    length = spec.connector_length_mm + spec.cable_exit_mm
    sign = 1 if spec.connector_end == '+x' else -1
    x = sign * (spec.sensor_length_mm / 2 + length / 2)
    path('connector', dict(kind='box', size_mm=[length, spec.connector_width_mm, spec.connector_height_mm]),
         [x + sign * 25, 0, z], [x, 0, z], 'FF-04')
    for index, y in enumerate((-ear, ear)):
        # Nuts approach from below BEFORE the fixture is mounted on standoffs.
        path(f'nut-{index}', dict(kind='box', size_mm=[8, 8, 3]),
             [0, y, -15], [0, y, -1.5], 'FF-05', ['base'], ['base'])
        path(f'shaft-{index}', dict(kind='cylinder', radius_mm=2, height_mm=z + 8, axis='z'),
             [0, y, (z + 5.5) / 2], [0, y, (z + 5.5) / 2], 'FF-05')
        path(f'head-{index}', dict(kind='cylinder', radius_mm=4.5, height_mm=4, axis='z'),
             [0, y, z + 32.5], [0, y, z + 7.5], 'FF-05', contacts=['clamp'])
        path(f'tool-{index}', dict(kind='cylinder', radius_mm=6, height_mm=25, axis='z'),
             [0, y, z + 43], [0, y, z + 18], 'FF-05', contacts=['clamp'])
    return AccessSpec.model_validate(dict(schema_version='1.0', units='mm',
                      parts=[dict(id=n, file=f'{n}.step', sha256=digest(out / f'{n}.step'))
                             for n in ('base', 'clamp')], paths=paths,
                      datums={'A': (0, 0, 0), 'B': (0, 0, z), 'C': (0, 0, z)},
                      assumptions=['Synthetic sensor and connector envelopes.',
                                   'Nut insertion precedes mounting. Mount on standoffs with >=3 mm underside clearance.',
                                   'Occupancy is explicitly specified for each step; no sequence inference.']))
