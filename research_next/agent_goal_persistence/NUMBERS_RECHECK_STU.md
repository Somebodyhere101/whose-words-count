# Numbers recheck: PAPER_B_SOURCE_MONITORING.md, §3.1 (PREREG_S), §3.2 (PREREG_T), §3.4 (PREREG_U)

Independent recheck, 2026-10-29. The scope is §3.1, §3.2 and §3.4 in full, plus every sentence in the Abstract, §1, §2, §4, §6 and Data and code that states a number or verdict resting on PREREG_S, T or U. §3.3 and §3.5–§3.7 are out of scope. `PLAN_7DAY.md`, `CONSOLIDATED_RESULTS.md` and `PAPER_DRAFT.md` were used only to locate files, never as evidence.

**Paper version checked.** `PAPER_B_SOURCE_MONITORING.md`, sha256 `35ec8a31282a0277…`, saved 2026-10-29 07:03:07 (463 lines).
- The file changed while this recheck ran: line 9 and the AI-use statement were edited after 05:21.
- §3.1–§3.4 are identical in both versions. Quotes below are from the 07:03 version.

**Paths.**
- `RF/` = `research_next/agent_goal_persistence/`.
- `SC/` = `C:/Users/caabm/AppData/Local/Temp/claude/C--Users-caabm-Downloads/b2d893aa-daa4-417d-a29a-85a40bff7760/scratchpad/recheck_stu/`, the scratch run folder. Nothing was written inside `RF/`.

**Method.**
- The three seals were checked with `sha256sum -c` from `RF/`.
- The sealed files and the three `cloud_prereg_*` folders were copied to `SC/`, and the seals were re-checked there.
- The pod archives (`results25/26/27.tgz`) were extracted and compared byte for byte with the raw files.
- Each analysis script was re-run on CPU (`CUDA_VISIBLE_DEVICES=""`, `AGP_DEVICE=cpu`), and its output was compared byte for byte with the stored `*_analysis.json`.
- Claims with no stored statistic were recomputed from the raw files with four scratch scripts (`SC/recompute_{s,t,u,jspace}.py`, outputs in `SC/rerun/`). They copy the sealed conventions: per-item averaging over orders, `signflip` with seed 0 and 20,000 permutations, and the sealed bootstrap with seed 0.

**Status legend** (as in `NUMBERS_RECHECK.md`).
- **MATCH:** the primary value, rounded half-up to the paper's precision, equals the paper's value.
- **ROUNDING:** off by one unit in the last digit, which rounding an already-rounded stored value explains.
- **MISMATCH:** the primary data contradict the statement under any reasonable reading of its scope.
- **UNVERIFIABLE:** no primary file is available.
- **Flag O#:** the numbers are right, but the wording claims more than the data or gate support. These are listed separately below.

## Summary

**Counts (97 claims in scope).**

| Status | Count |
|---|---|
| MATCH | 92 (17 of them flagged O1–O12; 2 more carry a note under O12) |
| ROUNDING | 1 |
| MISMATCH | 4 (1 numeric, 1 quantifier/scope, 1 factual, 1 path) |
| UNVERIFIABLE | 0 |

**Overstatements:** 12 (O1–O12). O12 rests partly on PREREG_W, which is out of scope.

**Seals and re-runs.**
- All three seals verify: 28 of 28 entries OK, in `RF/` and in the scratch copy.
- The bundles `agp21`, `agp22` and `agp23` contain every sealed file with a matching hash.
- All 20 raw result files are byte-identical to the pod archives.
- `s_analyze.py`, `t_analyze.py` and `u_analyze.py` reproduce their stored JSON **byte for byte**.
- `s_jspace.py` was not run, because it loads the Qwen3-1.7B weights for W_U. Its rule-(b) fractions were recomputed from `reps.pt` and the J-lens file, without model weights, and are identical to `s_jspace.json` at all six layers.
- **No gate verdict changes.**

## MISMATCH list, with exact evidence

**M1. §3.2 H1: "the role-marker tokens are the main carrier in 11 of 13 informative curves" [numeric].**
- Evidence: `RF/cloud_prereg_t/t_analysis.json` → `models.<model>.<pair>.<behaviour>.informative` / `.carrier`. The re-run is byte-identical.
- There are **16** informative curves, all of which pass the sanity check (`excluded_insane` is empty everywhere). **14 are MARKER, 2 are SHARED** and 0 are CONTENT:
  - OLMo: own→usr believe SHARED; sys→usr believe and attribute MARKER (3 curves).
  - Qwen3-1.7B: all six curves MARKER (both pairs × obey, believe, attribute).
  - Qwen3-8B: own→usr obey SHARED and attribute MARKER; sys→usr believe and attribute MARKER (4 curves).
  - SmolLM3: own→usr obey MARKER; sys→usr obey and attribute MARKER (3 curves).
- H1 itself uses only obey and believe curves: **8 of 10** are MARKER.
- "11 of 13" is what you get if SmolLM3's three MARKER curves are left out. It first appears in `PLAN_7DAY.md` (2026-10-28 17:25) and was carried into `CONSOLIDATED_RESULTS.md` and the paper.
- The rest of the sentence is correct: the two SHARED curves are the ones named, none is content-only, and 2 of 4 models are all-MARKER.
- **Suggested wording:** "Before the handoff, the role-marker tokens are the main carrier in 14 of 16 informative curves (8 of the 10 obey and believe curves that H1 uses). Two curves (Qwen3-8B own→usr obey; OLMo own→usr believe) share the carrier with the statement's own tokens, and none is content-only."

**M2. §3.1: "All edit effects were ≤ 0.03, against best-to-worst source gaps of 0.07–0.46" [quantifier/scope].**
- The statement is true only for the sealed **user→own ×1** test. Its largest effect is Qwen3-1.7B belief −0.0275 (`s_analysis.json` → `models.*.edit_tests`). The 0.07–0.46 gap range is correct (0.0729–0.4602).
- The same section describes the edit as a "user↔own tag transplant" and heads the bullets "between user and own text". The own→user arm at ×1 exceeds 0.03 (beyond the random control, from `SC/rerun/recompute_s.json` → `<model>.edits.own2usr_x1`):
  - Qwen3-8B belief: **+0.043** (p 5e-05; raw +0.020).
  - Qwen3-1.7B attribution: P(own letter) **−0.040** and P(user letter) **+0.045** (both p ≤ 0.0001).
- At ×2 the effects reach:
  - Qwen3-8B belief **+0.093** and obey **+0.062**;
  - Qwen3-1.7B: user→own belief −0.065, own→user P(own letter) −0.070;
  - OLMo belief −0.049 and −0.051.
