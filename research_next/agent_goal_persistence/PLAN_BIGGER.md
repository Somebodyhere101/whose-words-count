# PLAN_BIGGER: from a mechanism paper to a G1-scale result

Written 2026-10-28 19:30 +04:00, after PREREG_U, at the user's request: "Let us make this bigger, how shall we do it? Plan it out."

## Where G1 stands now

| Criterion | Status |
|---|---|
| Causal mechanism | Partly: the PREREG_T map |
| Generality | Partly: 4 models, 3 families, 1.7–8B |
| Capability that beats baselines | Missing (PREREG_U NONE) |
| Outside validation | Missing |

## The bet

**What we have.** Models do not carry one "who said this" tag. Each behaviour reads the source at its own depth:
- obeying is decided 4–9 layers after attributing or believing;
- it is decided from a source code the model copies onto the text's own tokens (the "content phase").

**What would make it big:**
1. **The same map everywhere:** every open family we can run, and 30B+.
2. **A selective lever** at the content phase. It stops a model obeying instructions inside tool output while the model keeps using that output's facts, and it beats prompt defences and V-Steer on standard benchmarks.
3. **A tool, a preprint and outside replication.**

**Prior art** (checks on 10-28: `REFERENCES_VERIFIED.md`, the PREREG_U section):
- No defence we found measures the obey-versus-use split, so a working *selective* defence would be new.
- The generic "restore the hierarchy" lane is taken: V-Steer (Zeng et al., COLM 2026).
- DRIP (R. Liu et al. 2025) and TrustAttention / "Heads of Security" (Shilov et al. 2026) are trained defences. We cite them; we do not re-run them.

## Money

- **Balance:** RunPod $8.63, read in the console at 19:20 +04:00. The page shows $0.00 until it has loaded. Spend rate is $0.001/h, which is the 10 GB volume `rt9jwj49za`.
- **Measured rates** (PLAN_7DAY log):

  | Item | Rate | Source |
  |---|---|---|
  | A100 SXM 80 GB | $1.79/h | secure cloud, US-KS-2, stock LOW (catalog read today) |
  | Patching sweeps | 3.40 s per B-param × layer swept | PREREG_T: 39 min / 687.8 |
  | Single-pass conditions | 0.115 s per B-param batch-forward | PREREG_U |
  | Downloads | 0.113 GB/s | PREREG_T |

- **Calibration:** "calibrated" means × 0.834, the median actual/estimate ratio over 20 cloud_runtime estimates (anchor).

**Costs by phase:**

| Phase | Computed | Calibrated | Notes |
|---|---|---|---|
| 0 readout audit + lever search | 64.9 min, $1.94 | 54.9 min, $1.64 | anchor E29 |
| 1 sealed selective defence (V) | 37.7 min, $1.12 | 31.5 min, $0.94 | arithmetic below |
| 2 map at scale (W), 2 pods | 337.8 min, $10.08 | 285.7 min, $8.52 | anchor E30 |
| 2b circuit (heads) | 46.6 min, $1.39 | 38.9 min, $1.16 | arithmetic below |
| 3 real benchmarks (X) | 418 min, $12.47 | 349 min, $10.40 | guess-heavy (decode speed, agent calls) |
| **Core total** | **$27.00** | **$22.66** | |
| Stretch: Qwen2.5-72B map | 107.8 min × $3.58/h = $6.43 | $5.36 | 2× A100 |
| **All** | **$33.43** | **$28.02** | |

**Need:** the current balance covers Phases 0, 1 and 2b. Before Phase 2, a top-up of about $30 (the user pays) covers everything including the 72B stretch at the uncalibrated estimate, with about $5 to spare.

## Phase 0: fix the ruler, find the lever (exploratory, labelled as such). E29

**Models.** Qwen3-1.7B, SmolLM3-3B, Qwen3-8B and OLMo-2-7B. Fresh pilot items (seed 2500), never reused in a sealed test.

### 0a. Readout audit

**Design.** For the base conditions and 4 patch points per model:
- generate 24 tokens greedily;
- classify which candidate answer appears first, by exact match (both answers are fictional words);
- compare with the first-token score.

**Gate, fixed now.** Keep the first-token readout for the map if both hold in at least 3 of 4 models:
- score > 0.5 agrees with the generated answer on at least 80% of decided items;
- the Spearman correlation of condition means is at least 0.7.

