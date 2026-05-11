# Evaluation — empirical metrics from the ETFA 2026 study

These tables reproduce the headline numbers from the ETFA 2026 verifier-first paper for the v0→v4 prompt series.

## Setup

- **Worked example**: IDTA 02006 Digital Nameplate for Industrial Equipment v3.0.1.
- **Model**: `qwen2.5:7b-instruct` served by Ollama at temperature 0.0.
- **Scoring scope**: pre-registered, 8 evidence blocks covering the first-level Nameplate fields, 58 in-scope gold records authored by the first author and adjudicated against the same evidence blocks.
- **K**: each prompt version is executed K=5 times at fixed prompt-SHA, fixed model, fixed hardware.

## Aggregate metrics (per-version)

| Version | F1 | Precision | Recall | TP | FP | FN |
|---|---|---|---|---|---|---|
| v0 | 0.361 | 0.929 | 0.224 | 13 | 1 | 45 |
| v1 | 0.390 | 0.667 | 0.276 | 16 | 8 | 42 |
| **v2** | **0.481** | 0.905 | 0.328 | 19 | 2 | 39 |
| v3 | 0.474 | **1.000** | 0.310 | 18 | 0 | 40 |
| v4 | 0.400 | 0.882 | 0.259 | 15 | 2 | 43 |

## Within-prompt-SHA stability (K=5)

Within-prompt-SHA stability rate is **1.000** for every version. Across all 25 runs (5 versions × K=5), the `(AAS path, constraint class, constraint value)` keyset is bit-identical per version, with **126 unique keys** across the v0→v4 grid and **zero unstable keys**.

The aggregate F1, precision, and recall per version exhibit **zero standard deviation across the K=5 runs**.

This is an empirical finding for the single `(model=qwen2.5:7b-instruct, hardware, prompt-SHA, T=0)` tuple reported. It is not a general claim about temperature-zero determinism. Prior literature documents that T=0 can produce divergent completions on other configurations.

## Per-class true-positive breakdown

Two structural effects are visible in the per-class TP breakdown:

1. **v2 wins on the `sme_type` class** with 7 TPs out of 13 gold records, more than double the 2 TPs of v0. This is the primary contribution of the bounded template node graph: it makes path-typed emission possible by anchoring the model in the addressable template node set.

2. **The graph-blind v1 emits `cardinality` records** (4 TPs at the cost of 8 FPs). v2, v3, and v4 emit none on this corpus, so the bounded graph trades `cardinality` emission for `sme_type` recall on this corpus.

## Calibration framing against a deterministic baseline

A rule-based regex baseline targeting compact-UML row patterns on the same 8-block scoring scope achieves **F1 = 0.847** (precision 0.887, recall 0.810, 47 TPs out of 58 gold). The best-F1 LLM version (v2) reaches **F1 = 0.481**, a **0.366 absolute F1 gap**.

The regex baseline does not transport to a second IDTA Submodel Template because the compact-UML patterns it relies on differ across templates. The LLM pipeline therefore trades raw F1 on regex-friendly tokens for backend-agnostic structural applicability, demonstrated by a cross-template walker check on IDTA 02003 v1.2.

## Practical output stability framing

Practical output stability is reported as a measurable property of the protocol at a fixed `(model, hardware, prompt-SHA, T)` tuple, and is *not* claimed as a property of the LLM in isolation.

## Citation

If you reproduce or build on these numbers, please cite both this repository ([CITATION.cff](../CITATION.cff)) and the ETFA 2026 paper.