- The paper's own exploratory number ("22% of the own–user gap at ×2" in Qwen3-8B) equals **0.062**, which also exceeds 0.03.
- **Suggested wording:** "All effects of the sealed user→own edit at ×1 were ≤ 0.03 (largest: Qwen3-1.7B belief, −0.028), against best-to-worst source gaps of 0.07–0.46. The reverse own→user edit (exploratory) moved more: up to 0.04 at ×1 and 0.09 at ×2."

**M3. §2: "Items, names and seeds are fresh in every sealed test" [factual, names].**
- Seeds are fresh (2100 / 2200 / 2300 in `cloud/rc25–27.sh`), and items are new draws. **Names are not fresh.**
- `code/src_monitor.py` builds every name as two syllables from a fixed list of 24 (`SYL`), so there are only **576 possible names** (checked: all 576 strings are distinct).
- Each test's names are unique within that test:
  - PREREG_S: n = 60 → 120 items × 3 names = **360** distinct names;
  - PREREG_T and PREREG_U: n = 48 → 288 each.
- By pigeonhole, at least **72 names are shared between S and T**, and at least 72 between S and U (360 + 288 − 576). This bound does not depend on the tokenizer-dependent rejection step.
- A simulation of the generator's random draws (assuming no rejections; approximate, since `transformers`/`tokenizers` are not installed) gives about 176 names shared S–T, 180 S–U and 139 T–U.
- PREREG_V's amendment ("the item generator ran out of unique names at n = 96") is the same 576-name limit.
- **Suggested wording:** "Items and seeds are fresh in every sealed test. Names are drawn from one fixed pool of 576 made-up two-syllable names, so individual names recur across tests."

**M4. Data and code: "Analyses: `cloud_*_analysis/*.json`" [path].**
- There is no `cloud_prereg_s_analysis`, `cloud_prereg_t_analysis` or `cloud_prereg_u_analysis` folder. The S/T/U analyses are `RF/cloud_prereg_s/s_analysis.json` (with `s_jspace.json`), `RF/cloud_prereg_t/t_analysis.json` and `RF/cloud_prereg_u/u_analysis.json`.
- The `cloud_*_analysis/` folders exist only for V, W, X, V0 and V1.
- **Suggested wording:** "Analyses: `cloud_prereg_{s,t,u}/*_analysis.json` (and `cloud_prereg_s/s_jspace.json`) for PREREG_S–U; `cloud_*_analysis/*.json` for the later tests."

## Overstatements, with suggested wording

**O1. Abstract: "Obeying and believing rank the five sources differently (FRAGMENTED in the first four models)".**
- The overall verdict is FRAGMENTED, but only 3 of 4 models are FRAGMENTED; OLMo is PARTIAL.
- The parenthesis also ties the verdict to the ranking. The ranking part of rule (c) (τ ≤ 0.2) holds in only **2 of 4** models: Qwen3-8B and SmolLM3, both exactly at τ = 0.2. Qwen3-1.7B's FRAGMENTED comes from the edit verdict (NONE); its behaviour verdict is MIXED (τ 0.4).
- **Suggest:** "Obeying and believing rank the five sources differently in the first four models (Kendall τ 0.2–0.4; sealed verdict FRAGMENTED in 3 of 4, OLMo PARTIAL), and 8 of 9 further models are not unified either."

**O2. "attribute near chance (0.32 and 0.32; chance 0.20)" and "Source effects do not require reportable source knowledge" (§3.1); also §1 ("behaviour does not require reportable source knowledge") and §4 ("they can work without reportable source knowledge").**
- Mean attribution is clearly **above** chance: +0.12 in both models, per-item sign-flip p 5e-05 (`recompute_s.json` → `mean_attr_vs_chance`).
- It is also above the preregistered "poor attribution" cut-off of ≤ 0.3, so neither model met that branch of rule (c).
- Per source, attribution reaches 0.64 (OLMo, quoted page) and 0.63 (SmolLM3, tool). It is near chance only for some sources (OLMo: system 0.19, user 0.18, own 0.25; SmolLM3: user 0.12, own 0.18).
- The evidence is a dissociation across behaviours, measured by a single first-token letter probability. It is not a test of necessity.
- **Suggest (§3.1):** "Source effects occur even where the source is poorly reported. OLMo and SmolLM3 show reliable source effects (p < 0.001) while attributing poorly (mean 0.32 in both, chance 0.20; near chance for several sources, e.g. OLMo system 0.19, user 0.18, own 0.25)."
- **Suggest (§1):** "behaviour does not track reportable source knowledge".
- **Suggest (§4):** "and they can work where the source is poorly reported".

**O3. §1: "a transplanted mean 'tag' does not carry behaviour (§3.1)".**
- This holds for the sealed user→own edit at natural size: NONE in 3 of 4 models; OLMo PARTIAL, where obedience moved +0.004.
- §3.1 itself says "Our null is at natural size only".
- The exploratory reverse edit moves obedience in 3 models, and Qwen3-8B belief by +0.043 (×1) and +0.093 (×2) beyond random. That belief shift is not mentioned anywhere in the paper.
- **Suggest:** "a transplanted mean 'tag' at natural size does not carry behaviour in the sealed user→own test (§3.1)".

**O4. §3.1 EXPL: Qwen3-1.7B's "attribution moves away from 'own' under this edit (−0.04 at ×1, −0.07 at ×2) while its obedience barely moves".**
- The attribution numbers are beyond-random values; raw they are −0.034 and −0.061.
- On the same beyond-random basis, Qwen3-1.7B's obedience moves +0.012 (×1, p 5e-05) and +0.029 (×2, p 0.0006). That is 33% and 77% of its own–user obey gap (0.037), larger shares than the 22% highlighted for Qwen3-8B.
- The bullet just above lists Qwen3-1.7B among the models whose obedience *does* move. "Barely moves" holds only for the raw change (+0.001, p 0.70; +0.015, p 0.013).
- **Suggest:** "…attribution moves away from 'own' under this edit (−0.04 at ×1, −0.07 at ×2, beyond random), more than its obedience does in absolute terms (+0.01 and +0.03)."

**O5. §3.1: "The source is readable from the statement's own tokens at the decision layer: 0.87–0.94 in three models, and 0.69 in Qwen3-1.7B at layer 13 (0.91 at layer 18)".**
- The numbers are right. However, Qwen3-1.7B fails the preregistered READABLE rule (a), which needs ≥ 0.8 at the decision layer (`readable: false`, 0.685). Layer 18 is not the decision layer.
- **Suggest:** "The source is readable (rule (a), ≥ 0.8) at the decision layer in three models (0.87–0.94). Qwen3-1.7B misses it there (0.69 at layer 13; 0.91 at layer 18)."

