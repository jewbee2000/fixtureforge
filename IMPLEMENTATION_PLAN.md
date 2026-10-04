# FixtureForge implementation plan

Revised 2026-10-04. Begin with [requirements and rationale](docs/REQUIREMENTS.md). The previous all-features-at-once plan is superseded by this useful-core-first sequence. The deterministic implementation now follows this sequence; see TASKS.md and evidence/progress.md for executed status. Estimates below were planning assumptions, not measured human effort.

## Purpose and feasibility

A fixture service-access checker plus a parametric sensor-clamp example: verify that connectors, screws, and tools can actually reach their intended positions. A part can be dimensionally correct while a screw cannot be tightened or a connector cannot be inserted. A repeatable access check could catch these errors before printing or machining. The sensor clamp gives a bounded practical example aligned with Walter's CAD, printing, and manufacturing interests.

The proposed contribution is explicit tool/connector access contracts and conservative straight-path clearance checks on imported geometry, with the clamp as one use case. This is the least established gap: evaluate CADCLAW first and build a compatible extension if that is sufficient. Confidence: low-to-medium until the M0 comparison and external STEP example work.

80–120 engineering hours as a provisional range, with the widest uncertainty. Re-estimate after the M0 CADCLAW and swept-envelope spike; a small integration is preferable if it solves the use case.

Core software can be built with minimal owner guidance, but novelty and adoption are not established. Use existing libraries and routine design judgment. Do not require physical measurements to finish a software release; do not claim those measurements occurred.

## Build sequence

### M0 Compare CADCLAW and prove the CAD stack

Work: Run the two access cases against existing tools; select reuse boundaries. Prove headless STEP round-trip, freeze path restrictions, collision tolerances, selectors, and intended-contact semantics.

Exit evidence: A concrete missing access check justifies the extension; simple independent solids validate the chosen kernel and swept-envelope construction.

Primary requirements: FF-01 FF-13. All earlier contracts remain regression requirements.

### M1 Check imported geometry and generate one fixture

Work: Build AccessSpec/import first, one external bracket example, then the 24 mm clamp with STEP/STL export.

Exit evidence: The external example does not call the generator; the clamp has two valid solids and independently measured dimensions.

Primary requirements: FF-02 FF-03 FF-08 FF-14. All earlier contracts remain regression requirements.

### M2 Verify clearance and independent geometry

Work: Build conservative straight-path sweeps, keepout checks, six reference clamps, eight invalid cases, and the between-samples obstruction case.

Exit evidence: Every invalid case fails for its intended reason; unsupported motion never passes as clear.

Primary requirements: FF-04 FF-05 FF-06 FF-07 FF-15 FF-19. All earlier contracts remain regression requirements.

### M3 Make reports useful for design review

Work: Show obstruction pairs, paths, datums, clearance, and assumptions. Add optional margin/sequence and revision comparison; model JSON is later work.

Exit evidence: An engineer can identify which tool path is blocked from the report and reproduce the check on imported STEP.

Primary requirements: FF-09 FF-10 FF-11 FF-16 FF-17 FF-18. All earlier contracts remain regression requirements.

### M4 Verify adoption and prepare the local release

Work: Run independent consumer walkthrough, fresh installation, boundary sweeps, resource/robustness checks, lint/types/tests, and exported artifact inspection. Update the blog honestly.

Exit evidence: All applicable Must checks pass; CAD evidence is clearly separate from physical printing or strength validation.

Primary requirements: FF-12 FF-20 FF-21 FF-22. All earlier contracts remain regression requirements.

## Method and dependencies

Use Python with a repository-local pinned environment; select compatible versions during M0. Read SPEC.md for existing reference-case constants. Requirements proceed M0 → M1 → M2 → M3 → M4; the machine-readable register identifies primary milestones and baseline dependencies. Tests and documentation evolve with each slice rather than accumulating at the end.

For every nontrivial feature: state the requirement, write an independent failing check, implement the smallest slice, inspect actual output, record evidence, and commit locally. Preserve known failures and explain repairs. A product model, elaborate UI, web service, or paid API is not needed for the useful first release. Reuse primary-source libraries after verifying current installation and capabilities.

## Model evaluation after the deterministic release


Freeze 20 evaluation specifications that were not used to tune the generator. For any live campaign, run each specification three times under one-shot JSON generation and three times under bounded repair: 120 model trials total. Compare against the deterministic parameterized builder on the same feasible specifications. Report validity, requirement satisfaction, attempts, and critical failures separately. A goal of 16 of 20 successful specifications is aspirational; all shipped reference designs must satisfy every critical rule regardless of model scores.

The evaluator's inputs are frozen before the campaign. One-shot and repair runs use the same budgets except for the explicitly reported repair allowance. Capture all attempts; do not discard unsuccessful trials. Separate a replay demonstration from a live model evaluation. These comparisons are project-local experiments, not claims about every AI model or engineering task.

## Risks and decision rules

The largest product risk is duplicating existing software or building a demonstration that accepts only its own fixtures. The M0 comparison and M4 independent consumer walkthrough are release gates. Prefer a narrow library/plugin when it satisfies the same needs. Do not silently drop external integration in order to finish a more impressive-looking demo.

If a technical dependency or required semantic cannot be implemented, record it as blocked or unsupported and do not label the release complete. If the entire useful contribution disappears after the baseline comparison, stop broad implementation and report the concrete result; do not invent novelty or ask for routine design approvals.

## Owner involvement and publication

No owner guidance is needed for routine architecture, naming, examples, or tests within these requirements. Physical tests, paid live model campaigns, and remote publication require separate resources or authorization. Do not contact maintainers or prospective users automatically. No pushes, deployment, or remote commits. Local commits are authorized.

## Definition of finished

All applicable Must requirements have independent executed evidence. Should/Could omissions and Won't scope are explicit. A clean consumer walkthrough works on a non-default input, and reports show a real detected failure and repair. The first-person article is updated only from observed work, remains unpublished, and has no invented anecdotes, physical measurements, or live-model scores. Hosted repositories and website publication remain pending a later instruction.
