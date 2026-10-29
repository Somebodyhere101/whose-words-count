# Whose words count? Chat role and partial control of goal adherence

**Draft 7, 2026-10-28** (adds PREREG_S; corrections from an independent recheck of 168 numeric claims, `NUMBERS_RECHECK.md`, and of every reference, `REFERENCES_VERIFIED.md`). [Author.] This is an AI-run study; see the AI-use statement at the end.

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
- a set of clean negative results, including the failure of an obvious fine-tuning fix.

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
- Statistics are paired by seed (same seed, same world): sign-flip permutation tests, Holm corrections where preregistered, and same-norm random-direction controls for every steering contrast.
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
- α = 2 unless noted. The control is a same-norm random direction.

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

**Design.** As in directional ablation (Arditi et al. 2024), the unit role direction is projected out of the embedding and every layer output while the reminder is read. A random direction, ablated the same way, is the control. The test ran on Qwen3-4B, 8B, 14B and 32B and on OLMo-2-7B, on fresh seeds.

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

**Verification.** The six sealed hashes matched the archived agp19 bundle or the preregistration. All 120 result files contain the expected 60 unique seeds (2000–2059). Transfer MD5: 2ceefa5a34f4f7762a233f6024b06f73. Codex reran the sealed analysis and separately recomputed the descriptive differences from raw data. This is a computational recheck by another AI, not outside or human validation. Sources: cloud_prereg_m/m.json and m_descriptive_check.json.

## 7. Accounts that failed

- **Deixis (FAIL, preregistered, Qwen3-4B and 1.7B).** The account: the discount follows first-person commitments. Instead, under +vR "I'll…" payloads are suppressed as much as other payloads or more: the most in Qwen3-4B, while in Qwen3-1.7B's system placement "You will" drops more (−0.83 vs −0.69). So the dial is pronoun-blind.
- **Addressee (INCONCLUSIVE, preregistered).** The account: text addressed to the model gets authority. The projection difference was −0.22 and −0.15 of the role gap, opposite in sign to the prediction but under the bar.
- **A lesson.** Three strong language models proposed these accounts independently and agreed. The experiments disagreed.

## 8. Injection: role steering blocks it (REPL.)

**Result (PASS on Qwen3-4B).** The direction is added to an injected instruction inside a document. Compliance falls from 0.209 to 0.000; the random control gives 0.642. The legitimate instruction rises from 0.79 to 1.00, and replies stay on-task in 24/24 cases.

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
- **Unfinished work.** The believe-or-obey scope test.

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

## Data, code and preregistrations

All code, seeds, result files, sealed preregistrations (`PREREG*.md` with `.sha256`) and archived cloud bundles (`bundles/`) are in `research_next/agent_goal_persistence/`. Cloud run and billing records are in `PLAN_7DAY.md`. The $17.43 billing reading at 2026-10-27 21:50 AST is a historical snapshot, not the total through 28 October. Reconcile the complete study cost before release.

## AI-use statement

Claude (Anthropic) designed, ran, analysed and wrote the original study. Codex (OpenAI) subsequently recovered and computationally rechecked PREREG_M and the fix pilot, ran the exploratory neutral-role decomposition diagnostic, checked reference-method software, expanded the prior-art comparison, and revised this unpublished draft. The author set the questions and the direction and did not independently check the technical content. Three other AI sessions proposed experiment plans that are described in the log; their suggestions were tested, not trusted.

## References (partly verified; complete and check before release)

- Zeng, S., Lee, S., Zhao, H., and Hockenmaier, J. 2026. Steering Instruction Hierarchies at Inference Time. COLM 2026. https://arxiv.org/abs/2607.26228
- Balp-Straffon, E., Hsu, C.-H., Gadhvi, R., Dev, S., McDougall, C. S., and Mujumdar, A. 2026. How Language Models Choose Sides: Internal Representations of Instruction Hierarchy. ICML 2026 Mechanistic Interpretability workshop. https://arxiv.org/abs/2608.28648

- Arike et al. 2025: goal drift in language-model agents.
- Wallace et al. 2024: The Instruction Hierarchy.
- Ye, Cui & Hadfield-Menell 2026: Prompt Injection as Role Confusion (ICML; arXiv 2603.12277).
- Steering Role Confusion (LessWrong, 2026).
- Reducing Role Confusion via Activation Steering (NeurIPS 2026).
- Chen et al. 2026: The Self-Correction Illusion (arXiv 2606.05976).
- Tsui 2025: Self-Correction Bench (arXiv 2507.02778).
- Leong 2026: Instruction Self-Arbitration Is Not a Trust Boundary (arXiv 2608.28502).
- Arditi et al. 2024: refusal is mediated by a single direction.
- Xu & Daneshjou 2026: sycophantic follow-through across post-training stages (NeurIPS 2026).
- Menon et al. 2026: inherited goal drift.
- Penman 2026: Semantic Overlays: Mitigating Prompt Injection with Annotations Beyond Tokens and Steering Vectors (arXiv 2608.23873). Abstract read.
- Lu et al. 2025: ARGUS: Defending Against Multimodal Indirect Prompt Injection via Steering Instruction-Following Behavior (arXiv 2512.05745). Abstract read.
- Stolfo et al. 2025: Improving Instruction-Following in Language Models through Activation Steering (ICLR; arXiv 2410.12877).
- Neural Procedural Memory: Empowering LLM Agents with Implicit Activation Steering (arXiv 2606.29824).
- Remember When It Matters: Proactive Memory Agent for Long-Horizon Agents (arXiv 2607.08716).
- Geng et al. 2026: Control Illusion: The Failure of Instruction Hierarchies in Large Language Models (AAAI; arXiv 2502.15851). Read (HTML v4): models, system/user adherence, social framings; data at github.com/yilin-geng/llm-instruction-conflicts.
- Zeng 2025: Who is In Charge? Dissecting Role Conflicts in Instruction Following (NeurIPS 2025 MechInterp Workshop; arXiv 2510.01228). Abstract read.
- Reasoning Up the Instruction Ladder for Controllable Language Models (ACL Findings 2026 / ICML 2026). Search summary only; read before citing numbers.
- Wang, Jiang, Yu & Huang 2025: The Illusion of Role Separation: Hidden Shortcuts in LLM Role Learning (ICML; arXiv 2505.00626). Abstract read.
- Joswin, Medicherla & Mammen 2026: A Mechanistic View of Authority Hierarchy in LLM Sycophancy (arXiv 2607.00415). Abstract page read.
- Maczan 2026: "As a Language Model...": Chat Template Switches LLM Self-Referential Voice and Activation Steering Reproduces It (arXiv 2609.25021). Abstract read.
