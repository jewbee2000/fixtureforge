# FixtureForge requirements and rationale

Revision 2026-10-04. Status: planned, not implemented. This audit supersedes the earlier unprioritized feature list. [requirements.json](../requirements.json) is the machine-readable register; [SPEC.md](SPEC.md) supplies detailed reference-case constants and contracts. Keep them synchronized.

## Purpose and practical value

A fixture service-access checker plus a parametric sensor-clamp example: verify that connectors, screws, and tools can actually reach their intended positions.

**Intended user:** A mechanical or test engineer designing small fixtures who wants repeatable checks of connector and tool access after CAD changes.

**Job to be done:** Supply STEP solids and an explicit JSON description of tools, datums, keepouts, assembly state, and insertion paths; receive a visual report identifying blocked access and the relevant geometry.

**Why it matters:** A part can be dimensionally correct while a screw cannot be tightened or a connector cannot be inserted. A repeatable access check could catch these errors before printing or machining. The sensor clamp gives a bounded practical example aligned with Walter's CAD, printing, and manufacturing interests.

## Existing tools and the proposed contribution

CADCLAW already provides STEP assembly validation, interference, dimensional checks, tolerance analysis, reports, and disassembly visualization. Its reviewed disassembly.py chooses removal axes and exports translated frames; that routine does not establish collision-free swept paths. CadQuery/build123d already provide parametric geometry. Broad claims such as a new pytest for CAD would be misleading.

The proposed contribution is explicit tool/connector access contracts and conservative straight-path clearance checks on imported geometry, with the clamp as one use case. This is the least established gap: evaluate CADCLAW first and build a compatible extension if that is sufficient. Confidence: low-to-medium until the M0 comparison and external STEP example work.

Research checked on 2026-10-04. This is a bounded comparison of public documentation and selected source code, not proof that no competing tool exists. No interviews, field deployments, or independent user adoption have been conducted. Do not claim industry validation or unique invention. A useful integration or plugin is an acceptable outcome.

