import cadquery as cq


def test_reimported_solids(built, oracle):
    assembly = cq.importers.importStep(str(built / 'assembly.step')).val()
    assert len(assembly.Solids()) == oracle['reference_24']['part_count']
    for name in ('base', 'clamp'):
        part = cq.importers.importStep(str(built / f'{name}.step')).val()
        assert len(part.Solids()) == 1
        assert part.isValid() and part.Volume() > 0
