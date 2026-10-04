# FixtureForge implementation plan

## Purpose and feasibility

Parametric sensor fixtures checked for geometry, fit, and assembly access.

This connects directly to Walter's printed bicycle parts, Onshape/SolidWorks work, mechatronic assemblies, and manufacturing interests. It provides visual and downloadable engineering artifacts that complement the other two software-heavy projects.

High for a restricted parameterized fixture and automated geometry checks; medium for reliable generated CAD code; physical fit and strength need measurements. The core uses a deterministic CAD builder. The optional model proposes parameters first, which is easier to verify than arbitrary CAD programs.

65–95 engineering hours for the complete original scope. First validate build123d and STEP round-tripping before investing in interface work. Optional owner review: 30–60 minutes for the fixture assumptions and final artifact; a later print-and-fit experiment is useful but not required.

## The result a visitor should see

Enter a sensor diameter, length, mounting pitch, and connector keepout. Generate a two-part clamp, STEP/STL files, and an inspection sheet. Show a visually plausible candidate rejected because a screw head or connector cannot be reached, then a corrected geometry.

## Technical approach

Python 3.12 if supported by the selected stable build123d release; otherwise pin a supported Python version after the spike. build123d/OpenCascade, Pydantic, NumPy, pytest, Hypothesis, Typer. Start with CLI, exported SVG/PNG views, and an HTML inspection report. Add an interactive mesh viewer only after geometry verification.

The public repository must be useful without live AI. The strongest evidence is a requirement that becomes an independent check, a candidate that fails it, and a justified repair. Do not turn the project into a generic chat interface. Retain the original research's specification, verification, and bounded repair approach while narrowing the first release to something one coding agent can complete.

## M0 Prove the CAD environment and freeze dimensions

Work: Install a supported stable build123d stack; create/export/reimport a simple block with a hole. Finalize coordinate system, sensor envelope, fixture rules, and hand measurements.

Exit evidence: CAD import/export works headlessly; supported Python/kernel versions are locked; dimension queries recover the known block.

Requirements: FF-01 FF-03 FF-08. Planning estimate: 12–18 h.


## M1 Build one deterministic fixture

Work: Implement validated FixtureSpec and base/clamp generation for the 24 mm reference case, plus STEP/STL export.

Exit evidence: Two valid solids and hand-checked nominal dimensions; cleanly reject impossible input.

Requirements: FF-01 FF-02 FF-03 FF-08. Planning estimate: 15–22 h.


## M2 Build independent geometry checks

Work: Add reimported geometry inspection, connector and fastener keepouts, assembly sampling, six references, and eight invalid cases.

Exit evidence: Every invalid case fails for the expected reason; no oracle calls geometry-builder dimension helpers.

Requirements: FF-04 FF-05 FF-06 FF-07. Planning estimate: 15–22 h.


## M3 Add constrained generation and report

Work: Accept model-proposed JSON, show failure-guided parameter repair using replay, and export inspection sheets. Freeform CAD generation is optional.

Exit evidence: Rejected candidate and corrected geometry are visible; assumptions and geometric limits are prominent.

Requirements: FF-09 FF-10 FF-11. Planning estimate: 10–15 h.


## M4 Prepare the portfolio release

Work: Exercise boundary configurations, document commands, capture geometry views, record evidence, and finish the blog.

Exit evidence: A fresh environment builds examples and validates exports. A physical fit check remains explicitly optional.

Requirements: FF-07 FF-08 FF-11 FF-12. Planning estimate: 13–18 h.


## Model evaluation after the deterministic release

Freeze 20 evaluation specifications that were not used to tune the generator. For any live campaign, run each specification three times under one-shot JSON generation and three times under bounded repair: 120 model trials total. Compare against the deterministic parameterized builder on the same feasible specifications. Report validity, requirement satisfaction, attempts, and critical failures separately. A goal of 16 of 20 successful specifications is aspirational; all shipped reference designs must satisfy every critical rule regardless of model scores.

The evaluator's inputs are frozen before the campaign. One-shot and repair runs use the same budgets except for the explicitly reported repair allowance. Capture all attempts; do not discard unsuccessful trials. Separate a replay demonstration from a live model evaluation. These comparisons are project-local experiments, not claims about every AI model or engineering task.

## Risks and fallback decisions

Robust geometry and assembly reasoning are the main risks. Limit the parameter domain, reject impossible combinations, measure exported solids, and show rejected cases. An API call reporting success does not establish manufacturability. If build123d cannot be installed in the current runtime, resolve that environment problem before proceeding; do not substitute mock meshes and present them as CAD results. A print is optional evidence, not something an agent can truthfully simulate.

## Owner involvement

No response from Walter is needed for routine naming, data models, fixtures, UI choices, or test implementation within this specification. The agent can define missing synthetic examples and document assumptions. Ask only when a decision would materially change the project's claim or exceed the authorized environment. An optional final review of the first-person article would improve the voice; no invented memory or measured result should be used to avoid that review.

Before any live API campaign, a model adapter, credential, and spending ceiling are needed. None is required for the deterministic product or replay. Physical validation requires Walter to perform or arrange the measurement. Remote publication requires a later instruction because the present instruction forbids pushes.

## Definition of finished

All required behaviors in docs/SPEC.md have independent evidence. The README gives a working fresh-clone setup and offline demo. Artifacts are real, versioned, and labeled by scope. The code, tests, environment lockfile, architecture, evidence, and article are locally committed. A future publication step creates or selects the GitHub repository, pushes the reviewed commits, verifies public links, then publishes the matching website article. Until that later step, remote GitHub and live-site completion remain pending.
