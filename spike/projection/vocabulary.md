# Projection vocabulary, spike 1 draft

Namespace: `https://weft.ghostsystems.ai/thread/0.1.0/` (prefix `proj:`), versioned in its path so
a future incompatible change to the vocabulary mints a new namespace rather than silently
reinterpreting old data under the same IRIs (mirrors the contract's own versioning, below).

| Term | Kind | Range | Derived from (normative graph) |
|---|---|---|---|
| `proj:Requirement` | Class | | `sysml:RequirementUsage` with a non-null `tk:declaredShortName` |
| `proj:Component` | Class | | `sysml:PartUsage` with a declared short name, whose `tk:type` is annotated by the `Component` metadata definition (decision 0005) |
| `proj:shortName` | Datatype property | `xsd:string` | `tk:declaredShortName` |
| `proj:SatisfyClaim` | Class | | `sysml:SatisfyRequirementUsage` |
| `proj:requirement` | Object property | `proj:Requirement` | `tk:satisfiedRequirement` |
| `proj:satisfiedBy` | Object property | `proj:Component` (in this model; the toolkit does not restrict a `satisfy` claim's satisfying element to a component) | `tk:satisfyingFeature` |
| `proj:verdict` | Datatype property | `xsd:string`, one of `"satisfied"`, `"violated"`, `"undecided"` | `sysmlv2 verify`'s text report, parsed and matched to its `proj:SatisfyClaim` by the requirement and satisfying-element names in the report line (not a graph pattern; see below) |
| `proj:verifiedBy` | Object property | `proj:VerificationCase` | `sysml:RequirementVerificationMembership.tk:verifiedRequirement`, restricted to memberships whose target has a declared short name, with the verification case found by walking `owningType` to the objective's owner |
| `proj:VerificationCase` | Class | | `sysml:VerificationCaseUsage` reached as above |

## Deriving `proj:verdict`

The other six terms are each one SPARQL CONSTRUCT query over the normative graph
(`construct-requirements.rq`, `construct-components.rq`, `construct-satisfy.rq`,
`construct-verified-by.rq`). `proj:verdict` is not: `sysmlv2 verify` is a separate evaluation over
the textual model, not a property the JSON export carries, and the 0.10.2 CLI has no `--format
json` option for `verify` (unlike `check` and `lint`). `project.py` runs `sysmlv2 verify` and
parses its text report (one line per claim, `satisfies <Requirement> by <element>: <verdict>`),
matching each line to a `proj:SatisfyClaim` individual by the requirement's qualified name and the
satisfying element's reference text. This is a narrowing a production derivation should close
either by asking the toolkit for a structured `verify` report or by deriving the verdict from the
same constraint-evaluation logic over the graph, not by re-parsing CLI text; it is recorded against
OQ6 in `docs/OPEN-QUESTIONS.md`.

## Versioning of the contract

The graph contract, including this vocabulary, is version 0.1.0 as of this spike. A change to a
minted IRI, an emitted class, a property's range, or the ordered-property representation is a data
migration for every user regardless of the package version (AGENTS.md rule 3), so the contract's
own version increments on any such change, independent of `weft`'s package version. 0.1.0 marks the
first version with content; nothing precedes it to be compared against.
