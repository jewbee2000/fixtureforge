# Progress

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
