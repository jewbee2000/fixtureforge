# Public interface 1.0

Use Python 3.12 on Windows x64 with the tested lock. `fixtureforge.api.build` and
`fixtureforge.api.inspect` return `(exit_code, result_dict)` and run all CAD work
in killable fresh processes. Pass JSON file and an empty output directory.
The CLI has the same contract:

```
python -m fixtureforge build examples/sensor_24mm.json --output artifacts/my-build
python -m fixtureforge inspect my-parts/access.json --output artifacts/my-inspection
python -m fixtureforge demo --offline --output artifacts/my-replay
```

Normal commands: 0 means all applicable checks passed; 1 means a geometric
violation; 2 means invalid, incomplete, unsupported or failed execution. An
existing nonempty output directory is rejected. An invalid output location is
reported on stdout; otherwise inspection.json always records the verdict.
The demo is different: it returns 0 when its deliberate failure was rejected
and its corrected fixture passed. It is labelled REPLAY, never live generation.

`--timeout` lowers the 120 second total CAD deadline; `--memory-mb` lowers the
2048 MiB sampled worker RSS limit. Memory is polled every 20 ms; native allocation
can temporarily overshoot. These controls are not a security sandbox. Max JSON
256 KiB, STEP 10 MiB/file, 20 parts, 40 paths, 2000 total imported faces.

JSON schemas are in schemas/. Fixture dimensions have explicit `_mm` suffixes;
documented defaults are applied to omitted fixture dimensions. Unknown keys,
units and versions fail. AccessSpec requires explicit `schema_version`, `units`,
parts and paths. Each part is a relative STEP file with SHA256, exactly one
solid, a unique ID and an optional translation in mm. Multiple identical solids
can have different IDs. STEP must declare millimeters; mixed or conversion-based
units are rejected rather than guessed. Paths cannot escape the input directory,
including through a symlink. External STEP inspection never calls the clamp
generator and never executes Python from input.

Each path supplies box dimensions or cylinder radius/height/axis, center start
and end coordinates, occupied part IDs, margin and optional intended end-contact
IDs. `orientation_deg` and `end_orientation_deg` must be zero. The axis field
orients cylinders along X/Y/Z. Only straight fixed-orientation translation is
supported. Axial sweeps are exact; diagonal box and nonaxial cylinder sweeps use
conservative axis-aligned bounds. Margins inflate all dimensions. Reports give
the nominal BREP distance and identify conservative bounds; distances there are
lower bounds on real clearance. Collision means overlap >1e-7 mm³ or touching
within 1e-6 mm, unless a named zero-volume final contact applies. Positive-volume
penetration is never ignored. A shortened full sweep tests that moving contact
occurs only at the endpoint. No articulated tool or curved path is supported.

Occupancy is authoritative per step, with no automatic sequence discovery.
For removal/reassembly, supply the remaining parts at each step in order. A
transition is a declared assembly assumption; the checker does not infer whether
removing that part is itself possible unless its removal path is also supplied.

The clamp profile uses M4-like synthetic envelopes, not a fastener standard.
It requires through bolts and 8×8×3 mm nut volumes below the base, with nuts
inserted before mounting. Mount on standoffs with at least 3 mm underside space.
The 0.4 mm diametral clearance and 1 mm split are nominal design assumptions;
they do not establish that the fixture grips the sensor. Radial wall containment
and a continuous base witness check are specific to this family, not arbitrary
minimum-wall analysis. Part-specific downward face warnings need slicer review.

Every inspection exports complete sweep STEP solids for other CAD tools. Run
`python scripts/cadclaw_check.py part.step sweep-path.step` for a CADCLAW static
cross-check. CADCLAW's own verdict semantics differ; FixtureForge's incomplete
result rules remain authoritative for this workflow.

Report artifacts include inspection.json, escaped standalone report.html,
actual-geometry dimensions.svg, manifest.json and sweep STEP files. Builds also
include named base/clamp STEP and STL, assembly.step and resolved input JSON.
STL has no intrinsic units: its mm convention is declared in the manifest.
No HTML includes remote scripts, fonts, telemetry, or network dependencies.
