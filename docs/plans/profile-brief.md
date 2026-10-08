# Profile brief

The profile is the first SysML v2 library package Weft ships. It defines the stereotypes that mark an element as a kind the digital thread tracks (requirement, interface, component, material artifact, and the others listed below), the metadata that carries trace links, and the alignment of each stereotype to BFO and CCO. Every Weft model imports it, and the exported ontology for a model inherits the profile's alignment (open question OQ4). This brief states what is built, from which inputs, and what each part states at minimum.

## Deliverables

| Path | Content |
|---|---|
| `library/WeftProfile.sysml` | Library package with the metadata definitions (stereotypes and trace metadata) |
| `ontology/weft-profile-alignment.ttl` | One alignment axiom per stereotype, and the CCO and BFO version IRIs the alignment was written against |
| `shapes/weft-profile.ttl` | SHACL shapes for the profile's rules, with the severity of each |
| `docs/profile.md` | Reference documentation, one entry per stereotype and per trace property |
| `models/profile-corpus/` | A model that uses every stereotype and every trace property |
| Tests | The four checks listed under acceptance criteria |

## Inputs

- Decisions 0001 to 0004, and open questions OQ2 (identity), OQ4 (ontology export), OQ5 (identity and trace links), and OQ10 (projection vocabulary).
- The SysML v2 standard library at the version pinned by sysml-toolkit (decision 0002), in particular the metadata facilities that let a metadata definition specialize a base type. The exact package and feature names are confirmed against the pinned library before writing, since the profile depends on them.
- BFO 2020 (ISO/IEC 21838-2).
- The current CCO release. Its version IRI is recorded in the alignment file, and the license terms of BFO and CCO are checked before either is packaged with Weft.
- The OSLC link properties for requirements, change management, and quality management (`oslc_rm:implementedBy`, `oslc_rm:validatedBy`, `oslc_rm:trackedBy`, and their counterparts), for the trace metadata.
- The example component requested in the data request issue, which the corpus model is built from once it is available.

## Content of each stereotype

Each stereotype entry in `docs/profile.md` states the following, and the profile is incomplete until every entry does.

1. The SysML element kinds it applies to (for example `part def`, `requirement def`, `interface def`, `port def`, `action def`).
2. What an instance of the exported class is. A `part def Pump` stereotyped as a material artifact exports a class whose instances are physical pumps, and the SysML element is a description of them. An entry that leaves this unstated cannot be aligned, because the BFO category depends on it.
3. The BFO category and the CCO class it aligns to, identified by label and IRI.
4. The metadata it requires, and which of those properties a SHACL shape requires at Violation severity.
5. Whether elements carrying it must have a declared short name. Every stereotype for an element the thread links to requires one (OQ2).

## Minimum stereotypes

| Stereotype | Applies to | Instances of the exported class | Candidate alignment | Status |
|---|---|---|---|---|
| Requirement | `requirement def`, `requirement` | Statements of what a system must do or be | CCO directive information content entity | Candidate |
| Material artifact | `part def`, `part` | Physical objects made to serve a function | CCO material artifact (BFO object) | Candidate |
| Component | `part def`, `part` | Constituents of the system under design, physical or software | Open; a software component is an information content entity in CCO, and a hardware component is a material artifact | Decision needed |
| Interface | `interface def`, `port def` | Open; the specification of an interaction and the realized connection fall in different BFO categories | Open | Decision needed |
| Function | `action def` | Open; a SysML action's instances are performances (BFO processes), while a BFO function is a disposition of a bearer | Open | Decision needed |

The three open rows are decided in the profile work and each decision is recorded in `docs/decisions/`. A stereotype is added beyond this table only if the corpus model or the example component needs it.

## Trace metadata

The profile defines one metadata definition for trace links, applied to the element the link concerns, with one feature per OSLC link property. Its features hold an external key (a ticket key, a commit hash, a test identifier). The derivation step resolves each key to an IRI through a per-project configuration that maps a key kind to a base IRI, and emits the OSLC property as an object property; it never emits the key as a literal (AGENTS.md rule 5). The brief's minimum is the three properties above. Rationale links to decision records are designed with this metadata, and whether a decision record is referenced by path, by IRI, or by a declared identifier is part of the same decision.

## Acceptance criteria

1. `sysmlv2 check --strict` passes on the profile and on the corpus model.
2. The corpus model uses every stereotype and every trace property, and a test fails if one is unused (AGENTS.md rule 8).
3. Every stereotype has exactly one alignment axiom, every alignment axiom names an existing stereotype, and a test checks both directions.
4. Every property that a shape requires at Violation severity is produced from the corpus model's textual notation by the derivation step (AGENTS.md rule 7).

The tests resolve BFO, CCO, and the profile from files in the package or the checkout, without network access (AGENTS.md rule 9).

## Out of scope

Reasoning over the exported ontology (OQ1), domain library packages beyond the profile, and the projection's own vocabulary (OQ10). The projection is designed after the profile, because its terms are expected to follow the stereotypes.
