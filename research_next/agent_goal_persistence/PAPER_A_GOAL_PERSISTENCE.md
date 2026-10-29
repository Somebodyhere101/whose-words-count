# Whose words count? Chat role and partial control of goal adherence

Sam Ramdan (ORCID 0009-0004-7723-4240)

Preprint v1, 2026-10-29. DOI: [10.5281/zenodo.23758885](https://doi.org/10.5281/zenodo.23758885). Paper A of two: the companion Paper B, *Who said this? Most chat models weigh a text's source differently for each behaviour, and a steering lever against injected instructions* ([10.5281/zenodo.23758887](https://doi.org/10.5281/zenodo.23758887)), covers the source-monitoring tests. Both papers were split from one technical report, released with the code and data as `PAPER_DRAFT.md` (https://github.com/Somebodyhere101/whose-words-count). This is an AI-run study; see the AI-use statement before the References.

Every claim carries its status:
- **PASS** or **FAIL:** a preregistered gate, hash-sealed before data;
- **a named verdict** of a sealed rule, such as ONE AXIS, AMBIGUOUS, MIXED, PARTIAL, NO_TREND, INCONCLUSIVE or DOES_NOT_TRACK;
- **PASS/FAIL (log gate):** a gate written in the dated plan log (`PLAN_7DAY.md`) before data, without a hash seal. This applies to stages 1–3: the fast instrument (§3), the representation test (§4), and the Qwen3-1.7B and 32B steering rows (§5). The deixis, addressee and injection tests (§7–§8) also have their rules in the log, but their scripts are hash-sealed;
- **EXPL.:** exploratory, no gate;
- **REPL.:** a replication of prior work.

Numbers come from the result files listed in `CONSOLIDATED_RESULTS.md`. Every deviation from plan is logged in `PLAN_7DAY.md`. Both files are in the public repository (see Data, code and preregistrations).

## Abstract

Agents are often given their goal as text, and the same sentence can arrive as a system instruction, a user message, or the agent's own earlier note.

**Behaviour.** In a simulated portfolio-manager task with pressure toward high-emission stocks, the identical goal reminder is followed less when it sits in the agent's own (assistant) turn than in a system turn.
- The gap passed two preregistered tests in Qwen3-1.7B on the sequential instrument, which generates every reply (+0.18, then +0.11 with a confound removed, in the share of high-emission picks).
- On the fast instrument, which reads choice probabilities, it grows with size across Qwen3, from +0.005 at 1.7B to +0.144 at 32B (exploratory, and confounded by headroom: at 1.7B the fixed text drives drift to the floor). A sealed size test across 15 models in four families found no general trend in goal holding or in source sensitivity (NO_TREND); source sensitivity rises with size only within the Qwen lineage.
- Outside Qwen it is clear in OLMo-2-7B, small in Granite-3.3-8B, and reversed in SmolLM3-3B.

**Mechanism.** A "role direction" is the mean difference between the activations of neutral sentences placed in assistant turns and in system/user turns. Added to the goal text alone, it moves goal adherence in both directions:
- strongly in Qwen3 1.7B–14B (one pass on a gate logged before data; the same gate was met at three more sizes);
- in three other families with the same sign at a family-specific depth: one preregistered pass and two weak effects.

**Origin.** In the open OLMo-2 lineage, the discount and the role direction are already present after supervised chat fine-tuning at 7B, the first stage that could be tested. The preregistered combined verdict across 7B and 13B is ambiguous, because the 13B gap is tiny. In an exploratory pilot (one model, 20 seeds), the discount was not detected when roles were written as plain-text labels (+0.013, n.s.), suggesting that it depends on the template's role tokens.

**What it is not.**
- The tested probes found no self-specific "this is mine" representation; this does not establish that none exists.
- A first-person (deixis) account failed its sealed test in two small Qwen3 models.
- Using the same direction against prompt injection replicates prior work.

**One axis.** On a cleaner task that separates following the goal from resisting pressure, the order user > system > own replicates under seal in three models from two families. The reminder's projections on the role direction fall in the same order as the placements are obeyed (ONE AXIS, 3/3). This match is correlational (§6b).
- **A sealed test in six more models passed:** four families, 1.7B to 32B. The direction's order matched behaviour in all 15 decided pairwise comparisons (three pairs per model, as preregistered), with none against.
- **Its limit:** every model showed the same order, so whether the axis would follow a model with a different order is untested.
- **Three further sealed tests sharpen the claim.**
  - Removing the direction narrows the user − own spread by 27–44% in three Qwen models, but not in OLMo (PARTIAL). It also weakens the reminder's overall effect by 22–36%; per unit of that effect, the spread narrows by about a quarter in Qwen3-4B and 8B and not at all in Qwen3-32B.
  - In a social-cue test, status headers move text toward the "own" end of the direction in six of seven models, but obedience follows only in the three smallest models, where size and family are confounded (MIXED). Text framed as citing a Nature study was obeyed less than text framed as citing a blog in 12/12 decided comparisons (reported, not gating).
  - In a test that describes the goal as the model's own plan or analysis, the text framed this way was followed more than the same text framed as another manager's plan or a colleague's analysis, in five of six models (MIXED). The role direction did not track these framing effects (4 of 11 agree; DOES_NOT_TRACK). An exploratory follow-up in one model traces most of the difference to a discount on another manager's plan.

**Two preregistered attempts to fix the discount by fine-tuning both failed.** Small fine-tunes reduce drift, but not below plain reminders. They partly learn to oppose pressure rather than to follow the goal. On average they also make forged assistant-turn injections slightly more effective (+0.02 to +0.07 in the two sealed tests; not tested for significance, and not in every adapter).

We report the negative results in full.

## 1. Introduction

**The problem.**
- Long-running agents drift from their goals under pressure (Arike et al. 2025).
- Chat models assign different authority to text depending on its role, a property that instruction-hierarchy training tries to shape (Wallace et al. 2024).
- Agents increasingly keep their goals and plans in their own earlier messages: notes, scratchpads, memory.

**Our question:** is goal text in the agent's own voice weaker than the same text given to it, and if so, why?

**Contributions:**
- an instrument that measures it cheaply;
- a scale trend in Qwen3 (exploratory), which a sealed size test across four families did not find in general (§6e);
- a causal handle with its cross-family limits;
- its presence at the earliest testable training stage (supervised fine-tuning) in one open lineage;
- a role direction whose ordering of user, system and own goal text matches how the models obey them, under seal in 9 models from 4 families (a correlational match; §6b);
- a set of clean negative results, including the failure of an obvious fine-tuning fix.

**The closest prior work.**
- **Role confusion.** Ye et al. (2026) show that role confusion drives prompt injection, and that models infer a text's role from how it sounds rather than from its role tag. Follow-ups steer it (Zhang, Lee & Park 2026; Liu 2026).
- **Relabelling text.** Chen et al. (2026) show that relabelling the role of byte-identical text changes self-correction.
- **A causal role direction.** Tsui (2026) reports a transferable conversational-role direction that causally gates self-correction. This is the closest precedent for our role direction.
- **Provenance.** Leong (2026, v2) finds source-format cues linearly decodable. Its pre-specified test for an abstract provenance representation halted without interpretable evidence either way.

Our injection results replicate the steering follow-ups. What may be new:
- the role direction's causal control of long-horizon goal adherence;
- its scale and family profile;
- its presence at the earliest testable training stage in an open lineage.

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

**Two instruments.**
- **Sequential instrument** (the main run and run B in §3; Qwen3-1.7B only). Episodes run one at a time, and every reply is generated in full. The outcome is the share of parsed test steps whose pick is a high-emission ticker.
- **Fast instrument** (every other result). Episodes are batched and use compact quarter texts, and the choice is read from probabilities:
  - at each test step, one forward pass up to "ALLOCATE:" gives the probability of each listed ticker; the first tokens are distinct;
  - p_hi is the renormalised probability of the two high-emission tickers;
  - the pick is then sampled, so the history stays the agent's own behaviour;
  - the outcome is mean p_hi over test steps, and lower means more adherence.
- Before use, the fast instrument had to reproduce the sequential instrument's directions on Qwen3-1.7B (§3).

**Engineering and statistics.**
- Batched episodes share one KV cache, with per-sequence positions.
- Each step's logical context length is recorded, so context-window validity can be checked: OLMo-2's 4,096-token window forced shorter episodes.
- Statistics are paired by seed (same seed, same world): sign-flip permutation tests, Holm (1979) corrections where preregistered, and same-norm random-direction controls for every steering contrast. Each control is a single isotropic draw; only the projection tests of PREREG_J and PREREG_M use a null of 50 random directions. See Limitations.
- Preregistrations are sha256-sealed before data. The exact code bundles sent to each cloud run are archived and verified against the seals.

**Construct caveat (EXPL.).** In a control world where low-emission stocks grow fastest, so that growth pressure *agrees* with the goal, OLMo-2-7B-Instruct's system reminder *raises* high-emission picks (0.088 → 0.277). The task's "goal adherence" therefore partly measures resistance to the pressure emails. All own-vs-given comparisons hold the reminder text fixed and vary only its role, so they compare the same text across roles. Whether the role changes the goal's authority or only the reminder's push against the pressure is separated only in the cleaner world of §6b. The construct should still be read as *adherence to the stated goal against pressure*.

## 3. Behaviour: the same goal text is weaker in the agent's own voice

**Models.** Qwen3 (Yang et al. 2025), OLMo-2 (Walsh et al. 2025), Granite-3.3 (IBM Granite Team 2024, 2025), SmolLM3 (Bakouch et al. 2025), SmolLM2 (Allal et al. 2025) and EuroLLM (Martins et al. 2024).

**Qwen3-1.7B, sequential instrument, 40 seeds per cell.**

| Test | Result | Status |
|---|---|---|
| Main 2×2 (PREREG) | Own notes drift more than a fixed reminder (H1, p 0.0001). The same fixed text in the agent's own turn is followed less (H2, +0.18, p 0.025). The own cells also contained the note-request text, a confound. | PASS (H1, H2) |
| Run B (PREREG_B), confound removed | H1 PASS (p_Holm 0.0001). H2 +0.11 (p_Holm 0.037; own worse in 26 of 35 non-tied seeds). The notes-framing contrast S1 was not detected. | PASS |

**Fast instrument (stage-1 gate).** On Qwen3-1.7B (n 40) it reproduces the three directions that the gate, logged before data, required: own notes drift more than the fixed reminder (H1), the fixed text is followed less in the agent's own turn (oF > gF, H2), and a reminder beats none (1 > gF). Mean p_hi (lower means more adherence):

| Cell | 1 | gF | oF | gN | oN |
|---|---|---|---|---|---|
| p_hi | 0.96 | 0.041 | 0.046 | 0.82 | 0.84 |

Status: PASS (log gate).

**Scale and families (fast instrument, 40 seeds; seed counts are positive/negative).** EXPL. unless marked.

| Model | own − given, fixed text (p_hi; positive = own followed less) | Given cell gF (p_hi) | Note |
|---|---|---|---|
| Qwen3-1.7B | +0.005 (28/12) | 0.041 | weak text: +0.107 (40/0) |
| Qwen3-4B (4-bit) | +0.021 (37/3) | 0.333 | |
| Qwen3-8B | +0.028 (33/7) | 0.233 | |
| Qwen3-14B | +0.110 (40/0) | 0.148 | |
| Qwen3-32B | +0.144 (37/3) | 0.638 | |
| OLMo-2-7B-Instruct | +0.079 (35/5) | 0.185 | scored on steps inside the 4,096-token window (post hoc); all steps of the same run +0.082 |
| OLMo-2-13B-Instruct | +0.008 | 0.127 | from PREREG_D (§6), 80 seeds |
| Granite-3.3-8B | +0.006 (p 0.046) | 0.067 | n.s. once low-mass steps are excluded |
| SmolLM3-3B | −0.014 (p 0.03) | 0.214 | reversed |
| SmolLM2-1.7B, EuroLLM-1.7B, OLMo-2-1B | — | — | do not respond to the goal at all (uninformative) |

**Reading.**
- The own-voice discount is common but not universal.
- In Qwen3 the fixed-text gap grows with size (exploratory), but the series is confounded by headroom. At 1.7B the fixed text drives p_hi to the floor (gF 0.041); with the weak text the same model's gap is +0.107, close to 14B's +0.110. The 4B run used 4-bit weights, and the top of the series, Qwen3-32B, holds goals unusually weakly (§6e). The sealed size test in §6e found no general size trend in goal holding or source sensitivity. In OLMo-2 the gap does not grow (PREREG_D: 7B Instruct +0.077 vs 13B +0.008).
- In every model that can do the task, the agent's own notes drift more than the fixed reminder in the same own turn (oN − oF from +0.13 at Qwen3-32B to +0.80 at Qwen3-1.7B). The notes are a different text, without the action rule, so this contrast is about content, not voice.

## 4. Representation: the tested probes found no self-specific "this is mine" tag (FAIL, log gate, Qwen3-1.7B; the control transfers as well or better in 9 more models)

**The test.** A probe trained to separate a sentence placed in the assistant turn from the same sentence in system/user turns was tested on attribution inside one user turn: "Earlier you wrote: …" vs "Your manager wrote: …". It must transfer at AUC ≥ 0.8 in both directions, at least 0.15 above a system-vs-user control.

**Result.**
- It fails in Qwen3-1.7B (0.80/0.796, control gap 0.12).
- The control transfers as well or better in SmolLM2, EuroLLM, Qwen3-4B, 8B, 14B, 32B, SmolLM3, OLMo-2-7B and Granite-3.3-8B.
- The role probe does transfer to attribution in Qwen3-1.7B (AUC about 0.80), but a system-vs-user control transfers nearly as well there (0.12 lower) and as well or better in the nine other models. The shared signal is therefore largely not specific to own-versus-given.

**Parallel.** Leong's pre-specified test for an abstract provenance representation (2026, v2; §1) halted without interpretable evidence either way; its v1 had claimed absence. Our negative result is therefore a separate, limited data point.

## 5. Mechanism: one role direction moves adherence in both directions

**Method.**
- vR is the difference of means computed in the representation test (§4): neutral sentences as assistant turn minus the same sentences as system/user turns, per layer, on the training split.
- While the goal reminder is read, we add −α·vR to own-turn reminders ("push toward given") or +α·vR to system-turn reminders ("push toward own").
- α = 2 unless noted. The control is one same-norm random direction (a single draw).
- Lower p_hi means more adherence. Beyond-random values are signed so that positive means the predicted direction.

| Model | Layer (depth) | Own text pushed toward given (p_hi) | Given text pushed toward own (p_hi) | Beyond random | Status |
|---|---|---|---|---|---|
| Qwen3-1.7B, weak text | 13 (0.46) | 0.772 → 0.634 | 0.658 → 0.815 | +0.086 / +0.072, Holm p 0.0001 | **PASS** (log gate) |
| Qwen3-4B | 17 (0.47) | 0.386 → 0.276 | 0.347 → 0.482 | +0.170 / +0.116 | EXPL. (gate met) |
| Qwen3-8B | 17 (0.47) | 0.306 → 0.154 | 0.258 → 0.580 | +0.21 to +0.30 | EXPL. (gate met) |
| Qwen3-14B | 18 (0.45) | 0.302 → 0.133 | 0.179 → 0.434 | +0.27 to +0.32 | EXPL. (gate met) |
| Qwen3-32B | 29 (0.45) | 0.881 → 0.838 | 0.747 → 0.770 | +0.040 / n.s. | **FAIL** (log gate). An exploratory sweep of 5 layers at 0.31–0.58 depth gives shifts of 0.02–0.10 per layer and direction, all of the predicted sign; 2 of these 10 contrasts are n.s. against random |

The gate logged before data was written for Qwen3-1.7B. The other sizes were scored against the same bar: 4B–14B met it, as exploratory replications, and 32B did not.

**Shared features.**
- About 0.2 depth is not uniformly inert:
  - in Qwen3-1.7B, layer 5 gives +0.060 / +0.142 beyond random (p ≤ 0.0001);
  - in Qwen3-8B, layer 7 gives small raw shifts (+0.02, p ≤ 0.0003) but none beyond random;
  - 4B, 14B and 32B are null there.

  The tests above use about 0.45 depth.
- α = 1 gives about half the effect.
- Ticker mass, a measure of format integrity, is unchanged.
- At 14B, own text pushed toward "given" is followed better than real system text (0.133 vs 0.179).

**Other families, PREREG_C.** The first tests at Qwen's layer depths failed: there were small effects at about 0.2 depth and none at about 0.45. In an exploratory depth sweep (seeds 400–419), a selection rule sealed in advance chose one layer per family; a sealed test then checked that layer on 40 fresh seeds (500–539):

| Model | Layer (depth) | Toward given (Δp_hi) | Toward own (Δp_hi) | Beyond random | Verdict |
|---|---|---|---|---|---|
| SmolLM3-3B, weak text | 7 (0.19) | −0.053 | +0.127 | +0.065 / +0.126 | **PASS** |
| OLMo-2-7B, fixed text | 10 (0.31) | −0.047 | +0.075 | +0.053 / +0.074 | present but weak (bar 0.05) |
| Granite-3.3-8B, weak text | 10 (0.25) | −0.018 | +0.035 | +0.038 / +0.038 | present but weak (near floor) |

**Reading.**
- By the sealed table, 1 PASS of 3 means the *strength* is family-dependent.
- The predicted *sign* holds in all four families. Each beyond-random test compares with one random draw (p_Holm 0.00015 against that draw). Outside Qwen the margins over that draw (+0.04 to +0.13) are no larger than the spread of single random directions in RNDCTL (SD 0.13–0.22, in the injection task of §8), so specificity outside Qwen is not established.
- The best depth is family-specific: Qwen about 0.46, OLMo 0.31, Granite 0.25, SmolLM3 0.19.
- SmolLM3 passes although its natural gap is reversed. So the natural gap is not simply the projection of the reminder onto vR; other role differences contribute.

## 6. Origin: the discount is present at the first testable stage, supervised fine-tuning (AMBIGUOUS, PREREG_D)

**Design.**
- Lineage: OLMo-2 SFT → DPO → Instruct (RLVR) at 7B and 13B.
- Native template; all six checkpoints share a byte-identical chat template.
- Cells 1/gF/oF/uF; 80 fresh seeds.
- Gate: competence (p(1) − p(gF) ≥ 0.05, p < 0.01).
- Values below are own − given in p_hi (positive = own followed less).

| Size | SFT | DPO | Instruct | Verdict by rule |
|---|---|---|---|---|
| 7B, own − given | **+0.063** (69/11) | +0.071 (76/4) | +0.077 (75/5) | H-SFT: arrives at SFT; no amplification at p < 0.01 (DPO +0.009, p 0.16; Instruct +0.005, p 0.031) |
| 13B, own − given | +0.0075 | +0.0066 | +0.0081 | H-pref by threshold only: a tiny, flat gap; only the final stage crossed p < 0.01 |

**Verdict.** The combined verdict is **AMBIGUOUS**. The rule lacked a minimum effect size, which we note as a design weakness.

**Descriptive reading.**
- At 7B, 82% of the final gap is present right after SFT.
- The role direction at layer 10 has cosine 0.994 between SFT and Instruct.
- The raw gap rises slightly (0.063 → 0.071 → 0.077), while the gap relative to the reminder's effect is highest after SFT: 0.133, against 0.106 after DPO and 0.113 after Instruct.
- The 13B verdict (H-pref) rests on a flat gap of 0.007–0.008 that crossed p < 0.01 only at the last stage. We do not read it as a preference-tuning origin. Xu et al. (2026) also trace a behaviour, sycophancy, across post-training stages.

**Pilots (EXPL.).**
- OLMo-2 base models (1B, 7B) do not respond to a goal reminder in a plain transcript, so a pretraining origin could not be tested.
- With plain "SYSTEM:/ASSISTANT:" labels instead of template tokens, OLMo-2-7B-Instruct's discount was not detected (+0.013, n.s.; 20 seeds), against +0.080 in its native format in the same pilot. This suggests that the discount depends on the template's role tokens. It contrasts with Ye et al. (2026), who find that internal role perception follows style and position rather than tags. The measures differ: they use probes, we measure a behavioural discount.
- **Authority order in OLMo-2, every stage and both sizes: user > system > own.** A user-turn reminder is followed best: uF − gF in p_hi is between −0.05 and −0.12 (negative = user followed more), p 0.0001.

## 6b. One axis for all three roles (PASS, PREREG_H and PREREG_I)

**A cleaner construct.** The construct caveat (§2) motivated a world that separates the three behaviours. Each quarter offers:
- a **goal pick:** low emission, low growth;
- a **pressure pick:** high emission, highest growth;
- a **contrarian trap:** high emission, lowest growth;
- a **filler.**

On this world (PREREG_G, 60 fresh seeds; EXPL., replicated under seal in PREREG_H), the own-voice discount holds in three models. Contrarian picks stay near zero in Qwen (≤ 0.003) and at a steady 0.11–0.12 in OLMo-2-7B in every reminder cell. So steering and roles move picks between the pressure option and the goal, not toward the trap.

| Model | system − own on p_goal (positive = system followed more) |
|---|---|
| Qwen3-8B | +0.030 |
| Qwen3-14B | +0.058 |
| OLMo-2-7B | +0.089 |

All three are at p 0.0001.

**The authority order (PASS, replicated under seal in PREREG_H on fresh seeds).** The identical goal reminder is followed most as a **user** turn, then as a **system** turn, then as the agent's **own** turn:

| Model | user − system (p_goal) | system − own (p_goal) |
|---|---|---|
| Qwen3-8B | +0.045 | +0.024 |
| Qwen3-14B | +0.022 | +0.061 |
| OLMo-2-7B | +0.108 | +0.061 |

All Holm p ≤ 0.00025.

**Replication on fresh seeds (EXPL., MPILOT; Qwen3-8B, 40 paired seeds; predictions hashed before launch).** MPILOT is an exploratory follow-up to PREREG_M (§6f). As in PREREG_H, every placement's reminder is inserted at the same steps and at the same point in each step, with no header, so only the role differs. The system-turn copy is again followed more than the assistant-turn copy: +0.028 [0.013, 0.046], 36 of 40 seeds, close to PREREG_H's +0.024. Because position is matched, the own-turn discount in this model is not an artefact of where the reminder sits.

**One axis (PASS: ONE AXIS in 3/3 models).** We projected the reminder's own tokens (byte-identical across roles) onto the unit role direction. In every model the projections order the placements as the agents obey them: user text furthest toward "given", then system, then own. Higher projection means nearer the "own" end. The user-versus-system part is not independent of how the direction is built: with vR = assistant − mean(system, user), system text projects above user text whenever system-turn states lie closer to assistant-turn states, and for the neutral sentences vR was built from, this follows exactly. The match with behaviour is therefore correlational.

| Model | system − user projection | own − system projection |
|---|---|---|
| Qwen3-8B | +2.12 (58/2 seeds) | +1.34 (60/0) |
| Qwen3-14B | +1.74 (60/0) | +1.33 (60/0) |
| OLMo-2-7B | +0.38 (60/0) | +0.12 (60/0) |

**Reading.**
- One learned, content-free direction orders goal text in all three chat roles as the models obey it, in two families; the match is correlational.
- Moving along it shifts adherence causally (§5; PREREG_G).
- The axis orders placements, not individual episodes, at least in Qwen. If it set adherence episode by episode, projection and p_goal would correlate negatively within a placement (text nearer "own" followed less). OLMo shows this in all three placements (−0.251, −0.415 and −0.313). Qwen3-14B shows the opposite in all three (+0.267, +0.267 and +0.424), and Qwen3-8B in two of three; its user cell (−0.147) has the predicted sign (exploratory).
- **A practical corollary:** a plain user-turn reminder beat steering the agent's own note (PREREG_G: FAIL for the steering capability). Steering a system-turn reminder further along the axis beat even the user placement in Qwen3-14B only.

**Generality (PASS, PREREG_I).** Six models not tested before in this world, fresh seeds 1500–1559 (32B: 1500–1539).
- **Families:** Qwen3, SmolLM3, Granite and OLMo-2.
- **Direction and layer:** each model uses its own direction at a layer fixed before the data. OLMo-2-13B's direction was computed in the same run. Qwen3-4B's direction came from the earlier 4-bit representation run (§4), while this run used bf16 weights; this was logged at sealing.
- **Rule:** each model contributes three pairs: user − system, system − own and user − own. A pair counts as decided when the behavioural difference is significant. It agrees when the projection difference has the matching sign at p < 0.05.
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
- **15 of the 18 pairs were decided and all 15 agree** (agree rate 1.0). The three undecided pairs are system − own in SmolLM3, Granite and OLMo-2-13B.
- **Adjacent pairs only.** User − own follows from the other two pairs, so it is not independent evidence. Counting only user − system and system − own, 9 of 12 pairs are decided and all 9 agree.
- **Projection differences:** every one has the same sign on every seed (60/0; 40/0 at 32B).
- **Taken with PREREG_H:** 9 models, 4 families, 1.7B–32B. PREREG_H tested the two adjacent pairs in each of its 3 models, and all 6 were decided and agree. So 15 of 15 decided adjacent pairs agree, or 21 of 21 if PREREG_I's user − own pairs are added.

**What the pass does and does not show.**
- **Every model showed the same order.** So the preregistration's sharpest case, a family whose order differs and an axis that flips with it, never occurred. A fixed guess of "user > system > own" would have scored the same.
- **User versus system.** The direction puts user text further toward "given" than system text in all 9 models, as its construction implies whenever system-turn states lie closer to assistant-turn states, and user text is obeyed more than system text in all 9. Every model shares that order, and removing the direction leaves most of the user − system gap (§6d), so this match is correlational.
- **Order, not spacing (EXPL.).** The ratio of the two gaps does not carry over from projection to behaviour: (system − own)/(user − system) has a Spearman correlation of 0.10 across the 9 models.
- **SmolLM3 (reported on its own, as preregistered).** Its own-vs-given reversal in the original world does not appear here: system ≈ own, and user is highest.
- **Qwen3-32B has the largest role gaps of any model** (user − own +0.40). It also holds the goal unusually weakly (§6e), so it is not evidence for a general size trend.

## 6c. Is the axis authority itself? Social cues within a role (MIXED, PREREG_J)

**Design.** The identical reminder follows one header line inside a system or user turn:
- authority: CEO vs new intern;
- expertise: a Nature study vs a personal blog;
- consensus: all twelve board members vs one board member.

These are adapted from Control Illusion (Geng et al. 2026). We tested 7 models on fresh seeds, with 50 random directions as a null.

**Rule.** Wherever a high-vs-low pair changes obedience, the projection should move with it.

**Result.** 20 of 28 decided pairs agree (0.71). That is above the random-direction null (95th percentile 0.64) but below the preregistered 0.8. **MIXED.**
- **Expertise agrees everywhere: 12/12 decided pairs, 6 models, both roles.**
  - "Based on a peer-reviewed study in Nature" is obeyed *less* than "based on a post on a personal blog".
  - The Nature-framed text also sits higher on the role direction, toward the model's *own* voice.
  - This was the non-obvious prediction stated in the preregistration before data. It was not a gate.
- **Authority and consensus split between the three smallest models and the four larger ones.** With seven models, size and family cannot be separated: the three smallest are two Qwen3 models and SmolLM3, and the four larger include the only OLMo and Granite models.
  - In six of seven models the high-status header moves the text toward the "own" end. In Granite the CEO header moves it slightly the other way (+0.005 and +0.023 toward "given").
  - In the three smallest models (Qwen3-1.7B, SmolLM3-3B, Qwen3-4B) the high-status header is also obeyed less, so these pairs agree.
  - In some pairs of the larger models the high-status header is obeyed *more*, so these pairs disagree. There are 8: Qwen3-14B, authority and consensus in both turns (4 pairs); Qwen3-8B, consensus in the system turn; OLMo-2-7B, authority in the system turn and consensus in the user turn; and Granite, consensus in the user turn.
- **Reading.** The role direction tracks evidence framing in six of seven models (Granite's expertise pairs are undecided), but status cues only in the three smallest models. In the larger ones, status may act through another route; with these seven models, size and family are confounded. This is consistent with Zeng (2025), who found distinct subspaces for role and social conflicts.

## 6d. Is the axis necessary? Directional ablation (PARTIAL, PREREG_K)

**Design.** As in directional ablation (Arditi et al. 2024), the unit role direction is projected out of the embedding and every layer output while the reminder is read. A random direction (a single draw), ablated the same way, is the control. The test ran on Qwen3-4B, 8B, 14B and 32B and on OLMo-2-7B, on fresh seeds.

**Result.** Removing the direction significantly narrows the user − own spread in three Qwen models, more than the random control, while the goal is still pursued: competence (the reminder's effect on p_goal) stays at 64–95% of plain.

| Model | Spread removed | Holm p (vs plain / vs random ablation) |
|---|---|---|
| Qwen3-4B | 42% | 0.017 / 0.016 |
| Qwen3-8B | 44% | 0.021 / 0.016 |
| Qwen3-32B | 27% | 0.047 / 0.003 |
| Qwen3-14B | 35% (n.s.) | — |
| OLMo-2-7B | none | — |

- **Verdict: PARTIAL.** No model reaches the preregistered 50%.
- **What disappears is mainly the system − own gap.** In Qwen3-8B it falls from 0.020 to 0.003; in Qwen3-32B, from 0.151 to 0.044.
- **The user − system gap mostly survives.**
- **Relative to the reminder's overall effect (descriptive).** The ablation also weakens the reminder itself: competence falls by 22%, 24% and 36% in Qwen3-4B, 8B and 32B, which alone shrinks every gap, while the random ablation leaves competence nearly unchanged. Per unit of competence, the user − own spread falls by about a quarter in Qwen3-4B and 8B (25% and 26%) and rises in Qwen3-32B (from 0.97 to 1.11). The system − own gap still falls per unit of competence, by 39%, 83% and 55%.

**Reading.** The direction is part of the machinery, mostly for the own-vs-given distinction it was built from: that gap shrinks even per unit of the reminder's effect. It does not account for the whole authority order, and part of the raw 27–44% reflects a general weakening of the reminder. This ablation did not establish a causal contribution in OLMo.

## 6e. Does size matter? (NO_TREND, PREREG_L)

**Design.** 15 models in four families, on fresh seeds, plain reminder cells:
- Qwen3 at 1.7, 4, 8, 14 and 32B;
- Qwen2.5 at 3, 7, 14 and 32B (Yang et al. 2024);
- OLMo-2 at 7, 13 and 32B;
- Falcon3 at 3, 7 and 10B (Falcon-LLM Team 2024).

Qwen3 and Qwen2.5 share a lineage, which the preregistration notes as a limit on "four families". Two measures per model:
- **goal holding, P:** mean p_goal with a system-turn reminder;
- **source sensitivity, A:** p_goal with a user-turn reminder minus p_goal with an own-turn reminder (the user − own spread).

The test was an exact within-family permutation test of whether size order predicts P (H1) or A (H2), with Holm across the two.

**Results.**
- **Goal holding: no trend** (p 0.13 unadjusted; Holm p 0.25, as sealed). In three of four families the larger models hold the goal *better*.
- **Qwen3-32B's weak goal holding replicates on fresh seeds.** Its system-turn p_goal was 0.342 in PREREG_I (§6b); here P is 0.34, against 0.89 at 14B. It is a property of that model: Qwen2.5-32B (0.90) and OLMo-2-32B (0.96) are among the most persistent models tested.
- **Source sensitivity: no general trend** (p 0.13 unadjusted; Holm p 0.25).
  - Within the Qwen lineage it rises monotonically with size in both Qwen3 and Qwen2.5 (EXPL.).
  - OLMo goes the other way.

**The authority order holds in all 15 models (EXPL.):**
- user > system is significant in 15/15;
- system > own is significant in 13/15, and positive in the remaining 2;
- nothing is significant the other way.

Together with PREREG_H/I, the order has been tested in 17 models from six families (Qwen3, Qwen2.5, OLMo-2, Falcon3, SmolLM3 and Granite), 1.7B–32B. User text is obeyed significantly more than system text in all 17, and no model significantly reverses either step of the order. This is the study's broadest behavioural result.

## 6f. Semantic self-attribution is distinct from chat-role placement (H1 MIXED, H2 MIXED, H3 DOES_NOT_TRACK; PREREG_M)

**Design.** Six models, 60 fresh seeds per model, 20 conditions. Two OWN minimal pairs compare a goal framed as the model's own analysis or plan against a colleague's analysis or another manager's plan, within the same system or user role. Two KNOW pairs compare established knowledge or a Nature source against a forum or blog. The goal text and probed tokens are unchanged.

**Sealed verdicts:** H1 OWN **MIXED** (1 model in the predicted direction, 5 significantly opposite after Holm); H2 KNOW **MIXED** (4 predicted, 1 opposite, 1 undecided); H3 **DOES_NOT_TRACK** (4/11 agree, 3 disagree, 4 unresolved). The SELF_DISCOUNT headline gate was not met. The formal H1 verdict is MIXED, rather than REVERSED, because one model (Qwen3-1.7B) significantly goes in the predicted direction.

| Model | OWN: p_goal, other-framed minus self-framed | Holm p |
|---|---:|---:|
| Qwen3-1.7B | +0.004 | 0.0198 |
| Qwen3-4B | −0.023 | 0.0003 |
| Qwen3-8B | −0.090 | 0.0003 |
| Qwen3-14B | −0.077 | 0.0003 |
| SmolLM3-3B | −0.010 | 0.0003 |
| OLMo-2-7B | −0.052 | 0.0003 |

Negative values mean that the goal text framed as the model's own analysis or plan was followed more than the same text framed as a colleague's analysis or another manager's plan. These are probability differences in the simulated task, not changes in general agent reliability. In all six models, the plain role order remains user > system > assistant on these same seeds. Thus placing text in an assistant turn and describing text as the model's own plan are empirically different manipulations; they should not be combined into a general claim that self-like text has less authority.

**Exploratory detail.** Nature < blog has the same descriptive sign in 11 of 12 model-by-role comparisons, with a reversal in Qwen3-8B's user turn. This is a narrower follow-up using modified wording, not an exact replication of PREREG_J. The broad knowledge family is mixed.

**Follow-up pilot (EXPL., MPILOT; Qwen3-8B only, 40 paired seeds; predictions from two AI systems hashed before launch).** Against a neutral header ("The plan for this fund:"):
- "another manager's plan" lowers goal choice by 0.150 [0.114, 0.187], 40 of 40 seeds;
- "your own plan" raises it by 0.033 [0.022, 0.045];
- a named third party ("Dana's plan") changes nothing (−0.003, n.s.);
- all 10 paraphrase sets agree in sign.

In this model, PREREG_M's OWN contrast is therefore mainly a discount on a rival manager's plan, with a small "your own" bonus, rather than a premium on self-framing. Two predictions failed: "your own" beat "my own" by less than the predicted 0.02 in the user turn, and "my own" in the assistant turn fell below the system turn (−0.017).

**Verification.** All six sealed hashes matched (the preregistration and the archived code bundle), and all 120 result files contain the expected 60 unique seeds (2000–2059). Checksums were verified; the records are in the repository. A separate AI session (Codex) reran the sealed analysis and recomputed the descriptive differences from raw data. This is a computational recheck by another AI, not outside or human validation.

## 7. Accounts that failed (deixis FAIL; addressee INCONCLUSIVE)

- **Deixis (FAIL, preregistered as INJ3_PREREG; Qwen3-4B and 1.7B).** The account: the discount follows first-person commitments, so an injected instruction worded as the agent's own commitment ("I'll…") should be obeyed more when pushed toward the agent's own voice (+vR). The test used the injection task of §8: a document to be summarised carries an instruction to skip the summary and reply only with a code word, inside the document or as a separate system message, and compliance is read from the first reply token (120 cases). The instruction was steered toward "own" in four wordings: imperative, "You will…", "I'll…" and "The assistant will…". The first-person wording was suppressed instead: the most of the four in Qwen3-4B (compliance 0.88 → 0.05), and second only to "You will…" in Qwen3-1.7B's system placement (−0.69 vs −0.83). In Qwen3-1.7B's document placement it was never obeyed, even unsteered. The direction's effect did not depend on the pronoun.
- **Addressee (INCONCLUSIVE, preregistered as ADDR_PREREG; Qwen3-4B and 1.7B).** The account: text addressed to the model gets authority. The projection difference was −0.22 and −0.15 of the role gap, opposite in sign to the prediction but under the rule's 0.30 bar.
- **A lesson.** Three strong language models proposed these accounts independently and agreed. The experiments disagreed.

## 8. Injection: role steering reduces it in one model (REPL.)

**Result (PASS on Qwen3-4B, INJ2_PREREG).** We call this test INJ2_PREREG: its rule was written in the run log before data, and its script was hash-sealed. The direction is added to an injected instruction inside a document. Compliance falls from 0.209 to 0.000. The run used 4-bit weights; in bf16 the model ignores the injection at baseline. The single random control gave 0.642. An exploratory check in the same setup, RNDCTL (48 cases, 16 random directions at each sign, predictions hashed before the run), shows that this draw was unusual (91st percentile): random draws flip sign and, in the document placement, average near zero (mean +0.015, SD 0.219). Against that distribution, −vR raises compliance beyond all 32 draws in all three placements tested (document, assistant turn, system turn). +vR's defensive effect is at the floor in the document and assistant placements, and only modestly beyond random in the system placement. The legitimate instruction rises from 0.79 to 1.00, and replies stay on-task in 24/24 cases.

**Prior art.** This replicates the steering results of Zhang, Lee & Park (2026) and Liu (2026), which build on the role-confusion account of Ye et al. (2026). It is not a contribution.

## 9. An obvious fix fails: fine-tuning on own-voice goal practice (FAIL, PREREG_E and PREREG_F)

**Design.**
- LoRA adapters (Hu et al. 2022; rank 16) trained on synthetic multi-turn decision tasks in 8 non-financial domains, in the reply format "CHOICE:". Training sets have 16, 48 or 240 conversations.
- Third-party pressure throughout; a goal reminder every 3 rounds, as an assistant turn ("own") or a system turn ("given"); identical targets.
- Evaluation on the held-out fund task in its own format, plus a forged-assistant-turn injection test.

**Results.**

| Experiment | Result | Status |
|---|---|---|
| Pilots E1–E2 | E1, 240 training conversations: drift removed (0.857 → 0.03–0.06 without reminders), but every cell at the floor. E2, a dose series: at 16 conversations, own-trained gap 0.009 vs given 0.023 (one adapter per arm). Shortcut test (growth pressure agrees with the goal): adapters trained on 240 conversations pick *against* the pressure (+0.08 to +0.10). Every dose raises forged-assistant injection compliance (+0.012 to +0.085; one adapter per dose, each p < 0.001 across 120 injection cases). | EXPL. |
| PREREG_E (run E3: 6 vs 6 adapters, 16 conversations each, fresh seeds) | Gap own 0.0150 vs given 0.0229 (−0.008), exact permutation p 0.071. Shortcut present even at 16 conversations. Forged-assistant injection +0.016 (own) and +0.032 (given) above the untrained model on average; 10 of 12 adapters above it. | **FAIL** |
| Pilot E4 (balanced data: half the rounds have pressure that agrees with the goal) | One own adapter removed drift (0.858 → 0.050) without a shortcut; its given twin failed the shortcut check. | EXPL. |
| PREREG_F (6 vs 6, balanced data, 240 conversations each; hypothesis formed after the data and labelled so) | No-reminder drift own 0.206 vs given 0.229 (p 0.64). It does not beat the untrained model *with* system reminders (0.182). Shortcut +0.072. Forged-assistant injection +0.065 (own) and +0.041 (given) above the untrained model on average; 8 of 12 adapters above it. | **FAIL** |

**Reading.**
- Small fine-tunes of either kind cut no-reminder drift, but not below plain reminders. The cut is about three quarters in PREREG_F (balanced data, 240 conversations) and 20–38% with 16–48 conversations. The unbalanced pilots with 240 conversations reached the floor, partly by learning to oppose the pressure (the shortcut test).
- They partly learn to oppose pressure rather than to follow the goal. They also make forged assistant-turn injections more effective: every E2 and E4 pilot adapter did (each p < 0.01 across 120 injection cases), and on average the sealed tests did (+0.02 to +0.07), though 6 of 24 sealed adapters fell below the untrained model and that average rise was not tested for significance.
- The training-data seed moved no-reminder drift from 0.08 to 0.32 within the own arm, and from 0.11 to 0.35 within the given arm.
- The pilots that suggested a role-specific benefit all shared one data seed. Their "consistent" pattern was one dataset seen several times.

## 10. Believe or obey? (EXPL., unfinished)

**The question.** Does the same role code govern credence in facts as it governs obedience to goals?

**Pilots on Qwen3-1.7B.** A matched "believe" arm used a fact sheet and false counter-claims.
- The first pilot was confounded: the goal drifted.
- The repaired pilot failed calibration (the claims were too strong) and narrowly failed validity (r = 0.46 between stated belief and action).

**Exploratory signals.**
- Repeating the fact sheet strongly protects belief against false claims.
- Whether the fact sheet is in the agent's own voice or given barely changes belief (≤ 0.03). In the pilot's matched obey arm, the same own-versus-given change moved goal obedience by +0.08 (own − given p_hi, 20 seeds).
- This leans toward separate codes for obeying and believing. It is not a finding.

**Follow-up.** Paper B (Ramdan 2026) takes the question up with sealed tests on synthetic items across five sources. In most models tested, obeying and believing rank the sources differently (sealed verdict FRAGMENTED), so the two behaviours weigh a text's source differently.

## 11. Limitations

- **Task.** One task family with synthetic pressure, and a construct that partly measures resistance to pressure (§2).
- **Models.** The strong causal effects are Qwen-centred. Sizes are ≤ 32B. No frontier models were tested.
- **One-axis generality.** All 9 models share one authority order, so the axis has only been shown to match that order, not to follow a different one. The match is correlational, and it covers the order, not the spacing between roles.
- **Statistics.** Many exploratory contrasts. Every gate decision was preregistered or logged before data, but the descriptive readings around ambiguous or failed gates are ours.
- **Context windows.** OLMo-2 results needed context-window restrictions (labelled) or shorter episodes.
- **Process.** The study was originally run end-to-end by Claude under time pressure and subsequently computationally rechecked and extended in Codex. Its pilots and post-hoc patterns misled it twice (§9), and only the sealed tests caught this.
- **Random-direction controls are single draws.** Apart from the 50-direction projection nulls of PREREG_J and PREREG_M, every random control in this paper is one isotropic draw of matched norm. That covers the role-steering contrasts (§5, PREREG_C and PREREG_G), the random ablation in PREREG_K, and the deixis and injection tests (INJ3_PREREG, INJ2_PREREG).
  - The exploratory 32-draw check (RNDCTL, §8; Qwen3-4B, in INJ2_PREREG's setup) found random-draw effects that flip sign with the draw and centre near zero, with an SD of 0.13–0.22 in first-token compliance.
  - One draw is therefore a weak control in both directions. "Beyond random" may overstate specificity, and "random did as well" may reflect one strong draw.
  - The fix is at least 16 draws with ± pairs, reporting the learned direction as a percentile of that distribution.
- **Unfinished work.** The believe-or-obey scope test in the agent task (§10). Paper B (Ramdan 2026) addresses believing versus obeying with sealed tests on synthetic items.

## 12. What may be new, and what is not

**Candidate contributions, requiring explicit comparison with the related work below:**
1. A direction extracted from role contrasts on neutral sentences changes goal adherence in the simulated trading task. It is strong in Qwen3 1.7B–14B. Its sign holds in three more families, at family-specific depth. A causal conversational-role direction has a close precedent in Tsui (2026), for self-correction. What is specific here is goal adherence over long horizons.
2. (EXPL.) The natural own-vs-given discount grows with size in Qwen3 but not in OLMo-2, and it is reversed in SmolLM3. The sealed size test (PREREG_L, §6e) found no general size trend in goal holding or source sensitivity; source sensitivity rises with size only within the Qwen lineage.
3. In OLMo-2-7B the discount and its direction are present right after supervised chat fine-tuning, the first stage that could be tested.
   - Preference stages add no amplification at the preregistered threshold (p < 0.01), although the gap rises slightly (0.063 → 0.071 → 0.077).
   - In an exploratory pilot (one model, 20 seeds), the discount was not detected with plain-text role labels, suggesting that it depends on the template's role tokens.
4. **A neutral-text role direction's ordering of user, system and assistant goal placements matches how they are obeyed in this task** (user > system > own; a correlational match, §6b).
   - ONE AXIS under seal in Qwen3-8B, Qwen3-14B and OLMo-2-7B.
   - PASS under seal in 6 more models (PREREG_I): 9 models, 4 families, 1.7B–32B. Every decided comparison agrees: 15 of 15 adjacent pairs, or 21 of 21 with PREREG_I's user − own pairs (§6b).
   - All 9 share the same order (§6b).
5. Negative results:
   - a deixis account that failed its sealed test in two small Qwen3 models;
   - two preregistered fine-tuning fixes failed, with a documented shortcut and an injection cost.

**Not new:**
- role confusion as the cause of injection (Ye et al. 2026), and steering it (Zhang, Lee & Park 2026; Liu 2026);
- **a causal conversational-role direction,** for self-correction (Tsui 2026; §1): a close precedent for contribution 1;
- source-format cues are linearly decodable, while a pre-specified test for an abstract provenance code halted without interpretable evidence either way (Leong 2026, v2);
  - its v2 also reports that steering along its source-format direction did not move tool-name mention (0/1,895, mention-scored); the author notes this cannot rule out an effect on execution;
  - its OLMo-2 lineage material from v1 was not carried into v2;
- role relabelling changes self-correction (Chen et al. 2026: behavioural, 12 settings, no mechanism, no goals);
- goal drift itself (Arike et al. 2025; Menon et al. 2026) and reminders against long-horizon "behavioral state decay" (Wu et al. 2026);
- **annotating span authority through a non-text channel:**
  - Semantic Overlays (Penman 2026) trains adapters that mark spans as non-executable, and strongly reduces injection on five benchmarks (e.g. AlpacaFarm 99.0% → 0%, TensorTrust 34.8% → 6.2%);
  - any capability built on our role direction is a special, untrained case of that idea, applied in the opposite direction: raising the authority of the agent's own notes;
- steering for instruction-following (Stolfo et al. 2025: instruction-specific vectors) and against multimodal injection (Lu et al. 2026);
- agent skills stored as steering vectors (Zhao et al. 2026);
- **system prompts losing to user messages:**
  - Geng et al. (2026, *Control Illusion*) show behaviourally, in six models including GPT-4o and Claude 3.5, that system/user separation does not reliably enforce priority.
  - They also show that social framings (authority, expertise, consensus) influence behaviour more strongly than system/user roles do.
  - So our behavioural user > system order is consistent with known results. What may be new is the representational axis whose order matches it; their paper has no mechanistic analysis.
- **role conflicts dissected mechanistically:** Zeng (2025).
  - Linear probes show that system–user conflicts and social-cue conflicts occupy *distinct subspaces*.
  - Direct logit attribution shows stronger conflict detection for system–user conflicts, but consistent resolution only for social cues.
  - That models obey social cues while often ignoring the system-over-user hierarchy is an earlier behavioural finding (for example Geng et al. 2026, above), which Zeng extends.
  - Steering vectors built from social cues amplify instruction following regardless of role.
  - This is the closest mechanistic prior work to our one-axis claim, and it points against a single shared axis. PREREG_J tests the narrower question of whether social cues move the identical goal text along our role direction.
- **training the hierarchy:** Zheng et al. (2026) report about 20-point gains on system–user conflicts across families, from training. It is the reference point for any inference-time fix. Our own exploratory attempt at such a fix, steering system text along the role direction, failed (Appendix A).
- **role identification through shortcuts:** Wang et al. (2025) find that fine-tuned models identify roles partly from task type and from proximity to the start of the text. In our design the reminder is inserted at the same steps, and at the same point in each step, for every role (§6b). Ye et al. (2026, Appendix K) likewise find that token position, not tags, determines "systemness".
- **authority personas in sycophancy:** Joswin et al. (2026) find a graded authority effect localised to one layer. The effect is entangled with question content, and a mean "authority" vector failed to reproduce it. This contrasts with our content-free role direction, for goal text rather than beliefs.
- **a chat-template direction:** Maczan (2026) finds that the chat template switches a model's self-referential voice and that one activation direction reproduces the switch. This is related to our role direction, but has no link to authority or goals.

**Further related work.**
- **Inference-time hierarchy interventions.** Zeng et al. (2026) restore instruction priority without training, by editing cached value vectors at selected heads. We did not compare our steering against it; any defence built on the role direction would need that comparison.
- **Readable signals versus causal directions.** Balp-Straffon et al. (2026) show that directions that read out a conflict well can steer it poorly. This is why we test the role direction causally, by steering (§5) and ablation (§6d), rather than resting on how well it orders the roles (§6b).
- **Predicting hierarchy failures from probes.** Ye et al. (2026, Appendix K) already predict instruction-hierarchy failures from role probes. Any monitoring use of the role direction would need this comparison.

## Data, code and preregistrations

Code, seeds, result files, sealed preregistrations and archived cloud bundles are at https://github.com/Somebodyhere101/whose-words-count, and the same files are archived with each paper on Zenodo as `code-and-data.zip`. Cloud runs and billing records are logged in `PLAN_7DAY.md`. Checksums were verified; the records are in the repository. Paths below are relative to `research_next/agent_goal_persistence/` in the repository.

**Seal files.** Each `.sha256` file lists the files it hashed before data.
- This paper's preregistrations: `PREREG.sha256` (the main run) and `PREREG_B.sha256` to `PREREG_M.sha256` (B, C, D, E, F, G, H, I, J, K, L and M), each next to its `PREREG*.md`.
- Tests whose rules are in the run log and whose script is hash-sealed: `INJ2_PREREG.sha256` (`code/inj2.py`; injection, §8), `INJ3_PREREG.sha256` (`code/inj3.py`; deixis, §7) and `ADDR_PREREG.sha256` (`code/addr.py`; addressee, §7).
- Predictions hashed before two exploratory pilots: `MPILOT_PRED.sha256` (MPILOT, §6b and §6f) and `RNDCTL_PRED.sha256` (RNDCTL, §8).
- Paper B's seals, in the same repository: `PREREG_S.sha256` to `PREREG_Y.sha256` (S, T, U, V, W, X and Y), `PILOT_V0.sha256` and `PILOT_V1.sha256`.

**Where the results are.** `CONSOLIDATED_RESULTS.md` lists the result files. The main analysis outputs for this paper are:
- §5 and §6: `cloud_prereg_c/c_results.json` and `cloud_lineage/d_results.json`;
- §6b–§6f: `cloud_prereg_g/g.json` to `cloud_prereg_m/m.json`, plus `cloud_prereg_m/m_descriptive_check.json` (the descriptive recheck of PREREG_M);
- MPILOT: `MPILOT_RESULTS.md` and `cloud_mpilot/mpilot_analysis.json`; RNDCTL: `RNDCTL_RESULTS.md` and `rndctl_q4b/`;
- §7 and §8: `inj3_verdict.txt`, `addr_verdict.txt` and `inj2_q4b_verdict.txt`;
- §9: `cloud_binding_e2/`, `cloud_binding_e3/` (PREREG_E), `cloud_binding_e4/` and `cloud_prereg_f/`;
- Appendix A: `cloud_ci_pilot/` and `decomposition_pilot_codex/`.

**Cloud cost.** The two papers share one set of cloud runs. The RunPod billing record, read on 29 October 2026, shows $23.22 on 27 October, $52.10 on 28 October and $20.05 on 29 October (UTC days): $95.37 in total, including $0.03 for the 10 GB results volume. Of the 29 October total, Paper B's PREREG_Y pods account for $18.45 and this paper's MPILOT follow-up for $1.59. Local runs used the author's laptop GPU. Pod times for each run are in `PLAN_7DAY.md`.

## AI-use statement

Claude (Anthropic) designed, ran, analysed and wrote this study. Claude proposed its direction on 2026-10-25: how agents keep or lose a goal, and goal text given to the agent versus written in its own voice. The proposal drew on the author's earlier studies, some unpublished, of how small models keep or lose an instruction, and answered the author's request for the biggest next step toward a breakthrough; the author approved it. Three other AI sessions, which the author commissioned with the same brief, proposed experiment plans that are described in the log; their suggestions were tested, not trusted. The believe-versus-obey question of §10 came from one of these plans (2026-10-27). Claude designed and launched the fix-test pilot (Appendix A.1). Codex (OpenAI) recovered the completed results of that pilot and of PREREG_M and rechecked both computationally, planned and ran the neutral-role decomposition diagnostic (Appendix A.2), checked reference-method software, expanded the prior-art comparison, and revised an earlier draft of the combined report.

**Rechecks.** On 2026-10-28, separate Claude sessions rechecked 168 numeric claims in the abstract, §2–§10 and both pilots against the primary result files, re-running every sealed analysis script; each reproduced its stored output, and no gate verdict changed. §11, §12 and the data section were only spot-checked. The MPILOT and RNDCTL results were added later; a Claude editing session checked their numbers here against the analysis files. Every reference was verified against its primary page (`REFERENCES_VERIFIED.md` and its addenda). Before release, two further Claude sessions read both papers, one for consistency and one as a sceptical reader. Their findings were checked against the records and fixed where they held (`PREPUB_REVIEW.md`, `PREPUB_SKIM.md` and the change log `PREPUB_FIXES_A.md`). These are AI rechecks, not outside or human validation. The author did not independently check the code, analyses or technical claims. The author is responsible for the released content.

## References

- Allal, L. B., et al. 2025. SmolLM2: When Smol Goes Big -- Data-Centric Training of a Small Language Model. *arXiv preprint*. arXiv:2502.02737.
- Arditi, A., et al. 2024. Refusal in Language Models Is Mediated by a Single Direction. *Advances in Neural Information Processing Systems 37 (NeurIPS 2024)*, 136037–136083. arXiv:2406.11717.
- Arike, R., et al. 2025. Evaluating Goal Drift in Language Model Agents. *Proceedings of the AAAI/ACM Conference on AI, Ethics, and Society (AIES 2025)* 8(1): 192–203. doi:10.1609/aies.v8i1.36541. arXiv:2505.02709.
- Bakouch, E., et al. (Hugging Face). 2025. SmolLM3: smol, multilingual, long-context reasoner. *Blog post*, 8 July 2025. https://huggingface.co/blog/smollm3
- Balp-Straffon, E., et al. 2026. How Language Models Choose Sides: Internal Representations of Instruction Hierarchy. *ICML 2026 Mechanistic Interpretability Workshop*. arXiv:2608.28648.
- Chen, K.-Y., et al. 2026. The Self-Correction Illusion: Role Relabeling Gates Explicit Error Flagging in Large Language Models. *arXiv preprint*. arXiv:2606.05976.
- Falcon-LLM Team (TII). 2024. The Falcon 3 Family of Open Models. *Blog post*, 17 December 2024. https://huggingface.co/blog/falcon3
- Geng, Y., et al. 2026. Control Illusion: The Failure of Instruction Hierarchies in Large Language Models. *Proceedings of the AAAI Conference on Artificial Intelligence (AAAI-26)* 40(36): 30816–30824. doi:10.1609/aaai.v40i36.40339. arXiv:2502.15851.
- Holm, S. 1979. A Simple Sequentially Rejective Multiple Test Procedure. *Scandinavian Journal of Statistics* 6(2): 65–70.
- Hu, E. J., et al. 2022. LoRA: Low-Rank Adaptation of Large Language Models. *ICLR 2022*. arXiv:2106.09685.
- IBM Granite Team. 2024. Granite 3.0 Language Models. *Technical report*, October 2024. https://github.com/ibm-granite/granite-3.0-language-models/blob/main/paper.pdf
- IBM Granite Team. 2025. granite-3.3-8b-instruct. *Model card*, 16 April 2025. https://huggingface.co/ibm-granite/granite-3.3-8b-instruct
- Joswin, E., Medicherla, S., and Mammen, P. M. 2026. A Mechanistic View of Authority Hierarchy in LLM Sycophancy. *arXiv preprint*. arXiv:2607.00415.
- Leong, J. W. 2026. Instruction Self-Arbitration Is Not a Trust Boundary: Configuration-Dependent Tool Calls and External Enforcement in LLM Agents. *arXiv preprint* (v2, 17 October 2026). arXiv:2608.28502.
- Liu, E. 2026. Reducing Role Confusion via Activation Steering. *NeurIPS 2026 Workshop: The Third Workshop on Agents in the Wild: Safety, Security, and Beyond*. https://openreview.net/forum?id=aJceCDuUjM
- Lu, W., et al. 2026. ARGUS: Defending Against Multimodal Indirect Prompt Injection via Steering Instruction-Following Behavior. *CVPR 2026*. arXiv:2512.05745.
- Maczan, J. 2026. "As a Language Model...": Chat Template Switches LLM Self-Referential Voice and Activation Steering Reproduces It. *COLM 2026 Workshop on Efficient Reasoning; KONVENS 2026 Workshop on Evaluating LLMs for Specialized Domains (Eval4SD)*. arXiv:2609.25021.
- Martins, P. H., et al. 2024. EuroLLM: Multilingual Language Models for Europe. *arXiv preprint*. arXiv:2409.16235.
- Menon, A., et al. 2026. Inherited Goal Drift: Contextual Pressure Can Undermine Agentic Goals. *ICLR 2026 Lifelong Agents Workshop*. arXiv:2603.03258.
- Penman, J. 2026. Semantic Overlays: Mitigating Prompt Injection with Annotations Beyond Tokens and Steering Vectors. *arXiv preprint*. arXiv:2608.23873.
- Ramdan, S. 2026. Who said this? Most chat models weigh a text's source differently for each behaviour, and a steering lever against injected instructions. Preprint (Paper B), Zenodo. doi:10.5281/zenodo.23758887.
- Stolfo, A., et al. 2025. Improving Instruction-Following in Language Models through Activation Steering. *ICLR 2025*. arXiv:2410.12877.
- Tsui, K. 2026. Self-Correction Bench: Uncovering and Addressing the Self-Correction Blind Spot in Large Language Models. *COLM 2026*. arXiv:2507.02778.
- Wallace, E., et al. 2024. The Instruction Hierarchy: Training LLMs to Prioritize Privileged Instructions. *arXiv preprint*. arXiv:2404.13208.
- Walsh, P., et al. (Team OLMo). 2025. 2 OLMo 2 Furious. *COLM 2025*. arXiv:2501.00656.
- Wang, Z., et al. 2025. The Illusion of Role Separation: Hidden Shortcuts in LLM Role Learning (and How to Fix Them). *ICML 2025*, PMLR 267: 63200–63210. arXiv:2505.00626.
- Wu, Y., et al. 2026. Remember When It Matters: Proactive Memory Agent for Long-Horizon Agents. *arXiv preprint*. arXiv:2607.08716.
- Xu, S., et al. 2026. Behaving Better, Thinking Worse: Sycophancy Across Post-Training Stages. *NeurIPS 2026*. https://openreview.net/forum?id=IUAXqLsMTC
- Yang, A., et al. (Qwen Team). 2024. Qwen2.5 Technical Report. *arXiv preprint*. arXiv:2412.15115.
- Yang, A., et al. 2025. Qwen3 Technical Report. *arXiv preprint*. arXiv:2505.09388.
- Ye, C., Cui, J., and Hadfield-Menell, D. 2026. Prompt Injection as Role Confusion. *ICML 2026*, PMLR 306: 148172–148202. arXiv:2603.12277.
- Zeng, S. 2025. Who is In Charge? Dissecting Role Conflicts in Instruction Following. *NeurIPS 2025 Mechanistic Interpretability Workshop*. arXiv:2510.01228.
- Zeng, S., et al. 2026. Steering Instruction Hierarchies at Inference Time. *COLM 2026*. arXiv:2607.26228.
- Zhang, K., Lee, D., and Park, J. 2026. Steering Role Confusion. *LessWrong*, 20 August 2026. https://www.lesswrong.com/posts/uz9pFutDAT7trygM9/steering-role-confusion
- Zhao, C., et al. 2026. Neural Procedural Memory: Empowering LLM Agents with Implicit Activation Steering. *arXiv preprint*. arXiv:2606.29824.
- Zheng, Z., et al. 2026. Reasoning Up the Instruction Ladder for Controllable Language Models. *Findings of the Association for Computational Linguistics: ACL 2026*, 39332–39354. doi:10.18653/v1/2026.findings-acl.1960. arXiv:2511.04694.

## Appendix A. Two exploratory fix pilots (both NO-GO)

Both pilots asked whether the role direction could serve as an inference-time fix for a different failure: a system instruction losing to a conflicting user instruction (Geng et al. 2026; §12). They used conflicts from Control Illusion's released data. The system message sets one constraint on the reply, for example to answer in English; the user message asks for a task with a conflicting constraint, for example to answer in French. A reply is a *system success* when it meets the system message's constraint, checked on the whole reply with a re-implementation of the published checks. Decoding was greedy, and each gate was fixed before data. Checksums were verified; the records are in the repository.

### A.1 Fix-test pilot: NO-GO

**Design.** Qwen3-8B and OLMo-2-7B; 15 base tasks with 12 prompt variants each, so 180 conflict prompts per model and condition. Conditions:
- *plain* and *emphasis:* Control Illusion's basic and emphasised separation prompts;
- *steering* at α = 2, 4 or 8: −α·vR added to the system message's tokens while the prompt is read, which pushes the system text toward "given".

**Gate.** A steering setting had to raise system success by at least 3 percentage points over plain in at least one model, without degenerate output.

| Model | Plain system success | Best steering | Gain | Emphasis baseline |
|---|---:|---:|---:|---:|
| Qwen3-8B | 8/180 (4.44%) | α 2: 12/180 (6.67%) | +2.22 percentage points | 13/180 (7.22%) |
| OLMo-2-7B | 42/180 (23.33%) | α 2: 42/180 (23.33%) | 0 | 43/180 (23.89%) |

No setting met the gate, so the planned confirmatory test on held-out tasks was not run. Both models worsen at larger strengths: α 8 gives Qwen3-8B 4/180 (2.22%) and OLMo 6/180 (3.33%). This is a descriptive pilot finding, not a confirmatory test of harm.

**Limits.** Replies were scored whole, while Control Illusion first removes acknowledgements of the conflict, so numerical equivalence to the published results is not established. Variants of the same base task are dependent. Output-length and degeneracy guards alone do not establish that replies are useful. No claim of a working hierarchy or prompt-injection defence follows.

### A.2 Neutral-role decomposition diagnostic: NO-GO

**Design.** Qwen3-1.7B at layer 13; two base tasks with 12 variants each, so 24 conflict prompts per condition, plus eight simple utility checks (arithmetic, copying, capitals). Two directions came from 36 neutral sentences, with identical content tokens and positions across roles (checked):
- R = assistant − mean(system, user), a fresh extraction of the role direction, not the archived vR;
- U = user − system.

U and its part orthogonal to R were rescaled to R's norm.

**Condition codes.** Steering acts on the system message unless stated.
- plain, emph: the basic and emphasised separation prompts, as in A.1;
- oldR2: −2R;
- user2, user4: +2U and +4U, which move the system text toward the user representation;
- orth2: +2 times the part of U orthogonal to R;
- pair2: +2U on the system message and −2U on the user message;
- random2: a random direction with the same norm and token masks as pair2.

**Gate.** A condition had to beat both plain and emphasis by at least 10 percentage points in system success, without more degenerate replies or fewer utility successes.

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

No targeted condition improved on plain prompting, so none met the gate, and no confirmatory run followed. The utility checks passed everywhere; this is a small screening check, not evidence of general utility retention. The diagnostic does not rule out other layers, extraction procedures or value-cache interventions, and it gives no positive support for this fixed intervention. The independent unit is the base task: two tasks, not 192 independent conflict samples.
