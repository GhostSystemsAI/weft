# Adopter capabilities

The initial adopter needs four capabilities from Weft. This plan maps each one onto the accepted decisions, the open questions, and the dependencies Weft builds on, states what is missing, and orders the work. It adds no decision; where a capability needs one, the question is listed under "Questions for the adopter" or added to [OPEN-QUESTIONS.md](../OPEN-QUESTIONS.md).

| ID | Capability |
|---|---|
| C1 | People use an LLM agent to build and edit the SysML v2 model. |
| C2 | People view and interact with the model in SysML tools, for visualization and editing. |
| C3 | Requirements are captured from source documents, decomposed, and linked (satisfy, derive, refine, verify, trace) to model elements and to issues in Jira, GitLab, and similar systems. |
| C4 | Weft generates reports, including a requirements traceability matrix, a gap analysis, and an architecture maturity report. |

## Coverage

| Capability | Covered by the design today | Missing |
|---|---|---|
| C1 | The intended workflow in the README and AGENTS.md rule 2 (prompts are not records). sysml-toolkit reports `check` and `lint` findings as JSON, edits text through span-anchored transformations that keep formatting, and runs a language server (decision 0002). | The agent's tool surface, the repair loop, and extraction of requirements from documents. Spike 1 excludes LLM generation. |
| C2 | sysml-toolkit renders seven PlantUML views (structure tree, interconnection, state, action, sequence, use case, mixed) and ships a language server with a VS Code client. The Flexo mirror (tier 1, decision 0001) exposes the standard SysML v2 API that other tools read. | Which tools the adopter uses. Graphical editing in a tool that keeps its own store is tier 2 in decision 0001, which is not planned. |
| C3 | Declared short names on linked elements (OQ2). The profile's trace metadata with OSLC properties, resolved to IRIs through a per-project key configuration (profile brief). Adapter sources as holons joined by portals (decision 0003). | A link from a requirement to the document passage it came from. The mapping from the adopter's link types to SysML v2 constructs. How issue state (status, assignee, resolution) reaches Weft. |
| C4 | Nothing in Weft. specl computes a maturity score from SHACL findings weighted by priority and records each assessment as a `prov:Activity`, and has no traceability matrix or coverage report. sysml-toolkit's `verify` decides each `satisfy` claim as satisfied, violated, or undecided. | Every report. |

## C1. Agent-assisted modeling

The toolkit already provides what an agent's repair loop needs (the agent writes textual notation, `sysmlv2 check --strict --format json` and `sysmlv2 lint --format json` return findings with source spans, and the agent revises until both pass). Edits to an existing model go through the transformation API (`rename`, `insert_member`, `remove`, `extract_definition`), which re-resolves references after each commit and leaves untouched text byte-identical, so a review diff shows only the intended change.

Two parts are Weft's own work. The first is the tool surface given to the agent, which is a set of commands (check, lint, describe an element, list members, apply a transformation, render a view) exposed as a CLI and, for agents that use the Model Context Protocol, as an MCP server. The second is requirement extraction (C3), where the agent reads a source document and proposes requirement elements; the proposal is reviewed as a pull request like any other model change.

The reasons behind a modeling choice go into decision records (AGENTS.md rule 2). The standard library's `ModelingMetadata::Rationale` annotates an element with text and an optional reference to an explanation element, and is a candidate carrier for the link from an element to its decision record; the profile work decides between it and a feature of Weft's trace metadata.

## C2. Visualization and editing in SysML tools

Three paths are available, and only the third conflicts with decision 0001.

| Path | Tier | What it gives | What it requires |
|---|---|---|---|
| Text editor with the toolkit's language server, and PlantUML views rendered in CI | 0 | Diagnostics, navigation, completion, and refactorings while editing; diagrams as build artifacts linked from the pull request | Nothing beyond the toolkit and a PlantUML renderer |
| A SysML v2 tool reads the Flexo mirror through the standard API | 1 | Visualization and querying in any tool that implements the SysML v2 API client | Flexo MMS and the mirror step |
| A graphical editor writes changes back | 2 | Graphical editing | A path from the tool's edits to a pull request against the textual notation, which depends on JSON-to-text conversion (OQ9) |

