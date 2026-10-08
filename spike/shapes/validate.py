"""Step 6: validate the stand-in instance table against the derived SHACL
shapes with pySHACL, and report which injected faults a shape caught.

Usage: python3 validate.py <shapes.ttl> <instances.ttl> <instances.csv> <findings.md>
"""
import csv
import sys

import pyshacl
from rdflib import Graph, URIRef

LIBRARY_BASE = "https://weft.ghostsystems.ai/spike1/pump-library/"


def main():
    shapes_ttl, instances_ttl, csv_path, findings_path = sys.argv[1:5]

    data = Graph().parse(instances_ttl, format="turtle")
    shapes = Graph().parse(shapes_ttl, format="turtle")

    conforms, results_graph, results_text = pyshacl.validate(
        data, shacl_graph=shapes, advanced=True, debug=False
    )

    violating_subjects = set()
    for s in results_graph.subjects(
        URIRef("http://www.w3.org/ns/shacl#focusNode"), None
    ):
        pass
    SH = "http://www.w3.org/ns/shacl#"
    for focus in results_graph.objects(None, URIRef(SH + "focusNode")):
        violating_subjects.add(str(focus))

    rows = list(csv.DictReader(open(csv_path)))
    found = 0
    lines = ["# Step 6 findings\n", f"pySHACL conforms: {conforms}\n", "| Row | Fault | Caught |", "|---|---|---|"]
    for row in rows:
        fault = row["fault"]
        if not fault:
            continue
        subj = f"{LIBRARY_BASE}instance/{row['id']}"
        caught = subj in violating_subjects
        found += int(caught)
        lines.append(f"| {row['id']} | {fault} | {'yes' if caught else 'no'} |")

    total_faults = sum(1 for row in rows if row["fault"])
    lines.insert(2, f"Injected faults: {total_faults}. Caught: {found}.\n")

    with open(findings_path, "w") as f:
        f.write("\n".join(lines) + "\n\n## Full pySHACL report\n\n```\n" + results_text + "\n```\n")

    print(f"conforms={conforms}; caught {found}/{total_faults} injected faults; findings -> {findings_path}")


if __name__ == "__main__":
    main()
