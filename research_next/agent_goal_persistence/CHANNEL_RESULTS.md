# CHANNEL results (2026-10-30): USER_PRIMACY. The user > system order does not follow the pressure's channel

Rules: `CHANNEL.md`, sealed before data (`CHANNEL.sha256`; sealed bundle archived as `bundles/ch.tgz`, md5
ba5f8813128b92462cc95661e3eda1aa). Analysis: `code/chan_analyze.py` → `cloud_chan/chan_analysis.json`.
Raw: `cloud_chan/out_chan/` (fetch md5 7f2a812673497d1a6a07a3e90f25889c; copy in `Documents/agp_res/chan`).
Run: pod agp-chan k3ycgm7sxa5fe3, H100 NVL (community), $2.59/h, 05:43–07:50 UTC (done flag 07:49:59), about 2.1 h,
about $5.5. 0 errors; every model has all 13 cells; terminated after the md5-checked fetch (list-pods empty).
Estimate: 186 min raw / 158 calibrated (A100-measured rate); actual about 127 min on the H100.
Execution notes: the analysis was run with `PYTHONUTF8=1` (Windows codec), no code or rule change. The laptop's
network dropped around 07:2x UTC; the pod ran on and the watcher survived.

## Gates
- In-pod manipulation check: PROCEED (moved pressure bites in both channels in Qwen3-8B and OLMo-2-7B: no-pressure
  0.997 / 0.269 vs user-turn 0.049 / 0.062 vs system-turn 0.092 / 0.092).
- gpt-oss-20b flip_gate on the H100: PASS (G3 cache TV 0.011).
- Validity: 10 of 10 models valid; all 10 have a base effect (D_U > 0, Holm p < 0.05); 5 lineages.

## Verdict: USER_PRIMACY (PRIMACY in 9 of 10 base models; Falcon3-10B NONE)

| Model | D_U (pressure as user turn) | D_S (pressure as system turn) | I = D_U − D_S | Label |
|---|---|---|---|---|
| Qwen3-8B | +0.115 | +0.083 | +0.033 (n.s.) | PRIMACY |
| Qwen3-32B | +0.102 | +0.225 | −0.123 | PRIMACY |
| Qwen2.5-7B | +0.131 | +0.172 | −0.041 | PRIMACY |
| Qwen2.5-14B | +0.211 | +0.308 | −0.096 | PRIMACY |
| OLMo-2-7B | +0.112 | +0.140 | −0.028 | PRIMACY |
| OLMo-2-13B | +0.036 | +0.059 | −0.023 | PRIMACY |
| Falcon3-7B | +0.034 | +0.071 | −0.038 | PRIMACY |
| Falcon3-10B | +0.095 | +0.031 | +0.064 | NONE (D_S < 0.5·D_U; placebo test J fails) |
| granite-3.3-8b | +0.013 | +0.029 | −0.016 | PRIMACY |
| gpt-oss-20b (developer role) | +0.024 | +0.052 | −0.029 | PRIMACY |

D = p_goal(user reminder) − p_goal(operator reminder), paired over 60 seeds (40 for Qwen3-32B). Every D_U and D_S is
positive with Holm p < 0.01.

## Reading (fixed in CHANNEL.md)

- **The channel-matching account is refuted.** No model reverses: the user reminder still beats the system reminder
  when the identical pressure arrives as a system turn (D_S > 0 in 10/10). In 8 of 10 the user advantage gets
  *larger* when the pressure moves to a system turn (I < 0, Holm p < 0.05 in 8). Only Falcon3-10B shrinks
  significantly, and not to a reversal.
- **The main confound behind the sealed order claim is removed.** User > system for goal reminders in this world is not
  an artefact of the pressure arriving in user turns. Papers A/B can state this, for these 10 models, 5 lineages,
  up to 32B, one task.
- By the stopping rule, the reversal lane closes again; no follow-up spending is licensed.

## Reported, not gating

- **System-turn pressure is weaker than user-turn pressure in all 10 models** (no-reminder p_goal, system-turn minus
  user-turn pressure: +0.008 to +0.385; Falcon3-10B +0.385). Claude's pre-launch bet on this (0.60) held.
- **Placebo (exploratory):** one neutral office notice as a system turn between the pressure and the decision raises
  no-reminder goal-following in all 10 models (+0.010 to +0.277; Qwen3-8B 0.171 → 0.356, Falcon3-7B 0.379 → 0.656)
  and shrinks the user advantage in 9 of 10 (OLMo-2-7B grows). Whatever text sits just before the decision carries
  extra weight. This is consistent with recency results (e.g. Laddha et al. 2610.33201, later message wins) and is not
  a sealed claim.
- Pooled share of the base gap removed by moving the pressure (mean I / D_U over the 10): −0.55 (the gap grows).

## Bets

Claude (recorded before launch): USER_PRIMACY 0.35 (happened), CHANNEL_MATCHING 0.15, CHANNEL_MODULATED 0.25, MIXED or
UNDECIDABLE 0.25; system-turn pressure weaker in most models 0.60 (held, 10/10). Workflow proposers' reversal odds
were 0.12–0.27.
