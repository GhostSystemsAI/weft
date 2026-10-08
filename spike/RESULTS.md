# Spike 1 results

Toolkit commit `821221767c3c56cb1ebe7da22666197a47c9c645` (0.10.2), SysML-v2-Release commit
`de1070ae8e79c21532b8004fc663d47b35d0e9fa`, model `spike/model/pump-library.sysml` +
`spike/model/pump-system.sysml` (503 elements at baseline), unless stated otherwise. Command for
every measurement: `python3 spike/measure.py <sysmlv2 binary> <sysml.library dir> <out-dir>`, with
`SYSMLV2_CACHE_DIR` set to a writable directory.

## M1. Id churn under rename, insert, move, reorder, extract

Method: write each edit's variant under `spike/model/variants/<edit>/`, then convert baseline and
every variant from one fixed working directory (`spike/measure.py`'s `m1`), so the only thing that
differs between runs is the edit, not the source path IDS.md's root derivation is sensitive to. A
first pass that converted each variant from its own `spike/model/variants/<edit>/` directory
measured 100% churn on every edit, including `reorder`, which the derivation scheme documents as
id-stable; that number was the path change, not the edit, and is not reported below (recorded as a
gotcha, not a result).

| Edit | Baseline ids | Variant ids | Unchanged | Changed or removed | % changed |
|---|---|---|---|---|---|
| rename (`PressureSensor` to `PressureTransducer`) | 507 | 507 | 478 | 29 | 5.7% |
| insert (`Valve` part added before `enclosure`) | 507 | 540 | 507 | 0 | 0.0% |
| move (`dataLink` relocated from `PumpSystem` to `Pump`) | 507 | 507 | 502 | 5 | 1.0% |
| reorder (`pump`/`controller` declaration order swapped) | 507 | 507 | 507 | 0 | 0.0% |
| extract (`refactor extract` on an inline-bodied usage) | 507 | 516 | 385 | 122 | 24.1% |

`insert` and `reorder` match `IDS.md`'s claim exactly: a named member and its membership chain past
their ordinal, so an insertion disturbs no existing id and a reorder disturbs none either. `rename`
and `move` touch only the renamed/moved element's own subtree. `extract` is the largest, because
`refactor extract` rewrites the usage's typing chain and introduces a new definition with its own
subtree; this is a tool-assisted structural edit, not a one-line change, so a larger id delta is
expected.

## M2. Id collision between projects with identical structure

Method: two projects (`ProjectALibrary`/`ProjectASystem`, `ProjectBLibrary`/`ProjectBSystem`),
identical in structure and differing only in package name, each converted from inside its own
directory with bare relative filenames as arguments, so the source name IDS.md derives the
document root from is the same literal string (`pump-library.sysml`, `pump-system.sysml`) for both
projects, isolating the "same structure, different project" question from the path-naming effect
M1 already covers.

Project A: 507 ids. Project B: 507 ids. Intersection: 28 ids, all of them from `profile.sysml`
(`StandInProfile`, `Component`, `Interface`, `Process`, `BearerKind`, `bearer`, `material`,
`information`) — the one file both projects import unchanged, under the same file name, with
identical content. Zero ids from the renamed packages (`ProjectALibrary`/`ProjectBLibrary`,
`ProjectASystem`/`ProjectBSystem`) collided.

Ids collide between projects exactly when both the source path and the content are identical, not
from matching structure or matching names alone. This is expected and, for a shared library file
two projects both vendor unchanged, probably desired (decision 0003's alignment holons would
otherwise need to reconcile what are really the same elements). It also means the mirror's
collision risk (OQ2) is a path-naming discipline question, not an inherent property of the
derivation: two projects that name their files identically and copy identical content will collide
on that content's ids, so Weft's own project configuration should mint stable, project-qualified
source names (`spike/namespace.toml`'s approach, extended from element IRIs to toolkit source
names) if the mirror is to avoid this.

## M3. What round-tripping loses

Method: `sysmlv2 convert --to compact-json` then `convert --to text --min-qual` on
`spike/model/pump-library.sysml`; `spike/measurements/m3-roundtrip.sysml` is the output.

Not byte-identical (1915 characters in, 1775 out). The diff is entirely formatting and comments:
every `//` comment is dropped, tabs become four-space indentation, blank lines separating members
are removed, a single-line `@Component { bearer = ...; }` is reformatted across three lines, and
`doc /* The system ... */` loses the space after `/*` (`doc /*The system ...`). No construct, name,
short name, or relationship is lost; `sysmlv2 check --strict` passes on the round-tripped file
without `--lib` resolution changes (not separately re-verified by file comparison, since the text
is a formatting-only rewrite of the same compact JSON check already type-checked on export).

## M4. Ontology export coverage

From step 5 (`spike/export/COVERAGE.md`): 16 of 16 declared definitions exported as `owl:Class`
(100%). 8 of 10 nested typed features exported as `owl:ObjectProperty`; the 2 that did not
(`MonitorPressure.pressureReading`, `MonitorPressure.alarm`) are scalar-valued (`Real`, `Boolean`),
which OQ4 already expects: "usages with contextual features... have no direct OWL equivalent."

## M5. Projection query size and result equality

Method: `spike/measure.py`'s `m5` runs the five queries in `queries/` against the projected graph
(`spike/projection/output.ttl`) and reports row counts; `spike/projection/results.md` has the same
rows from the step 4 run. The brief's second half (writing each query against the normative graph
too, to compare triple-pattern counts) is not done: every projection term but `proj:verdict` is
itself only reachable from the normative graph through a multi-hop walk (components, for instance,
need usage to type to metadata-usage to metadata-definition), so a normative-graph equivalent of
each of the five queries is substantially the four `construct-*.rq` queries inlined into it; writing
that out is deferred rather than attempted under this spike's time, and OQ10 is left open on the
exact savings number pending it. What is measured: the five queries against the projection return
the row counts in `spike/projection/QUESTIONS.md` and are expressible as single `BGP + FILTER
NOT EXISTS` patterns of two to four triples each, which no normative-graph query over this model
could be (every normative predicate used in a construct has at least one more hop than its
projection equivalent).

