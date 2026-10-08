"""Regression fence for step 6: a class annotated by a metadata definition
must inherit that definition's property shapes onto its own NodeShape (the
derivation decision shacl_export.py documents), and a class with no
annotation must not pick up a stray property shape. Run directly:

    cd spike/shapes && python3 -m pytest test_shacl_export.py
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from rdflib import Graph, SH, URIRef

import shacl_export

BASE = "https://weft.ghostsystems.ai/spike1/test-library/"


def _elements():
    return [
        {"@id": "stereotype", "@type": "MetadataDefinition", "declaredName": "Stamped"},
        {
            "@id": "stereotype-fm",
            "@type": "FeatureMembership",
            "owningType": {"@id": "stereotype"},
            "ownedMemberElement": {"@id": "stamp-feature"},
            "memberName": "stamp",
        },
        {"@id": "stamp-feature", "@type": "ReferenceUsage", "declaredName": "stamp", "type": [{"@id": "stereotype"}]},
        {"@id": "annotated", "@type": "PartDefinition", "declaredName": "Annotated"},
        {"@id": "plain", "@type": "PartDefinition", "declaredName": "Plain"},
        {
            "@id": "md-usage",
            "@type": "MetadataUsage",
            "type": [{"@id": "stereotype"}],
            "annotatedElement": [{"@id": "annotated"}],
        },
    ]


def test_annotated_class_inherits_metadata_property_shape(tmp_path):
    json_path = tmp_path / "in.json"
    json_path.write_text(json.dumps(_elements()))
    out_ttl = tmp_path / "shapes.ttl"
    sys.argv = ["shacl_export.py", str(json_path), BASE, str(out_ttl)]
    shacl_export.main()

    g = Graph()
    g.parse(out_ttl, format="turtle")

    annotated_shape = URIRef(f"{BASE}shape/Annotated")
    plain_shape = URIRef(f"{BASE}shape/Plain")

    annotated_props = set(g.objects(annotated_shape, SH.property))
    plain_props = set(g.objects(plain_shape, SH.property))

    assert len(annotated_props) == 1
    assert plain_props == set()  # Plain carries no metadata, so it inherits nothing
