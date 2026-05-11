# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] — 2026-05-11

### Added

- Five SHA-pinned LLM prompts (`prompts/prompt_v0.txt` … `prompts/prompt_v4.txt`)
  for schema-aware constraint extraction from IDTA Submodel Template
  specification PDFs.
- Byte-pinned hashes in `prompts/SHA256SUMS`, verified by the CI workflow.
- Design-rationale documentation in `docs/PROMPT_EVOLUTION.md` describing
  what each version adds and why.
- Empirical evaluation in `docs/EVALUATION.md` with the full v0→v4
  metric tables from the ETFA 2026 study (F1, precision, recall,
  per-class breakdowns, K=5 stability).
- Original per-run trace metadata snapshotted in
  `docs/ORIGINAL_EVOLUTION_LOG.md`.
- Worked rendering example in `examples/render_prompt.py` showing
  placeholder substitution (`template_id`, `template_version`,
  `template_name`).
- CI workflow `.github/workflows/ci.yml` (matrix Python 3.11+3.12)
  that verifies SHA-256 pins, runs ruff lint, and runs pytest.
- MIT licence and Zenodo-ready `CITATION.cff` (DOI pending).

### Headline empirical claim

- Within-prompt-SHA stability rate **1.000** across **K=5** runs at
  `(model=qwen2.5:7b-instruct, hardware, prompt-SHA, T=0)` tuple.
- v2 reaches the highest F1 = **0.481** at precision 0.905.
- v3 reaches the highest precision = **1.000** at F1 = 0.474 under
  an honesty contract.
- 126 unique constraint keys across the v0..v4 25-run grid.

[Unreleased]: https://github.com/hadijannat/idta-smt-extraction-prompts/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/hadijannat/idta-smt-extraction-prompts/releases/tag/v0.1.0
