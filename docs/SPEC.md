# FixtureForge specification

Status: deterministic implementation with executed evidence in ../evidence/progress.md. Reference dimensions remain the contract; see DECISIONS.md and PUBLIC_API.md for documented implementation choices. Physical measurements remain absent. Read [REQUIREMENTS.md](REQUIREMENTS.md) first for priorities, rationale, external-user interfaces, and release gates.


## Restricted fixture family

Design a cylindrical sensor cradle with a lower base and an upper clamp. The sensor axis is X. The base lies on the XY mounting plane with Z upward. Sensor diameter D ranges 12–40 mm; supported length L ranges 25–80 mm. The fixture supports a defined 20 mm central axial band, leaving sensor ends and connector envelope accessible. Require L at least 25 mm so a five-millimeter total margin remains outside that band. Four mounting holes sit on a rectangular pattern outside the sensor envelope. Two M4 clamp screws join the halves through side ears.

Treat every input as millimeters with explicit field suffixes. The initial manufacturing profile is FDM with a 0.4 mm nozzle and 0.2 mm layer height; these are assumptions, not proof of printability or tolerances. Nominal diametral clearance is 0.4 mm; allowable configurable range 0.2–1.0 mm. Define bore_diameter = D + clearance_diametral. Nominal structural wall thickness is 3 mm, configurable 2.4–6 mm. Minimum base thickness is 5 mm. The build envelope for each part is 180 × 180 × 180 mm.

Use M4 through-hole diameter 4.5 mm, head-access cylinder diameter 9 mm, and vertical tool-access diameter 12 mm extending 25 mm above the head seat. These are deliberately chosen clearance envelopes, not claims of universal fastener-standard compliance. Use through bolts and nuts for version 1, with an explicitly modeled nut access volume; do not model printed threads.

The clamp has a 1 mm split gap at its mating plane so nominal halves cannot overlap. Screw bosses remain connected to their parent solid. The base's mounting pattern uses independent X/Y pitch inputs large enough to keep mounting holes outside the bore and structural walls. The generator computes minimum feasible pitches from the envelopes and rejects infeasible requested values instead of silently changing dimensions.

## Datums, checks, and physical limits

Datum A is the bottom mounting plane Z=0. Datum B is the plane X=0 at the center of the supported band. Datum C is the plane Y=0 through the sensor axis. All exported dimensions use this coordinate system. Define connector keepout as an axis-aligned box attached to the selected sensor end, with independently specified length, width, height, and cable exit clearance. The exact envelope belongs to the example specification, not a guessed catalog connector.

Check exact BREP validity, positive volume, and expected solid count before mesh export. The lower base and upper clamp must be separate valid single solids. Verify bore diameter and hole locations from exported/reimported STEP geometry, not just the original input variables. Use independent section/intersection queries and compare distances to specified tolerances. A geometric numerical tolerance of 0.05 mm is an acceptance threshold for software round-tripping; it does not describe printer accuracy.

Perform collision tests between each part and the sensor envelope, connector envelope, fastener envelope, and tool envelope, excluding explicitly intended contact interfaces and the fastener material passing through its intended clearance hole. Encode exclusions narrowly and test them; a blanket ignore list would hide real collisions. For supported fixed-orientation straight paths, validate the complete conservative swept envelope under FF-15. Sampled translations may illustrate the motion but cannot justify a continuous-path pass; unsupported motion is explicitly inconclusive.

Print each half with its flat split or mounting face on the bed, as appropriate. Report orientation and local geometric overhang warnings. Do not claim support-free printability, adequate clamping force, structural strength, thermal stability, fatigue life, or general DFM compliance from geometric checks. There is no FEA, slicer, G-code, or machine control in v1.

## Software boundaries and outputs

Proposed modules: requirements/, geometry/, export/, inspect/, generate/, report/. FixtureSpec has all dimensions, envelopes, manufacturing profile version, intended assembly direction, and source of assumptions. Prefer model-proposed FixtureSpec JSON compiled by deterministic geometry code. An optional freeform code-generation challenge uses a separate isolated runner and the same independent acceptance suite.

Output assembly.step, base.stl, clamp.stl, inspection.json, dimensions.svg, report.html, and manifest.json. Include input hash, CAD kernel and library versions, source commit, geometry hashes, assembly transform, and test results. Import STEP in a fresh process for verification. STL is a tessellated manufacturing convenience and cannot serve as the only dimensional oracle.

