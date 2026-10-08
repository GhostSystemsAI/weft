# Status

State of the project as of 2026-10-08. The session that changes the project's state updates this file before it ends; [AGENTS.md](AGENTS.md) holds the rules that do not change from session to session.

## Phase

Design. The repository holds decision records, open questions, plans for the profile and for the adopter's capabilities, and no code.

## Settled

| Decision | Content |
|---|---|
| [0001](docs/decisions/0001-git-is-the-record.md) | SysML v2 textual notation in git is the record. Flexo MMS is an optional one-way mirror (tier 1), and every core feature works at tier 0 without a server. |
| [0002](docs/decisions/0002-sysml-toolkit-for-parsing-and-checking.md) | sysml-toolkit parses, checks, and converts to and from SysML v2 API JSON. |
| [0003](docs/decisions/0003-holonic-for-graph-organization.md) | holonic organizes the derived graphs, one holon per model version. |
| [0004](docs/decisions/0004-python.md) | Python, 3.11 or later. |

## Proposed

| Decision | Content |
|---|---|
| [0005](docs/decisions/0005-component-stereotype.md) | Component is a role. A required `bearer` feature records whether a material artifact bears it or an information content entity's concretization does. |
| [0006](docs/decisions/0006-interface-stereotype.md) | Interface applies to `interface def` and `port def` only, as a directive information content entity. Realized connections are instance data. |
| [0007](docs/decisions/0007-action-definition-stereotype.md) | The `action def` stereotype is named Process and aligns to BFO process, because CCO's Function is a disposition. |

## Open work

| Item | Location | State | Next action |
|---|---|---|---|
| Adopter capabilities | [docs/plans/adopter-capabilities.md](docs/plans/adopter-capabilities.md) | Drafted; four of five questions answered | Verify the three Kotar points under OQ11 with a model edited in Kotar. Decide in the profile work whether a user story is a use case or a requirement with a stakeholder |
| Buildability review | [docs/reviews/2026-10-08-buildability.md](docs/reviews/2026-10-08-buildability.md) | Filed as a pull request | Work the ordered list at the end of the review. Items 1 to 5 (license, pins, package and CI, stereotype decisions, thread queries) are one gap-closing pull request; spike 1 follows it |
| Data for the spike | [zwelz3/weft#1](https://github.com/zwelz3/weft/issues/1) | Requested | The maintainer supplies a component, an instance table, trace data, and an adapter ontology excerpt |
| Spike 1 | [zwelz3/weft#2](https://github.com/zwelz3/weft/issues/2) | Not started | Steps 1 to 5 and measurements M1 to M4 can start on a public example before #1 is answered. The adopter capabilities plan proposes taking the step 4 queries from the traceability matrix and gap analysis |
| Profile | [docs/plans/profile-brief.md](docs/plans/profile-brief.md) | Stereotype decisions proposed in 0005 to 0007 | The maintainer accepts or revises 0005 to 0007. Then rename the Function row in the brief to Process and start the requirement stereotype |
| Report to Flexo maintainers | [docs/outreach/flexo-sysmlv2-rdf.md](docs/outreach/flexo-sysmlv2-rdf.md) | Drafted and reviewed, not filed | The maintainer files it on Open-MBEE/flexo-mms-sysmlv2 |
| holonic enhancements | [#51](https://github.com/zwelz3/holonic/issues/51), [#52](https://github.com/zwelz3/holonic/issues/52), [#53](https://github.com/zwelz3/holonic/issues/53) | #30 and #50 merged to holonic `main` in [zwelz3/holonic#54](https://github.com/zwelz3/holonic/pull/54), not yet released. Two defects found during that work are in [zwelz3/holonic#56](https://github.com/zwelz3/holonic/pull/56), which replaces #55 (merged into the feature branch after #54, so it missed `main`) | Merge #56. Until holonic 0.9.0 is released, Weft's spike depends on holonic `main`. #52 after spike step 7, which supplies its two-version fixture. #51 and #53 deferred: the adopter needs no cross-source identity yet, and Kotar works against git rather than Flexo |

The design questions behind this work are in [docs/OPEN-QUESTIONS.md](docs/OPEN-QUESTIONS.md) (OQ1 to OQ13).

## Versions reviewed

| Project | Version | How it was reviewed |
|---|---|---|
| [sysml-toolkit](https://github.com/Open-MBEE/sysml-toolkit) | 0.10.2, pinned at `821221767c3c56cb1ebe7da22666197a47c9c645` with SysML-v2-Release at `de1070ae8e79c21532b8004fc663d47b35d0e9fa` (decision 0002) | First from a source archive of `main` with no commit hash recorded, then from a clone at `821221767c3c56cb1ebe7da22666197a47c9c645`, built with Rust 1.97 and run against SysML-v2-Release `de1070ae8e79c21532b8004fc663d47b35d0e9fa` (fetched with `git submodule update --init spec-refs/SysML-v2-Release`). The probe's results are in [docs/plans/adopter-capabilities.md](docs/plans/adopter-capabilities.md). |
| [flexo-mms-sysmlv2](https://github.com/Open-MBEE/flexo-mms-sysmlv2) | Commit `61d1c9da77e1f0eebd4734290b8bb04fb04162f0` | Clone |
| [holonic](https://github.com/zwelz3/holonic) | `main`, reviewed at `d8d1758752827c35fc6781e89e01557b6e5e1825` after the 0.8.0 release; pinned at `25d1c841936ff96ab0adbb644e076939f44829dd`, the merge of #54 (decision 0003) | Clone and source archive |
| [OpenSysML](https://github.com/Open-MBEE/OpenSysML) | Documentation only; `main` was at `a5bd7eb7d8462ff1308cfab7b1046f58245e3d53` on 2026-10-08 | README on pkg.go.dev, which is not tied to a commit; opensysml.org was unreachable from the session that reviewed it |

## Findings that are easy to rediscover

- The toolkit's Python package is named `sysmlv2`, and that name on PyPI belongs to an unrelated placeholder project. The bindings are built from source (decision 0002).
- Flexo's per-ref SPARQL endpoints choose the dataset only for queries that name no graphs, and holonic's layer reads use `GRAPH` patterns ([zwelz3/holonic#53](https://github.com/zwelz3/holonic/issues/53)).
- holonic validates the union of a holon's interior graphs, so two model versions cannot share a holon (OQ3).
- Claude Code reads `AGENTS.md` when no `CLAUDE.md` exists in the working directory or above it (v2.1.277 or later). Adding a `CLAUDE.md` to this repository stops that unless the new file imports `@AGENTS.md`.

## Working conventions

Pushes go directly to `main` while the project is in design. Commits are authored by the maintainer, and agents add no AI attribution to commits or to pull request bodies (AGENTS.md rule 11). Documents are drafted with the `better-language-skill` skill.
