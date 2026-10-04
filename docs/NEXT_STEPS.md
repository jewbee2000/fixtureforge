# Proposed next iteration

The deterministic release is implemented and its applicable Must requirements
have executed evidence. The next question is whether the access contract helps
an engineer with their own assembly. The following work is proposed; it has not
been executed by adding this roadmap.

## 1. Validate one real consumer workflow

Ask an independent mechanical/test engineer to supply a redistributable or
locally retained assembly they authored. Have them configure AccessSpec, inspect
one known obstruction, correct the design/path, and compare the result with
manual CAD inspection. Record setup friction, missed cases, conservative false
positives, and whether the report identifies an actionable design change.

Exit evidence: a documented practitioner walkthrough with permission to retain
its evidence. The existing agent-executed bracket walkthrough remains useful
installation evidence; it does not establish practitioner adoption. Do not
contact anyone automatically or put proprietary parts in the public repository.

## 2. Close the report presentation gap

Review generated reports in a normal browser at desktop and mobile widths.
Check the rejected/corrected navigation, pair labels, path diagrams, units,
datums, clearance values and conservative-sweep explanation. Keep screenshots
and fix any unreadable or misleading output. Static CAD images have been
inspected, but browser layout remains unverified.

Exit evidence: visual review of both a passing imported assembly and a rejected
case, with all local links working. This should precede presenting the report
as a polished design-review interface.

## 3. Put the existing release checks in Windows CI

Use the tested Python 3.12/Windows dependency pins in a fresh GitHub Actions
environment. Run dependency checks, Ruff, mypy, the acceptance suite and the
offline replay. Distinguish tests that execute CAD checks from assertions over
retained historical evidence. Upload generated CAD/reports as workflow artifacts
and record the commit and lockfile used by each run. Keep expected geometry
independent of production helpers.

Exit evidence: a successful fresh-run pipeline plus a demonstrated failure when
a known critical defect is introduced. Other operating systems can be added
only after their dependency installation and kernel behavior are verified.

## 4. Add revision comparison if consumer feedback supports it

FF-17 is the best next feature candidate: compare two inspection reports by
stable path and part IDs, identify newly blocked/cleared pairs, and link each
change to its visual view. Compare semantic geometry/results rather than STEP
bytes or report timestamps.

Exit evidence: relocating one boss introduces exactly the expected obstruction;
a no-change rebuild reports no semantic change. Keep this bounded to the
existing straight-path contract.

## 5. Validate the clamp physically if it will be presented as useful hardware

If an existing printer and suitable measurement tools are available, print one
reference pair and measure the bore, mounting pattern and split. Try the actual
sensor, fasteners, connector and driver in the prescribed assembly sequence.
Record material, print profile, instrument resolution, measurement locations,
photographs and failures. Verify that the split/clearance arrangement can grip
the sensor before making that claim. Strength/load testing needs a separate
defined procedure and evidence.

Physical work is optional for the software release. No purchases are authorized
by this roadmap. Model-generated proposals remain lower priority: retain the
offline core, require a separately authorized API budget, and establish real
isolation before any untrusted code execution.

## Publication state

The project is published at https://github.com/jewbee2000/fixtureforge under
Walter's 2026-10-04 authorization. No changes have been pushed to the blog
repository. The article remains a draft; later editorial approval, browser
preview and verified links are still required before blog publication.
