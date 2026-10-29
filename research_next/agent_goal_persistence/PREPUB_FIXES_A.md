# Paper A pre-publication fixes: change log (2026-10-29)

**File changed:** `RF\PAPER_A_GOAL_PERSISTENCE.md` only. CRLF kept (626 CRLF, 0 bare LF). Final md5 `64ea764f4c14c8134ac0e99927ea290d`.
- Backups: `scratchpad\PAPER_A_before_fixes.md` (original, md5 79121b2c…) and `scratchpad\PAPER_A_after_round1.md` (md5 654f8516…).
- Scripts: `scratchpad\fix_paper_a.py` (round 1, 90 replacements) and `scratchpad\fix_paper_a_round2.py` (round 2, 55 replacements). Each old string was asserted to occur exactly once, and each script writes only after every replacement succeeds. Both were dry-run on a copy and reviewed before being applied.
- Checks after round 2: all 36 reference entries are cited and every in-text author–year has an entry. No "map-guided", "inj2" (outside file names), MD5, pod ID or dated process label remains.
- Not touched, as instructed: the title, the author line, the "Cloud cost" paragraph and the AI-use statement (byte-identical). In the front-matter paragraph only Paper B's title was changed, under the round-2 decision ("anywhere Paper A names Paper B's title").

**Counts.**
- Round 1 (prepub_review.md):
  - must-fix: 6 of 6 fixed within my scope;
  - should-fix: 29 fixed, 2 reserved (A-S27, A-S28);
  - nice-to-have: 15 fixed, 1 partly (A-N3), 1 checked with no change needed (A-N17), 2 skipped (A-N7 by instruction; A-N19 reserved).
- Round 2 (skim): 14 of 14 fixed, plus skim B4's Paper A part and the new Paper B title.

---

## Round 1: prepub_review.md, Paper A

### Must-fix
- **A-M1: FIXED (my scope).**
  - Deleted the §6f transfer MD5 and "(added 2026-10-28)".
  - Retitled "Additional prior art verified in Codex (2026-10-28)" as "Further related work".
  - Removed every log detail from Appendix A: pod ID, MD5, archive copies, "cached", the interruption notes.
  - "Checksums were verified; the records are in the repository" now appears in §6f, the Data section and Appendix A.
  - L5–6 (front matter), L501 (cost) and L505 (AI-use) were left to the coordinator.
- **A-M2: FIXED.** Abstract changes:
  - "Three further sealed tests".
  - J/M replaced by "a social-cue test" and "a test that describes the goal as the model's own plan or analysis".
  - "in six of seven models". Source: `j.json`; Granite's authority projections are +0.0048 and +0.0234, toward "given".
  - 12/12 from `j.json`; 5 of 6 and 4 of 11 from `m.json`.
- **A-M3: FIXED.**
  - The Qwen3 trend is labelled exploratory in the abstract, the contributions, §3 and §12 item 2.
  - Abstract adds: a sealed size test across 15 models in four families found no general trend in goal holding or source sensitivity (NO_TREND); source sensitivity rises with size only within the Qwen lineage.
  - Sources: `l.json` (p 0.126, Holm 0.253; ρ Qwen3 1.0, Qwen2.5 1.0, OLMo −0.5) and `PREREG_L.md`.
- **A-M4: FIXED, then revised in round 2 (A3).** §4 is retitled and the "encoded separately" sentence replaced. Final wording is under A3.
- **A-M5: FIXED.**
  - Limitations now lists only Paper A's single-draw controls: §5, PREREG_C and PREREG_G steering; PREREG_K's random ablation; the deixis test (INJ3_PREREG); the injection test (INJ2_PREREG).
  - Sources: `PREREG_C.md`, `PREREG_G.md` (C3), `PREREG_K.md` (ablrand), `inj3_verdict.txt` (rand+2), `inj2_q4b_verdict.txt`.
  - **Correction from the records:** the exceptions are PREREG_J *and* PREREG_M. Both use 50-direction projection nulls (`PREREG_M.md`; `m.json` null_t_q95). `RNDCTL_RESULTS.md` says "only PREREG_J". §2 was corrected the same way.
