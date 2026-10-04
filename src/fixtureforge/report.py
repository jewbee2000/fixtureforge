import html
import json
from pathlib import Path

from .files import write_json

BOUNDARY = ('Computed nominal CAD geometry only. Physical fit, clamping force, strength, '
            'print quality, thermal stability and fatigue have not been measured. '
            'A conservative obstruction does not prove that every real articulated tool is blocked.')


def summarize(checks):
    if not checks or any(c['status'] == 'inconclusive' for c in checks):
        return 'inconclusive'
    if any(c['status'] == 'fail' for c in checks):
        return 'fail'
    return 'pass'


def result(checks, **data):
    return dict(schema_version='1.0', status=summarize(checks), checks=checks,
                claim_boundary=BOUNDARY, physical_tests='not_performed', **data)


def diagram(check):
    sweep = check.get('sweep_bounds_mm')
    if not sweep:
        return ''
    pairs = check['pairs']
    all_bounds = [sweep] + [p['part_bounds_mm'] for p in pairs]
    chunks = []
    for axis, title in ((0, 'XZ'), (1, 'YZ')):
        low = [min(b[0][a] for b in all_bounds) for a in (axis, 2)]
        high = [max(b[1][a] for b in all_bounds) for a in (axis, 2)]
        scale = min(330 / max(high[0] - low[0], 1), 230 / max(high[1] - low[1], 1))

        def rect(b, color, label, axis=axis, low=low, high=high, scale=scale):
            x = 30 + (b[0][axis] - low[0]) * scale
            y = 30 + (high[1] - b[1][2]) * scale
            w = (b[1][axis] - b[0][axis]) * scale
            h = (b[1][2] - b[0][2]) * scale
            return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{color}" fill-opacity=".25" stroke="{color}"><title>{html.escape(label)}</title></rect>'

        content = ''.join(rect(p['part_bounds_mm'], '#d65b39' if p['status'] == 'fail' else '#386981', p['part']) for p in pairs)
        content += rect(sweep, '#7738a8', 'entire swept envelope bounds')
        chunks.append(f'<svg viewBox="0 0 400 290" aria-label="{title} bounds"><text x="10" y="20">{title} projection · bounds in mm</text>{content}</svg>')
    return '<div class="projections">' + ''.join(chunks) + '</div><small>Bounding-box illustration only. Verdict uses complete BREP intersections; purple is the sweep, orange marks an obstructing part.</small>'


def write_report(out: Path, report):
    write_json(out / 'inspection.json', report)
    cards = []
    for c in report['checks']:
        details = html.escape(json.dumps({k: v for k, v in c.items() if k not in ('pairs',)}, indent=2))
        pairs = ''.join(f"<li>{html.escape(p['part'])}: {p['status']}; overlap {p['overlap_mm3']:.6g} mm³; nominal gap {p['nominal_clearance_mm']:.6g} mm</li>" for p in c.get('pairs', []))
        cards.append(f'<section class="{c["status"]}"><h2>{html.escape(c["id"])} <span>{c["status"].upper()}</span></h2><p>{html.escape(c["requirement"])} · {html.escape(c["message"])}</p><ul>{pairs}</ul>{diagram(c)}<details><summary>Computed values and frozen path</summary><pre>{details}</pre></details></section>')
    svg = '<img src="dimensions.svg" alt="Actual CAD geometry in isometric projection">' if (out / 'dimensions.svg').exists() else ''
    document = '''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>FixtureForge inspection</title><style>
body{font:16px/1.55 system-ui;margin:0;background:#eef1f0;color:#203440}main{max-width:1050px;margin:auto;padding:32px}h1{font-size:40px}h2{font-size:21px}section{background:white;border-left:5px solid #357660;padding:20px;margin:18px 0;border-radius:8px}.fail{border-color:#c94c2c}.inconclusive{border-color:#ac7700}span{float:right;font-size:14px}.boundary{background:#fff4d9;padding:20px}pre{white-space:pre-wrap;overflow-wrap:anywhere;font-size:12px}.projections{display:flex}svg{width:50%;background:#fafafa}img{max-width:100%;background:white}small{display:block}a{color:#245e78}@media(max-width:650px){main{padding:15px}.projections{display:block}svg{width:100%}h1{font-size:30px}}
</style><main><p>FIXTUREFORGE · LOCAL CAD INSPECTION · SCHEMA 1.0</p>'''
    document += f'<h1>Access inspection: {report["status"].upper()}</h1><p class="boundary">{html.escape(BOUNDARY)}</p>{svg}'
    document += '<p><a href="inspection.json">Machine-readable result</a> · <a href="manifest.json">Provenance</a></p>'
    if report.get('mode') == 'REPLAY':
        document += '<p><a href="rejected/report.html">Inspect rejected candidate</a> · <a href="corrected/report.html">Inspect corrected fixture</a></p>'
    document += ''.join(cards) + '</main></html>'
    (out / 'report.html').write_text(document, encoding='utf-8')
