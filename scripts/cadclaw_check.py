"""Optional interoperability example; FixtureForge retains authoritative verdicts.

python scripts/cadclaw_check.py PART.step SWEEP.step
"""
import json
import sys

import cadquery as cq
from cadclaw.interference import InterferenceCheck

parts = [cq.importers.importStep(p).val() for p in sys.argv[1:]]
labels = {id(s): p for s, p in zip(parts, sys.argv[1:], strict=True)}
result = InterferenceCheck(parts, lambda p: labels[id(p)], min_volume=1e-7).run()
print(json.dumps({'passed': result.passed, 'clips': [vars(c) for c in result.clips],
                  'note': 'CADCLAW static cross-check of authored sweep; not the strict access contract'}, indent=2))
raise SystemExit(0 if result.passed else 1)
