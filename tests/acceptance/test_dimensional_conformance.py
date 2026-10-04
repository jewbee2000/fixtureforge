import cadquery as cq
import pytest
from OCP.BRepAdaptor import BRepAdaptor_Surface
from OCP.GeomAbs import GeomAbs_Cylinder, GeomAbs_Plane


def test_dimensions_from_surfaces(built, oracle):
    expected = oracle['reference_24']
    for name in ('base', 'clamp'):
        part = cq.importers.importStep(str(built / f'{name}.step')).val()
        bb = part.BoundingBox()
        actual = [bb.xmin, bb.xmax, bb.ymin, bb.ymax, bb.zmin, bb.zmax]
        assert actual == pytest.approx(expected[f'{name}_bounds'], abs=0.05)
        bore = []
        mounts = set()
        planes = []
        for face in part.Faces():
            surface = BRepAdaptor_Surface(face.wrapped)
            if surface.GetType() == GeomAbs_Cylinder:
                cylinder = surface.Cylinder()
                direction = cylinder.Axis().Direction()
                origin = cylinder.Location()
                if abs(direction.X()) > 0.999:
                    bore.append(2 * cylinder.Radius())
                    assert origin.Z() == pytest.approx(expected['bore_axis_z'], abs=0.05)
                    assert origin.Y() == pytest.approx(0, abs=0.05)
                elif abs(direction.Z()) > 0.999 and abs(origin.X()) > 1:
                    mounts.add((round(origin.X(), 4), round(origin.Y(), 4)))
                    assert cylinder.Radius() == pytest.approx(2.25, abs=0.05)
            if surface.GetType() == GeomAbs_Plane:
                plane = surface.Plane()
                if abs(plane.Axis().Direction().Z()) > 0.999:
                    planes.append(plane.Location().Z())
        assert bore and all(abs(d - expected['bore_diameter']) <= 0.05 for d in bore)
        if name == 'base':
            assert mounts == {(-20, -32), (-20, 32), (20, -32), (20, 32)}
            assert any(abs(z - 5) < 0.05 for z in planes)
            assert any(abs(z) < 0.05 for z in planes)
