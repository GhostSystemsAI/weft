# Step 2 check

Command, run from the repository root with `SYSMLV2_CACHE_DIR=/tmp/spike1-toolkit/cache` set to a
writable directory (the default `~/.cache` is read-only in this environment):

```
sysmlv2 check --strict --lib /tmp/spike1-sysml-release/sysml.library \
  spike/model/profile.sysml spike/model/pump-system.sysml
```

Output: none on stdout or stderr. Exit status 0.

## Model contents

`spike/model/profile.sysml`: the stand-in profile, three `metadata def`s (`Component`, with the
required `bearer` feature mirroring decision 0005; `Interface`, mirroring decision 0006; `Process`,
mirroring decision 0007) and the `BearerKind` enumeration.

`spike/model/pump-system.sysml`: a pump system with

- 5 part definitions: `PumpSystem`, `Pump`, `Controller`, `PressureSensor`, `Enclosure`, each
  carrying `@Component`.
- 2 interface/port definitions: `PowerPort` (`port def`) and `DataLink` (`interface def`), each
  carrying `#Interface`.
- 1 action definition: `MonitorPressure`, carrying `#Process`.
- 6 requirements, each with a declared short name (`REQ-001` to `REQ-006`): `MaxPressure`,
  `ResponseTime`, `PowerDraw`, `DataLatency`, `EnclosureRating`, `StartupTime`.
- 6 `satisfy` claims, one per requirement, naming `pumpSystemUnderTest` or one of its parts as the
  satisfying element.
- 1 verification case (`PumpSystemAcceptance` def, `pumpSystemAcceptanceTest` usage) with a
  `verify` relationship for each of the two requirements it covers (`MaxPressure`, `ResponseTime`).

## Public model

`sysml/src/examples/Geometry Examples/SimpleQuadcopter.sysml` in the SysML-v2-Release clone at
`/tmp/spike1-sysml-release/`, used for step 3's second graph and measurement M2. The Annex A
`SimpleVehicleModel.sysml` was tried first and rejected: `sysmlv2 check --lib` reports 17 errors
against it (ambiguous references such as `ignitionCmdPort` and `vehicleToRoadPort` resolving to
multiple memberships), a toolkit/spec-vintage mismatch unrelated to this spike. `SimpleQuadcopter.sysml`
and three validation-suite files (`1a-Parts Tree.sysml`, `8-Requirements.sysml`,
`2a-Parts Interconnection.sysml`) were tried and all pass `check --strict --lib` cleanly;
`SimpleQuadcopter.sysml` was kept because it has part definitions, ports, and connections.
