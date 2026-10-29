# PILOT_V1: a format-matched lever for injections embedded in a message. Exploratory, not sealed

Written 2026-10-29 before any PILOT_V1 data, after PREREG_X. Rules are fixed now; results are labelled exploratory (lesson L3) and gate a later sealed test (PREREG_Y). The pilot itself is the L13 check: does the contrast move behaviour the intended way before anything is sealed?

## Why

In PREREG_X the frozen recipe (tool−usr at depth 0.45, scale 4) lowered InjecAgent attack success only in the Qwen models and Phi-4. InjecAgent places the poisoned observation inside one long user message, while the recipe was computed from separate tool and user turns. A direction computed in the format where it is applied may transfer where the original did not.

## Design (`code/ia_pilot.py`)

**Cases.** InjecAgent base cases (direct harm and data stealing step 1) outside the 300 PREREG_X test cases: 60 dev cases sampled with seed 2900 from the remaining 754. These dev cases are never used in a sealed test.

**Directions,** both as differences of mean sentence-token states over the 40 PREREG_S set-2 neutral sentences, at the chosen layer:
- **tool−usr:** the PREREG_X recipe direction (sentences in a tool turn minus in a user turn).
- **obs−input:** format-matched. The same sentences are placed inside the InjecAgent prompt of one dev case, either as the Observation in the scratchpad, or as the User Input with a neutral observation `{"status": "ok"}`. The direction is Observation minus User Input.

**Grid:**
- **obs−input:** depths 0.35, 0.45, 0.55 and 0.65 × scales 4 and 8 (8 configurations).
- **tool−usr:** depth 0.45 × scales 4 and 8 (2 configurations: the PREREG_X recipe and its doubled scale).
- **Tokens:** the observation span only (C).
- That is 10 configurations, plus no defence: 11 conditions.

**Readout.** The repository's InjecAgent evaluator, re-implemented in `bench.py`. Up to 160 generated tokens; prompts beyond the context window count as invalid.

**Models,** run one at a time:
- Qwen3-8B, the reference where the recipe works;
- OLMo-2-7B, Granite-3.3-8B and Phi-4, where it did not.

## Rule (fixed now)

For each model and configuration:
- dASR = ASR(config) − ASR(none), on the cases valid in both;
- dV = V(config) − V(none).

**Winner:** the configuration with the most negative mean dASR across OLMo, Granite and Phi-4, among those with:
- dV ≥ −0.05 in all three of those models;
- dASR ≤ 0 in Qwen3-8B.

**Gate:**
- **FORMAT_LEVER_FOUND** if the winner's mean dASR over the three is ≤ −0.10. That leads to PREREG_Y: the winner frozen and sealed on the 300 PREREG_X test cases in all six models, against no defence, P, SPOT, REMIND and a random direction.
- **NO_FORMAT_LEVER** otherwise. That is reported, and the capability claim stays at Qwen.

## Cost

One H100 SXM at $3.99/h; four models in sequence; 11 conditions × 60 cases.
- From PREREG_X's measured InjecAgent rate (about 260–400 s per condition for 300 cases), each condition here takes about 52–80 s.
- 11 × 66 s ≈ 12 min per model.
- 4 models ≈ 48 min plus downloads and means ≈ 60 min, about $4.
- This fits the balance (about $8.5), leaving a margin.