Otherwise, re-run PREREG_T with a generation readout on these 4 models before Phase 2 (about +$2). Defences use the generation readout in every case.

### 0b. Lever search

**Grid, 280 configurations per model:**
- **Directions:**
  - vR, the authority axis from PREREG_H/I, which exists for all 4 models and for Granite;
  - tool − user and own − user content means;
  - the PREREG_U framing vector, both signs;
  - a random direction as control.
- **Layers:** the PREREG_T content-phase peak ±3.
- **Scales:** 1, 2, 4 and 8 × the residual norm.
- **Token sets:** the statement tokens, or the whole tool turn.

**Readout.** First-token for every configuration; the top 5 per model are re-checked with generation.

**Utility.**
- The cost to user-turn obedience.
- Perplexity on 40 neutral paragraphs.

**Selection rule, fixed now.** Choose one recipe: a direction type, a depth rule and a relative scale. It must be the recipe that passes in the most models, where passing means all four of:
- d_obey ≤ −0.10 (generation);
- |d_bel| ≤ |d_obey|/2;
- user-obedience cost ≤ 0.05;
- perplexity rises by at most 10%.

**Gate.**
- If a passing recipe exists in at least 2 of 4 models, go to Phase 1.
- If not, the capability falls back to a content-phase injection *detector* (a probe). It is tested in Phase 3 against an activation-delta detector baseline (TaskTracker-style). This is a weaker claim, and we say so.

**Cost (E29).**

| Item | Calculation | Time |
|---|---|---|
| Search | 280 × 4 × 20.3 × 0.115 s | 43.6 min |
| Audit | 12 conditions × 8 batches × (20.3 × 0.115 + 24 × 0.03 × 4) s | 8.3 min |
| Top-5 checks | | 3 min |
| Downloads | 40.6 GB | 6 min |
| Pod start | | 4 min |
| **Total** | | **64.9 min, $1.94** |

## Phase 1: PREREG_V, the sealed selective defence

**Models and items.**
- The 4 Phase-0 models, plus 2 held-out families never used in the pilot: Granite-3.3-8B and Phi-4 (14.7B).
- Fresh items: 96 instructions and 96 facts, both orders.
- The recipe is frozen from Phase 0. For held-out models the layer comes from the depth rule, with no tuning.

**Conditions:**

| Condition | What it is |
|---|---|
| base | no defence |
| DEF | the recipe |
| DEF-random | a random direction with the same norm |
| P | defensive system prompt |
| SPOT | spotlighting / datamarking (Hines et al. 2024) |
| SANDWICH | the user request repeated after the tool output |
| V-Steer | official code (commit fb0e214, smoke-tested by Codex), adapted to tool-versus-user, where it runs |
| usr, usr_DEF | the cost to user obedience |

**Readout.** Generation is primary; first-token is secondary.

**Hypotheses, as in PREREG_U plus a control and transfer:**
- **H1 effective:** d_obey ≤ −0.10.
- **H2 selective:** the selectivity CI lies above 0, and |d_bel| ≤ |d_obey|/2.
- **H3 beats baselines:** selectivity above P, SPOT and SANDWICH.
- **H4 control:** the random direction has no effect.
- **H5 transfer:** at least 1 of the 2 held-out families is SELECTIVE.

**Verdict.** SELECTIVE_DEFENSE if at least 4 of 6 models meet H1–H3. Transfer is reported separately.

**Cost: 37.7 min, $1.12.**

| Item | Calculation | Time |
|---|---|---|
| Compute | 9 conditions × 16 batches × (43.2 × 0.115 + 24 × 0.03 × 43.2/8.2) s = 1,261 s | 21 min |
| Downloads | 86.2 GB | 12.7 min |
| Pod start | | 4 min |

## Phase 2: PREREG_W, the map at scale. E30

**Models.** Nine new ones; none is gated, so no Hugging Face credentials are needed.

| Family | Models | With earlier runs |
|---|---|---|
| Qwen3 | 0.6B, 4B, 14B, 32B | with 1.7B and 8B, a 6-size ladder |
| OLMo-2 | 13B, 32B | with 7B, a ladder of 7/13/32B |
| Phi | Phi-4 (14.7B) | |
| Granite | Granite-3.3-8B | |
| gpt-oss | gpt-oss-20b (MoE) | |

That makes 6 families (with SmolLM3) and 0.6–32B.

