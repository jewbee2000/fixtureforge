"""Conservative swept BREP access checks; no sampling-based clearance verdicts."""
import math

import cadquery as cq
from OCP.BRepAlgoAPI import BRepAlgoAPI_Common

from .models import AccessPath, Envelope

VOLUME_EPS = 1e-7
DISTANCE_EPS = 1e-6


def overlap(a, b):
    op = BRepAlgoAPI_Common(a.wrapped, b.wrapped)
    op.Build()
    if not op.IsDone():
        raise RuntimeError('Boolean common failed; clearance is inconclusive')
    common = cq.Shape.cast(op.Shape())
    if not common.isValid():
        raise RuntimeError('Boolean common returned invalid geometry')
    value = sum(s.Volume() for s in common.Solids())
    if not math.isfinite(value) or value < -VOLUME_EPS:
        raise RuntimeError('Boolean returned invalid volume')
    return value


def envelope_shape(env: Envelope, center, margin=0):
    if env.kind == 'box':
        assert env.size_mm is not None
        return cq.Workplane('XY').box(*(v + 2 * margin for v in env.size_mm)).findSolid().translate(center)
    assert env.radius_mm is not None and env.height_mm is not None
    axis = 'xyz'.index(env.axis)
    direction = [0, 0, 0]
    direction[axis] = 1
    start = list(center)
    start[axis] -= env.height_mm / 2 + margin
    return cq.Solid.makeCylinder(env.radius_mm + margin, env.height_mm + 2 * margin,
                                 cq.Vector(*start), cq.Vector(*direction))


def swept_shape(path: AccessPath, margin=0):
    delta = [b - a for a, b in zip(path.start_mm, path.end_mm, strict=True)]
    env = path.envelope
    if env.kind == 'cylinder':
        axis = 'xyz'.index(env.axis)
        if all(abs(d) < 1e-12 for i, d in enumerate(delta) if i != axis):
            assert env.height_mm is not None
            longer = env.model_copy(update={'height_mm': env.height_mm + abs(delta[axis])})
            center = [(a + b) / 2 for a, b in zip(path.start_mm, path.end_mm, strict=True)]
            return envelope_shape(longer, center, margin), 'exact_axial_cylinder'
    first = envelope_shape(env, path.start_mm, margin).BoundingBox()
    last = envelope_shape(env, path.end_mm, margin).BoundingBox()
    lo = [min(getattr(first, f'{a}min'), getattr(last, f'{a}min')) for a in 'xyz']
    hi = [max(getattr(first, f'{a}max'), getattr(last, f'{a}max')) for a in 'xyz']
    shape = cq.Workplane('XY').box(*(upper - lower for lower, upper in zip(lo, hi, strict=True))).findSolid()
    shape = shape.translate(cq.Vector(*[(lower + upper) / 2 for lower, upper in zip(lo, hi, strict=True)]))
    exact = env.kind == 'box' and sum(abs(d) > 1e-12 for d in delta) <= 1
    return shape, 'exact_axial_box' if exact else 'conservative_bounding_box'


def bounds(shape):
    box = shape.BoundingBox()
    return [[getattr(box, f'{a}min') for a in 'xyz'],
            [getattr(box, f'{a}max') for a in 'xyz']]


def evaluate_path(path: AccessPath, parts):
    nominal, method = swept_shape(path)
    swept, _ = swept_shape(path, path.margin_mm)
    pairs = []
    for part_id in path.occupied:
        part = parts[part_id]
        volume = overlap(swept, part)
        distance = nominal.distance(part)
        if not math.isfinite(distance):
            raise RuntimeError('distance query failed')
        inflated_distance = swept.distance(part)
        end_touch = part_id in path.intended_end_contacts
        # End contact is a zero-volume interface. Never ignore penetration.
        contact_ok = False
        if end_touch and volume <= VOLUME_EPS and path.margin_mm == 0:
            end = envelope_shape(path.envelope, path.end_mm)
            contact_ok = end.distance(part) <= DISTANCE_EPS
            delta = [b - a for a, b in zip(path.start_mm, path.end_mm, strict=True)]
            length = math.sqrt(sum(d * d for d in delta))
            if length > 0 and contact_ok:
                # Full shortened sweep, not sampled poses: only endpoint may touch.
                fraction = min(0.5, 0.001 / length)
                shortened = path.model_copy(update={
                    'end_mm': tuple(b - d * fraction for b, d in zip(path.end_mm, delta, strict=True))})
                prior, _ = swept_shape(shortened)
                contact_ok = prior.distance(part) > DISTANCE_EPS
        collision = volume > VOLUME_EPS or (inflated_distance <= DISTANCE_EPS and not contact_ok)
        pairs.append({'part': part_id, 'status': 'fail' if collision else 'pass',
                      'overlap_mm3': volume, 'nominal_clearance_mm': distance,
                      'intended_end_contact': contact_ok, 'part_bounds_mm': bounds(part)})
    return {'id': path.id, 'requirement': path.requirement,
            'status': 'fail' if any(p['status'] == 'fail' for p in pairs) else 'pass',
            'message': 'Conservative envelope obstruction' if any(p['status'] == 'fail' for p in pairs)
            else 'Entire conservative envelope clear (declared end contacts allowed)',
            'nominal_clearance_mm': min(p['nominal_clearance_mm'] for p in pairs),
            'clearance_interpretation': 'lower bound for conservative sweeps',
            'method': method, 'margin_mm': path.margin_mm,
            'conservative_inflation': method == 'conservative_bounding_box',
            'start_mm': path.start_mm, 'end_mm': path.end_mm,
            'occupied': path.occupied, 'sweep_bounds_mm': bounds(swept), 'pairs': pairs}
