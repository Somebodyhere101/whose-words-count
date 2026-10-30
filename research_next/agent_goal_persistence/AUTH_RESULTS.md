# AUTHPILOT results (2026-10-29, exploratory): the rival-plan penalty vanishes in Qwen once the plan is assigned

Predictions, gates, rules and both bets: `AUTH_PRED.md` (hashed before launch; `sha256sum -c AUTH_PRED.sha256` passes
for AUTH_PRED.md, authpilot.py, rc_auth.sh, ss_auth.sh and the bundle). Scoring: `code/auth_analyze.py`, written before
the data. Output: `cloud_authpilot/auth_analysis.json`, raw files `cloud_authpilot/out_auth/` (1770 per model, 0 errors).

**Run:** pod agp-authpilot (A100 SXM, US-KS-2, $1.79/h), 11:59–13:02 UTC, about 63 min, about $1.9 (estimate 60 min).
Pod terminated after the md5-verified fetch (FETCHED_OK e0c72e38c97a3e55fb11171ddbce5d98).

## Gates

| | Qwen3-8B | OLMo-2-7B-Instruct |
|---|---|---|
| Competence (gF − none) | +0.685 [0.594, 0.770], 30/30 | +0.608 [0.575, 0.640], 30/30 |
| Rival penalty with no authority, P(x) | +0.126 [0.096, 0.161], 30/30 (reproduces MPILOT's 0.150) | +0.088 [0.073, 0.106], 30/30 |

## Main result

Penalty P = p(neutral header) − p("Another manager's"), seed-paired, mean over system/user turns and paraphrases.

| Authority | Qwen3-8B | OLMo-2-7B |
|---|---|---|
| none (x) | +0.126 [0.096, 0.161] | +0.088 [0.073, 0.106] |
| binding (b0–b2) | **+0.000 [−0.011, 0.013]**, 16/30 | **+0.036 [0.029, 0.042]**, 29/30 |
| background (k0–k2) | +0.171 [0.129, 0.216] | +0.094 [0.078, 0.111] |

Per paraphrase, binding: Qwen −0.005 / +0.001 / +0.006; OLMo +0.039 / +0.021 / +0.047.
Background framing makes the penalty larger in Qwen (+0.044 over none), not smaller.

## Outcomes (scored by the pre-written rules)

| Outcome | Rule | Result | Value | Codex | Claude |
|---|---|---|---|---|---|
| A1_Q | n_BIND − n_x ≥ 0.02 | TRUE | +0.035 [0.022, 0.051] | .72 | .60 |
| A2_Q | P(BIND) ≥ 0.05 | **FALSE** | +0.000 | .64 | .55 |
| A2-kill_Q | CI upper of P(BIND) < 0.05 | **TRUE** | upper 0.013 | .18 | .25 |
| A3_Q | P(x) − P(BIND) ≥ 0.03 | TRUE | +0.126 [0.094, 0.160] | .72 | .70 |
| A4_Q | BACK − x ≤ −0.02 | TRUE | −0.061 [−0.083, −0.042] | .84 | .75 |
| A5_Q | \|d_BIND − n_BIND\| < 0.02 | TRUE (by point) | +0.016 [0.010, 0.023] | .72 | .65 |
| A1_L | n_BIND − n_x ≥ 0.02 | **FALSE** | +0.004 [−0.004, 0.011] | .65 | .55 |
| A2_L | P(BIND) ≥ 0.05 | FALSE | +0.036 | .42 | .35 |
| A2-kill_L | CI upper of P(BIND) < 0.05 | TRUE | upper 0.042 | .34 | .35 |
| A6_L | P(x) ≥ 0.05 | TRUE | +0.088 | .64 | .55 |

**Brier (10 decided outcomes): Codex 0.251, Claude 0.235.** Both are at coin-flip level (0.25). Both bettors put
the penalty surviving authority in Qwen as the likely result; it did not.

## Reading

1. **Kill rule fires (Qwen).** With its baseline reproduced, the rival penalty goes from 0.126 to zero (CI ±0.012)
   once the plan is assigned, in all three paraphrases. By the rule written before launch, the Qwen penalty is read as
   remit/applicability ("someone else's plan is not my job"), not a source tag that overrides authority. The
   "source tag" lane for G1, as stated, is closed for Qwen3-8B.
2. **OLMo keeps a small residual.** A2-kill is TRUE by rule (rules out ≥ 0.05), but a +0.036 penalty survives
   assignment in 29/30 seeds. This is not established as a model difference: no paired cross-model contrast was
   preregistered (Codex: a cross-model difference "needs a direct paired comparison").
3. **Not preregistered, noted only:** in Qwen the self bonus survives assignment (s_BIND − n_BIND +0.023
   [0.014, 0.032]); "Your own" adds above neutral even when every plan is binding, while "Another manager's" no longer
   costs anything. In OLMo binding headers barely raise following of the neutral plan (A1_L FALSE).
4. **A5 passes by its point rule, but its CI excludes zero:** a binding "Dana's" plan is followed slightly more than
   a binding neutral one in Qwen (+0.016).

## Limitations

- No comprehension check that the model read the header as intended.
- One task (the 3-way fund world); 30 seeds; two models of 7–8B.
- **Possible ceiling compression in Qwen:** binding cells sit at 0.88–0.92. There is headroom (s_BIND reaches
  0.909–0.923 and still differs from n), but a smaller penalty could be masked near the top.
- A2-kill rules out a penalty of 0.05 or more; it does not establish zero (Qwen's CI happens to bracket zero).
