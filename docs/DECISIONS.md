# Implementation decisions

## M0 contract, 2026-10-04

This is a narrow CadQuery integration, subject to the executable baseline gate.
Do not build a replacement CAD kernel or general validation framework. CADCLAW
is evaluated on the same independently authored solids before product code.

* Python 3.12, Windows x64; use the resolved, tested lockfile. No global packages.
* Explicit millimeters only. Input JSON schema version `1.0`; unknown keys fail.
* Imported part identity: relative STEP filename, SHA256, exactly one solid per
  file, unique user ID, explicit translation. This intentionally avoids guessing
  product identity from STEP order or bounding boxes. Export assembly STEP plus
  per-part STEP files. Multiple parts with the same shape remain distinct IDs.
* Initial orientation is axis-aligned. Motion is a fixed-orientation straight
  translation. Box sweeps use the enclosing axis-aligned box (exact for axial
  travel, conservative for diagonal travel). Cylinder travel along its axis uses
  an exact extended cylinder; transverse/diagonal travel uses its bounding box.
  The report must identify that extra conservatism. Rotation and curves are
  unsupported, never a clearance pass.
* Contact means a named part/path interface may touch with zero volume at the
  specified final pose only. It never suppresses a positive-volume collision.
  No blanket ignored-part list. Occupancy is explicit for every path.
* Numeric overlap tolerance: 1e-7 mm^3; contact distance: 1e-6 mm. Required
  clearance defaults to 0 mm; a positive user margin inflates each envelope.
* Limits frozen before measurement: JSON <= 256 KiB, each STEP <= 10 MiB,
  <= 20 parts, <= 40 paths, <= 2,000 faces total, coordinates <= 1,000 mm,
  dimensions <= 500 mm. Default deadline 120 seconds and worker RSS 2 GiB;
  request may lower these bounds. Target: each reference build < 60 seconds
  on this Dell XPS 15 9510, i9-11900H (8 cores/16 threads), 64 GiB RAM.
  Parent kills CAD worker on timeout/memory overrun; this is resource control,
  not a sandbox. No input code execution or live model interface is enabled.
* Clamp construction adds side ears outside the bore. Ear screw centers are
  Y=±(bore radius + wall + 7). Pitch X minimum 32 mm; pitch Y minimum twice
  (bore radius + wall + 14). Base footprint is (pitch X+12)×(pitch Y+12).
  Base thickness 5–12 mm; pitches <=160 mm; support band exactly 20 mm.
  These are documented design choices, not fastener standards. Nut access
  occurs before mounting; sensor then clamp, then screw/tool insertion.
* M4 overhang checks will report actual downward-facing planar faces and intended
  bed faces. This is a geometric warning, not slicer or printability approval.

Optional revision diff and model generation are deferred until the Must gates.
No generated-code experiment will run without the required isolation.
