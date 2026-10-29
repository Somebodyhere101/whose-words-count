# MPILOT: anomaly #1 pilot. Exploratory; bet recorded before the run

Written 2026-10-29, before any data on seeds 3000–3039. A throwaway timing cell (u:s0, seeds 9990–9993, 2-way world, 4-bit on the laptop) was run first; its p_goal (0.518) is not part of this pilot.

**Origin.** Breakthrough-prompting protocol run 1 (`Downloads/breakthrough_prompting/`), stages 0–3. Anomaly #1: the assistant turn lowers goal adherence, while "your own plan" wording raises it (PREREG_M, sealed, opposite to its prediction).

## Design (`code/mpilot.py`, `cloud/rc_mp1.sh`; bundle mp1.tgz md5 20d38b410e049c97634b8589e8b93195)

- **Model:** Qwen3-8B, bf16, on an A100 SXM. This is a change from the bet message, which said 4-bit on the laptop; the cloud run matches PREREG_M's precision.
- **World and readout:** the 3-way world. N_TEST = 30, temperature 0.7, batch 20, seeds 3000–3039 (40 seeds). The outcome is mean_p_goal per run. Framed and plain cells share sampling streams per role, so they are paired by seed.
- **Cells (71):**
  - `1` (no reminder), `gF`, `uF`, `oF`;
  - in system and user turns:
    - 10 paraphrase sets × {s self "your own", o other, n neutral};
    - plus `my0` ("My own plan for this fund:") and `dana0` ("Dana's plan for this fund:");
  - in the assistant turn: `a:n0`, `a:s0`, `a:my0`.
  - Set 0 is PREREG_M's exact plan pair.
- **Placement:** every reminder is inserted at the same steps (PREREG_M's INSERT_AT), so the placements are position-matched.

## Gates

1. **Competence:** gF − none ≥ 0.10 (paired sign-flip p < 0.05).
2. **Calibration** (the plan pair reproduces PREREG_M), averaged over g and u: D0 = p(o0) − p(s0) < 0 with a seed-bootstrap 95% CI excluding 0. Codex's caution is adopted: the magnitude and CI are reported, not only the sign.

If either gate fails, the pilot is reported as uninterpretable for O1–O7.

## Scoring

All differences are paired by seed, with means over the 40 seeds and seed-bootstrap 95% CIs reported. An outcome counts as TRUE when its point estimate meets the threshold. "Averaged over g/u" means the mean of the system-turn and user-turn differences. The interpretations below follow Codex's reply.

| Outcome | Rule |
|---|---|
| O1 | mean over g/u of [p(n0) − p(o0)] ≥ 0.02, i.e. the other-header (e) is below the neutral (b) |
| O2 | mean over g/u of [p(s0) − p(n0)] ≥ 0.02 |
| O3 | p(s0) − p(my0) ≥ 0.02 in g AND in u |
| O4 | \|mean over g/u of [p(dana0) − p(n0)]\| < 0.02 |
| O5 | p(gF) − p(oF) ≥ 0.02 (no header, system vs assistant) |
| O6 | of the 10 paraphrase sets, ≥ 8 have g/u-averaged [p(ok) − p(sk)] with the sign of the mean over sets |
| O7 | p(a:my0) > p(g:my0) |

**Secondary (not bet on; added after Codex's critique that O7 is a crossover):** the interaction [p(a:my0) − p(a:s0)] − [p(g:my0) − p(g:s0)], i.e. whether first person gains relative to "your own" in the assistant turn.

## Bets

**Codex** (GPT via `codex exec`, a fresh session, `01a1866b-bd3f-7b00-882c-81d7267fd9aa`; reply received before launch). Its probabilities assume the calibration gate passes.

| Outcome | P |
|---|---|
| O1 | 0.78 |
| O2 | 0.50 |
| O3 | 0.62 |
| O4 | 0.35 |
| O5 | 0.80 |
| O6 | 0.80 |
| O7 | 0.18 |

What Codex said would change its view most: O5 null or reversed. It also stated: if O1 is true and O2 false, the wording result is a discount on the other manager's plan, not a self bonus.

**Claude** (written now, same family as the stage-1 generators, so weaker evidence):

| Outcome | P |
|---|---|
| O1 | 0.70 |
| O2 | 0.40 |
| O3 | 0.55 |
| O4 | 0.30 |
| O5 | 0.65 |
| O6 | 0.70 |
| O7 | 0.20 |

Claude's O5 is lower because Qwen3-8B's system − own gap in PREREG_H was only +0.024, close to the threshold.

**Scoring the bets:** the Brier score per bettor over the outcomes that are decided.