**Design.**
- PREREG_T code and rules, fresh seed. The 32B models are swept at every 2nd layer.
- A behaviour-only PREREG_S fragmentation test (obey, believe and attribute over 5 sources) on the same models.

**Candidate rules, fixed at sealing:**
- **W1:** obeying reads later than attributing in a majority of the 9 models.
- **W2:** markers carry the source in a majority of curves.
- **W3:** the obey content-phase peak sits at a fixed relative depth band. We predicted 0.56 for OLMo in PREREG_U.
- **W4:** obey and believe rank the sources differently in a majority (fragmentation at scale).
- **Scale:** a two-sided trend of the obey lag across the Qwen3 ladder (6 sizes) and the OLMo-2 ladder (3 sizes). Reported, not gating.

**Cost (E30): 337.8 min on 2 pods, about 2.5–3 h of wall-clock time, $10.08.**

| Item | Calculation | Time |
|---|---|---|
| Patching | 4,800.8 B·layers × 3.40 s | 272 min |
| Behaviour-only test | | 20 min |
| Downloads | 255.9 GB | 37.7 min |
| Pod starts | 2 pods | 8 min |

**Stretch, only if W1 holds at 32B.** Qwen2.5-72B, sys→usr only, every 2nd layer:

| Item | Calculation | Time |
|---|---|---|
| Patching | 1,454 B·layers × 3.40 s | 82.4 min |
| Download | 145 GB | 21.4 min |
| Pod start | | 4 min |
| **Total** | **× $3.58/h (2× A100) = $6.43** | **107.8 min** |

2× A100 stock in US-KS-2 reads LOW. The fallback is 2× H100 NVL at $6.38/h.

## Phase 2b: the circuit (the "how", not just the "where")

**Question.** Which attention heads copy the source code from the role markers onto the statement's tokens?

**Design.** Head-level patching across the 10 layers before the content phase, on Qwen3-8B and OLMo-2-7B. Exploratory; a sealed confirmation follows if a small set of heads carries it.

**Why.** A sharper lever for Phase 3, and a mechanism at component level.

**Before running.** A prior-art check (lesson L2).

**Cost: 46.6 min, $1.39.**

| Item | Calculation | Time |
|---|---|---|
| Compute | 320 × 4 × (8.2 + 7.3) × 0.115 s = 2,282 s | 38 min |
| Downloads | | 4.6 min |
| Pod start | | 4 min |

## Phase 3: PREREG_X, real attacks

This phase uses the frozen defence, or the detector fallback.

**Benchmarks.** All three are public. AgentDojo accepts custom pipeline elements, checked in its documentation today.

| Benchmark | Measures | Scope |
|---|---|---|
| SEP (Zverev et al., ICLR 2025) | separation score and utility score | 1,000-item sample |
| InjecAgent (Zhan et al. 2024) | attack success rate, base and enhanced | 1,054 cases |
| AgentDojo (Debenedetti et al. 2024) | utility and attack success | one suite, the "important_instructions" attack, 50 injection cases plus 20 user tasks |

**Baselines.**
- No defence, P, spotlighting, sandwich, and V-Steer where it runs.
- Trained defences are cited from their papers, not re-run.

**Exploratory, then sealed: does the map predict attacks?** Compare fake role markers inside tool output with authority-claim text. Does each model's map predict which kind succeeds?

**Gate (G1 capability, benchmark level).** In a majority of models, on both SEP and InjecAgent: lower attack success than the best prompt baseline, at no more than a 5-point utility loss. AgentDojo serves as confirmation.

**Cost: 418 min, $12.47. Guess-heavy.**

| Item | Calculation | Time |
|---|---|---|
| SEP | 250 batches × (32.0 × 0.115 + 100 × 0.03 × 32.0/8.2) s | 64 min |
| InjecAgent | 264 batches × (32.0 × 0.23 + 150 × 0.03 × 3.90) s | 110 min |
| AgentDojo | 2 models × 280 episodes × 4 calls × 6 s | 224 min |
| Downloads | | 12 min |
| Pod starts | | 8 min |

## Phase 4: show it and hand it out

- **Tool.** `sourcemap`, with three commands:
  - `map(model)`: the PREREG_T map plus fragmentation in one command, on one GPU;
  - `defend(model)`: the hook;
  - `eval(model)`: the SEP and InjecAgent harness.

  It ships with tests and the same license as the earlier repos.
