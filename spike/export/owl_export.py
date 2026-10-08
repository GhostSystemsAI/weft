"""Step 5: derive OWL from a SysML v2 library package's full-json export.

Classes come from definitions (PartDefinition, PortDefinition,
InterfaceDefinition, ActionDefinition, RequirementDefinition,
MetadataDefinition, EnumerationDefinition), named by declaredName and minted
under the library's own namespace (OQ4: "Class IRIs come from the library
namespace and the declared name"). rdfs:subClassOf comes from
Subclassification relationships between two exported classes. Object
properties come from a definition's nested typed features (a part, port, or
interface usage member whose type is itself an exported class); domain is
the owning definition, range is the feature's type. A feature typed by a
scalar (Real, Boolean, and the rest of ScalarValues) or left untyped exports
no property, logged as a coverage gap: OWL has no primitive-datatype
equivalent for SysML's typed value features without a chosen XSD mapping,
which this spike does not attempt.

Usage: python3 owl_export.py <library.full.json> <library-base-iri> <out.ttl> <coverage.md>
"""
import json
import sys

from rdflib import Graph, Namespace, URIRef, RDF, RDFS, OWL, Literal

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

FEATURE_USAGE_TYPES = {
    "PartUsage",
    "PortUsage",
    "InterfaceUsage",
    "ReferenceUsage",
}


def main():
    json_path, library_base, out_ttl, coverage_path = sys.argv[1:5]
    elements = json.load(open(json_path))
    by_id = {e["@id"]: e for e in elements}
    LIB = Namespace(library_base)

    g = Graph()
    g.bind("owl", OWL)

    class_iri = {}
    exported = []
    skipped = []

    for e in elements:
        if e["@type"] in DEFINITION_TYPES and e.get("declaredName"):
            name = e["declaredName"]
            iri = URIRef(f"{library_base}class/{name}")
            class_iri[e["@id"]] = iri
            g.add((iri, RDF.type, OWL.Class))
            exported.append((e["@type"], name, "owl:Class"))
        elif e["@type"] in DEFINITION_TYPES:
            skipped.append((e["@type"], e.get("@id"), "no declaredName"))

    for e in elements:
        if e["@type"] == "Subclassification":
            general = e.get("general", {}).get("@id") or e.get("superclassifier", {}).get("@id")
            specific = e.get("specific", {}).get("@id") or e.get("subclassifier", {}).get("@id")
            if general in class_iri and specific in class_iri:
                g.add((class_iri[specific], RDFS.subClassOf, class_iri[general]))

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
            prop_iri = URIRef(f"{library_base}property/{by_id[owner_id]['declaredName']}_{name}")
            g.add((prop_iri, RDF.type, OWL.ObjectProperty))
            g.add((prop_iri, RDFS.domain, class_iri[owner_id]))
            g.add((prop_iri, RDFS.range, class_iri[range_id]))
            exported.append(("FeatureMembership", f"{by_id[owner_id]['declaredName']}.{name}", "owl:ObjectProperty"))
        else:
            skipped.append(("FeatureMembership", f"{by_id.get(owner_id, {}).get('declaredName')}.{name}",
                             "feature's type is not an exported class (scalar-valued or untyped)"))

    g.serialize(destination=out_ttl, format="turtle")

    declared_defs = [e for e in elements if e["@type"] in DEFINITION_TYPES]
    with open(coverage_path, "w") as f:
        f.write("# Step 5 export coverage\n\n")
        f.write(f"{len(declared_defs)} definitions declared, {len(class_iri)} exported as `owl:Class`.\n\n")
        f.write("| Metaclass | Name | Exported as |\n|---|---|---|\n")
        for metaclass, name, kind in exported:
            f.write(f"| {metaclass} | {name} | {kind} |\n")
        f.write("\n## Not exported\n\n")
        f.write("| Metaclass | Identifier | Why |\n|---|---|---|\n")
        for metaclass, ident, why in skipped:
            f.write(f"| {metaclass} | {ident} | {why} |\n")

    print(f"wrote {out_ttl}: {len(g)} triples; {len(class_iri)} classes; coverage -> {coverage_path}")


if __name__ == "__main__":
    main()
