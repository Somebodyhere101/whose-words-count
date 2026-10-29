# MPILOT results (exploratory, 2026-10-29)

**Records.** Predictions, both bets and the scoring rules are in `MPILOT_PRED.md`, hashed in `MPILOT_PRED.sha256` before launch.

**Run.** Pod `agp-mpilot` (9evtdc8qut6cr9, A100 SXM, US-KS-2, $1.79/h), 06:51–07:44 UTC, about $1.6. The fetch was md5-verified (f8450d96ae5b78b4c67ee68382577baa), and the pod was terminated afterwards.

**Data and analysis.** Data: `cloud_mpilot/out_mp` (2,840 runs, also in `Documents/agp_res/mpilot`). Analysis: `code/mpilot_analyze.py` → `mpilot_analysis.json`.

**Model.** Qwen3-8B bf16, 3-way world, 40 paired seeds. Differences are on mean_p_goal, with seed-bootstrap 95% CIs.

## Gates: both pass

| Gate | Result |
|---|---|
| Competence: gF − none | **+0.708** [0.648, 0.762], 40/40 |
| Calibration: PREREG_M plan pair, D0 = other − self (system/user mean) | **−0.183** [−0.227, −0.140], 0/40 positive. Same sign as PREREG_M and larger. |

## Outcomes

| Outcome | Estimate (95% CI) | Rule met? |
|---|---|---|
| O1: "Another manager's" below neutral | **+0.150** [0.114, 0.187], 40/40 | TRUE |
| O2: "Your own" above neutral | **+0.033** [0.022, 0.045], 36/40 | TRUE |
| O3: "Your own" above "My own" in both system and user turns | system **+0.051** [0.030, 0.075]; user +0.016 [0.008, 0.026] | FALSE (user below 0.02; the direction holds in both) |
| O4: "Dana's" ≈ neutral | **−0.003** [−0.014, 0.008] | TRUE |
| O5: system > assistant turn, no header, matched position | **+0.028** [0.013, 0.046], 36/40 | TRUE |
| O6: ≥ 8/10 paraphrase sets share the sign | 10/10 negative (o − s from −0.052 to −0.192) | TRUE |
| O7: "My own" in the assistant turn > in the system turn | **−0.017** [−0.029, −0.005] | FALSE |
| Secondary interaction: (a:my − a:s) − (g:my − g:s) | **+0.037** [0.019, 0.056], 34/40 | first person gains relative to "your own" in the assistant turn |

**Brier scores:** Codex **0.174**, Claude 0.214. Codex's bets were better calibrated.

## What it means (exploratory, one model)

1. **The PREREG_M wording effect is mostly a penalty on the rival's plan, not a self bonus.**
   - Against the neutral "The plan for this fund:", "Another manager's plan" loses 0.150 and "Your own plan" gains only 0.033. So about 82% of the self/other gap is the other-penalty.
   - Codex's prediction for "O1 true, O2 false" nearly holds: the self bonus exists but is small.
2. **The penalty is not just any third party.**
   - "Dana's plan" ≈ neutral (−0.003).
   - Exploratory: the sets that use "A colleague's" or "Someone else's" (sets 3, 6, 8: o − s −0.086, −0.095, −0.052) penalise less than the "Another manager's" sets (−0.16 to −0.19).
   - The discount tracks a competing manager. Named versus unnamed and the word "another" are not separated here: Codex flagged that confound.
3. **The turn gap survives at a matched position** (+0.028, 36/40) in bf16 Qwen3-8B. This replicates PREREG_H's +0.024 with the position confound (A12, Ye et al.) controlled.
4. **"Your" outranks "My" in the system turn** (+0.051). Its gain in the user turn is small (+0.016). The positive interaction says first person fits the assistant turn better. But "My own" in the assistant turn still does not overtake the system turn (O7 false).

## For the papers

- **The PREREG_M write-up** ("self-like framing obeyed more") should be restated. On Qwen3-8B, the effect is mainly a discount on another manager's plan, with a small "your own" bonus.
- **The own-turn discount** now has a position-matched replication on Qwen3-8B.

Both are exploratory: a single model with 40 seeds. A sealed replication would need another family, for example OLMo-2-7B, and a named/unnamed × "another" factorial.
