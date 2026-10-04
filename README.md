# FixtureForge

Check whether a declared straight tool or connector path clears imported STEP
parts. This is a small CadQuery integration with explicit JSON contracts,
conservative full-path envelopes, and local reports. A two-part sensor clamp is
the parametric example. See [the baseline decision](docs/BASELINE.md): CadQuery,
build123d and CADCLAW already solve the underlying geometry operations.

Repository: [jewbee2000/fixtureforge](https://github.com/jewbee2000/fixtureforge).
See [next steps](docs/NEXT_STEPS.md) for the proposed next iteration.

![Rejected and corrected tool access](evidence/replay.png)

Actual STEP edges and swept bounds from a deliberately seeded replay. No physical
measurements or live model evaluation are represented.

## Reproduce locally

Tested on Windows x64, Python 3.12.2. Install inside this repository:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-lock.txt
.\.venv\Scripts\python.exe -m pip install --no-build-isolation --no-deps -e .
.\.venv\Scripts\python.exe -m fixtureforge demo --offline --output artifacts/my-demo
```

Open `artifacts/my-demo/corrected/report.html` and
`artifacts/my-demo/rejected/report.html`. The demo returns 0 only when the intended
negative case fails and the corrected fixture passes. Use a new empty output
directory for every run. Dependencies need downloading during setup; installed
builds and inspections use no network, credentials or model API.

```powershell
.\.venv\Scripts\python.exe -m fixtureforge build examples/sensor_24mm.json --output artifacts/my-clamp
.\.venv\Scripts\python.exe scripts/external_example.py artifacts/my-bracket
.\.venv\Scripts\python.exe -m fixtureforge inspect artifacts/my-bracket/blocked.json --output artifacts/my-failure
# Expected exit 1, with a named obstruction in the report.
.\.venv\Scripts\python.exe -m fixtureforge inspect artifacts/my-bracket/clear.json --output artifacts/my-success
```

Python API: `fixtureforge.api.build(spec_path, output)` and
`fixtureforge.api.inspect(access_path, output)` return `(exit_code, report)`.
Normal commands use 0/pass, 1/geometric violation and 2/incomplete or invalid.
[Public contract](docs/PUBLIC_API.md) · [Schemas](schemas) ·
[Executed consumer walkthrough](docs/CONSUMER.md).

## Evidence and scope

Run `python -m pytest -q`, `python -m ruff check src scripts tests` and
`python -m mypy src/fixtureforge` in the environment. The repository retains
executed consumer and performance evidence used by the acceptance tests.
To regenerate those runs, follow docs/CONSUMER.md and run
`python scripts/benchmark.py --output artifacts/my-benchmark` with a new output
directory. It writes `performance.json` alongside the three builds and preserves
the historical evidence. Full requirement mapping: [evidence](evidence/requirements-evidence.json).

The software checks six reference clamp sizes, independent STEP cylinder/plane
dimensions, STL integrity, eight seeded defect causes and an external bracket.
It retains failed inputs and reports; see [progress](evidence/progress.md) and
[decisions](docs/DECISIONS.md). Offline replay is tested with Python socket egress
denied. This is not OS isolation or a generated-code sandbox.

Limits: 20 declared parts, 40 paths, 10 MiB STEP per file, 256 KiB JSON, 2000
imported faces, 120 seconds and 2 GiB sampled worker RSS. Only axis-aligned
box/cylinder envelopes and straight translations are supported. Diagonal sweeps
can over-report obstructions. Each STEP file must contain one unambiguous solid
and declare millimeters. Input transforms are translations; no rotating paths.

The clamp needs nuts inserted before mounting and at least 3 mm underside space
on standoffs. It has not been printed, loaded, or shown to grip a real sensor.
No FEA, slicer, machining, arbitrary motion planning, flexible cable routing,
model API or generic CAD validation platform is included. Revision report diff
and live model proposals are deferred. A later publication audit verified the
retained replay reports in a browser at desktop and 390 px mobile widths;
[screenshots and scope](evidence/publication-audit/README.md) are retained.

The independent consumer was run by the same coding agent in a fresh environment;
external practitioner adoption remains unverified. [Licensing and data handling](docs/LICENSING.md).
The [article draft](docs/BLOG_DRAFT.md) remains unpublished on the blog. The
GitHub project is public; website publication remains pending separate authorization.