**O6. §3.2 Design: "Only the role word differs, so the two prompts are token-aligned" and "Patching all positions reproduces the donor exactly (sanity check)". The Abstract's "token-aligned role-word minimal pairs" has the same issue.**
- This holds exactly in 7 of 8 model-pairs (maximum |ALL − donor| = 0.00000 on every prompt).
- In OLMo own→usr, all 192 behaviour and 192 attribution prompt pairs differ in length by one token: the assistant turn ends in EOS (`patch.json` → `pairs.own->usr.{beh,attr}.mismatch` = 192). The extra token is not patched.
- As a result, T_ALL for OLMo's informative own→usr belief curve is **1.097** at layer 1 and **1.075** at layer 10. It passes the preregistered [0.9, 1.1] band but is not exact. Single prompts differ by up to 0.23 at layer 1.
- PREREG_T discloses this; the paper does not.
- **Suggest:** "…token-aligned, except OLMo own→usr, where the assistant turn's end token adds one position (aligned segment by segment; that token is not patched). Patching all positions reproduces the donor exactly in 7 of 8 model-pairs and within 10% in OLMo own→usr."

**O7. §3.2 EXPL: "Attribution … never routes through the statement's own tokens: maximum C transfer is 0.02–0.24 in 6 of 6 curves".**
- A C transfer of 0.24 (Qwen3-8B own→usr, layer 15) and 0.16 (Qwen3-1.7B own→usr) is a quarter and a sixth of the attribution effect. That contradicts "never".
- §3.3 reports this claim as not replicated, but §3.2 still states it unqualified.
- **Suggest:** "Attribution reads the role marker mostly from the later positions and routes little through the statement's own tokens (maximum C transfer 0.02–0.24 in 6 of 6 curves; §3.3 finds content use in about half the new models)."

**O8. §3.2 EXPL: "This also explains PREREG_S's null. Its mean-vector edit acted at the decision layer, before the obey content phase, and at natural size."**
- The factual part is right: the S edit layers (13, 7, 17, 10) precede the obey C-transfer peaks (16; 15–17; 23).
- The causal claim is untested:
  - `src_monitor.py`'s hook adds the vector to the decision layer's *output*, so it stays in the residual stream through the content phase;
  - size and mean-versus-item code are not separated;
  - the account says nothing about the belief and attribution nulls.
- **Suggest:** "This may explain PREREG_S's null for obedience (untested): its mean-vector edit was added at the decision layer, before the obey content phase, and at natural size."

**O9. §3.4: "The splice did not lower obedience (Δ between −0.017 and +0.020)".**
- In Qwen3-8B the splice lowered obedience by 0.017 with p 0.001 (`u_analysis.json` → `models.Qwen3-8B.conditions.U*`). That is significant, though only a third of the preregistered −0.05.
- In SmolLM3 it *raised* obedience (+0.020, p 5e-05).
- **Suggest:** "The splice did not lower obedience by the preregistered 0.05 in any model (Δ between −0.017 and +0.020; Qwen3-8B's −0.017 was significant, p 0.001)."

**O10. §3.4: "so the splice had nothing protective to carry" and "Status of the capability criterion. No defence beat the baselines."**
- The sealed splice indeed never met H1. H4 held only in OLMo, where U* beat the defensive prompt on selectivity (CI of the difference [0.116, 0.220]) because the prompt cut belief by 0.152.
- PREREG_U's reported-only mean-vector conditions, which the paper lists only as "mean vectors", contradict "nothing protective". They add the framed − plain statement-token mean at the U* layer:
  - **M1** (×1) lowered obedience in both Qwen models (−0.022 and −0.020, p 5e-05).
  - **M4** (×4) lowered it by **−0.167** (Qwen3-1.7B) and **−0.113** (Qwen3-8B).
- Applying the sealed H1–H4 rules to M4 in Qwen3-1.7B gives **all four true, i.e. SELECTIVE_DEFENSE** (`SC/rerun/recompute_u.json`):
  - belief −0.069 (≤ half of 0.167);
  - selectivity +0.098, CI [0.036, 0.163];
  - beats framing, CI [0.038, 0.192];
  - beats the defensive prompt, CI [0.073, 0.239].
- In Qwen3-8B, M4 meets H1 only: |belief change| 0.069 is more than half of 0.113. In OLMo and SmolLM3 it does not help.
- This is exploratory, but it bears directly on §3.5, which then "finds" a scale-4 mean-difference vector on the statement tokens.
- **Suggest:** "The sealed splice did not beat the baselines. Exploratory: the reported-only 4× framed-minus-plain mean vector (M4) met all four sealed criteria in Qwen3-1.7B (obey −0.167, belief −0.069; selectivity +0.098 [0.036, 0.163], above framing and the defensive prompt) and cut obedience by 0.113 in Qwen3-8B without passing the half rule. It did not help in OLMo or SmolLM3." Also change "nothing protective to carry" to "nothing protective to carry at natural size".

**O11. §3.4 EXPL: "The splice is selective, but for belief."**
- This holds in **2 of 4** models: OLMo (+0.091 at layer 15, obey +0.004, p 0.11) and Qwen3-8B (+0.138 at layer 20, obey −0.000, p 0.94). Both are about half the framing's effect (0.51 and 0.50).
- Qwen3-1.7B: the splice lowers belief at mid layers (−0.02 to −0.036; maximum +0.013 at layer 3).
- SmolLM3: at its belief peak (layer 17, +0.028) obedience also rises +0.020 (p 5e-05), and the selectivity CI includes 0.
- **Suggest:** "In OLMo and Qwen3-8B the splice is selective, but for belief: … (not in Qwen3-1.7B or SmolLM3)."

**O12. Abstract: "This holds across 14 open models from 7 families, 0.6B to 32B" [cross-scope; rests partly on PREREG_W].**
- The bullet counts above it (92%, 9 of 10, 4 of 5) are for the 10 PREREG_W models and include exceptions.
- PREREG_T's four models add: 4 of 4 DISSOCIATED; 14 of 16 MARKER curves; obey after attribute in 3 of 3 comparable models.
- §1 ("The role-marker tokens carry the source") and §4 ("the common carrier") are consistent with the curve counts. PREREG_T's sealed H1, however, was MIXED (2 of 4 models all-MARKER).
- **Suggest:** "The map covers 14 open models from 7 families, 0.6B to 32B (the counts above are for the 10 replication models)." The PREREG_W checker should confirm the W part.

## Gate verdicts

Every verdict the paper reports for S, T and U follows from its sealed rule applied to the stored data. The re-runs are byte-identical. Per-model values are in the order OLMo-2-7B / Qwen3-1.7B / Qwen3-8B / SmolLM3-3B.

