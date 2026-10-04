# Publication audit — October 4, 2026

This is a later review for Walter's consolidated article about four AI coding
projects. It is separate from the original implementation evidence. The starting
repository commit was `e6dc788`; the application source and acceptance oracle
were unchanged during this audit.

## Re-executed checks

- `python -m pytest -q --junitxml=artifacts/article-audit-acceptance.xml`:
  **61 passed in 89.58 seconds**. The resulting JUnit file is retained here.
- `python -m ruff check src scripts tests`: passed.
- `python -m mypy src/fixtureforge`: passed, 12 source files.
- `python -m pip check`: no broken requirements.

The 61 cases include four assertions over historical baseline, consumer and
performance evidence. Running pytest does not reinstall the clean consumer or
repeat the entire baseline campaign. It does rerun the six reference builds,
external bracket failure/repair, independent STEP/STL inspection, eight seeded
defect causes, input/resource checks and the offline demo. Test counts are an
inventory, not a quality score.

## Browser inspection

Served the retained `artifacts/release-demo` reports over `127.0.0.1` and inspected
them in the Codex in-app browser. The original browser blockage did not recur.
Checked the rejected and corrected reports at the default desktop viewport and
390 px mobile width. Text and diagrams were readable; the observed mobile page
widths did not exceed the viewport. The rejected report's SVG loaded, and the
corrected tool path's PASS status and zero overlap were visible. No application
or CSS fix was required. This is a visual check of these two replay reports,
not a browser compatibility or accessibility certification.

- [Rejected report, desktop](rejected-report-desktop.jpg): tool-1 fails against
  the clamp with **382.377 mm³** computed overlap.
- [Rejected report, mobile](rejected-report-mobile.jpg): the projections stack.
- [Corrected tool card, desktop](corrected-tool-desktop.jpg): zero overlap;
  the near-zero numerical gap is the declared intended end contact.
- [Corrected report, mobile](corrected-report-mobile.jpg): long check identifiers
  and PASS labels remain readable.

These are browser screenshots, not fabricated output. The original
`../replay.png` is a clearer side-by-side CAD visualization for the article.

## Reproducibility cleanup

The original `scripts/benchmark.py` always reused `artifacts/performance-0`
through `performance-2`, even though builds correctly reject nonempty output
directories. The README asked for fresh outputs without providing a way to
select them. The script now requires `--output NEW_DIRECTORY`, stores its three
builds and `performance.json` together, retains a failure log if a build fails,
and takes platform/Python information from the measured manifest. It does not
overwrite the original `evidence/performance.json` or print a hardcoded machine
identity when used on another computer.

Executed the updated script with
`python scripts/benchmark.py --output artifacts/publication-audit-benchmark`;
the new results are retained in [performance.json](performance.json). This is
audit-phase work, not an achievement retroactively attributed to the first run.

## Remaining limits

The code is a small, readable CadQuery integration for declared straight paths.
It does not demonstrate physical grip, load capacity, print quality, practitioner
adoption, arbitrary motion planning, live model generation or OS sandboxing.
The test oracle and implementation were written by the same coding agent in
separate commits; structural separation is useful but not independent human
validation. Windows CI and real practitioner feedback remain future work.
