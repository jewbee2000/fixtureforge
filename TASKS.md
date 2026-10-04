# Implementation tasks

Implementation is in progress. Check off only after recording executed evidence.

- [x] M0 — Compare CADCLAW and prove the CAD stack. Executed baseline and input checks; see docs/BASELINE.md and evidence/baseline.json.
- [x] M1 — Imported build123d bracket and 24 mm fixture pass independent STEP dimensions and STL checks.
- [x] M2 — Six references pass; eight seeded defects fail intended requirements. Schemas, CLI and full sweep checks executed.
- [x] M3 — REPLAY rejection/repair works, named obstruction pairs and projected path bounds exported. Browser layout review is explicitly unverified.
- [x] M4 — 61 acceptance cases passed; fresh wheel consumer, semantic repeat, limits, lint/types and measured performance passed. See evidence/requirements-evidence.json. Physical and practitioner validation remain unverified.

- [x] FF-16 selected: margins and declared occupancy tested. FF-17 revision diff deferred. FF-18 model proposals deferred; FF-10 generated-code execution not applicable. Won't features remain excluded.
- [x] Complete the independent consumer walkthrough and compare its cost with the baseline. See docs/CONSUMER.md; this was agent-executed, not practitioner adoption.

See IMPLEMENTATION_PLAN.md and docs/REQUIREMENTS.md.

## Proposed next iteration

- [ ] Obtain one independent practitioner walkthrough on their own assembly.
- [ ] Verify passing/failing HTML reports at desktop and mobile widths.
- [ ] Add fresh Windows/Python 3.12 CI using the existing local checks.
- [ ] Select FF-17 revision comparison if the consumer workflow supports it.
- [ ] Optionally print and measure one reference fixture using existing equipment.

These are proposed follow-up work, not incomplete Must requirements for the
deterministic release. See docs/NEXT_STEPS.md. Blog publication remains pending.
