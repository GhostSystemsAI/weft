"""Step 6: convert the stand-in instance table (instances.csv) to RDF
instance triples, applying each row's injected fault. This table is a
stand-in for the real adopter's instance data (issue #1); step 6 repeats
with the real table once it arrives.

Faults:
  dangling_ref      an object property references an id absent from the
                     table (no rdf:type triple exists for it at all).
  missing_required  an object property this spike's shapes require
                     (minCount 1) is left empty.
  missing_bearer    the bearer property is left empty (minCount 1 on a
                     datatype-shaped stand-in).
  wrong_bearer_type  bearer is asserted as a plain string literal instead of
                     a BearerKind individual (sh:class violation).
  duplicate_bearer   two bearer values are asserted (maxCount 1 violation).

Usage: python3 build_instances.py <instances.csv> <library-base-iri> <out.ttl>
"""
import csv
import sys

from rdflib import Graph, Namespace, URIRef, RDF, Literal

REF_PROPERTIES = {
    "pump_ref": ("pump", "Pump"),
    "controller_ref": ("controller", "Controller"),
    "sensor_ref": ("sensor", "Enclosure"),  # placeholder, overwritten below
    "enclosure_ref": ("enclosure", "Enclosure"),
}
REF_PROPERTIES["sensor_ref"] = ("sensor", "PressureSensor")


def main():
    csv_path, library_base, out_ttl = sys.argv[1:4]
    LIB = Namespace(library_base)
    g = Graph()

    rows = list(csv.DictReader(open(csv_path)))
    present_ids = {row["id"] for row in rows}

    bearer_kind_class = URIRef(f"{library_base}class/BearerKind")
    for value in ("material", "information"):
        g.add((URIRef(f"{library_base}individual/BearerKind/{value}"), RDF.type, bearer_kind_class))

    for row in rows:
        subj = URIRef(f"{library_base}instance/{row['id']}")
        class_iri = URIRef(f"{library_base}class/{row['class']}")
        g.add((subj, RDF.type, class_iri))

        fault = row["fault"]
        bearer_raw = row["bearer"]
        bearer_prop = URIRef(f"{library_base}property/Component_bearer")

        if fault == "missing_bearer":
            pass  # no bearer triple at all: minCount violation
        elif fault == "wrong_bearer_type":
            g.add((subj, bearer_prop, Literal(bearer_raw)))  # plain literal, not a BearerKind individual
        elif fault == "duplicate_bearer":
            for value in bearer_raw.split(","):
                g.add((subj, bearer_prop, URIRef(f"{library_base}individual/BearerKind/{value}")))
        elif bearer_raw:
            g.add((subj, bearer_prop, URIRef(f"{library_base}individual/BearerKind/{bearer_raw}")))

        for field, (name, range_class) in REF_PROPERTIES.items():
            ref_id = row.get(field)
            if not ref_id:
                continue
            prop_iri = URIRef(f"{library_base}property/PumpSystem_{name}")
            target = URIRef(f"{library_base}instance/{ref_id}")
            g.add((subj, prop_iri, target))
            if fault == "dangling_ref" and ref_id not in present_ids:
                pass  # deliberately no rdf:type for the dangling target

    g.serialize(destination=out_ttl, format="turtle")
    print(f"wrote {out_ttl}: {len(g)} triples from {len(rows)} rows")


if __name__ == "__main__":
    main()