| Test / gate | Rule (sealed docstring) | Data | Verdict | Paper | Follows rule |
|---|---|---|---|---|---|
| S (a) READABLE | 5-way accuracy at decision layer ≥ 0.8 | OLMo 0.94 (L10), Q1.7 0.685 (L13), Q8 0.88 (L17), Smol 0.87 (L7) | T / **F** / T / T | "readable … 0.69 in Qwen3-1.7B" (see O5) | yes |
| S (c) behaviour | UNIFIED τ ≥ 0.6 and attr ≥ 0.6; FRAGMENTED τ ≤ 0.2 or attr ≤ 0.3; else MIXED | τ 0.4/0.4/0.2/0.2; mean attr 0.3245/0.7378/0.871/0.3221; all obey and believe informative (p 5e-05) | MIXED / MIXED / FRAGMENTED / FRAGMENTED | not stated per model | yes |
| S (d) edit (user→own ×1 vs random, Holm) | CAUSALLY_UNIFIED all / PARTIAL some / NONE | OLMo obey +0.0043 (Holm 0.0065, moved); others not moved or opposite | PARTIAL / NONE / NONE / NONE | "moved nothing … in three models; in OLMo only obedience" | yes |
| S headline | SOURCE_MONITOR / FRAGMENTED if (c) FRAG or (d) NONE / PARTIAL | — | PARTIAL / FRAG / FRAG / FRAG → **overall FRAGMENTED** (3 ≥ 3) | FRAGMENTED (3 of 4; OLMo PARTIAL) | yes |
| S (b) J-space, Qwen3-1.7B L13 | OUTSIDE if source ≤ 2 × floor | 0.0503 ≤ 0.0625 (content 0.1182) | **OUTSIDE** (stored; recomputed identically) | OUTSIDE | yes |
| T H1 | model MARKER if all informative obey/believe curves MARKER; majority 3 of 4 | OLMo {SHARED, MARKER}; Q1.7 all MARKER; Q8 {SHARED, MARKER}; Smol all MARKER | MIXED / MARKER / MIXED / MARKER → **overall MIXED** (2 < 3) | H1 MIXED, 2 of 4 | yes |
| T H2 | DISSOCIATED if carriers differ (M vs C) or handoffs ≥ 3 apart with CI excluding 0 | OLMo att−bel −6 [−6, −4]; Q1.7 att−obey −6 [−6, −4], bel−obey −5 [−5, −3] (own), −4 [−5, −3], −4 [−6, −3] (sys); Q8 att−obey −9 [−9, −6]; Smol att−obey −9 [−10, −9] | all DISSOCIATED → **overall DISSOCIATED** | DISSOCIATED 4/4 | yes |
| U per model | SELECTIVE_DEFENSE H1–H4; SELECTIVE H1+H2; else NONE | U* d_obey +0.0032 / −0.0106 / −0.0167 / +0.0196 (H1 false everywhere) | NONE ×4 → **overall NONE** | NONE in all four | yes |

**Fragility notes (no verdict change).**
- Both rule-(c) FRAGMENTED verdicts (Qwen3-8B and SmolLM3) sit exactly on τ = 0.2.
- An item bootstrap (2,000 resamples, seed 0) gives P(τ ≤ 0.2) = 0.73 for Qwen3-8B and 0.25 for SmolLM3. SmolLM3's 95% interval is [0.2, 0.8], with P(τ ≥ 0.6) = 0.29.
- SmolLM3's discordant pairs rest on source differences of 0.002–0.03. Qwen3-8B's usr–doc reversal rests on a belief difference of 0.008.
- The overall FRAGMENTED verdict does not depend on τ: all three FRAGMENTED headlines are also reached through (d) NONE.

## Other notes (no status change)

- **N1. Incomplete §3.1 list of opposite moves.** "Belief moved slightly the opposite way in Qwen3-1.7B and OLMo" is correct (−0.028 and −0.024; Holm 0.00015). Two more sealed tests moved significantly the opposite way: Qwen3-1.7B obedience −0.005 (Holm 0.0003) and OLMo attribution −0.004 (Holm 0.00015).
- **N2. J-lens provenance.**
  - The J-lens file (`n_prompts` 466, Salesforce-wikitext) in `C:/Users/caabm/Documents/Codex/2026-09-06/co/work/` is byte-identical (sha256 `6fcc7901…`) to the Hugging Face cache copy of `neuronpedia/jacobian-lens` (`qwen3-1.7b/jlens/Salesforce-wikitext`). PREREG_S calls it "the user's September WikiText J-lens fit"; it appears to be the published neuronpedia fit. The paper's "the September WikiText J-lens fit" is accurate as worded.
  - The file is an input that is not listed in `PREREG_S.sha256`.
- **N3. Possible J-lens layer offset.**
  - The J-lens has keys 0–26 for a 28-block model, which suggests 0-indexed block outputs. `reps.pt` layer 13 is the output of block 13 (1-indexed), so `s_jspace.py` may pair it with the next block's Jacobian.
  - The verdict is robust: with J[12], J[13] or J[14] the layer-13 source fraction is 0.0498 / 0.0503 / 0.0389, all OUTSIDE. Layer 22 stays source > content under every offset.
- **N4. J-lens token readings.** The five genre mappings ("user → question marks", …) match `s_jspace.json` → `layers.13.jlens_reading`. They were not recomputed, because they need W_U from the model weights.
- **N5. Units of "+0.69 to +0.91 over belief" (§3.2).**
  - These are differences in transfer, as fractions of each behaviour's own gap (T_C obey − T_C believe at layer 16: own→usr 1.220 − 0.313 = 0.907; sys→usr 1.092 − 0.401 = 0.691). They are not probability changes.
  - In probability units, the C patch at layer 16 moves obedience 0.114 and 0.225, against belief 0.062 and 0.066.
  - Within the own→usr window the difference falls to 0.19 at layer 18.
- **N6. Items can differ between models within one test.** `make_items` draws from one random stream and rejects candidates whose two answers share a first token *under each model's tokenizer*. After the first model-specific rejection, the item lists diverge. This could not be checked, because `transformers` and `tokenizers` are not installed. The paper does not claim identical items across models.
- **N7. Wording, minor.**
  - §6 "fictional facts and passwords": the instructions use three templates (password, code word, project name).
  - "read at the first answer word": the readout is the first answer *token*.
  - §2's example "Velmora" cannot be produced by the generator (two syllables, e.g. "Velmor"); "Tancab" can.
- **N8. Reported-only PREREG_U results that the paper omits.**
  - P's cost on user-turn obedience is not significant in any model (OLMo +0.009, Qwen3-1.7B +0.038, Qwen3-8B +0.026, SmolLM3 +0.004; p ≥ 0.064).
  - M1 and M4: see O10.
