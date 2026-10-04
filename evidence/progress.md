# Progress

## Final clean-source demonstration and wheel verification

At clean source commit `677a997b85ab0f098996f8b69326586c99c86d87`,
`python -m fixtureforge demo --offline --output artifacts/release-demo` returned
0. The preserved rejected/corrected reports have fail/pass statuses respectively,
and the replay index and root manifest both exist. The latest wheel was installed
from disk with `--no-index --no-deps --force-reinstall` in the separate consumer
environment. Its replay passed, and two new 18 mm builds gave identical inspection
JSON with the corrected bed-orientation label. All four refresh commands exited
0. See release-demo.json and release-wheel.json for hashes, actual commands and
clean source provenance. Earlier snapshots remain retained as historical runs.

The project now has no remaining applicable Must work. The explicit limitations
above remain: no physical or practitioner validation, no browser layout review,
no OS-level egress isolation, and no generated-code or live-model execution.
The final evidence-only commit does not change the verified product source.

## Final artifact review

Review found the replay index linked a missing root manifest and did not link
its two child reports. Added the root manifest, links to both preserved outcomes,
and a shared remaining-time budget across replay steps. The offline acceptance
test now asserts those artifacts. This is a reporting fix; geometry and oracle
values are unchanged. Targeted rerun: 8 passed; lint and types passed. A fresh
clean-commit demo follows. The requirement map overlays those latest executed
cases on the 61-case full run, without treating repeated cases as new coverage.

Review also corrected the upper clamp's bed-orientation label: its split face
is already its minimum-Z face, so printing orientation translates that plane to
Z=0 without a 180-degree rotation. Geometry and clearance verdicts are unchanged;
the claim-boundary test now checks the corrected label. The earlier wording is
visible in preserved run artifacts and must not guide physical printing.

## M4 completed — 2026-10-04

Final full acceptance command `python -m pytest -q --tb=short
--junitxml=evidence/acceptance.xml`: **61 passed in 85.50 seconds**, exit 0.
`python -m ruff check src scripts tests`: passed. `python -m mypy
src/fixtureforge`: passed, 12 source files. `python -m pip check`: passed.
Output files are retained. Requirement IDs, actual test names, input/oracle/lock
hashes, artifact hashes and source provenance are in requirements-evidence.json.

`python scripts/package_release.py` produced the local wheel with embedded
source provenance. `python scripts/consumer_walkthrough.py
C:/Users/Walt/Documents/Codex/2026-10-03/g/outputs/consumers/fixtureforge-20261004`
installed it in a separate fresh environment. Installation: 75.63 seconds;
complete sequence: 109.01 seconds with warm package cache. A 40-line/730-byte
non-default AccessSpec failed as expected (1), then passed (0) after changing Y.
No consumer source code or package edits. Two 18 mm builds gave identical
inspection JSON. This is agent-executed workflow evidence, not human adoption.

`python scripts/benchmark.py`: three fresh-interpreter 24 mm builds took
6.8473, 6.7414 and 6.7511 seconds, each exit 0. Sampled peak worker RSS:
412286976, 413732864 and 413433856 bytes, below the frozen 2 GiB limit and
60 second target. Full commands and artifact hashes are retained. Baseline's
small geometry timing excludes imports and is not a comparable speed benchmark.

Static CAD and replay PNGs were inspected. A caption overlap found on the first
replay rendering was corrected. Local HTML browser navigation was blocked by
browser URL policy; browser layout verification remains unrun. Reports' numerical
contents, escaping, local resources and structural data were checked.

The canonical 767-word website draft and repository copy now describe observed
work, with the actual replay image and no fabricated biography or measurements.
`bundle check` and both normal / `--drafts --unpublished` Jekyll builds passed in
the website-drafts checkout. The normal HTML output contains no FixtureForge
article; the explicit preview does. `published: false` remains set. Desktop/mobile
browser preview and hosted repository/evidence links remain publication work.

Disposition: FF-16 implemented (margin and explicit occupancy); FF-17 revision
diff deferred; FF-18 live/model proposals deferred; FF-10 not applicable because
generated-code execution is disabled. No remote, deployment, model spend or
hardware purchase. Future work is independent practitioner feedback, physical
fit/load testing if desired, and publication only after separate authorization.

## M1–M3 core complete — 2026-10-04

