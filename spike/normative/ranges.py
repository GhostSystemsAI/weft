"""Build a (metaclass, property) -> declared range map from the toolkit's
published KerML/SysML JSON Schema at the pinned commit. The schema's $ref
$comment on each array-item or oneOf branch names the metaclass the toolkit
declares as that property's range; convert.py uses this map to decide every
object property's range before emitting it (AGENTS.md rule 5), rather than
guessing from observed data.
"""
import json
import re

SCHEMA_FILES = [
    "/tmp/spike1-toolkit-src/spec-refs/KerML.schema.json",
    "/tmp/spike1-toolkit-src/spec-refs/SysML.schema.json",
]


def _range_from_node(node):
    if not isinstance(node, dict):
        return None
    comment = node.get("$comment")
    if comment:
        return comment.rsplit("/", 1)[-1]
    for key in ("oneOf", "anyOf"):
        for branch in node.get(key, []):
            r = _range_from_node(branch)
            if r:
                return r
    items = node.get("items")
    if items:
        return _range_from_node(items)
    return None


def build_range_map():
    """Returns {(metaclass, property): range_metaclass}, plus a
    property-name-only fallback map for properties whose range does not vary
    by owning metaclass."""
    per_class = {}
    by_name = {}
    for path in SCHEMA_FILES:
        defs = json.load(open(path))["$defs"]
        for cls, schema in defs.items():
            variants = schema.get("anyOf") or [schema]
            for variant in variants:
                props = variant.get("properties", {})
                for prop, node in props.items():
                    r = _range_from_node(node)
                    if r is None:
                        continue
                    per_class[(cls, prop)] = r
                    by_name.setdefault(prop, set()).add(r)
    return per_class, by_name


if __name__ == "__main__":
    per_class, by_name = build_range_map()
    print(f"{len(per_class)} (metaclass, property) ranges from schema")
    multi = {k: v for k, v in by_name.items() if len(v) > 1}
    print(f"{len(multi)} properties whose range varies by owning metaclass")