- **N9. Timing of "sealed before data."** File times are consistent with sealing before data. They are the only evidence available locally (seal file times against tar member times from the pod):
  - S: sealed 15:59:50, first output 16:00:44;
  - T: sealed 16:35:36, first output 16:39:43;
  - U: sealed 17:26:46, first output 17:27:48.
- **N10. Bundle layout.**
  - In `agp21–23` the run scripts are stored as `code/rc2x.sh` and `code/ss2x.sh` (the seal lists `cloud/…`). Their hashes match the seal entries.
  - Each bundle also carries an unsealed `code/agp.py`, which no S/T/U code imports.
- **N11. Model revisions.** `rc25–27.sh` download models by name, without a revision pin. `transformers==5.16.1` is pinned.

## Re-run log

**Environment.** Python 3.12.10, numpy 2.5.3, torch 2.14.1+cpu (no CUDA). `CUDA_VISIBLE_DEVICES=""` and `AGP_DEVICE=cpu`. No network, GPU or installs.
- `transformers` and `tokenizers` are **not installed**. They are needed only by the unrun model-side scripts and for regenerating item lists; they were not installed.
- A first attempt with `python -I` failed with `No module named 'numpy'`, because numpy lives in the user site-packages, which `-I` disables. All runs used `python -E -P` instead.

**Seals.** In `RF/`, and again in `SC/`:
- `sha256sum -c PREREG_S.sha256`: 9/9 OK.
- `sha256sum -c PREREG_T.sha256`: 9/9 OK.
- `sha256sum -c PREREG_U.sha256`: 10/10 OK.

**Raw data integrity.**
- `results25.tgz`: 12 files (behaviour, edits and reps × 4 models).
- `results26.tgz`: 4 `patch.json` files.
- `results27.tgz`: 4 `defense.json` files.
- All 20 were extracted in `SC/` and are byte-identical to `cloud_prereg_{s,t,u}/out_*`. Each `last_status.txt` shows `@@ERRS 0`.

**Bundles.** `RF/bundles/agp21.tgz`, `agp22.tgz` and `agp23.tgz` were extracted in `SC/`. All 9, 9 and 10 sealed files are present with matching sha256, and the bundled `.sha256` files are identical to the ones in `RF/`.

| Script (sealed) | Command (from `SC/`) | Result vs stored file |
|---|---|---|
| `s_analyze.py` | `python -E -P code/s_analyze.py --root cloud_prereg_s/out_s` | **Byte-identical** to `cloud_prereg_s/s_analysis.json` (sha256 `e26839ab…`). With `--jspace cloud_prereg_s/s_jspace.json`, the `models` block is identical and a `jspace` key is added; the stored file was made without `--jspace`. |
| `t_analyze.py` | `python -E -P code/t_analyze.py --root cloud_prereg_t/out_t` | **Byte-identical** to `cloud_prereg_t/t_analysis.json` (sha256 `42444571…`) |
| `u_analyze.py` | `python -E -P code/u_analyze.py --root cloud_prereg_u/out_u` | **Byte-identical** to `cloud_prereg_u/u_analysis.json` (sha256 `4639f653…`) |
| `s_jspace.py` | **Not run.** It calls `AutoModelForCausalLM.from_pretrained('Qwen/Qwen3-1.7B')` for W_U. | Replaced by `SC/recompute_jspace.py`, which loads `reps.pt` and the J-lens with `weights_only=True`, on CPU. Source, content, floor, the four pair fractions and the set-1 values are **identical** to `s_jspace.json` at layers 6, 10, 13, 14, 18 and 22; the verdict is OUTSIDE. The token readings were not recomputed. |
| Recomputations | `SC/recompute_s.py`, `recompute_t.py` and `recompute_u.py` on the `out_*` folders | Edits in both directions and at both scales, attribution against chance, curve counts, ALL checks, U-layer derivation, M1/M4 under H1–H4 and the U sweep. Outputs are in `SC/rerun/`. Every condition the sealed script also computes (F, P, M1, M4, U*) matches the stored values exactly. |

---

## Claim table

### Abstract

| # | Location / claim (quoted) | Paper | Found | Source | Status |
|---|---|---|---|---|---|
| A1 | "Obeying and believing rank the five sources differently" | — | Kendall τ 0.4 / 0.4 / 0.2 / 0.2 (OLMo, Q1.7, Q8, Smol), all < 1 | `s_analysis.json` `models.*.kendall_tau` | MATCH |
| A2 | "(FRAGMENTED in the first four models)" | FRAGMENTED | Overall FRAGMENTED; per model 3 FRAGMENTED + OLMo PARTIAL; rule-(c) FRAGMENTED in 2 of 4 | `s_analysis.json` `overall`, `headline`, `behaviour_verdict` | MATCH · **O1** |
| A3 | "Activation patching between token-aligned role-word minimal pairs" | — | Aligned in 7 of 8 model-pairs; OLMo own→usr off by 1 token in 384/384 prompts | `patch.json` `mismatch` | MATCH · **O6** |
| A4 | "This holds across 14 open models from 7 families, 0.6B to 32B" (T part) | — | T: 4/4 DISSOCIATED; 14/16 MARKER curves; obey after attribute in 3/3 comparable | `t_analysis.json` | MATCH (T part) · **O12** |
| A5 | "All confirmatory claims are preregistered and hash-sealed" (S/T/U) | — | 3 seals, 28/28 OK; bundles match | `PREREG_{S,T,U}.sha256`, `bundles/agp21–23` | MATCH |

### §1

| # | Location / claim (quoted) | Paper | Found | Source | Status |
|---|---|---|---|---|---|
| I1 | "Obeying and believing rank sources differently" | — | τ 0.2–0.4 | `s_analysis.json` | MATCH |
| I2 | "behaviour does not require reportable source knowledge" | — | Source effects p 5e-05 with mean attribution 0.32 (OLMo, Smol); attribution above chance (p 5e-05) | `s_analysis.json`; `recompute_s.json` | MATCH · **O2** |
| I3 | "a transplanted mean 'tag' does not carry behaviour" | — | Sealed user→own ×1: NONE ×3, PARTIAL (OLMo); reverse arm moves obedience in 3 models and Q8 belief +0.043/+0.093 | `s_analysis.json`; `recompute_s.json` | MATCH · **O3** |
| I4 | "The role-marker tokens carry the source, and behaviours read it at different depths" (T part) | — | 14/16 curves MARKER (sealed H1 MIXED); H2 DISSOCIATED 4/4 | `t_analysis.json` | MATCH · note in O12 |

### §2 Setup