Read-only use of graphical tools fits decision 0001. Graphical editing does not, because decision 0001 marks tier 2 as not planned. If the adopter needs graphical editing, tier 2 moves into scope, OQ9 moves onto the critical path, and the edit path has to be designed so that git remains where changes are reviewed. Open question OQ11 records this.

Whether a given graphical tool can import textual notation directly, which would give a tier 0 path for viewing, is not verified for any tool.

## C3. Requirements capture, decomposition, and linking

### Link types

SysML v2 expresses most of the requirement relationships the adopter names with its own constructs, so the profile adds metadata only where the language has none.

| Adopter's link | SysML v2 construct | Notes |
|---|---|---|
| Decomposition | A requirement usage nested in another, or `require` of a requirement inside another | Composition. The parent is satisfied when its composed requirements are. |
| Derive | A connection typed by `RequirementDerivation::Derivation` (`#derivation connection { end #original ::> a; end #derive ::> b; }`) | Standard library package `Requirement Derivation`. |
| Refine | A dependency annotated with `ModelingMetadata::Refinement` (`#refinement dependency a to b;`) | Standard library package `Metadata`. |
| Satisfy | `satisfy R by x;` | sysml-toolkit's `verify` decides the claim when the constraint's inputs are bound. |
| Verify | `verify R;` inside the objective of a `verification def` or `verification` usage | The verification case is a model element; the test that implements it is external. |
| Trace | `dependency a to b;` | SysML v2 has no trace keyword. A generic dependency carries no meaning beyond "related", so the profile may define a metadata kind for it. |
| Tracked by, implemented by, validated by (an issue, a commit, a test) | The profile's trace metadata, one feature per OSLC property | Keys resolve to IRIs through the per-project configuration (profile brief). |
| Source passage | Not yet designed | OQ12. |

### Source passages

A requirement extracted from a document needs a link to the passage it came from, so that a reviewer can check the extraction and a later revision of the document can be compared against the requirements derived from it. The profile brief's trace metadata covers issues, commits, and tests and has no feature for a source. The link's range and its target's identity are open (OQ12): a document IRI with a fragment identifier, a `dct:source`, or a `prov:wasDerivedFrom` from the requirement to a passage resource each fix a different property range, and the choice is a graph-contract decision (AGENTS.md rule 3).

### Issue systems

The profile brief stores issue keys in the model and resolves them to IRIs. That is enough for a traceability matrix that lists keys. A report that shows an issue's status, or a gap analysis that finds requirements whose issues are closed while the requirement is unverified, needs the issue's state, which lives in Jira or GitLab. Under decision 0001 the core works without a server, and under AGENTS.md rule 9 validation fetches nothing; neither forbids a separate synchronization step. The leaning recorded in OQ13 is an adapter per issue system that runs as its own step (in CI or on demand), writes the issue state as a source holon, and is never called during validation or report generation. Reports then run on the last synchronized state and state its timestamp.

Creating issues from requirements (the reverse direction) is a separate feature, and whether the adopter needs it is listed under "Questions for the adopter".

## C4. Reports

Each report is a set of SPARQL queries over the projection and the adapter holons, rendered by a command that runs on a git checkout (tier 0).

| Report | Content |
|---|---|
| Requirements traceability matrix | One row per requirement: short name, text, parent, derived requirements, satisfying elements and the `verify` verdict for each claim, verification cases, issues, commits, tests, and source passage |
| Gap analysis | Requirements with no satisfying element, no verification, or no issue; elements stereotyped as components that no requirement concerns; derived requirements with no original; issue keys in the model that resolve to no synchronized issue; `satisfy` claims that `verify` reports as violated |
| Architecture maturity | Counts of `ModelingMetadata::StatusInfo` values (TBD, TBR, TBC, done, closed), `check`, `lint`, and SHACL findings weighted by severity as specl weights them, coverage fractions from the gap analysis, and the history of each measure across tagged versions |

