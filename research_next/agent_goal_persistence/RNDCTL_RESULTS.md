# RNDCTL results (exploratory, 2026-10-29)

Predictions and the amendment are in `RNDCTL_PRED.md`. The hashes in `RNDCTL_PRED.sha256` were taken before the full run. Raw data: `rndctl_q4b/rndctl.json`; summary: `rndctl_q4b/summary.txt`.

Setup: Qwen3-4B in 4-bit, as in inj2. The smoke test reproduced inj2's per-case values exactly. Layer 17, 48 cases, 16 isotropic draws each at +2 and −2, the original inj2 draw, ±2·vR, and an inflate arm. Readout is the first token (p_code / p_legit).

## Shifts in p_code from base

| Placement | Base | dir +2 | dir −2 | Original draw +2 (percentile) | 32 random shifts: mean / SD / range | corr(+r, −r) | Draws up at both signs | Inflate |
|---|---|---|---|---|---|---|---|---|
| doc | 0.222 | −0.222 | +0.638 | +0.423 (91st) | +0.015 / 0.219 / [−0.220, +0.465] | −0.85 | 0/16 | +0.019 |
| asst | 0.014 | −0.014 | +0.681 | +0.631 (top) | +0.051 / 0.132 / [−0.014, +0.574] | −0.24 | 0/16 | +0.006 |
| sys | 0.771 | −0.771 | +0.108 | +0.098 (top) | −0.101 / 0.195 / [−0.696, +0.093] | −0.59 | 1/16 | +0.008 |

## Verdicts against the predictions

- **D (direction-free dilution): REFUTED in all three placements.** Draws are anti-symmetric, not symmetric: 0–1 of 16 raise p_code at both signs, against a predicted ≥ 13.
- **N (norm only): REFUTED.** Inflating the span to the same norm moves p_code by ≤ 0.02.
- **S (per-draw direction): SUPPORTED** in doc (r = −0.85) and sys (r = −0.59). In asst it is weak (r = −0.24), because base 0.014 is at the floor.
- **Tail: SUPPORTED.** The single inj2 draw was the most compliance-raising of 33 in asst and sys, and at the 91st percentile in doc. inj2's "random raises compliance to 0.64" was one unusual draw. The average random draw does roughly nothing (mean +0.015 in doc).

## What survives about the learned direction

- **−vR is specific in every placement.** It raises p_code beyond all 32 random shifts: doc +0.638 vs max +0.465; asst +0.681 vs +0.574; sys +0.108 vs +0.093 (a small margin).
- **+vR as a defence depends on the measure:**
  - **Lowering p_code is uninformative at doc and asst,** because base is near the floor. 4/32 random shifts in doc and 19/32 in asst come within 0.02 of the direction's effect.
  - **sys:** no random draw reaches the direction's −0.771 (the lowest is −0.696). That margin is small.
  - **p_legit (the reply starts with "Summary") separates better:**
    - sys: the direction reaches 0.999, against the best random draw's 0.925;
    - doc: 1.000, but 2/32 random draws also reach ≥ 0.99;
    - asst: random draws are already at 1.0, so there is no separation.

## Consequences for the paper (rule fixed in RNDCTL_PRED.md before the run)

**S holds,** so every "beyond random" contrast that used one isotropic draw is a contrast against one sample from a wide distribution. On this model the SD of that distribution is about 0.13–0.22 in p_code.

**The inj2 gate wording ("dir-vs-rand +0.642") overstates specificity.** The fair statement for Qwen3-4B:
- the role direction's sign-specific effect (−vR raising compliance) exceeds every one of 32 random draws in all three placements;
- the defensive effect (+vR) is at the floor in doc and asst, and only modestly beyond the random distribution in sys.

**Other single-draw RND comparisons** have the same weakness: V H4, X X5, Y X5, and the "beyond random" steering shifts in §6. They should be described as single-draw controls, or rerun with ≥ 16 draws. Only PREREG_J uses a distribution (50 random directions). PREREG_K also used a single seeded draw (g_eval's), a correction from the lab front desk session on 2026-10-29.

**This is a single model with 48 cases, exploratory.** The next check would repeat it on one of the benchmark models (for example OLMo-2-7B on SEP) with 16 draws.
