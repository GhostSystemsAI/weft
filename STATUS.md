# Status

State of the project as of 2026-10-08. The session that changes the project's state updates this file before it ends; [AGENTS.md](AGENTS.md) holds the rules that do not change from session to session.

## Phase

Design. The repository holds decision records, open questions, a plan for the profile, and no code.

## Settled

| Decision | Content |
|---|---|
| [0001](docs/decisions/0001-git-is-the-record.md) | SysML v2 textual notation in git is the record. Flexo MMS is an optional one-way mirror (tier 1), and every core feature works at tier 0 without a server. |
| [0002](docs/decisions/0002-sysml-toolkit-for-parsing-and-checking.md) | sysml-toolkit parses, checks, and converts to and from SysML v2 API JSON. |
| [0003](docs/decisions/0003-holonic-for-graph-organization.md) | holonic organizes the derived graphs, one holon per model version. |
| [0004](docs/decisions/0004-python.md) | Python, 3.11 or later. |

## Open work

| Item | Location | State | Next action |
|---|---|---|---|
| Data for the spike | [zwelz3/weft#1](https://github.com/zwelz3/weft/issues/1) | Requested | The maintainer supplies a component, an instance table, trace data, and an adapter ontology excerpt |
| Spike 1 | [zwelz3/weft#2](https://github.com/zwelz3/weft/issues/2) | Not started | Steps 1 to 5 and measurements M1 to M4 can start on a public example before #1 is answered |
| Profile | [docs/plans/profile-brief.md](docs/plans/profile-brief.md) | Not started | Decide the component, interface, and function stereotypes, recording each in `docs/decisions/` |
| Report to Flexo maintainers | [docs/outreach/flexo-sysmlv2-rdf.md](docs/outreach/flexo-sysmlv2-rdf.md) | Drafted and reviewed, not filed | The maintainer files it on Open-MBEE/flexo-mms-sysmlv2 |
| holonic enhancements | [#50](https://github.com/zwelz3/holonic/issues/50), [#51](https://github.com/zwelz3/holonic/issues/51), [#52](https://github.com/zwelz3/holonic/issues/52), [#53](https://github.com/zwelz3/holonic/issues/53) | Filed | #50 waits on [holonic#30](https://github.com/zwelz3/holonic/issues/30) |

The design questions behind this work are in [docs/OPEN-QUESTIONS.md](docs/OPEN-QUESTIONS.md) (OQ1 to OQ10).

## Versions reviewed

| Project | Version | How it was reviewed |
|---|---|---|
| [sysml-toolkit](https://github.com/Open-MBEE/sysml-toolkit) | 0.10.2 | From a source archive of `main`, with no commit hash recorded. The archive's `spec-refs/` submodules were empty, so the standard library has to be fetched separately before `--lib` can be used. |
| [flexo-mms-sysmlv2](https://github.com/Open-MBEE/flexo-mms-sysmlv2) | Commit `61d1c9da77e1f0eebd4734290b8bb04fb04162f0` | Clone |
| [holonic](https://github.com/zwelz3/holonic) | `main` at commit `d8d1758`, after the 0.8.0 release | Clone and source archive |
| [OpenSysML](https://github.com/Open-MBEE/OpenSysML) | Documentation only | README on pkg.go.dev; opensysml.org was unreachable from the session that reviewed it |

## Findings that are easy to rediscover

- The toolkit's Python package is named `sysmlv2`, and that name on PyPI belongs to an unrelated placeholder project. The bindings are built from source (decision 0002).
- Flexo's per-ref SPARQL endpoints choose the dataset only for queries that name no graphs, and holonic's layer reads use `GRAPH` patterns ([zwelz3/holonic#53](https://github.com/zwelz3/holonic/issues/53)).
- holonic validates the union of a holon's interior graphs, so two model versions cannot share a holon (OQ3).
- Claude Code reads `AGENTS.md` when no `CLAUDE.md` exists in the working directory or above it (v2.1.277 or later). Adding a `CLAUDE.md` to this repository stops that unless the new file imports `@AGENTS.md`.

## Working conventions

Pushes go directly to `main` while the project is in design. Commits are authored by the maintainer, and agents add no AI attribution to commits or to pull request bodies (AGENTS.md rule 11). Documents are drafted with the `better-language-skill` skill.
