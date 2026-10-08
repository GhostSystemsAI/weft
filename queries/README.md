# Thread queries

The five SPARQL queries in this directory are the specification for spike 1, step 4 ([zwelz3/weft#2](https://github.com/zwelz3/weft/issues/2)), and for the projection. They are taken from the requirements traceability matrix and the gap analysis in [docs/plans/adopter-capabilities.md](../docs/plans/adopter-capabilities.md), so the spike measures the projection against the queries the adopter runs.

| File | Report | Question |
|---|---|---|
| [requirement-satisfied-by.rq](requirement-satisfied-by.rq) | Traceability matrix | Which elements satisfy each requirement, with the `verify` verdict for each claim |
| [requirement-verified-by.rq](requirement-verified-by.rq) | Traceability matrix | Which verification cases verify each requirement |
| [unsatisfied-requirements.rq](unsatisfied-requirements.rq) | Gap analysis | Which requirements have no satisfying element |
| [unverified-requirements.rq](unverified-requirements.rq) | Gap analysis | Which requirements have no verification case |
| [orphan-components.rq](orphan-components.rq) | Gap analysis | Which components no requirement concerns |

Each file states, in its header comment, the question it answers, the projection terms it assumes, and its expected columns. The `proj:` namespace and the terms in it are placeholders, because the projection vocabulary is open (OQ10).

The queries are untested until [docs/graph-contract.md](../docs/graph-contract.md) exists past its skeleton and fixes the projection terms. Spike 1 fills the contract, and a test then runs each query against the corpus.
