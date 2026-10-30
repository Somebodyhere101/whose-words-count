# Agent goal persistence and the role-authority direction: consolidated results (as of 2026-10-29)

Every result below carries its status:
- **PASS:** a preregistered gate was met;
- **FAIL:** the gate was not met;
- **UNINF.:** uninformative (ceiling or floor);
- **EXPL.:** exploratory, no gate.

Details and dates are in `PLAN_7DAY.md`. The preregistrations are `PREREG*.md` and `*_PREREG.sha256`. The AI-use statements are at the end of each paper. In short: Claude (Anthropic) designed, ran, analysed and wrote the study; Claude proposed the goal-persistence direction on 2026-10-25 in reply to the author's request for the biggest next step, and the author approved it; the question of where a text comes from was the author's (2026-10-28); the author did not independently check the technical content.

## 1. Behaviour: given vs own goal text in an agent (simulated trading, pressure emails)

| Test | Model | Result | Status |
|---|---|---|---|
| Main 2×2 (PREREG.md) | Qwen3-1.7B | Own notes drift more than a fixed reminder (H1, p 0.0001). Same text in own turn followed less (H2, +0.18, p 0.025) | PASS (H1, H2) |
| Run B, confound removed (PREREG_B.md) | Qwen3-1.7B | H1 PASS; H2 +0.11, p 0.037, 26/9 seeds; notes-framing S1 not detected | PASS |
| Fast instrument check | Qwen3-1.7B | All three directions hold | PASS |
| Weak goal text | Qwen3-1.7B | own − given +0.107, 40/40 seeds | EXPL. |
| Scale (fixed text, own − given) | Qwen3 1.7B / 4B / 8B / 14B / 32B | +0.005 / +0.021 / +0.028 / **+0.110 (40/40)** / **+0.144 (37/40)** | EXPL. (trend) |
| Second family | SmolLM3-3B | Natural effect slightly *reversed* (−0.014) | EXPL. |
| Third family | OLMo-2-7B (steps inside its 4,096-token window; post-hoc restriction) | **own − given +0.079 (35/5, p 0.0001)**; own notes − given notes +0.059 (34/6) | EXPL. |
| Fourth family | Granite-3.3-8B | own − given +0.006 (p 0.046; n.s. once low-mass steps are excluded); weak text +0.013 (32/8) | EXPL. |
| Other families | SmolLM2-1.7B, EuroLLM-1.7B | Cannot do the task (no response to the goal) | UNINF. |

### 1b. Origin: which training stage installs the gap (OLMo-2 lineage, `PREREG_D.md`, native template, 80 fresh seeds)

| Size | SFT | DPO | Instruct (RLVR) | Rule verdict |
|---|---|---|---|---|
| 7B, own − given | +0.063 (69/11) | +0.071 (76/4) | +0.077 (75/5) | H-SFT: arrives at SFT; no amplification at p < 0.01 |
| 13B, own − given | +0.0075 | +0.0066 | +0.0081 | H-pref by threshold only: the gap is tiny and flat |

- **Combined verdict: AMBIGUOUS** (status FAIL to reach a combined claim).
- **No evidence for a preference-stage origin.** At 7B, 82% of the gap and the role direction (cos 0.994 to the final model) are present right after SFT.
- **Pilots:**
  - OLMo-2 base models (1B, 7B) do not respond to a goal reminder in a plain transcript, so the pretraining origin is untestable here.
  - With plain-text role labels, OLMo-2-7B-Instruct's gap vanishes (+0.013 vs +0.080 native). The discount rides on the template's role tokens.
- **Exploratory: authority order in OLMo-2 is user > system > own** at both sizes and every stage.

### 1c. Clean construct and the authority order (3-way world: goal pick, pressure pick and contrarian trap separated)

| Test | Result | Status |
|---|---|---|
| PREREG_G: steered own note > system *and* user placement (Qwen3-8B, 14B) | Beats system (+0.033, +0.022) and random, but not user (−0.022, −0.011) | **FAIL** |
| Own-voice discount on the clean construct (PREREG_G, reported) | system − own +0.030 / +0.058 / +0.089 (Qwen3-8B / 14B / OLMo-2-7B), p 0.0001 | EXPL. → replicated in PREREG_H A2 |
| **PREREG_H: authority order user > system > own** | A1 +0.045 / +0.022 / +0.108; A2 +0.024 / +0.061 / +0.061 (Holm p ≤ 0.00025) | **PASS (replicated in 3/3)** |
| **PREREG_H: is authority one axis?** Projection of the goal reminder on the role direction | user < system < own in all 3 models (60/0 or 58/2 seeds) | **ONE AXIS (3/3)** |
| **PREREG_I: does the axis generalise?** 6 more models: Qwen3-1.7B, SmolLM3-3B, Qwen3-4B, Granite-3.3-8B, OLMo-2-13B, Qwen3-32B | Behaviour and projection both user > system > own in all 6. 15 decided pairs, 15 agree, 0 disagree. Undecided: system − own in SmolLM3, Granite and OLMo-13B | **PASS** (2026-10-28) |

- **One learned, content-free role direction orders the authority of all three chat roles for goal text.**
  - It holds in 9 models from 4 families (Qwen3, SmolLM3, Granite, OLMo-2), from 1.7B to 32B, with 21 of 21 decided comparisons agreeing.
  - Moving along the direction shifts adherence causally.
- **vR was built only from own-vs-given contrasts,** so the user-vs-system ordering it shows is not built in. User text sits further toward "given" in 9/9 models, and user − system is decided in 9/9.
- **Limits:**
  - All 9 models share the same order, so the axis was never tested against a model with a different order.
  - The axis predicts the order but not the spacing between roles: a Spearman correlation of 0.10 for the gap ratios (EXPL.).
- **Qwen3-32B has the largest role gaps:** user 0.587 / system 0.342 / own 0.184 on p_goal.
- **PREREG_J (2026-10-28): MIXED.** Social headers within a role: 20/28 decided pairs agree (0.71; random null q95 0.64).
  - Expertise: 12/12. "Nature" is obeyed less than "blog" and sits toward "own".
  - Authority and consensus: they move text toward "own" in every model, but are obeyed less only in small models and more in Qwen3-14B and OLMo.
  - File: `cloud_prereg_j/j.json`.
- **PREREG_K (2026-10-28): PARTIAL.** Directional ablation of vR while the reminder is read erases 42%, 44% and 27% of the user − own spread in Qwen3-4B, 8B and 32B (Holm p < 0.05 vs plain and vs random ablation).
  - Mainly the system − own gap disappears.
  - Qwen3-14B: 35%, n.s. OLMo-2-7B: none.
  - Competence retained at 64–95%. File: `cloud_prereg_k/k.json`.
- **PREREG_L (2026-10-28): NO_TREND** for goal holding vs size (p 0.13; larger models hold goals better in 3/4 families) and for source sensitivity vs size (p 0.13; it rises monotonically within Qwen3 and Qwen2.5, while OLMo goes the other way).
  - The Qwen3-32B collapse replicates (P 0.34 vs 0.89 at 14B) but is model-specific: Qwen2.5-32B 0.90, OLMo-2-32B 0.96.
  - **EXPL.:** user > system > own holds in all 15 models of 4 families. user > system is 15/15 significant; system > own is 13/15 significant and 2/15 positive. File: `cloud_prereg_l/l.json`.
- **Combined reading:** vR is one carrier of authority, mostly for own-vs-given, not the whole order. Social status acts elsewhere in larger models, consistent with Zeng 2025.
- **Files:** `cloud_prereg_i/i.json`; the full table is in `PLAN_7DAY.md` (2026-10-28 07:20).

## 2. Representation: is there an abstract "this is mine" tag?

- **Stage-2 gate (role-based vs "Earlier you wrote" transfer >= 0.8, control >= 0.15 lower): FAIL** in Qwen3-1.7B (0.80/0.796, gap 0.12).
- The tested probes did not isolate a transferable abstract tag in SmolLM2, EuroLLM, Qwen3-4B, 8B, 14B, 32B, SmolLM3, OLMo-2-7B or Granite-3.3-8B (the control transfers as well or better).
- **Supported limit:** the tested role and attribution contrasts did not yield the predicted transferable tag. This does not establish the absence of such information elsewhere.

