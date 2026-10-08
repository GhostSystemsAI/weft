# Stable element identity across renames for text-authored models

> Draft issue for [Open-MBEE/sysml-toolkit](https://github.com/Open-MBEE/sysml-toolkit), not yet filed. The maintainer files it; this copy records the text that was reviewed.

## Context

We are building Weft, git-first digital-thread tooling for SysML v2. Models are textual notation in git, checked in CI with this toolkit, and each commit can be mirrored into Flexo MMS through the SysML v2 API. Trace links from tickets, commits, tests, and decision records point at model elements, so those links need element identifiers that survive ordinary edits.

All references are to commit `821221767c3c56cb1ebe7da22666197a47c9c645` (release 0.10.2). We consume scheme 2 identifiers through the Python bindings.

## What IDS.md already records

[IDS.md](https://github.com/Open-MBEE/sysml-toolkit/blob/821221767c3c56cb1ebe7da22666197a47c9c645/IDS.md#backlog-stable-identity-across-renames) lists "stable identity across renames" as backlog. It states that renaming a named element changes its graph-derived id and the ids of its owned subtree, and that rename stability is "deferred pending an identity-lifecycle design". The entry names five candidates for that design to compare:

- a repository- or session-assigned stable `elementId` paired with a separate graph-derivation key used for CBOR elision and delta matching;
- persistent identity sidecars for text-authored models;
- explicit identity annotations in source;
- rename and move rebasing across snapshots and portable deltas;
- migration behavior for already-emitted payloads.

## What a downstream consumer needs

1. An element that is renamed or moved keeps one identifier across the commits before and after the edit, so a mirror such as Flexo records one element with a history rather than a deletion and a creation.
2. The identifier is reproducible from the git checkout alone, without a server, because the model in git is our record.
3. The derivation-key properties IDS.md protects (deterministic reconstruction, compact internal deltas, compatibility with explicit-id payloads) are kept, since we also consume the derived ids.

Of the candidates in IDS.md, the first (a stable `elementId` with a separate derivation key) combined with the second (an identity sidecar for text-authored models) meets all three. The sidecar is versioned with the text in git and supplies `elementId`, while the derived id remains the key for elision and deltas. A sidecar format owned by the toolkit would let every text-first tool share one convention instead of each inventing its own.

## Question

Is the identity-lifecycle design scheduled, and would a contribution of a sidecar format and its rename and move maintenance be welcome? Until then Weft keeps a sidecar map of its own (qualified path to identifier), and we would rather converge on the toolkit's format than migrate from ours later.
