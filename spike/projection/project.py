"""Build the projection graph from the pump-system normative graph and run
the five thread queries against it. Usage:

    python3 project.py <normative.ttl> <verify.txt> <out-projection.ttl> <queries-dir>

<verify.txt> is the captured stdout of
`sysmlv2 verify --lib <lib> spike/model/profile.sysml spike/model/pump-system.sysml`.
"""
import re
import sys
from pathlib import Path

from rdflib import Graph, Namespace, Literal

HERE = Path(__file__).parent

PROJ = Namespace("https://weft.ghostsystems.ai/thread/0.1.0/")
TK = Namespace("https://weft.ghostsystems.ai/spike1/toolkit-vocab#")

VERIFY_LINE = re.compile(
    r"\(SatisfyRequirementUsage, satisfies \S+::(?P<req>\w+) by (?P<elem>\S+)\): (?P<verdict>\w+)"
)


def build_projection(normative_ttl):
    g = Graph()
    g.parse(normative_ttl, format="turtle")

    projection = Graph()
    for construct_file in sorted(HERE.glob("construct-*.rq")):
        query = construct_file.read_text()
        for triple in g.query(query):
            projection.add(triple)
    return g, projection


def attach_verdicts(normative, projection, verify_text):
    # Match each verify report line to its SatisfyClaim by the requirement's
    # declaredName and the satisfying element's reference text (the report
    # names elements by qualified reference, not by elementId, since verify
    # works over the textual model directly).
    name_to_req = {}
    for s, _, o in normative.triples((None, None, None)):
        pass
    q = """
    PREFIX sysml: <https://www.omg.org/spec/SysML/20250201/>
    PREFIX tk: <https://weft.ghostsystems.ai/spike1/toolkit-vocab#>
    SELECT ?claim ?reqName ?elemRef WHERE {
      ?claim a sysml:SatisfyRequirementUsage ;
             tk:satisfiedRequirement ?req ;
             tk:satisfyingFeature ?elem .
      ?req tk:declaredName ?reqName .
      OPTIONAL { ?elem tk:declaredName ?elemName }
      BIND(COALESCE(?elemName, "") AS ?elemRef)
    }
    """
    claims_by_req = {}
    for row in normative.query(q):
        claims_by_req.setdefault(str(row.reqName), []).append(str(row.claim))

    for line in verify_text.splitlines():
        m = VERIFY_LINE.search(line)
        if not m:
            continue
        req_name = m.group("req")
        verdict = m.group("verdict").lower()
        for claim_iri in claims_by_req.get(req_name, []):
            projection.add((__import__("rdflib").URIRef(claim_iri), PROJ.verdict, Literal(verdict)))


def run_queries(projection, queries_dir, out_path):
    lines = []
    for rq_file in sorted(Path(queries_dir).glob("*.rq")):
        text = rq_file.read_text()
        header = "\n".join(l for l in text.splitlines() if l.startswith("#"))
        lines.append(f"## {rq_file.name}\n")
        try:
            results = list(projection.query(text))
        except Exception as e:
            lines.append(f"ERROR: {e}\n")
            continue
        lines.append(f"{len(results)} row(s)\n")
        for row in results:
            lines.append("  " + " | ".join(str(v) for v in row))
        lines.append("")
    out_path.write_text("\n".join(lines))
    return lines


def main():
    normative_ttl, verify_txt, out_ttl, queries_dir = sys.argv[1:5]
    normative, projection = build_projection(normative_ttl)
    attach_verdicts(normative, projection, Path(verify_txt).read_text())
    projection.serialize(destination=out_ttl, format="turtle")
    results_path = Path(out_ttl).parent / "results.md"
    lines = run_queries(projection, queries_dir, results_path)
    print(f"projection: {len(projection)} triples -> {out_ttl}")
    print(f"results -> {results_path}")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
