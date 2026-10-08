# Graph contract

Status: skeleton; spike 1 fills it.

This document states what Weft emits from a model: the IRIs it mints, the triples it derives, and the range of each property. Every change to it is a data migration for every user (AGENTS.md rule 3).

## IRI minting

Elements are minted under a namespace that the project's configuration names, and Weft never invents a base on a project's behalf (AGENTS.md rule 4).

## Element mapping from toolkit JSON

Each element in the SysML v2 API JSON that sysml-toolkit emits at the commit pinned in decision 0002 maps to a node whose IRI derives from the element's scheme 2 identifier.

## Relationship mapping and property ranges

Each relationship and each property has a decided range before it is emitted, and an object property is never emitted as a literal (AGENTS.md rule 5).

## Ordered-property representation

Multi-valued properties whose order the metamodel defines keep that order in the graph in a form a SPARQL query can read (OQ7).

## Projection vocabulary

The projection's terms and namespace are fixed here, and the placeholder `proj:` terms in [queries/](../queries/) are replaced by them (OQ10).

## Versioning of the contract

The contract carries its own version, and a change to emitted triples increments it regardless of the package version (AGENTS.md rule 3).
