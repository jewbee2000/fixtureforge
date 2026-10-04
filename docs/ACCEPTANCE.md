# Acceptance and evidence plan

This is a test design, not a report of passing tests. The concrete contracts and thresholds are in [SPEC.md](SPEC.md). Machine-readable traceability is in [requirements.json](../requirements.json). Every listed test path is planned and must be created during implementation.

| ID | Required behavior | Independent acceptance evidence |
| --- | --- | --- |
| FF-01 | FixtureSpec validates units, bounds, and coupled feasibility constraints before geometry construction. | Reject negative, nonfinite, out-of-range, and impossible pitch/diameter combinations with a specific explanation. |
| FF-02 | Every accepted configuration produces exactly two valid, positive-volume single solids. | Inspect each BREP and STEP reimport in a fresh process; reject null, merged, or self-invalid geometry. |
| FF-03 | Bore, hole pitches, base thickness, and datums agree with requirements within 0.05 mm. | Independent section/edge/plane queries of reimported STEP measure dimensions. |
| FF-04 | Sensor and connector keepouts remain clear except for explicitly intended contact surfaces. | Boolean intersections and known collision mutations verify the rule and its exclusions. |
| FF-05 | Fastener and tool-access envelopes remain usable in the prescribed assembly sequence. | Sampled assembly and tool sweeps identify intentional impossible-access configurations. |
| FF-06 | Wall, base, and build-volume requirements are checked on generated geometry. | Deliberately thin or oversized parts fail even if their input metadata claims compliance. |
| FF-07 | All six reference designs pass and all eight invalid cases are rejected for their intended cause. | Frozen inventory and explicit case-to-requirement mapping, not just counting nonzero exits. |
| FF-08 | STEP and STL export preserve units and per-part identity; round trips remain within tolerance. | Reimport STEP, compare volume/bounds, and check STL watertightness and triangle orientation. |
| FF-09 | Offline demonstration shows a rejected candidate and a corrected fixture without a model service. | Run without credentials and network; inspect actual generated CAD and reports. |
| FF-10 | Any generated-code experiment uses bounded isolation and a read-only evaluator. | Timeout, path-escape, and evaluator-write probes fail; JSON-only generation cannot execute code. |
| FF-11 | Inspection output separates computed geometry from unmeasured physical fit and strength. | Report labels geometric checks, assumptions, and absent physical tests explicitly. |
| FF-12 | Fresh installation and deterministic inputs reproduce the required artifacts within numerical tolerance. | Record stable versions; compare geometry semantically rather than assuming STEP file bytes are invariant. |

## Test layers

Use schema tests for input constraints; deterministic unit and contract tests for semantics; property/stateful tests for combinations; mutation tests for whether the oracle catches wrong implementations; and one end-to-end offline demonstration for packaging and artifact integrity. Avoid test counts as a proxy for engineering quality. Every seeded critical defect must be caught for an identified behavioral reason.

Expected values must come from the written contract, hand arithmetic, independent geometry inspection, or explicit state tables. Do not compute expected output by invoking the implementation under test. Freeze the oracle and case inventory in a distinct commit before the product-agent experiment.

## Required release evidence

Provide a manifest with commit and dirty-tree hash, environment lock hash, requirement IDs, input hashes, oracle hash, actual commands, exit codes, artifact hashes, and known limitations. Record cases as pass, fail, blocked, or not run. Supply a readable report and a representative negative example. Do not ship a prewritten passing result in place of running tests.

Target validation after implementation: formatter/linter, strict type check on core modules, pytest with relevant property tests, and the documented offline demo. Add a CI workflow only when its commands work locally; do not add decorative green badges before a real run.