| # | Location / claim (quoted) | Paper | Found | Source | Status |
|---|---|---|---|---|---|
| S1 | Fixed system prompt "You are a helpful assistant."; five sources; page and tool wrappers | — | `BASE_SYS`; `wrap()`: 'Here is an excerpt from a web page:\n"…"', 'Tool output:\n…' | `code/src_monitor.py` | MATCH |
| S2 | Fact/instruction examples; "Each competes with a user message giving a different answer, in both orders. A final user question asks for the answer." | — | `FACTS`/`INSTR` templates; `contexts()` orders 0/1; question appended | `code/src_monitor.py` | MATCH (N7: "Velmora" is illustrative) |
| S3 | "Items, names and seeds are fresh in every sealed test." | fresh | Seeds 2100/2200/2300 fresh; names from a 576-name pool, ≥ 72 shared S–T and S–U | `code/src_monitor.py` `SYL`, `make_items`; `cloud/rc25–27.sh` | **MISMATCH (M3)** |
| S4 | Obey/believe readout = P(answer) / P(both answers) at first answer token; attribute = P(correct letter) of five | — | `score = pa/(pa+pb)`; `attr = pl[letter]/pl.sum()` | `src_monitor.py`, `src_patch.py`, `src_defense.py` | MATCH |
| S5 | "run in bf16 with Hugging Face Transformers" (S/T/U) | bf16 | `DTYPE = bfloat16` unless CPU; `transformers==5.16.1` | `code/agp_batch.py`; `cloud/rc25–27.sh` | MATCH |
| S6 | "written with its analysis code before data and sealed by SHA-256 hashes of every file it used. It was bundled…" (S/T/U) | — | Seals OK; bundles match; seal precedes first output by 54 s / 4 min / 62 s; J-lens input not in the seal (N2) | seals; `bundles/`; tar member times | MATCH |

### §3.1 PREREG_S

| # | Location / claim (quoted) | Paper | Found | Source | Status |
|---|---|---|---|---|---|
| R1 | Items: "60 fictional facts and 60 fictional instructions … in both orders" | 60 + 60 | 60 `obey*` + 60 `believe*` ids; 1,200 rows/model (120 × 5 sources × 2 orders) | `out_s/*/behaviour.json` | MATCH |
| R2 | Source readout: five-way nearest centroid, "fresh set of 40 neutral sentences" | 40 | `NEUTRAL2` (40), leave-one-sentence-out; `probe_acc` = set 2 | `src_monitor.py`; `behaviour.json` | MATCH |
| R3 | Edit: "user↔own tag transplant at the decision layer, with same-norm random controls" | — | `usr2own`/`own2usr` × {1, 2}; random rescaled to ‖c_own − c_usr‖ | `src_monitor.py`; `edits.json` | MATCH |
| R4 | Models Qwen3-1.7B, SmolLM3-3B, Qwen3-8B, OLMo-2-7B-Instruct | — | Same, layers 13/7/17/10 | `cloud/rc25.sh`; `behaviour.json` `model`, `layer` | MATCH |
| R5 | Rule: majority; readable; τ ≥ 0.6; attribution ≥ 0.6; edit as predicted | — | Same as sealed docstring | `code/s_analyze.py` | MATCH |
| R6 | "Result: FRAGMENTED (3 of 4 models; OLMo PARTIAL)" | 3/4 | FRAGMENTED; OLMo PARTIAL | `s_analysis.json` `overall`, `headline` | MATCH |
| R7 | "rank the five sources differently in every model (τ = 0.2–0.4)" | 0.2–0.4 | 0.4, 0.4, 0.2, 0.2 | `kendall_tau` | MATCH (fragility note) |
| R8 | Qwen3-8B "obeys the user most (0.53)" | 0.53 | 0.5343 (max of 5) | `authority.obey.usr` | MATCH |
| R9 | "and its own earlier turn least (0.25)" | 0.25 | 0.2474 (min) | `authority.obey.own` | MATCH |
| R10 | "but believes the system most (0.75)" | 0.75 | 0.7477 (max) | `authority.believe.sys` | MATCH |
| R11 | "It believes tool output (0.67)" | 0.67 | 0.66499 (stored 0.665) | `authority.believe.tool`; recompute | ROUNDING |
| R12 | "while obeying it less (0.42)" | 0.42 | 0.4181 | `authority.obey.tool` | MATCH |
| R13 | "Qwen3-1.7B obeys tool output more than the user (0.71 vs 0.51)" | 0.71 / 0.51 | 0.7062 / 0.5132 | `authority.obey` | MATCH |
| R14 | "OLMo and SmolLM3 show reliable source effects (p < 0.001)" | p < 0.001 | obey and believe best–worst p 5e-05 in both | `obey_range`, `believe_range` | MATCH |
| R15 | "yet attribute near chance (0.32 and 0.32; chance 0.20)" | 0.32 / 0.32 | 0.3245 / 0.3221; +0.12 above chance, p 5e-05 | `mean_attribution`; `recompute_s.json` | MATCH · **O2** |
| R16 | "Qwen3-8B attributes well (0.87)" | 0.87 | 0.871 | `mean_attribution` | MATCH |
| R17 | "readable … at the decision layer: 0.87–0.94 in three models" | 0.87–0.94 | Smol 0.87 (L7), Q8 0.88 (L17), OLMo 0.94 (L10) | `probe_acc` | MATCH |
| R18 | "0.69 in Qwen3-1.7B at layer 13" | 0.69 | 0.685 (= 137/200); `readable: false` | `probe_acc.13` | MATCH · **O5** |
| R19 | "(0.91 at layer 18)" | 0.91 | 0.905 (= 181/200) | `probe_acc.18` | MATCH |
| R20 | "At natural size (×1) the edit moved nothing as predicted in three models" | 3 | Q1.7, Q8, Smol: no test `moved` | `edit_tests` | MATCH |
| R21 | "In OLMo only obedience moved (+0.004)" | +0.004 | +0.00433, Holm p 0.0065 | `edit_tests.obey` | MATCH |
| R22 | "Belief moved slightly the opposite way in Qwen3-1.7B and OLMo" | — | −0.0275 / −0.0236, Holm 0.00015 | `edit_tests.believe` | MATCH (N1: incomplete) |
| R23 | "All edit effects were ≤ 0.03" | ≤ 0.03 | Sealed user→own ×1 max 0.0275; own→user ×1 up to 0.043 (Q8 belief), 0.045 (Q1.7 attribution); ×2 up to 0.093 | `edit_tests`; `recompute_s.json` | **MISMATCH (M2)** |
| R24 | "against best-to-worst source gaps of 0.07–0.46" | 0.07–0.46 | 0.0729–0.4602 | `obey_range`/`believe_range.mean` | MATCH |
| R25 | J-space verdict at layer 13: "OUTSIDE" | OUTSIDE | OUTSIDE (0.0503 ≤ 2 × 0.0312) | `s_jspace.json`; recomputed | MATCH |
| R26 | "The fraction is 0.050 against a random floor of 0.031; the sentence-content variation is 0.118" | 0.050 / 0.031 / 0.118 | 0.0503 / 0.0312 / 0.1182 | `s_jspace.json` `layers.13`; recomputed | MATCH |
| R27 | "with the September WikiText J-lens fit; proxy = top 64 right singular vectors of J_l" | 64 | K = 64; J-lens `n_prompts` 466, Salesforce-wikitext | `s_jspace.py`; J-lens metadata | MATCH (N2, N3) |
| R28 | EXPL "At layer 22 the source fraction is 0.127 against content 0.037" | 0.127 / 0.037 | 0.1273 / 0.0371 | `s_jspace.json` `layers.22`; recomputed | MATCH |
| R29 | EXPL J-lens readings at layer 13 (user → question marks; page → closing quotes; tool → code punctuation; own → end-of-text and ellipses; system → line breaks and colons) | — | Top-8 tokens agree with each label | `s_jspace.json` `layers.13.jlens_reading` | MATCH (stored only; needs W_U, N4) |
| R30 | EXPL "The reverse transplant (own→user) does move obedience a little, in Qwen3-1.7B, Qwen3-8B and OLMo" | 3 models | Beyond random ×1: +0.012, +0.027, +0.012 (all p 5e-05); SmolLM3 −0.003 (p 0.12) | `recompute_s.json` `own2usr_x1.obey` | MATCH |
| R31 | EXPL "In Qwen3-8B this is 22% of the own–user gap at ×2" | 22% | 0.0618 / 0.2869 = 0.216 (beyond random; raw 0.117) | `recompute_s.json` `own2usr_x2.obey` | MATCH |
| R32 | EXPL Qwen3-1.7B attribution "−0.04 at ×1, −0.07 at ×2" | −0.04 / −0.07 | P(own letter): −0.0404 / −0.0699 beyond random (raw −0.034 / −0.061) | `recompute_s.json` `P_true_letter` | MATCH |
| R33 | EXPL "while its obedience barely moves" | — | Beyond random +0.012 (p 5e-05) / +0.029 (p 0.0006) = 33% / 77% of gap; raw +0.001 / +0.015 | `recompute_s.json` | MATCH (raw) · **O4** |
| R34 | Reading: "Some models already believe tool output while obeying it less" | — | Q8 0.665 vs 0.418; OLMo 0.566 vs 0.504 (not Q1.7, Smol) | `authority` | MATCH |
| R35 | "Our null is at natural size only" | — | Scales ×1 and ×2 only | `edits.json` keys | MATCH |
| R36 | "Limits: four models, 1.7B–8B; … one edit layer per model" | — | Yes | `rc25.sh` | MATCH |

