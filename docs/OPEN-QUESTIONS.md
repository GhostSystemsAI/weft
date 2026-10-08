# Open questions

Design questions that are not yet decided. Each entry states the question, what is known, and the current leaning. A question leaves this file when a decision record in `docs/decisions/` settles it.

## OQ1. Reasoning

Reasoning is deferred. OWL reasoning over the exported class layer would detect contradictions that SHACL cannot, for example an element stereotyped as a process whose definition is aligned to a BFO material entity, where BFO declares the two disjoint. Deferring reasoning also defers most of the value of BFO/CCO alignment (OQ4), because without a reasoner or a query that uses the aligned categories the alignment serves as documentation.

Undecided when reasoning becomes a priority is where it runs. An OWL RL rule set inside the quad store keeps inferences current but is limited to the RL profile. A DL reasoner run in CI covers more of OWL 2 and produces results only at build time.

## OQ2. Element identity

sysml-toolkit derives each user element's identifier from model structure and names, and documents identifier schemes 2 and 3 with a migration function between them. A rename therefore changes the renamed element's identifier. Decision records, trace links, and the Flexo mirror (decision 0001) all need identifiers that survive edits.

Current leaning, in two parts:

- Every element that the thread links to (requirements, interfaces, components, decisions) carries a declared short name, for example `requirement <'REQ-014'> brakeResponse`. A shape or lint rule enforces this. Weft mints the element's IRI from the short name under a namespace the project controls, and not from the derived identifier or the qualified name, because moving an element changes its qualified name.
- Element-level identity for the mirror is kept in a sidecar map in git (qualified path to UUID), updated by tooling when an element is renamed or moved.

Unverified is whether derived identifiers can collide between two projects whose elements have identical names and structure. It matters for the mirror, because flexo-mms-sysmlv2 mints every element into one URN namespace.

## OQ3. Versions and holons

Each ref (a branch head or a baseline) is a holon whose interior holds that version's normative graph. Element IRIs are stable across version holons, so the IRI identifies the element over its lifetime and the named graph identifies its state at one version. A query that does not scope by graph sees every version's statements at once; thread queries therefore go through a helper that requires a version.

A holon per commit was considered and rejected, because it materializes every commit, which Flexo avoids by materializing only referenced commits. Inferring the latest version from the newest provenance timestamp was rejected, because with more than one branch it selects whichever branch changed last. The current version is a recorded ref.

Two versions cannot share a holon. holonic validates the union of a holon's interior graphs against the union of its boundary graphs, and `traverse()` injects into the first registered interior, so a holon holding two versions would be validated as one merged model.

Open is how a holon's interior refers to a Flexo snapshot when the mirror is in use. A holonic backend that reads through Flexo's per-ref endpoints is the leading option, with holonic's own registry, boundary, and context graphs kept outside the graphs Flexo manages.

## OQ4. Ontology export and reuse

Ontologies are exported from SysML library packages so that a domain definition is reused across models rather than minted again by each one. A library package derives to one ontology with its own namespace and `owl:versionIRI`, and a model that imports the library in SysML derives an ontology that `owl:imports` it. Class IRIs come from the library namespace and the declared name, so two models importing the same library version produce the same class IRIs.

Definitions and specialization derive to OWL classes and `rdfs:subClassOf` without loss. Usages with contextual features, redefinition in context, and feature chains have no direct OWL equivalent, so reusable knowledge belongs in definitions inside library packages.

BFO/CCO grounding is applied through a profile. A stereotype such as `«MaterialArtifact»` is aligned once to its BFO/CCO class in an alignment file kept outside the SysML, and an element that carries the stereotype inherits the alignment in the exported ontology. A test asserts that every stereotype has exactly one alignment axiom and that every alignment axiom names an existing stereotype.

## OQ5. Identity links and trace links

`owl:sameAs` states that two IRIs denote one individual. It applies to co-reference, such as one pump recorded in an asset database and in a configuration database. It does not apply to a ticket that tracks a requirement or a commit that implements one; those are trace links and use the OSLC link vocabulary.

Current leaning is a holon subtype that holds only identity assertions, each with provenance naming the matcher or person that made it. Queries and portals can include or exclude that graph, and a wrong match is withdrawn by removing it from one graph. This requires a holonic enhancement; holonic's `AlignmentHolon` holds vocabulary mappings and is not extended to entity identity.

## OQ6. Derived shapes for instance data

SHACL shapes generated from definitions (`sh:datatype` and `sh:class` from typing, cardinality from multiplicity) would validate records in other systems against the model. A shape that targets a class reports conformance when no instance of that class is present, so records that arrive with the wrong type pass without a finding. This is open question OQ11 in holonic, and derived shapes depend on its resolution. holonic issue [#30](https://github.com/zwelz3/holonic/issues/30), in which unclassified validation results are dropped and `fail_on_breach` lets data through, also has to be fixed before boundaries enforce derived shapes.

## OQ7. Flexo's RDF representation

flexo-mms-sysmlv2 (at `61d1c9da77e1f0eebd4734290b8bb04fb04162f0`) maps API JSON to RDF key by key. Element IRIs are `urn:sysmlv2:element:<id>` on every deployment, each element carries only its most specific metaclass, multi-valued properties keep their order only in a serialized JSON string, and a JSON `null` is stored as `rdf:nil`. Round trips through the API are unaffected. The issues limit direct SPARQL consumers, and a report to the Flexo maintainers is drafted but not filed.

## OQ8. Behavioral execution

Out of scope at the start. OpenSysML is the only implementation that executes actions and state machines, and its state machines accept constructs outside the SysML v2 grammar (`initial`, `region`, `history`, `choice`, `junction`, `defer`), so a model that uses them is specific to OpenSysML. The first use case that would justify execution is verification, for example running an interface protocol modeled as a state machine against recorded traffic.

## OQ9. Round trip for edits made in Flexo

Tier 2 in decision 0001 depends on converting SysML v2 API JSON back to textual notation. sysml-toolkit reads JSON back to text; which formatting and comment placement the conversion loses is not yet measured.
