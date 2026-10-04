# FixtureForge

Parametric sensor fixtures checked for geometry, fit, and assembly access.

**Status: planned; implementation has not started.** This repository contains the requirements, execution plan, acceptance design, and blog draft for an agent-assisted engineering project. It does not yet contain working application code or benchmark results.

Start with [START_HERE.md](START_HERE.md). The [implementation plan](IMPLEMENTATION_PLAN.md) defines the build and [specification](docs/SPEC.md) defines what must be proven.

The intended demonstration: Enter a sensor diameter, length, mounting pitch, and connector keepout. Generate a two-part clamp, STEP/STL files, and an inspection sheet. Show a visually plausible candidate rejected because a screw head or connector cannot be reached, then a corrected geometry.

The final release must run offline without hardware or a model key. Live AI evaluations and physical validation, where applicable, are separate and explicitly labeled.
