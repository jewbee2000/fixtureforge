import cadquery as cq
import pytest

from fixtureforge.access import evaluate_path
from fixtureforge.models import AccessPath


def test_clearance_margin_and_explicit_occupancy():
    part = cq.Workplane('XY').box(2, 2, 2).translate((5, 0, 5)).val()
    other = cq.Workplane('XY').box(2, 2, 2).translate((50, 0, 5)).val()
    path = AccessPath(id='test', envelope={'kind': 'box', 'size_mm': [2, 2, 2]},
                      start_mm=(0, 0, 0), end_mm=(0, 0, 10), occupied=['part'])
    assert evaluate_path(path.model_copy(update={'margin_mm': 2.99}), {'part': part})['status'] == 'pass'
    assert evaluate_path(path.model_copy(update={'margin_mm': 3.01}), {'part': part})['status'] == 'fail'
    removed = path.model_copy(update={'margin_mm': 3.01, 'occupied': ['remaining']})
    assert evaluate_path(removed, {'part': part, 'remaining': other})['status'] == 'pass'


def test_contact_never_hides_overlap():
    part = cq.Workplane('XY').box(2, 2, 2).translate((0, 0, 5)).val()
    path = AccessPath(id='contact', envelope={'kind': 'box', 'size_mm': [2, 2, 2]},
                      start_mm=(0, 0, 0), end_mm=(0, 0, 5), occupied=['part'],
                      intended_end_contacts=['part'])
    assert evaluate_path(path, {'part': part})['status'] == 'fail'


@pytest.mark.parametrize('change', [{'motion': 'curve'}, {'end_orientation_deg': [0, 90, 0]},
                                    {'occupied': ['a', 'a']}, {'intended_end_contacts': ['b']}])
def test_unsupported_semantics(change):
    payload = dict(id='invalid', envelope={'kind': 'box', 'size_mm': [2, 2, 2]},
                   start_mm=[0, 0, 0], end_mm=[0, 0, 5], occupied=['a'])
    payload.update(change)
    with pytest.raises(ValueError):
        AccessPath(**payload)