### §3.2 PREREG_T

| # | Location / claim (quoted) | Paper | Found | Source | Status |
|---|---|---|---|---|---|
| T1 | Question: "PREREG_S showed that the readable source tag … barely moves behaviour when transplanted as a mean vector" | — | Sealed edit ≤ 0.028 | `s_analysis.json` | MATCH |
| T2 | "Only the role word differs, so the two prompts are token-aligned" | — | 0 mismatches in 7 model-pairs; OLMo own→usr 192 + 192 prompts off by 1 token (EOS) | `patch.json` `mismatch` | MATCH (7/8) · **O6** |
| T3 | M / C / D position sets; "Every layer is patched, separately for obey, believe and attribute" | — | `patched.{M,C,D}` × all layers × {beh, attr} | `src_patch.py`; `patch.json` | MATCH |
| T4 | "Same four models; fresh items" | — | Seed 2200, 48 + 48 items | `patch.json` `seed`, `items` | MATCH (names: M3) |
| T5 | Handoff = first layer with T_D ≥ 0.5 | — | As in `summarize()` | `t_analyze.py` | MATCH |
| T6 | "Patching all positions reproduces the donor exactly (sanity check)" | exactly | Exact in 7/8 model-pairs; OLMo own→usr believe T_ALL 1.097 (L1), 1.075 (L10) | `t_analysis.json` `all_check`; `recompute_t.json` | MATCH (7/8) · **O6** |
| T7 | "H2, DISSOCIATED in 4/4 models" | 4/4 | All 4 DISSOCIATED (timing) | `per_model.*.H2` | MATCH |
| T8 | "Obeying is read 4–9 layers after attributing or believing" | 4–9 | Q1.7 4–6; Q8 9; Smol 9 | `handoff` | MATCH |
| T9 | "Qwen3-1.7B: obey L18–19, believe L14, attribute L13–14" | — | obey 19/18, believe 14/14, attribute 13/14 (own/sys) | `handoff` | MATCH |
| T10 | "Qwen3-8B: obey L25, attribute L16" | — | own→usr 25 / 16 | `handoff` | MATCH |
| T11 | "SmolLM3: obey L21, attribute L12" | — | sys→usr 21 / 12 (own→usr obey 20) | `handoff` | MATCH |
| T12 | "OLMo, which has no informative obey gap, attributes at L10 and believes at L16" | — | Obey gaps −0.006 (p 0.62) and +0.041 (p 0.0001, below the 0.05 size threshold); sys→usr attribute 10, believe 16 (own→usr believe 15) | `t_analysis.json` | MATCH |
| T13 | "Bootstrap CIs of the differences exclude 0" | — | [−6, −4], [−6, −4], [−5, −3], [−5, −3], [−6, −3], [−9, −6], [−10, −9] | `comparisons.*.ci95` | MATCH |
| T14 | "H1, MIXED" | MIXED | MIXED | `overall_H1` | MATCH |
| T15 | "main carrier in 11 of 13 informative curves" | 11/13 | 14/16 (8/10 obey/believe) | `carrier`, `informative` | **MISMATCH (M1)** |
| T16 | "Two curves share the carrier … and none is content-only" | 2 / 0 | 2 SHARED (Q8 own obey; OLMo own believe); 0 CONTENT | `carrier` | MATCH |
| T17 | "The preregistered majority (3 of 4 models all-MARKER) was missed: 2 of 4" | 2/4 | Q1.7, Smol MARKER | `per_model.*.H1` | MATCH |
| T18 | EXPL Attribution "never routes through the statement's own tokens: maximum C transfer is 0.02–0.24 in 6 of 6 curves" | 0.02–0.24 | 0.022–0.243 over 6 informative attribution curves | `curves.C` max | MATCH · **O7** |
| T19 | EXPL obey "maximum C transfer 0.38–1.33" | 0.38–1.33 | 0.379–1.332 (5 obey curves; peaks L15–L23) | `curves.C` | MATCH |
| T20 | EXPL "In Qwen3-1.7B (layer 16) and Qwen3-8B (layer 23), patching only the statement's tokens carries the full obey effect" | ≥ 1 | T_C 1.220 / 1.092 at L16; 1.332 at L23 | `curves.C` | MATCH |
| T21 | EXPL "This also explains PREREG_S's null … at the decision layer, before the obey content phase" | — | S layers 13/7/17/10 precede obey C peaks 16/15–17/23; the S vector persists in the residual stream | `rc25.sh`; `curves.C`; `src_monitor.py` Hook | MATCH (fact) · **O8** |
| T22 | EXPL "(Qwen3-1.7B layer 16: +0.69 to +0.91 over belief)" | 0.69–0.91 | T_C obey − T_C believe = 0.691 (sys), 0.907 (own) | `recompute_t.json` | MATCH (N5: units) |
| T23 | Figures `prereg_t_sys_to_usr.png`, `prereg_t_own_to_usr.png` | — | Both exist | `RF/figures/` | MATCH |

