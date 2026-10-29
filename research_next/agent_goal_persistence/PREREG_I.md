# PREREG_I: does the role direction predict the authority order across families and sizes?

Written 2026-10-27, before any data from these models in this setting. Sealed in `PREREG_I.sha256` with:
- `code/i_analyze.py`;
- `cloud/rc18.sh`;
- `code/g_eval.py`, `code/agp_fast.py`, `code/agp_batch.py`, `code/src_probe.py`.

## Background

**PREREG_H found ONE AXIS in Qwen3-8B, Qwen3-14B and OLMo-2-7B.** The authority order of the identical goal reminder, user > system > own, matched its position on the model's own role direction vR: user lowest (most "given"), then system, then own. vR was built from own-vs-given contrasts only.

**The generality question.** Does the axis predict *whatever order a model shows*?
- **Why order flips matter:** if a family orders the placements differently, the axis should flip with it.
- **SmolLM3-3B is the sharp case.** Its natural own-vs-given gap was reversed in the original task.

## Design

**Models.** Six models, none tested in the 3-way world before:

| Model | Direction file | Layer (depth) | N_TEST | Seeds | Batch |
|---|---|---|---|---|---|
| Qwen3-1.7B | stage2 | 13 (0.46) | 30 | 1500–1559 | 20 |
| SmolLM3-3B | stage2 | 7 (0.19, PREREG_C) | 30 | 1500–1559 | 20 |
| Qwen3-4B | stage2 | 17 (0.47) | 30 | 1500–1559 | 20 |
| Granite-3.3-8B | stage2 | 10 (0.25, PREREG_C) | 30 | 1500–1559 | 20 |
| OLMo-2-13B-Instruct | computed in-run by `src_probe.py` | 12 (0.30) | 22 | 1500–1559 | 10 |
| Qwen3-32B | stage2 | 20 (0.31, best in the 32B sweep) | 30 | 1500–1539 (n 40, for memory) | 6 |

- The OLMo-2-13B layer comes from OLMo-2-7B's depth.
- The Qwen3-32B layer choice is exploratory but fixed here.

**What is run** (`g_eval.py --probe`, 3-way world):
- cells 1 / gF / oF / uF, the fixed goal text as the reminder;
- the projection of the reminder's own tokens onto unit vR, byte-identical tokens across roles (checked for every tokenizer).

## Rules (`code/i_analyze.py`)

**Competence gate per model:** p_goal(gF) − p_goal(1) ≥ 0.10, p < 0.05. Otherwise the model is excluded.

**For each included model and each pair** (user, system), (system, own), (user, own):
- **Decided:** a pair is decided when the behavioural difference in p_goal is significant (sign-flip p < 0.05), in either direction.
- **Agrees:** the projection difference has the matching sign (more authority = lower on vR), with p < 0.05.
- **Disagrees:** the projection difference is significant in the opposite direction.
- **Unresolved:** otherwise.

**Verdict:**

| Verdict | Condition |
|---|---|
| PASS | at least 8 decided pairs, and agree/decided ≥ 0.8 |
| FAIL | agree/decided < 0.5 |
| MIXED | otherwise |

**Reported:** each model's full behavioural and projection orders, and whether they match.

## Readings fixed now

- **PASS:** the content-free role direction predicts how each model ranks system, user and own goal text, across 3 families and from 1.7B to 32B, including any family whose order differs. Together with PREREG_H, the role-authority axis is general.
- **FAIL or MIXED:** the axis is specific to the models in PREREG_H, or the order is not stable across families.
- **SmolLM3** is reported on its own whatever happens.

## Cost and time

Measured rates, scaled by model size; the scaling is a guess where marked. A100 SXM, $1.79/h.

| Model | Compute | Download and load |
|---|---|---|
| Qwen3-1.7B | 4 cells × 3 batches × 10 s ≈ 2 min | about 0.7 min |
| SmolLM3-3B | 4 × 3 × 15 s ≈ 3 min | about 0.8 min |
| Qwen3-4B | ≈ 3 min | about 1 min |
| Granite-3.3-8B | 4 × 3 × 25 s ≈ 5 min | about 2.3 min |
| OLMo-2-13B | probe about 5 min + 4 × 3 × 70 s (guess) ≈ 19 min | about 3.5 min |
| Qwen3-32B | 4 cells × 2 × about 150 s (guess, batch 6) ≈ 20 min | about 9 min |

**Total:** about 52 min of compute + about 17 min of downloads and loads + boot 2.4 + fetch 1.7 ≈ **73 min, about $2.18.**
