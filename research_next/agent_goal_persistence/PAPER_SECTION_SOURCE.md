<!-- To be merged into PAPER_DRAFT.md after §6f once the independent numbers and reference checks finish. Written 2026-10-28. -->

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
- **Edit.** A user↔own tag transplant at the decision layer, with same-norm random controls.
- **Models.** Qwen3-1.7B, SmolLM3-3B, Qwen3-8B, OLMo-2-7B-Instruct.
- **Rule.** SOURCE_MONITOR requires, in a majority of models, all of: a readable tag; obey and believe ranking the sources alike (Kendall τ ≥ 0.6); attribution ≥ 0.6; and an edit that moves the behaviours as predicted.

**Result: FRAGMENTED** (3 of 4 models; OLMo PARTIAL).
- **Obey and believe rank the five sources differently in every model** (τ = 0.2–0.4).
  - Qwen3-8B obeys the user most (0.53) and its own earlier turn least (0.25), but believes the system most (0.75).
  - It believes tool output (0.67) while obeying it less (0.42).
  - Qwen3-1.7B obeys tool output *more* than the user (0.71 vs 0.51).
- **Source effects do not require reportable source knowledge.** OLMo and SmolLM3 show reliable source effects (p < 0.001) yet attribute near chance (0.32 and 0.32; chance 0.20). Qwen3-8B attributes well (0.87).
- **The source is readable from the statement's own tokens** at the decision layer: 0.87–0.94 in three models, and 0.69 in Qwen3-1.7B at layer 13 (0.91 at layer 18).
- **Transplanting that readable tag between user and own text does not carry the behaviour.**
  - At natural size (×1) the edit moved nothing as predicted in three models.
  - In OLMo only obedience moved (+0.004).
  - Belief moved slightly the *opposite* way in Qwen3-1.7B and OLMo.
  - All edit effects were ≤ 0.03, against best-to-worst source gaps of 0.07–0.46.
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
- **The reverse transplant (own→user) does move obedience a little,** in Qwen3-1.7B, Qwen3-8B and OLMo. In Qwen3-8B this is 22% of the own–user gap at ×2.
- **Qwen3-1.7B's attribution moves away from "own"** under this edit (−0.04 at ×1, −0.07 at ×2) while its obedience barely moves.

**Reading.**
- Source information is present but used piecemeal. This predicts that a defence which fixes one behaviour (for example obedience to injected text) will leave the others (belief, attribution) unchanged.
- It also suggests a different kind of defence. Some models already believe tool output while obeying it less. A *selective* intervention could lower obedience to injected instructions while keeping belief in the injected text's facts. Defences built to be selective (Shilov et al. 2026; R. Liu et al. 2025; Penman 2026) report attack success and generic utility, but none measures belief in the injected text's own facts.

**Prior art and limits.**
- Leong (2026: no abstract provenance code) and Zeng (2025: distinct subspaces) predicted fragmentation.
- An *amplified* user-minus-tool mean vector does steer injection (Zhang, Lee & Park 2026; Liu 2026). Our null is at natural size only.
- The joint obey/believe/attribute test with a causal transplant appears not to have been run before (prior-art check, 2026-10-28).
- **Limits:** four models, 1.7B–8B; synthetic items; one edit layer per model.