Initial full suite: `python -m pytest -q --tb=short --junitxml=evidence/acceptance.xml`
gave **55 passed in 87.51 seconds**. This includes six reference sizes, the eight
intended defect causes, independent STEP surface queries and STL checks,
external build123d input/repair, margin and occupancy checks, Boolean failure,
input/worker bounds, and the offline demo with Python socket egress denied.
This is an application-level egress guard, not OS firewall isolation; no native
networking code is used by the application. The guard's attempted connection was
also rejected. No model credentials are needed.

`python -m fixtureforge demo --offline --output artifacts/replay`: exit 0, with
actual rejected candidate (exit 1) and corrected fixture (exit 0). Both reports
and all inputs are retained. `scripts/preserve_failures.py` retains seeded STEP
mutations and summaries. Review tightened two mutations to avoid incidental
defects: connector rib now remains attached; tool obstruction is outside the
screw-head radius. Original results retained in seeded-failures-v1.json and
artifacts/seeded-failures; revised defects in artifacts/seeded-failures-v2.

Ruff and mypy exposed formatting/type issues, repaired without changing expected
geometry. First type diagnostics retained in types-first.txt. `pip check` passed.
Browser local-file preview was blocked by browser URL policy; no browser-layout
claim is made. A static PNG is generated from actual STEP tessellation for safe
visual inspection, without HTML execution. Next: cold consumer installation,
semantic reproduction, performance measurements, final evidence and article.

## M0 complete — 2026-10-04

`python scripts/baseline.py` executed CADCLAW 0.10.0, CadQuery 2.8.0 and
build123d 0.12.0 on two synthetic access cases. Both endpoint overlaps were zero;
both full sweeps overlapped 4 mm³. CADCLAW detected the prebuilt swept solids.
Headless STEP cube roundtrip measured 1000 mm³. See baseline.json for actual
versions, source hashes and artifact hashes. `pip check` passed.

`python -m pytest tests/acceptance/test_input_validation.py
tests/acceptance/test_baseline_artifacts.py -q`: 13 passed. The prior import
failure is preserved in oracle-before-implementation.txt. Gate decision is a
narrow CadQuery access integration with reusable STEP sweep exports for CADCLAW.
No generic validator or model feature is being added. Full-path checks reject
Boolean failures, unlike silently treating incomplete work as clear.

M1 first slice: `python -m fixtureforge build examples/sensor_24mm.json --output
artifacts/first-24` returned 0/pass. `test_swept_access.py`: 3 passed. Fresh-process
STEP import, deterministic geometry checks, exported SVG/HTML, and worker limits
are implemented. External inputs, wider mutation coverage and visual inspection
remain next.

## 2026-10-04 implementation start

Read all requested contracts plus AGENT_WORKFLOW and BLOG_BRIEF. Verified Python
3.12, Git, and hardware. Docker CLI 28.0.4 cannot reach its daemon; generated-code
execution remains disabled. `py -3.12 -m venv .venv` created the project environment.
Dependency resolution is in progress; no CAD result is claimed yet. Git uses a
per-command safe.directory override for this explicitly supplied workspace.

Frozen initial independent hand calculations and acceptance assertions before
production code. `tests/oracle/reference.json` records all eight intended failure
causes. Decisions and limits are in docs/DECISIONS.md. Next: execute baseline,
freeze tested dependencies, then implement the smallest imported-STEP slice.

2026-10-03 — Preparation only. Requirements, acceptance designs, milestones, agent guidance, and unpublished article draft created. Application code, executable acceptance tests, model campaigns, and physical validation have not been implemented or run. Next task: M0 in IMPLEMENTATION_PLAN.md.

## 2026-10-04 requirements audit

Added explicit Must/Should/Could/Won't priorities, per-requirement rationale and acceptance, existing-tool evidence, M0 differentiation gate, and external consumer release criteria. No application implementation or tests were run. All application requirements remain not implemented.

Planning verification: work/verify_project_packages.py checked unique IDs, priorities, nonempty rationale and acceptance, valid dependency references, milestone/spec mapping, local document links, unchanged unpublished website draft status, and absent project remotes. git diff --check passed. Space plan readback verified all 22 requirement IDs and five exclusions under the correct parent. These checks validate documentation consistency, not application behavior.
