# PREREG_T: where is the source signal the model actually uses?

Written 2026-10-28 after PREREG_S (FRAGMENTED) and before any PREREG_T data. This follows the approved plan, step 3 ("scale it the J-space way"), which the user authorised with "autonomously do the rest, and do it fast".

Sealed in `PREREG_T.sha256` with:
- `code/src_patch.py`, `code/t_analyze.py`;
- `cloud/rc26.sh`, `cloud/ss26.sh`;
- the helpers `code/src_monitor.py`, `code/agp_batch.py`, `code/agp_b.py`, `code/chat_fmt.py`.

## Why this test

**What PREREG_S showed:**
- The source of a sentence is readable from its own tokens (0.69–0.94 at the decision layer).
- Moving the mean "tag" vector between user and own-turn text barely changes whether the model obeys or believes it.
- Obeying, believing and attributing use source information differently.
- Exploratory: read through the J-lens, the readable tag looked genre-like.

So the source signal that behaviour uses must live somewhere else. The candidates:
- the role-marker tokens;
- an item-specific (non-mean) code on the content tokens;
- positions after the turn that have already read the source.

**What this test does.** It localizes that signal with activation patching, separately for each behaviour. The output is a layer-by-layer map: where each behaviour reads "who said this".

## Design (`code/src_patch.py`)

**Pairs.** The same statement is placed in a donor turn and a recipient turn: own → usr, and sys → usr.
- These turns are token-aligned in all four models: only the role word differs.
- Exception, OLMo own: the assistant turn ends in EOS while a user turn's final ".\n" merges into one token.
- Alignment is therefore segment by segment: the prefix and the content from the start, the end tokens and the later positions from the end. The unmatched EOS is not patched.
- The quoted-page and tool sources wrap the statement in extra words, so they are not aligned and are left out.

**Items.** Fresh: 48 fact and 48 instruction items, seed 2200. Both orders of the statement and the competing user message, as in PREREG_S.

