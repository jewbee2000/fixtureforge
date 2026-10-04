# Implementation tasks

All tasks are unstarted. Check off only after recording executed evidence.

- [ ] M0 — Compare CADCLAW and prove the CAD stack. Gate: A concrete missing access check justifies the extension; simple independent solids validate the chosen kernel and swept-envelope construction.
- [ ] M1 — Check imported geometry and generate one fixture. Gate: The external example does not call the generator; the clamp has two valid solids and independently measured dimensions.
- [ ] M2 — Verify clearance and independent geometry. Gate: Every invalid case fails for its intended reason; unsupported motion never passes as clear.
- [ ] M3 — Make reports useful for design review. Gate: An engineer can identify which tool path is blocked from the report and reproduce the check on imported STEP.
- [ ] M4 — Verify adoption and prepare the local release. Gate: All applicable Must checks pass; CAD evidence is clearly separate from physical printing or strength validation.

- [ ] Record dispositions for every Should/Could item and verify Won't claims remain excluded.
- [ ] Complete the independent consumer walkthrough and compare its cost with the baseline.

See IMPLEMENTATION_PLAN.md and docs/REQUIREMENTS.md.
