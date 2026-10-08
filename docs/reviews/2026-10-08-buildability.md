# Buildability review, 2026-10-08

Review of the design documents on `main` and on the branch that adds the adopter capabilities plan, against the question: how far are these specifications from something a contributor or an agent can start building? Facts about dependencies were checked against GitHub on 2026-10-08 and are dated where they matter.

## Verdict

The decisions are settled and consistent, the profile brief is close to buildable, and the adopter plan gives a defensible order of work. What stops a build from starting is not a missing decision. It is three artifacts that the documents refer to but do not yet contain: the graph contract that AGENTS.md rule 3 protects, a pinned and reproducible environment, and the three stereotype decisions the profile brief defers. With those written, spike 1 and the profile can start the same day.

## Readiness by area

| Area | State | What blocks a build |
|---|---|---|
| Decisions 0001 to 0004 | Buildable. Each has context, decision, consequences, alternatives. | Nothing. 0002 should name the commit it pins (see below). |
| Profile (`docs/plans/profile-brief.md`) | Close. Deliverable paths, inputs, acceptance criteria, and tests are stated. | Three stereotype decisions (Component, Interface, Function). Confirmation of the standard library's metadata facilities at the pinned library commit. The example component from issue #1, or a public stand-in named now. |
| Graph contract (normative graph, projection, IRIs) | Not written. Rule 3 declares the emitted triples a migration surface, OQ2 states an IRI leaning, and spike step 3 says "through a JSON-LD context", but no document states the mapping from toolkit JSON to triples, the namespace configuration, or the projection vocabulary. | A `docs/graph-contract.md` (or equivalent) that fixes IRI minting, the element and relationship mapping, the ordered-property representation, and the projection terms, so that rule 3 has something to protect and tests have something to assert. Spike 1 produces the evidence for it; the contract is the spike's deliverable. |
| Element identity (OQ2) | Leaning only. | Verified 2026-10-08: sysml-toolkit's `IDS.md` lists "stable identity across renames" as backlog and defers it "pending an identity-lifecycle design". File the upstream issue before building a sidecar map. Decision 0002 should also state which id scheme Weft consumes (IDS.md: legacy lowering is scheme 2, canonical lowering is scheme 3, opt-in). |
| holonic integration (0003) | Blocked on a release. | Verified 2026-10-08: holonic issues #30 and #50 are closed, PR #54 merged, PR #56 still open, latest release still v0.8.0 (2026-08-12). The spike needs `main` pinned by hash until 0.9.0 ships. Issue #2 still says holonic 0.8.0; that pin lacks the fixes step 6 depends on. |
| sysml-toolkit (0002) | Pinned on the branch, not in the decision. | The branch records commit `8212217…` and library commit `de1070a…`; move both pins into decision 0002 and into the environment definition. The repository layout (`crates/sysmlv2-py`, maturin) confirms the Python bindings exist and are built from source. |
| Package and CI | Absent. | No `pyproject.toml`, no `src/` layout, no CI workflow, although decision 0004 commits to Linux and Windows CI across Python versions. The toolkit bindings are a Rust extension; build abi3 wheels once per pinned commit in one job and cache them, or Windows CI will be slow and fragile. |
| Reports (C4) | Plan level. | The traceability matrix and gap analysis are defined as query sets but no query is written. The adopter plan's proposal to take spike step 4's five queries from these reports is the right fix; write those five now. |
| Agent tool surface (C1) | Idea level. | A command list exists (check, lint, describe, list members, transform, render). Nothing states the input and output of each or how the repair loop terminates. Lowest priority per the plan's own ordering. |
| Kotar round trip (C2, OQ11) | Unverified. | Three properties to verify with one graphically edited model. Nothing to build until then. |
| Repository hygiene | Gaps. | No LICENSE file (dependencies are Apache-2.0 and MIT; the repository blocks contribution until a license is chosen). The `better-language-skill` AGENTS.md names is not vendored or described, so an agent without it cannot comply. |

## Findings on AGENTS.md

- Rule 3 said "because the version is pre-1.0" where "even though" was meant. Fixed in this change.
- Rule 11 collides with default agent tooling, which adds a `Co-Authored-By` trailer unless overridden per project. Add one sentence naming where the override lives for each tool that is used on the repository.
- Add a pinning invariant: every dependency not on PyPI is pinned by commit hash in the repository, and every "Versions reviewed" row carries one.
- Add a license invariant once a LICENSE file exists.
- Rule 6 is an invariant only relative to the pinned toolkit release, since which well-formedness constraints the toolkit implements changes per release. Say so.
- The STATUS-update rule has no enforcement. STATUS.md on `main` was stale on holonic the day it was written. A CI check that fails when an open-work row links an issue whose state no longer matches would catch this.
- The claim that Claude Code reads AGENTS.md when no CLAUDE.md exists (v2.1.277 or later) is unverified here. Keep it, mark the source.

## Findings on the profile brief

- Treat Component as a role borne by either a material artifact or an information content entity. This removes the hardware-versus-software fork from the stereotype and moves it to the bearer.
- Apply Interface to the definition only, as an information content entity, and leave the realized connection to instance data.
- Do not name the action-def stereotype Function. CCO's Function is a disposition, while an action's instances are processes. Name it for what it exports.
- Two different OQ11s exist in the documents: OQ6 cites holonic's OQ11 and the branch introduces Weft's own OQ11. Prefix cross-project references (`holonic OQ11`).

## Findings on the adopter plan

- The link-type table is the strongest part of the branch. It is concrete, each row names a standard library construct, and the toolkit probe confirms every row passes `check --strict`. It can go straight into the profile as the requirement stereotype's specification.
- The maturity query registry is buildable as described (one file per query, a test that runs each against the corpus). It depends on the projection, which depends on the graph contract above.
- OQ13's open point (commit synchronized issue state or keep it as an artifact) has a safe default: artifact, with the synchronization time in the holon's context graph, as the plan already proposes. Decide it and remove the fork.

## What makes it buildable, in order

1. Choose a license and add the file. Vendor or inline the style rules.
2. Move the toolkit and library pins into decision 0002, with the id scheme consumed. Pin holonic `main` by hash in issue #2 and STATUS.md until 0.9.0.
3. Add `pyproject.toml`, a `src/weft` package, and one CI workflow that builds the toolkit wheel once and caches it. Decision 0004 is not implementable without this.
4. Record decisions 0005 to 0007 for Component, Interface, and the action-def stereotype, using the framings above or better ones.
5. Write the five thread queries from the traceability matrix and gap analysis. They are the specification for spike step 4 and for the projection.
6. Run spike 1 against a public model from SysML-v2-Release at the pinned commit. Its deliverable is `docs/graph-contract.md`, not code.
7. File the upstream sysml-toolkit issue on rename-stable identity, citing the IDS.md backlog entry, before any sidecar-map code.
8. Update STATUS.md with a CI check that keeps it honest.
