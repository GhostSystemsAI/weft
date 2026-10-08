# Graph contract

Status: skeleton; spike 1 fills it.

This document states what Weft emits from a model: the IRIs it mints, the triples it derives, and the range of each property. Every change to it is a data migration for every user (AGENTS.md rule 3).

## IRI minting

Elements are minted under a namespace that the project's configuration names (`spike/namespace.toml` in the spike), and Weft never invents a base on a project's behalf (AGENTS.md rule 4).

Two patterns, chosen per element kind:

- A `RequirementUsage` or `RequirementDefinition` with a declared short name mints `{base}requirement/{short_name}`, the short name percent-escaped the way `IDS.md` escapes an id-name (characters outside `[A-Za-z0-9_-]` percent-escaped). This is the only element kind the thread links to by short name today (OQ2), so it is the only kind minted from a name rather than from the toolkit's derived id.
- Every other element mints `{base}element/{elementId}`, where `elementId` is the scheme 2 identifier `sysmlv2 convert --to full-json` assigns (decision 0002 pins the toolkit commit this scheme is observed at). The CLI exposes no flag to select scheme 3 (`GraphFormat::CanonicalV3`); it is a Rust-API-only option (`spike/ENVIRONMENT.md`), so this spike mints from scheme 2 only.
- A reference that resolves to no element in the converted document (a standard-library element, resolved only when `--lib` is given and not expanded into the output array) mints `https://weft.ghostsystems.ai/spike1/library-element/{elementId}`, a namespace distinct from any project's, so a library reference is never minted into a project's namespace and a project's namespace never collides with the library's (AGENTS.md rule 4).

## Element mapping from toolkit JSON

Each element in the SysML v2 API JSON that sysml-toolkit emits at the commit pinned in decision 0002 maps to a node typed `rdf:type <class IRI>`, where the class IRI is the metaclass's `$id` in the toolkit's own published JSON Schema (`SysML.schema.json` for a SysML metaclass, else `KerML.schema.json`), both read from the toolkit source clone at the pinned commit. Using the toolkit's own schema `$id`s as class IRIs means the exported graph's classes are the toolkit's own metaclass identifiers, not an IRI spike 1 invents; the library package export in step 5 mints Weft's own class IRIs for user-defined definitions, which is a different mapping from this one.

A property whose JSON value is `null` or an empty array is not asserted; a property with no value in a given element asserts nothing rather than an empty or a blank-valued triple.

## Relationship mapping and property ranges

Every object property's range is decided from the toolkit's JSON Schema before it is emitted (AGENTS.md rule 5), not inferred from what a particular model happens to contain. `spike/normative/ranges.py` reads both schema files' `$defs` and, for every `(metaclass, property)` pair, follows the property's `$ref`/`$comment` chain to the metaclass the schema declares as that reference's target; `spike/normative/convert.py` looks up this map for every reference-valued property before emitting its triples and records a gap file for any pair missing a range. Converting both spike models (`pump-system`, 503 elements, 11,985 triples; `quadcopter`, 4,061 elements, 98,433 triples) produced zero `(metaclass, property)` range gaps: every object property the two models exercise has a schema-declared range. Three property names (of several thousand pairs) have a range that varies by owning metaclass; the per-class lookup resolves these before falling back to a by-name lookup, so this did not produce a gap either.

A property whose value is a single `{"@id": ...}` reference or a list of such references is an object property, range as looked up above, emitted as one triple per reference; a property whose value is a string, number, or boolean is a datatype property, which needs no range decision because `rdfs:Literal` subtypes carry no object-property traceability concern (AGENTS.md rule 5 concerns object properties specifically). No property in either model is emitted as a literal where the schema declares it a reference, and no reference is emitted as a literal.

## Ordered-property representation

Multi-valued properties whose order the metamodel defines keep that order in the graph in a form a SPARQL query can read (OQ7). Spike 1 narrows this to one concrete decision and one open gap:

- `ownedRelationship` is represented as an `rdf:List` (`rdf:first`/`rdf:rest` on a blank node chained from the owner), because it is the one property the toolkit's own id derivation depends on positionally (`IDS.md`'s `r{i}`/`e{j}` positional segments count this array's order), so it is the property this spike's measurements (M1) exercise directly. `rdflib`'s `Collection` helper reads and writes it, and a SPARQL query walks it with the property path `rdf:rest*/rdf:first`.
- Every other multi-valued property observed in the two models (`feature`, `member`, `nestedPart`, and the rest) is emitted as a plain set of triples, unordered. The KerML metamodel does distinguish ordered from unordered features through a `Feature::isOrdered` facet, but the toolkit's JSON Schema does not carry that facet per property name the way it carries ranges; determining it in general means reading the KerML specification's OCL-stated semantics for each property, which this spike did not do for every property, only for the one the id scheme already forced a decision on. A production derivation decides the remaining properties' order representation from the metamodel rather than this spike's one-property allowlist; this is left as a narrowed form of OQ7, not closed by it.

An index-property representation (`sysml:index` on a reified link) and holonic's own ordering mechanism were considered for `ownedRelationship` and not used: `rdf:List` needed no additional vocabulary beyond what `rdflib` already ships, and the list is read back only by the id-churn measurement (M1), which walks it once per edit rather than querying into the middle of it, so the property-path cost of `rdf:List` over an index property did not matter here.

## Projection vocabulary

The projection's terms and namespace are fixed here, and the placeholder `proj:` terms in [queries/](../queries/) are replaced by them (OQ10).

## Versioning of the contract

The contract carries its own version, and a change to emitted triples increments it regardless of the package version (AGENTS.md rule 3).
