# FixtureForge specification

Status: implementation-ready proposal. No implementation or benchmark results are claimed.


## Restricted fixture family

Design a cylindrical sensor cradle with a lower base and an upper clamp. The sensor axis is X. The base lies on the XY mounting plane with Z upward. Sensor diameter D ranges 12–40 mm; supported length L ranges 25–80 mm. The fixture supports a defined 20 mm central axial band, leaving sensor ends and connector envelope accessible. Require L at least 25 mm so a five-millimeter total margin remains outside that band. Four mounting holes sit on a rectangular pattern outside the sensor envelope. Two M4 clamp screws join the halves through side ears.

Treat every input as millimeters with explicit field suffixes. The initial manufacturing profile is FDM with a 0.4 mm nozzle and 0.2 mm layer height; these are assumptions, not proof of printability or tolerances. Nominal diametral clearance is 0.4 mm; allowable configurable range 0.2–1.0 mm. Define bore_diameter = D + clearance_diametral. Nominal structural wall thickness is 3 mm, configurable 2.4–6 mm. Minimum base thickness is 5 mm. The build envelope for each part is 180 × 180 × 180 mm.

Use M4 through-hole diameter 4.5 mm, head-access cylinder diameter 9 mm, and vertical tool-access diameter 12 mm extending 25 mm above the head seat. These are deliberately chosen clearance envelopes, not claims of universal fastener-standard compliance. Use through bolts and nuts for version 1, with an explicitly modeled nut access volume; do not model printed threads.

The clamp has a 1 mm split gap at its mating plane so nominal halves cannot overlap. Screw bosses remain connected to their parent solid. The base's mounting pattern uses independent X/Y pitch inputs large enough to keep mounting holes outside the bore and structural walls. The generator computes minimum feasible pitches from the envelopes and rejects infeasible requested values instead of silently changing dimensions.

## Datums, checks, and physical limits

Datum A is the bottom mounting plane Z=0. Datum B is the plane X=0 at the center of the supported band. Datum C is the plane Y=0 through the sensor axis. All exported dimensions use this coordinate system. Define connector keepout as an axis-aligned box attached to the selected sensor end, with independently specified length, width, height, and cable exit clearance. The exact envelope belongs to the example specification, not a guessed catalog connector.

Check exact BREP validity, positive volume, and expected solid count before mesh export. The lower base and upper clamp must be separate valid single solids. Verify bore diameter and hole locations from exported/reimported STEP geometry, not just the original input variables. Use independent section/intersection queries and compare distances to specified tolerances. A geometric numerical tolerance of 0.05 mm is an acceptance threshold for software round-tripping; it does not describe printer accuracy.

Perform collision tests between each part and the sensor envelope, connector envelope, fastener envelope, and tool envelope, excluding explicitly intended contact interfaces and the fastener material passing through its intended clearance hole. Encode exclusions narrowly and test them; a blanket ignore list would hide real collisions. Validate the nominal insertion path using sampled translations along the chosen assembly direction and document that sampling cannot prove all continuous motions are collision-free.

Print each half with its flat split or mounting face on the bed, as appropriate. Report orientation and local geometric overhang warnings. Do not claim support-free printability, adequate clamping force, structural strength, thermal stability, fatigue life, or general DFM compliance from geometric checks. There is no FEA, slicer, G-code, or machine control in v1.

## Software boundaries and outputs

Proposed modules: requirements/, geometry/, export/, inspect/, generate/, report/. FixtureSpec has all dimensions, envelopes, manufacturing profile version, intended assembly direction, and source of assumptions. Prefer model-proposed FixtureSpec JSON compiled by deterministic geometry code. An optional freeform code-generation challenge uses a separate isolated runner and the same independent acceptance suite.

Output assembly.step, base.stl, clamp.stl, inspection.json, dimensions.svg, report.html, and manifest.json. Include input hash, CAD kernel and library versions, source commit, geometry hashes, assembly transform, and test results. Import STEP in a fresh process for verification. STL is a tessellated manufacturing convenience and cannot serve as the only dimensional oracle.

Target command, to be implemented: `python -m fixtureforge build examples/sensor_24mm.json --output artifacts/demo`. It exits nonzero for infeasible inputs or failed geometry. `python -m fixtureforge demo --offline --output artifacts/demo` additionally demonstrates a rejected candidate and corrected version. Commands are future interfaces, not implemented in this planning package.

## Reference designs and bounded complexity

Create six reference configurations spanning diameters 12, 16, 20, 24, 32, and 40 mm with distinct valid mounting pitches and connector envelopes. Create eight invalid cases: below-minimum wall, impossible pitch, connector collision, screw-head collision, inaccessible tool path, merged halves, invalid/empty solid, and envelope larger than the build volume. Add boundary combinations rather than assuming independent parameter ranges always compose to valid designs.

The principal engineering result is a reproducible mapping from requirements to validated geometry. Optional real printing adds a separate inspection sheet with instrument resolution, measurement locations, print profile, actual dimensions, and photographs. Never substitute CAD dimensions for measured dimensions in that sheet.

## Acceptance requirements

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
