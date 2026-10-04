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


def test_diagonal_is_labelled_conservative():
    # Away from the true diagonal, but inside its enclosing rectangular sweep.
    obstacle = cq.Workplane('XY').box(1, 1, 1).translate((0, 8, 0)).val()
    path = AccessPath(id='diagonal', envelope={'kind': 'box', 'size_mm': [2, 2, 2]},
                      start_mm=[0, 0, 0], end_mm=[10, 10, 0], occupied=['part'])
    result = evaluate_path(path, {'part': obstacle})
    assert result['status'] == 'fail'
    assert result['method'] == 'conservative_bounding_box'
    assert result['conservative_inflation'] is True
