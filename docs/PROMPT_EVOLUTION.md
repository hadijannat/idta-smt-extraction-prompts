# Prompt evolution — design rationale for v0 → v4

This document explains what each prompt version adds on top of the previous one, and why.

The v0→v4 series is *additive*: each version preserves the contract of its predecessor and adds exactly one new design feature. This makes the series a controlled single-axis ablation of the prompting pillar of the verifier-first protocol.

All five versions share:

- An output contract of a JSON array of typed constraint records, no prose, no markdown fences.
- An atomicity rule that forbids merging multiple constraints into a single record.
- A canonical constraint-value vocabulary (`cardinality`, `sme_type`, `semantic_identity`, `value_type`, `structural_containment`, `naming`, `language_rule`, `conditional`, `recommendation_vs_hard`, `external_reference`, `allowed_values`, `format`, `ambiguous`).
- A formalization-status vocabulary that encodes calibrated abstention (`exact`, `approximate`, `ambiguous`, `prose_only`, `requires_external_resolution`).

Each version is templated with three placeholders: `{template_id}`, `{template_version}`, `{template_name}`.

## v0 — structured baseline

`prompt_v0.txt` establishes the formal record contract so that subsequent versions can be compared on extraction, formalization, citation, and schema discipline rather than on raw JSON shape.

The baseline forbids prose, requires a JSON array (possibly empty), and fixes the per-record schema with required fields including `field_idShort`, `constraint_class`, `constraint_value`, `evidence_ids`, and `formalization_status`. The model is asked to read whatever evidence is provided and emit zero or more records.

The baseline is intentionally minimal: it does not say *how* to read structured tables, it does not constrain the AAS path universe, and it does not give an example.

## v1 — adds layout-aware reading discipline

`prompt_v1.txt` adds two reading rules on top of v0:

1. **Compact-UML parsing.** The IDTA specification PDFs use a compact UML-like table notation for cardinalities, type fragments, and semantic IDs. v1 explicitly tells the model how to parse the compact-UML row pattern so that the structural information in the table cell rows is not lost in the prose interpretation.
2. **Metadata-label rule.** v1 distinguishes evidence-label headings (e.g. "idShort:", "semanticId:") from the values that follow them, so that the model does not confuse a label with a value.

v1 also adds a strict **evidence-citation rule**: every emitted record must cite at least one `evidence_id` from the input, and records without an evidence id are forbidden.

## v2 — adds the bounded template node graph

`prompt_v2.txt` adds the bounded template node graph as a prompt-time constraint:

> The set of AAS paths the model is allowed to emit is exactly the set enumerated from the IDTA JSON template by a deterministic walker. Any path outside the graph is a hallucination.

This is the load-bearing change. It moves the prompt from open-world (any AAS path the model can imagine) to closed-world (only paths that the published IDTA Submodel Template machine-readably contains). The empirical effect is the largest single-version F1 gain across the v0→v4 series, driven mostly by an improvement on the `sme_type` constraint class.

The bounded template node graph itself is published as a standalone library at [`idta-smt-walker`](https://github.com/hadijannat/idta-smt-walker), verified on 131 IDTA Submodel Template JSONs.

## v3 — adds the honesty contract

`prompt_v3.txt` adds an explicit honesty contract on top of v2:

> The model is required to mark a record as `prose_only`, `ambiguous`, or `requires_external_resolution` whenever it cannot point to specific evidence that supports the emitted `constraint_value`. Confident emission requires evidence; absence of evidence requires abstention.

The empirical effect is the highest precision in the series (P = 1.000) at the cost of a small F1 drop. v3 trades recall for an absolute zero false-positive rate.

## v4 — adds nine first-level few-shot examples

`prompt_v4.txt` adds nine worked examples drawn from the first-level Nameplate fields on top of v3.

Each example is a `(constraint_class, constraint_value, formalization_status, evidence_ids)` quadruple grounded in a real evidence block. The intent of the examples is to give the model concrete shape patterns for each constraint class.

The empirical effect on the IDTA 02006 corpus is a regression: v4 narrows the model's emission distribution toward the example shapes, missing classes that the examples do not cover. The lesson recorded in the ETFA paper is that few-shot examples can *narrow* coverage by over-anchoring the model to example shapes when the examples are drawn from a single SMT corpus.

## Summary table

| Version | Adds | Headline empirical effect on IDTA 02006 v3.0.1 |
|---|---|---|
| v0 | structured baseline | establishes the contract |
| v1 | layout-aware reading + evidence-citation rule | +F1 vs v0; emits `cardinality` records aggressively |
| v2 | bounded template node graph | **largest single-version F1 gain**, +sme_type recall |
| v3 | honesty contract | **highest precision (1.000)** at slight F1 cost |
| v4 | nine first-level few-shot examples | F1 regression (narrowed emission distribution) |

See [`EVALUATION.md`](EVALUATION.md) for the full metric tables.
