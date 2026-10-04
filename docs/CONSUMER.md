# Executed clean consumer walkthrough

This is an **agent-executed** walkthrough, not practitioner feedback. Evidence:
evidence/consumer.json, including exact absolute commands, exit codes, durations,
input/report hashes and installed wheel provenance. The source package was never
edited in the consumer directory.

The consumer lives at `outputs/consumers/fixtureforge-20261004`, outside this
repository, with a new `.venv`. It installed requirements-runtime-lock.txt and
the locally built wheel. Dependency installation used the registry/cache;
subsequent CAD commands needed no service. Recorded setup took 75.63 seconds;
the full automated sequence took 109.01 seconds on the recorded machine. These
are wall times with a warm package cache, not human effort or universal estimates.

The independently authored bracket STEP was copied in. The consumer wrote a
40-line, 730-byte AccessSpec with a non-default 3×2×2 mm connector travelling
from X=-12 to X=12 at Y=0, Z=5. It failed with exit 1. Changing the start and end
Y coordinates to 5 cleared the bracket and returned 0. No consumer Python code
was needed; the commands use the documented CLI. An 18 mm sensor fixture with
36×60 mm pitches then built twice; the complete inspection JSON was equal.
STEP bytes are not used as the reproducibility oracle because exporter headers
and identifiers need not be byte-stable.

Equivalent commands after installing the wheel in a fresh environment:

```
python -m pip install -r requirements-runtime-lock.txt
python -m pip install --no-deps fixtureforge-0.1.0-py3-none-any.whl
python -m pip check
python -m fixtureforge inspect blocked.json --output blocked
# Expected exit 1; retain its report. Change only Y in a copy of the JSON.
python -m fixtureforge inspect corrected.json --output corrected
python -m fixtureforge build sensor-18.json --output sensor-18
python -m fixtureforge build sensor-18.json --output sensor-18-repeat
```

Reproduce the entire walkthrough with `python scripts/package_release.py`,
`python scripts/external_example.py artifacts/external-source`, and
`python scripts/consumer_walkthrough.py <new-consumer-directory>`.
The last directory must not already exist. It is retained for inspection.

Compared with the baseline, this adds a pinned binary CAD dependency stack and
explicit JSON configuration. Direct CadQuery already does the key Boolean
operation in a few lines; CADCLAW consumes authored sweep solids. FixtureForge
removes the need for consumer code to construct sweeps, track part hashes,
propagate incomplete results, manage worker limits, and make a visual report.
It does not remove the need to understand the geometry or author the envelopes.

Three fresh-interpreter 24 mm builds took 6.74–6.85 seconds, with sampled peak
worker RSS below 414 MB; see evidence/performance.json. M0's 0.082 second baseline
measures only tiny synthetic geometry after imports. The workloads and timing
boundaries differ, so these numbers are not a speed comparison. The added report
and process work is worthwhile only if the explicit reusable contracts help the
engineer's workflow. No independent engineer has tested that hypothesis yet.
