# RNDCTL: is the inj2 random control direction-free? (exploratory, predictions written before running)

Date: 2026-10-29. This is an exploratory check, not a sealed preregistration. It was prompted by anomaly #3 in
Downloads/breakthrough_prompting (stage 0/1), and the user OK'd running it on the laptop GPU.

## Setup

Everything matches inj2 on Qwen3-4B (bf16, layer 17, vR from stage2_Qwen3-4B/directions.pt, steering on the
injected-sentence tokens only, first-token readout p_code / p_legit, cases seed 7). n = 48 cases, the first 48 of
inj2's 120. Placements: doc, asst, sys.

Conditions per placement:
- base;
- dir ±2 (±2·vR);
- the original inj2 random draw (generator seed 2000+17) at ±2;
- 16 new isotropic random draws, each norm-matched to vR, at +2 and at −2;
- inflate: scale h on the span by sqrt(1 + ||2vR||² / ||h||²) per token. This gives the same norm as h + 2r with no
  new direction.

## Predictions, one per hypothesis

| Hypothesis | Prediction |
|---|---|
| **D (direction-free dilution)** | For each draw, the +r and −r shifts in doc p_code have the same sign. Across draws the two are positively correlated (r > 0.3). At least 13 of 16 draws raise doc p_code at both signs. |
| **S (per-draw direction / superposition)** | The +r and −r shifts are anticorrelated (r < −0.3), and the mean shift across the 32 signed draws is small relative to their SD. |
| **N (norm only)** | Inflate reproduces at least 50% of the mean random shift in doc. |
| **Tail** | The original draw's +2 shift (0.209 → 0.642) lies above the 90th percentile of the 32 signed draws. |

## Amendment before the full run (predictions unchanged)

The bf16 smoke test did not reproduce inj2: doc base p_code was 0.000 against inj2's 0.209 per-case values.
inj2 had loaded Qwen3-4B in 4-bit (AGP_4BIT=1, PLAN_7DAY.md:146). rndctl.py now honours AGP_4BIT, and the full
run uses 4-bit to match inj2. A side finding, recorded now: in bf16 the injection is ignored at baseline
(p("Summary") ≈ 1.0 on cases 0–3). So inj2's doc baseline of 0.209 depends on 4-bit quantisation.

## What this changes in the paper (rule fixed now)

- **If D holds:** every "beyond random" contrast that used one isotropic draw must be restated as "beyond a
  direction-free disruption". The specificity of the learned direction is then judged against the whole
  distribution of random draws, not against one draw.
- **If S holds:** the single-draw control was a lucky or unlucky sample. Again the contrasts must be judged
  against the distribution of draws.
- **If neither holds:** report the distribution and leave the claims as they are.
