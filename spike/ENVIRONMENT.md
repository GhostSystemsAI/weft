# Spike 1 environment

Disposable code and records for spike 1. Nothing under `spike/` is part of the `weft` package.

## Toolkit

sysml-toolkit 0.10.2, commit `821221767c3c56cb1ebe7da22666197a47c9c645`. Fetched the prebuilt binary
`sysmlv2-0.10.2-x86_64-unknown-linux-gnu.tar.gz` and `SHA256SUMS` from the GitHub release page into
`/tmp/spike1-toolkit/`. The archive's SHA-256 matched the published sum
(`cfa5a8e37cc1b427c82cdc51515fc5821bdcdd70e5f4d2095a7460f3520ba4c1`). Rust was not needed: the
release ships a working `sysmlv2` CLI binary with `convert --to full-json` for element ids with
derived properties and implied relationships, `check --strict`, `lint`, `verify`, and `describe`.
The binary is an ELF 64-bit executable; no build step ran.

A source clone of the toolkit at the same commit lives at `/tmp/spike1-toolkit-src/`, used only to
read `IDS.md` for the id-derivation scheme. The toolkit vendors SysML-v2-Release as the submodule
`spec-refs/SysML-v2-Release`, cloned separately for this spike (its remote is
`https://github.com/Systems-Modeling/SysML-v2-Release`, not `Open-MBEE/SysML-v2-Release`, which
does not exist) into `/tmp/spike1-sysml-release/`, checked out at `de1070ae8e79c21532b8004fc663d47b35d0e9fa`
per decision 0002.

## Id schemes offered

Per `IDS.md`, the toolkit derives every non-root user element's id as `uuid5(parent id, segment)`,
chained from the document root. Two graph formats exist in the Rust API: `GraphFormat::LegacyV2`
(scheme 2, the default) and `GraphFormat::CanonicalV3` (scheme 3, opt-in, exposed only through
`Model::with_graph_format` / `Session::from_sources_with_graph_format`). The 0.10.2 CLI's `convert`
command takes no flag to select a graph format, so the CLI always emits scheme 2. Measurement M1
and M2 (step 8) therefore report one scheme, not several; this narrows OQ2's framing of "per scheme
the CLI offers" to the single scheme the CLI exposes.

## Public model

`sysml/src/examples/Vehicle Example/SysML v2 Spec Annex A SimpleVehicleModel.sysml` and its sibling
units (`VehicleDefinitions.sysml`, `VehicleUsages.sysml`, `VehicleIndividuals.sysml`) in the release
clone, used as the public model required by step 2.

## Python environment

venv at `/tmp/spike1-venv/`, Python 3.12.3.

| Package | Version |
|---|---|
| rdflib | 7.6.0 |
| pyshacl | 0.40.1 |
| pytest | 9.1.1 |
| holonic | 0.9.0.dev0, installed from `git+https://github.com/zwelz3/holonic@d8d1758` per this brief |

holonic's commit here (`d8d1758752827c35fc6781e89e01557b6e5e1825`) is the one this brief specifies
and matches the "first reviewed" commit in decision 0003, not the `25d1c84` commit that decision
pins for the Weft package proper. Step 7 notes where this matters.
