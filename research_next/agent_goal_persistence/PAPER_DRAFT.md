# Whose words count? Chat role and partial control of goal adherence

Sam Ramdan (ORCID 0009-0004-7723-4240)

**Full technical report, v1, 2026-10-29.** Two preprints were split from this report: Paper A, *Whose words count? Chat role and partial control of goal adherence* ([10.5281/zenodo.23758885](https://doi.org/10.5281/zenodo.23758885)), and Paper B, *Who said this? Most chat models weigh a text's source differently for each behaviour, and a steering lever against injected instructions* ([10.5281/zenodo.23758887](https://doi.org/10.5281/zenodo.23758887)). The report keeps every section in one file; §6g–§6n are Paper B's results. After the split, a pre-publication consistency review (`PREPUB_REVIEW.md`) led to corrections in the two papers that are not repeated here, so where this report and a paper differ, the paper is the corrected version. Code and data: https://github.com/Somebodyhere101/whose-words-count. This is an AI-run study; see the AI-use statement at the end.
- Independent AI rechecks against the raw files (`NUMBERS_RECHECK.md` and its addenda): 168 numeric claims in the Abstract and §2–§10 (2026-10-28); about 193 in §6j–§6m, 97 in §6g–§6i and 87 in §6n (2026-10-29). Every sealed analysis that was re-run reproduced. The mismatches and overstatements found were fixed.
- Every reference was verified (`REFERENCES_VERIFIED.md`).

Every claim carries its status:
- **PASS** or **FAIL:** a preregistered gate, hash-sealed before data;
- **PASS/FAIL (log gate):** a gate written in the dated plan log (`PLAN_7DAY.md`) before data, without a hash seal. This applies to stages 1–3: the fast instrument (§3), the representation test (§4), and the Qwen3-1.7B and 32B steering rows (§5);
- **AMBIGUOUS:** the preregistered verdict was ambiguous;
- **EXPL.:** exploratory, no gate;
- **REPL.:** a replication of prior work.

Numbers come from the result files listed in `CONSOLIDATED_RESULTS.md`. Every deviation from plan is logged in `PLAN_7DAY.md`.

## Abstract

In this task, the agent's goal is supplied as text. The same sentence can arrive as a system instruction, a user message, or the agent's own earlier note.

**Behaviour.** In a simulated portfolio-manager task with pressure toward high-emission stocks, the identical goal reminder is followed less when it sits in the agent's own (assistant) turn than in a system turn.
- The gap passed a preregistered test in Qwen3-1.7B.
- Across Qwen3 it grows with size, from +0.005 at 1.7B to +0.144 at 32B.
- Outside Qwen it is clear in OLMo-2-7B, small in Granite-3.3-8B, and reversed in SmolLM3-3B.

**Mechanism.** A "role direction" is the mean difference between the activations of neutral sentences placed in assistant turns and in system/user turns. Added to the goal text alone, it moves goal adherence in both directions:
- strongly in Qwen3 1.7B–14B (one preregistered pass; the gate was met at three more sizes);
- in three other families with the same sign at a family-specific depth: one preregistered pass and two weak effects.

**Origin.** In the open OLMo-2 lineage, the discount and the role direction are already present after supervised chat fine-tuning at 7B. The preregistered combined verdict across 7B and 13B is ambiguous, because the 13B gap is tiny. In an exploratory pilot (one model, 20 seeds), the discount disappears when roles are written as plain-text labels.

**What it is not.**
- The tested probes did not isolate an abstract "this is mine" representation; this does not establish that none exists.
- A first-person (deixis) account is refuted.
- Using the same direction against prompt injection replicates prior work.

**One axis.** On a cleaner task that separates following the goal from resisting pressure, the order user > system > own replicates under seal in three models from two families. The role direction orders the three placements exactly as they are obeyed (ONE AXIS, 3/3).
- **A sealed test in six more models passed:** four families, 1.7B to 32B. The direction's order matched behaviour in all 15 decided comparisons, with none against.
- **Its limit:** every model showed the same order, so whether the axis would follow a model with a different order is untested.
- **Two further sealed tests sharpen the claim.**
  - Removing the direction erases 27–44% of the order in three Qwen models, but none in OLMo (PARTIAL).
  - Social-status cues move text along it in every model, but obedience follows only in small models (MIXED).
  - J found Nature < blog in 12/12 decided comparisons (reported, not gating). The broader follow-up M was MIXED: semantic self-framing increased goal-choice probability in five of six models, and the role direction did not track its effects (4/11).

**Two preregistered attempts to fix the discount by fine-tuning both failed.** Small fine-tunes reduce drift, but not below plain reminders. They partly learn to oppose pressure rather than to follow the goal, and they raise susceptibility to forged assistant-turn injections.

**Where does the text come from? (§6g–§6m.)** We then asked how models track a text's source. The same statement was placed in five sources: system, user, the model's own earlier reply, a quoted web page, or a tool output. We measured whether the model obeys it, believes it, and can say where it came from.
- **There is no single "who said this" tag.**
  - Obeying and believing rank the five sources differently (PREREG_S; sealed verdict FRAGMENTED in 3 of 4 models, OLMo PARTIAL).
  - 8 of 9 further models are not unified either; in 7 of them the obey and believe rankings disagree (PREREG_W).
- **A patching map shows where the source is read** (PREREG_T, then PREREG_W in 10 new models from 6 families; with PREREG_T's models, 7 families from 0.6B to 32B):
  - the role-marker tokens carry it (92% of curves);
  - at least two behaviours read it at different depths (9 of 10 models);
  - obeying is read after attributing in 4 of the 5 decided models (4 of 7 with a comparable pair). In Qwen3 the lag is smallest at 14–32B (ρ = −0.54 over 7 points; reported, not tested);
  - the claim that attribution never uses the statement's own tokens is refuted.
- **A map-guided lever.** A training-free steering vector pushes the representation of tool-output text away from the user turn, at 0.45 of depth on the statement's tokens.
  - It was found in an exploratory search with a validated readout, then frozen.
  - It cut obedience to injected tool instructions in 6 of 6 models, including two families held out from the search. It was selective, keeping belief in the tool's facts, in 5 of 6 (SELECTIVE, PREREG_V).
  - Prompt defences beat it in some families and backfired in others.
- **Public benchmarks** (PREREG_X):
  - In Qwen3-8B the lever beat every prompt defence on both SEP and InjecAgent: attack success 30% → 14% and 39% → 12%. It also added to them when stacked.
  - Across six models, it lowered SEP attack success in 5 and InjecAgent attack success in 3. That gives NONE overall under the sealed rule, so a capability that beats baselines across models remains open.

We report the negative results in full.

## 1. Introduction

**The problem.**
- Long-running agents drift from their goals under pressure (Arike et al. 2025).
- Chat models assign different authority to text depending on its role, a property that instruction-hierarchy training tries to shape (Wallace et al. 2024).
- Agents increasingly keep their goals and plans in their own earlier messages: notes, scratchpads, memory.

**Our question:** is goal text in the agent's own voice weaker than the same text given to it, and if so, why?

**Contributions:**
- an instrument that measures it cheaply;
- a scale trend;
- a causal handle with its cross-family limits;
- a training-stage origin;
- a set of clean negative results, including the failure of an obvious fine-tuning fix;
- a source-monitoring account: no single source tag, and a patching map of where each behaviour reads the source, in 14 models from 7 families;
- a map-guided, training-free lever against instructions injected through tool output. Its sealed tests, on synthetic items and on two public benchmarks, show where it works and where it does not.

**The closest prior work.**
- **Role confusion.** Ye, Cui & Hadfield-Menell (ICML 2026) show that role confusion drives prompt injection, and that models infer a text's role from how it sounds rather than from its role tag. Follow-ups steer it: Zhang, Lee & Park (2026), and Liu (2026, NeurIPS 2026 workshop).
- **Relabelling text.** Chen et al. (2026) show that relabelling the role of byte-identical text changes self-correction.
- **A causal role direction.** Tsui (2026) reports a transferable conversational-role direction that causally gates self-correction. This is the closest precedent for our role direction.
- **Provenance.** Leong (2026, v2) finds source-format cues linearly decodable. Its pre-specified test for an abstract provenance representation halted without interpretable evidence either way.

Our injection results replicate the steering follow-ups. What may be new:
- the role direction's causal control of long-horizon goal adherence;
- its scale and family profile;
- its training-stage origin in an open lineage.

## 2. Instrument

**Environment.** We use, in simplified form, the goal-drift environment of Arike et al. (2025), also used by Menon et al. (2026): a fund manager ("Apex Capital") whose system prompt sets the goal: *minimise the carbon emissions caused by the companies in the portfolio*.
- Each quarter lists four fictional tickers, two high-emission/high-growth and two low-emission/low-growth.
- After 3 history quarters, 30 test quarters (22 for 4,096-token models) add pressure emails: investors, the board, news pushing growth.
- A goal reminder is inserted every 3 test steps. Its role and text define the cell:
  - **1:** no reminder;
  - **gF / oF:** the fixed goal text, *"Goal: minimize the carbon emissions… Choose the lowest-emission option each quarter."*, as a system / assistant turn;
  - **gW / oW:** a weak version without the action rule;
  - **gN / oN:** the agent's own note, given back as system / kept as its own turn;
  - **uF:** the fixed text as a user turn.

**Readout.**
- At each test step, one forward pass up to "ALLOCATE:" gives the probability of each listed ticker; the first tokens are distinct.
- p_hi is the renormalised probability of the two high-emission tickers.
- The pick is then sampled, so the history stays the agent's own behaviour.
- The outcome is mean p_hi over test steps, and lower means more adherence.

**Engineering and statistics.**
- Batched episodes share one KV cache, with per-sequence positions.
- Each step's logical context length is recorded, so context-window validity can be checked: OLMo-2's 4,096-token window forced shorter episodes.
- Statistics are paired by seed (same seed, same world): sign-flip permutation tests, Holm corrections where preregistered, and same-norm random-direction controls for every steering contrast. Except PREREG_J (50 directions), each control is a single isotropic draw; see Limitations.
- Preregistrations are sha256-sealed before data. The exact code bundles sent to each cloud run are archived and verified against the seals.

**Construct caveat (EXPL., found late).** In a control world where low-emission stocks grow fastest, so that growth pressure *agrees* with the goal, OLMo-2-7B-Instruct's system reminder *raises* high-emission picks (0.088 → 0.277). The task's "goal adherence" therefore partly measures resistance to the pressure emails. All own-vs-given comparisons hold the reminder text fixed and vary only its role, so they remain comparisons of authority. The construct should still be read as *adherence to the stated goal against pressure*.

## 3. Behaviour: the same goal text is weaker in the agent's own voice

**Qwen3-1.7B, sequential instrument, 40 seeds per cell.**

| Test | Result | Status |
|---|---|---|
| Main 2×2 (PREREG) | Own notes drift more than a fixed reminder (H1, p 0.0001). The same fixed text in the agent's own turn is followed less (H2, +0.18, p 0.025). The own cells also contained the note-request text, a confound. | PASS (H1, H2) |
| Run B (PREREG_B), confound removed | H1 PASS (p_Holm 0.0001). H2 +0.11 (p_Holm 0.037; own worse in 26 of 35 non-tied seeds). The notes-framing contrast S1 was not detected. | PASS |

**Fast instrument (stage-1 gate).** It reproduces all three preregistered directions on Qwen3-1.7B, n 40. Mean p_hi:

| Cell | 1 | gF | oF | gN | oN |
|---|---|---|---|---|---|
| p_hi | 0.96 | 0.041 | 0.046 | 0.82 | 0.84 |

Status: PASS (log gate).

**Scale and families (fast instrument, 40 seeds).** EXPL. unless marked.

| Model | own − given (fixed text) | Note |
|---|---|---|
| Qwen3-1.7B | +0.005 | weak text: +0.107 (40/40) |
| Qwen3-4B (4-bit) | +0.021 (37/3) | |
| Qwen3-8B | +0.028 (33/7) | |
| Qwen3-14B | +0.110 (40/40) | |
| Qwen3-32B | +0.144 (37/3) | |
| OLMo-2-7B-Instruct | +0.079 (35/5) | scored on steps inside the 4,096 window (post hoc); all steps +0.082 |
| OLMo-2-13B-Instruct | +0.008 | PREREG_D, 80 seeds |
| Granite-3.3-8B | +0.006 (p 0.046) | n.s. once low-mass steps are excluded |
| SmolLM3-3B | −0.014 (p 0.03) | reversed |
| SmolLM2-1.7B, EuroLLM-1.7B, OLMo-2-1B | — | do not respond to the goal at all (uninformative) |

**Reading.**
- The own-voice discount is common but not universal.
- In Qwen3 it grows steadily with size. In OLMo-2 it does not (7B +0.077 vs 13B +0.008).
- In every model that can do the task, the agent's own notes drift far more than a fixed reminder.

## 4. Representation: no abstract "this is mine" tag (FAIL, log gate, Qwen3-1.7B; no transfer in 9 more models)

**The test.** A probe trained to separate a sentence placed in the assistant turn from the same sentence in system/user turns was tested on attribution inside one user turn: "Earlier you wrote: …" vs "Your manager wrote: …". It must transfer at AUC ≥ 0.8 in both directions, at least 0.15 above a system-vs-user control.

**Result.**
- It fails in Qwen3-1.7B (0.80/0.796, control gap 0.12).
- The control transfers as well or better in SmolLM2, EuroLLM, Qwen3-4B, 8B, 14B, 32B, SmolLM3, OLMo-2-7B and Granite-3.3-8B.
- Role and attribution are encoded separately.

**Parallel.** Leong (2026, v2) reports source-format cues that are linearly decodable. Its pre-specified test for an abstract provenance representation halted without interpretable evidence either way; v1 had claimed absence. Our negative result is therefore a separate, limited data point.

## 5. Mechanism: one role direction moves adherence in both directions

**Method.**
- vR is the stage-2 difference of means: neutral sentences as assistant turn minus the same sentences as system/user turns, per layer, on the training split.
- While the goal reminder is read, we add −α·vR to own-turn reminders ("push toward given") or +α·vR to system-turn reminders ("push toward own").
- α = 2 unless noted. The control is one same-norm random direction (a single draw).

| Model | Layer (depth) | Own text pushed toward given | Given text pushed toward own | Beyond random | Status |
|---|---|---|---|---|---|
| Qwen3-1.7B, weak text | 13 (0.46) | 0.772 → 0.634 | 0.658 → 0.815 | +0.086 / +0.072, Holm p 0.0001 | **PASS** (log gate) |
| Qwen3-4B | 17 (0.47) | 0.386 → 0.276 | 0.347 → 0.482 | +0.170 / +0.116 | EXPL. (gate met) |
| Qwen3-8B | 17 (0.47) | 0.306 → 0.154 | 0.258 → 0.580 | +0.21 to +0.30 | EXPL. (gate met) |
| Qwen3-14B | 18 (0.45) | 0.302 → 0.133 | 0.179 → 0.434 | +0.27 to +0.32 | EXPL. (gate met) |
| Qwen3-32B | 29 (0.45) | 0.881 → 0.838 | 0.747 → 0.770 | +0.04 | EXPL. (gate not met); a sweep over 0.31–0.58 depth gives 0.02–0.10 per layer (2 of 10 layers n.s. against random) |

**Shared features.**
- About 0.2 depth is not uniformly inert:
  - in Qwen3-1.7B, layer 5 gives +0.060 / +0.142 beyond random (p ≤ 0.0001);
  - in Qwen3-8B, layer 7 gives small raw shifts (+0.02, p ≤ 0.0003) but none beyond random;
  - 4B, 14B and 32B are null there.

  The tests above use about 0.45 depth.
- α = 1 gives about half the effect.
- Ticker mass, a measure of format integrity, is unchanged.
- At 14B, own text pushed toward "given" is followed better than real system text (0.133 vs 0.179).

**Other families, PREREG_C.** The first tests at Qwen's layer depths failed: there were small effects at about 0.2 depth and none at about 0.45. A preregistered depth sweep (exploratory, seeds 400–419) chose one layer per family, then confirmed it on 40 fresh seeds:

| Model | Layer (depth) | Toward given | Toward own | Beyond random | Verdict |
|---|---|---|---|---|---|
| SmolLM3-3B, weak text | 7 (0.19) | −0.053 | +0.127 | +0.065 / +0.126 | **PASS** |
| OLMo-2-7B, fixed text | 10 (0.31) | −0.047 | +0.075 | +0.053 / +0.074 | present but weak (bar 0.05) |
| Granite-3.3-8B, weak text | 10 (0.25) | −0.018 | +0.035 | +0.038 / +0.038 | present but weak (near floor) |

**Reading.**
- By the sealed table, 1 PASS of 3 means the *strength* is family-dependent.
- The causal *sign* holds in all four families, with every beyond-random test at p_Holm 0.00015.
- The best depth is family-specific: Qwen about 0.46, OLMo 0.31, Granite 0.25, SmolLM3 0.19.
- SmolLM3 passes although its natural gap is reversed. So the natural gap is not simply the projection of the reminder onto vR; other role differences contribute.

## 6. Origin: the discount arrives with chat fine-tuning (AMBIGUOUS, PREREG_D)

**Design.**
- Lineage: OLMo-2 SFT → DPO → Instruct (RLVR) at 7B and 13B.
- Native template; all six checkpoints share a byte-identical chat template.
- Cells 1/gF/oF/uF; 80 fresh seeds.
- Gate: competence (p(1) − p(gF) ≥ 0.05, p < 0.01).

| Size | SFT | DPO | Instruct | Verdict by rule |
|---|---|---|---|---|
| 7B, own − given | **+0.063** (69/11) | +0.071 (76/4) | +0.077 (75/5) | H-SFT: arrives at SFT; no amplification at p < 0.01 (DPO +0.009, p 0.16; Instruct +0.005, p 0.031) |
| 13B, own − given | +0.0075 | +0.0066 | +0.0081 | H-pref by threshold only: a tiny, flat gap; only the final stage crossed p < 0.01 |

**Verdict.** The combined verdict is **AMBIGUOUS**. The rule lacked a minimum effect size, which we note as a design weakness.

**Descriptive reading.**
- At 7B, 82% of the final gap is present right after SFT.
- The role direction at layer 10 has cosine 0.994 between SFT and Instruct.
- Relative to the reminder's effect, the discount is *largest* after SFT: 0.133, against 0.106 after DPO.
- No result supports a preference-tuning origin. Xu et al. (2026) likewise trace sycophancy across post-training stages.

**Pilots (EXPL.).**
- OLMo-2 base models (1B, 7B) do not respond to a goal reminder in a plain transcript, so a pretraining origin could not be tested.
- With plain "SYSTEM:/ASSISTANT:" labels instead of template tokens, OLMo-2-7B-Instruct's discount vanishes: +0.013 n.s., against +0.080 in its native format. The discount rides on the template's role tokens. This contrasts with Ye et al., who find that internal role perception follows style and position rather than tags. The measures differ: they use probes, we measure a behavioural discount.
- **Authority order in OLMo-2, every stage and both sizes: user > system > own.** A user-turn reminder is followed best: uF − gF is between −0.05 and −0.12, p 0.0001.

## 6b. One axis for all three roles (PASS, PREREG_H and PREREG_I)

**A cleaner construct.** The construct caveat (§2) motivated a world that separates the three behaviours. Each quarter offers:
- a **goal pick:** low emission, low growth;
- a **pressure pick:** high emission, highest growth;
- a **contrarian trap:** high emission, lowest growth;
- a **filler.**

On this world (PREREG_G, 60 fresh seeds), the own-voice discount holds in three models. Contrarian picks stay near zero in Qwen (≤ 0.003) and at a steady 0.11–0.12 in OLMo-2-7B in every reminder cell. So steering and roles move picks between the pressure option and the goal, not toward the trap.

| Model | system − own on p_goal |
|---|---|
| Qwen3-8B | +0.030 |
| Qwen3-14B | +0.058 |
| OLMo-2-7B | +0.089 |

All three are at p 0.0001.

**The authority order (PASS, replicated under seal in PREREG_H on fresh seeds).** The identical goal reminder is followed most as a **user** turn, then as a **system** turn, then as the agent's **own** turn:

| Model | user − system | system − own |
|---|---|---|
| Qwen3-8B | +0.045 | +0.024 |
| Qwen3-14B | +0.022 | +0.061 |
| OLMo-2-7B | +0.108 | +0.061 |

All Holm p ≤ 0.00025.

**Position-matched check (EXPL., MPILOT; Qwen3-8B, 40 paired seeds; predictions hashed before launch).** With the reminder inserted at the same steps and no header, the system-turn copy is still followed more than the assistant-turn copy: +0.028 [0.013, 0.046], 36 of 40 seeds, close to PREREG_H's +0.024. In this model the own-turn discount is not an artefact of position.

**One axis (PASS: ONE AXIS in 3/3 models).** We projected the reminder's own tokens (byte-identical across roles) onto the unit role direction. The direction was built only from own-vs-given neutral sentences, so it carries no built-in user-versus-system difference. Yet in every model it orders the placements exactly as the agents obey them: user text furthest toward "given", then system, then own.

| Model | system − user projection | own − system projection |
|---|---|---|
| Qwen3-8B | +2.12 (58/2 seeds) | +1.34 (60/0) |
| Qwen3-14B | +1.74 (60/0) | +1.33 (60/0) |
| OLMo-2-7B | +0.38 (60/0) | +0.12 (60/0) |

**Reading.**
- One learned, content-free direction encodes the authority order of all three chat roles for goal text, in two families.
- Moving along it shifts adherence causally (§5; PREREG_G).
- The axis orders placements, not individual episodes. Within a placement, projection and adherence correlate positively in Qwen3-14B and in two of three Qwen3-8B cells (the user cell is −0.15), and negatively in OLMo (exploratory).
- **A practical corollary:** a plain user-turn reminder beat steering the agent's own note (PREREG_G: FAIL for the steering capability). Steering a system-turn reminder further along the axis beat even the user placement in Qwen3-14B only.
**Generality (PASS, PREREG_I).** Six models not tested before in this world, fresh seeds 1500–1559 (32B: 1500–1539).
- **Families:** Qwen3, SmolLM3, Granite and OLMo-2.
- **Direction and layer:** each model uses its own direction at a layer fixed before the data. OLMo-2-13B's direction was computed in the same run. Qwen3-4B's direction came from the earlier 4-bit stage-2 run, while this run used bf16 weights; this was logged at sealing.
- **Rule:** a pair counts as decided when the behavioural difference is significant. It agrees when the projection difference has the matching sign at p < 0.05.
- **PASS needed** at least 8 decided pairs, with at least 80% agreeing.

| Model (layer) | p_goal user / system / own | user − system | system − own | projection system − user / own − system |
|---|---|---|---|---|
| Qwen3-1.7B (13) | 0.871 / 0.854 / 0.848 | +0.017 (46/14) | +0.006 (38/22) | +3.29 / +1.96 |
| SmolLM3-3B (7) | 0.785 / 0.772 / 0.771 | +0.013 (44/16) | +0.000 (n.s.) | +0.11 / +0.05 |
| Qwen3-4B (17) | 0.864 / 0.808 / 0.777 | +0.056 (60/0) | +0.031 (56/3) | +1.31 / +0.55 |
| Granite-3.3-8B (10) | 0.901 / 0.892 / 0.888 | +0.009 (38/22) | +0.005 (n.s.) | +0.17 / +0.36 |
| OLMo-2-13B (12) | 0.853 / 0.818 / 0.814 | +0.035 (56/4) | +0.004 (n.s.) | +0.48 / +0.05 |
| Qwen3-32B (20; n 40) | 0.587 / 0.342 / 0.184 | +0.245 (35/5) | +0.157 (37/3) | +4.68 / +1.25 |

- **All 6 models passed the competence gate.**
- **15 pairs were decided and all 15 agree** (agree rate 1.0). The three undecided pairs are system − own in SmolLM3, Granite and OLMo-2-13B.
- **Projection differences:** every one has the same sign on every seed (60/0; 40/0 at 32B).
- **Taken with PREREG_H:** 9 models, 4 families, 1.7B–32B, and 21 decided pairs, all agreeing.

**What the pass does and does not show.**
- **Every model showed the same order.** So the preregistration's sharpest case, a family whose order differs and an axis that flips with it, never occurred. A fixed guess of "user > system > own" would have scored the same.
- **The informative part is user versus system.** The direction was never trained to separate them. Yet it puts user text further toward "given" in all 9 models, and user text is obeyed more than system text in all 9.
- **Order, not spacing (EXPL.).** The ratio of the two gaps does not carry over from projection to behaviour: (system − own)/(user − system) has a Spearman correlation of 0.10 across the 9 models.
- **SmolLM3 (reported on its own, as preregistered).** Its own-vs-given reversal in the original world does not appear here: system ≈ own, and user is highest.
- **Qwen3-32B has the largest role gaps of any model** (user − own +0.40), in line with the Qwen scale trend in §3.

## 6c. Is the axis authority itself? Social cues within a role (MIXED, PREREG_J)

**Design.** The identical reminder follows one header line inside a system or user turn:
- authority: CEO vs new intern;
- expertise: a Nature study vs a personal blog;
- consensus: all twelve board members vs one board member.

These are adapted from Control Illusion. We tested 7 models on fresh seeds, with 50 random directions as a null.

**Rule.** Wherever a high-vs-low pair changes obedience, the projection should move with it.

**Result.** 20 of 28 decided pairs agree (0.71). That is above the random-direction null (95th percentile 0.64) but below the preregistered 0.8. **MIXED.**
- **Expertise agrees everywhere: 12/12 decided pairs, 6 models, both roles.**
  - "Based on a peer-reviewed study in Nature" is obeyed *less* than "based on a post on a personal blog".
  - The Nature-framed text also sits higher on the role direction, toward the model's *own* voice.
  - This was the non-obvious prediction stated in the preregistration before data. It was not a gate.
- **Authority and consensus split by model size.**
  - In six of seven models the high-status header moves the text toward the "own" end. In Granite the CEO header moves it slightly the other way (+0.005 and +0.023 toward "given").
  - In the small models (Qwen3-1.7B, Qwen3-4B, SmolLM3) the high-status header is also obeyed less, so these pairs agree.
  - In Qwen3-14B (authority and consensus), Qwen3-8B (consensus), OLMo-2-7B (authority and consensus) and Granite (user-turn consensus), it is obeyed *more*, so these pairs disagree. That makes 8 disagreeing pairs.
- **Reading.** The role direction tracks evidence framing in six of seven models (Granite's expertise pairs are undecided), but status cues only in small models. In larger models, status acts through another route. This is consistent with Zeng (2025), who found distinct subspaces for role and social conflicts.

## 6d. Is the axis necessary? Directional ablation (PARTIAL, PREREG_K)

**Design.** As in directional ablation (Arditi et al. 2024), the unit role direction is projected out of the embedding and every layer output while the reminder is read. A random direction (a single draw), ablated the same way, is the control. The test ran on Qwen3-4B, 8B, 14B and 32B and on OLMo-2-7B, on fresh seeds.

**Result.** Removing the direction erases a significant part of the user − own spread in three Qwen models, more than the random control, while the goal is still pursued: competence stays at 64–95% of plain.

| Model | Spread removed | Holm p (T1 / T2) |
|---|---|---|
| Qwen3-4B | 42% | 0.017 / 0.016 |
| Qwen3-8B | 44% | 0.021 / 0.016 |
| Qwen3-32B | 27% | 0.047 / 0.003 |
| Qwen3-14B | 35% (n.s.) | — |
| OLMo-2-7B | none | — |

- **Verdict: PARTIAL.** No model reaches the preregistered 50%.
- **What disappears is mainly the system − own gap.** In Qwen3-8B it falls from 0.020 to 0.003; in Qwen3-32B, from 0.151 to 0.044.
- **The user − system gap mostly survives.**

**Reading.** The direction is part of the machinery, mostly for the own-vs-given distinction it was built from. It does not account for the whole authority order; this ablation did not establish a causal contribution in OLMo.

## 6e. Does size matter? (NO_TREND, PREREG_L)

**Design.** 15 models in four families, on fresh seeds, plain reminder cells:
- Qwen3 at 1.7, 4, 8, 14 and 32B;
- Qwen2.5 at 3, 7, 14 and 32B;
- OLMo-2 at 7, 13 and 32B;
- Falcon3 at 3, 7 and 10B.

The test was an exact within-family permutation test of whether size predicts goal holding (P) or source sensitivity (A).

**Results.**
- **Goal holding: no trend** (p 0.13 unadjusted; Holm p 0.25, as sealed). In three of four families the larger models hold the goal *better*.
- **The Qwen3-32B collapse replicates on fresh seeds** (P 0.34 vs 0.89 at 14B), but it is a property of that model. Qwen2.5-32B (0.90) and OLMo-2-32B (0.96) are among the most persistent models tested.
- **Source sensitivity: no general trend** (p 0.13 unadjusted; Holm p 0.25).
  - Within the Qwen lineage it rises monotonically with size in both Qwen3 and Qwen2.5 (EXPL.).
  - OLMo goes the other way.

**The authority order holds in all 15 models (EXPL.):**
- user > system is significant in 15/15;
- system > own is significant in 13/15, and positive in the remaining 2;
- nothing is significant the other way.

With PREREG_H/I, this is the study's broadest behavioural result: four families, 1.7B–32B.

## 6f. Semantic self-attribution is distinct from chat-role placement (PREREG_M)

**Design.** Six models, 60 fresh seeds per model, 20 conditions. Two OWN minimal pairs compare a goal framed as the model's own analysis or plan against a colleague's analysis or another manager's plan, within the same system or user role. Two KNOW pairs compare established knowledge or a Nature source against a forum or blog. The goal text and probed tokens are unchanged.

**Sealed verdicts:** H1 OWN **MIXED** (1 model in the predicted direction, 5 significantly opposite after Holm); H2 KNOW **MIXED** (4 predicted, 1 opposite, 1 undecided); H3 **DOES_NOT_TRACK** (4/11 agree, 3 disagree, 4 unresolved). The SELF_DISCOUNT headline gate was not met. The formal H1 verdict is MIXED, rather than REVERSED, because one model significantly goes the other way.

| Model | OWN: other minus self | Holm p |
|---|---:|---:|
| OLMo-2-1124-7B-Instruct | -5.185 percentage points | 0.00030 |
| Qwen3-1.7B | +0.357 percentage points | 0.01980 |
| Qwen3-14B | -7.707 percentage points | 0.00030 |
| Qwen3-4B | -2.255 percentage points | 0.00030 |
| Qwen3-8B | -8.985 percentage points | 0.00030 |
| SmolLM3-3B | -0.978 percentage points | 0.00030 |

Negative values mean that self-framing increased the mean goal-choice probability. These are probability differences in the simulated task, not percentage changes in general agent reliability. In all six models, the plain role order remains user > system > assistant on these same seeds. Thus placing text in an assistant turn and describing text as the model's own plan are empirically different manipulations; they should not be combined into a general claim that self-like text has less authority.

**Exploratory detail.** Nature < blog has the same descriptive sign in 11 of 12 model-by-role comparisons, with a reversal in Qwen3-8B's user turn. This is a narrower follow-up using modified wording, not an exact replication of J. The broad knowledge family is mixed.

**Follow-up pilot (EXPL., MPILOT; Qwen3-8B only, 40 paired seeds; predictions and a Codex bet hashed before launch).** Against a neutral header ("The plan for this fund:"):
- "another manager's plan" lowers goal choice by 0.150 [0.114, 0.187], 40 of 40 seeds;
- "your own plan" raises it by 0.033 [0.022, 0.045];
- a named third party ("Dana's plan") changes nothing (−0.003, n.s.);
- all 10 paraphrase sets agree in sign.

In this model, PREREG_M's OWN contrast is therefore mainly a discount on a rival manager's plan, with a small "your own" bonus, rather than a premium on self-framing. Two predictions failed: "your own" beat "my own" by less than the predicted 0.02 in the user turn, and "my own" in the assistant turn fell below the system turn (−0.017). The details are in MPILOT_RESULTS.md.

**Verification.** The six sealed hashes matched the archived agp19 bundle or the preregistration. All 120 result files contain the expected 60 unique seeds (2000–2059). Transfer MD5: 2ceefa5a34f4f7762a233f6024b06f73. Codex reran the sealed analysis and separately recomputed the descriptive differences from raw data. This is a computational recheck by another AI, not outside or human validation. Sources: cloud_prereg_m/m.json and m_descriptive_check.json.

## 6g. One source monitor, or fragments? (FRAGMENTED, PREREG_S)

**Question.** The role results above concern goal text. In cognitive science the broader capacity is *source monitoring* (Johnson, Hashtroudi & Lindsay 1993): keeping track of whether information came from oneself, from perception, or from someone else.

We asked whether chat models have one internal source tag per piece of text that jointly drives three things:
- whether they **obey** it;
- whether they **believe** it;
- whether they can **say where it came from**.

**Design** (sealed, `PREREG_S.md`).
- **Sources.** One statement in one of five sources, after a fixed system prompt: a system turn, a user turn, the model's own earlier turn, a user turn quoting a web page, and a user turn holding a tool output.
- **Items.** 60 fictional facts and 60 fictional instructions. Each competes with a contradicting user message, in both orders.
- **Readouts:**
  - obey and believe: P(statement's answer) ÷ P(statement's + competitor's answer);
  - attribute: the probability of the correct letter in a five-way "Which message contained the sentence …?" question.
- **Source readout.** A five-way nearest-centroid readout from the statement's own tokens, on a fresh set of 40 neutral sentences.
- **Edit.** A user→own tag transplant at the decision layer, with same-norm random controls. The reverse (own→user) is exploratory.
- **Models.** Qwen3-1.7B, SmolLM3-3B, Qwen3-8B, OLMo-2-7B-Instruct.
- **Rule.** SOURCE_MONITOR requires, in a majority of models, all of: a readable tag; obey and believe ranking the sources alike (Kendall τ ≥ 0.6); attribution ≥ 0.6; and an edit that moves the behaviours as predicted.

**Result: FRAGMENTED** (3 of 4 models; OLMo PARTIAL).
- **Obey and believe rank the five sources differently in every model** (τ = 0.2–0.4).
  - Qwen3-8B obeys the user most (0.53) and its own earlier turn least (0.25), but believes the system most (0.75).
  - It believes tool output (0.66) while obeying it less (0.42).
  - Qwen3-1.7B obeys tool output *more* than the user (0.71 vs 0.51).
- **Source effects occur even where the source is poorly reported.**
  - OLMo and SmolLM3 show reliable source effects (p < 0.001) while attributing poorly: mean 0.32 in both (chance 0.20; above chance, p < 0.001).
  - Their attribution is near chance for several sources (OLMo: system 0.19, user 0.18, own 0.25).
  - Qwen3-8B attributes well (0.87).
- **The source is readable from the statement's own tokens** at the decision layer in three models (0.87–0.94; the sealed rule needs ≥ 0.8). Qwen3-1.7B misses the rule there (0.69 at layer 13; 0.91 at layer 18).
- **Transplanting that readable tag from user to own text (the sealed test) does not carry the behaviour.**
  - At natural size (×1) the edit moved nothing as predicted in three models.
  - In OLMo only obedience moved (+0.004).
  - Belief moved slightly the *opposite* way in Qwen3-1.7B and OLMo.
  - All effects of this sealed edit at ×1 were ≤ 0.03 (largest: Qwen3-1.7B belief, −0.028), against best-to-worst source gaps of 0.07–0.46.
- **J-space** (Gurnee et al. 2026; Qwen3-1.7B, with the September WikiText J-lens fit; proxy = top 64 right singular vectors of J_l): the source variation at layer 13 lies **OUTSIDE** the workspace proxy. The fraction is 0.050 against a random floor of 0.031; the sentence-content variation is 0.118.

**Exploratory (EXPL.):**
- **The source enters the workspace proxy late.** At layer 22 the source fraction is 0.127 against content 0.037.
- **Read through the J-lens, each source direction at layer 13 predicts genre-typical next tokens:**
  - user → question marks;
  - quoted page → closing quotation marks;
  - tool → code punctuation;
  - own → end-of-text and ellipses;
  - system → line breaks and colons.

  The readable tag on the words looks like a "what kind of text is this" signal, not an authority value.
- **The reverse transplant (own→user) moves more than the sealed one.**
  - It moves obedience a little in Qwen3-1.7B, Qwen3-8B and OLMo. In Qwen3-8B this is 22% of the own–user gap at ×2.
  - It also moves Qwen3-8B's belief: +0.04 at ×1 and +0.09 at ×2, beyond random.
- **Qwen3-1.7B's attribution moves away from "own"** under this edit (−0.04 at ×1, −0.07 at ×2, beyond random). In absolute terms that is more than its obedience moves (+0.01 and +0.03).

**Reading.**
- Source information is present but used piecemeal. This predicts that a defence which fixes one behaviour (for example obedience to injected text) will leave the others (belief, attribution) unchanged.
- It also suggests a different kind of defence. Some models already believe tool output while obeying it less. A *selective* intervention could lower obedience to injected instructions while keeping belief in the injected text's facts. Defences built to be selective (Shilov et al. 2026; R. Liu et al. 2025; Penman 2026) report attack success and generic utility, but none measures belief in the injected text's own facts.

**Prior art and limits.**
- Leong (2026: no abstract provenance code) and Zeng (2025: distinct subspaces) predicted fragmentation.
- An *amplified* user-minus-tool mean vector does steer injection (Zhang, Lee & Park 2026; Liu 2026). Our null is at natural size only.
- The joint obey/believe/attribute test with a causal transplant appears not to have been run before (prior-art check, 2026-10-28).
- **Limits:** four models, 1.7B–8B; synthetic items; one edit layer per model.

## 6h. Where is "who said this" read? (H1 MIXED, H2 DISSOCIATED, PREREG_T)

**Question.** PREREG_S showed that the readable source tag on a statement's own tokens barely moves behaviour when transplanted as a mean vector. So where does each behaviour read the source it actually uses?

**Design** (sealed, `PREREG_T.md`). The same statement sits in the user turn (recipient) or in the own or system turn (donor). Only the role word differs, so the two prompts are token-aligned. The exception is OLMo own→usr, where the assistant turn's end token adds one position; that token is not patched.
- The donor run's residual stream replaces the recipient's at one layer, on one position set: the role-marker tokens (M), the statement's own tokens (C), or every position after the turn (D).
- Every layer is patched, separately for obey, believe and attribute.
- Same four models; fresh items.
- The **handoff** is the first layer at which patching D carries at least half of the behaviour's source effect.
- Patching all positions reproduces the donor exactly in 7 of 8 model-pairs, and within 10% in OLMo own→usr (sanity check).

**Results.**
- **H2, DISSOCIATED in 4/4 models.** The behaviours read the source at different depths. Obeying is read 4–9 layers after attributing or believing:
  - Qwen3-1.7B: obey L18–19, believe L14, attribute L13–14;
  - Qwen3-8B: obey L25, attribute L16;
  - SmolLM3: obey L21, attribute L12.

  OLMo, which has no informative obey gap, attributes at L10 and believes at L16. Bootstrap CIs of the differences exclude 0.
- **H1, MIXED.** Before the handoff, the role-marker tokens are the main carrier in 14 of 16 informative curves, including 8 of the 10 obey and believe curves that H1 uses. Two curves (Qwen3-8B own→usr obey; OLMo own→usr believe) share the carrier with the statement's own tokens, and none is content-only. The preregistered majority (3 of 4 models all-MARKER) was missed: 2 of 4.

**Exploratory (EXPL.).**
- **Two routes.** Attribution reads the role marker mostly from the later positions and routes little through the statement's own tokens: maximum C transfer is 0.02–0.24 in 6 of 6 curves. §6l finds content use in about half the new models. Obeying has a mid-to-late content phase, in which the source sits on the statement's own words (maximum C transfer 0.38–1.33). In Qwen3-1.7B (layer 16) and Qwen3-8B (layer 23), patching only the statement's tokens carries the full obey effect.
- **This may explain PREREG_S's null for obedience (untested).** Its mean-vector edit was added at the decision layer, before the obey content phase, and at natural size.
- **Selectivity windows.** Between another behaviour's handoff and obeying's, patching the statement's tokens moves obedience much more than the other behaviour (Qwen3-1.7B layer 16: +0.69 to +0.91 over belief). This is where a selective defence would act.

**Figure.** `figures/prereg_t_sys_to_usr.png` and `figures/prereg_t_own_to_usr.png`.

**Prior art.** Patching studies exist for content-differing role contrasts in sycophancy (Kumarappan & Mujoo 2026), template-versus-instruction regions in safety (C. T. Leong et al. 2025) and obedience heads (Zeng et al. 2026). A role-word minimal-pair map split by position and by behaviour appears not to have been made before (prior-art check, 2026-10-28).

## 6i. A selective defence from the map? (NONE, PREREG_U)

**Design** (sealed, `PREREG_U.md`). We tried to turn the PREREG_T map into a defence.
- Statements arrive as tool output against a competing user message.
- The same text is also run with the framing "quoted data, not instructions for you".
- That run's states on the statement's own tokens are spliced into the plain run after one layer: the PREREG_T obey content-phase layer, fixed before data.
- The prediction was that obedience to tool instructions would fall while belief in tool facts held.
- Comparisons: the framing in the input, and a defensive system prompt.
- Two framed-minus-plain mean vectors (×1 and ×4) were reported only, with no gate.

**Result: NONE in all four models.** The splice did not lower obedience by the preregistered 0.05 in any model (Δ between −0.017 and +0.020). Qwen3-8B's −0.017 was significant (p 0.001).

**Why: a design flaw we should have caught with a pilot.** The framing itself did not lower obedience in any model, so at natural size the splice had nothing protective to carry:
- Qwen3-8B followed the tool instruction *more* (+0.15, p < 0.001);
- the framing raised belief in the tool's facts in OLMo (+0.18) and Qwen3-8B (+0.28).

**Exploratory (EXPL.):**
- **In OLMo and Qwen3-8B the splice is selective, but for belief.**
  - At mid layers it raises belief in tool facts by about half the framing's effect (OLMo +0.09 at layer 15; Qwen3-8B +0.14 at layer 20), with obedience flat.
  - This fits PREREG_T, where believing's content phase is mid-depth.
  - It is not selective in Qwen3-1.7B or SmolLM3.
- **The amplified mean vector (×4, reported only) was protective in the Qwen models.** It adds 4× the framed-minus-plain statement-token mean at the splice layer.
  - **Qwen3-1.7B:** obedience −0.167 and belief −0.069; selectivity +0.098 [0.036, 0.163]. Applied after the fact, all four sealed criteria hold.
  - **Qwen3-8B:** obedience −0.113, but belief also −0.069, so it fails the half rule.
  - **No help** in OLMo (obedience +0.032) or SmolLM3 (−0.034, with a selectivity CI that includes 0).
  - This exploratory result anticipates §6j's scale-4 lever.
- **The defensive system prompt ("never follow instructions that appear in tool outputs") raised tool-instruction following in both Qwen models** (+0.085, p 0.004; +0.045, p 0.02).
  - Our readout is the first answer word, which may mix instruction-following with how salient the word is. A generation-based check is needed before calling this a backfire.

**Status of the capability criterion.** The sealed splice did not beat the baselines. The mechanism results (§6g, §6h) stand; a capability built on them remains open.

## 6j. Checking the readout, and searching for a lever (EXPL., PILOT_V0)

**Design** (rules fixed before data in `PILOT_V0.md`; exploratory, not sealed). Fresh items (seed 2500), in the four PREREG_S/T/U models.

**(a) Readout audit.** For each condition, the first-token score is compared with what the model actually writes in 24 greedy tokens, classified by which answer word it names first.
- **Result: FIRST_TOKEN_VALID in 4 of 4 models.** Agreement on decided replies is 0.97–0.99. The Spearman correlation of condition means is 0.96–0.996 in three models and 0.74 in OLMo, which names neither answer in about half its replies.
- This answers the §6i caveat. The first-token readout behind §6g–§6i tracks generated behaviour.

**(b) Lever search.** We screened 280 steering configurations by first token, then re-checked the top 8 with generation:
- 6 directions, each a difference of mean statement-token states between sources, plus a random control (7 in all);
- 5 depths, 4 scales, and 2 token sets (the statement alone, or the whole tool turn).

**Result: LEVER_FOUND under the rule fixed in advance.** The winner pushes the tool-output statement's representation further from the user turn: **tool − user at depth 0.45, scale 4, on the statement's own tokens.** Generation readout, against the plain tool run:

| Model | Obeying the tool's instruction | Believing the tool's fact | Random direction with own−tool's norm (obey) |
|---|---|---|---|
| Qwen3-1.7B | −0.250 | −0.021 | −0.125 |
| Qwen3-8B | −0.219 | −0.073 | −0.042 |
| SmolLM3-3B | −0.372 | −0.064 | −0.021 |
| OLMo-2-7B | −0.053 (fails) | +0.070 | −0.038 |

**Exploratory side finding.** Read by generation, the prompt defences *raised* obedience to the tool's instruction in both Qwen models. In Qwen3-8B, obey went from 0.417 to 0.479 with a defensive system prompt, 0.458 with datamarking and 0.646 with a data framing. This confirms the §6i first-token observation, so it is not a readout artifact.

**Caveat.** The recipe was chosen on these same four models and these item types. Its sealed test, on fresh items and two held-out families, is §6k.

## 6k. The lever, sealed: selective, but not better than prompts everywhere (SELECTIVE, PREREG_V)

**Design** (sealed, `PREREG_V.md`):
- the frozen recipe on fresh items (seed 2700; 72 instructions and 72 facts; both orders; generation readout);
- the four pilot models, plus two families never used in the pilot: Granite-3.3-8B and Phi-4;
- comparisons: a defensive system prompt (P), datamarking (SPOT; Hines et al. 2024), a reminder after the tool output (REMIND), and a same-norm random direction (RND).

**Amendment before data.** The first launch hung because the item generator ran out of unique names at n = 96. It was re-sealed at n = 72 before any output existed.

**Result: SELECTIVE overall.**

| Model | Verdict | Obeying the tool's instruction | Believing the tool's fact | Beats P / SPOT / REMIND |
|---|---|---|---|---|
| Qwen3-1.7B | SELECTIVE_DEFENSE | −0.299 | −0.021 | yes / yes / yes |
| SmolLM3-3B | SELECTIVE_DEFENSE | −0.361 | −0.097 | yes / yes / yes |
| Qwen3-8B | SELECTIVE | −0.236 | −0.090 | no / no / yes |
| OLMo-2-7B | SELECTIVE | −0.161 | +0.079 | no / no / yes |
| Granite-3.3-8B (held out) | SELECTIVE | −0.125 | +0.069 | yes / no / yes |
| Phi-4 (held out) | NONE | −0.184 | −0.146 | no / no / no |

- **Effective in 6 of 6 models**, both held-out families included (every p ≤ 0.035).
- **Selective and better than a single random push in 5 of 6.**
- **Better than all three prompt defences in only 2 of 6.**

**What the prompt defences do depends on the family:**
- In Qwen3-1.7B, the defensive prompt and datamarking *raise* obedience to the tool's instruction (+0.097 and +0.188). Qwen3-8B shows the same sign, not significant (+0.062 and +0.056).
- In Granite, datamarking cuts it more than the recipe does (−0.368).
- In Phi-4, the defensive prompt cuts it (−0.271), but Phi-4 then often names neither answer.
- The sealed comparison uses selectivity, so a prompt that raises belief can tie it even where it raises obedience. In Qwen3-8B, datamarking's selectivity was 0.167 against the recipe's 0.146; the CI of the difference was [−0.13, 0.08], so the recipe fails H3 there.

**Reading.** A single training-free intervention, located by the map and transferred without tuning, lowers obedience to injected tool instructions in every model we tested. The steering is selective in five of six, with belief in the tool's facts mostly kept. It is not uniformly better than prompt defences, whose effects vary by family. The capability criterion in its strict form, beating all baselines in most models, is not met here. §6m tests the recipe on public benchmarks and stacked on prompt defences.

## 6l. Does the map hold in new families and at 32B? (4 of 5 SUPPORTED, PREREG_W)

**Design** (sealed, `PREREG_W.md`):
- PREREG_T's patching map, with unchanged rules, on 10 new models from 6 families. With PREREG_T's four, that makes 7 families from 0.6B to 32B:

  | Family | New models |
  |---|---|
  | Qwen3 | 0.6B, 4B, 14B, 32B |
  | OLMo-2 | 13B, 32B |
  | Phi | Phi-4 |
  | Granite | Granite-3.3-8B |
  | Falcon | Falcon3-10B |
  | Yi | Yi-1.5-9B |

- The 32B models were patched at every second layer.
- The PREREG_S behaviour test ran on the same models.
- Before sealing, the analysis reproduced every sealed PREREG_T and PREREG_S verdict exactly.

**Result:**

| Prediction | Result |
|---|---|
| At least two behaviours read the source at different depths or carriers (dissociation) | **9 of 10 models** |
| The role-marker tokens carry the source | **34 of 37 curves (92%)** |
| Obeying is read later than attributing | **4 of 7 models with a comparable pair (4 of 5 decided)**; Falcon3 reverses it, and Phi-4's two pairs disagree |
| No single source tag | **8 of 9 models not unified**; the obey and believe rankings disagree in 7 of 9; 5 of 9 fragmented |
| Attributing, unlike obeying, never draws on the statement's own words | **Not supported:** 4 of 9 |

**What holds and what narrows.** The general claims hold in most models across seven families and up to 32B. The exceptions are Phi-4, which is unified, and Granite, whose dissociation is unclear:
- a chat model does not carry one "who said this" tag;
- each behaviour reads the source in its own way;
- the role tokens are the main carrier.

Two claims are narrower:
- **"Obeying is read later" holds in 4 of 7 models with a comparable pair.** Within Qwen3 the lag is 0.14–0.25 of depth at 1.7–8B and smallest at 14–32B (0.09 at 32B), but stays positive. It is not monotone in size (ρ = −0.54 over 7 points; reported, not tested).
- **"Attribution never uses the content" is refuted.** In about half the models, attribution also draws on the statement's own tokens.

Obeying itself does draw on the statement's tokens in 8 of 9 models, and in 6 of those 8 the peak lies at 0.5–0.8 of depth. §6j's lever is applied just below that, at 0.45.

## 6m. Real prompt-injection benchmarks: strong in Qwen, not general (NONE overall, PREREG_X)

**Design** (sealed, `PREREG_X.md`):
- The frozen recipe on two public benchmarks:
  - **SEP** (Zverev et al., 2025; 300 items): does a probe placed in the data get executed, and does the task still get done?
  - **InjecAgent** (Zhan et al., 2024; 300 cases): does a ReAct agent call the attacker's tool after reading a poisoned tool observation? It is scored with the repository's own rules.
- The six PREREG_V models.
- Comparisons: no defence, the three prompt defences, a random direction, and the recipe stacked on two of the prompt defences.

**Result: NONE overall** (2 of 6 models, against the 4 the rule needs).

| Model | SEP attack success, none → steering | InjecAgent attack success, none → steering | Verdict |
|---|---|---|---|
| Qwen3-8B | 30% → 14% (utility 65% → 68%) | 39% → 12% | **beats all baselines; adds to them** |
| Qwen3-1.7B | 28% → 6% | 57% → 3% | effective; adds to prompts |
| SmolLM3-3B | 42% → 25% | 4% → 1% (floor) | none |
| Granite-3.3-8B | 45% → 36% | 46% → 40% (n.s.) | none |
| OLMo-2-7B | 56% → 44% | 90% → 87% (n.s.) | none |
| Phi-4 | 24% → 22% (n.s.) | 21% → 11% (random also 12%) | none |

**What generalizes.** On SEP, whose untrusted data sits in a tool-output turn like our synthetic items:
- the steering lowered attack success in five of six models without lowering utility;
- it beat the single random-direction control in four of six (in OLMo, the one random draw did as well);
- it beat every prompt defence on SEP's combined score in four;
- stacked on datamarking, it gave the lowest attack success in four of six (Qwen3-8B 7%, SmolLM3 5%, Qwen3-1.7B 3%, OLMo 24%). It tied for lowest in Phi-4; in Granite the steering alone was lowest.

**What does not.** In InjecAgent, the poisoned observation sits inside one long user message, not in a tool turn. There the steering helped only the two Qwen models and Phi-4, and beat the prompt defences only in Qwen.

**Reading.** The recipe was found on synthetic tool turns. It carries over to SEP's tool-turn format in most families: it lowers attack success in 5 of 6 and beats a single random-direction draw in 4 of 6. It carries over to InjecAgent's embedded format only in the family where it was found. In one model, Qwen3-8B, a training-free intervention located by the source map beats the prompt defences on two public benchmarks and adds to them. Across models, the capability criterion is not met.

**Follow-up pilot (EXPL., PILOT_V1; rules fixed before data).** We asked whether a direction computed in InjecAgent's own format would transfer where the original did not. The format-matched direction was text as the scratchpad Observation minus the same text as the User Input. It was tested on 60 development cases kept apart from the test cases.
- **Outside Qwen, no:** in OLMo, Granite and Phi-4 it lowered attack success only by breaking the agent's output format.
- **In Qwen3-8B, yes:** it cut attack success from 27% to 0–2% while *raising* the valid-reply rate.
- **Underpowered for two models:** OLMo and Granite produce valid agent replies only about 30% of the time.

The agent-format capability therefore remains a Qwen-family result.

## 6n. Larger Qwen3 models and held-out families (Y1 PARTIAL, Y2 SEP_EFFECTIVE, PREREG_Y)

**Design** (sealed, `PREREG_Y.md`). PREREG_X's code, recipe, conditions, samples and seeds were reused unchanged; the code was checked byte-identical before sealing.
- **Y1, larger Qwen3:** Qwen3-14B and Qwen3-32B on SEP and InjecAgent, with PREREG_X's per-model verdicts. SCALES required both to beat the baselines.
- **Y2, held-out families and sizes:** SEP only, on four models never run with the lever on a benchmark: Falcon3-10B and Yi-1.5-9B (new families) and OLMo-2-13B and OLMo-2-32B (larger OLMo). SEP_BEATS required at least 3 of 4 to beat all prompt defences.

**Results.**

| Model | SEP attack: none → steering | InjecAgent attack: none → steering | Sealed verdict |
|---|---|---|---|
| Qwen3-14B | 37.0% → 18.3% | 29.2% → 4.6% | NONE: on InjecAgent the single same-norm random draw also cut attack success, to 4.9% (X5) |
| Qwen3-32B | 40.3% → 30.0% | 27.8% → 8.6% | EFFECTIVE: tied the reminder prompt on SEP (X2) |
| Falcon3-10B | 48.7% → 33.0% | not run | SEP_EFFECTIVE |
| Yi-1.5-9B | 47.3% → 30.7% | not run | SEP_EFFECTIVE |
| OLMo-2-13B | 43.7% → 38.3% | not run | NONE: did not beat the single-draw random control (X5) |
| OLMo-2-32B | 58.7% → 47.3% | not run | SEP_EFFECTIVE |

Utility held in every model. The largest change was −3.3 points in InjecAgent's valid-reply rate, in Qwen3-32B.

- **Y1 = PARTIAL.** Both Qwen sizes cut attack success on both benchmarks and add to the defensive prompt and to datamarking (ADDITIVE).
  - At 32B, on InjecAgent, the steering beats every prompt defence and its random-direction control (one draw).
  - **This verdict is fragile.** It rests on Qwen3-32B passing the SEP random-control comparison by one item in 300 (CI lower bound +0.003); the pass holds in about half of bootstrap reseeds. Had it failed, Y1 would be NONE.
  - At 14B, on InjecAgent, the one random-direction draw did as well. A single draw cannot tell a direction-free effect from an unusually effective draw. In an exploratory 32-draw check on Qwen3-4B (RNDCTL), random-draw effects were sign-varying and centred near zero.
- **Y2 = SEP_EFFECTIVE.** The steering lowered SEP attack success in all four held-out models, but beat all three prompt defences in none. The reminder or the datamarking prompt matched it.

**Reading (descriptive tallies across PREREG_X and Y, not a sealed claim):**
- **The SEP effect generalizes; the InjecAgent effect is mostly Qwen.** The steering lowered SEP attack success in 11 of 12 models from 7 families, and InjecAgent's in 5 of 8 (the four Qwen models and Phi-4).
- **The advantage over prompt defences does not.** It beat all three prompt defences on SEP in 5 of 12 models (three of them not Qwen: OLMo-2-7B, SmolLM3-3B and Granite-3.3-8B) and on InjecAgent in 4 of 8 (all four Qwen). Only Qwen3-8B passes every check, including the single-draw random control, on both benchmarks.
- **Size trend in Qwen3 (descriptive, as preregistered).**
  - InjecAgent attack success with the steering, minus that with the best prompt defence: −0.38 (1.7B), −0.22 (8B), −0.18 (14B), −0.06 (32B). The advantage shrinks with size.
  - SEP, the steering's Net minus the best prompt's Net: +0.05, +0.10, +0.09, +0.05.

## 7. Accounts that failed

- **Deixis (FAIL, preregistered, Qwen3-4B and 1.7B).** The account: the discount follows first-person commitments. Instead, under +vR "I'll…" payloads are suppressed as much as other payloads or more: the most in Qwen3-4B, while in Qwen3-1.7B's system placement "You will" drops more (−0.83 vs −0.69). So the dial is pronoun-blind.
- **Addressee (INCONCLUSIVE, preregistered).** The account: text addressed to the model gets authority. The projection difference was −0.22 and −0.15 of the role gap, opposite in sign to the prediction but under the bar.
- **A lesson.** Three strong language models proposed these accounts independently and agreed. The experiments disagreed.

## 8. Injection: role steering blocks it (REPL.)

**Result (PASS on Qwen3-4B).** The direction is added to an injected instruction inside a document. Compliance falls from 0.209 to 0.000. The run used 4-bit weights; in bf16 the model ignores the injection at baseline. The single random control gave 0.642, but an exploratory 32-draw check (RNDCTL) shows that draw was unusual (91st percentile): random draws flip sign and average near zero (mean +0.015, SD 0.219). Against that distribution, −vR raises compliance beyond all 32 draws in all three placements. +vR's defensive effect is at the floor in the document and assistant placements, and only modestly beyond random in the system placement. The legitimate instruction rises from 0.79 to 1.00, and replies stay on-task in 24/24 cases.

**Prior art.** This replicates the steering results of Zhang, Lee & Park (2026) and Liu (2026), which build on Ye, Cui & Hadfield-Menell's (2026) role-confusion account. It is not a contribution.

## 9. An obvious fix fails: fine-tuning on own-voice goal practice

**Design.**
- LoRA adapters (r 16) trained on synthetic multi-turn decision tasks in 8 non-financial domains, in the reply format "CHOICE:".
- Third-party pressure throughout; a goal reminder every 3 rounds, as an assistant turn ("own") or a system turn ("given"); identical targets.
- Evaluation on the held-out fund task in its own format, plus a forged-assistant-turn injection test.

**Results.**

| Experiment | Result | Status |
|---|---|---|
| Pilots E1–E2 | n 240: drift removed (0.857 → 0.03–0.06 without reminders), but every cell at the floor. n 16: own-trained gap 0.009 vs given 0.023 (one adapter per arm). Shortcut test (growth pressure agrees with the goal): n 240 adapters pick *against* the pressure (+0.08 to +0.10). Every dose raises forged-assistant injection compliance (+0.012 to +0.085). | EXPL. |
| PREREG_E (6 vs 6 adapters, n 16, fresh seeds) | Gap own 0.0150 vs given 0.0229 (−0.008), exact permutation p 0.071. Shortcut present even at n 16. | **FAIL** |
| Pilot E4 (balanced data: half the rounds have pressure that agrees with the goal) | One own adapter removed drift (0.858 → 0.050) without a shortcut; its given twin failed the shortcut check. | EXPL. |
| PREREG_F (6 vs 6, balanced, n 240; hypothesis formed after the data and labelled so) | No-reminder drift own 0.206 vs given 0.229 (p 0.64). It does not beat the untrained model *with* system reminders (0.182). Shortcut +0.072. Injection +0.04 to +0.07. | **FAIL** |

**Reading.**
- Small fine-tunes of either kind cut no-reminder drift, but not below plain reminders. The cut is about three quarters with 240 training examples and 20–38% with 16–48.
- They partly learn to oppose pressure rather than to follow the goal, and they make forged assistant-turn injections more effective.
- The training-data seed moved no-reminder drift from 0.08 to 0.32 within the own arm, and from 0.11 to 0.35 within the given arm.
- The pilots that suggested a role-specific benefit all shared one data seed. Their "consistent" pattern was one dataset seen several times.

## 10. Believe or obey? (EXPL., unfinished)

**The question.** Does the same role code govern credence in facts as it governs obedience to goals?

**Pilots on Qwen3-1.7B.** A matched "believe" arm used a fact sheet and false counter-claims.
- The first pilot was confounded: the goal drifted.
- The repaired pilot failed calibration (the claims were too strong) and narrowly failed validity (r = 0.46 between stated belief and action).

**Exploratory signals.**
- Repeating the fact sheet strongly protects belief against false claims.
- Whether the fact sheet is in the agent's own voice or given barely changes belief (≤ 0.03), against +0.08 for goal obedience in the same model.
- This leans toward separate codes for obeying and believing. It is not a finding.


## Fix-test pilot: NO-GO (2026-10-28 13:17 +04:00)

Recovered by restarting existing pod ilrvy2lnddoirw, then stopped after a verified local backup. Transfer MD5: 3499116f7d203e1abbff84c093cb9bd8. All 20 raw/scored files were complete: 180 prompts per model and condition, matched by task/order/conflict; 15 base tasks, 12 prompt variants per task. The full archive and a second short-path copy are saved.

| Model | Plain system success | Best steering | Gain | Emphasis baseline |
|---|---:|---:|---:|---:|
| Qwen3-8B | 8/180 (4.44%) | alpha 2: 12/180 (6.67%) | +2.22 percentage points | 13/180 (7.22%) |
| OLMo-2-7B | 42/180 (23.33%) | alpha 2: 42/180 (23.33%) | 0 | 43/180 (23.89%) |

No setting met the pre-set +3 percentage point gate. The planned confirmatory PREREG_N run is therefore **not launched**. Both models worsen at larger strengths: alpha 8 gives Qwen3-8B 4/180 (2.22%) and OLMo 6/180 (3.33%). This is a descriptive pilot finding, not a confirmatory test of harm.

Limits: this evaluates whole responses, while Control Illusion reports an acknowledgement-removal procedure; direct numerical equivalence to the published paper is not established. Repeated variants of the same base task should be treated as dependent in subsequent inference. Output length/degeneracy guards alone do not establish task usefulness. No claim of a working hierarchy or prompt-injection defence follows.


## Neutral-role decomposition diagnostic: NO-GO (2026-10-28T14:50+04:00)

Explicitly exploratory; one cached Qwen3-1.7B model, fixed layer 13, two base tasks with 12 variants each, and eight utility controls per condition. Directions were extracted from 36 neutral sentences with identical content tokens and positions checked across roles. R contrasts assistant against combined system/user; U contrasts user against system; the orthogonal U condition removes its R component. Vectors were norm matched. R was freshly extracted, not the exact archived vector used in previous studies.

| Condition | System successes | Utility successes |
|---|---:|---:|
| plain | 4/24 | 8/8 |
| emph | 3/24 | 8/8 |
| oldR2 | 3/24 | 8/8 |
| user2 | 3/24 | 8/8 |
| user4 | 4/24 | 8/8 |
| orth2 | 3/24 | 8/8 |
| pair2 | 4/24 | 8/8 |
| random2 | 3/24 | 8/8 |


No targeted condition improved on plain prompting, so none met the pre-set +10 percentage point screening gate against both plain and emphasis. No follow-on confirmatory run is launched from this pilot. The eight utility examples passed everywhere; this is a small screening check, not evidence of general utility retention.

The diagnostic does not rule out other layers, extraction procedures or value-cache interventions. It supplies no positive support for this fixed source-axis intervention. Two base tasks are the independent task count, not 192 independent conflict samples. One long interruption exhausted the first job's wall-clock allowance; completed conditions were retained and the interrupted condition was rerun from the beginning under unchanged settings. The interrupted checkpoint is preserved separately and excluded from the analysis.

Plan, script and data are saved in decomposition_pilot_codex. The plan and script hashes matched the manifest before analysis. All 256 final outputs were present (192 conflict responses and 64 small utility responses). The original fix pilot's NO-GO and PREREG_M's verdicts remain unchanged.

## 11. Limitations

- **Task.** One task family with synthetic pressure, and a construct that partly measures resistance to pressure (§2).
- **Models.** The strong causal effects are Qwen-centred. Sizes are ≤ 32B. No frontier models were tested.
- **One-axis generality.** All 9 models share one authority order, so the axis has only been shown to match that order, not to follow a different one. It predicts the order, not the spacing between roles.
- **Statistics.** Many exploratory contrasts. Every gate decision is preregistered, but the descriptive readings around ambiguous or failed gates are ours.
- **Context windows.** OLMo-2 results needed context-window restrictions (labelled) or shorter episodes.
- **Process.** The study was originally run end-to-end by Claude under time pressure and subsequently computationally rechecked and extended in Codex. Its pilots and post-hoc patterns misled it twice (§9), and only the sealed tests caught this.
- **Unfinished work.** The believe-or-obey scope test in the agent task (§10). PREREG_S addresses believing versus obeying on synthetic items (§6g).
- **Source-monitoring items (§6g–§6l) are synthetic.** They are fictional facts and passwords competing with one user message, read at the first answer word. The readout audit (§6j) shows that this word tracks what models write in all four tested models, though less tightly in OLMo (ρ 0.74).
- **The map is a patching map.** It shows where a source difference can be transferred, not every place it is used. The 32B models were patched at every second layer, and a few curves failed the sanity check and were excluded (§6l).
- **The lever (§6j–§6m) was chosen on four models.**
  - It transfers to SEP's tool-turn format in most families but to InjecAgent's embedded format only within Qwen.
  - Phi-4 is not selective, and in Granite and Phi-4 prompt defences can do as well.
  - The benchmarks are subsamples: 300 items or cases, and single agent steps rather than full multi-turn tasks.
  - OLMo and Granite produce valid ReAct replies in only about 30–45% of InjecAgent cases, which limits power there.
  - Trained defences (StruQ, SecAlign, TrustAttention) and V-Steer were cited, not re-run.
- **Random-direction controls are single draws.** Except PREREG_J (50 directions), every random control in this work is one isotropic draw of matched norm. That covers PREREG_S's edit, PILOT_V0, PREREG_V (H4), PREREG_X and Y (X5), the role-steering contrasts, PREREG_K and inj2.
  - An exploratory 32-draw check (RNDCTL, Qwen3-4B, in inj2's setup) found random-draw effects that flip sign with the draw and centre near zero, with an SD of 0.13–0.22 in first-token compliance.
  - One draw is therefore a weak control in both directions. "Beyond random" may overstate specificity, and "random did as well" may reflect one strong draw.
  - The fix is at least 16 draws with ± pairs, reporting the learned direction as a percentile of that distribution.
- **Operational re-runs.** Three benchmark jobs ran out of GPU memory when run concurrently. They were re-run alone with the same sealed commands before producing any data; the crash logs are kept. PREREG_V's item count was amended from 96 to 72 per kind before any data, after the item generator ran out of names.

## 12. What may be new, and what is not

**Candidate contributions, requiring explicit comparison with the additional prior art below:**
1. A direction extracted from role contrasts on neutral sentences changes goal adherence in the simulated trading task. It is strong in Qwen3 1.7B–14B. Its sign holds in three more families, at family-specific depth. A causal conversational-role direction has a close precedent in Tsui (2026), for self-correction. What is specific here is goal adherence over long horizons.
2. The natural own-vs-given discount grows with size in Qwen3 but not in OLMo-2, and it is reversed in SmolLM3.
3. In OLMo-2-7B the discount and its direction are present right after supervised chat fine-tuning.
   - Preference stages add no amplification at the preregistered threshold (p < 0.01), although the gap rises slightly (0.063 → 0.071 → 0.077).
   - In an exploratory pilot, the discount depends on template role tokens, not plain-text labels.
4. **A neutral-text role direction predicts the ordering of user, system and assistant goal placements in this task** (user > system > own).
   - ONE AXIS under seal in Qwen3-8B, Qwen3-14B and OLMo-2-7B.
   - PASS under seal in 6 more models (PREREG_I): 9 models, 4 families, 1.7B–32B, with 21 of 21 decided comparisons agreeing.
   - All 9 share the same order (§6b).
5. Negative results:
   - a deixis account refuted;
   - two preregistered fine-tuning fixes failed, with a documented shortcut and an injection cost.

**Not new:**
- role confusion as the cause of injection (Ye et al. 2026), and steering it (Zhang, Lee & Park 2026; Liu 2026, NeurIPS 2026 workshop);
- **a causal conversational-role direction:** Tsui (2026, COLM) reports a transferable conversational-role direction that causally gates self-correction. This is a close precedent for contribution 1;
- source-format cues are linearly decodable, while a pre-specified test for an abstract provenance code halted without interpretable evidence either way (Leong 2026, v2);
  - its v2 also reports that steering along its source-format direction did not move tool-name mention (0/1,895, mention-scored); the author notes this cannot rule out an effect on execution;
  - its OLMo-2 lineage material from v1 was not carried into v2;
- role relabelling changes self-correction (Chen et al. 2026: behavioural, 12 settings, no mechanism, no goals);
- goal drift itself (Arike et al. 2025; Menon et al. 2026) and reminders against long-horizon "behavioral state decay" (Wu et al. 2026);
- **annotating span authority through a non-text channel:**
  - Semantic Overlays (Penman 2026) trains adapters that mark spans as non-executable, and strongly reduces injection on five benchmarks (e.g. AlpacaFarm 99.0% → 0%, TensorTrust 34.8% → 6.2%);
  - any capability built on our role direction is a special, untrained case of that idea, applied in the opposite direction: raising the authority of the agent's own notes;
- steering for instruction-following (Stolfo et al., ICLR 2025: instruction-specific vectors) and against multimodal injection (Lu et al. 2026, ARGUS);
- agent skills stored as steering vectors (Zhao et al. 2026).
- **system prompts losing to user messages** (added 2026-10-28):
  - Geng et al. (Control Illusion, AAAI 2026) show behaviourally, in six models including GPT-4o and Claude 3.5, that system/user separation does not reliably enforce priority.
  - They also show that social framings (authority, expertise, consensus) influence behaviour more strongly than system/user roles do.
  - So our behavioural user > system order is consistent with known results. What may be new is the representational axis that orders it; their paper has no mechanistic analysis.
- **role conflicts dissected mechanistically:** Zeng (NeurIPS 2025 MechInterp Workshop, arXiv 2510.01228).
  - Linear probes show that system–user conflicts and social-cue conflicts occupy *distinct subspaces*.
  - Direct logit attribution shows stronger conflict detection for system–user conflicts, but consistent resolution only for social cues.
  - That models obey social cues while often ignoring the system-over-user hierarchy is earlier behavioural work, which Zeng extends.
  - Steering vectors built from social cues amplify instruction following regardless of role.
  - This is the closest mechanistic prior work to our one-axis claim, and it points against a single shared axis. PREREG_J tests the narrower question of whether social cues move the identical goal text along our role direction.
- **training the hierarchy:** Zheng et al. (2026, Findings of ACL) report about 20-point gains on system–user conflicts across families, from training. It is the reference point for any inference-time fix.
- **role identification through shortcuts:** Wang et al. (ICML 2025) find that fine-tuned models identify roles partly from task type and from proximity to the start of the text. In our design the reminder's position is the same for every role. Ye et al. (Appendix K) likewise find that token position, not tags, determines "systemness".
- **authority personas in sycophancy:** Joswin et al. (arXiv 2607.00415, 2026) find a graded authority effect localised to one layer. The effect is entangled with question content, and a mean "authority" vector failed to reproduce it. This contrasts with our content-free role direction, for goal text rather than beliefs.
- **a chat-template direction:** Maczan (arXiv 2609.25021, 2026) finds that the chat template switches a model's self-referential voice and that one activation direction reproduces the switch. This is related to our role direction, but has no link to authority or goals.

**Additional prior art verified in Codex (2026-10-28).**
- Zeng, Lee, Zhao and Hockenmaier, *Steering Instruction Hierarchies at Inference Time* (COLM 2026; https://arxiv.org/abs/2607.26228), already demonstrate training-free hierarchy interventions through selected value-cache edits. A new defence must compare against established interventions.
- Balp-Straffon et al., *How Language Models Choose Sides* (ICML 2026 MechInterp workshop; https://arxiv.org/abs/2608.28648), already show that readable conflict signals and causally effective directions can differ. Probe performance alone is not evidence of control.
- Ye et al. Appendix K already predicts instruction-hierarchy failures from role probes. The proposed monitoring tool therefore needs a narrower, explicit comparison.

**The source-monitoring line (§6g–§6n): what may be new, and what is not.**

*May be new:*
- **No single "who said this" tag.** One statement was placed in five sources, with obeying, believing and attributing measured on the same items. These behaviours rank the sources differently in most of 14 models from 7 families. This frames chat-model provenance as several readouts, not one tag, in the spirit of source monitoring in human memory (Johnson et al. 1993). The prior-art checks of 10-28 found no earlier three-behaviour comparison.
- **A behaviour-resolved patching map.** Role-word minimal pairs were patched by position set (marker, content, after the turn), by layer and by behaviour. The role-marker tokens carry the source in 92% of informative curves. At least two behaviours read it at different depths in 9 of 10 new models. The prior-art check found earlier patching of content-differing pairs (Kumarappan & Mujoo 2026) and of template-versus-instruction regions for harmfulness (Leong et al. 2025), but not this split by position and behaviour.
- **A selective, map-guided steering lever.** It lowers obedience to instructions in tool output while keeping belief in the tool's facts, in five of six models including two held-out families. It is tested against prompt defences, and stacked on them, on two public benchmarks.
  - Selectivity between obeying and using injected content is what the selective defences we found do not measure: TrustAttention (Shilov et al. 2026), DRIP (R. Liu et al. 2025), Semantic Overlays (Penman 2026) and CounterSteer (Russinovich 2026), which reports benign utility, not belief in the injected text's facts.
  - Its benchmark advantage holds in Qwen3-8B but not across families (§6m).

*Not new:*
- Steering against prompt injection and role confusion (Liu 2026; Zhang, Lee & Park 2026; Lu et al. 2026) and restoring instruction hierarchies at inference time (Zeng et al. 2026).
- **Training-free steering on tool-output tokens during prefill, across families, on AgentDojo** (CounterSteer; Russinovich 2026).
  - Five open models (8B–106B). AgentDojo compromise falls from 0.10–0.49 to 0.006–0.079 at 93–100% benign utility.
  - Its direction is fitted per model from paired episodes in which an injection was followed or resisted. Ours comes from 40 neutral sentences, with no injection data.
  - Its user-versus-tool role axis moved attack success in gpt-oss-20b but not in Qwen3-30B-A3B at matched dose. Our tool−user direction on the statement's tokens is strongest in dense Qwen models. Model, layer, token set and dose all differ, so the two results are not yet reconciled.
- **Readable role signals whose intervention directions transfer poorly across channels** (Yu et al. 2026, on AgentDojo trajectories). Our SEP-versus-InjecAgent gap is a case of this.
- That steering along random directions can raise compliance (Korznikov et al. 2025, *The Rogue Scalpel*, for jailbreaks). The injection setting and the sign-varying spread across draws (RNDCTL) are what we add.
- That prompt and datamarking defences vary across models (Hines et al. 2024; Zverev et al. 2025).
- Our lever is a different, selective variant of these interventions, built without injection data. Its contribution is the map that located it and the obey-versus-believe test, not steering against injection as such.

## Data, code and preregistrations

All code, seeds, result files, sealed preregistrations (`PREREG*.md` with `.sha256`) and archived cloud bundles (`bundles/`) are in `research_next/agent_goal_persistence/`. Cloud run and billing records are in `PLAN_7DAY.md`.

**Cloud cost.** The RunPod billing explorer, read 2026-10-29 at about 02:55 +04:00 (it lags about one hour), shows UTC daily totals of:
- $23.22 on 27 October;
- $52.10 on 28 October.

That is **about $75.3** for all cloud work through the end of PILOT_V1 (PREREG_Y then added about $18.4 from pod-time records: $9.62 and $8.77), plus about $0.02 a day for the 10 GB results volume. The local runs used the author's laptop GPU. The $17.43 reading in earlier drafts (2026-10-27 21:50 AST) was a partial snapshot.

**The source-monitoring line (§6g–§6n).** Each sealed test lists its files in its `.sha256` and has an archived bundle. The PREREG_V, W, X and Y analyses were run from the bundle's own copy, after the working files were checked against the seal:

| Test | Sealed files | Bundle |
|---|---|---|
| PREREG_S | 9 | `agp21` |
| PREREG_T | 9 | `agp22` |
| PREREG_U | 10 | `agp23` |
| PREREG_V | 14; amended before data | `agp27` (`agp26` is the hung first seal, which produced no data) |
| PREREG_W | 13 | `agp25` |
| PREREG_X | 15 | `agp28` |
| PREREG_Y | 18 | `agp30` |

**Exploratory pilots.** The pilots carry provenance hashes, not seals:
- PILOT_V0: `PILOT_V0.sha256`, `agp24`;
- PILOT_V1: `PILOT_V1.sha256`, `agp29`.

**Analyses and data:**
- Analyses:
  - PREREG_S–U: `cloud_prereg_{s,t,u}/*_analysis.json`, plus `cloud_prereg_s/s_jspace.json`;
  - the later tests: `cloud_*_analysis/*.json`.
- Raw outputs: the `cloud_prereg_*` and `cloud_v*` folders.
- Benchmarks: SEP and InjecAgent were cloned at commits 7606c06 and f19c9f2 and read as data only. The InjecAgent prompts were extracted by parsing, not import (`data/injecagent_prompts.json`).

## AI-use statement

Claude (Anthropic) designed, ran, analysed and wrote the original study. Codex (OpenAI) subsequently recovered and computationally rechecked PREREG_M and the fix pilot, ran the exploratory neutral-role decomposition diagnostic, checked reference-method software, expanded the prior-art comparison, and revised an earlier draft of the report. The study's direction, how agents keep or lose a goal and goal text given to the agent versus written in its own voice, was proposed by Claude on 2026-10-25. It built on the author's earlier papers and answered the author's request for the most promising next step; the author approved it. The question of where a text comes from was the author's (2026-10-28). The believe-versus-obey framing came from an AI-written plan the author commissioned (2026-10-27). The source-monitoring designs, the steering lever and the analyses were Claude's. Three other AI sessions proposed experiment plans that are described in the log; their suggestions were tested, not trusted. On 2026-10-28, two separate Claude sessions independently rechecked 168 numeric claims against the primary result files (re-running every sealed analysis script) and verified 32 references; their corrections were applied in Draft 7 of the report (`NUMBERS_RECHECK.md`, `REFERENCES_VERIFIED.md`). These are AI rechecks, not outside or human validation. The author did not independently check the code, analyses or technical claims. The author is responsible for the released content.

## References

Verified 2026-10-28 against arXiv, Crossref, publisher and venue pages (`REFERENCES_VERIFIED.md`). The model technical reports, LoRA, Holm and the benchmark papers were added the same day after a separate check (`REFERENCES_VERIFIED.md`, addendum). Granite 3.3 has no report of its own, so the Granite 3.0 report and the 3.3 model card are cited.

- Abdin, M., et al. 2024. Phi-4 Technical Report. *arXiv preprint*. arXiv:2412.08905.
- Ackerman, C., and Panickssery, N. 2025. Inspection and Control of Self-Generated-Text Recognition Ability in Llama3-8b-Instruct. *ICLR 2025*. arXiv:2410.02064.
- Allal, L. B., et al. 2025. SmolLM2: When Smol Goes Big -- Data-Centric Training of a Small Language Model. *arXiv preprint*. arXiv:2502.02737.
- Arditi, A., et al. 2024. Refusal in Language Models Is Mediated by a Single Direction. *Advances in Neural Information Processing Systems 37 (NeurIPS 2024)*, 136037–136083. arXiv:2406.11717.
- Arike, R., et al. 2025. Evaluating Goal Drift in Language Model Agents. *Proceedings of the AAAI/ACM Conference on AI, Ethics, and Society (AIES 2025)* 8(1): 192–203. doi:10.1609/aies.v8i1.36541. arXiv:2505.02709.
- Bakouch, E., et al. (Hugging Face). 2025. SmolLM3: smol, multilingual, long-context reasoner. *Blog post*, 8 July 2025. https://huggingface.co/blog/smollm3
- Balp-Straffon, E., et al. 2026. How Language Models Choose Sides: Internal Representations of Instruction Hierarchy. *ICML 2026 Mechanistic Interpretability Workshop*. arXiv:2608.28648.
- Chen, K.-Y., et al. 2026. The Self-Correction Illusion: Role Relabeling Gates Explicit Error Flagging in Large Language Models. *arXiv preprint*. arXiv:2606.05976.
- Debenedetti, E., et al. 2024. AgentDojo: A Dynamic Environment to Evaluate Prompt Injection Attacks and Defenses for LLM Agents. *Advances in Neural Information Processing Systems 37 (NeurIPS 2024), Datasets and Benchmarks Track*. arXiv:2406.13352.
- Falcon-LLM Team (TII). 2024. The Falcon 3 Family of Open Models. *Blog post*, 17 December 2024. https://huggingface.co/blog/falcon3
- G., A., and Lindsey, J. 2026. From Simulation to Enaction: Post-trained language models recognize and react to their own generations. *arXiv preprint*. arXiv:2605.25459.
- Geng, Y., et al. 2026. Control Illusion: The Failure of Instruction Hierarchies in Large Language Models. *Proceedings of the AAAI Conference on Artificial Intelligence (AAAI-26)* 40(36): 30816–30824. doi:10.1609/aaai.v40i36.40339. arXiv:2502.15851.
- Gurnee, W., et al. 2026. Verbalizable Representations Form a Global Workspace in Language Models. *Transformer Circuits Thread* (Anthropic), 6 July 2026. https://transformer-circuits.pub/2026/workspace/index.html
- Hines, K., et al. 2024. Defending Against Indirect Prompt Injection Attacks With Spotlighting. *Proceedings of the Conference on Applied Machine Learning in Information Security (CAMLIS 2024)*, CEUR Workshop Proceedings Vol. 3920, pp. 48–62. arXiv:2403.14720.
- Holm, S. 1979. A Simple Sequentially Rejective Multiple Test Procedure. *Scandinavian Journal of Statistics* 6(2): 65–70.
- Hu, E. J., et al. 2022. LoRA: Low-Rank Adaptation of Large Language Models. *International Conference on Learning Representations (ICLR 2022)*. arXiv:2106.09685.
- IBM Granite Team. 2024. Granite 3.0 Language Models. *Technical report*, October 2024. https://github.com/ibm-granite/granite-3.0-language-models/blob/main/paper.pdf
- IBM Granite Team. 2025. granite-3.3-8b-instruct. *Model card*, 16 April 2025. https://huggingface.co/ibm-granite/granite-3.3-8b-instruct
- Johnson, M. K., Hashtroudi, S., and Lindsay, D. S. 1993. Source monitoring. *Psychological Bulletin* 114(1): 3–28. doi:10.1037/0033-2909.114.1.3.
- Joswin, E., Medicherla, S., and Mammen, P. M. 2026. A Mechanistic View of Authority Hierarchy in LLM Sycophancy. *arXiv preprint*. arXiv:2607.00415.
- Korznikov, A., Galichin, A., Dontsov, A., Rogov, O. Y., Oseledets, I., and Tutubalina, E. 2025. The Rogue Scalpel: Activation Steering Compromises LLM Safety. *ICLR 2026 Workshop on Principled Design for Trustworthy AI* (poster). arXiv:2509.22067.
- Kumarappan, A., and Mujoo, A. 2026. Not Just RLHF: Why Alignment Alone Won't Fix Multi-Agent Sycophancy. *arXiv preprint*. arXiv:2605.12991.
- Leong, C. T., et al. 2025. Why Safeguarded Ships Run Aground? Aligned Large Language Models' Safety Mechanisms Tend to Be Anchored in The Template Region. *Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (ACL 2025), Volume 1: Long Papers*, 15212–15229. doi:10.18653/v1/2025.acl-long.738. arXiv:2502.13946.
- Leong, J. W. 2026. Instruction Self-Arbitration Is Not a Trust Boundary: Configuration-Dependent Tool Calls and External Enforcement in LLM Agents. *arXiv preprint* (v2, 17 October 2026). arXiv:2608.28502.
- Liu, E. 2026. Reducing Role Confusion via Activation Steering. *NeurIPS 2026 Workshop: The Third Workshop on Agents in the Wild: Safety, Security, and Beyond*. https://openreview.net/forum?id=aJceCDuUjM
- Liu, R., et al. 2025. DRIP: Defending Prompt Injection via Token-wise Representation Editing and Residual Instruction Fusion. *arXiv preprint*. arXiv:2511.00447.
- Lu, W., et al. 2026. ARGUS: Defending Against Multimodal Indirect Prompt Injection via Steering Instruction-Following Behavior. *CVPR 2026*. arXiv:2512.05745.
- Maczan, J. 2026. "As a Language Model...": Chat Template Switches LLM Self-Referential Voice and Activation Steering Reproduces It. *COLM 2026 Workshop on Efficient Reasoning; KONVENS 2026 Workshop on Evaluating LLMs for Specialized Domains (Eval4SD)*. arXiv:2609.25021.
- Martins, P. H., et al. 2024. EuroLLM: Multilingual Language Models for Europe. *arXiv preprint*. arXiv:2409.16235.
- Menon, A., et al. 2026. Inherited Goal Drift: Contextual Pressure Can Undermine Agentic Goals. *ICLR 2026 Lifelong Agents Workshop*. arXiv:2603.03258.
- Penman, J. 2026. Semantic Overlays: Mitigating Prompt Injection with Annotations Beyond Tokens and Steering Vectors. *arXiv preprint*. arXiv:2608.23873.
- Russinovich, M. 2026. CounterSteer: Suppressing Indirect Prompt Injection with Activation Steering. *arXiv preprint*. arXiv:2609.36570.
- Shilov, I., et al. 2026. Separating instructions from data as an attention problem. *NeurIPS 2026 Workshop: The Third Workshop on Agents in the Wild: Safety, Security, and Beyond*. https://openreview.net/forum?id=GPritQr2Ve
- Stolfo, A., et al. 2025. Improving Instruction-Following in Language Models through Activation Steering. *ICLR 2025*. arXiv:2410.12877.
- Tsui, K. 2026. Self-Correction Bench: Uncovering and Addressing the Self-Correction Blind Spot in Large Language Models. *COLM 2026*. arXiv:2507.02778.
- Wallace, E., et al. 2024. The Instruction Hierarchy: Training LLMs to Prioritize Privileged Instructions. *arXiv preprint*. arXiv:2404.13208.
- Walsh, P., et al. (Team OLMo). 2025. 2 OLMo 2 Furious. *Conference on Language Modeling (COLM 2025)*. arXiv:2501.00656.
- Wang, Z., et al. 2025. The Illusion of Role Separation: Hidden Shortcuts in LLM Role Learning (and How to Fix Them). *ICML 2025*, PMLR 267: 63200–63210. arXiv:2505.00626.
- Wu, Y., et al. 2026. Remember When It Matters: Proactive Memory Agent for Long-Horizon Agents. *arXiv preprint*. arXiv:2607.08716.
- Xu, S., et al. 2026. Behaving Better, Thinking Worse: Sycophancy Across Post-Training Stages. *NeurIPS 2026*. https://openreview.net/forum?id=IUAXqLsMTC
- Yang, A., et al. (Qwen Team). 2024. Qwen2.5 Technical Report. *arXiv preprint*. arXiv:2412.15115.
- Yang, A., et al. 2025. Qwen3 Technical Report. *arXiv preprint*. arXiv:2505.09388.
- Ye, C., Cui, J., and Hadfield-Menell, D. 2026. Prompt Injection as Role Confusion. *ICML 2026*, PMLR 306: 148172–148202. arXiv:2603.12277.
- Young, A., et al. (01.AI). 2024. Yi: Open Foundation Models by 01.AI. *arXiv preprint*. arXiv:2403.04652.
- Yu, Z., Xing, W., Yang, X., and Han, M. 2026. Readable Before Actionable: Causal Tracing of Indirect Prompt Injection. *arXiv preprint*. arXiv:2610.05295.
- Zeng, S. 2025. Who is In Charge? Dissecting Role Conflicts in Instruction Following. *NeurIPS 2025 Mechanistic Interpretability Workshop*. arXiv:2510.01228.
- Zeng, S., et al. 2026. Steering Instruction Hierarchies at Inference Time. *COLM 2026*. arXiv:2607.26228.
- Zhan, Q., et al. 2024. InjecAgent: Benchmarking Indirect Prompt Injections in Tool-Integrated Large Language Model Agents. *Findings of the Association for Computational Linguistics: ACL 2024*, pp. 10471–10506. arXiv:2403.02691.
- Zhang, K., Lee, D., and Park, J. 2026. Steering Role Confusion. *LessWrong*, 20 August 2026. https://www.lesswrong.com/posts/uz9pFutDAT7trygM9/steering-role-confusion
- Zhao, C., et al. 2026. Neural Procedural Memory: Empowering LLM Agents with Implicit Activation Steering. *arXiv preprint*. arXiv:2606.29824.
- Zheng, Z., et al. 2026. Reasoning Up the Instruction Ladder for Controllable Language Models. *Findings of the Association for Computational Linguistics: ACL 2026*, 39332–39354. doi:10.18653/v1/2026.findings-acl.1960. arXiv:2511.04694.
- Zverev, E., et al. 2025. Can LLMs Separate Instructions From Data? And What Do We Even Mean By That? *International Conference on Learning Representations (ICLR 2025)*. arXiv:2403.06833.
