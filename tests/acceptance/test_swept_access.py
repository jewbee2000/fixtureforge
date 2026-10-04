"""Expected geometry is hand-authored; never imported from builder helpers."""
import cadquery as cq
import pytest

from fixtureforge.access import evaluate_path
from fixtureforge.models import AccessPath


@pytest.mark.parametrize('shape', [
    {'kind': 'box', 'size_mm': [2, 2, 2]},
    {'kind': 'cylinder', 'radius_mm': 1, 'height_mm': 2, 'axis': 'z'},
])
def test_obstruction_between_endpoints(shape):
    obstacle = cq.Workplane('XY').box(1, 1, 4).translate((0, 0, 5)).val()
    path = AccessPath(id='middle', envelope=shape, start_mm=[0, 0, 0],
                      end_mm=[0, 0, 10], occupied=['obstacle'])
    result = evaluate_path(path, {'obstacle': obstacle})
    assert result['status'] == 'fail'
    assert abs(result['pairs'][0]['overlap_mm3'] - 4) < 1e-6


def test_exact_clearance():
    obstacle = cq.Workplane('XY').box(2, 2, 2).translate((5, 0, 5)).val()
    path = AccessPath(id='clear', envelope={'kind': 'box', 'size_mm': [2, 2, 2]},
                      start_mm=[0, 0, 0], end_mm=[0, 0, 10], occupied=['obstacle'])
    result = evaluate_path(path, {'obstacle': obstacle})
    assert result['status'] == 'pass'
    assert result['nominal_clearance_mm'] == pytest.approx(3)