Implemented command: `python -m fixtureforge build examples/sensor_24mm.json --output artifacts/demo`. It exits nonzero for infeasible inputs or failed geometry. `python -m fixtureforge demo --offline --output artifacts/demo` additionally demonstrates a rejected candidate and corrected version. These commands are implemented; see PUBLIC_API.md for failure semantics.

## Reference designs and bounded complexity

Create six reference configurations spanning diameters 12, 16, 20, 24, 32, and 40 mm with distinct valid mounting pitches and connector envelopes. Create eight invalid cases: below-minimum wall, impossible pitch, connector collision, screw-head collision, inaccessible tool path, merged halves, invalid/empty solid, and envelope larger than the build volume. Add boundary combinations rather than assuming independent parameter ranges always compose to valid designs.

The principal engineering result is a reproducible mapping from requirements to validated geometry. Optional real printing adds a separate inspection sheet with instrument resolution, measurement locations, print profile, actual dimensions, and photographs. Never substitute CAD dimensions for measured dimensions in that sheet.

## Public interface applicability

The two-solid count, six valid clamps, eight invalid clamps, and 0.05 mm dimensional tolerance apply to the generated sensor-clamp family. Imported assemblies may have any supported declared part count; they are judged against AccessSpec, not the clamp dimension rules. A clearance pass means the conservative envelope is clear under the stated nominal geometry and tolerance. An envelope intersection can be a conservative obstruction, not proof that a real articulated tool could never fit. Reports must distinguish these outcomes.

## Acceptance requirements

The authoritative rationale, applicability, and independent acceptance evidence for these requirements are in [REQUIREMENTS.md](REQUIREMENTS.md). Reference-case behavior above does not replace the public-interface requirements.

| ID | Priority | Milestone | Requirement |
| --- | --- | --- | --- |
| FF-01 | must | M0 | FixtureSpec validates units, bounds, and coupled feasibility constraints before geometry construction. |
| FF-02 | must | M1 | Every accepted configuration produces exactly two valid, positive-volume single solids. |
| FF-03 | must | M1 | Bore, hole pitches, base thickness, and datums agree with requirements within 0.05 mm. |
| FF-04 | must | M2 | Sensor and connector keepouts remain clear except for explicitly intended contact surfaces. |
| FF-05 | must | M2 | Fastener and tool-access envelopes remain usable in the prescribed assembly sequence. |
| FF-06 | must | M2 | Wall, base, and build-volume requirements are checked on generated geometry. |
| FF-07 | must | M2 | All six reference designs pass and all eight invalid cases are rejected for their intended cause. |
| FF-08 | must | M1 | STEP and STL export preserve units and per-part identity; round trips remain within tolerance. |
| FF-09 | must | M3 | Offline demonstration shows a rejected candidate and a corrected fixture without a model service. |
| FF-10 | must | M3 | Any generated-code experiment uses bounded isolation and a read-only evaluator. |
| FF-11 | must | M3 | Inspection output separates computed geometry from unmeasured physical fit and strength. |
| FF-12 | must | M4 | Fresh installation and deterministic inputs reproduce the required artifacts within numerical tolerance. |
| FF-13 | must | M0 | Compare CADCLAW and direct CadQuery/build123d checks on a screw-tool obstruction and connector insertion case before building the checker. |
| FF-14 | must | M1 | Check externally authored STEP parts using an explicit AccessSpec JSON without calling the clamp generator. |
| FF-15 | must | M2 | For v1, tool and connector paths are fixed-orientation straight translations of supported convex box/cylinder envelopes; test the entire conservative swept envelope. |
| FF-16 | should | M3 | Support user-specified tool clearance margins and removal/reassembly sequences with explicit remaining-part occupancy. |
| FF-17 | should | M3 | Compare inspection reports between CAD revisions and locate changed obstruction pairs in a visual view. |
| FF-18 | could | M3 | Add model-proposed FixtureSpec JSON and bounded repair as an optional demonstration after deterministic geometry and access checking work. |
| FF-19 | must | M2 | Publish a versioned input and result schema, stable requirement IDs, public Python API, and a scriptable CLI with clear failure semantics. |
| FF-20 | must | M4 | Declare resource limits and measure repeatable performance for the supported workload in the pinned environment. |
| FF-21 | must | M4 | Keep offline workflows local by default and document dependency, fixture, manual, and example licensing. |
| FF-22 | must | M4 | Demonstrate adoption from a separate clean consumer directory using only the documented public interface. |