## 3. Mechanism: steering the role direction (vR, from neutral sentences) on the goal text only

| Model | Layer (depth) | Own text pushed toward given | Given text pushed toward own | Beyond random | Status |
|---|---|---|---|---|---|
| Qwen3-1.7B (weak text) | 13 (0.46) | 0.772 to 0.634 | 0.658 to 0.815 | +0.07 to +0.09 | **PASS** |
| Qwen3-4B | 17 (0.47) | 0.386 to 0.276 | 0.347 to 0.482 | +0.12 to +0.17 | EXPL. (gate met) |
| Qwen3-8B | 17 (0.47) | 0.306 to 0.154 | 0.258 to 0.580 | +0.21 to +0.30 | EXPL. (gate met) |
| Qwen3-14B | 18 (0.45) | 0.302 to 0.133 | 0.179 to 0.434 | +0.27 to +0.32 | EXPL. (gate met) |
| Qwen3-32B | 29 (0.45) | 0.881 to 0.838 | 0.747 to 0.770 (n.s. vs random) | +0.04 | FAIL at this layer; sweep 0.31–0.58 depth: same sign everywhere, 0.03–0.10 per layer |
| SmolLM3-3B | 7 / 17 | small, in the Qwen direction at layer 7 | | +0.01 to +0.05 | FAIL (near floor) |
| Granite-3.3-8B (weak text) | 8 (0.2) | 0.135 to 0.110 | 0.113 to 0.159 | +0.015 to +0.040 | FAIL (below 0.05; layer 18 null) |
| OLMo-2-7B (fixed text) | 6 (0.19) | 0.310 to 0.278 | 0.192 to 0.242 | +0.03 to +0.04 | FAIL (exploratory: includes out-of-window steps; layer 15 null) |
| **PREREG_C confirmation** (depth chosen by a sweep, fresh seeds 500–539, n = 40) | | | | | |
| SmolLM3-3B (weak text) | 7 (0.19) | 0.511 to 0.458 | 0.537 to 0.663 | +0.065 / +0.126 | **PASS** |
| OLMo-2-7B (fixed text, episodes inside its window) | 10 (0.31) | 0.254 to 0.206 | 0.185 to 0.261 | +0.053 / +0.074 | PRESENT BUT WEAK (−0.047, bar 0.05) |
| Granite-3.3-8B (weak text) | 10 (0.25) | 0.148 to 0.130 | 0.117 to 0.152 | +0.038 / +0.038 | PRESENT BUT WEAK (near floor) |

- **Outside Qwen, by the preregistered table:** 1 PASS of 3, so the dial's *strength* is **family-dependent**. The generality-of-strength claim is not supported.
- **The causal sign holds in all four families.** It beats random in both directions on fresh seeds (Holm p 0.00015 each).
- **The depth is family-specific:** Qwen about 0.46, OLMo 0.31, Granite 0.25, SmolLM3 0.19.
- **SmolLM3 passes even though its natural gap is reversed.** So the natural gap is not just the projection on vR.

- **Every model:** early layers (about 0.2 depth) give null; alpha 1 gives about half the effect; the output format is intact.
- **14B:** own text pushed toward "given" holds *better* than real system text (0.133 vs 0.179).

## 4. Transfer to prompt injection (same direction)

- Exploratory: Qwen3-4B, injection in a separate message; +vR makes the model ignore it (0.991 to 0.049), and it writes on-task summaries in 12/12 (topic word present, codeword absent).
- **Preregistered confirmation (inj2): PASS** on Qwen3-4B for the realistic in-document injection (0.209 to 0.000; random 0.642). The legitimate instruction rises 0.79 to 1.00; 24/24 on-task replies (gate checked: topic word present, codeword absent; summary quality not graded).
  - The tool-output placement was ineligible: the model already ignores it.
- **PRIOR ART:** Ye, Cui & Hadfield-Menell (ICML 2026, arXiv 2603.12277) and "Steering Role Confusion" (LessWrong, 2026-08-20). **This is a replication, not a discovery.**

## 4b. Capability: commitment-binding fine-tune (OLMo-2-7B-Instruct, LoRA on 8 synthetic non-finance domains)

| Pilot | Finding | Status |
|---|---|---|
| E1 (n 240) | Drift on the held-out fund task falls from 0.857 to 0.03–0.06 even without reminders, so every cell is at the floor. Forged-assistant injection +0.055 in both arms. | EXPL. |
| E2 dose series | At n 16 (the measurable dose), gap own-trained 0.009 vs given-trained 0.023, a difference of −0.014 (35/5). One adapter per arm. | EXPL. |
| E2 shortcut test | n 240 adapters pick *against* the pressure when it agrees with the goal: own +0.10 (SHORTCUT), given +0.076 (UNCLEAR). **The E1 capability reading is withdrawn.** | EXPL. |
| E2 injection | The cost grows with dose: +0.012 (given16) up to +0.085 (given48). | EXPL. |
| PREREG_E | 6 vs 6 independently trained adapters at n 16, fresh seeds. Mean gap own 0.0150 vs given 0.0229 (−0.008); exact permutation p 0.071. Shortcut is present at n 16 too (+0.10 to +0.12). | **FAIL** |

| E4 (balanced data) | own240b removes no-reminder drift (0.858 → 0.050) and passes the shortcut test (−0.002). given240b fails it (+0.063), so the rule is not met. Injection costs +0.14 (own) and +0.18 (given). | EXPL. |
| Post-hoc pattern | Own-voice training beats given-voice training on no-reminder drift in 6/6 pilot pairs, and on E3 (p 0.089). | EXPL. |
| PREREG_F | Own-voice goal practice → persistence without reminders (6 vs 6, balanced n 240, fresh seeds). No-reminder drift own 0.206 vs given 0.229 (p 0.64). It does not beat the untrained model with reminders (0.182). Shortcut gate +0.072. | **FAIL** |

- **Fine-tuning summary:**
  - small fine-tunes cut no-reminder drift (0.84 → about 0.2), but not below plain system reminders;
  - they add a partial contrarian shortcut and an injection cost of +4 to +8 points;
  - no role-specific capability is confirmed.
- **Why the single-adapter pilots misled:** the training-data seed moves no-reminder drift between 0.08 and 0.35 within one arm, and the pilots shared one data seed.

- **Construct caveat (E2):** in the swapped-growth world the base model's system reminder *raises* high-emission picks (0.088 → 0.277). The fund task's "goal adherence" partly measures resistance to the pressure emails.

## 5. Pragmatic accounts (from Opus 5.5, Fable 5.1 and a fresh Claude, all independently)

- **Deixis/commissive account:** the sign flips with the pronoun. **REFUTED** (preregistered) in 4B and 1.7B: "I'll…" payloads fall the most under +vR.
- **Addressee account (no-steering projection test):** INCONCLUSIVE, leaning against (−0.22 and −0.15 of the gap).
- The earlier self-instruction study also shows no turn × wording crossover.
- **Lesson:** three-model agreement was wrong; the experiment decided.

## 6. Prior-art map (what is not ours)

- **Role confusion causing injection, and steering it:** Ye et al. 2026; Steering Role Confusion 2026.
- **Self-correction blind spot:** Tsui 2025 (arXiv 2507.02778).
- **Role relabeling of byte-identical claims:** raises self-correction by 23–93 points (Chen et al. 2026, arXiv 2606.05976). Behavioural only, 12 settings.
- **Goal drift in agents and inherited drift:** Arike et al. 2025; Menon et al. 2026.
- **Instruction hierarchy:** Wallace et al. 2024.
- **No abstract provenance representation:** Leong 2026 (arXiv 2608.28502 v2, "Instruction Self-Arbitration Is Not a Trust Boundary…"). Source-format cues are linearly decodable (97.5–100%, four open models), but a preregistered crossed-probe test gave "no interpretable evidence of an abstract provenance representation". **This parallels our stage-2 negative result, which is therefore not new on its own.**
  - **Read in full 2026-10-27.**
    - Probes on Qwen2.5-32B, Llama-3.3-70B, DeepSeek-R1-32B and Gemma-3-27B.
    - The crossed test (Qwen2.5-32B, Llama-3.3-70B) transferred at or below chance, so "no stable, same-orientation source direction".
    - An additive steering bridge on 7 models changed tool mention in 0 of 1,895 trials. This contrasts with our role direction, which moves goal adherence strongly in Qwen.
    - The OLMo-2 post-training lineage appears only in Appendix N, as v1 material "not carried into this version as evidence". So v2 makes no stage claim.
