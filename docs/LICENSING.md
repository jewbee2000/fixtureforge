# Provenance, licensing and local data handling

FixtureForge source, documentation, synthetic clamp specifications, independently
scripted bracket and generated examples are MIT-licensed under LICENSE. Walter
directed the project; a coding agent implemented these examples. They are not
employer designs, catalog parts or physical measurements. No proprietary manual
or manufacturer model is bundled. The external bracket is authored in
scripts/external_example.py using build123d, independently of the clamp builder.

Dependency licenses remain those of their respective authors. The runtime and
development pins are in requirements-runtime-lock.txt and requirements-lock.txt.
evidence/dependency-licenses.json records installed package versions, declared
license metadata, upstream URLs and the hashes/paths of installed notice files.
Those notices remain in the virtual environments. CadQuery and build123d use
Apache-2.0 licenses; OCCT has its LGPL exception terms. See the actual package
notices for complete terms. CADCLAW is a separately installed baseline/integration
dependency; no CADCLAW source is copied into this package.

All build/inspect/demo workflows operate on local STEP and JSON. They require
no account or credentials and contain no telemetry, model client or networking
implementation. Dependency installation uses the package registry. Tests run
the demonstration with inherited API keys/tokens removed and Python socket
creation, name lookup and connection denied, including in child workers. That is
an application-level egress check, not OS firewall or hostile-code isolation.
Native dependency vulnerabilities are not ruled out by this test.

Generated-code execution is disabled. The killable worker is a deadline/RSS
mechanism, not a sandbox. Only trusted fixed operations run; imported files are
not scripts. Treat any native CAD parser as software requiring ordinary patching
and appropriately trusted inputs. We make no security certification claim.

The HTML report escapes input text and includes no remote resources. Output
directories must be empty, part filenames must stay within the input directory,
and input hashes prevent accidental part identity drift. Reports and manifests
are local and may contain user-selected file names and geometry information.
CAD commands do not upload user inputs or reports. On 2026-10-04 Walter authorized
publication of the project source, its synthetic examples and committed evidence
to https://github.com/jewbee2000/fixtureforge. Local virtual environments and large
generated artifacts remain ignored. No website or blog deployment is authorized.
