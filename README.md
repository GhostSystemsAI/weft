# Weft

Weft connects the requirements, interfaces, and components in a SysML v2 model to the tickets, commits, tests, decision records, and records in other systems that make up the rest of an engineering digital thread. The model is kept as SysML v2 textual notation in git, and Weft derives the RDF graphs that the thread queries and validates.

The project is in design. The repository holds design documents and no code.

## Intended workflow

People describe an architecture, a component, an interface, or a requirement in natural language to an LLM agent, and the agent produces or edits SysML v2. The natural-language prompt is not stored; the reviewed model is the specification, and the reasons behind a modeling choice are kept in decision records linked to the elements they concern.

From the model, Weft derives the following graphs:

| Graph | Content | Purpose |
|---|---|---|
| Normative graph | KerML-level elements and relationships, complete | Fidelity and round trip to textual notation |
| Projection | A small set of thread-level terms (component, interface, requirement, decision) | Linking and querying across systems |
| Exported ontology | OWL classes derived from SysML library packages, with BFO/CCO alignment through a profile | Reuse of domain definitions across models |
| Derived shapes | SHACL shapes generated from definitions and multiplicities | Validation of instance data held in other systems against the model |

Links to external artifacts use the OSLC link vocabulary (`oslc_rm:implementedBy`, `oslc_rm:validatedBy`, `oslc_rm:trackedBy`) and are validated with SHACL.

## Git for everyone, Flexo MMS for those who adopt it

Git is the record. Every core feature works on a git checkout without a server, and a team that runs [Flexo MMS](https://github.com/Open-MBEE) gains shared, versioned, multi-project querying from a one-way mirror of its git history. [docs/decisions/0001-git-is-the-record.md](docs/decisions/0001-git-is-the-record.md) states the tiers and the reasons for them.

## Related projects

| Project | Role for Weft |
|---|---|
| [sysml-toolkit](https://github.com/Open-MBEE/sysml-toolkit) | Rust parser, validator, and interchange library for SysML v2 and KerML, with Python bindings. Weft's dependency for parsing, well-formedness checking, and JSON interchange (decision 0002). |
| [OpenSysML](https://github.com/Open-MBEE/OpenSysML) | Go implementation that also executes actions and state machines. Not a dependency; behavioral execution is out of scope for now (see the open questions). |
| [flexo-mms-sysmlv2](https://github.com/Open-MBEE/flexo-mms-sysmlv2) | SysML v2 API service on Flexo MMS. The target of the optional mirror. |
| [holonic](https://github.com/zwelz3/holonic) | Four-graph holon substrate (interior, boundary, projection, context) over a quad store. Organizes the derived graphs and the sources they link to (decision 0003). |
| [specl](https://github.com/zwelz3/specl) | Markdown specification language with an RDF graph contract. Weft carries over its working rules on graph contracts and identity. |

## Environment

Weft is a Python library (decision 0004). The deployed quad store is Apache Jena Fuseki, and tier 0 runs on an in-memory rdflib store. Sources such as Excel workbooks and Teamwork Cloud reach the thread through adapters, each with its own ontology; no central ontology unifies them, and Weft links to them through holonic alignment holons and portals.

## Documents

- [STATUS.md](STATUS.md) records the current state and open work.
- [docs/decisions/](docs/decisions/) holds the decision records.
- [docs/plans/](docs/plans/) holds briefs for work that has not started.
- [docs/OPEN-QUESTIONS.md](docs/OPEN-QUESTIONS.md) lists the design questions that are not yet decided, with the current leaning for each.
