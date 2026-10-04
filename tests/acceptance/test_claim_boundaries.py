import json


def test_unmeasured_claims_are_explicit(built):
    report = json.loads((built / 'inspection.json').read_text())
    assert report['physical_tests'] == 'not_performed'
    assert 'strength' in report['claim_boundary']
    assert 'not been measured' in report['claim_boundary']
    assert any(c['id'] == 'physical-validation' and c['status'] == 'not_applicable'
               for c in report['checks'])
