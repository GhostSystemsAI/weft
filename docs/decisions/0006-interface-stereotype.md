# 0006. Interface on the definition only, as an information content entity

- Status: proposed
- Date: 2026-10-08

## Context

The profile brief ([docs/plans/profile-brief.md](../plans/profile-brief.md)) lists Interface as a minimum stereotype for `interface def` and `port def`, and leaves open what an instance of the exported class is. Two readings fall in different BFO categories. The specification of an interaction, such as the signals, protocol, and connector a port must provide, is an information content entity. A realized connection, such as a cable installed between two pumps in one plant, is a material entity or a relational quality between two material entities.

The buildability review ([docs/reviews/2026-10-08-buildability.md](../reviews/2026-10-08-buildability.md)) proposed applying the stereotype to the definition only.

## Decision

The Interface stereotype applies to `interface def` and `port def`, and not to `interface` or `port` usages. The exported class's instances are interface specifications. The class is a subclass of [CCO directive information content entity](https://www.commoncoreontologies.org/ont00000965), under [CCO information content entity](https://www.commoncoreontologies.org/ont00000958), because an interface definition prescribes what a conforming connection provides.

Realized connections are instance data. A record of an installed connection, held in an adapter holon or in a source such as a cabling workbook, links to the interface specification it conforms to. The derivation emits that link as an object property whose range is the exported interface class (AGENTS.md rule 5). The property's name and namespace are fixed in [docs/graph-contract.md](../graph-contract.md).

An element carrying the stereotype requires a declared short name (OQ2).

## Consequences

The stereotype has one BFO category, and its alignment needs no case split.

Interface usages in a model are not stereotyped. A query for the interfaces a component exposes follows the usage to its definition, and the projection carries that step (OQ10).

The CCO IRIs above are confirmed against the CCO release recorded in the alignment file before that file is written.

## Alternatives considered

The stereotype on usages as well as definitions, with the usage exported as a realized connection. Rejected because a usage in a SysML model is a feature of a definition, not a connection in the world, and exporting it as a material entity would assert installations that the model does not record.

Two stereotypes, Interface specification and Interface connection. Rejected because the profile brief adds a stereotype only when the corpus model or the example component needs it, and no source for realized connections exists in the repository yet.
