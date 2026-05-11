# idta-smt-extraction-prompts

> Five SHA-pinned LLM prompts (v0–v4) for schema-aware constraint extraction from IDTA Submodel Template PDFs. Companion to [`idta-smt-walker`](https://github.com/hadijannat/idta-smt-walker) and the ETFA 2026 verifier-first paper.

[![CI](https://github.com/hadijannat/idta-smt-extraction-prompts/actions/workflows/ci.yml/badge.svg)](https://github.com/hadijannat/idta-smt-extraction-prompts/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## What this is

A pinned collection of the five LLM prompts used in an ETFA 2026 study on schema-constrained extraction of structural constraints from Asset Administration Shell (AAS) [Industrial Digital Twin Association (IDTA)](https://industrialdigitaltwin.org/) Submodel Template (SMT) specification PDFs.

Each prompt is templated with `{template_id}`, `{template_version}`, and `{template_name}` placeholders, so the same prompt body applies to any IDTA Submodel Template (for example 02006 Digital Nameplate, 02003 Technical Data, 02023 Carbon Footprint, and so on). The prompts emit JSON arrays of typed constraint records with calibrated abstention via a closed status vocabulary.

The five versions are *additive*: each adds exactly one design feature on top of the previous version. This makes the v0→v4 series a controlled ablation along a single axis of the verifier-first protocol.

## Versions

| Version | F1 | P | R | TP | FP | FN | Adds |
|---|---|---|---|---|---|---|---|
| v0 | 0.361 | 0.929 | 0.224 | 13 | 1 | 45 | structured baseline |
| v1 | 0.390 | 0.667 | 0.276 | 16 | 8 | 42 | + layout-aware reading discipline |
| **v2** | **0.481** | 0.905 | 0.328 | 19 | 2 | 39 | **+ bounded template node graph** |
| v3 | 0.474 | **1.000** | 0.310 | 18 | 0 | 40 | + honesty contract |
| v4 | 0.400 | 0.882 | 0.259 | 15 | 2 | 43 | + nine first-level few-shot examples |

Headline numbers measured on IDTA 02006 Digital Nameplate v3.0.1 with `qwen2.5:7b-instruct` at temperature 0.0, pre-registered 8-block scoring scope (58 in-scope gold records). Within-prompt-SHA stability rate **1.000 across K=5 runs** for every version, with 126 unique (AAS path, constraint class, constraint value) keys.

The v1→v2 transition (adding the bounded template node graph) contributes the largest single-version F1 gain. The bounded template node graph itself is published as a separate library at [`idta-smt-walker`](https://github.com/hadijannat/idta-smt-walker).

For the full v0→v4 design rationale see [`docs/PROMPT_EVOLUTION.md`](docs/PROMPT_EVOLUTION.md). For the full empirical evaluation see [`docs/EVALUATION.md`](docs/EVALUATION.md).

## SHA-pinning

Each prompt is byte-pinned by SHA-256. The pins are recorded in [`prompts/SHA256SUMS`](prompts/SHA256SUMS) and verified by the CI workflow on every push:

```
c0271aadca28a38c85e4b445aa494b696ce380c9d54197127087669732245107  prompt_v0.txt
631b7e685d2c3f2b0c61b25bd626ea2fa4cbb3ae159b81f85f118237188d8781  prompt_v1.txt
94f0ca8ed392ff436f7b96f7349d157cdeb6f6a4f107ec59d53ef28b5ee18cab  prompt_v2.txt
6357b0863ded66de925d6cedaa0c6ccdf78f6c79860133ddc3dfa505eebd16d5  prompt_v3.txt
dccf6c3ab1716b337864d8eeaa500ea25d6d409facda8a4b66bbf4b53f68ed98  prompt_v4.txt
```

Verify locally:

```bash
cd prompts && shasum -a 256 -c SHA256SUMS
```

The pins are load-bearing: a single byte changed in any prompt file invalidates the corresponding F1 number above. This is what "within-prompt-SHA stability" means in the paper.

## Quick usage

The prompts are plain text files with three placeholders. Substitute them via `str.format()` or any templating engine:

```python
from pathlib import Path

prompt = (Path("prompts") / "prompt_v2.txt").read_text(encoding="utf-8")
rendered = prompt.format(
    template_id="IDTA 02006",
    template_version="3.0.1",
    template_name="Digital Nameplate for Industrial Equipment",
)
# Now feed `rendered` to your LLM along with the evidence-block context
# and the bounded template node graph (see idta-smt-walker).
```

A working example is at [`examples/render_prompt.py`](examples/render_prompt.py).

## Repository layout

```
idta-smt-extraction-prompts/
├── prompts/
│   ├── prompt_v0.txt        structured baseline
│   ├── prompt_v1.txt        + layout-aware reading discipline
│   ├── prompt_v2.txt        + bounded template node graph
│   ├── prompt_v3.txt        + honesty contract
│   ├── prompt_v4.txt        + nine first-level few-shot examples
│   └── SHA256SUMS           byte-pinned hashes (CI-verified)
├── docs/
│   ├── PROMPT_EVOLUTION.md  v0→v4 design rationale
│   ├── EVALUATION.md        full ETFA 2026 metric tables
│   └── ORIGINAL_EVOLUTION_LOG.md  per-run trace metadata from the source experiment
├── examples/
│   └── render_prompt.py     placeholder-substitution example
└── tests/
    └── test_prompt_hashes.py  CI: pins enforced
```

## Reproducibility companion

This repo is one of three coordinated reproducibility companions to the ETFA 2026 paper:

| Companion | Purpose |
|---|---|
| [`idta-smt-walker`](https://github.com/hadijannat/idta-smt-walker) | The bounded template node graph implementation (Pillar 2 of the protocol) |
| **`idta-smt-extraction-prompts`** *(this repo)* | The five SHA-pinned prompts that drive the LLM proposer |
| ETFA 2026 paper | The verifier-first protocol that composes both with a deterministic conjunctive verifier |

## Citation

If you use these prompts, please cite them via the metadata in [`CITATION.cff`](CITATION.cff). Once a Zenodo DOI is assigned it will be included there as well.

## License

[MIT](LICENSE)
