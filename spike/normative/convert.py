"""Convert sysml-toolkit full-form interchange JSON to RDF (Turtle) per the
mapping spike 1 decides in docs/graph-contract.md. Not a JSON-LD context: the
full-json shape (one flat array of elements, each with ~150 to 200 fields,
most null or empty for a given element) does not fit a JSON-LD context
cleanly, because JSON-LD expects a fixed small term set per node shape and a
single @id-or-literal coercion per term, while the toolkit emits the same
property name across many metaclasses with a range that the schema, not the
instance document, declares. A direct mapping driven by the schema's range
map (ranges.py) is simpler and keeps every object property's range an
explicit, checked decision (AGENTS.md rule 5) instead of a JSON-LD @context
guess.

Usage: python3 convert.py <full.json> <project-key> <namespace.toml> <out.ttl>
"""
import json
import re
import sys
import tomllib
from urllib.parse import quote

from rdflib import Graph, Namespace, URIRef, Literal, RDF, BNode
from rdflib.collection import Collection

from ranges import build_range_map

KERML_NS = "https://www.omg.org/spec/KerML/20250201/"
SYSML_NS = "https://www.omg.org/spec/SysML/20250201/"
PROP = Namespace("https://weft.ghostsystems.ai/spike1/toolkit-vocab#")

# Decided per step 3: ownedRelationship position is the one property the id
# derivation itself (IDS.md) depends on, so it is the representative ordered
# property for this spike. It is represented as an rdf:List so a SPARQL
# query can walk it with a property path. Every other multi-valued property
# observed in the two models (feature, member, nestedPart, and so on) is
# emitted as a plain set of triples: the metamodel does distinguish ordered
# from unordered features, but the JSON schema does not carry that flag per
# property, and reading it would mean parsing the KerML OCL body text. A
# production derivation reads the metamodel's own `isOrdered` facet instead
# of this spike's one-property allowlist (open question OQ7).
ORDERED_PROPERTIES = {"ownedRelationship"}

SKIP_KEYS = {"@id", "@type", "elementId", "aliasIds"}

KERML_CLASSES = set(json.load(open("/tmp/spike1-toolkit-src/spec-refs/KerML.schema.json"))["$defs"].keys())
SYSML_CLASSES = set(json.load(open("/tmp/spike1-toolkit-src/spec-refs/SysML.schema.json"))["$defs"].keys())


def class_iri(metaclass):
    if metaclass in SYSML_CLASSES:
        return URIRef(SYSML_NS + metaclass)
    if metaclass in KERML_CLASSES:
        return URIRef(KERML_NS + metaclass)
    return URIRef(PROP["Unknown" + metaclass])


def escape_short_name(name):
    # Mirrors IDS.md's escape_name: percent-escape characters outside
    # [A-Za-z0-9_-] so the minted IRI is a valid, stable path segment.
    return quote(name, safe="_-")


def load_namespace(path, key):
    cfg = tomllib.load(open(path, "rb"))[key]
    return cfg


def main():
    json_path, project_key, ns_path, out_path = sys.argv[1:5]
    elements = json.load(open(json_path))
    ns = load_namespace(ns_path, project_key)
    base = ns["base"]

    by_id = {e["@id"]: e for e in elements}
    per_class_range, by_name_range = build_range_map()

    def mint(elem):
        etype = elem["@type"]
        short = elem.get("declaredShortName")
        if etype in ("RequirementUsage", "RequirementDefinition") and short:
            return URIRef(ns["requirement_mint_pattern"].format(base=base, short_name=escape_short_name(short)))
        return URIRef(ns["element_mint_pattern"].format(base=base, element_id=elem["elementId"]))

    def resolve_ref(ref_id):
        target = by_id.get(ref_id)
        if target is None:
            # External (standard-library) reference: keep the toolkit id
            # under the library's own id space, distinct from this
            # project's minted namespace (AGENTS.md rule 4).
            return URIRef(f"https://weft.ghostsystems.ai/spike1/library-element/{ref_id}")
        return mint(target)

    g = Graph()
    gaps = []

    for elem in elements:
        subj = mint(elem)
        etype = elem["@type"]
        g.add((subj, RDF.type, class_iri(etype)))
        for key, value in elem.items():
            if key in SKIP_KEYS or value is None:
                continue
            if isinstance(value, list):
                if not value:
                    continue
                if all(isinstance(v, dict) and "@id" in v for v in value):
                    prop_iri = PROP[key]
                    range_cls = per_class_range.get((etype, key))
                    if range_cls is None:
                        ranges = by_name_range.get(key)
                        range_cls = next(iter(ranges)) if ranges and len(ranges) == 1 else None
                    if range_cls is None:
                        gaps.append((etype, key))
                    if key in ORDERED_PROPERTIES:
                        items = [resolve_ref(v["@id"]) for v in value]
                        list_node = BNode()
                        Collection(g, list_node, items)
                        g.add((subj, prop_iri, list_node))
                    else:
                        for v in value:
                            g.add((subj, prop_iri, resolve_ref(v["@id"])))
                else:
                    # Array of literals (e.g. aliasIds, handled above) or
                    # mixed scalars; emit each as a datatype triple.
                    for v in value:
                        if isinstance(v, bool):
                            g.add((subj, PROP[key], Literal(v)))
                        elif isinstance(v, (str, int, float)):
                            g.add((subj, PROP[key], Literal(v)))
            elif isinstance(value, dict) and "@id" in value:
                prop_iri = PROP[key]
                range_cls = per_class_range.get((etype, key)) or (
                    next(iter(by_name_range.get(key, [])), None) if len(by_name_range.get(key, [])) == 1 else None
                )
                if range_cls is None:
                    gaps.append((etype, key))
                g.add((subj, prop_iri, resolve_ref(value["@id"])))
            elif isinstance(value, bool):
                g.add((subj, PROP[key], Literal(value)))
            elif isinstance(value, (str, int, float)):
                g.add((subj, PROP[key], Literal(value)))

    g.serialize(destination=out_path, format="turtle")

    gap_path = out_path.replace(".ttl", ".gaps.txt")
    with open(gap_path, "w") as f:
        seen = set()
        for etype, key in gaps:
            if (etype, key) not in seen:
                seen.add((etype, key))
                f.write(f"{etype}.{key}\n")
    print(f"wrote {out_path}: {len(g)} triples; {len(seen)} (metaclass, property) range gaps logged to {gap_path}")


if __name__ == "__main__":
    main()
