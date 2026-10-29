# PREREG_H: is authority one axis? Does the role direction order system, user and own goal reminders as the agents obey them?

Written 2026-10-27, before any projection data exists. Sealed in `PREREG_H.sha256` with:
- `code/h_analyze.py`;
- `cloud/rc17.sh`;
- `code/g_eval.py`, `code/agp_fast.py`, `code/agp_batch.py`.

## Background

**PREREG_G** (3-way world, fresh seeds, n 60) found the authority order **user > system > own** for the identical goal reminder in Qwen3-8B, Qwen3-14B and OLMo-2-7B. This was reported but not gating:

| p_goal | Qwen3-8B | Qwen3-14B | OLMo-2-7B |
|---|---|---|---|
| user | 0.948 | 0.957 | 0.820 |
| system | 0.894 | 0.924 | 0.726 |
| own | 0.863 | 0.866 | 0.637 |

**What vR is.** The role direction is assistant-turn minus mean(system, user) activations for neutral sentences. It separates "own" from "given" by construction. It says nothing in advance about user versus system.

**The question.**
- **ONE AXIS:** a single content-free code sets authority if the reminder's position along vR also puts user text further toward "given" than system text.
- **TWO FACTORS:** if instead user text sits at or above system text on vR while being obeyed more, the user advantage comes from a second factor. Candidates are channel or recency matching with the user-turn pressure emails, or mid-conversation system messages being atypical.

**Prior art:** Geng et al. 2025 (*Control Illusion*) report that system/user hierarchies often fail behaviourally. We are not aware of a test that places all three roles on one learned direction.

## Design

| Model | vR layer | N_TEST |
|---|---|---|
| Qwen/Qwen3-8B | 17 | 30 |
| Qwen/Qwen3-14B | 18 | 30 |
| allenai/OLMo-2-1124-7B-Instruct | 10 | 22 |

- **Cells** on the 3-way world, with the fixed goal text as the reminder every 3 steps (`g_eval.py --probe`):

  | Cell | Reminder |
  |---|---|
  | 1 | none |
  | gF | system turn |
  | oF | the agent's own turn |
  | uF | user turn |

- **Probe.** While each reminder is read, the hidden state at the vR layer is averaged over the reminder's own tokens and projected onto unit vR. The fixed text is used without its first and last word, so the probed tokens are byte-identical across roles in every tokenizer (checked). Per run: the mean over the 10 inserts.
- **Seeds:** fresh 1400–1459 (n 60). Temperature 0.7, batch 20.

## Rules (`code/h_analyze.py`)

**Per model:** paired sign-flip tests over seeds, each Holm-corrected across the three models.

| Test | Contrast | Means |
|---|---|---|
| A1 | p_goal(uF) − p_goal(gF) > 0 | users outrank system |
| A2 | p_goal(gF) − p_goal(oF) > 0 | system outranks own |
| P1 | proj(gF) − proj(uF) > 0 | user text sits more toward "given" |
| P2 | proj(oF) − proj(gF) > 0 | own text sits more toward "own" |

**Per-model verdict:**
- **ORDER REPLICATED:** A1 and A2 pass.
- **ONE AXIS:** the order replicates and P1 and P2 also pass.
- **TWO FACTORS:** A1 passes but P1 is significantly reversed (mean < 0, Holm p < 0.05).
- **MIXED:** anything else.

**Overall verdict:**
- **ONE AXIS:** every model with a replicated order is ONE AXIS, and there are at least two such models.
- **TWO FACTORS:** at least two models are TWO FACTORS.
- **MIXED:** otherwise.

**Exploratory:** the within-placement correlation across seeds of projection with p_goal.

## Readings fixed now

- **ONE AXIS:** one learned, content-free direction orders the authority of all three chat roles for goal text, in two families. This is a unifying mechanism for the instruction hierarchy as these models actually apply it.
- **TWO FACTORS:** role authority is not one axis. vR captures own-versus-given, but the user advantage has another source. That is a target for follow-up.
- **MIXED:** the order or the projections do not replicate cleanly.
- **This run is also the sealed replication of the user > system > own order (A1, A2), which PREREG_G reported without a gate.**

## Cost and time

Measured. A100 SXM, $1.79/h.

| Item | Source | Minutes |
|---|---|---|
| Boot | measured | 2.4 |
| Downloads | measured | 6.6 |
| Loads | measured | 1.5 |
| Qwen3-14B: 4 cells × 3 batches × 30 s | measured | 6.0 |
| Qwen3-8B: the same, at most | upper bound | 6.0 |
| OLMo: 4 × 3 × 19 s | measured | 3.8 |
| Fetch | measured | 1.7 |
| **Total** | | **28.0** |

28.0 min ≈ **$0.84**.
