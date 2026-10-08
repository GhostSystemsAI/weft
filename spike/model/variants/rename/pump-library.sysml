// Spike 1 step 5: the pump system's definitions, moved into a library
// package so step 5 (ontology export) exports reusable classes rather than
// a model's usages (OQ4: "Ontologies are exported from SysML library
// packages so that a domain definition is reused across models rather than
// minted again by each one"). pump-system.sysml imports this package and
// keeps only usages, requirements, and the satisfy/verify relationships.
library package PumpLibrary {
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
		part <'CMP-SENS'> sensor : PressureTransducer;
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

	part def PressureTransducer {
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
}