- **A-M6: FIXED.** The sentence now reads "Any monitoring use of the role direction would need this comparison."

### Should-fix
- **A-S1: FIXED.**
  - Legend: added "a named verdict of a sealed rule (ONE AXIS, AMBIGUOUS, MIXED, PARTIAL, NO_TREND, INCONCLUSIVE, DOES_NOT_TRACK)". Also noted that the deixis, addressee and injection tests have log rules with hash-sealed scripts (NUMBERS_RECHECK "inj2, inj3 and addr have code-only hashes").
  - Statuses added to the headings of §6f (A-S18), §7 ("deixis FAIL; addressee INCONCLUSIVE") and §9 ("FAIL, PREREG_E and PREREG_F").
- **A-S2: FIXED.** The Qwen3-32B row is now "**FAIL** (log gate)".
  - Sources: `stage3_32b_results.txt` (L29 beyond random +0.040, p < 0.0001; given→own +0.039, p 0.435, now shown as "n.s.") and PLAN_7DAY 2026-10-27 12:00 ("gate FAILS").
  - Sweep confirmed from `sweep32_results.txt`: 5 layers × 2 directions, shifts 0.023–0.102, kept as "0.02–0.10". CONSOLIDATED's "0.03–0.10" is a rounding of the log. "2 of 10 layers" is corrected to "2 of these 10 contrasts" (layer 23 given→own p 0.074; layer 26 own→given p 0.523).
  - Added one sentence: the gate was written for 1.7B, and the other sizes were scored against the same bar.
- **A-S3: FIXED.** §2 now defines the two instruments:
  - sequential: one episode at a time, full generation, share of parsed high-emission picks (`PREREG.md`, `PREREG_B.md`);
  - fast: batched, compact quarters, probability readout (PLAN_7DAY 10-26 21:50).
  - The abstract names the instrument behind +0.18 / +0.11 (sequential; NUMBERS_RECHECK §3.2/§3.4) and +0.005 → +0.144 (fast).
- **A-S4: FIXED.** "one pass on a gate logged before data".
- **A-S5: FIXED.**
  - Abstract and §6f now say the text framed as the model's own analysis or plan was followed more than the same text framed as a colleague's or another manager's.
  - The sign sentence below the §6f table was rewritten (D = other − self, from `PREREG_M.md` and `m.json`).
- **A-S6: FIXED.** The one-axis contribution was added and the list now ends with a full stop.
- **A-S7: FIXED.** Each OLMo-2-7B value is labelled with its experiment:
  - §3 reading: "PREREG_D: 7B Instruct +0.077 vs 13B +0.008" (`d_results.json`);
  - table: +0.079 inside the window and +0.082 "all steps of the same run" (fast run, reproduced from raw files);
  - §6 pilot: +0.080 "in the same pilot" (PLAN_7DAY 10-27 15:18).
- **A-S8: FIXED.**
  - Abstract, §6 and §12 now read "was not detected (+0.013, n.s.; 20 seeds), suggesting that it depends on the template's role tokens".
  - 20 seeds = seeds 300–319 (PLAN_7DAY 15:18); p 0.54 (NUMBERS_RECHECK Abs.7).
- **A-S9: FIXED.**
  - The code shows that positions were already matched in the main design. `INSERT_AT = range(0, 30, 3)`, and gF/oF/uF go through the same `run_batch` branch in `code/agp_fast.py` and in the sealed PREREG_H bundle `bundles/agp13.tgz`. `g_eval.py` and `mpilot.py` both call it.
  - So §12's claim was kept, made precise ("same steps, same point in each step"), and §6b's MPILOT paragraph was recast as a replication on fresh seeds.
  - +0.028 [0.013, 0.046], 36/40 is from `mpilot_analysis.json`.
