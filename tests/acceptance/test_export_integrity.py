import cadquery as cq
import numpy as np
import trimesh


def test_mesh_identity_units_orientation(built):
    for name in ('base', 'clamp'):
        part = cq.importers.importStep(str(built / f'{name}.step')).val()
        mesh = trimesh.load_mesh(built / f'{name}.stl')
        assert mesh.is_watertight and mesh.is_winding_consistent
        assert mesh.volume > 0
        assert abs(mesh.volume - part.Volume()) / part.Volume() < 0.005
        bb = part.BoundingBox()
        assert np.allclose(mesh.bounds, [[bb.xmin, bb.ymin, bb.zmin],
                                         [bb.xmax, bb.ymax, bb.zmax]], atol=0.05)
