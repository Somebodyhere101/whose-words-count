# Paper B pre-publication fixes: change log (2026-10-29)

File changed: `RF\PAPER_B_SOURCE_MONITORING.md` only.
- md5: 869edac630cca1bd0be612973d372360 originally (backup: `scratchpad\PAPER_B_before_fixes_869edac6.md`); 5e883b93201d0bdac0faad6f934b5ad6 after round 1 (backup: `scratchpad\PAPER_B_after_round1_5e883b93.md`); ad084b8be10383d8908a71f868068df7 after round 2.
- CRLF kept: 564 CRLF, 0 bare LF, no double blank lines.
- Method: guarded scripts in the scratchpad. Each asserts exactly one match per replacement and an unchanged md5 before writing.
  - Round 1: `fix_paper_b.py` (67 replacements) and `fix_paper_b_2.py` (3).
  - Round 2: `fix_paper_b_3.py` (40) and `fix_paper_b_4.py` (5).
- After the network interruption, the file was re-read and its md5 confirmed as the round-1 state before round 2 was written. Nothing from round 2 had been applied.
- Coordinator-owned text is byte-identical to the original after both rounds: the title line, author line, Preprint/DOI paragraph, "Numbers come from ..." sentence, Compute paragraph and AI-use statement.
- Every reference entry is cited, and every citation has an entry. All tables have consistent column counts.

Abbreviations: XA = `cloud_prereg_x_analysis/x_analysis.json`; YA = `cloud_prereg_y_analysis/y_analysis.json`; VA = `cloud_prereg_v_analysis/v_analysis.json`; WA = `cloud_prereg_w_analysis/w_analysis.json`; V0A = `cloud_v0_analysis/v0_analysis.json`; V1A = `cloud_v1_analysis/v1_analysis.json`; SA = `cloud_prereg_s/s_analysis.json`.

## Must-fix