- **A-S10: FIXED.** "encodes" → "orders". The round-2 wording adds "correlational" (A2).
- **A-S11: FIXED.** Blank line added before "Generality".
- **A-S12: FIXED.**
  - The counting rule is now stated: three pairs per model, as in `PREREG_I.md`.
  - Adjacent pairs only: 9 of 12 decided in PREREG_I (`i.json`), and 15 of 15 decided with PREREG_H's 6 (`PREREG_H.md` A1/A2; `h.json`).
  - 21 of 21 is now stated as including user − own. The abstract and §12 were changed the same way.
- **A-S13: FIXED.** "(Geng et al. 2026)" added at the first mention of Control Illusion.
- **A-S14: FIXED.** "Holm p (vs plain / vs random ablation)" (`PREREG_K.md`: T1 flattening vs plain, T2 vs random ablation).
- **A-S15: FIXED.**
  - §6e notes that Qwen3 and Qwen2.5 share a lineage (`PREREG_L.md`).
  - The union is now "17 models from six families".
  - user > system is significant in all 17: `i.json` (SmolLM3 p 0.00075, Granite p 0.00105) and §6e's 15/15 (NUMBERS_RECHECK §6e.6).
- **A-S16: FIXED.** P and A are defined as in `PREREG_L.md`: P = mean p_goal(gF); A = p_goal(uF) − p_goal(oF).
- **A-S17: FIXED.** "Qwen3-32B's weak goal holding… system-turn p_goal 0.342 in PREREG_I; here P is 0.34" (`i.json` g 0.3415; `l.json` P 0.3376).
- **A-S18: FIXED.** §6f heading: "(H1 MIXED, H2 MIXED, H3 DOES_NOT_TRACK; PREREG_M)" (`m.json`).
- **A-S19: FIXED.**
  - "predictions from two AI systems hashed before launch".
  - The MPILOT_RESULTS.md and m.json file names were moved to the Data section, with the correct path `cloud_prereg_m/m_descriptive_check.json`.
- **A-S20: FIXED.** The deixis paragraph was rewritten. Final wording is under A8. Numbers are from `inj3_verdict.txt`: 4B document p1 0.882 → 0.050; 1.7B system p2 −0.826, p1 −0.693.
- **A-S21: FIXED.**
  - §8 is retitled "role steering reduces it in one model (REPL.)" and names the test INJ2_PREREG: rule in the log, script `code/inj2.py` sealed in `INJ2_PREREG.sha256`, and inj2.py's docstring says "preregistered in PLAN_7DAY.md".
  - RNDCTL is described in §8: 48 cases, 16 draws at each sign, predictions hashed (`RNDCTL_RESULTS.md`, `rndctl_q4b/summary.txt`).
- **A-S22: FIXED.** "+0.08" is the matched obey arm of believe-or-obey pilot 1: own − given p_hi +0.081, 20 seeds (PLAN_7DAY 10-27 16:32; NUMBERS_RECHECK §10.4, 20/0).
- **A-S23: FIXED.**
  - Reference entry added. Paper B is cited as "Paper B (Ramdan 2026)" in §10 and §11.
  - The entry title was updated in round 2 to the coordinator's new title.
- **A-S24: FIXED.** "was preregistered or logged before data".
- **A-S25: FIXED.**
  - Now cited as Zeng et al. (2026) and Balp-Straffon et al. (2026), with no inline titles or URLs.
  - Each bullet states the relation: we did not compare against V-Steer; the role direction is tested causally, not by probe fit.
  - Claims checked against REFERENCES_VERIFIED entries 1–2.
- **A-S26: FIXED (cost paragraph untouched).**
  - Gives the GitHub URL and the Zenodo `code-and-data.zip`.
  - Lists all 27 `.sha256` files in RF: Paper A's PREREG and PREREG_B–M; INJ2/INJ3/ADDR (code-only seals); MPILOT_PRED and RNDCTL_PRED (prediction hashes); Paper B's PREREG_S–Y and PILOT_V0/V1.
  - Adds the main analysis paths.
