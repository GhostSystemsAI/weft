# RDF representation of elements for direct SPARQL consumers

> Draft issue for [Open-MBEE/flexo-mms-sysmlv2](https://github.com/Open-MBEE/flexo-mms-sysmlv2), not yet filed. The maintainer files it; this copy records the text that was reviewed.

## Context

We are building git-first tooling for SysML v2 (textual models in git, checked in CI) that mirrors each commit into Flexo through the standard SysML v2 API. Round trips through the API work, because the JSON that goes in comes back out. The points below concern consumers that read the triplestore directly over SPARQL, such as a digital-thread layer that links model elements to tickets, commits, and tests. For those consumers the triples are the contract rather than the JSON.

All references are to commit `61d1c9da77e1f0eebd4734290b8bb04fb04162f0`.

## Observations

### 1. Element IRIs use one URN namespace on every deployment

`SYSMLV2.element(id)` mints `urn:sysmlv2:element:<id>` for every project on every deployment ([Namespaces.kt#L13-L21](https://github.com/Open-MBEE/flexo-mms-sysmlv2/blob/61d1c9da77e1f0eebd4734290b8bb04fb04162f0/src/main/kotlin/org/openmbee/flexo/sysmlv2/Namespaces.kt#L13-L21)). The IRI does not dereference, so an external graph that links to an element cannot resolve the link. Uniqueness across projects also rests entirely on the element identifiers, which some tools derive from model structure and names rather than generating at random.

Are these IRIs meant to be public identifiers that external data links to? If they are, would a configurable base per deployment or per project be in scope?

### 2. Elements carry only their most specific metaclass

The `@type` key becomes a single `rdf:type` triple ([CommitApi.kt#L196](https://github.com/Open-MBEE/flexo-mms-sysmlv2/blob/61d1c9da77e1f0eebd4734290b8bb04fb04162f0/src/main/kotlin/org/openmbee/flexo/sysmlv2/apis/CommitApi.kt#L196)). The service does not load the KerML and SysML class hierarchy, and the only `rdfs:subClassOf` triples in the repository describe MMS's own classes (`src/test/resources/cluster.trig`). A pattern such as `?x a sysml:Feature` therefore matches no `sysml:PartUsage`. A `PrimitiveConstraint` on `@type` in the query API also matches `rdf:type` exactly ([QueryApi.kt#L45](https://github.com/Open-MBEE/flexo-mms-sysmlv2/blob/61d1c9da77e1f0eebd4734290b8bb04fb04162f0/src/main/kotlin/org/openmbee/flexo/sysmlv2/apis/QueryApi.kt#L45)).

Does the SysML v2 API specification expect a `@type` constraint to match specializations? Separately, would a vocabulary graph holding the metaclass hierarchy (generated from the published `SysML.xmi` or JSON schema) be welcome, so that SPARQL consumers can use `rdf:type/rdfs:subClassOf*`?

### 3. Order is recoverable only from a JSON string

An array value is written twice, as unordered triples and as a serialized JSON string under `urn:sysmlv2:annotation:json:<key>` ([CommitApi.kt#L211-L237](https://github.com/Open-MBEE/flexo-mms-sysmlv2/blob/61d1c9da77e1f0eebd4734290b8bb04fb04162f0/src/main/kotlin/org/openmbee/flexo/sysmlv2/apis/CommitApi.kt#L211-L237)). Reads prefer the JSON string ([ElementApi.kt#L95-L97](https://github.com/Open-MBEE/flexo-mms-sysmlv2/blob/61d1c9da77e1f0eebd4734290b8bb04fb04162f0/src/main/kotlin/org/openmbee/flexo/sysmlv2/apis/ElementApi.kt#L95-L97)), so the API preserves order while a SPARQL query cannot see it. Membership order, parameter order, and feature-chain order carry meaning in KerML, and a direct consumer loses each of them.

Is the JSON string a permanent part of the storage format? Would an ordering in the triples (an `rdf:List`, or an index on each entry) be considered, keeping the string for the API path if it is still needed?

### 4. `null` is stored as `rdf:nil`

A JSON `null` becomes `rdf:nil` ([CommitApi.kt#L202-L205](https://github.com/Open-MBEE/flexo-mms-sysmlv2/blob/61d1c9da77e1f0eebd4734290b8bb04fb04162f0/src/main/kotlin/org/openmbee/flexo/sysmlv2/apis/CommitApi.kt#L202-L205)). The code comment explains the choice (lists are not otherwise used). A generic RDF consumer reads `rdf:nil` as the empty list, and the two meanings would collide if item 3 adopted `rdf:List`. An absent triple or a dedicated term avoids the collision.

### 5. Ownership of the vocabulary namespace

Properties and types are minted as `https://www.omg.org/spec/SysML#<jsonKey>` ([Namespaces.kt#L12](https://github.com/Open-MBEE/flexo-mms-sysmlv2/blob/61d1c9da77e1f0eebd4734290b8bb04fb04162f0/src/main/kotlin/org/openmbee/flexo/sysmlv2/Namespaces.kt#L12)). Was this namespace coordinated with OMG or with the API specification's JSON-LD material, or chosen locally? Consumers who align these terms with other ontologies depend on the answer, because an alignment to a namespace that later changes has to be redone.

## Why this matters now

Items 2 and 3 limit what the triplestore answers without going back through the REST API, and items 1 and 5 decide whether external graphs can link to Flexo-held elements and terms. None of them affects API correctness. Changing emitted IRIs or triple shapes after deployments accumulate data becomes a migration for each of them, which is the reason for raising the points before that happens.

We can contribute, for example a generated metaclass-hierarchy graph for item 2 or a design note for item 3, and would like to know which items are in scope first.
