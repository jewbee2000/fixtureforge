"""Labelled deliberate-mutation replay; no model, code execution or credentials."""
from .api import build, inspect, prepare_output
from .files import read_json, write_json
from .models import FixtureSpec
from .report import result, write_report


def demo(output, *, timeout=120, memory_mb=2048):
    out = prepare_output(output)
    write_json(out / 'candidate.json', FixtureSpec().model_dump(mode='json'))
    code, corrected = build(out / 'candidate.json', out / 'corrected', timeout=timeout, memory_mb=memory_mb)
    if code:
        write_report(out, corrected)
        return code, corrected
    bad = read_json(out / 'corrected/access.json')
    # Retained failed access proposal: driver through the middle of the clamp.
    bad['paths'] = [p for p in bad['paths'] if p['id'] == 'tool-1']
    bad['paths'][0]['start_mm'][1] = 0
    bad['paths'][0]['end_mm'][1] = 0
    for part in bad['parts']:
        part['file'] = 'corrected/' + part['file']
    bad['assumptions'].append('REPLAY: deliberately incorrect driver line, not a model response.')
    write_json(out / 'rejected-candidate.json', bad)
    rejected_code, rejected = inspect(out / 'rejected-candidate.json', out / 'rejected', timeout=timeout, memory_mb=memory_mb)
    expected = rejected_code == 1 and any(c['id'] == 'tool-1' and c['status'] == 'fail' for c in rejected['checks'])
    report = result([dict(id='replay-rejection', requirement='FF-09', status='pass' if expected else 'fail',
                          message='REPLAY: deliberate tool-axis mutation rejected; corrected fixture passes',
                          rejected_exit_code=rejected_code, corrected_exit_code=code)],
                    mode='REPLAY', live_model_evaluation='not_run')
    write_report(out, report)
    return (0 if expected else 1), report
