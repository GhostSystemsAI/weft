"""Step 8: M1 to M6. Run from the repository root with the venv active and
SYSMLV2_CACHE_DIR set to a writable directory. Needs the sysmlv2 binary,
the SysML-v2-Release clone, and the step 3 to 7 artifacts already built
(spike/normative, spike/projection, spike/export, spike/shapes).

Usage: python3 spike/measure.py <toolkit-bin> <sysml-lib-dir> <out-dir>
"""
import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).parent.parent
VARIANTS = ["baseline", "rename", "insert", "move", "reorder", "extract"]


def element_ids(json_path):
    elements = json.load(open(json_path))
    return {e["elementId"] for e in elements}


def m1(toolkit, lib, out_dir):
    # IDS.md: a document's root id (and everything chained under it) derives
    # from "$root/" + source_name, where source_name is the path given on
    # the command line. Converting each variant from its own
    # spike/model/variants/<edit>/ directory would change every id on every
    # edit, including ones the edit never touched, because the source path
    # itself differs per variant -- measuring the edit's path churn, not the
    # edit's structural churn. This copies each variant's content over one
    # fixed set of file paths (a working directory) before converting, so
    # the source name is identical across every run and the id diff
    # isolates the edit.
    work_dir = out_dir / "m1-work"
    work_dir.mkdir(exist_ok=True)
    names = ("profile.sysml", "pump-library.sysml", "pump-system.sysml")
    work_paths = [work_dir / n for n in names]

    ids = {}
    for variant in VARIANTS:
        for n, wp in zip(names, work_paths):
            wp.write_text((REPO / f"spike/model/variants/{variant}/{n}").read_text())
        out = out_dir / f"m1-{variant}.json"
        subprocess.run(
            [toolkit, "convert", "--lib", lib, "--to", "full-json", *map(str, work_paths), "-o", str(out)],
            check=True,
        )
        ids[variant] = element_ids(out)

    baseline = ids["baseline"]
    rows = []
    for variant in VARIANTS[1:]:
        kept = baseline & ids[variant]
        changed = len(baseline) - len(kept)
        rows.append(
            {
                "edit": variant,
                "baseline_total": len(baseline),
                "variant_total": len(ids[variant]),
                "ids_unchanged": len(kept),
                "ids_changed_or_removed": changed,
                "pct_changed": round(100 * changed / len(baseline), 1),
            }
        )
    return rows


def m2(toolkit, lib, out_dir):
    # Two structurally identical projects under different package names.
    # IDS.md: a document root's id derives from "$root/" + source_name, the
    # path given on the command line, so two projects collide only if BOTH
    # their structure/names AND their relative source paths match. This
    # spike runs the toolkit from inside each project's own directory with
    # bare relative filenames as arguments (the natural case: two adopters
    # each naming their file e.g. "pump-library.sysml" at their repo root),
    # so source_name is the literal string "pump-library.sysml" for both --
    # isolating whether same-structure-different-package-name alone
    # collides, independent of the path-naming effect M1 controls for.
    a_dir = out_dir / "m2-project-a"
    b_dir = out_dir / "m2-project-b"
    a_dir.mkdir(exist_ok=True)
    b_dir.mkdir(exist_ok=True)

    base_library = (REPO / "spike/model/pump-library.sysml").read_text()
    base_system = (REPO / "spike/model/pump-system.sysml").read_text()
    profile = (REPO / "spike/model/profile.sysml").read_text()

    (a_dir / "profile.sysml").write_text(profile)
    (b_dir / "profile.sysml").write_text(profile)
    (a_dir / "pump-library.sysml").write_text(base_library.replace("PumpLibrary", "ProjectALibrary"))
    (b_dir / "pump-library.sysml").write_text(base_library.replace("PumpLibrary", "ProjectBLibrary"))
    (a_dir / "pump-system.sysml").write_text(
        base_system.replace("PumpSystemModel", "ProjectASystem").replace("PumpLibrary", "ProjectALibrary")
    )
    (b_dir / "pump-system.sysml").write_text(
        base_system.replace("PumpSystemModel", "ProjectBSystem").replace("PumpLibrary", "ProjectBLibrary")
    )

    out_a = (out_dir / "m2-a.json").resolve()
    out_b = (out_dir / "m2-b.json").resolve()
    subprocess.run(
        [toolkit, "convert", "--lib", lib, "--to", "full-json",
         "profile.sysml", "pump-library.sysml", "pump-system.sysml", "-o", str(out_a)],
        check=True, cwd=a_dir,
    )
    subprocess.run(
        [toolkit, "convert", "--lib", lib, "--to", "full-json",
         "profile.sysml", "pump-library.sysml", "pump-system.sysml", "-o", str(out_b)],
        check=True, cwd=b_dir,
    )
    ids_a = element_ids(out_a)
    ids_b = element_ids(out_b)
    return {
        "project_a_total": len(ids_a),
        "project_b_total": len(ids_b),
        "intersection": len(ids_a & ids_b),
    }


def m3(toolkit, lib, out_dir):
    original = REPO / "spike/model/pump-library.sysml"
    json_out = out_dir / "m3.json"
    text_out = out_dir / "m3-roundtrip.sysml"
    subprocess.run([toolkit, "convert", "--lib", lib, "--to", "compact-json", str(original), "-o", str(json_out)], check=True)
    result = subprocess.run(
        [toolkit, "convert", "--lib", lib, "--to", "text", "--min-qual", str(json_out), "-o", str(text_out)],
        capture_output=True, text=True,
    )
    original_text = original.read_text()
    roundtrip_text = text_out.read_text() if text_out.exists() else ""
    identical = original_text.strip() == roundtrip_text.strip()
    return {
        "convert_exit": result.returncode,
        "byte_identical": identical,
        "original_chars": len(original_text),
        "roundtrip_chars": len(roundtrip_text),
        "stderr": result.stderr.strip()[:2000],
    }


def m5(out_dir):
    import rdflib

    normative = rdflib.Graph()
    normative.parse(REPO / "spike/normative/output/pump-system.ttl", format="turtle")
    projection = rdflib.Graph()
    projection.parse(REPO / "spike/projection/output.ttl", format="turtle")

    rows = []
    for rq in sorted((REPO / "queries").glob("*.rq")):
        text = rq.read_text()
        proj_patterns = text.count(".") + text.count(";")  # rough proxy, replaced below
        proj_result = list(projection.query(text))
        rows.append({"query": rq.name, "projection_rows": len(proj_result)})
    return rows


def main():
    toolkit, lib, out_dir = sys.argv[1], sys.argv[2], Path(sys.argv[3])
    out_dir.mkdir(parents=True, exist_ok=True)

    print("## M1\n", m1(toolkit, lib, out_dir))
    print("## M2\n", m2(toolkit, lib, out_dir))
    print("## M3\n", m3(toolkit, lib, out_dir))
    print("## M5\n", m5(out_dir))


if __name__ == "__main__":
    main()
