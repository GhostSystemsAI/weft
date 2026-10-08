// Spike 1 stand-in profile, mirroring decisions 0005 to 0007 with metadata
// definitions rather than the full BFO/CCO alignment, which belongs to the
// profile work proper (docs/plans/profile-brief.md). This package is
// disposable: it exists only to exercise the toolkit's metadata mechanism
// for spike 1's measurements.
library package StandInProfile {

	enum def BearerKind {
		material;
		information;
	}

	// Mirrors decision 0005. Applies to `part def` and `part`.
	metadata def Component {
		bearer : BearerKind;
	}

	// Mirrors decision 0006. Applies to `interface def` and `port def` only.
	metadata def Interface;

	// Mirrors decision 0007. Applies to `action def`.
	metadata def Process;
}
