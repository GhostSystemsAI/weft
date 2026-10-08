# Working rules

Invariants for any session on this repository. Read [STATUS.md](STATUS.md) first for the current state and open work, then [README.md](README.md), the records in [docs/decisions/](docs/decisions/), and [docs/OPEN-QUESTIONS.md](docs/OPEN-QUESTIONS.md) before proposing a design change. A session that changes the project's state updates STATUS.md before it ends.

## Invariants

1. **Git is the record.** Decision 0001 places the authoritative model in git and makes Flexo MMS an optional one-way mirror. Every core feature works on a git checkout without network access. A feature that requires a server is an addition at tier 1 and is labeled as one.

2. **Natural language is not stored as specification.** Prompts that produce or edit the model are not records. The reasons behind a modeling choice go into a decision record linked to the elements it concerns, because the prompt that carried them is not kept.

3. **The graph contract is a migration surface.** The IRIs Weft mints, the triples it emits, and each property's range are a data migration for every user when they change, independent of the version number. A change to emitted triples is not an ordinary change even though the version is pre-1.0.

4. **IRIs are minted only into namespaces their owner controls.** A project's elements are minted under that project's namespace, and a library's classes under that library's namespace. Weft never invents a base on a user's behalf, and thread links never point at an identifier minted into a shared namespace, such as `urn:sysmlv2:element:`.

5. **Object properties are never emitted as literals.** Decide a property's range before emitting it. A link emitted as a string reduces traceability to string matching and contradicts any ontology that declares the property an object property.

6. **Metamodel well-formedness belongs to the SysML toolkit.** The SysML v2 specification states its well-formedness constraints in OCL, and sysml-toolkit implements and tests them. Weft runs the toolkit's checks on textual notation and does not reimplement those constraints in SHACL. Weft's SHACL covers project policy, profile rules, and instance data. The set of constraints the toolkit implements changes between releases, so this rule holds relative to the release pinned in decision 0002.

7. **A Violation-severity shape must be satisfiable through the primary authoring path.** Every property a shape requires at Violation severity is producible from SysML textual notation through Weft's derivation. Assert this in the test suite.

8. **Dogfood every item class.** Each element kind, stereotype, and link type Weft supports is exercised by a model in this repository, and a test asserts that the corpus uses each one.

9. **No network access at validation time.** Shapes, vocabularies, and libraries resolve from the installed package or the checkout.

10. **A record written before the work is a plan.** Changelog entries are written at release time, from what shipped.

11. **Agents do not claim authorship.** The person directing the work is the commit author. An agent does not set itself as author or co-author, and commit messages and pull or merge request bodies carry no AI attribution (no `Co-Authored-By` trailer naming a model, no session link, no "Generated with" footer). Agent tools add such trailers by default, so the override is part of the repository: Claude Code's trailer is turned off by the checked-in `.claude/settings.json` (`includeCoAuthoredBy: false`). An agent run with another tool turns off the equivalent before its first commit.

12. **Dependencies off PyPI are pinned by commit.** Every dependency resolved from source (sysml-toolkit, its vendored standard library, and holonic until a release carries the fixes Weft needs) is pinned by commit hash in the repository, and every row of the versions table in STATUS.md records the hash it was reviewed at.

## Style

Draft documents with the `better-language-skill` skill. The skill is not vendored in this repository, so the following rules stand in for it when it is unavailable. American English spelling. Section headings are sentences or noun phrases. No em-dashes for sentence flow. State material impersonally in documentation. Do not estimate work in calendar time. One claim per sentence. No hedging, filler, or rhetorical questions. Name the concrete thing (a file, a commit, an issue) rather than the category it belongs to. Lists only for parallel items; argument stays in prose.
