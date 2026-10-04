import json

import pytest

from fixtureforge.api import build
from fixtureforge.models import PartSpec
from fixtureforge.report import result, write_report


@pytest.mark.parametrize('filename', ['../escape.step', 'C:/private.step', '\\\\host\\share\\part.step', 'a:stream.step'])
def test_traversal_is_invalid(filename):
    with pytest.raises(ValueError):
        PartSpec(id='p', file=filename, sha256='0' * 64)


def test_output_traversal_is_rejected(tmp_path):
    with pytest.raises(ValueError, match='traversal'):
        build('examples/sensor_24mm.json', tmp_path / '..' / 'escape')


def test_html_escapes_input(tmp_path):
    report = result([dict(id='bad', requirement='FF-19', status='inconclusive',
                          message='<script>alert(1)</script>')])
    write_report(tmp_path, report)
    content = (tmp_path / 'report.html').read_text()
    assert '<script>alert' not in content and '&lt;script&gt;' in content


def test_duplicate_keys_fail(tmp_path):
    source = tmp_path / 'ambiguous.json'
    source.write_text('{"units":"inch","units":"mm"}')
    code, report = build(source, tmp_path / 'out')
    assert code == 2 and 'duplicate JSON key' in report['checks'][0]['message']
    manifest = json.loads((tmp_path / 'out/manifest.json').read_text())
    assert manifest['telemetry'] == 'none'
