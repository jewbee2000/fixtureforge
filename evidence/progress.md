# Progress

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