- **A-S27: SKIPPED.** Reserved to the coordinator.
- **A-S28: SKIPPED.** Reserved to the coordinator. Facts for it are in the decisions list below.
- **A-S29: FIXED.**
  - Appendix A moved after the References. It is pointed to from §12 ("training the hierarchy").
  - It now has a short design description (Control Illusion conflicts; "system success" defined; greedy decoding; gates fixed before data) and a legend for the condition codes.
  - PREREG_N is reworded as "the planned confirmatory test on held-out tasks was not run". Timestamps were removed from the headings.
  - Design facts are from PLAN_7DAY 10-28 12:15, `code/n_pilot.py` and `DECOMPOSITION_PILOT_PLAN.txt`. The table numbers are unchanged (NUMBERS_RECHECK Fix.1–6, Dec.1–7).
- **A-S30: FIXED.** The "Verified 2026-10-28" note was deleted.
- **A-S31: FIXED.**
  - Dropped G. & Lindsey, C. T. Leong, R. Liu (DRIP) and Zhan (InjecAgent).
  - Cited at first use: Holm in §2; the models in §3 (SmolLM2, SmolLM3, EuroLLM); Qwen2.5 and Falcon3 in §6e; LoRA in §9.
  - Added the Qwen3, OLMo 2 and Granite (report + model card) and Falcon3 entries, copied from PAPER_DRAFT/Paper B. OLMo 2's venue was shortened to "*COLM 2025*" for internal consistency.

### Nice-to-have
- **A-N1: FIXED.** The abstract's opening sentence was rewritten.
- **A-N2: FIXED.** "of the user − own spread".
- **A-N3: PARTLY.**
  - The Tsui "Not new" bullet in §12 and Leong's §4 paragraph were shortened, with pointers to §1.
  - The §12 Leong item was kept, because its sub-bullets carry details found nowhere else.
- **A-N4: FIXED.** "found late" was removed.
- **A-N5: FIXED.** The three stage-1 directions are now named, from the PLAN_7DAY stage-1 gate (10-26 21:50) and `fast_val_results.txt`.
- **A-N6: FIXED.**
  - "stage-2" replaced by "the representation test (§4)", in §5 and §6b.
  - The depth-sweep sentence now reads: exploratory sweep (seeds 400–419) with a selection rule sealed in advance, then a sealed test on seeds 500–539 (`PREREG_C.md`).
- **A-N7: SKIPPED.** No renumbering, as instructed.
- **A-N8: FIXED.** "EXPL., replicated under seal in PREREG_H".
- **A-N9: FIXED.** All 8 disagreeing pairs are listed with their turns (`j.json`).
- **A-N10: FIXED.** "may act".
- **A-N11: FIXED.** "one model (Qwen3-1.7B) significantly goes in the predicted direction" (`m.json`: D +0.00357, Holm p 0.0198).
- **A-N12: FIXED.** The §6f table now:
  - uses probability differences, from `m.json` D means: +0.004, −0.023, −0.090, −0.077, −0.010, −0.052;
  - uses the "−" minus sign and writes "OLMo-2-7B";
  - is sorted by family and size.
- **A-N13: FIXED.** "J" → "PREREG_J".
- **A-N14: FIXED.**
  - "n 240 / n 16" replaced by training conversations; the doses (16, 48, 240) are stated.
  - E3 is labelled as the PREREG_E run (`PREREG_E.md`; `cloud_binding_e3/e3.json`).
- **A-N15: FIXED.**
  - The full stop mid-list became a semicolon.
  - "earlier behavioural work" now has "(for example Geng et al. 2026, above)".
- **A-N16: FIXED.**
  - Ye et al. (2026) is used throughout; inline arXiv IDs and venue notes were removed.
  - Hu's venue is now "*ICLR 2022*". "pp." and "G., A." went with the dropped entries.
