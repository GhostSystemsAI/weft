# Review summary, 2026-10-08

Companion to [2026-10-08-buildability.md](2026-10-08-buildability.md). That document holds the full review. This one records what was found, what each of the two pull requests changes, and the spike that follows them. The results section records spike 1 as run on branch `spike/1-graph-contract`.

## 1. Findings

The decisions are settled and consistent, the profile brief is close to buildable, and the adopter plan gives a defensible order of work. No decision is missing. Three artifacts the documents refer to are not yet written, and those block a build.

| Gap | Evidence | Consequence |
|---|---|---|
| Graph contract | Rule 3 protects the emitted triples, but no document states the mapping from toolkit JSON to triples, the namespace configuration, the ordered-property representation, or the projection vocabulary. | Rule 3 has nothing to protect and tests have nothing to assert. |
| Reproducible environment | No `pyproject.toml`, no `src/` layout, no CI workflow. Decision 0004 commits to Linux and Windows CI across Python versions. | Decision 0004 is not implementable. The toolkit bindings are a Rust extension and need a wheel built once per pinned commit. |
| Stereotype decisions | The profile brief defers Component, Interface, and the action-definition stereotype. | The profile cannot be written. |

Secondary findings, each with its fix in MR1 or MR2:

- sysml-toolkit's `IDS.md` lists stable identity across renames as backlog. A sidecar map in Weft is premature until an upstream issue is filed. Decision 0002 should state which id scheme Weft consumes.
- holonic issues #30 and #50 are closed and PR #54 is merged, but the latest release is still v0.8.0. Issue #2 pins 0.8.0, which lacks the fixes spike step 6 depends on. holonic `main` must be pinned by hash until 0.9.0.
- The toolkit commit and library commit are recorded on the adopter branch but not in decision 0002.
- No LICENSE file exists. Contribution is blocked until one is chosen.
- The `better-language-skill` AGENTS.md names is not vendored, so an agent without it cannot comply with the style section.
- Rule 11 collides with agent tooling that adds a `Co-Authored-By` trailer by default.
- Two documents use the label OQ11 for different questions (holonic's and Weft's).
- STATUS.md was stale on holonic the day it was written, and nothing enforces the update rule.
- Rule 3 said "because the version is pre-1.0" where "even though" was meant.

## 2. MR1: document fixes