- **Chen et al. 2026, abstract read 2026-10-27.**
  - Behavioural only: 12 model-domain settings, including closed APIs and open models up to 70B. Moving a byte-identical wrong claim out of the thought role raises explicit correction by 23–93 points (10/12 significant).
  - No probes, no steering, no training stages, no goals.
- **Post-training stages (OLMo-3):**
  - sycophantic follow-through splits sharply between SFT and DPO (Xu & Daneshjou, NeurIPS 2026);
  - DPO more than doubles sycophantic agreement (arXiv 2608.31079);
  - cue-following peaks at SFT (MATS/ICLR 2026).
  - These are adjacent to the planned lineage study.
- **Ye, Cui & Hadfield-Menell, role probes (full text read 2026-10-27, first 100k characters).**
  - **Their probes:** 5-way linear probes (system, user, CoT, assistant, tool) per layer, trained on web text wrapped in each role tag. Models: gpt-oss-20b/120b, Nemotron-3, Qwen3-30B-A3B.
  - **Their findings:** "Role perception is determined by style, not tags". Userness predicts exfiltration success, and CoTness predicts CoT-forgery success.
  - **What they do not do:**
    - measure an axis that orders roles by authority ("system beats user beats tool" appears only conceptually);
    - relate probe scores to how strongly benign instructions or goals are followed;
    - steer along a probe direction; they edit text only.
  - **So our PREREG_H result is distinct from theirs:** one content-free direction orders user, system and own goal text exactly as they are obeyed, and steering along it moves adherence.
- **Non-text span annotation (read at abstract level 2026-10-27).** Semantic Overlays (Penman, arXiv 2608.23873, Aug 2026) trains adapters that mark spans in the residual stream ("non-executable"):
  - SEP separation 24.3% → 99.0%;
  - TensorTrust attack success 34.8% → 6.2%;
  - AlpacaFarm 99% → 0%;
  - utility unchanged.
  - **This is the closest prior art for any "steer a span's authority" capability.** Our role-direction boost of the agent's own notes is the mirror use (raising authority) and uses an untrained direction.
- **ARGUS** (Lu et al., arXiv 2512.05745, Dec 2025) steers instruction-following in representation space against multimodal indirect injection. Adjacent.
- **Instruction steering** (Stolfo et al., ICLR 2025, arXiv 2410.12877): instruction-specific with-minus-without vectors improve format, length and keyword adherence.
- **Agent memory as steering vectors:** Neural Procedural Memory (arXiv 2606.29824) performs comparably to textual instructions.
- **Long-horizon "behavioral state decay"** fixed by injected reminders: arXiv 2607.08716 (Meta, 2026).
- **Self-recognition created by post-training:** "From Simulation to Enaction" (2026 preprint, emergentmind 2605.25459). Post-trained, not pretrained, models recognise their own on-policy generations. Relevant to how "own" text is represented. Unread.

## 7. What may be new (pending outside check)

1. One neutral-sentence role direction at about 0.46 depth **causally sets long-horizon agent goal adherence** in four Qwen sizes (1.7B–14B), with the effect growing with size. At 32B it is weaker and spread across depth. In three other families the same causal sign is confirmed on fresh seeds, at a family-specific depth (0.19–0.31). Its strength is family-dependent: it passes the preregistered bar in SmolLM3 and is present but weak in OLMo and Granite (`PREREG_C.md`).
2. The natural own-vs-given goal gap **grows with model size** in Qwen (1.7B to 32B). It **replicates in OLMo-2-7B** (+0.079) and weakly in Granite-3.3-8B, and is reversed in SmolLM3-3B.
3. **Negative results:**
   - there is no abstract "mine" tag in 9 models (a parallel finding exists: Leong 2026, arXiv 2608.28502);
   - the dial is pronoun-blind (deixis refuted);
   - commissives are suppressed most.
4. **One role direction orders all three chat roles' authority for goal text** (user > system > own). It holds under seal in 9 models from 4 families, 1.7B–32B (PREREG_H and PREREG_I). Its limits are in §1c.

## 8. Open items

- 32B layer sweep: done 2026-10-27 12:35 (see sweep32_results.txt): weaker, distributed effect.
- Capable second families at 7–8B: done 2026-10-27 13:50 (OLMo-2-7B, Granite-3.3-8B; PLAN_7DAY.md).
- Depth sweep and preregistered confirmation of the dial in OLMo, Granite and SmolLM3 (`PREREG_C.md`): done 2026-10-27 14:40. 1 PASS, 2 present but weak, so the strength is family-dependent and the sign holds.
- Read Chen et al. 2026 and Tsui 2025 in full before any step-3 claim.
- Outside review.
- Write-up.

## PREREG_M computational recheck in Codex


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


## Fix-test pilot: NO-GO (2026-10-28 13:17 +04:00)

Recovered by restarting existing pod ilrvy2lnddoirw, then stopped after a verified local backup. Transfer MD5: 3499116f7d203e1abbff84c093cb9bd8. All 20 raw/scored files were complete: 180 prompts per model and condition, matched by task/order/conflict; 15 base tasks, 12 prompt variants per task. The full archive and a second short-path copy are saved.

| Model | Plain system success | Best steering | Gain | Emphasis baseline |
|---|---:|---:|---:|---:|
| Qwen3-8B | 8/180 (4.44%) | alpha 2: 12/180 (6.67%) | +2.22 percentage points | 13/180 (7.22%) |
| OLMo-2-7B | 42/180 (23.33%) | alpha 2: 42/180 (23.33%) | 0 | 43/180 (23.89%) |

No setting met the pre-set +3 percentage point gate. The planned confirmatory PREREG_N run is therefore **not launched**. Both models worsen at larger strengths: alpha 8 gives Qwen3-8B 4/180 (2.22%) and OLMo 6/180 (3.33%). This is a descriptive pilot finding, not a confirmatory test of harm.

Limits: this evaluates whole responses, while Control Illusion reports an acknowledgement-removal procedure; direct numerical equivalence to the published paper is not established. Repeated variants of the same base task should be treated as dependent in subsequent inference. Output length/degeneracy guards alone do not establish task usefulness. No claim of a working hierarchy or prompt-injection defence follows.

## Additional competitive baselines verified in Codex

See PRIOR_ART_UPDATE_CODEX.txt. V-Steer and conflict-specific probe steering already provide direct hierarchy interventions; Ye et al. already predict per-case hierarchy failures. Their methods must be compared before proposing a new defence or monitor. The neutral-role decomposition pilot is exploratory and uses no additional cloud spending. Its screening result will be recorded separately.

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

## PREREG_S: one source monitor, or fragments? FRAGMENTED (2026-10-28 16:20 +04:00)

**Run.** Sealed (`PREREG_S.sha256`, 9/9 OK after the run; bundle `agp21.tgz`, md5 d8d89a83…), run 25 on pod `orrprhdweesjpl`, 12:00–12:17 UTC. Archive md5 d112a8d139d896954ea7ea10e4261f25. Outputs: `cloud_prereg_s/` (`s_analysis.json`, `s_jspace.json`).

**Design.** Identical statements in five sources (system, user, own earlier turn, quoted web page, tool output). Readouts: obey, believe and attribute ("which message said this?"). Plus a 5-way source readout from the statement's own tokens, and a user→own tag-transplant edit at the decision layer (sealed; the reverse, own→user, is exploratory) with same-norm random controls.

**Sealed verdict: FRAGMENTED** (3 of 4 models; OLMo PARTIAL).

