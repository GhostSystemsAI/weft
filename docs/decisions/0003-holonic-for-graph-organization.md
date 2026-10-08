# 0003. holonic for graph organization

- Status: accepted
- Date: 2026-10-08

## Context

Weft produces several graphs from each model version (normative graph, projection, exported ontology, derived shapes) and links them to graphs produced by adapters for other sources, such as Excel workbooks and Teamwork Cloud. Each adapter has its own ontology; no central ontology unifies them. The graphs need named-graph organization, validation boundaries, provenance of how each graph was produced, and controlled movement of data between vocabularies. The deployed quad store is Apache Jena Fuseki.

[holonic](https://github.com/zwelz3/holonic) (0.8.0 on PyPI, Python 3.11 or later) organizes a dataset into holons, each an IRI with four kinds of named graph. Interior graphs hold data, boundary graphs hold SHACL shapes and portal definitions, projection graphs hold what other holons see, and context graphs hold membership and provenance. Portals move data between holons through SPARQL CONSTRUCT queries, alignment holons hold vocabulary mappings, and traversal and validation are recorded with PROV-O. holonic ships an in-memory rdflib backend and a Fuseki backend.

## Decision

Weft organizes its graphs as holons using holonic.

| Holon layer | Content for one model version |
|---|---|
| Interior | Normative graph; exported ontology as a second interior graph |
| Boundary | Hand-written policy shapes and derived shapes |
| Projection | Thread projection; rendered views |
| Context | Model membership, the ref the version belongs to, provenance of the derivation |

Each source that an adapter covers is its own holon, and portals carry data between source holons and model holons.

## Consequences

Tier 0 (decision 0001) runs on the rdflib backend and needs no server. A deployment with Fuseki uses the Fuseki backend with the same holon structure.

A model version is a holon of its own and never shares a holon with another version, because holonic validates the union of a holon's interior graphs as one dataset (open question OQ3).

The adapters' separate ontologies are reconciled through alignment holons and portals rather than through a central ontology that Weft would have to define first.

holonic requires enhancements before this design works end to end. Both projects have the same maintainer, so each is a holonic issue:

- a check that fails validation on interior nodes whose types no boundary shape targets ([zwelz3/holonic#50](https://github.com/zwelz3/holonic/issues/50), after [#30](https://github.com/zwelz3/holonic/issues/30));
- a holon subtype for identity assertions ([#51](https://github.com/zwelz3/holonic/issues/51));
- a query helper that requires a version scope ([#52](https://github.com/zwelz3/holonic/issues/52));
- a backend that reads model versions from Flexo MMS ([#53](https://github.com/zwelz3/holonic/issues/53)).

## Alternatives considered

Plain named graphs with conventions defined in Weft. Rejected because Weft would reimplement holonic's registry, membrane validation, and provenance recording.