- **Visible effects.**
  - A demo gallery: side-by-side generations of the same injected web page, with and without the lever.
  - One scale figure: the map across about 13 models.
- **Paper 2:** map → defence → scale. Zenodo DOI as for papers 3/5/9; arXiv if the user wants it (endorsement may be needed).
- **Outside validation.** This needs the user's OK; outreach is on hold.
  - A replication kit: reproduce one model in about 15 minutes.
  - Send it to the authors the work builds on: V-Steer, SEP/ASIDE, TrustAttention.
  - **ICML 2027:** the deadline is about 22–28 Jan 2027 (tentative, per deadline trackers read today). SaTML 2027 closed on 29 Sep.

## Schedule (+04:00)

| When | Work |
|---|---|
| 10-28 evening | Phase 0 code and pre-launch tests, then the about 1 h run |
| 10-29 | Phase 1 sealed and run; Phase 2 sealed; Phase 2b |
| 10-30 | Phase 2 runs (needs the top-up) |
| 10-31 to 11-02 | Phase 3 harness, SEP and InjecAgent. **Paper v1 (G2) final on 11-02**, with whatever is sealed by then |
| 11-03 to 11-08 | AgentDojo, the 72B stretch, the tool and gallery, the paper 2 draft |
| 11-09 to 11-15 | Release and outreach (user's OK) |

## Protected

- **G2 is not traded for scale.** The remaining paper tasks are:
  - citations (model technical reports, LoRA, Holm);
  - cost reconciliation;
  - removing the annotations;
  - the author name.
- Every confirmatory claim goes behind a seal. Pilots are labelled exploratory (L3).
- Cloud runs survive the laptop sleeping: the volume, self-stop scripts and the CPU-pod fetch (L10, L11).

## Risks, stated now

- **The capability lane has failed three times:** fine-tuning (E/F), authority steering (G and the N pilot), and the splice (U). Phase 0 can come back empty; the fallback, a detector, is weaker.
- **The first-token readout may partly measure word salience** (PREREG_U hinted at this). Phase 0a decides.
- **30B+ models have broken patterns before:** the Qwen3-32B anomaly, and weak steering at 32B. The map may not hold at scale; if so, we report it.
- **Prior art moves weekly:** "Heads of Security" was posted on 10-27. Re-check before every seal.
- **Outside validation is not in our control.** We can only make the work cheap to check.

## Decisions for the user

1. A go on this plan. Phase 0 runs on the current balance, about $1.6–1.9.
2. A top-up of about $30 before Phase 2.
3. The author name for the papers.
4. Later: OK for outreach and for publishing on Zenodo or arXiv.
5. Optional: a frontier behavioural test of fragmentation (GPT, Claude, Gemini). It needs API keys, and the user runs that one script; Claude never handles keys.

## AgentDojo after the prior-art check (2026-10-29)

**What changed.** CounterSteer (Russinovich, arXiv 2609.36570, September 2026) already shows training-free steering on tool-result tokens in prefill across five families on AgentDojo, with strong numbers: compromise 0.006–0.079, benign utility 93–100%. A plain "steering works on AgentDojo across families" result would no longer be new. Its direction, however, is fitted on labelled injection episodes, and it reports no selectivity measure. Its role axis failed on Qwen3-30B-A3B, while ours works best in dense Qwen.

**Options, to be costed with anchor after PREREG_Y:**
- **A. Our data-free lever on full AgentDojo v1.2.2** (949 cases), on 3–4 families with native tool templates. Compare against the built-in defences and against CounterSteer's published numbers.
  - New: no injection data, preregistered, utility under attack as a selectivity proxy.
  - It needs a batched multi-episode harness, because sequential HF decoding is too slow. Cost: compute before proposing.
- **B. A selectivity benchmark,** single-turn and cheap. The obey-versus-use test from PREREG_S/V is applied to several defences: prompt defences, our lever, and a CounterSteer-style direction fitted on our own followed-versus-resisted items.
  - New: a measurement axis that the field lacks ("no paper measures selectivity directly").
- **C. Reconcile the Qwen discrepancy.** Run our lever on Qwen3-30B-A3B (MoE) on SEP and InjecAgent, and a role-probe axis on dense Qwen. This is small and targeted.

**Leaning:** B, then C, which play to what is distinctively ours. A only if Y1 and Y2 pass and the batched harness is cheap enough.
