# Evidence directory

Executed deterministic evidence is retained here. No live-model or physical
trial has been performed.

* requirements-evidence.json maps all 22 requirements to executed assertions or
  explicit non-applicable/deferred dispositions, with hashes and provenance.
* release-demo.json and release-wheel.json identify the final clean product
  source and its verified installed-wheel replay and repeated 18 mm builds.
* acceptance.xml / acceptance.txt contain 61 passing cases. Lint, types and
  dependency checks have separate output files.
* baseline.json records the pinned existing-tool comparison.
* consumer.json records installation in a separate fresh environment, expected
  failure, correction, non-default input and semantic reproduction.
* performance.json records three fresh-interpreter builds and sampled peak RSS.
* seeded-failures*.json preserve defect outcomes; raw CAD and complete reports
  are in ignored artifacts/seeded-failures and artifacts/seeded-failures-v2.
* fixture-24.png and replay.png were rendered from actual reimported STEP and
  visually inspected. The later [publication audit](publication-audit/README.md)
  contains browser screenshots, a new acceptance run and a separate benchmark.
* The website normal and draft-preview build logs are retained. The normal
  build excludes the article; its front matter remains published: false.

Regeneration scripts are in scripts/. Use a new output directory or retain and
rename a previous run before repeating commands. Large CAD artifacts and virtual
environments remain local/ignored. Documentation contains no proposed repository
URL presented as live. See progress.md for command history and limitations.

Each manifest must identify run mode (deterministic, replay, live), source commit, dirty diff hash if any, requirement IDs, input and oracle hashes, environment versions, commands, exit codes, artifacts, and limitations. Live runs additionally record actual model/provider, attempts, tokens when available, time, budget, and costs when known. Preserve unavailable values as null; never replace them with invented zeros.