- [CADCLAW capabilities and scope](https://github.com/sunnyday-technologies/CADCLAW)
- [CADCLAW disassembly implementation](https://github.com/sunnyday-technologies/CADCLAW/blob/main/cadclaw/disassembly.py)
- [CadQuery](https://github.com/CadQuery/cadquery)
- [build123d](https://github.com/gumyr/build123d)

## Priorities and release policy

Must means release blocking for its stated applicability. Should is valuable but can be deferred with a written reason. Could is optional and must not delay a useful core. Won't means excluded from v1. Conditional Must requirements do not force an optional feature into the release; if that feature is enabled, its checks are mandatory.

M0 must establish a concrete gap or a useful integration before broad implementation. If the baseline already solves the chosen workflow, deliver the smallest reusable extension/examples package and document that choice. Do not pad scope to preserve the project name. Keep all required evidence and explain any revised requirement before implementing it.

Requirements are proposed engineering decisions, not discovered industry standards. The sample thresholds in SPEC.md are explicit reference-case choices. Users must be able to state their own contracts where the public interface supports them.

## Reference profiles and external inputs

The two-solid count, six valid clamps, eight invalid clamps, and 0.05 mm dimensional tolerance apply to the generated sensor-clamp family. Imported assemblies may have any supported declared part count; they are judged against AccessSpec, not the clamp dimension rules. A clearance pass means the conservative envelope is clear under the stated nominal geometry and tolerance. An envelope intersection can be a conservative obstruction, not proof that a real articulated tool could never fit. Reports must distinguish these outcomes.

## Requirement register
### FF-01 — Must — M0

FixtureSpec validates units, bounds, and coupled feasibility constraints before geometry construction.

**Rationale:** Individually legal dimensions can combine into impossible geometry; reject rather than silently redesign.

**Acceptance:** Reject negative, nonfinite, out-of-range, and impossible pitch/diameter combinations with a specific explanation.

**Applies:** Core v1 release **Planned evidence:** `tests/acceptance/test_input_validation.py`. **Status:** not implemented.

### FF-02 — Must — M1

Every accepted configuration produces exactly two valid, positive-volume single solids.

**Rationale:** Pretty meshes are not sufficient evidence of valid editable manufacturing solids.

**Acceptance:** Inspect each BREP and STEP reimport in a fresh process; reject null, merged, or self-invalid geometry.

**Applies:** Core v1 release **Planned evidence:** `tests/acceptance/test_solid_validity.py`. **Status:** not implemented.

### FF-03 — Must — M1

Bore, hole pitches, base thickness, and datums agree with requirements within 0.05 mm.

**Rationale:** Inspecting exports independently catches generator mistakes and conversion drift.

**Acceptance:** Independent section/edge/plane queries of reimported STEP measure dimensions.

**Applies:** Core v1 release **Planned evidence:** `tests/acceptance/test_dimensional_conformance.py`. **Status:** not implemented.

### FF-04 — Must — M2

Sensor and connector keepouts remain clear except for explicitly intended contact surfaces.

**Rationale:** A nominally fitting clamp is unusable if it obstructs the sensor or connector.

**Acceptance:** Boolean intersections and known collision mutations verify the rule and its exclusions.

**Applies:** Core v1 release **Planned evidence:** `tests/acceptance/test_keepout_clearance.py`. **Status:** not implemented.

### FF-05 — Must — M2

Fastener and tool-access envelopes remain usable in the prescribed assembly sequence.

**Rationale:** Fasteners need a usable tool path, not just a correctly sized hole.

**Acceptance:** Conservative swept tool envelopes identify intentional inaccessible configurations; sampled frames only illustrate the specified straight path and cannot establish clearance.

**Applies:** Core v1 release **Planned evidence:** `tests/acceptance/test_assembly_access.py`. **Status:** not implemented.

### FF-06 — Must — M2

Wall, base, and build-volume requirements are checked on generated geometry.

**Rationale:** Manufacturing rules must be checked against the actual shape rather than trusted input metadata.

**Acceptance:** Deliberately thin or oversized parts fail even if their input metadata claims compliance.

**Applies:** Core v1 release **Planned evidence:** `tests/acceptance/test_manufacturing_geometry.py`. **Status:** not implemented.

### FF-07 — Must — M2

All six reference designs pass and all eight invalid cases are rejected for their intended cause.

**Rationale:** Known invalid designs test whether the geometry inspector catches realistic mistakes.

**Acceptance:** Frozen inventory and explicit case-to-requirement mapping, not just counting nonzero exits.

**Applies:** Core v1 release **Planned evidence:** `tests/acceptance/test_case_inventory.py`. **Status:** not implemented.

### FF-08 — Must — M1

STEP and STL export preserve units and per-part identity; round trips remain within tolerance.

**Rationale:** Engineers need interoperable editable geometry and unambiguous units.

**Acceptance:** Reimport STEP, compare volume/bounds, and check STL watertightness and triangle orientation.

**Applies:** Core v1 release **Planned evidence:** `tests/acceptance/test_export_integrity.py`. **Status:** not implemented.

### FF-09 — Must — M3

Offline demonstration shows a rejected candidate and a corrected fixture without a model service.

**Rationale:** The useful core should work without paid model access.

**Acceptance:** Run without credentials and network; inspect actual generated CAD and reports.

**Applies:** Core v1 release **Planned evidence:** `tests/acceptance/test_offline_demo.py`. **Status:** not implemented.

### FF-10 — Must — M3

Any generated-code experiment uses bounded isolation and a read-only evaluator.

**Rationale:** A generated script must not be able to rewrite the inspector or escape its execution boundary.

**Acceptance:** Timeout, path-escape, and evaluator-write probes fail; JSON-only generation cannot execute code.

**Applies:** Only when executing untrusted generated code; ordinary STEP/JSON inspection must not execute Python from its inputs. **Planned evidence:** `tests/acceptance/test_generation_boundary.py`. **Status:** not implemented.

### FF-11 — Must — M3

Inspection output separates computed geometry from unmeasured physical fit and strength.

**Rationale:** Geometric clearance is not evidence of clamping force, print quality, or physical strength.

**Acceptance:** Report labels geometric checks, assumptions, and absent physical tests explicitly.

**Applies:** Core v1 release **Planned evidence:** `tests/acceptance/test_claim_boundaries.py`. **Status:** not implemented.

### FF-12 — Must — M4

Fresh installation and deterministic inputs reproduce the required artifacts within numerical tolerance.

**Rationale:** Kernel versions and numerical tolerance matter more than byte-identical STEP exports.

**Acceptance:** Record stable versions; compare geometry semantically rather than assuming STEP file bytes are invariant.

**Applies:** Core v1 release **Planned evidence:** `tests/acceptance/test_reproducibility.py`. **Status:** not implemented.

### FF-13 — Must — M0

Compare CADCLAW and direct CadQuery/build123d checks on a screw-tool obstruction and connector insertion case before building the checker.

**Rationale:** The original plan overlaps heavily with an existing open-source project.

**Acceptance:** Record pinned versions, precise supported checks, actual geometry, and missing behavior in docs/BASELINE.md. If a configuration or small plugin meets the requirements, build that integration rather than a generic CAD validation platform.

**Applies:** Core v1 release **Planned evidence:** `tests/acceptance/test_baseline_artifacts.py`. **Status:** not implemented.

### FF-14 — Must — M1

Check externally authored STEP parts using an explicit AccessSpec JSON without calling the clamp generator.

**Rationale:** The checker must help engineers with their CAD, not only validate geometry it generated itself.

**Acceptance:** An independently scripted bracket/connector example imports through the public API and finds one known obstruction. Require mm units, stable part selectors, transforms, tool envelopes, and intended contacts; ambiguous identities or units are an error.

**Applies:** Core v1 release **Planned evidence:** `tests/acceptance/test_external_step.py`. **Status:** not implemented.

### FF-15 — Must — M2

For v1, tool and connector paths are fixed-orientation straight translations of supported convex box/cylinder envelopes; test the entire conservative swept envelope.

**Rationale:** Sampling can miss an obstruction; restricted geometry makes a meaningful full-path check feasible.

**Acceptance:** Freeze start/end transforms and assembly occupancy per step. A known obstruction between coarse sample positions must be caught. Reject unsupported rotation, curved motion, or failed Boolean geometry as unsupported/inconclusive, never clear. Report nominal clearance and any conservative inflation. Sampled illustrations alone cannot yield a continuous-path pass.

**Applies:** Core v1 release **Planned evidence:** `tests/acceptance/test_swept_access.py`. **Status:** not implemented.

### FF-16 — Should — M3

Support user-specified tool clearance margins and removal/reassembly sequences with explicit remaining-part occupancy.

**Rationale:** Different tools and maintenance sequences need different envelopes; avoid claiming universal wrench access.

**Acceptance:** Changing a margin around a known threshold changes the verdict predictably. Removing a part clears only the documented subsequent steps. Unknown sequence rules are rejected.

**Applies:** If selected after Must requirements pass **Planned evidence:** `tests/acceptance/test_access_sequence.py`. **Status:** not implemented.

### FF-17 — Should — M3

Compare inspection reports between CAD revisions and locate changed obstruction pairs in a visual view.

**Rationale:** This makes access constraints useful in everyday design review and CI.

**Acceptance:** A relocated boss introduces one new tool collision; identify the affected path and parts. A no-change rebuild produces no semantic difference.

**Applies:** If selected after Must requirements pass **Planned evidence:** `tests/acceptance/test_inspection_diff.py`. **Status:** not implemented.

### FF-18 — Could — M3

Add model-proposed FixtureSpec JSON and bounded repair as an optional demonstration after deterministic geometry and access checking work.

**Rationale:** The portfolio objective is satisfied by a verified agent-built tool, without making model generation a dependency.

**Acceptance:** Validate model JSON through the same schema and inspector; preserve failed attempts. Freeform code requires separate isolation and is not part of normal import.

**Applies:** If selected after Must requirements pass **Planned evidence:** `tests/acceptance/test_optional_generation.py`. **Status:** not implemented.

### FF-19 — Must — M2

Publish a versioned input and result schema, stable requirement IDs, public Python API, and a scriptable CLI with clear failure semantics.

**Rationale:** CI must not confuse an unsupported check or crashed evaluator with a valid result.

**Acceptance:** For normal check commands: exit 0 only when every applicable required check passes; exit 1 for violations; exit 2 for invalid, incomplete, unsupported, or failed execution. Results preserve individual pass/fail/inconclusive/not_applicable states. The demo command separately verifies its expected negative cases. Unknown schema versions are rejected.

**Applies:** Core v1 release **Planned evidence:** `tests/acceptance/test_public_contract.py`. **Status:** not implemented.

### FF-20 — Must — M4

Declare resource limits and measure repeatable performance for the supported workload in the pinned environment.

**Rationale:** A tool that hangs or silently drops large input cannot be trusted in an engineering workflow.

**Acceptance:** During M0 freeze input-size/case limits and a target runtime with machine details. M4 records actual elapsed time and peak memory; an oversized input or elapsed-time limit produces a bounded error and incomplete result. CAD work runs in a killable worker. Compare against the baseline; do not claim universal performance.

**Applies:** Core v1 release **Planned evidence:** `tests/acceptance/test_resource_limits.py`. **Status:** not implemented.

### FF-21 — Must — M4

Keep offline workflows local by default and document dependency, fixture, manual, and example licensing.

**Rationale:** Engineers must be able to inspect data handling and legally reuse the code and examples.

**Acceptance:** No credentials or telemetry are needed; the offline demo completes with egress disabled after installation. Source examples have provenance and redistributable licenses, or use a download recipe and lawful independently authored fixtures. Escape user text in HTML; reject output path traversal and avoid executing input data.

**Applies:** Core v1 release **Planned evidence:** `tests/acceptance/test_data_and_license_boundaries.py`. **Status:** not implemented.

### FF-22 — Must — M4

Demonstrate adoption from a separate clean consumer directory using only the documented public interface.

**Rationale:** A successful bundled demo alone is not evidence that another engineer can use the tool.

**Acceptance:** Record a complete cold-start walkthrough: install, configure one non-default input, get an expected failure, correct it, and reproduce success without editing package source. Include actual commands, setup time, code/config size, and limitations versus the baseline. Label agent-executed walkthroughs as such; practitioner validation remains unverified until real feedback exists.

**Applies:** Core v1 release **Planned evidence:** `tests/acceptance/test_consumer_walkthrough.py`. **Status:** not implemented.

## Explicit scope exclusions

### FF-W01 — Won't have in v1

**A generic CAD system or replacement for CADCLAW, CadQuery, or build123d.** Reuse kernels and inspection capabilities; the differentiator is a bounded access workflow.

Verification: Absent from the v1 supported-features list; README and reports do not claim this capability.

### FF-W02 — Won't have in v1

**Arbitrary motion planning, articulated wrenches, flexible cable routing, or automatic assembly sequence discovery.** A fixed straight path has a tractable geometric contract; general motion planning is a separate project.

Verification: Absent from the v1 supported-features list; README and reports do not claim this capability.

### FF-W03 — Won't have in v1

**Automatic interpretation of unlabeled STEP intent or arbitrary GD&T drawings.** Parts, datums, contact exceptions, units, and access paths must be explicit.

Verification: Absent from the v1 supported-features list; README and reports do not claim this capability.

### FF-W04 — Won't have in v1

**FEA, machining toolpaths, G-code, or certified DFM analysis.** These need process/material models and validation beyond geometric inspection.

Verification: Absent from the v1 supported-features list; README and reports do not claim this capability.

### FF-W05 — Won't have in v1

**Claims of physical fit, adequate clamping force, strength, or printability without measurements.** The 0.05 mm threshold is software inspection tolerance, not manufacturing capability.

Verification: Absent from the v1 supported-features list; README and reports do not claim this capability.

## Completion and actual usefulness

Technical readiness requires passing evidence for every applicable Must requirement, explicit dispositions for Should items, a negative-case demonstration, a clean installation, and an external consumer example. A failing or inconclusive required check blocks a successful result. All planned test paths above are future work.

Practical usefulness is a separate hypothesis. Record the baseline comparison and the consumer walkthrough, including friction and limitations. A later independent engineer using the tool on their own driver, trace, or CAD assembly would be stronger evidence. Do not contact anyone or fabricate that validation. The first release may honestly be described as a useful candidate tool with demonstrated workflows, not a field-proven industry standard.

Retain the agentic workflow: commit the contract and independent oracle before candidate repair; make small reviewable changes; inject known defects; preserve failed attempts and environment hashes. Product AI features are optional. Development history and reproducible engineering checks are the primary portfolio evidence. No pushes, deployment, paid APIs, or hardware purchases are authorized by this plan.
