// Spike 1 model: a small pump system, exercising 3 to 5 part definitions,
// 2 port/interface definitions, 1 action definition, 6 requirements each
// with a short name, satisfy and verify relationships, and one verification
// case. Disposable spike code (AGENTS.md rule 8 applies to the real `weft`
// corpus, not to this package).
package PumpSystemModel {
	private import ScalarValues::*;
	private import StandInProfile::*;

	#Interface port def PowerPort;
	#Interface interface def DataLink;

	#Process action def MonitorPressure {
		in pressureReading : Real;
		out alarm : Boolean;
	}

	part def PumpSystem {
		@Component { bearer = BearerKind::material; }

		part <'CMP-PUMP'> pump : Pump;
		part <'CMP-CTRL'> controller : Controller;
		part <'CMP-SENS'> sensor : PressureSensor;
		part <'CMP-ENCL'> enclosure : Enclosure;

		port powerIn : PowerPort;
		interface dataLink : DataLink;

		perform action monitor : MonitorPressure;
	}

	part def Pump {
		@Component { bearer = BearerKind::material; }
		port powerPort : PowerPort;
	}

	part def Controller {
		@Component { bearer = BearerKind::information; }
		interface dataPort : DataLink;
	}

	part def PressureSensor {
		@Component { bearer = BearerKind::material; }
	}

	part def Enclosure {
		@Component { bearer = BearerKind::material; }
	}

	requirement def MaxPressureDef {
		doc /* The system shall limit sustained pressure to 10 bar. */
		subject system : PumpSystem;
	}

	requirement def ResponseTimeDef {
		doc /* The controller shall raise an alarm within 200 ms of an over-pressure reading. */
		subject system : PumpSystem;
	}

	verification def PumpSystemAcceptance {
		objective acceptanceObjective {
			verify requirement maxPressureVerdict : MaxPressureDef;
			verify requirement responseTimeVerdict : ResponseTimeDef;
		}
	}

	part <'CMP-SYS'> pumpSystemUnderTest : PumpSystem;

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