| Model | Source readout at decision layer | Obey vs believe order, Kendall τ | Mean attribution (chance 0.20) | Behaviour | Edit usr→own ×1 | Headline |
|---|---|---|---|---|---|---|
| Qwen3-1.7B (L13) | 0.685 (not readable; 0.905 at L18) | 0.4 | 0.738 | MIXED | NONE (believe moved the opposite way, −0.028) | FRAGMENTED |
| SmolLM3-3B (L7) | 0.87 | 0.2 | 0.322 | FRAGMENTED | NONE | FRAGMENTED |
| Qwen3-8B (L17) | 0.88 | 0.2 | 0.871 | FRAGMENTED | NONE | FRAGMENTED |
| OLMo-2-7B (L10) | 0.94 | 0.4 | 0.325 | MIXED | PARTIAL (obey +0.004; believe −0.024 and attribution −0.004 opposite) | PARTIAL |

**Behaviour, source by source** (score = P(own answer) ÷ P(own + competitor's); 0.5 = parity with a competing user message):
- **Qwen3-8B:** obeys the user most (0.53) and its own earlier turn least (0.25). Believes the system most (0.75). Tool output is believed (0.67) but obeyed less (0.42), already a selective pattern.
- **Qwen3-1.7B:** obeys tool output most (0.71, above the user's 0.51), which is an injection weakness. Believes its own earlier turn most (0.73).
- **OLMo-2-7B:** believes its own turn (0.72) and the system (0.69). It discounts quoted web text for both behaviours (obey 0.39, believe 0.26), yet attributes near chance (0.33).
- **SmolLM3-3B:** small source effects (ranges 0.07–0.09); attribution 0.32.

**Behaviour does not need reportable source knowledge.** OLMo and SmolLM3 show reliable source effects (p < 0.001) while barely able to say where a sentence came from.

**J-space (Qwen3-1.7B, sealed rule b): OUTSIDE** at layer 13.
- Source fraction 0.0503 against floor 0.0312 (2× floor = 0.0625); content fraction 0.1182.
- Set 1, seen before sealing, gave the same numbers (0.0496), so the fresh set reproduces it.

**Exploratory (not in the sealed rules):**
- **The source enters the workspace late.** At layer 22 the source fraction is 0.127 against content 0.037.
- **The J-lens reading of each source direction at layer 13 is genre-like.** It is not authority-like:
  - user → question marks ("?", "哪些");
  - quoted page → closing quotation marks;
  - tool → code punctuation ("};", "\");");
  - own → end-of-text and ellipses;
  - system → line breaks and colons.

  So the readable tag on the text looks like a "what kind of text is this, what comes next" signal. That fits its failure to move obeying.
- **The reverse transplant (own→user) moves behaviour a little, in the Qwen models.**
  - Obedience moves as predicted in Qwen3-1.7B, Qwen3-8B and OLMo (Qwen3-8B: +0.027 at ×1, +0.062 at ×2, which is 22% of its −0.287 own–user gap).
  - Qwen3-1.7B attribution moves away from "own" (−0.040 at ×1, −0.070 at ×2).
  - The sealed direction (user→own) moved nothing. So the tag on the text is partly necessary but not sufficient, and the source signal the model uses must largely live elsewhere: role markers, or the answer position.

**Reading (as fixed before data):** source information exists but is used piecemeal. Defences that fix one behaviour (for example obedience) should leave others (belief, attribution) exposed.

**Prior art:** Leong 2026 (no abstract provenance code) and Zeng 2025 (distinct subspaces) predicted this direction. The joint obey/believe/attribute test with a causal transplant appeared open in the prior-art check.

**Caution added after the localization prior-art check (16:35).** The PREREG_S transplant null is at natural size (×1, ×2 of the centroid difference).
- "Steering Role Confusion" (LessWrong, Aug 2026) moves gpt-oss-20b attack success from about 0 to about 80% with an *amplified* user-minus-tool mean vector on command tokens.
- Liu (NeurIPS 2026) uses that direction as a defence.
- So the claim is only that the natural-size mean tag does not carry behaviour here. It is not that content-token directions can never steer it. PREREG_T tests natural-size, item-specific content patching directly.

## PREREG_T: where is "who said this" read? H1 MIXED, H2 DISSOCIATED (2026-10-28 17:25 +04:00)

**Run.**
- Sealed: `PREREG_T.sha256`, 9/9 OK after the run. Bundle `agp22.tgz`, md5 480ece39….
- Run 26 on pod `iax96f2y34tl94`, 12:36–13:15 UTC. Archive md5 8f86d85bdba952b1a1aca879d7e4c99b.
- Outputs: `cloud_prereg_t/t_analysis.json`. Figures: `figures/prereg_t_own_to_usr.png`, `figures/prereg_t_sys_to_usr.png`.

**Design.** The same statement goes in the user turn (recipient) or in the own/system turn (donor). The donor's residual stream is patched into the recipient at one layer, on one position set: role-marker tokens (M), the statement's own tokens (C), or everything after the turn (D). Every layer; obey, believe and attribute separately. 4 models, fresh items (seed 2200).
- The sanity patch of all positions reproduces the donor (1.00 everywhere; OLMo own→usr 1.08–1.10 because of its one-token misalignment, within the rule).

**H2, sealed: DISSOCIATED in 4/4 models.** Behaviours read the source at different depths. Handoff is the layer at which patching the later positions carries ≥ 50% of the effect:

| Model | Pair | Obey | Believe | Attribute |
|---|---|---|---|---|
| Qwen3-1.7B | own→usr | L19 | L14 | L13 |
| Qwen3-1.7B | sys→usr | L18 | L14 | L14 |
| Qwen3-8B | own→usr | L25 | – | L16 |
| Qwen3-8B | sys→usr | – | L19 | L17 |
| SmolLM3-3B | own→usr | L20 | – | – |
| SmolLM3-3B | sys→usr | L21 | – | L12 |
| OLMo-2-7B | own→usr | – | L15 | – |
| OLMo-2-7B | sys→usr | – | L16 | L10 |

(– = gap not informative.) Obeying is read 4–9 layers after attributing or believing, with bootstrap CIs excluding 0.

**H1, sealed: MIXED.** The role-marker tokens are the carrier before the handoff in 14 of 16 informative curves, including 8 of the 10 obey and believe curves that H1 uses (corrected 2026-10-29 from "11 of 13", which left out SmolLM3's three curves). The other 2 (Qwen3-8B own→usr obey; OLMo own→usr believe) are SHARED with the content tokens. No curve is content-only. Qwen3-1.7B and SmolLM3 are MARKER; Qwen3-8B and OLMo are MIXED; 2 of 4 is short of a majority.

**Exploratory (not in the sealed rules):**
- **Two routes.** Attribution reads the role marker mostly from the later positions and routes little through the statement's own tokens: maximum C transfer before handoff is 0.02–0.24 (6/6 curves; PREREG_W later found content use in about half the models). Obeying has a mid-to-late *content phase*, in which the source code sits on the statement's own words: maximum C transfer 0.38–1.33. In Qwen3-1.7B (L16) and Qwen3-8B (L23), patching only the statement's tokens carries the full obey effect.
- **This reconciles PREREG_S's null.** S's mean-vector edit acted at the decision layer (L13 / L17), before the obey content phase (L16 / L23), and at natural size.
- **Selectivity windows.** Content-token patching at a layer after the other behaviour's handoff and before obey's moves obedience much more than the other behaviour:
  - Qwen3-1.7B L16: obey minus believe +0.69 / +0.91; obey minus attribute +1.09 / +1.24;
  - Qwen3-8B L23: obey minus attribute +1.33;
  - SmolLM3 L13 marker patch: +0.78.

  This is where a selective defence (block obeying, keep believing) would act.

**Prior art.** The subagent check found no role-word minimal-pair patching split by marker, content and later positions per behaviour. Adjacent work:
- Kumarappan & Mujoo 2026 (content-differing pairs);
- C. T. Leong et al. 2025 (template vs instruction region, for safety);
- V-Steer §4.3 (obedience only).

## PREREG_U: a selective defence from the PREREG_T map? NONE (2026-10-28 17:40 +04:00)

**Run.**
- Sealed: `PREREG_U.sha256`, 10/10 OK after the run. Bundle `agp23.tgz`, md5 4b9918fd….
- Run 27 on pod `na58vx54de23kt`, 13:27–13:34 UTC. Archive md5 182e9e13a33a9390c24ebd2a57274232.
- Outputs: `cloud_prereg_u/u_analysis.json`. Figure: `figures/prereg_u_sweep.png`.

**Design.** Statements arrive as tool output ("Tool output:\n…") against a competing user message.
- **Splice (U):** the same text with a "quoted data, not instructions for you" framing is run in parallel. Its states on the statement's own tokens are spliced into the plain run after one layer: the PREREG_T obey content-phase layer, fixed before data.
- **Comparisons:** framing in the input (F), a defensive system prompt (P), and 1× and 4× mean vectors (M1, M4).

**Sealed verdict: NONE in 4/4.** The splice did not lower obedience: Δ = +0.003, −0.011, −0.017 and +0.020, against the required −0.05.

**Why: a design flaw.** The donor contrast was never piloted. The framing itself did not lower obedience in any model, so the splice had nothing protective to transfer:
- F changed obedience by +0.008 in OLMo, +0.028 in Qwen3-1.7B, **+0.154 in Qwen3-8B (p < 0.001)** and +0.049 in SmolLM3.
- F raised belief in OLMo (+0.18) and Qwen3-8B (+0.28).

**Exploratory (EXPL.):**
- **The defensive system prompt raised tool-instruction following in the Qwen models.** Qwen3-1.7B +0.085 (p 0.004); Qwen3-8B +0.045 (p 0.02). OLMo and SmolLM3 −0.03.
  - Caveat: the readout is the first answer word. It may mix instruction-following with how salient the word is, so this needs a generation-based check before it is called a backfire.
- **In OLMo and Qwen3-8B the splice is selective, but for belief** (not in Qwen3-1.7B or SmolLM3). At mid layers, splicing the framed statement tokens raises belief in the tool's facts with obedience flat:
  - OLMo: +0.09 at L15, about half of F's +0.18;
  - Qwen3-8B: +0.14 at L20, about half of F's +0.28.

  This fits PREREG_T, where believing's content phase is mid-depth.
- **The 4× mean vector lowered obedience more than belief in Qwen.** This is a possible lead, but a large perturbation.
  - Qwen3-1.7B: −0.167 vs −0.069, selectivity +0.098 [0.036, 0.163]. Applied after the fact, all four sealed criteria hold.
  - Qwen3-8B: −0.113 vs −0.069, which fails the half rule.
  - No help in OLMo (+0.032) or SmolLM3 (−0.034, with a selectivity CI that includes 0).

**Lesson.** Pilot that a donor manipulation moves the target behaviour in the intended direction before building an intervention on it.

## PILOT_V0 (PLAN_BIGGER Phase 0): readout audit and lever search. EXPLORATORY; rules fixed before data in PILOT_V0.md

**Run.** 2026-10-28, pod `veadr80jeiftal` (H100 NVL). The four models ran concurrently, from launch 15:52 to done about 16:27 UTC. Fetch md5 30e461996b6e5505a4aa1e05155f918c. Items are fresh (seed 2500): 48 instructions and 48 facts, both orders. Analysis: `cloud_v0_analysis/v0_analysis.json`.

### (a) Readout audit: FIRST_TOKEN_VALID in 4 of 4 models

The first-token score used in PREREG_S, T and U tracks what the models write in 24 generated tokens:

| Model | Agreement on decided jobs | Spearman ρ of condition means |
|---|---|---|
| Qwen3-1.7B | 0.986 | 0.989 |
| Qwen3-8B | 0.973 | 0.996 |
| SmolLM3-3B | 0.990 | 0.962 |
| OLMo-2-7B | 0.968 | 0.744 |

OLMo names neither answer in about half of its replies, so its decided set is smaller.

### (b) Lever search: LEVER_FOUND

The winner, chosen by the rule fixed in advance, is **tool−usr at depth 0.45, scale 4, on the statement tokens (C)**. It pushes the representation of tool-output text further from the user turn. Generation readout, against the plain tool run:

| Model | d_obey | d_bel | Decided rate drop | Passes |
|---|---|---|---|---|
| Qwen3-1.7B | −0.250 | −0.021 | 0.005 | yes |
| Qwen3-8B | −0.219 | −0.073 | 0.000 | yes |
| SmolLM3-3B | −0.372 | −0.064 | 0.000 | yes |
| OLMo-2-7B | −0.053 | +0.070 | 0.010 | no |

**Random direction**, same norm and settings: d_obey −0.125 (Qwen3-1.7B, where it also passes), −0.042 and −0.021, and −0.038 in OLMo.

**Runner-up.** The same direction on the whole tool turn (W) passes in 2 of 4. In Qwen3-8B it also cuts belief (−0.427), so it is not selective there.

### (c) Context, read by generation (exploratory)

- **The prompt defences raised obedience to tool-embedded instructions** in Qwen3-1.7B and Qwen3-8B. In Qwen3-8B, obey went from 0.417 (plain tool) to 0.479 with P (defensive system prompt), 0.458 with spot (datamarking) and 0.646 with frame. This matches PREREG_U's first-token finding.
- **SmolLM3 is the exception for spot:** obey fell from 0.479 to 0.385 while belief rose.
- **Source table:** "own" stays the least obeyed source in Qwen3-8B (0.271), as in PREREG_S.

### Next

Phase 1 (PREREG_V) tests the frozen recipe on fresh items (seed 2700) in the 4 pilot models plus 2 held-out families (Granite-3.3-8B, phi-4), against P, SPOT, REMIND and a random control. It was sealed and launched at 16:30 UTC (bundle `agp26`, md5 5c71d35032a54ba622da49f16c3f2005).

## PREREG_V (PLAN_BIGGER Phase 1): the sealed selective-defence test. Overall SELECTIVE

**Run.** Sealed bundle `agp27` (md5 ba5100e8f8b6ac15870de0e3c907d0bf; amended before any data from n 96 to n 72 per kind, because `make_items` ran out of names).
- Pod `veadr80jeiftal`, H100 NVL, 16:51 to about 17:00 UTC.
- Fetch md5 4f459237867a44b460c144fa17e65320. Working-copy seal check: 14/14 OK.
- Analysis: `cloud_prereg_v_analysis/v_analysis.json`.

**The recipe:** tool−usr at depth 0.45, scale 4, on the statement tokens. Read by generation, on fresh items (seed 2700, 72 instructions and 72 facts, both orders), against the plain tool run:

| Model | Verdict | d_obey (p) | d_bel | sel(DEF) 95% CI | RND d_obey | Beats P / SPOT / REMIND |
|---|---|---|---|---|---|---|
| Qwen3-1.7B | **SELECTIVE_DEFENSE** | −0.299 (0.0001) | −0.021 | [0.18, 0.38] | −0.118 | yes / yes / yes |
| SmolLM3-3B | **SELECTIVE_DEFENSE** | −0.361 (0.0001) | −0.097 | [0.19, 0.33] | −0.076 | yes / yes / yes |
| Qwen3-8B | SELECTIVE | −0.236 (0.0001) | −0.090 | [0.05, 0.25] | −0.069 | no / no / yes |
| OLMo-2-7B | SELECTIVE | −0.161 (0.035) | +0.079 | [0.07, 0.39] | +0.076 | no / no / yes |
| Granite-3.3-8B (held out) | SELECTIVE | −0.125 (0.0006) | +0.069 | [0.13, 0.27] | −0.090 | yes / no / yes |
| Phi-4 (held out) | NONE | −0.184 (0.0001) | −0.146 | [−0.05, 0.13] | 0.000 | no / no / no |

**H1 (effective):** 6/6. **H2 (selective):** 5/6. **H3 (beats all prompts):** 2/6. **H4 (beats random):** 5/6. **H5 (transfer):** Granite SELECTIVE, Phi-4 NONE.

**Prompt defences depend on the family:**
- In the Qwen models, P and SPOT raise obedience: Qwen3-1.7B +0.097 and +0.188; Qwen3-8B +0.062 and +0.056.
- In Granite, SPOT cuts it strongly (−0.368).
- In Phi-4, P cuts obedience (−0.271) but the decided rate falls by 0.354, because Phi-4 often answers neither option.
- **H3 compares selectivity (sel = d_bel − d_obey), so prompts that raise belief can win H3 even where they raise obedience** (Qwen3-8B: SPOT sel +0.167 against DEF +0.146). This is a property of the sealed metric, reported as is.

**Reading, fixed in advance:** SELECTIVE. The mechanism is a real selective handle: it lowers obedience in 6 of 6 models, including both held-out families, and is selective in 5 of 6. Prompt defences do as well or better in some families (Granite and Phi-4) and backfire in others (the Qwen models). The strict capability claim (SELECTIVE_DEFENSE in at least 4 of 6) is **not met**.

**Next:** Phase 3 (PREREG_X) tests the recipe on SEP and InjecAgent against the prompt defences, and stacked on them (X6). Sealed and launched 17:06 UTC.

## PREREG_W (PLAN_BIGGER Phase 2): the source map at scale. 4 of 5 predictions SUPPORTED

**Run.** Sealed bundle `agp25` (md5 2dc3458d8dae6fd03d771a277ab6b038); seal check 13/13 OK.
- Three H100 SXM pods, 16:52 to about 17:48 UTC: A `jfliwqroqhqarh`, B `jzjug88fmko5bh`, C `73tt16cn59g6zt`. All terminated after md5-verified fetches (A e62fca7f…, B 52a078e4…, C cbf2f095…).
- **Models:** 10 new ones from 6 families (Qwen3 0.6/4/14/32B, OLMo-2 13/32B, Phi-4, Granite-3.3-8B, Falcon3-10B, Yi-1.5-9B); 7 families with PREREG_T's SmolLM3. The 32B models were swept at stride 2 (34 of 64 layers).
- Analysis: `cloud_prereg_w_analysis/w_analysis.json`.

| Hypothesis | Rule | Result |
|---|---|---|
| W1, dissociation (PREREG_T's H2) | majority DISSOCIATED | **SUPPORTED, 9/10** (Granite UNCLEAR: mostly uninformative gaps) |
| W2, markers carry | ≥ 60% of curves MARKER | **SUPPORTED, 34/37 = 92%** |
| W3, obeying read later than attributing | majority OBEY_LATER | **SUPPORTED, 4/7** with a comparable pair (4 of 5 decided) |
| W4, no single tag (PREREG_S rule) | majority not UNIFIED | **SUPPORTED, 8/9** (5/9 FRAGMENTED; Phi-4 UNIFIED) |
| W5, content phase | obey content and attribute no content | **NOT SUPPORTED**: obey content 8/9 ✓, attribute no content only 4/9 ✗ |

**W3 by model:**
- OBEY_LATER: Qwen3-4B, 14B and 32B, and OLMo-32B.
- OBEY_EARLIER: Falcon3.
- UNDECIDED: Yi, Phi-4, OLMo-13B and Qwen3-0.6B.

**W5 detail.** Attribution also draws on the statement's own tokens (max T_C ≥ 0.2) in Qwen3-4B (0.27), OLMo-13B (0.40), Granite (0.36), Yi (0.24) and Falcon (0.29). PREREG_T's exploratory "attribution never routes through the content" does not generalize. The obey half does: obeying draws on the statement's tokens in 8 of 9 models. The relative depth of the obey content peak is mostly 0.53–0.79; the exceptions are OLMo-13B (0.30) and Phi-4 (0.43).

**Scale trend (reported).** In the Qwen3 ladder, the relative obey lag shrinks with size (Spearman −0.54): 0.14–0.21 at 1.7B, 0.25 at 4B and 8B, 0.13–0.18 at 14B, 0.09 at 32B. It stays positive. The OLMo ladder has only one computable lag (32B: 0.31).

**Sanity exclusions (ALL check outside [0.9, 1.1]), excluded from comparisons per the rule:**
- OLMo-32B attribute, own→usr;
- OLMo-13B obey, own→usr;
- Yi obey and believe, own→usr (the one-token role-word misalignment).

**Reading.** The core map generalizes across 7 families and up to 32B:
- behaviours read "who said this" differently;
- the role markers carry it;
- there is no single source tag.

Two parts are weaker or narrower. "Obeying is read later" holds in a bare majority and weakens with size within Qwen. "Attribution never uses the content" is refuted.

## PREREG_X (PLAN_BIGGER Phase 3): public prompt-injection benchmarks. Overall NONE (2 of 6); strong in the Qwen models

**Run.** Sealed bundle `agp28` (md5 abd279ee9da0ceafaa76016f20be7e49); seal check 15/15 OK.
- Two H100 SXM pods: 1 `xx71fmnf2cunzm` and 2 `4jij5v7h0sm6fr`, 17:06 to about 19:45 UTC. Both terminated after md5-verified fetches; list-pods is empty.
- Running three models concurrently ran out of GPU memory: Qwen3-8B (both benchmarks) and Granite's InjecAgent crashed before writing any data. They were re-run alone with the same sealed commands and batch sizes. The crash logs are kept as `*_oom_attempt1.txt`.
- Benchmark commits: SEP 7606c06, InjecAgent f19c9f2.
- Analysis: `cloud_prereg_x_analysis/x_analysis.json`. Figure: `figures/prereg_x_benchmarks.png`.

**Data:** SEP, 300 items. InjecAgent, 300 cases, with ASR computed on valid replies.

| Model | Verdict / X6 | SEP attack: none → DEF (utility none → DEF) | SEP DEF+SPOT | InjecAgent ASR: none → DEF (valid n) | InjecAgent DEF+SPOT |
|---|---|---|---|---|---|
| Qwen3-8B | **BEATS_BASELINES / ADDITIVE** | 30.0% → 13.7% (64.7 → 67.7) | 7.0% | 39.2% → 11.9% (233) | 10.1% |
| Qwen3-1.7B | EFFECTIVE / ADDITIVE | 28.3% → 5.7% (45.7 → 47.0) | 3.3% | 56.8% → 3.2% (30) | 6.3% |
| SmolLM3-3B | NONE | 41.7% → 24.7% (48.0 → 54.0) | 4.7% | 3.9% → 0.7%, floor (116) | 2.1% |
| Granite-3.3-8B | NONE | 44.7% → 35.7% (66.3 → 68.0) | 38.3% | 46.1% → 40.5%, n.s. (77) | 38.1% |
| OLMo-2-7B | NONE | 56.0% → 44.0% (61.3 → 73.7) | 24.0% | 89.6% → 87.1%, n.s. (98) | 62.0% |
| Phi-4 | NONE / PARTLY | 24.3% → 22.3%, n.s. | 14.7% | 21.5% → 11.0% (198); RND 12.4% | 9.7% |

**By hypothesis:**

| Hypothesis | Models passing |
|---|---|
| X1, SEP effect | 5/6 (all but Phi-4) |
| X2, SEP beats all prompts | 4/6 (OLMo, Qwen3-8B, SmolLM3, Granite; Qwen3-1.7B ties SPOT) |
| X3, InjecAgent effect | 3/6 (Qwen3-1.7B, Qwen3-8B, Phi-4) |
| X4, InjecAgent beats prompts | 2/6 (the Qwen models) |
| X5, beats the random control on both | 2/6 |
| X6, adds to both prompts | 2/6 (the Qwen models); Phi-4 adds to P only |

**Reading, fixed in advance.** Overall NONE: fewer than 4 of 6 models are EFFECTIVE. The capability criterion is met in one model (Qwen3-8B) and not across models.

**Pattern (stated as observed, not as a sealed claim):**
- On SEP (a tool-output-style turn), the steering lowers attack success in 5 of 6 families and beats the prompt defences in 4.
- On InjecAgent, where the injected observation sits inside a long user message rather than in a tool turn, it helps only the Qwen models and Phi-4.
- The recipe was tuned on synthetic tool turns. It transfers to SEP's tool-turn format broadly, but to InjecAgent's embedded format only in the Qwen family.
- Stacking on datamarking gives the lowest SEP attack success in 4 of 6 models. It ties for lowest in Phi-4 (DEF+P is 14.7% too), and in Granite the steering alone is lowest.

## PILOT_V1: a format-matched lever for injections embedded in a message. EXPLORATORY; NO_FORMAT_LEVER

**Run.** Pod `ccelf8b05wcqtu` (H100 SXM), 20:47 to about 21:45 UTC; terminated after an md5-verified fetch (cefc9360…). Rules in PILOT_V1.md, fixed before data. Data: 60 InjecAgent dev cases outside the 300 PREREG_X test cases.

**Question.** In PREREG_X, the recipe failed on InjecAgent in OLMo, Granite and Phi-4, where the observation is embedded in a user message. Would a direction computed in that format work instead? It is obs−input: neutral sentences as the Observation minus the same sentences as the User Input, inside the InjecAgent template.

**Result: NO_FORMAT_LEVER.** The winner among the eligible configurations (valid-rate drop ≤ 5 points in the three models, no harm in Qwen3-8B) was obs−input at depth 0.65 × 8. Its mean dASR over OLMo, Granite and Phi-4 was −0.029, short of the −0.10 gate.

- **Shallow settings (0.35–0.45) "work" only by breaking the agent.** In OLMo and Phi-4, ASR falls 0.06–1.0 while valid replies fall 8–53 points. That is not a defence.
- **Deeper settings keep validity but do little:** OLMo −0.09 / −0.22 on 9–11 valid pairs; Granite +0.14 to +0.20; Phi-4 −0.04 to −0.07.
- **Qwen3-8B (reference): the format-matched direction is strong.** ASR goes from 0.27 to 0.00–0.02 at depths 0.35–0.55, with the valid rate up 10–13 points. That is better than the PREREG_X recipe on these dev cases (−0.13).
- **Power.** OLMo and Granite give valid ReAct replies in only about 30% of cases, so 1–16 pairs were usable per configuration. The pilot cannot rule out small effects there.

**Reading.** No format-matched lever that keeps the agent working was found outside Qwen. The InjecAgent capability stays a Qwen-family result (plus a partial Phi-4 effect in PREREG_X). PREREG_Y is not triggered.

## PREREG_Y: the lever at larger Qwen3 sizes (Y1) and its SEP advantage in held-out families (Y2). Y1 PARTIAL, Y2 SEP_EFFECTIVE

**Run.**
- Sealed bundle `agp30` (md5 28b86845…), with a seal check of 18/18 from a clean extract before the analysis. The PREREG_X code is byte-identical.
- **Part A:** pod `w4ahinp7ckgye2` (H100 SXM, US-NE-1), 03:25–05:48 UTC. Fetched with md5 ee26efed…; the pod is terminated. Benchmark commits were verified on the pod. There were no out-of-memory retries; Qwen3-32B's SEP ran at batch 32.
- **Part B:** Qwen3-32B on InjecAgent, pod `kvnpaw0mlnbvt5` (H100 NVL, network volume), 03:38–06:18 UTC, at batch 8 with no out-of-memory retry. Fetched with md5 1d3acd95…; the pod is terminated.
- **Analysis:** `cloud_prereg_y_analysis/` (`y_analysis.json`, md5 8bd9a033…; `y_tables.md`), run on both parts combined from a clean bundle copy.

**Y2, final: SEP_EFFECTIVE.** The steering lowers SEP attack success in every held-out model (X1 4/4), but beats all three prompt defences in none (X2 0/4).

| Held-out model | SEP attack: none → steering (utility) | Lowest prompt attack | X1 | X2 (the prompt it fails against) | X5 (SEP) | Verdict |
|---|---|---|---|---|---|---|
| Falcon3-10B | 48.7% → 33.0% (67.3 → 68.0) | SPOT 28.3% | yes | no (SPOT, CI [−0.02, 0.14]) | yes | SEP_EFFECTIVE |
| Yi-1.5-9B | 47.3% → 30.7% (66.7 → 66.0) | SPOT 37.7% | yes | no (REMIND, CI [−0.13, 0.03]) | yes | SEP_EFFECTIVE |
| OLMo-2-13B | 43.7% → 38.3% (69.3 → 70.0) | SPOT 39.3% | yes (−0.053, p 0.005) | no (REMIND) | no (RND, CI [−0.01, 0.09]) | NONE |
| OLMo-2-32B | 58.7% → 47.3% (88.7 → 89.3) | REMIND 49.3% | yes | no (REMIND, CI [−0.04, 0.08]) | yes | SEP_EFFECTIVE |

**Reading, fixed in advance:** the lever helps on SEP in held-out models but does not beat the prompt defences there.

**Observed, not preregistered:** PREREG_X's observed "beats all prompts on SEP in 4 of 6" does not replicate in new families: on SEP the steering is about as good as the best prompt defence (usually the reminder), not better.

**Y1, final: PARTIAL.** Qwen3-14B is NONE, failing X5 only; Qwen3-32B is EFFECTIVE, failing X2 only. Both are ADDITIVE.

**Qwen3-14B: NONE, because of X5 alone.**
- **X1–X4 all hold.**
  - SEP: attack success 37.0% → 18.3% (utility 71.0 → 72.3%), beating P, SPOT and REMIND.
  - InjecAgent: attack success 29.2% → 4.6% (valid 94.7 → 93.3%), beating all three prompt defences.
  - ADDITIVE on top of both P and SPOT.
- **X5 fails on InjecAgent.** The same-norm random vector also cuts attack success, to 4.9% (with a valid rate of 89.3%); DEF − RND has CI [−0.03, 0.02]. On SEP the steering does beat the random vector (CI [0.02, 0.14]).
- **At 14B, on InjecAgent, the single random draw did as well.** One draw cannot separate a direction-free effect from an unusually effective draw. RNDCTL (exploratory, Qwen3-4B, 32 draws) found random effects sign-varying and centred near zero, but in a different setup (Qwen3-4B), so it does not settle the question here. A multi-draw benchmark control would.
**Qwen3-32B: EFFECTIVE (X1, X3, X4 and X5 hold; X2 fails).**
- SEP: attack success 40.3% → 30.0% (utility 73.3 → 72.3%). It beats P and SPOT but ties the reminder (CI [−0.02, 0.11]), so X2 fails.
- InjecAgent: attack success 27.8% → 8.6% (valid 96.0 → 92.7%). It beats all three prompt defences (the reminder by CI [−0.12, −0.03]).
- It beats the random vector on both benchmarks (InjecAgent RND 18.5%, CI [−0.16, −0.07]), on SEP only by one item in 300 (CI lower bound +0.003), which holds in about half of bootstrap reseeds. Y1's PARTIAL rests on that margin.
- ADDITIVE with P and SPOT (DEF+P 7.7% on InjecAgent).

**The Qwen3 size series (PREREG_X and Y): 1.7B EFFECTIVE, 8B BEATS_BASELINES, 14B NONE (X5), 32B EFFECTIVE (X2); ADDITIVE at every size.**
- The lever cuts attack success substantially at every Qwen3 size on both benchmarks. It beats every prompt defence on both at 8B and 14B, but passes the single-draw random control as well only at 8B.
- **Size trend (descriptive, as preregistered).** InjecAgent attack success with the steering minus the best prompt's: −0.38, −0.22, −0.18, −0.06 (1.7B to 32B). On SEP, Net minus the best prompt's Net: +0.05, +0.10, +0.09, +0.05.
- At 14B the InjecAgent drop is matched by the single random draw (see above).
- No size trend is claimed; this is reported, not tested.

**Cost.**
- Part A: about $9.6 (pod time about 2.41 h at $3.99/h), against E33's computed $10.88.
- Part B: about $8.8 (about 2.75 h at $3.19/h), against E34's $8.86.
- PREREG_Y total: about $18 from pod times (the recheck finds at least $18.16 from logged times). To be reconciled with the billing explorer.

## RNDCTL (2026-10-29, exploratory): the single random draw is not a neutral control

Qwen3-4B (4-bit), the inj2 setup, 48 cases, 16 isotropic draws at ±2 (`RNDCTL_RESULTS.md`; predictions in
`RNDCTL_PRED.md`, hashed before the run). Random effects flip with the draw's sign (corr(+r, −r) −0.85 doc,
−0.59 sys) and are not a norm effect (inflate ≤ 0.02). inj2's draw was an outlier: 91st percentile in doc and the top
draw in asst and sys. −vR beats all 32 draws in every placement. +vR's defence is at the floor in doc and asst and only
modestly beyond random in sys (−0.771 vs the lowest draw's −0.696). Single-draw RND comparisons (inj2, V H4, X X5,
Y X5) should be reported as single-draw, or rerun with ≥ 16 draws.

## MPILOT (2026-10-29, exploratory): the PREREG_M wording effect is mainly a rival-plan penalty; the turn gap survives a matched position

Qwen3-8B bf16, 3-way world, 71 cells × 40 paired seeds (`MPILOT_RESULTS.md`; bets from Codex and Claude, recorded
before launch in `MPILOT_PRED.md`). Both gates pass (competence +0.708; the PREREG_M plan pair reproduces, D0 −0.183
[−0.227, −0.140]).

Against a neutral header:
- "Another manager's plan" −0.150 [0.114, 0.187];
- "Your own plan" +0.033 [0.022, 0.045];
- "Dana's plan" −0.003, n.s.

10/10 paraphrase sets share the sign. With no header, system − assistant at matched insert steps is +0.028 [0.013, 0.046]. "Your own" > "My own" in the system turn (+0.051). First person gains relative to "your own" in the assistant turn (interaction +0.037), but does not overtake the system turn. Brier scores: Codex 0.174, Claude 0.214.

**MPILOT failed predictions:**
- **O3 FALSE by rule:** "Your own" − "My own" was +0.051 [0.030, 0.075] in the system turn but only +0.016 [0.008, 0.026] in the user turn, under the 0.02 threshold.
- **O7 FALSE:** "My own" in the assistant turn − in the system turn was −0.017 [−0.029, −0.005].

Codex and Claude both bet against O7 (0.18 and 0.20). Both bet for O3 (0.62 and 0.55).

## AUTHPILOT (2026-10-29, exploratory): the rival-plan penalty vanishes in Qwen once the plan is assigned

Qwen3-8B and OLMo-2-7B-Instruct, bf16, 3-way world, 59 cells × 30 paired seeds (`AUTH_RESULTS.md`; bets from Codex and
Claude, recorded and hashed before launch in `AUTH_PRED.md`). Both gates pass in both models; Qwen reproduces MPILOT's
rival penalty (P(x) +0.126 [0.096, 0.161]).

Rival penalty (neutral − "Another manager's"):
- **Qwen:** none +0.126; binding **+0.000 [−0.011, 0.013]**; background-only +0.171.
- **OLMo:** none +0.088; binding +0.036 [0.029, 0.042] (29/30 seeds); background-only +0.094.

**Kill rule fired:** A2-kill TRUE in Qwen with its baseline reproduced, so by the pre-written rule the penalty is
remit/applicability, not a source tag that overrides authority. OLMo's small residual is not a tested model difference.
Brier: Codex 0.251, Claude 0.235.

**AUTHPILOT failed predictions:**
- **A2_Q FALSE:** the penalty did not survive binding authority in Qwen (+0.000). Codex 0.64, Claude 0.55 bet it would.
- **A1_L FALSE:** binding headers did not raise following of the neutral plan in OLMo (+0.004). Codex 0.65, Claude 0.55.
- A2-kill_Q came out TRUE against both bets (Codex 0.18, Claude 0.25).

## REVPILOT (2026-10-29, exploratory): can hierarchy training reverse user > system? NO_REVERSAL (design flaw)

Qwen3-8B and OLMo-2-7B; LoRA adapters trained (n 240, two data seeds per arm) to let the system (sys) or the user
(usr) win system-user conflicts in 8 non-finance domains; evaluated on the 3-way fund world, seeds 5000-5029
(`REVPILOT.md`, `REVPILOT_RESULTS.md`). Base models replicate user > system (D = gF − uF: Qwen −0.032, OLMo −0.093).

Both arms drove p_goal to the ceiling, even with no reminder (Qwen about 0.998 in every cell; OLMo sys1000 0.948 with
no reminder), so all four Qwen adapters and one OLMo adapter are BROKEN by the pre-written rule, and OLMo's D moved
toward zero in both arms (OPPOSITE fails). Cause: every training round carried a pressure line that the targets
ignored in both arms, so both learned pressure resistance, the thing the fund world measures. The axis question is
untested, not answered. About $1.8.

**REVPILOT failed predictions:** none were bet; the pilot's go rule failed (no model REVERSED or SHIFTED with OPPOSITE
and not BROKEN).

**REVPILOT pilots 2 and 3 (same day, exploratory; `REVPILOT_RESULTS.md`).** Pilot 2 (no pressure lines, n 48)
confounded role with position: the system always spoke first, so the arms learned "first instruction wins" vs
"latest wins" (Qwen system-reminder following 0.931 → 0.568/0.774 in the sys arm). Pilot 3 balanced the order; the
arms then did not differ (sys − usr in D: Qwen +0.004, OLMo +0.024), while data seeds within an arm differed by up
to 0.12. The user > system order survived every readable adapter. By the stopping rule fixed before pilot 3, the
reversal lane is closed; PREREG_R was not run. Three pilots cost about $3.8.

## TAGSTYLE (2026-10-29, exploratory): role tag × writing style. OUTCOME NONE by rule; style moves behaviour far more than the tag

60 obey + 60 believe items (seed 2800), statement in a system or user turn × plain / system register / casual
register, 6 models (`TAGSTYLE.md`, `TAGSTYLE_RESULTS.md`). OLMo-2-7B and SmolLM3 are INVALID (attribution mass < 0.5).
No pattern held in 4 valid models, so no sealed follow-up. Descriptively, the style effect on obedience exceeds the
tag effect in 4 of 6 models, 3 of the 4 valid ones (Qwen3-8B +0.64 vs −0.02, Granite +0.45 vs −0.08, phi-4 +0.37 vs
+0.09), and on belief in 5 of 6 (3 of 4 valid); perceived source follows style in 3 of the 4 models with a valid
attribution readout (narrowly in phi-4). S compares two rewrites, a bigger change than one tag switch. The tag effects Papers A/B study are real but small next to
register, consistent with Ye et al.'s "style, not tags". Caveat: the registers carry credibility and authority cue
words. About $0.25.

## FLIP (2026-10-30, sealed): does the role axis follow gpt-oss's trained priority? SAME/AGREE; no reversed model, lane stops

gpt-oss-20b (explicit system > developer > user training), harmony wrappers written by hand and checked against the
official template; 3-way fund world, seeds 9100-9159; vR at layer 11 (`FLIP.md`, `FLIP_RESULTS.md`). Gate PASS; valid
(mass ≥ 0.978; every reminder +0.44 over none).

- p_goal: none 0.531, system 0.965, developer 0.967, user 0.974, own 0.949. D = developer − user = −0.0075 (CI −0.013
  to −0.003, p < 0.001) → SAME: the user's mid-conversation reminder is followed slightly more, as in the 9 models.
- Axis: user −176 vs developer −118 on vR (t −234 vs null q95 |t| 121) → AGREE; pairs 4 agree, 1 unresolved,
  1 undecided, 0 disagree. gpt-oss is a 10th model and 5th family where vR orders the reminder as behaviour does.
- Caveats: the random null is high (most directions separate user-turn tokens); system, developer and own sit within
  2 units on vR, so vR mostly separates user from the rest and does not scale with the (small) behavioural gaps;
  mid-conversation developer/system turns are outside the official template.
- By the rule fixed before data, no 120b run; the priority-reversal lane is closed. About 9 min, about $0.40.

## CHANNEL (2026-10-30, sealed): does user > system follow the pressure's channel? USER_PRIMACY; the confound is removed

The pressure lines of each test step were moved out of the quarter message into their own user turn or their own
system turn (developer for gpt-oss), with a neutral-system-turn placebo; 10 models, 5 lineages (Qwen3, Qwen2.5, OLMo-2,
Falcon3, Granite, gpt-oss), seeds 9300-9359 (`CHANNEL.md`, `CHANNEL_RESULTS.md`). Manipulation check PROCEED; all 10
valid with a base effect.

- PRIMACY in 9 of 10 (Falcon3-10B NONE): the user reminder beats the system reminder even when the pressure arrives as
  a system turn (D_S > 0 in 10/10), and the user advantage grows in 8 of 10. No reversal; channel matching refuted.
- System-turn pressure is weaker than user-turn pressure in all 10. Exploratory: one neutral system turn between the
  pressure and the decision raises goal-following in all 10 (recency).
- The user > system order in the 3-way world is not a pressure-channel artefact. Reversal lane closed again. About
  2.1 h on an H100 NVL, about $5.5.