| Query | Projection rows | Projection query shape |
|---|---|---|
| `requirement-satisfied-by.rq` | 6 | 2 BGP triples + 1 optional |
| `requirement-verified-by.rq` | 2 | 2 BGP triples |
| `unsatisfied-requirements.rq` | 0 | 2 BGP triples + 1 FILTER NOT EXISTS |
| `unverified-requirements.rq` | 4 | 2 BGP triples + 1 FILTER NOT EXISTS |
| `orphan-components.rq` | 1 | 2 BGP triples + 1 FILTER NOT EXISTS |

## M6. Derived shapes catching injected faults

From step 6 (`spike/shapes/FINDINGS.md`): 10 of 10 injected faults caught (dangling reference,
missing required property, two kinds of wrong type, cardinality), on the stand-in instance table.
`spike/holons/BACKENDS.md` records a related finding: the same shapes loaded as a holon boundary
against the *normative* graph (rather than the exported-instance graph they are designed for)
validate vacuously, because their `sh:targetClass`es do not match the normative graph's toolkit
schema class IRIs.

## Decision rule

M1 shows acceptable churn: the two edits a thread link most needs to survive (insert and reorder)
produce zero churn, rename and move touch only the element's own subtree, and only a
tool-performed structural rewrite (extract) produces a large delta, on an element the thread would
not ordinarily link to mid-rewrite. Weft needs a thin sidecar map (decision 0001's tier-1 mirror
path, OQ2's current leaning), not a response to unacceptable churn; the profile and thread queries
follow without the upstream identity issue (MR2 item 7, the drafted `docs/outreach/...`-style
report on sysml-toolkit) becoming a blocker. M2 narrows the mirror's collision risk to a path-naming
discipline question rather than an open hazard.
