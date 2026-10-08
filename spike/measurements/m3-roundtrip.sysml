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
        @Component {
            bearer = BearerKind::material;
        }
        part <'CMP-PUMP'> pump : Pump;
        part <'CMP-CTRL'> controller : Controller;
        part <'CMP-SENS'> sensor : PressureSensor;
        part <'CMP-ENCL'> enclosure : Enclosure;
        port powerIn : PowerPort;
        interface dataLink : DataLink;
        perform action monitor : MonitorPressure;
    }
    part def Pump {
        @Component {
            bearer = BearerKind::material;
        }
        port powerPort : PowerPort;
    }
    part def Controller {
        @Component {
            bearer = BearerKind::information;
        }
        interface dataPort : DataLink;
    }
    part def PressureSensor {
        @Component {
            bearer = BearerKind::material;
        }
    }
    part def Enclosure {
        @Component {
            bearer = BearerKind::material;
        }
    }
    requirement def MaxPressureDef {
        doc /*The system shall limit sustained pressure to 10 bar. */
        subject system : PumpSystem;
    }
    requirement def ResponseTimeDef {
        doc /*The controller shall raise an alarm within 200 ms of an over-pressure reading. */
        subject system : PumpSystem;
    }
    verification def PumpSystemAcceptance {
        objective acceptanceObjective {
            verify requirement maxPressureVerdict : MaxPressureDef;
            verify requirement responseTimeVerdict : ResponseTimeDef;
        }
    }
}
