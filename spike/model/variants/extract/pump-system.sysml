// Spike 1 model: a small pump system, exercising 3 to 5 part definitions,
// 2 port/interface definitions, 1 action definition, 6 requirements each
// with a short name, satisfy and verify relationships, and one verification
// case. Disposable spike code (AGENTS.md rule 8 applies to the real `weft`
// corpus, not to this package). Definitions live in pump-library.sysml
// (step 5); this package holds the usages.
package PumpSystemModel {
	private import PumpLibrary::*;

	part <'CMP-SYS'> pumpSystemUnderTest : PumpSystem;

	part def AuxiliaryPump :> Pump {
		doc /* Spare pump kept for redundancy; extracted to its own definition by M1's extract edit. */
	}
	part auxiliaryPump : AuxiliaryPump;

	verification pumpSystemAcceptanceTest : PumpSystemAcceptance {
		subject testSystem : PumpSystem = pumpSystemUnderTest;
		objective testObjective {
			verify MaxPressure :>> acceptanceObjective.maxPressureVerdict;
			verify ResponseTime :>> acceptanceObjective.responseTimeVerdict;
		}
	}

	requirement <'REQ-001'> MaxPressure : MaxPressureDef;

	requirement <'REQ-002'> ResponseTime : ResponseTimeDef;

	requirement <'REQ-003'> PowerDraw {
		doc /* The pump shall draw no more than 500 W at rated flow. */
		subject pumpPart : Pump;
	}

	requirement <'REQ-004'> DataLatency {
		doc /* The controller's data link shall report sensor readings within 50 ms. */
		subject controllerPart : Controller;
	}

	requirement <'REQ-005'> EnclosureRating {
		doc /* The enclosure shall meet an IP65 ingress rating. */
		subject enclosurePart : Enclosure;
	}

	requirement <'REQ-006'> StartupTime {
		doc /* The system shall reach a ready state within 5 s of power-on. */
		subject system : PumpSystem;
	}

	satisfy MaxPressure by pumpSystemUnderTest;
	satisfy ResponseTime by pumpSystemUnderTest;
	satisfy PowerDraw by pumpSystemUnderTest.pump;
	satisfy DataLatency by pumpSystemUnderTest.controller;
	satisfy EnclosureRating by pumpSystemUnderTest.enclosure;
	satisfy StartupTime by pumpSystemUnderTest;
}
