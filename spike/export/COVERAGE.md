# Step 5 export coverage

16 definitions declared, 16 exported as `owl:Class`.

| Metaclass | Name | Exported as |
|---|---|---|
| EnumerationDefinition | BearerKind | owl:Class |
| MetadataDefinition | Component | owl:Class |
| MetadataDefinition | Interface | owl:Class |
| MetadataDefinition | Process | owl:Class |
| PortDefinition | PowerPort | owl:Class |
| ConjugatedPortDefinition | ~PowerPort | owl:Class |
| InterfaceDefinition | DataLink | owl:Class |
| ActionDefinition | MonitorPressure | owl:Class |
| PartDefinition | PumpSystem | owl:Class |
| PartDefinition | Pump | owl:Class |
| PartDefinition | Controller | owl:Class |
| PartDefinition | PressureSensor | owl:Class |
| PartDefinition | Enclosure | owl:Class |
| RequirementDefinition | MaxPressureDef | owl:Class |
| RequirementDefinition | ResponseTimeDef | owl:Class |
| VerificationCaseDefinition | PumpSystemAcceptance | owl:Class |
| FeatureMembership | Component.bearer | owl:ObjectProperty |
| FeatureMembership | PumpSystem.pump | owl:ObjectProperty |
| FeatureMembership | PumpSystem.controller | owl:ObjectProperty |
| FeatureMembership | PumpSystem.sensor | owl:ObjectProperty |
| FeatureMembership | PumpSystem.enclosure | owl:ObjectProperty |
| FeatureMembership | PumpSystem.powerIn | owl:ObjectProperty |
| FeatureMembership | PumpSystem.dataLink | owl:ObjectProperty |
| FeatureMembership | Pump.powerPort | owl:ObjectProperty |
| FeatureMembership | Controller.dataPort | owl:ObjectProperty |

## Not exported

| Metaclass | Identifier | Why |
|---|---|---|
| FeatureMembership | MonitorPressure.pressureReading | feature's type is not an exported class (scalar-valued or untyped) |
| FeatureMembership | MonitorPressure.alarm | feature's type is not an exported class (scalar-valued or untyped) |
