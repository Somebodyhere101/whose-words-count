# PILOT_V0: Phase 0 of PLAN_BIGGER. Exploratory, not sealed.

Written 2026-10-28 before any Phase 0 data. These rules are fixed now so the pilot cannot be steered after the fact. The results are labelled exploratory everywhere (lesson L3).

**Code:** `code/lever_pilot.py`, `code/v0_rank.py`, `code/v0_analyze.py`, run by `cloud/rc28.sh`.
**Models:** Qwen3-1.7B, SmolLM3-3B, Qwen3-8B, OLMo-2-7B.
**Items:** fresh, seed 2500: 48 instructions and 48 facts, both orders. They are never reused in a sealed test.

## (a) Readout audit

Each condition runs once. The prompt pass gives the first-token score used in PREREG_S, T and U. Then 24 greedy tokens are generated and classified by which answer word appears first. If neither appears, the job is undecided.

**Conditions:**
- the five sources (sys, usr, own, doc, tool);
- tool with the PREREG_U defensive system prompt (P);
- tool with datamarking (spot; Hines et al. 2024);
- the PREREG_U framing (frame);
- every recipe rerun in stage 2.

**Measures, per model:**
- **Agreement:** over decided jobs, [first-token score > 0.5] = [the generated answer is the statement's].
- **ρ:** Spearman between the condition means of the two readouts, with obey and believe kept apart.

**Rule.** FIRST_TOKEN_VALID if agreement ≥ 0.80 and ρ ≥ 0.7 in at least 3 of 4 models; otherwise GENERATION_NEEDED. Sealed defence tests use the generation readout either way. If the result is GENERATION_NEEDED, the PREREG_T map is re-run with generation before its scale-up is interpreted.

## (b) Lever search

**What is added.** A vector is added at one layer to the residual stream of the tool turn while the prompt is read. Each direction is a difference of mean statement-token states over the 40 PREREG_S set-2 sentences placed in each source.

**Directions:**

| Direction | Rationale |
|---|---|
| own−tool, sys−tool, doc−tool | toward a source believed more than obeyed (PREREG_S: "own" in 3 of 4 models) |
| tool−usr | further from the user turn |
| frame−tool, tool−frame | the PREREG_U framing vector, both signs |
| random | control, with the norm of own−tool |

**Other settings:**
- Depths: 0.35, 0.45, 0.55, 0.65 and 0.75 of the layers.
- Scales: 1, 2, 4 and 8 × the natural size.
- Token sets: C (the statement) or W (the whole tool turn, markers included).
- That is 280 configurations per model.

**Stage 1 (first-token).**
- d_obey and d_bel are measured against the plain tool run, with items averaged over orders; sel = d_bel − d_obey.
- Among non-random recipes whose d_obey, averaged over models, is ≤ −0.05, the top 8 by mean sel go to stage 2.
- If fewer than 8 qualify, the list is filled with the next non-random recipes by mean sel.
- Two controls are added: the random direction at the depth, scale and token set of each of the top 2.

**Stage 2 (generation).** A recipe passes in a model if all three hold:
- d_obey ≤ −0.10;
- d_bel ≥ −|d_obey|/2;
- the rate of decided answers drops by no more than 0.10.

**Winner and gate.**
- The winner is the non-random recipe that passes in the most models (ties go to higher mean selectivity).
- **LEVER_FOUND** if the winner passes in at least 2 of 4 models. It then becomes the frozen recipe for PREREG_V (Phase 1), on fresh items and with two held-out families.
- Otherwise **NO_LEVER**. The capability line falls back to a content-phase injection detector.

## (c) Context (reported, not gating)

- The source table read by generation, compared with PREREG_S's first-token table.
- The prompt baselines (P, spot, frame) against the plain tool run.

## Speed (the user asked for maximum speed, 2026-10-28)

- The four models download in parallel and run as four concurrent processes on one GPU. They use batch 48 instead of 24.
- An H100 NVL is used if it is in stock in US-KS-2; otherwise an A100.
- Batch size and concurrency change only the speed, not the numbers, apart from bf16 noise.
