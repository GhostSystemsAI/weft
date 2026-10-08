# 0002. sysml-toolkit for parsing, checking, and interchange

- Status: accepted
- Date: 2026-10-08

## Context

Weft reads SysML v2 textual notation, checks it against the specification's well-formedness rules, converts it to and from SysML v2 API JSON, and applies edits (rename, insert, move) to the text. It is written in Python (decision 0004). Three implementations were considered.

[sysml-toolkit](https://github.com/Open-MBEE/sysml-toolkit) is a Rust workspace under Apache-2.0 with a `sysmlv2` CLI and Python bindings built with maturin. It parses with error recovery, resolves names against a vendored standard library that carries the normative KerML element identifiers, writes compact and full JSON and reads JSON back to text, implements the specification's validation constraints and a separate lint layer (both report as JSON), and provides a transformation API that edits text without disturbing its formatting. Its README states that behavioral execution is not implemented. Version 0.10.2 was reviewed.

[OpenSysML](https://github.com/Open-MBEE/OpenSysML) is a Go implementation reached from Python over gRPC. It executes actions and state machines. Its state machines accept constructs that the SysML v2 grammar does not define (`initial`, `region`, `history`, `choice`, `junction`, `defer`), which sysml-toolkit's test fixtures record as OpenSysML extensions.

The OMG pilot implementation is the reference implementation and runs on Java and Eclipse.

## Decision

Weft uses sysml-toolkit, pinned to a specific release, through its Python bindings for in-process work and through its CLI in CI.

The pins are the following.

| Dependency | Pin |
|---|---|
| sysml-toolkit | Commit `821221767c3c56cb1ebe7da22666197a47c9c645`, release 0.10.2 |
| SysML-v2-Release, the standard library the toolkit vendors as the `spec-refs/SysML-v2-Release` submodule | Commit `de1070ae8e79c21532b8004fc663d47b35d0e9fa` |

Changing either pin is a change to this decision, and the versions table in STATUS.md records the new hash.

Weft consumes element identifiers under scheme 2, the toolkit's legacy lowering (`GraphFormat::LegacyV2`). The toolkit's `IDS.md` at the pinned commit defines scheme 2 as the default for every existing constructor, and scheme 3 (`GraphFormat::CanonicalV3`, canonical lowering) as an opt-in. A Rust client selects scheme 3 with `Model::with_graph_format` or `Session::from_sources_with_graph_format` before it loads sources. The Python bindings in `crates/sysmlv2-py` expose no graph-format selection at the pinned commit, so a Weft process that uses them receives scheme 2 identifiers. A move to scheme 3 changes the identifiers of the operands that canonical lowering wraps and of their descendants, and is a graph-contract migration under AGENTS.md rule 3.

## Consequences

Model text that passes Weft's checks is portable to any implementation that follows the SysML v2 grammar, because the toolkit rejects the OpenSysML-only constructs.

Weft inherits the toolkit's derivation of element identifiers from model structure and names, under which a rename changes the renamed element's identifier. Open question OQ2 covers the identity layer this requires.

Behavioral execution is unavailable (open question OQ8).

The bindings are built from source. Their package name, `sysmlv2`, is already registered on PyPI by an unrelated placeholder project, so Weft cannot declare a PyPI dependency on the toolkit and resolves it from the pinned source or from a wheel built in CI. Building from source requires Rust 1.97 or later, as stated in the toolkit's workspace manifest.

## Alternatives considered

OpenSysML was rejected as the parser because models written for it can use constructs outside the SysML v2 grammar and because access from Python goes through a separate server process. It remains the candidate if behavioral execution is needed later.

The pilot implementation was rejected because it requires a Java and Eclipse runtime in every environment that runs Weft's checks, including CI.