- **A-N17: CHECKED, no change.** "Xu, S., et al." is correct (REFERENCES_VERIFIED #12: five authors). CONSOLIDATED's "Xu & Daneshjou" is the error.
- **A-N18: FIXED.** Double blank lines removed; a blank line added before §12; the Appendix moved; heading timestamps removed.
- **A-N19: SKIPPED.** Reserved: it is in the AI-use statement.

---

## Skim findings (round 2: prepub_skim.md, Paper A A1–A14)

- **A1: FIXED** (abstract and §6d, merged with A-N2).
  - The raw 27–44% is kept, worded as "narrows".
  - Added the competence-normalised reading:
    - competence falls 22%, 24% and 36% in 4B, 8B and 32B;
    - random ablation leaves competence nearly unchanged;
    - per unit of competence, the spread falls 25% and 26% in 4B and 8B and rises in 32B, from 0.97 to 1.11;
    - the system − own gap still falls per unit of competence, by 39%, 83% and 55%.
  - The §6d Reading was adjusted to match.
  - Source: `cloud_prereg_k/k.json`, from competence_by_arm and the p_goal means:
    - 4B competence 0.5621 → 0.4358, spread 0.0835 → 0.0483;
    - 8B competence 0.7059 → 0.5399, spread 0.0788 → 0.0443;
    - 32B competence 0.3379 → 0.2167, spread 0.3274 → 0.2403;
    - random-ablation competence 0.5528, 0.7062 and 0.3316;
    - g−o pairs 0.0285 → 0.0135, 0.0204 → 0.0026 and 0.1508 → 0.0435.
  - These normalised figures are descriptive. The sealed PARTIAL verdict is unchanged.
- **A2: FIXED** (merged with A-S10).
  - Dropped "carries no built-in user-versus-system difference" and "The informative part is user versus system".
  - Added the construction argument: with vR = a − (s+u)/2, proj(s) − proj(u) = (|a−u|² − |a−s|²)/2. I checked the algebra; it holds exactly for the neutral-sentence means.
  - The match is called correlational in the abstract, §1, §6b (paragraph, Reading and bullet), §11 and §12 (item 4 "matches"; the Geng bullet "whose order matches it").
- **A3: FIXED** (merged with A-M4).
  - §4 heading: "the tested probes found no self-specific 'this is mine' tag (FAIL, log gate, Qwen3-1.7B; the control transfers as well or better in 9 more models)".
  - New sentence: the role probe does transfer in 1.7B (≈0.80), but the control is only 0.12 lower there and as good or better in the nine others, so the shared signal is largely not self-specific (NUMBERS_RECHECK §4.2–4.3).
  - The abstract bullet now says "found no self-specific…".
  - The skim's "transfers about as well" was not used for 1.7B, where the control is 0.12 lower.
- **A4: FIXED.**
  - §6 heading: "present at the first testable stage, supervised fine-tuning (AMBIGUOUS, PREREG_D)".
  - §1 (two places), the abstract and §12 item 3 say "first (testable) stage".
  - "No result supports a preference-tuning origin" replaced by: "The 13B verdict (H-pref) rests on a flat gap of 0.007–0.008 that crossed p < 0.01 only at the last stage. We do not read it as a preference-tuning origin." Source: `d_results.json` 13B G 0.0075 / 0.0066 / 0.0081 with p 0.0278 / 0.0271 / 0.00855. The sealed verdicts are unchanged.
- **A5: FIXED** (merged with A-M3).
  - The §3 table gains a "Given cell gF (p_hi)" column: 0.041, 0.333, 0.233, 0.148, 0.638, 0.185 (OLMo, steps 0–22), 0.127, 0.067, 0.214.
  - The headroom caveats were added to the §3 reading and the abstract: 1.7B at the floor; weak-text gap +0.107; 4B in 4-bit; 32B idiosyncratic.
  - §6b's "in line with the Qwen scale trend" was replaced by a reconciliation with §6e.
  - Sources:
    - gF computed from the raw fast-instrument run files: `fast_val/`, `fast_Qwen3-4B/`, `cloud_results/out_fast_Qwen3-8B` and `-14B/`, `cloud_results32/out_fast_Qwen3-32B/`, `cloud_families/out_fast_*`, `fast_SmolLM3-3B/`;
    - the recomputation reproduces every published gap and seed count exactly (for example 8B +0.0283, 33/7; OLMo +0.0790, 35/5; SmolLM3 −0.0141);
    - the summary files agree where they exist (`fast_val_results.txt`, `replication_results.txt`, `stage3_32b_results.txt`);
    - 13B gF 0.1268 is from `d_results.json`;
    - the 1.7B seed count 28/12 is from `fast_val_results.txt`.
- **A6: FIXED.** The construct caveat now says the comparisons hold the text fixed across roles, and that authority versus push-against-pressure is separated only in the §6b world.
- **A7: FIXED** (§5 Reading).
  - States that each p is against one draw.
  - Outside Qwen the margins (+0.04 to +0.13; `c_results` values in the paper's table) are no larger than RNDCTL's single-draw SD (0.13–0.22, from `rndctl_q4b/summary.txt`, a different task). Specificity outside Qwen is therefore "not established", which is softer than the skim's "untested".
- **A8: FIXED** (merged with A-S20).
  - The abstract and §12 now read "failed its sealed test in two small Qwen3 models".
  - §7 gains a design sentence: the injection task, the code-word instruction inside the document or as a system message, first-token compliance, 120 cases. Sources: PLAN_7DAY deixis entry and `inj3_verdict.txt`.
  - §7 also notes the 1.7B document floor case (p1 base 0.000).
  - The FAIL label is kept, because the sealed verdict is "deixis refuted".
- **A9: FIXED.**
  - "Every model" is kept, because it holds: oN − oF in all 8 capable models, from +0.13 (Qwen3-32B) to +0.80 (Qwen3-1.7B). Recomputed from the raw fast files: +0.796, +0.559, +0.559, +0.443, +0.132, +0.350 (OLMo, steps 0–22), +0.423 and +0.231, each with ≥ 34/40 seeds; matches NUMBERS_RECHECK §3.20.
  - Added the caveat that the notes are a different text, so the contrast is about content, not voice.
- **A10: FIXED.**
  - Measure and direction were added to the §3, §5, §5 PREREG_C, §6, §6b PREREG_G and PREREG_H table headers or notes. §6 uF − gF now gives its sign.
  - The §6b correlation sentence was rewritten with the correct predicted sign.
  - **The skim's suggested text was not used, because it is wrong.** The projection points toward "own", and own is obeyed least, so an episode-level axis predicts a *negative* projection–p_goal correlation. OLMo matches that (−0.251, −0.415, −0.313). Qwen3-14B is opposite (+0.267, +0.267, +0.424), and so is Qwen3-8B in 2 of 3 cells; its user cell (−0.147) has the predicted sign (`h.json`).
- **A11: FIXED.** "three smallest vs four larger models; size and family cannot be separated" is now stated in the §6c heading bullet and Reading, and in the abstract (PREREG_J's seven models, from `j.json`).
- **A12: FIXED, with a deviation from the coordinator's note.**
  - Tests *do* exist for the pilots. In `e2.json` and `e4.json`, every pilot adapter's injection rise has a paired test across 120 cases, with each p < 0.01 (E2 all p 5e-05; E4 own48b p 0.008).
  - The sealed runs (`e3.json`, `f.json`) have no test. In them, 6 of 24 adapters fall below the untrained model (PREREG_E 10/12 above base 0.573; PREREG_F 8/12 above base 0.4885), so the skim's "in every adapter" would be false.
  - The abstract now says: "+0.02 to +0.07 in the two sealed tests; not tested for significance, and not in every adapter".
  - The §9 table rows and Reading give the arm means (E +0.016 / +0.032; F +0.065 / +0.041) and the adapter counts.
- **A13: FIXED.** The Instruct value was found: R = 0.0767 / 0.6794 = 0.113 (`d_results.json`; SFT 0.0628 / 0.4739 = 0.133, DPO 0.0714 / 0.6716 = 0.106). The relative gap does not fall throughout, so the text says "highest after SFT: 0.133, against 0.106 after DPO and 0.113 after Instruct", next to the raw rise 0.063 → 0.071 → 0.077.
- **A14: FIXED.**
  - "About three quarters" now applies to PREREG_F only: 0.842 → 0.206 and 0.229, cuts of 76% and 73% (NUMBERS_RECHECK MISMATCH #10).
  - The unbalanced 240-conversation pilots "reached the floor, partly by learning to oppose the pressure". "Partly" softens the skim's wording, since the shortcut test shows only a partial shortcut.
- **Extra: skim B4 (its Paper A §10 part): FIXED.** "which supports separate readouts" → "In most models tested, obeying and believing rank the sources differently (sealed verdict FRAGMENTED), so the two behaviours weigh a text's source differently". This matches Paper B's new title.
- **Extra: Paper B title: FIXED.** The exact new title is in the Ramdan 2026 entry and in the front-matter paragraph. No "map-guided" remains.

---

## Needs the coordinator's decision
1. **Front matter.** Under the "anywhere" instruction, I changed only Paper B's title inside the reserved paragraph; revert it if you prefer. That paragraph still says "see the AI-use statement at the end". With Appendix A now after the References, that statement is no longer last.
2. **A12 premise.** Pilot tests do exist (see above). "Not tested for significance" is applied to the sealed-run averages only.
3. **A10.** The skim's suggested correlation wording would have reversed the meaning; the paper now has the correct sign.
4. **A-S2 labels.** The 32B row is FAIL (log gate) while 4B–14B are "EXPL. (gate met)". This follows CONSOLIDATED and the log, and one sentence in §5 explains it. Make it uniform if you prefer.
5. **Data paths.** The Data section names files by their RF paths (for example `cloud_prereg_m/m_descriptive_check.json`, `decomposition_pilot_codex/`). Please confirm the GitHub repo and `code-and-data.zip` keep that layout.
6. **Read-only records that disagree with the result files** (the paper follows the result files):
   - CONSOLIDATED's 32B sweep "0.03–0.10" (file: 0.023–0.102);
   - CONSOLIDATED's "Xu & Daneshjou" (correct: Xu et al.);
   - RNDCTL_RESULTS's "only PREREG_J uses a distribution" (PREREG_M does too);
   - MPILOT_RESULTS's "position confound controlled" (positions were already matched in PREREG_H, per the code and the agp13 bundle).
7. **Facts for A-S28 (AI-use statement).**
   - (i) NUMBERS_RECHECK.md's 168 claims covered Draft 6's abstract, §2–§10 (including §6b–§6f, PREREG_G–M), the fix pilot and the decomposition diagnostic. §11, §12 and Data were only spot-checked. MPILOT and RNDCTL came later; I checked their Paper A numbers against `mpilot_analysis.json` and `rndctl_q4b/summary.txt`, and they match.
   - (ii) Paper A now has 36 references; "32 references" referred to the earlier list. The model and method entries were verified in the REFERENCES_VERIFIED addendum.
   - (iii) PLAN_7DAY 10-27 15:45 records "Believe or obey?" as one of the "one experiment" answers the user brought from other model sessions.
   - (iv) PLAN_7DAY shows that Claude designed and launched the fix-test pilot (10-28 12:15) and Codex recovered it (13:17). Codex planned and ran the decomposition diagnostic (13:23; `DECOMPOSITION_PILOT_PLAN.txt`).
8. **A-S27** (the cost paragraph) is still unchanged.
