"""Regression fence for the step 3 design decisions in docs/graph-contract.md:
requirement short names mint under a distinct path from every other element,
and only ownedRelationship keeps its order as an rdf:List. Run directly
(not part of the weft package's pytest sweep):

    cd spike/normative && python3 -m pytest test_convert.py
"""
import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from rdflib import RDF
from rdflib.collection import Collection

import convert

NS_TOML = """
[proj]
base = "https://weft.ghostsystems.ai/spike1/test/"
requirement_mint_pattern = "{base}requirement/{short_name}"
element_mint_pattern = "{base}element/{element_id}"
"""


def _write(path, content):
    path.write_text(content)
    return path


def test_requirement_short_name_mints_separately_from_element_id(tmp_path):
    elements = [
        {
            "@id": "11111111-1111-1111-1111-111111111111",
            "@type": "RequirementUsage",
            "elementId": "11111111-1111-1111-1111-111111111111",
            "declaredShortName": "REQ-001",
        },
        {
            "@id": "22222222-2222-2222-2222-222222222222",
            "@type": "PartUsage",
            "elementId": "22222222-2222-2222-2222-222222222222",
            "declaredShortName": None,
        },
    ]
    json_path = _write(tmp_path / "in.json", json.dumps(elements))
    ns_path = _write(tmp_path / "ns.toml", NS_TOML)
    out_path = tmp_path / "out.ttl"

    sys.argv = ["convert.py", str(json_path), "proj", str(ns_path), str(out_path)]
    convert.main()

    text = out_path.read_text()
    assert "requirement/REQ-001" in text
    assert "element/22222222-2222-2222-2222-222222222222" in text
    assert "element/11111111" not in text  # the requirement did not mint from its id


def test_owned_relationship_is_an_rdf_list_and_other_multivalued_props_are_not(tmp_path):
    elements = [
        {
            "@id": "a",
            "@type": "Feature",
            "elementId": "a",
            "ownedRelationship": [{"@id": "r0"}, {"@id": "r1"}],
            "chainingFeature": [{"@id": "r0"}, {"@id": "r1"}],
        },
        {"@id": "r0", "@type": "FeatureMembership", "elementId": "r0"},
        {"@id": "r1", "@type": "FeatureMembership", "elementId": "r1"},
    ]
    json_path = _write(tmp_path / "in.json", json.dumps(elements))
    ns_path = _write(tmp_path / "ns.toml", NS_TOML)
    out_path = tmp_path / "out.ttl"

    sys.argv = ["convert.py", str(json_path), "proj", str(ns_path), str(out_path)]
    convert.main()

    from rdflib import Graph

    g = Graph()
    g.parse(out_path, format="turtle")

    subj = convert.URIRef("https://weft.ghostsystems.ai/spike1/test/element/a")
    owned = list(g.objects(subj, convert.PROP["ownedRelationship"]))
    assert len(owned) == 1  # one rdf:List head, not two separate triples
    items = list(Collection(g, owned[0]))
    assert len(items) == 2

    chaining = list(g.objects(subj, convert.PROP["chainingFeature"]))
    assert len(chaining) == 2  # plain repeated triples, no list node