"Architecture maturity" has no agreed definition yet, and the measure above is a starting point for the adopter to revise.

Spike 1 (issue #2, step 4) writes five thread queries before defining the projection. Taking those five queries from the traceability matrix and the gap analysis makes the spike measure the projection against the queries the adopter will run.

## Evidence from a probe of sysml-toolkit

A probe model was checked with sysml-toolkit 0.10.2 at commit `821221767c3c56cb1ebe7da22666197a47c9c645`, built from source with Rust 1.97 in under three minutes, against the standard library from SysML-v2-Release at commit `de1070ae8e79c21532b8004fc663d47b35d0e9fa`. The model declared requirements with short names, a stand-in trace metadata definition with string features, a `#derivation` connection, a `#refinement` dependency, a plain `dependency`, two `satisfy` claims, a `verify` inside a verification case objective, `StatusInfo`, and `Rationale`. The results bear on C2 to C4.

| Observation | Bears on |
|---|---|
| `sysmlv2 check --strict` passes on every construct in the link-type table above. | C3 |
| Declared short names appear as `declaredShortName` in compact JSON, so the derivation can mint IRIs from them as OQ2 proposes. | C3 |
| Metadata values do not appear on the `MetadataUsage` element; they are reached through its owned feature values and literals, so the derivation step walks those relationships to read a trace key. | C3 |
| `sysmlv2 verify` reported a `satisfy` claim with a bound mass under its limit as satisfied, and one over the limit as violated with the deciding values, and exited with status 1 when a claim was violated. The verdicts can feed the gap analysis, and the exit status can gate CI. | C4 |
| None of the seven PlantUML views is a requirements diagram that draws derive, satisfy, and verify edges between requirements and the elements that satisfy or verify them. The toolkit's structured graph output, intended for a native renderer, carries `satisfy` and `verify` edge kinds that a Weft view could render. | C2 |

## Order of work

| Step | Work | Depends on | Delivers to the adopter |
|---|---|---|---|
| 1 | Spike 1, with the step 4 queries taken from C4 | Nothing; issue #1 data improves steps 6 and 7 | Evidence for OQ2, OQ4, OQ6, OQ9, and OQ10 |
| 2 | Profile, starting with the requirement stereotype, the trace metadata, and the source passage link | Step 1, OQ12 | The authoring syntax for C3 |
| 3 | Derivation of the normative graph and the projection | Steps 1 and 2 | The graphs C4 queries |
| 4 | Traceability matrix and gap analysis at tier 0 | Step 3 | The first C4 reports, from a git checkout |
| 5 | Agent tool surface and requirement extraction | Step 2 | C1, and the capture half of C3 |
| 6 | Issue adapters for Jira and GitLab | Step 3, OQ13 | Issue state in the C4 reports |
| 7 | Architecture maturity report | Steps 4 and 6, and the adopter's definition | C4 complete |
| 8 | Tool interoperability: PlantUML views in CI, then the Flexo mirror | Step 3 for views, OQ2 for the mirror | C2 |

Reports come before the agent surface because the reports define what the projection must answer, and an agent that writes a model before the profile exists produces text that a later profile change invalidates.

## Questions for the adopter

1. Which SysML tools are used for visualization, and does "editing" mean graphical editing in such a tool? A yes moves tier 2 into scope (OQ11).
2. Which issue systems hold the work (Jira Cloud, Jira Data Center, GitLab), and should Weft create issues from requirements or only record keys that people enter?
3. In which formats do source documents arrive (Word, PDF, ReqIF exported from a requirements tool, spreadsheets)?
4. Which link types are in use today, and which of them does the adopter's process treat as distinct (in particular trace and refine)?
5. What does the adopter mean by architecture maturity, and in which format are reports delivered (HTML, a spreadsheet, a document)?
