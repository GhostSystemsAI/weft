# 0007. Process as the stereotype for action definitions

- Status: proposed
- Date: 2026-10-08

## Context

The profile brief ([docs/plans/profile-brief.md](../plans/profile-brief.md)) names the `action def` stereotype Function and leaves its alignment open. An instance of a SysML action definition is a performance, an occurrence that unfolds in time. In BFO that is a [process](http://purl.obolibrary.org/obo/BFO_0000015). A BFO [function](http://purl.obolibrary.org/obo/BFO_0000034) is a disposition ([BFO disposition](http://purl.obolibrary.org/obo/BFO_0000016)) of a material bearer, which exists whether or not it is ever realized, and CCO's function classes specialize it. A stereotype named Function and aligned to a process class reads as the disposition to anyone who knows BFO or CCO, and a stereotype aligned to the disposition misstates what the action definition's instances are.

The buildability review ([docs/reviews/2026-10-08-buildability.md](../reviews/2026-10-08-buildability.md)) recommended naming the stereotype for what it exports.

## Decision

The stereotype for `action def` is named Process. The exported class's instances are processes, and the class is a subclass of [BFO process](http://purl.obolibrary.org/obo/BFO_0000015).

Process names what the exported class contains. It is the BFO term for that category, and it does not collide with a KerML or SysML metaclass name, so `#Process action def Pump_fluid` reads without ambiguity in textual notation.

Where a model needs the function a component has, the alignment relates the two through [realizes](http://purl.obolibrary.org/obo/BFO_0000055): a process realizes a function borne by a component. That function is a disposition of the component's bearer (decision 0005), and a stereotype for it is added only when the corpus model or the example component needs one.

An element carrying the stereotype requires a declared short name (OQ2).

## Consequences

The exported class has one BFO category, and the profile documentation states that its instances are performances of the action.

The profile brief's minimum stereotype table lists the row as Function. That row is renamed when this decision is accepted.

The alignment file can state a more specific CCO class, such as an act class for processes with an agent, in a later revision without renaming the stereotype.

## Alternatives considered

Function, as the profile brief proposes. Rejected because CCO's Function is a disposition and the action definition's instances are processes.

Performance. Rejected because it is the KerML metaclass that SysML actions specialize, so `#Performance` would name the metamodel and not the exported class.

Action. Rejected because it repeats the SysML keyword the stereotype is applied to and adds no information.

Activity. Rejected because it is the SysML v1 term, which carries v1 semantics into a v2 model.
