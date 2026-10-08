"""Regression fence for step 7: a boundary shape whose sh:targetClass
matches nothing in the interior must not be reported as a validating pass
in the same breath as a shape that actually fired. This guards the finding
BACKENDS.md records (the normative holon's True conforms is vacuous).
Run directly: cd spike/holons && python3 -m pytest test_load_holons.py
"""
import holonic

NS = "https://weft.ghostsystems.ai/spike1/holons-test/"


def test_vacuous_boundary_conforms_but_fires_no_shape():
    ds = holonic.HolonicDataset()
    holon = NS + "holon/empty-target"
    ds.add_holon(holon, "test holon")
    ds.add_interior(holon, f"<{NS}instance/thing> a <{NS}class/Unrelated> .")
    ds.add_boundary(
        holon,
        f"""
        @prefix sh: <http://www.w3.org/ns/shacl#> .
        <{NS}shape/Thing> a sh:NodeShape ;
            sh:targetClass <{NS}class/Thing> ;
            sh:property [ sh:path <{NS}property/required> ; sh:minCount 1 ] .
        """,
    )
    result = ds.validate_membrane(holon)
    assert result.conforms is True
    assert result.violations == []
    # Conforms is true only because no node in the interior is typed
    # NS:class/Thing; it is not evidence the required-property shape ran.


def test_matching_boundary_actually_catches_a_missing_required_property():
    ds = holonic.HolonicDataset()
    holon = NS + "holon/matching-target"
    ds.add_holon(holon, "test holon")
    ds.add_interior(holon, f"<{NS}instance/thing> a <{NS}class/Thing> .")
    ds.add_boundary(
        holon,
        f"""
        @prefix sh: <http://www.w3.org/ns/shacl#> .
        <{NS}shape/Thing> a sh:NodeShape ;
            sh:targetClass <{NS}class/Thing> ;
            sh:property [ sh:path <{NS}property/required> ; sh:minCount 1 ; sh:severity sh:Violation ] .
        """,
    )
    result = ds.validate_membrane(holon)
    assert result.conforms is False
    assert len(result.violations) >= 1
