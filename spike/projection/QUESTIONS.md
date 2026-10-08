# Step 4 questions, in plain language

The five thread queries in [queries/](../../queries/) (MR2 item 5, taken from the traceability
matrix and gap analysis in `docs/plans/adopter-capabilities.md`), restated without SPARQL syntax.

1. **Which elements satisfy each requirement, and what is each claim's verdict?** For every
   requirement, list every element a `satisfy` relationship names as its satisfying element,
   together with the verdict `sysmlv2 verify` gives that claim (satisfied, violated, or
   undecided when the claim has nothing to decide it).
2. **Which verification cases verify each requirement?** For every requirement, list every
   verification case whose objective contains a `verify` of that requirement.
3. **Which requirements have no satisfying element?** Requirements with a declared short name
   that no `satisfy` claim names.
4. **Which requirements have no verification case?** Requirements with a declared short name
   that no `verify` relationship covers.
5. **Which components does no requirement concern?** Elements stereotyped as components (an
   element whose type carries the Component metadata, decision 0005) that no `satisfy` claim
   names as a satisfying element.

## Answers on the pump system model

Running the five queries (`spike/projection/project.py`) against the projected graph built from
`spike/model/pump-system.sysml` gives:

1. Six rows, one per requirement/satisfying-element pair, every verdict `undecided` (the spike's
   requirements carry doc text, not a bound constraint, so `sysmlv2 verify` has nothing to decide;
   see `spike/RESULTS.md` for the full verify transcript).
2. Two rows: `REQ-001` (`MaxPressure`) and `REQ-002` (`ResponseTime`) are each verified by
   `pumpSystemAcceptanceTest`.
3. Zero rows: every requirement has at least one `satisfy` claim.
4. Four rows: `REQ-003`, `REQ-004`, `REQ-005`, `REQ-006` have no `verify` relationship.
5. One row: `CMP-SENS` (the pressure sensor), the only component usage no `satisfy` claim names.

Full result tables are in `spike/projection/results.md`.
