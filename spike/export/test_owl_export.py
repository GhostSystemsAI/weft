"""Regression fence for step 5: a definition with no declaredName must not
mint a class, and a feature typed by a scalar (no exported class target)
must not mint an owl:ObjectProperty with a dangling range. Run directly:

    cd spike/export && python3 -m pytest test_owl_export.py
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from rdflib import Graph, OWL, RDF

import owl_export

BASE = "https://weft.ghostsystems.ai/spike1/test-library/"


def _run(tmp_path, elements):
    json_path = tmp_path / "in.json"
    json_path.write_text(json.dumps(elements))
    out_ttl = tmp_path / "out.ttl"
    coverage = tmp_path / "COVERAGE.md"
    sys.argv = ["owl_export.py", str(json_path), BASE, str(out_ttl), str(coverage)]
    owl_export.main()
    g = Graph()
    g.parse(out_ttl, format="turtle")
    return g, coverage.read_text()


def test_definition_without_declared_name_mints_no_class(tmp_path):
    elements = [
        {"@id": "a", "@type": "PartDefinition", "declaredName": "Named"},
        {"@id": "b", "@type": "PartDefinition", "declaredName": None},
    ]
    g, coverage = _run(tmp_path, elements)
    classes = {str(o) for o in g.subjects(RDF.type, OWL.Class)}
    assert classes == {BASE + "class/Named"}
    assert "no declaredName" in coverage


def test_scalar_typed_feature_exports_no_object_property(tmp_path):
    elements = [
        {"@id": "owner", "@type": "PartDefinition", "declaredName": "Owner"},
        {
            "@id": "fm",
            "@type": "FeatureMembership",
            "owningType": {"@id": "owner"},
            "ownedMemberElement": {"@id": "feat"},
            "memberName": "count",
        },
        {"@id": "feat", "@type": "PartUsage", "declaredName": "count", "type": [{"@id": "Real"}]},
    ]
    g, coverage = _run(tmp_path, elements)
    assert len(list(g.subjects(RDF.type, OWL.ObjectProperty))) == 0
    assert "not an exported class" in coverage
