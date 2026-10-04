# Implementation tasks

All tasks below are unstarted. The preparation commit contains specifications and editorial drafts, not application code.

- [ ] M0 — Prove the CAD environment and freeze dimensions. Evidence: CAD import/export works headlessly; supported Python/kernel versions are locked; dimension queries recover the known block.
- [ ] M1 — Build one deterministic fixture. Evidence: Two valid solids and hand-checked nominal dimensions; cleanly reject impossible input.
- [ ] M2 — Build independent geometry checks. Evidence: Every invalid case fails for the expected reason; no oracle calls geometry-builder dimension helpers.
- [ ] M3 — Add constrained generation and report. Evidence: Rejected candidate and corrected geometry are visible; assumptions and geometric limits are prominent.
- [ ] M4 — Prepare the portfolio release. Evidence: A fresh environment builds examples and validates exports. A physical fit check remains explicitly optional.

Update this file only after checking the milestone evidence. See IMPLEMENTATION_PLAN.md for dependencies and estimates.
