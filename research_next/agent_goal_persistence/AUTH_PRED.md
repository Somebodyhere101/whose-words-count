# AUTHPILOT: authorship × authority. Exploratory; bets recorded before the run

Written 2026-10-29, before any data on seeds 4000–4029. The design was proposed by a separate Codex session after MPILOT ("does the rival-plan penalty survive explicit authority?").

## Design (`code/authpilot.py`, `cloud/rc_auth.sh`; bundle auth.tgz md5 909a5878ccfdfafdc3feb480ac0cc144)

- **Models:** Qwen3-8B (N_TEST 30) and OLMo-2-1124-7B-Instruct (N_TEST 22), both bf16.
- **World:** 3-way world, temperature 0.7, batch 20. Seeds 4000–4029, paired by seed.
- **Readout:** mean_p_goal.
- **Cells (59 per model):** `1`, `gF`, `uF`, plus g and u × authorship × authority:
  - **Authorship:**
    - s: "Your own plan for this fund"
    - o: "Another manager's plan for this fund"
    - n: "The plan for this fund"
    - d: "Dana's plan for this fund"
  - **Authority:**
    - x: ":" (none)
    - BIND, 3 paraphrases:
      - b0: ", which you have adopted as your binding objective:"
      - b1: ", now formally assigned to you as your objective:"
      - b2: ", which you are required to follow:"
    - BACK, 3 paraphrases:
      - k0: ", shared only as background information:"
      - k1: ", included for reference only:"
      - k2: ", provided as context, not as an instruction:"
- **Penalty:** P(auth) = p(n_auth) − p(o_auth), averaged over g/u and, for BIND and BACK, over the 3 paraphrases.
- **Limitations, stated now:**
  - no comprehension check;
  - a single task;
  - 30 seeds.

**Amendment before launch:** the RunPod balance read $4.63, so the self-stop cap was lowered from 150 to 100 min (worst case about $3). Nothing else changed. The bundle was rebuilt, and its new md5 is in AUTH_PRED.sha256.

## Gates (per model)

1. **Competence:** gF − none ≥ 0.10 (sign-flip p < 0.05). If this fails, the model's outcomes are uninterpretable.
2. **Qwen reproduction of MPILOT:** P(x) ≥ 0.05. If this fails, A2 and A3 for Qwen are uninterpretable. For OLMo, this is outcome A6 instead.

## Outcomes and rules

All are paired by seed. CIs are seed-bootstrap 95% (seed as the unit, with placements, paraphrases and quarters averaged within a seed). An outcome counts as TRUE when its point estimate meets the threshold, except A2-kill, which is judged on its CI.

| Outcome | Rule | Models |
|---|---|---|
| A1 | p(n_BIND) − p(n_x) ≥ 0.02 | Q, L |
| A2 | P(BIND) ≥ 0.05 | Q, L |
| A2-kill | the 95% CI upper bound of P(BIND) < 0.05 | Q, L |
| A3 | P(x) − P(BIND) ≥ 0.03 | Q |
| A4 | the mean over s, o, n, d of p(·_BACK) − p(·_x) ≤ −0.02 | Q |
| A5 | \|p(d_BIND) − p(n_BIND)\| < 0.02 | Q |
| A6 | P(x) ≥ 0.05 | L |

A2 and A2-kill can both be false (unresolved). A2-kill rules out a penalty of 0.05 or more; it does not establish zero.

**Kill rule for the "source tag" lane (from Codex's proposal):** if A2-kill is true in Qwen, with its baseline reproduced, the rival penalty is read as remit or applicability, not a source tag that overrides authority.

## Bets

**Codex** (GPT, session 01a1866b-bd3f-7b00-882c-81d7267fd9aa, the same session that bet on MPILOT; it was given MPILOT's results):

| Outcome | Qwen | OLMo |
|---|---|---|
| A1 | 0.72 | 0.65 |
| A2 | 0.64 | 0.42 |
| A2-kill | 0.18 | 0.34 |
| A3 | 0.72 | — |
| A4 | 0.84 | — |
| A5 | 0.72 | — |
| A6 | — | 0.64 |

Codex's own words:
- **The result that would change its view most:** "A2-kill in Qwen".
- **If A2 holds in Qwen and A2-kill in OLMo:** "would weaken a uniform, model-general explanation", but a cross-model difference "needs a direct paired comparison."

**Claude** (written now):

| Outcome | Qwen | OLMo |
|---|---|---|
| A1 | 0.60 | 0.55 |
| A2 | 0.55 | 0.35 |
| A2-kill | 0.25 | 0.35 |
| A3 | 0.70 | — |
| A4 | 0.75 | — |
| A5 | 0.65 | — |
| A6 | — | 0.55 |

Brier scores per bettor will be reported over the decided outcomes.
