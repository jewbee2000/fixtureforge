import cadquery as cq
import pytest

from fixtureforge import access
from fixtureforge.models import AccessPath


def test_kernel_failure_cannot_be_clear(monkeypatch):
    class FailedBoolean:
        def __init__(self, *args):
            pass

        def Build(self):
            pass

        def IsDone(self):
            return False

    monkeypatch.setattr(access, 'BRepAlgoAPI_Common', FailedBoolean)
    path = AccessPath(id='p', envelope={'kind': 'box', 'size_mm': [1, 1, 1]},
                      start_mm=[0, 0, 0], end_mm=[0, 0, 3], occupied=['part'])
    with pytest.raises(RuntimeError, match='inconclusive'):
        access.evaluate_path(path, {'part': cq.Workplane('XY').box(1, 1, 1).val()})