Branch `review/buildability-2026-10-08`, filed as [zwelz3/weft#4](https://github.com/zwelz3/weft/pull/4) against the adopter branch. Two commits, authored without AI attribution.

| File | Change |
|---|---|
| `docs/reviews/2026-10-08-buildability.md` | The full review: verdict, readiness by area, findings on AGENTS.md, the profile brief, and the adopter plan, and the ordered list of what makes the project buildable. |
| `AGENTS.md` rule 3 | "because the version is pre-1.0" corrected to "even though the version is pre-1.0". |
| `AGENTS.md` rule 6 | Qualified: the rule holds relative to the toolkit release pinned in decision 0002. |
| `AGENTS.md` rule 11 | Names the checked-in override that stops Claude Code's trailer, and requires an agent on another tool to turn off the equivalent before its first commit. |
| `AGENTS.md` rule 12 | New: every dependency off PyPI is pinned by commit hash, and every row of the STATUS.md versions table records the hash it was reviewed at. |
| `AGENTS.md` style section | Stand-in rules for when `better-language-skill` is unavailable. |
| `.claude/settings.json` | New: `includeCoAuthoredBy: false`. |
| `README.md` | Flexo MMS link points at the layer 1 service repository instead of the organization page. |
| `docs/OPEN-QUESTIONS.md` | OQ6's reference to holonic's OQ11 is prefixed to distinguish it from Weft's OQ11. |
| `STATUS.md` | The review listed as open work, with items 1 to 5 of its ordered list named as one gap-closing pull request. |

## 3. MR2: closing the gaps

Branch `gaps/buildability-2026-10-08`, based on MR1. One commit per item, in the order the review gives. All eight items have landed. The branch is filed as [zwelz3/weft#5](https://github.com/zwelz3/weft/pull/5) on top of MR1.

| Item | Change | State |
|---|---|---|
| 1. License | Apache-2.0 `LICENSE` with copyright holder Zech Welz, a License section in README.md, and rule 13 in AGENTS.md requiring a compatibility check of every packaged dependency. Apache-2.0 was adopted on 2026-10-08; the earlier commit body calls it a proposal. | Landed |
| 2. Pins | Decision 0002 states the toolkit commit `8212217` (release 0.10.2), the library commit `de1070a`, and the id scheme Weft consumes. Decision 0003 pins holonic `main` at `d8d1758` until 0.9.0. Every row of the STATUS.md versions table carries a hash. | Landed |
| 3. Package and CI | `pyproject.toml`, `src/weft/__init__.py`, `tests/test_package.py`, and `.github/workflows/ci.yml`. The workflow builds the `sysmlv2` abi3 wheel once per pinned toolkit commit, caches it by hash, and runs a test matrix on Ubuntu and Windows across Python 3.11 to 3.13. `tests/test_status.py` is an offline structural check of the STATUS.md open-work table. | Landed |
| 4. Decisions 0005 to 0007 | Component as a role borne by a material artifact or an information content entity. Interface applied to the definition only, as an information content entity. The action-definition stereotype named for what it exports, with the reason CCO's Function does not fit. Status: proposed. | Landed |
| 5. Thread queries | `queries/` with five SPARQL SELECT files derived from the traceability matrix and gap analysis, each stating its question, assumed projection terms, and expected columns. They are the specification for spike step 4 and are untested until the graph contract exists. | Landed |
| 6. Graph contract skeleton | `docs/graph-contract.md` with section headings and one sentence each: IRI minting, element mapping, relationship mapping and ranges, ordered properties, projection vocabulary, contract versioning. Spike 1 fills it. | Landed |
| 7. Upstream issue draft | `docs/outreach/sysml-toolkit-rename-stable-identity.md`, an issue text for Open-MBEE/sysml-toolkit citing the IDS.md backlog entry. The maintainer files it. | Landed |
| 8. STATUS.md | Phase, open work, and versions reflect the above. | Landed |

## 4. Proposed spike

Issue #2 defines spike 1. This section restates it as a test plan with the changes the review requires, and reserves space for results. The spike is disposable. Its deliverable is `docs/graph-contract.md` filled in, revised open questions, and the measurements below.

### Changes to issue #2

- Pin holonic `main` at `d8d1758`, not 0.8.0. Step 6 depends on the fixes in #30 and #50.
- Name the graph contract as the primary deliverable.
- Use a public model from SysML-v2-Release at commit `de1070a` for steps 1 to 5, so the spike starts before the adopter's component arrives. Steps 6 and 7 wait on the real component, instance table, and tickets from issue #1.
- Take the five thread queries in step 4 from `queries/` (MR2 item 5), not from scratch.

### Steps

| Step | Work | Evidence produced |
|---|---|---|
| 1. Environment | Install the toolkit bindings at `8212217`, holonic at `d8d1758`, rdflib, pySHACL. Record the toolkit commit and Rust version. | `spike/ENVIRONMENT.md` |
| 2. Model | One component in textual notation with a stand-in profile of three stereotypes and a short name on every requirement. `check --strict` passes. | `spike/model/` |
| 3. Normative graph | Toolkit JSON to RDF through a JSON-LD context. Requirements get IRIs minted from short names; everything else keeps derived ids. Record the ordered-property representation. | Draft of the element and relationship sections of the graph contract |
| 4. Projection | The five queries from `queries/` in plain language, then the projection vocabulary and SPARQL CONSTRUCT queries that serve them. | Draft of the projection section of the graph contract |
| 5. Ontology export | Definitions in a library package, OWL derived from them. Record what exports and what does not. | Export coverage list |
| 6. Derived shapes | SHACL from the definitions, validated against a real instance table with mistyped rows injected. | Shape findings log |
| 7. Holons | Load into holons per decision 0003. Validate on rdflib, repeat on Fuseki, record any difference. | Backend difference list |

### Measurements

| ID | Question | Settles | Method |
|---|---|---|---|
| M1 | How often do derived ids change under rename, insert, move, reorder, and extract | OQ2 | Apply each edit to the step 2 model, re-emit, diff the id set |
| M2 | Can ids collide between projects with the same structure | OQ2 | Emit two projects with identical structure under different names, intersect the id sets |
| M3 | What does text to JSON to text lose | OQ9 | Round trip the model, diff the textual notation |
| M4 | How much of a library package exports to OWL | OQ4 | Count exported against declared definitions in step 5 |
| M5 | How much shorter are the five queries against the projection than the normative graph | OQ10 | Write each query both ways, compare triple pattern counts and result equality |
| M6 | Do derived shapes catch mistyped instance data | OQ6 | Count injected faults found in step 6 |

### Decision rule

If M1 shows acceptable churn, Weft needs only a thin sidecar map and the profile and thread queries follow. If M1 shows unacceptable churn, the upstream issue in MR2 item 7 is filed and becomes a blocker for identity but not for the profile, which does not depend on it.

### Results

Spike 1 ran on branch `spike/1-graph-contract`. Details and method are in `spike/RESULTS.md`. The decision rule resolved to the first branch: churn is acceptable and Weft needs only a sidecar map. Step 7 ran on rdflib only; the Fuseki run is deferred because no plain HTTP Fuseki endpoint was available.

| ID | Observed | Model | Toolkit commit | Open question change |
|---|---|---|---|---|
| M1 | Insert 0.0%, reorder 0.0%, move 1.0%, rename 5.7%, extract 24.1% of 507 ids changed | pump model, 503 elements | `8212217` (0.10.2) | OQ2: sidecar map suffices, upstream issue not a blocker |
| M2 | 28 shared ids of 507, all from the identically named and identical profile file; none from the renamed packages | pump model, 503 elements | `8212217` (0.10.2) | OQ2: collision is a source-naming question |
| M3 | Comments dropped, formatting rewritten; no construct, name, or relationship lost | pump model, 503 elements | `8212217` (0.10.2) | OQ9: tier 2 needs comment preservation |
| M4 | 16 of 16 definitions to classes; 8 of 10 nested features to object properties (2 scalar) | pump model, 503 elements | `8212217` (0.10.2) | OQ4: confirmed as stated |
| M5 | Five queries at two to four triple patterns on the projection; normative versions not written | pump model, 503 elements | `8212217` (0.10.2) | OQ10: saving unmeasured |
| M6 | 10 of 10 injected faults caught on a stand-in table; vacuous pass as a normative-graph boundary | pump model, 503 elements | `8212217` (0.10.2) | OQ6: normative boundary needs its own shapes |