**Readouts, as in PREREG_S:**
- obey (instruction items) and believe (fact items): score P(A)/(P(A)+P(B));
- attribute ('Which message contained the sentence …?', five lettered options): P(letter of the donor's source).

**Patching.**
- The donor run is cached at every layer.
- The recipient run is repeated with the residual stream after one layer replaced by the donor's, on one position set:
  - M: the turn's marker tokens (role prefix and end tokens);
  - C: the statement's content tokens;
  - D: every position after the turn (the competing message, the question and the answer header);
  - ALL = M + C + D, at the first, the decision and the last layer only, as a sanity check: it must reproduce the donor.
- Every layer is patched, for each set.

**Models and decision layers:** as in PREREG_S — Qwen3-1.7B (13), SmolLM3-3B (7), Qwen3-8B (17), OLMo-2-7B-Instruct (10). That is three families, 1.7B–8B.

## Rules (`code/t_analyze.py`)

Per model, pair and behaviour. Values are averaged over the two orders per item.

**Gap and transfer.**
- gap = mean(donor − recipient). A behaviour is INFORMATIVE if |gap| ≥ 0.05 with sign-flip p < 0.05 over items.
- Transfer T_s(l) = mean(patched − recipient) ÷ gap.
- Sanity: T_ALL must lie in [0.9, 1.1] at the check layers. A model-pair failing it for a behaviour is excluded for that behaviour.

**Handoff and carrier.**
- Handoff h = the first layer at which T_D ≥ 0.5: the point by which most of the used source information has left the turn.
- Carrier before the handoff: A_M = mean T_M over layers < h, and A_C likewise.

| Carrier | Condition |
|---|---|
| MARKER | A_M ≥ 2·A_C and A_M ≥ 0.2 |
| CONTENT | A_C ≥ 2·A_M and A_C ≥ 0.2 |
| SHARED | both ≥ 0.2, otherwise |
| WEAK | both < 0.2 |
| NONE | h = 1 |

- Bootstrap over items (1000 resamples) for the handoff layers.

**H1: where obeying and believing read the source.**
- A model is MARKER if every informative obey/believe curve (both pairs) is MARKER, and CONTENT if every one is CONTENT.
- Overall: MARKER_CARRIES or CONTENT_CARRIES by majority (3 of 4 models), else MIXED.

**H2: do the behaviours read it differently?**
- A model is DISSOCIATED if, within a pair, two informative behaviours either:
  - have different carriers, both in {MARKER, CONTENT}; or
  - have handoff layers ≥ 3 apart, with the bootstrap 95% CI of the difference excluding 0.
- A model is SHARED if, in every pair, all informative behaviours share one carrier and handoffs within 2 layers (at least one comparison needed).
- Otherwise UNCLEAR. Overall by majority, else UNCLEAR.

## Expectations, stated now

**H1: MARKER_CARRIES.** The mean content-token transplant failed in PREREG_S, so the role-marker tokens are the likelier carrier. Full item-specific content patching is a much stronger intervention than the mean vector, though, so CONTENT is a live alternative.

**H2: DISSOCIATED.** PREREG_S found the behaviours use source differently. Exploratory hint: in Qwen3-1.7B, attribution moved with the content-token edit while obedience did not.

## Readings fixed now

- **MARKER_CARRIES.** Models decide whose words they are from the role tokens. The readable tag on the words themselves is a by-product. A defence can then target the role-marker read, not the text.
- **CONTENT_CARRIES.** The source is re-encoded onto the words, item by item, not as one shared vector. That explains why the mean transplant failed.
- **DISSOCIATED.** Each behaviour reads the source at a different place or time. This is the mechanism behind PREREG_S's fragmentation, and it shows where a selective defence (block obeying, keep believing) could act.
- **SHARED.** One read point serves all behaviours. Fragmentation then arises after the read, downstream.

## Tests before sealing (code paths only; no numbers enter the analysis)

- **Qwen3-0.6B on CPU,** 2 items per kind. The ALL check must reproduce the donor.
- **OLMo and SmolLM3 tokenizers and chat formats, with a stand-in network:**
  - every path ran;
  - OLMo own → usr differs by one token in every prompt, as expected, and aligned as designed: `assistant`↔`user` paired, '.'↔'.Ċ', EOS left out.
- **Planted patch files with known answers.** All four models got the expected H1/H2 labels (MARKER/DISSOCIATED, CONTENT/SHARED, MIXED/UNCLEAR, MARKER/DISSOCIATED-by-timing).

## Prior art (subagent check, 2026-10-28, before sealing)

**Role-token patching: partly covered.**
- V-Steer (2607.26228, §4.3) attributes obedience to heads reading content spans, with no layer sweep.
- 2605.12991 (§4.3, §6) patches peer-pressure flips at layers 14–18 of Llama-3.1-8B, but its paired runs differ in content, not only the role word.
- Leong et al. (2502.13946, §3.3) patch template positions against instruction positions, but for harmfulness, not source.

**Obey / believe / attribute: partly covered.** Each has been studied alone: obeying in V-Steer and Balp-Straffon; attribution in Ackerman & Panickssery 2410.02064 and G. & Lindsey 2605.25459 §3.3–3.4. None splits all three on one manipulated source.

**Natural-size content code not causal, delimiters carry it: appears open, and prior work leans the other way.**
- "Steering Role Confusion" (LessWrong, Aug 2026) adds an *amplified*, norm-scaled user-minus-tool mean difference at layer 11 on command tokens. It moves attack success in gpt-oss-20b from about 0 to about 80%.
- Liu (NeurIPS 2026) uses the same direction as a defence.
- PREREG_S's null was at natural size (×1, ×2 of the centroid difference), so it does not contradict them. This test's C patch is also natural-size, item-specific and complete, which makes it the matching test.

**Selective defences: partly covered.** TrustAttention (NeurIPS 2026), DRIP (2511.00447) and Semantic Overlays (2608.23873) are built to be selective. None measures belief in the injected text's own facts.

**What appears new:** role-word minimal-pair patching split by marker, content and later positions, layer by layer and separately for obey, believe and attribute on identical text.

## Cost

Estimated from PREREG_S's measured run:
- PREREG_S did about 2,760 batch-32 forwards per 4 models in about 15 minutes, including about 6 minutes of downloads.
- This run is about 13,300 batch-24 forwards, roughly 3.6 times PREREG_S's compute.
- Total: about 9 × 3.6 + 6 ≈ 38 minutes, or about $1.1 at $1.79/h.
