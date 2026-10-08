# 0001. Git is the record

- Status: proposed
- Date: 2026-10-08

## Context

Weft needs one authoritative store for SysML v2 models. Two candidates exist.

Git, hosted on GitHub or GitLab, is already used by the teams Weft targets. Textual notation diffs line by line, and pull requests give review and approval without additional infrastructure.

Flexo MMS versions RDF with branches and immutable locks, materializes snapshots for referenced commits, and exposes a SPARQL endpoint per ref. Its SysML v2 service implements the standard SysML v2 API. Git has no equivalent of these features. While Flexo is the stronger store for querying across versions and projects, making it the record requires every user to run it, and a requirement to deploy a model server excludes teams that would otherwise adopt Weft.

## Decision

The SysML v2 textual notation in git is the record. Flexo MMS is an optional mirror, and the features it enables are arranged in tiers so that each tier adds to the one below it without replacing it.

| Tier | Adopted by | Adds |
|---|---|---|
| 0, git only | Every user | Models in git. CI runs well-formedness checks and lint, and builds the derived graphs as artifacts. Trace links live in the model as metadata. Queries run locally against an in-memory store. |
| 1, Flexo mirror | Teams that run Flexo MMS | A CI step converts each git commit to SysML v2 API JSON and commits it to Flexo. Git branches map to Flexo branches and git tags to locks. Server-side SPARQL across versions and projects, Flexo's diff API, and a holonic backend that reads through Flexo become available. |
| 2, edits from MMS | Not planned | Changes made in tools that write to Flexo return to git as pull requests, so git remains where changes are reviewed and merged. |

Every core feature works at tier 0 without network access. A feature available only at tier 1 is an addition to the core, and a core feature that requires tier 1 violates this decision.

## Consequences

The mirror is one way. Flexo holds a queryable copy of git history and is never written to first, so the two stores cannot diverge at tier 1.

The mirror needs element identifiers that survive edits. sysml-toolkit derives a user element's identifier from model structure and names, so a rename reaches Flexo as a deletion and a creation, and Flexo's history no longer connects the two. Textual notation has no syntax for an element identifier, which means stable identifiers have to be kept outside the model text (open question OQ2).

Weft does not use Flexo's RDF as its normative graph. The flexo-mms-sysmlv2 service stores elements under `urn:sysmlv2:element:` regardless of project, records only the most specific metaclass of each element, and keeps the order of multi-valued properties only inside a serialized JSON string (open question OQ7). Weft derives its normative graph, projection, ontologies, and shapes from the toolkit at tier 0, and uses Flexo as versioned storage and a query endpoint.

Trace links to tickets, commits, and tests are written as metadata on the element they describe, so they are versioned with that element and need no server. OSLC services that read Jira or a requirements tool directly are a tier 1 addition.

## Alternatives considered

Flexo as the record, with git optional. This is the established MMS model, in which modeling tools commit to the server directly. It was rejected because it makes a server deployment a precondition of adoption.

Two-way synchronization between git and Flexo at tier 1. It was rejected because concurrent edits in both stores require a merge policy that neither store's review process covers. Tier 2 achieves the same result through pull requests, where the existing review process applies.