### §3.4 PREREG_U

| # | Location / claim (quoted) | Paper | Found | Source | Status |
|---|---|---|---|---|---|
| U1 | Statements as tool output against a competing user message; framing "quoted data, not instructions for you" | — | `SM.wrap('tool')`; `FRAME`; both orders | `src_defense.py`; `defense.json` `frame` | MATCH |
| U2 | Splice "after one layer: the PREREG_T obey content-phase layer, fixed before data" | — | Layers 16/17/23/18. They reproduce from PREREG_T's averaged obey C curves (Q1.7 L16, Smol L17, Q8 L23; OLMo 0.5608 × 32 → 18). Sealed 17:26:46, before the first U output at 17:27:48. Content-token mismatches 0. | `rc27.sh`; `recompute_t.json`; `defense.json` | MATCH |
| U3 | "Comparisons: the framing in the input, a defensive system prompt, and mean vectors" | — | F, P, M1, M4 (also usr/usr_P) | `defense.json` `res` | MATCH |
| U4 | "Result: NONE in all four models" | NONE ×4 | NONE ×4; overall NONE | `u_analysis.json` | MATCH |
| U5 | "The splice did not lower obedience (Δ between −0.017 and +0.020)" | −0.017 to +0.020 | U* d_obey −0.0167 (p 0.001), −0.0106, +0.0032, +0.0196 | `conditions.U*` | MATCH · **O9** |
| U6 | "The framing itself did not lower obedience in any model" | 0 of 4 | F d_obey +0.0082, +0.0281, +0.1538, +0.0488 | `conditions.F` | MATCH |
| U7 | "so the splice had nothing protective to carry" | — | Framed − plain mean vector lowers obedience in both Qwen models (M1 −0.02; M4 −0.167 / −0.113) | `conditions.M1/M4` | MATCH (premise) · **O10** |
| U8 | "Qwen3-8B followed the tool instruction more (+0.15, p < 0.001)" | +0.15 | +0.1538, p 5e-05 | `Qwen3-8B.conditions.F` | MATCH |
| U9 | "the framing raised belief in the tool's facts in OLMo (+0.18) and Qwen3-8B (+0.28)" | +0.18 / +0.28 | +0.1763 / +0.2790 | `conditions.F.d_bel` | MATCH |
| U10 | EXPL "raises belief … by about half the framing's effect (OLMo +0.09 at layer 15; Qwen3-8B +0.14 at layer 20) with obedience flat" | +0.09 / +0.14 | +0.0906 (obey +0.004, p 0.11) / +0.1383 (obey −0.000, p 0.94); ratios 0.51 / 0.50 | `U_sweep`; `recompute_u.json` | MATCH · **O11** |
| U11 | EXPL "This fits PREREG_T, where believing's content phase is mid-depth" | — | Believe C peaks: OLMo L13–14 /32, Q8 L16 /36, Q1.7 L11–16 /28 (0.39–0.57 depth) | `t_analysis.json` `curves.C` | MATCH |
| U12 | EXPL defensive prompt "raised tool-instruction following in both Qwen models (+0.085, p 0.004; +0.045, p 0.02)" | — | +0.0851, p 0.0036; +0.0450, p 0.02005 | `conditions.P` | MATCH |
| U13 | "No defence beat the baselines" | — | Sealed splice: H3 false ×4; H4 true only in OLMo (H1/H2 false). Reported-only M4 meets H1–H4 in Qwen3-1.7B | `u_analysis.json`; `recompute_u.json` | MATCH (sealed splice) · **O10** |

### §4 Discussion

| # | Location / claim (quoted) | Paper | Found | Source | Status |
|---|---|---|---|---|---|
| D1 | "Behaviours … disagree about which sources matter most" | — | τ 0.2–0.4; attribution ranks the sources differently again | `s_analysis.json` | MATCH |
| D2 | "They read the source at different depths" | — | H2 DISSOCIATED 4/4 | `t_analysis.json` | MATCH |
| D3 | "and they can work without reportable source knowledge" | — | As R15 | `s_analysis.json`; `recompute_s.json` | MATCH · **O2** |
| D4 | "The role-marker tokens are the common carrier, but each behaviour consults them differently" | — | 14/16 MARKER curves (sealed H1 MIXED); handoffs differ by 4–9 layers | `t_analysis.json` | MATCH · note in O12 |

### §6 Limitations

| # | Location / claim (quoted) | Paper | Found | Source | Status |
|---|---|---|---|---|---|
| L1 | "fictional facts and passwords competing with one user message, read at the first answer word" | — | Three instruction templates (password, code word, project name); first answer token | `src_monitor.py` | MATCH (N7) |

### Data and code, and line 9

| # | Location / claim (quoted) | Paper | Found | Source | Status |
|---|---|---|---|---|---|
| C1 | "Each sealed test lists its files in its `.sha256` and has an archived bundle" (S/T/U) | — | Yes | `RF/PREREG_*.sha256`, `bundles/` | MATCH |
| C2 | Table: PREREG_S 9 / `agp21`; PREREG_T 9 / `agp22`; PREREG_U 10 / `agp23` | 9 / 9 / 10 | 9 / 9 / 10 entries; bundles contain them with matching hashes | seals; `bundles/agp21–23.tgz` | MATCH (N10) |
| C3 | "Analyses: `cloud_*_analysis/*.json`" | — | S/T/U analyses are in `cloud_prereg_{s,t,u}/`; no `*_analysis` folders for them | `RF/` listing | **MISMATCH (M4)** |
| C4 | "Raw outputs: the `cloud_prereg_*` … folders" | — | `cloud_prereg_{s,t,u}/out_*` plus pod archives | `RF/` | MATCH |
| C5 | Line 9 / AI-use: "§3.1, §3.2 and §3.4 are being rechecked" | — | This recheck | — | MATCH |
