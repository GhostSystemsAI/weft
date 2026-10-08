"""Step 6: derive SHACL shapes from a SysML v2 library package's full-json
export, reusing step 5's class and property IRIs (owl_export.py) so the
shapes validate against the same classes the OWL export declares.

One sh:NodeShape per definition, sh:targetClass the class IRI. One
sh:property per structural feature (a part, port, or interface member),
sh:path the property IRI, sh:class the feature's type, sh:minCount/
sh:maxCount 1 (this spike's model declares no explicit multiplicity, so
every feature gets the metamodel's implicit default of exactly one; a model
with declared multiplicity ranges needs this extended to read them).

A stereotype's own features (here, Component's `bearer`) are declared on the
metadata definition, not on the component class it annotates (decision
0005's `@Component { bearer = ...; }` nests `bearer` inside Component, not
inside Pump). For a shape that validates component instance data to catch a
missing or mistyped bearer value, this derivation also adds the metadata
definition's property shapes onto the NodeShape of every class that
metadata annotates (sh:property, not sh:node, so the merged shape is one
NodeShape per component class rather than an indirection a pySHACL target
has to follow). This is a derivation choice this spike documents rather than
a general rule; OQ6 covers where else membrane validation needs it.

Severity is sh:Violation throughout, so a shape this derivation emits is
satisfiable through the primary authoring path (AGENTS.md rule 7): every
property it requires is one sysml-toolkit's JSON export surfaces directly.

Usage: python3 shacl_export.py <library.full.json> <library-base-iri> <out.ttl>
"""
import json
import sys

from rdflib import Graph, Namespace, URIRef, RDF, RDFS, SH

DEFINITION_TYPES = {
    "PartDefinition",
    "PortDefinition",
    "InterfaceDefinition",
    "ConjugatedPortDefinition",
    "ActionDefinition",
    "RequirementDefinition",
    "MetadataDefinition",
    "EnumerationDefinition",
    "VerificationCaseDefinition",
}

FEATURE_USAGE_TYPES = {"PartUsage", "PortUsage", "InterfaceUsage", "ReferenceUsage"}


def collect(elements, library_base):
    by_id = {e["@id"]: e for e in elements}
    class_iri = {}
    for e in elements:
        if e["@type"] in DEFINITION_TYPES and e.get("declaredName"):
            class_iri[e["@id"]] = URIRef(f"{library_base}class/{e['declaredName']}")

    # (owner_class_id, name) -> (prop_iri, range_class_id)
    properties_by_owner = {}
    for e in elements:
        if e["@type"] != "FeatureMembership":
            continue
        owner_id = e.get("owningType", {}).get("@id")
        member_id = e.get("ownedMemberElement", {}).get("@id")
        name = e.get("memberName") or e.get("ownedMemberName")
        if owner_id not in class_iri or member_id is None or not name:
            continue
        member = by_id.get(member_id)
        if member is None or member["@type"] not in FEATURE_USAGE_TYPES:
            continue
        type_refs = member.get("type") or []
        range_id = type_refs[0]["@id"] if type_refs else None
        if range_id in class_iri:
            owner_name = by_id[owner_id]["declaredName"]
            prop_iri = URIRef(f"{library_base}property/{owner_name}_{name}")
            properties_by_owner.setdefault(owner_id, []).append((prop_iri, range_id))

    annotations = []  # (annotated_element_id, metadata_type_id)
    for e in elements:
        if e["@type"] == "MetadataUsage":
            type_refs = e.get("type") or []
            ann_refs = e.get("annotatedElement") or []
            if type_refs and ann_refs:
                annotations.append((ann_refs[0]["@id"], type_refs[0]["@id"]))

    return class_iri, properties_by_owner, annotations


def main():
    json_path, library_base, out_ttl = sys.argv[1:4]
    elements = json.load(open(json_path))
    class_iri, properties_by_owner, annotations = collect(elements, library_base)

    g = Graph()
    SHAPES = Namespace(f"{library_base}shape/")

    for class_id, iri in class_iri.items():
        shape_iri = URIRef(f"{library_base}shape/{iri.rsplit('/', 1)[-1]}")
        g.add((shape_iri, RDF.type, SH.NodeShape))
        g.add((shape_iri, SH.targetClass, iri))

        own_and_inherited = list(properties_by_owner.get(class_id, []))
        for annotated_id, metadata_type_id in annotations:
            if annotated_id == class_id:
                own_and_inherited += properties_by_owner.get(metadata_type_id, [])

        for prop_iri, range_id in own_and_inherited:
            prop_shape = URIRef(f"{prop_iri}-shape")
            g.add((shape_iri, SH.property, prop_shape))
            g.add((prop_shape, SH.path, prop_iri))
            g.add((prop_shape, SH["class"], class_iri[range_id]))
            g.add((prop_shape, SH.minCount, __import__("rdflib").Literal(1)))
            g.add((prop_shape, SH.maxCount, __import__("rdflib").Literal(1)))
            g.add((prop_shape, SH.severity, SH.Violation))

    g.serialize(destination=out_ttl, format="turtle")
    print(f"wrote {out_ttl}: {len(g)} triples; {len(class_iri)} node shapes")


if __name__ == "__main__":
    main()
