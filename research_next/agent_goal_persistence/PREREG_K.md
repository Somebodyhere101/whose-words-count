# PREREG_K: is the role direction necessary for the authority order?

Written 2026-10-28, before any data on seeds 1800–1859, and before the results of PREREG_J were seen.

Sealed in `PREREG_K.sha256` with:
- `code/k_analyze.py`;
- `cloud/rc21.sh`;
- `code/g_eval.py`, `code/agp_fast.py`, `code/agp_batch.py`.

## Background

**What earlier tests showed.**
- **PREREG_H/I (correlational):** the role direction vR orders the identical goal text user < system < own, the reverse of how it is obeyed, in 9 models.
- **Stage 3, PREREG_C and G (sufficiency):** adding ±vR to the goal text shifts adherence in the predicted direction, strongly in Qwen.
- **The open question is necessity.** If the role direction is removed from the goal text's representation, does the authority order flatten?

**Precedent.** Arditi et al. (2024) showed this pattern for refusal: removing one direction at every layer switched refusal off.

**Prior art against it.**
- Zeng (2025) finds system–user conflicts and social conflicts in distinct subspaces.
- Role identity is decodable along several directions (Ye et al. 2026).
- So removing one direction may leave the order intact.

**The test is falsifiable both ways.**
- If the order survives the ablation, vR is a correlate or one of several carriers.
- If it collapses while the goal is still followed, vR is necessary.

## Design

**World and readout.** The 3-way world and the p_goal readout, as in PREREG_G–J.

**Cells per model** (`g_eval.py --ablate`):
- none (`1_base`);
- the plain reminder as a system, user or own turn (`gF/uF/oF_base`);
- the same three with **vR ablated** (`_abl`);
- the same three with a **random direction ablated** (`_ablrand`), seeded 1000 + layer, the same random vector g_eval uses as its steering control.

**The ablation** (`agp_fast.Ablate`).
- **What is removed:** the unit direction is projected out of the embedding output and out of every decoder layer's output. This happens only while the reminder message is read: its role wrapper and its text.
- **Effect on stored state:** the cached keys and values of the reminder carry no component along the direction at any layer. The rest of the context is untouched.
- **Mechanical check** (Qwen3-1.7B): the largest |projection| over the reminder tokens falls from 25.5 to bf16 rounding (≤ 2.4 over all tokens, including a massive first-token activation of 1503).
- **Sampling:** ablated cells share the sampling stream of their plain cell.

**Smoke test** (Qwen3-1.7B, not in the model set; seeds 1–6, N_TEST 12). Only competence and ticker mass were read; spreads were not computed.

| Measure | Plain | vR ablated | Random ablated |
|---|---|---|---|
| Competence, mean over placements minus none | 0.861 | 0.772 | 0.865 |
| Ticker mass | 0.934 | 0.941 | 0.935 |

So the guards are likely to hold.

**Models** (layers as in PREREG_C/H/I; the models with a measurable plain order):

| Model | Direction | Layer | N_TEST | Seeds | Batch |
|---|---|---|---|---|---|
| Qwen3-4B | stage 2 (4-bit run) | 17 | 30 | 1800–1859 | 20 |
| Qwen3-8B | stage 2 | 17 | 30 | 1800–1859 | 20 |
| OLMo-2-7B-Instruct | stage 2 | 10 | 22 | 1800–1859 | 20 |
| Qwen3-14B | stage 2 | 18 | 30 | 1800–1859 | 20 |
| Qwen3-32B | stage 2 | 20 | 30 | 1800–1839 | 6 |

Granite, SmolLM3 and Qwen3-1.7B are left out: their plain user − own spreads (about 0.013–0.023 in PREREG_I) are too small to measure flattening.

## Rules (`code/k_analyze.py`)

**Measure.** S = p_goal(uF) − p_goal(oF) per seed: the full spread of the authority order.

**Gate per model** (else UNINFORMATIVE): competence gF − none ≥ 0.10, and plain S > 0, both with sign-flip p < 0.05.

**Guards** (else INVALID, because the ablation would have broken the agent rather than flattened the order):
- under vR ablation, the mean over placements of p_goal − none is ≥ 0.10 and ≥ half its plain value;
- the mean ticker mass is ≥ 0.8 × plain.

**Tests.**
- **T1, flattening:** S_plain − S_abl > 0.
- **T2, specificity:** S_ablrand − S_abl > 0.
- Sign-flip tests, Holm across the tested models, separately for T1 and T2.
- **F = 1 − mean(S_abl) / mean(S_plain)**, the share of the order removed.

**Result per model:**

| Result | Condition |
|---|---|
| FLATTENS | T1 and T2 hold, and F ≥ 0.5 |
| PARTIAL | T1 and T2 hold, and 0.2 ≤ F < 0.5 |
| NO | otherwise |

**Verdict:**

| Verdict | Condition |
|---|---|
| UNINFORMATIVE | fewer than 3 tested models |
| NECESSARY | at least 3 FLATTEN, and they are at least 60% of the tested models |
| NOT_NECESSARY | no model FLATTENS or is PARTIAL |
| PARTIAL | otherwise |

**Reported, not gating:**
- the pair spreads u−g and g−o, plain, ablated and random;
- per-placement p_goal;
- ticker mass.

**Analysis check.** `k_analyze.py` returns the intended verdict on six planted cases:

| Planted case | Verdict |
|---|---|
| Order removed (F ≈ 0.9) | NECESSARY |
| F ≈ 0.3 | PARTIAL |
| No change | NOT_NECESSARY |
| Ablation breaks competence | UNINFORMATIVE, models INVALID |
| No plain order | UNINFORMATIVE |
| 2 of 4 flatten | PARTIAL |

## Readings fixed now

- **NECESSARY.** One direction carries the authority order of chat roles for goal text: removing it flattens the hierarchy while the goal is still pursued. With the sufficiency results, the direction is necessary and sufficient, the refusal-direction pattern for role authority. (This is the strongest claim the study could make. It is still one task and two families.)
- **PARTIAL.** vR carries part of the order. The rest is carried elsewhere, consistent with Zeng's distinct subspaces.
- **NOT_NECESSARY.** vR tracks and can push authority, but the order does not depend on it.
- **UNINFORMATIVE.** The ablation broke the agent, or the order was absent.

## Infrastructure

The run shares the network volume `rt9jwj49za` with PREREG_J:
- **Folder:** `/workspace/agpk`.
- **Run-numbered markers:** `run21.log`, `PACKED21`, `FETCHED21` and `results21.tgz`.
- **Self-stop:** `cloud/ss21.sh` stops the pod 6 minutes after packing.

## Cost and time

Anchor E24, computed from measured per-cell times:
- Qwen3-4B and Qwen3-32B: PREREG_I. Qwen3-8B and OLMo-2-7B: today's pilot. Qwen3-14B: scaled from 8B (guess).
- **Arithmetic:** 2.4 boot + 10 cells × 414.5 s/60 + 14.4 download + 1.7 fetch = 87.6 min.
- Calibrated: 72 min. About $2.1–2.6 at $1.79/h.