- B-M1: LEFT TO COORDINATOR (front matter L3/L9 and the Compute sentence). The "cite Paper A formally" part is done under B-S29. Note for the coordinator: §3.8 was rechecked (`NUMBERS_RECHECK_Y.md`: 87 claims, `y_analyze.py` re-run byte-identical, no verdict change).
- B-M2: FIXED. §1 contributions now say one exploratory claim (attribution never uses the statement's tokens) was refuted and the obey-later lag holds in a bare majority (4 of 7 with a comparable pair). Source: WA counts W3 "4/7", W5 attr_no_content "4/9", W5 NOT_SUPPORTED.
- B-M3: FIXED. §5 lever bullet: effective in 6 of 6 (both held-out families), selective in 5 of 6 (one held-out family, Granite); benchmark sub-bullet replaced with the review's wording, plus "on both benchmarks" at 14B. Sources: CONSOLIDATED PREREG_V table (from `v_analysis.json`); YA via NUMBERS_RECHECK_Y M1 (14B X2 and X4 true, X5 false; 32B X2 false).
- B-M4: FIXED. §3.1: Leong now "(2026, v2: source-format cues are decodable; its test for an abstract provenance code was inconclusive)" (REFERENCES_VERIFIED W5); Zeng 2025's finding stated precisely (REFERENCES_VERIFIED W8). §6: StruQ and SecAlign removed (no verified entry in REFERENCES_VERIFIED.md or PAPER_DRAFT.md); V-Steer named as Zeng et al. 2026 (PREREG_T.md "V-Steer (2607.26228, §4.3)", PREREG_U.md "V-Steer (Zeng et al. 2026)", REFERENCES_VERIFIED #1). The not-re-run list now names TrustAttention, DRIP, Semantic Overlays, V-Steer and CounterSteer (PLAN_BIGGER.md: DRIP and TrustAttention are trained, cited not re-run; CONSOLIDATED §6: Semantic Overlays trains adapters).
- B-M5: FIXED. §6 lists only Paper B's single-draw controls (PREREG_S edit, PILOT_V0, PREREG_V H4, PREREG_X/Y X5); PREREG_J, PREREG_K, role-steering contrasts and inj2 removed. RNDCTL is now "a 32-draw random-direction check in a related injection setup (Qwen3-4B, 4-bit; Paper A, §8)" with the "different setup, does not settle it" caveat. "Centre near zero" corrected to "mean shifts of −0.10 to +0.05, SDs 0.13–0.22" (RNDCTL_RESULTS.md: means +0.015/+0.051/−0.101, SD 0.219/0.132/0.195; NUMBERS_RECHECK_Y W2). The PILOT_V0 norm caveat is from `code/lever_pilot.py`.

## Should-fix

- B-S1: FIXED. Legend gains a "Pilot verdicts (FIRST_TOKEN_VALID, LEVER_FOUND)" line: rule written before data with provenance hashes, not sealed, exploratory (PILOT_V0.md, `*.sha256`).
- B-S2: LEFT TO COORDINATOR (front matter). The full recheck reports are `NUMBERS_RECHECK.md`, `NUMBERS_RECHECK_STU.md` and `NUMBERS_RECHECK_Y.md`.
- B-S3: FIXED in abstract and body ("Most models show no single ... tag"; §4 heading "In most models, ..."; §5 "... in most models"). Title left to coordinator. §3.3's list item kept because the list is introduced by "hold in most models".
- B-S4: FIXED. "or through different carriers" added in the abstract, §1, §4 and §5. §3.2 now states the sealed H2 rule (different carriers, or handoffs ≥ 3 layers apart with bootstrap CI excluding 0; PREREG_T.md).
- B-S5: FIXED. Abstract rewritten without Y1/Y2/PREREG_Y/SEP_EFFECTIVE/EFFECTIVE/NONE. SEP and InjecAgent glossed, the overall rule stated in words (PREREG_X.md: effective on both benchmarks and beats random, in 4 of 6; 2 of 6 met it, XA). Fragility note added (one item in 300, about half of reseeds: Paper B §3.8; NUMBERS_RECHECK_Y R1). "Beat all three prompt defences in none" per NUMBERS_RECHECK_Y W1.
- B-S6: FIXED. §1: "such as whether something was perceived or imagined, and who said it"; "whether to act on a text" presented as this paper's addition.
- B-S7: FIXED. §1: "On the public benchmarks it beats all baselines only in Qwen3-8B"; synthetic-item claims labelled as such. The follow-up count is now "4 are effective by the sealed rules and none beats all baselines". YA: 32B EFFECTIVE; Falcon3, Yi and OLMo-2-32B SEP_EFFECTIVE; 14B and OLMo-2-13B NONE.
- B-S8: FIXED. §3.7 gains an "Operational re-runs" bullet: Qwen3-8B (both benchmarks) and Granite's InjecAgent. Sources: crash logs `cloud_prereg_x/1b/out_x/log_x_{sep,ia}_Qwen3-8B_oom_attempt1.txt` and `cloud_prereg_x/2b/out_x/log_x_ia_granite-3.3-8b-instruct_oom_attempt1.txt`; PLAN_7DAY.md 2026-10-28 21:50 entry. §2 now points to §3.6 and §3.7.
- B-S9: LEFT TO COORDINATOR (Compute paragraph). See the decision note below.
- B-S10: FIXED. §3.1 J-space bullet now defines the J-lens/J-space proxy and states the rule. OUTSIDE if the source share is ≤ 2 × the random floor 64/2048 (0.0625); INSIDE if it is ≥ the content share; BETWEEN otherwise. "September" dropped; the fit is described as "fitted on 466 WikiText prompts". Sources: PREREG_S.md rule (b); `code/s_jspace.py` docstring; NUMBERS_RECHECK_STU.md N2. Values unchanged (0.050, 0.031, 0.118).
- B-S11: FIXED. All four process notes replaced with "To our knowledge, ..." (§3.1, §3.2, and two in §5).
- B-S12: FIXED. Both PREREG_T figures embedded as Figures 1 (`figures/prereg_t_sys_to_usr.png`) and 2 (`figures/prereg_t_own_to_usr.png`), each on its own line, with captions written from the PNGs. The captions give the 4 × 3 grid (models × obey/believe/attribute) and the M/C/D line styles. They also give transfer on the y-axis (cut at about −0.25 and 1.3), the handoff and decision-layer lines, and the per-panel labels. Results now cite "(Figures 1 and 2)".
- B-S13: FIXED. §3.3 list now comes first, then the Phi-4/Granite exceptions.
- B-S14: FIXED. The seven points are now identified as per-model-pair lags (own→user or system→user) at five Qwen3 sizes, with Spearman ρ = −0.54 against size (WA trend.Qwen3: 0.1429, 0.2143, 0.25, 0.25, 0.125, 0.175, 0.0938; spearman −0.536). "Smallest at 14–32B" corrected to "0.13–0.18 at 14B and 0.09 at 32B", because 14B's 0.175 exceeds 1.7B's 0.143 (WA; CONSOLIDATED agrees).
- B-S15: FIXED. §3.4 design defines selective and the half rule: |belief change| ≤ half |obedience change|, and the CI of selectivity above 0 (PREREG_U.md H2).
- B-S16: FIXED. §3.5: "behind §3.1, §3.2 and §3.4 ... in the four audited models. The ten further models of §3.3 were not audited." The same sentence is added to §6.
- B-S17: FIXED, except for the header. The LEVER_FOUND pass rule is stated (PILOT_V0.md stage 2: d_obey ≤ −0.10; d_bel ≥ −|d_obey|/2; decided-rate drop ≤ 0.10; pass in ≥ 2 of 4). OLMo is marked "fails: drop under 0.10" (V0A −0.0526). The random direction's pass in Qwen3-1.7B is reported (V0A random|0.45|4|C: d_obey −0.125, pass true). The header was NOT changed to "same norm": see the conflict note below. It was clarified to "own−tool's norm; same depth, scale and tokens", and one sentence was added: that norm is 4–22% larger than tool−user's at depth 0.45. Computed from `cloud_v0/out_v0/*/gen.json` norms: OLMo 2.4164/1.9784, Qwen3-1.7B 19.3785/17.6439, Qwen3-8B 10.2485/9.7077, SmolLM3 1.1716/1.1296.
- B-S18: FIXED. Labels are now defined in the design paragraphs:
  - §3.6: H1–H4, with SELECTIVE_DEFENSE/SELECTIVE/NONE and the 4-of-6 overall rule (PREREG_V.md).
  - §3.7: Net, attack success on valid replies, X1–X6, BEATS_BASELINES/EFFECTIVE/NONE, ADDITIVE and 4 of 6 (PREREG_X.md).
  - §3.8: the SCALES/PARTIAL/NONE and SEP_BEATS/SEP_EFFECTIVE/NONE ladders (PREREG_Y.md).
  - Also added: the PREREG_S FRAGMENTED/PARTIAL rule in §3.1 (PREREG_S.md), the PREREG_T H1/H2 rules in §3.2 (PREREG_T.md), and the PREREG_W majority/60% rule in §3.3 (PREREG_W.md).
- B-S19: FIXED. §3.6 reading: "in all six models of this test".
- B-S20: FIXED. The §3.7 table gains an "InjecAgent valid replies (of 300), none → steering" column, recounted from the raw `cloud_prereg_x/*/out_x/*/injecagent.json` files. The counts are 260→268, 81→93, 129→142, 115→131, 125→140 and 233→219; they match XA valid rates × 300. A note gives the paired n: 30 (Qwen3-1.7B) to 233 (Qwen3-8B), the XA X3 n. §3.8 adds 284→280 (14B) and 288→278 (32B) from `cloud_prereg_y_all/out_y/*/injecagent.json` (= NUMBERS_RECHECK_Y rows 15, 18). Precision note: the review's "about 30 replies" for Qwen3-1.7B is the paired n; its 56.8% → 3.2% rates rest on 81 and 93 valid replies.
- B-S21: FIXED. §3.8 cites "Paper A (Ramdan 2026, §8)" and gives the different-setup caveat (CONSOLIDATED PREREG_Y section). §5 no longer counts RNDCTL as "what we add"; it points to Paper A §8 and to this paper's single draws (§6).
- B-S22: FIXED. §4 notes that Phi-4's InjecAgent cut (21.5% → 11.0%) was matched by its single random draw (12.4%) (XA phi-4: ASR none 0.2146, DEF 0.1096, RND 0.1244; X5 false). §3.8 adds that in Phi-4 and Qwen3-14B the single random draw did as well (NUMBERS_RECHECK_Y O3).
- B-S23: FIXED. §4: "may be the better choice; we did not compare against them"; prompt defences "often do as well, and some backfire".
- B-S24: FIXED. §5: "Obeying and believing rank the sources differently (Kendall τ < 0.6) in 11 of the 13 models, from 7 families, in which both rankings are informative." Sources: SA τ 0.4/0.2/0.2/0.4; WA W4 τ for the 9 informative models (Falcon 0.4, OLMo-13B −0.2, Qwen3-0.6B −0.8, 14B 0.4, 32B 0.0, 4B 0.2, Yi 0.6, Granite 0.0, Phi-4 0.8; OLMo-32B UNINFORMATIVE). The §3.3 table now states the same τ < 0.6 criterion behind "7 of 9".
- B-S25: FIXED. §3.3 lists the four sanity exclusions. Source: WA sane=false, all informative, all own→user: OLMo-2-32B attribute, OLMo-2-13B obey, Yi obey and believe; the rule is PREREG_T.md (T_ALL in [0.9, 1.1]). §6 now says "four curves".
- B-S26: FIXED. Data and code now give https://github.com/Somebodyhere101/whose-words-count and the Zenodo `code-and-data.zip`. No claim was added about the repository's folder layout, which is not yet fixed (RELEASE_CHECKLIST.md).
- B-S27: LEFT TO COORDINATOR (AI-use statement).
- B-S28: LEFT TO COORDINATOR (AI-use statement). For reference, NUMBERS_RECHECK.md addendum: "about 193" checked; 177 MATCH, 6 MISMATCH, 1 UNVERIFIABLE, plus 8 overstatement flags.
- B-S29: FIXED. "G., A., and Lindsey, J. 2026" dropped. Paper A entry added exactly as given (alphabetical, after Penman). It is cited in the body as "Paper A (Ramdan 2026, §8)" in §3.8 and as "Paper A, §8" in §5 and §6. Every remaining reference entry is cited, and every citation has an entry (checked by script).

## Nice-to-have

- B-N1: FIXED. "same-norm" in the abstract.
- B-N2: FIXED. §3.1 no longer repeats the Johnson definition or §2's sources and readouts; it points to §1 and §2 and keeps the PREREG_S-specific item counts.
- B-N3: NO CHANGE NEEDED. 0.66 is correct: the unrounded value is 0.66499 (NUMBERS_RECHECK_STU R11; SA stores 0.665). CONSOLIDATED's 0.67 is the rounding slip.
- B-N4: FIXED. "will leave" → "may leave".
- B-N5: FIXED. "own→usr" → "own→user" in the text, and the pair notation is defined in §3.2. Figure file names are unchanged.
- B-N6: FIXED. The §3.3 table was moved out of the list item.
- B-N7: FIXED. "(§3.5 performs it)" added.
- B-N8: FIXED. Commas removed in "Zverev et al. 2025" and "Zhan et al. 2024"; "Johnson, Hashtroudi & Lindsay 1993" in §5; "C. T. Leong et al. 2025" in §5.
- B-N9: FIXED. The §3.7 table and stacking line now use one decimal, from XA: 30.0→13.7 (utility 64.7→67.7), 39.2→11.9; 28.3→5.7, 56.8→3.2; 41.7→24.7, 3.9→0.7; 44.7→35.7, 46.1→40.5; 56.0→44.0, 89.6→87.1; 24.3→22.3, 21.5→11.0, RND 12.4. Stacked on datamarking: 7.0, 4.7, 3.3, 24.0.
- B-N10: FIXED. Valid-reply rates are now made explicit:
  - about 30% on PILOT_V1's development cases (V1A no-defence V: OLMo 0.3167, Granite 0.300);
  - 38–42% on PREREG_X's test cases with no defence (XA: Granite 0.3833, OLMo 0.4167);
  - applied in §3.7, §4 and §6.
- B-N11: FIXED. "its attack success is 0.38 below the best prompt's at 1.7B and 0.06 below at 32B".
- B-N12: FIXED. "fitted on 40 neutral sentences, without injection data, though it was selected on synthetic injection items (PILOT_V0)"; "fitted without injection data".
- B-N13: FIXED. "§3.5–§3.8".
- B-N14: FIXED. "Korznikov, A., et al."; "pp." removed for Hines and Zhan; "G., A." gone with the dropped entry; also "Yu, Z., et al." (four authors), per REFERENCES_VERIFIED's convention of listing all authors only when there are three or fewer.
- B-N15: FIXED. All five double blank lines removed.
- B-N16: FIXED. RNDCTL (4-bit) is now attributed to Paper A, so §2's "all run in bf16" holds for this paper.

## Skim findings (round 2: `prepub_skim.md`, Paper B, B1–B15)

- B1: FIXED (coordinator decision 1). The title line is left to the coordinator.
  - "Map-guided", "located by the map" and "the map that located it" are removed from the abstract, §1, §3.6, §3.7 and §5. The abstract heading is now "A steering lever, found by search", and §1 Q3 now asks whether a selective lever is possible.
  - The lever is described as found by a pre-specified search (PILOT_V0: 7 directions × 5 depths × 4 scales × 2 token sets = 280).
  - §3.5 states the candidate directions exactly as PILOT_V0.md lists them: own, system or web page minus tool (from PREREG_S's rankings); tool − user; and PREREG_U's framing vector, both signs. It adds that none came from the map, which patched only system→user and own→user (PREREG_T.md: tool and web-page sources not aligned, left out).
  - §3.2's "selectivity window" now notes that the defence built there (§3.4) failed. §4 and §5 call the map–lever link interpretive.
  - Note: PLAN_BIGGER.md had planned the search "at the PREREG_T content-phase peak ±3"; the pilot as run used relative depths 0.35–0.75 (PILOT_V0.md).
- B2: FIXED (coordinator decision 2). Records: `code/src_monitor.py` wrap(); `code/bench.py` lines 6–7, 84–86 and 109–123.
  - The tool source and SEP's data are both a user turn prefixed "Tool output:\n". The tool − user direction differs from plain user text only by that prefix. InjecAgent is the repository's own prompt in one user turn.
  - §2 now says no model's own tool-message format is used.
  - §3.7 states that SEP's data was placed in the training wrapper and that InjecAgent keeps its own ReAct prompt. "What generalizes"/"What does not" became "On SEP (descriptive)"/"On InjecAgent".
  - §3.8's reading now reads "on SEP, in the training wrapper ... on InjecAgent, in its own format ...". §4 and the abstract are aligned.
  - §5 CounterSteer: "Our tool − user direction is not a role axis: both of its ends are user turns ... not directly comparable."
  - §6 adds "Models' own tool-message formats were not tested". The §6 transfer bullet is reworded to match.
- B3: FIXED (coordinator decision 3). §3.1 gains "The verdict by criterion" (SA):
  - behaviour criterion: FRAGMENTED in Qwen3-8B and SmolLM3 (τ 0.2), MIXED in Qwen3-1.7B and OLMo (τ 0.4);
  - Qwen3-1.7B's FRAGMENTED headline comes from the edit criterion alone (edit_verdict NONE);
  - OLMo misses narrowly (mean attribution 0.3245 against 0.30; obey edit +0.00433 "moved", Holm p 0.0065).

  The τ step is stated (one swapped pair of five sources = 0.2). In the abstract, Qwen3-1.7B's verdict is said to rest on the null edit. No bootstrap CI was added (see decisions).
- B4: FIXED (coordinator decision 3). The claim is now "no single source ordering across behaviours": abstract heading, §3.1 heading, the §3.3 list, and the §4 and §5 headings.
  - The §3.3 table row names the preregistered hypothesis "no single tag" in quotes, as a label.
  - §4 and §5 add that the results do not rule out one source code read with behaviour-specific weights.
  - §5 no longer says the three behaviours were measured "on the same items": obeying uses instructions and believing uses facts.
  - §6 adds the different-item-types caveat.
- B5: FIXED. §3.2's "may explain PREREG_S's null" is replaced by "Why PREREG_S's edit failed is open". In Qwen3-1.7B the lever acts at the edit's own layer (13 of 28); in Qwen3-8B it acts at 16, against the edit's 17 of 36. Sources: `cloud_v0/out_v0/*/gen.json` layers {0.45: 13} and {0.45: 16}, n_layers 28 and 36; PREREG_S.md decision layers 13 and 17. §4 now says the lever acts at about 0.45, below the obey content peak (0.5–0.8, §3.3), and that why ×4 works where ×1 did not is untested.
- B6: FIXED. Qwen3-8B is marked as one of the four selection models in the abstract, §1, §3.7 and §3.8. §3.7 and the abstract add that the only two non-NONE models in PREREG_X (Qwen3-8B, Qwen3-1.7B) were selection models and both held-out families got NONE (XA verdicts; PILOT_V0.md models).
- B7: FIXED. §3.7 quotes PREREG_X's preregistered reading of NONE ("the effect on synthetic items does not carry over to real injections", PREREG_X.md) and labels the rest descriptive. The verdict column is renamed "Sealed verdict (needs both benchmarks and the random control)". A note explains that SmolLM3's 3.9% InjecAgent baseline cannot pass X3's 5-point drop (XA: 5/129).
- B8: FIXED, but not with the reviewer's wording. §4 now says that in other families the lever matches or beats the prompt defences on SEP: XA X2 true in OLMo-2-7B, SmolLM3 and Granite, and YA X2 0/4 with confidence intervals spanning 0. On InjecAgent it does no better than its single random draw in any of the four non-Qwen models, and at least one prompt defence does as well in each (XA X5 false; per-prompt intervals). The reviewer's "the prompt defences that backfired did so in Qwen" was NOT used, because VA contradicts it: OLMo-2-7B's reminder raised obedience by +0.432 (p 0.00165, 22 decided instruction items). §4 instead says prompt defences can backfire, in Qwen3-1.7B (defensive prompt, datamarking) and OLMo-2-7B (reminder).
- B9: FIXED, with the same correction. The abstract now reads "some raised obedience instead (significantly in Qwen3-1.7B and OLMo-2-7B)" (VA: Qwen3-1.7B P +0.097, p 0.005; SPOT +0.188, p 0.00005; OLMo REMIND +0.432, p 0.0017). §3.6 adds the OLMo reminder result. §3.5's "confirms ... not a readout artifact" is replaced by: same sign, untested in the pilot; significant in the sealed test in Qwen3-1.7B but not Qwen3-8B (VA P p 0.079, SPOT p 0.113).
- B10: FIXED. "Keeping belief" is replaced in the abstract, §3.6 and §5 by "belief in the tool's facts fell by at most 0.10, less than half the drop in obedience". §3.6 adds that this is 38% and 27% of the obedience drop in Qwen3-8B and SmolLM3 (VA: 0.0903/0.2361 and 0.0972/0.3611).
- B11: FIXED. §1's "behaviour does not track reportable source knowledge" is replaced by "source effects on behaviour occur even in models that attribute sources poorly in a five-way lettered question". §3.1 now names the lettered question. §6 adds that the attribution readout was not checked against generation (PILOT_V0.md audited only the answer-word readouts).
- B12: FIXED. §2 Readouts states the 0.5 parity baseline and that the user-source score is about 0.5 by construction (src_monitor.py contexts(): the competitor is always ("user", comp), both orders). §3.1 is rewritten. In Qwen3-8B no other source beats a competing user message for obedience (SA: system 0.497, web page 0.478, tool 0.418, own 0.247). Qwen3-1.7B's 0.71 for tool output is set against a user-against-user score of 0.51.
- B13: FIXED. The abstract, §1 and §5 now say that before the handoff the role-marker tokens, not the statement's own words, carry the source. §3.2 defines transfer (values above 1 = overshoot) and notes that the difference starts on the markers because only the role word differs.
- B14: FIXED. §1's "Most of them implicitly treat ..." is replaced by "Several steering defences act along a single role or user-versus-tool direction (Liu 2026; Zhang, Lee & Park 2026). That fits a picture in which one internal source signal governs how a text is used." The descriptions are from REFERENCES_VERIFIED W3 and the 2026-10-29 addendum.
- B15: FIXED.
  - §3.8's "Utility held in every model" is replaced: SEP utility moved by −1.0 to +1.3 points (YA U none/DEF), and InjecAgent's valid-reply rate, labelled a format measure, fell by 1.3 and 3.3 points.
  - SEP-utility columns were added to the §3.7 table (from XA: 64.7→67.7, 45.7→47.0, 48.0→54.0, 66.3→68.0, 61.3→73.7, 63.7→65.3) and the §3.8 table (from YA: 71.0→72.3, 73.3→72.3, 67.3→68.0, 66.7→66.0, 69.3→70.0, 88.7→89.3).

## Extra corrections made alongside (records-backed)

- §4: "On SEP in held-out families" → "in the four held-out models" (two are OLMo sizes; NUMBERS_RECHECK_Y W3).
- §3.3 lag values and the RNDCTL means (see B-S14 and B-M5).

## Needs the coordinator's decision

1. **Cost (B-M1 L101 / B-S9).** Paper B says "about $56 ... about $38 through PILOT_V1 and about $18 for PREREG_Y". The records disagree:
   - **The $38.** NUMBERS_RECHECK_Y row 8 marks it UNVERIFIABLE, and no record gives it.
   - **The billing explorer.** PAPER_DRAFT.md's data section, the figure Paper A uses, gives about $75.3 for all cloud work through the end of PILOT_V1 (27 Oct $23.22 + 28 Oct $52.10). That covers both papers' cloud work, and no record separates Paper B's share.
   - **PREREG_Y.** It is about $18.4 from pod times ($9.62 + $8.77); the recheck's record-derived minimum is $18.16.
2. **B-S17 header (records conflict with the review).** The review asked for "same norm". The highest-authority records show that the PILOT_V0 random control has own−tool's norm:
   - PILOT_V0.md: "random: control, with the norm of own−tool";
   - `code/lever_pilot.py`: `direction('random')` is scaled to the own−tool norm;
   - the raw `gen.json` norms: random = own-tool;
   - NUMBERS_RECHECK.md addendum: "The pilot's random direction has own−tool's norm, not the recipe's".

   CONSOLIDATED_RESULTS.md ("same norm and settings") and the sealed PREREG_V.md (line 32, "same-norm random direction at the same settings") are imprecise on this point. I kept and clarified the paper's header. Those two files are read-only and were not touched.
3. **Front matter (B-S2).** It still reads "Independent AI rechecks ... `NUMBERS_RECHECK.md` and its addenda". The coordinator may want to name `NUMBERS_RECHECK_STU.md` and `NUMBERS_RECHECK_Y.md` as well.
4. **Cross-paper FYI (Paper A, not edited).** PAPER_A_GOAL_PERSISTENCE.md §11 (line 438) still lists Paper B's controls (PREREG_S edit, PILOT_V0, PREREG_V H4, PREREG_X/Y X5) among "every random control in this work".

### Added in round 2

5. **B8/B9: the records contradict the skim reviewer.** Both of the reviewer's suggested wordings say prompt-defence backfires were confined to Qwen ("raised obedience in Qwen3-1.7B"; "the prompt defences that backfired did so in Qwen"). VA shows a third significant backfire outside Qwen: OLMo-2-7B's reminder, d_obey +0.4318, p 0.00165, on 22 decided instruction items.
   - What I did: I followed the higher-authority record and added the OLMo result to §3.6, §4 and the abstract.
   - Why it may need a look: it rests on few items, because OLMo often names neither answer, and neither CONSOLIDATED nor the earlier paper mentioned it.
   - Options: keep it; or drop "OLMo-2-7B" from the abstract and keep it only in §3.6.
6. **B3: τ intervals already exist in a recheck file.** Per your instruction I added no CIs. However, NUMBERS_RECHECK_STU.md ("Fragility notes") already reports an item bootstrap of τ (2,000 resamples):
   - Qwen3-8B: P(τ ≤ 0.2) = 0.73;
   - SmolLM3: 95% interval [0.2, 0.8], P(τ ≥ 0.6) = 0.29.

   You may want to cite this as recorded rather than as new analysis.
7. **Title alignment.** The abstract and section headings now use "No single source ordering across behaviours" and "A steering lever, found by search". These match your planned title ("Most chat models weigh a text's source differently for each behaviour, and a steering lever against injected instructions"). The title line itself is unchanged and still says "a map-guided lever".
8. **B1 and the plan.** PLAN_BIGGER.md had planned the search "at the PREREG_T content-phase peak ±3", i.e. guided by the map. The pilot as run (PILOT_V0.md) used fixed relative depths 0.35–0.75 instead. So "found by search, link to the map interpretive" matches what ran. If anyone cites the plan, the two descriptions differ.
