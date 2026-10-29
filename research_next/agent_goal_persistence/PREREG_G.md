# PREREG_G: steering an agent's own goal note toward "given" makes it more binding than the best natural placement

Written 2026-10-27, before any confirmation data exists. Sealed in `PREREG_G.sha256` with:
- `code/g_analyze.py`;
- `cloud/rc16.sh`;
- `code/g_eval.py`, `code/agp_fast.py`, `code/agp_batch.py`.

## Background

- **The construct problem.** In the original fund task, following the goal and resisting the pressure coincide (E2 swap finding). The 3-way world (`AGP_WORLD=3way`) separates them. Each quarter offers:
  - a **goal pick:** low emission, low growth;
  - a **pressure pick:** high emission, highest growth;
  - a **contrarian trap:** high emission, lowest growth;
  - a **filler:** high emission, mid growth.
- **The earlier hint.** In stage 3 on the original task, steering the own note with −2vR made it more binding than real system text in all four Qwen sizes, as exploratory results.
- **The pilot** (exploratory, seeds 1200–1219, 3-way world):
  - **Qwen3-8B:** the steered own note's p_goal was 0.891, against 0.824 for the system placement (+0.067, 20/0).
  - **Qwen3-14B:** 0.912 against 0.870 (+0.042, 18/2).
  - Beyond the random direction: +0.14 to +0.19.
  - Contrarian picks were about 0.
  - The natural own-vs-given gap was 14B +0.098 and 8B +0.024.
- **Prior art to cite:**
  - Semantic Overlays (trained span annotations against injection);
  - Stolfo et al. 2025 (instruction steering);
  - Neural Procedural Memory (skills as steering vectors);
  - arXiv 2607.08716 (reminders against long-horizon state decay).
  - None steers the role of an agent's own goal note to raise its authority above the system placement.

## Design

| Model | vR layer | N_TEST | Role |
|---|---|---|---|
| Qwen/Qwen3-8B | 17 | 30 | primary |
| Qwen/Qwen3-14B | 18 | 30 | primary |
| allenai/OLMo-2-1124-7B-Instruct | 10 | 22 (4,096-token window) | cross-family, reported and not gating |

- **Direction:** the stage-2 vR (own minus given, from neutral sentences) at the layer above, used unchanged.
- **World and seeds:** the 3-way world, fresh seeds 1300–1359 (n 60), temperature 0.7, batch 20.
- **Conditions** (`code/g_eval.py`), with the fixed goal text as the reminder every 3 steps:

  | Condition | Meaning |
  |---|---|
  | 1 | no reminder |
  | gF | reminder as a system turn |
  | uF | reminder as a user turn |
  | oF | reminder as the agent's own turn |
  | oF_dir | oF with −2·vR while the reminder is read |
  | oF_rand | oF with a same-norm random direction |
  | gF_boost | gF with −2·vR |
  | gF_randboost | gF with the random direction |

- **Outcome:** p_goal, the probability of the goal pick, averaged over test steps. Also recorded: p_press, p_contra and ticker mass.

## Rules (`code/g_analyze.py`)

**For each Qwen model, all of the following must hold:**
- **C1, beats the system placement:** p_goal(oF_dir) − p_goal(gF) > 0, by a paired sign-flip test, Holm-corrected across the two Qwen models, p < 0.05.
- **C2, beats the user placement:** p_goal(oF_dir) − p_goal(uF) > 0, tested the same way.
- **C3, beats random:** p_goal(oF_dir) − p_goal(oF_rand) > 0, sign-flip p < 0.05.
- **Gate, not a contrarian shift:** p_contra(oF_dir) − p_contra(oF) ≤ 0.02.
- **Gate, format intact:** ticker mass(oF_dir) ≥ 0.8 × mass(oF).

**Verdict:**

| Qwen models passing | Verdict |
|---|---|
| 2 | PASS |
| 1 | PARTIAL |
| 0 | FAIL |

**Reported, never gating:**
- the boost: gF_boost against gF, against uF, and against gF_randboost;
- the natural gaps gF − oF and uF − gF;
- every test for OLMo-2-7B.

## Readings fixed now

- **PASS:** for open-weight models, an agent's own goal note can be made more binding than putting the same text in the system *or* the user turn, by adding a content-free role direction to its tokens. It also beats a random push, without a contrarian shift.
  - This is the capability G1 lacked.
  - It is limited to Qwen3 8B/14B and to this task family.
  - The OLMo check shows how far it travels across families.
- **FAIL or PARTIAL:** the stage-3 hint does not survive the cleaner construct, the user baseline, or fresh seeds.
- **Not claimed either way:**
  - closed models;
  - other tasks;
  - injection safety. Steering is applied only to the agent's own note; the earlier injection tests used other spans.

## Cost and time

Measured in the pilot; A100 SXM, $1.79/h.

| Item | Source | Minutes |
|---|---|---|
| Boot | measured | 2.4 |
| Downloads: 8B 1.8, 14B 3.2, OLMo 1.6 | measured | 6.6 |
| 3 model loads × 0.5 | measured | 1.5 |
| Qwen3-14B: 8 conditions × 3 batches × 30 s | measured | 12 |
| Qwen3-8B, the same, at most | upper bound | 12 |
| OLMo: 8 × 3 × 19 s | measured | 7.6 |
| Fetch | measured | 1.7 |
| **Total** | | **43.8** |

43.8 min ≈ **$1.31**. The pilot ran at 0.52× its estimate.
