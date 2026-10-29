# Pre-publication review of Paper A and Paper B (2026-10-29)

**Files reviewed:**
- `PAPER_A_GOAL_PERSISTENCE.md` (585 lines)
- `PAPER_B_SOURCE_MONITORING.md` (533 lines)

Doubts were resolved against `PAPER_DRAFT.md` and `CONSOLIDATED_RESULTS.md` only. No file was edited.

**How to read the entries:**
- Line numbers ("L") refer to the papers as saved at 12:02 today.
- **[split]** marks a problem that the split created, or that the split made wrong. Every other problem was carried over unchanged from Draft 8 of `PAPER_DRAFT.md`.

## Counts

| | Must-fix | Should-fix | Nice-to-have |
|---|---|---|---|
| Paper A | 6 | 31 | 19 |
| Paper B | 5 | 29 | 16 |

**Checks that passed:**
- **Citations.** Every author–year citation in the text has an entry in the reference list. The exceptions are the defences named in B L454 and the two companion papers, which are cited by filename (see B-M4, A-S23 and B-S29).
- **Tables.** No table has a column-count mismatch.
- **AI-use statements.** Both state that an AI designed, ran, analysed and wrote the work. Both end with the two required sentences.
- **Cross-references.** Paper B's internal section pointers were renumbered correctly from §6g–§6n to §3.x, except for B-S16 and B-S25. Paper A's internal pointers (§2, §3, §5, §6b, §9, §10) are correct.
- **Named files.** Every file, figure and bundle the papers name exists in the folder. I checked this by name only.

---

## Paper A: "Whose words count?"

### Must-fix

**A-M1. Draft and process notes are visible to readers.**
- L5 [split]: "Paper A of two, split 2026-10-29 from the full technical report (`PAPER_DRAFT.md`, Draft 8)."
  - The range "(former §6g–§6m)" is also wrong. The draft's source-monitoring sections ran from §6g to §6n.
- L6: "Draft 7 added PREREG_S, plus corrections from an independent recheck of 168 numeric claims…"
  - PREREG_S is no longer in this paper.
  - "Independent" conflicts with the AI-use statement's "AI rechecks, not outside or human validation".
  - The line is a bullet with no parent item.
- L379: "Transfer MD5: 2ceefa5a34f4f7762a233f6024b06f73."
- L473: "(added 2026-10-28)".
- L488: "**Additional prior art verified in Codex (2026-10-28).**"
- L501: "The $17.43 reading in earlier drafts (2026-10-27 21:50 AST) was a partial snapshot."
- L505: "…and revised this unpublished draft." and "their corrections are in Draft 7".
- L513: "Recovered by restarting existing pod ilrvy2lnddoirw, then stopped after a verified local backup. Transfer MD5: 3499116f… The full archive and a second short-path copy are saved."
- *Fix:*
  - Delete all of these.
  - Replace L5–6 with one sentence that cites Paper B as a formal reference.
  - Keep provenance as "checksums were verified; records are in the repository".
  - Retitle L488 "Further related work".

**A-M2. Abstract L40–43 disagrees with the body and uses undefined labels.**
- L40 announces "Two further sealed tests sharpen the claim", but the bullets that follow cover three sealed tests: PREREG_K, PREREG_J and PREREG_M.
- L43 uses "J found Nature < blog in 12/12…" and "The broader follow-up M was MIXED". "J" and "M" are not defined in the abstract.
- L42 says "Social-status cues move text along it in every model". §6c (L303) says six of seven: "In Granite the CEO header moves it slightly the other way". The abstract still has the older wording from `CONSOLIDATED_RESULTS.md`.
- *Fix:*
  - Write "Three further sealed tests…".
  - Replace J and M with plain descriptions: "a social-cue test" and "a test that describes the goal as the model's own plan".
  - Change "in every model" to "in six of seven models".

**A-M3. The scale trend is presented as a finding, but the paper's own sealed size test found no trend.**
- L23 (abstract): "Across Qwen3 it grows with size, from +0.005 at 1.7B to +0.144 at 32B." This is exploratory (the §3 table marks it EXPL.), but the abstract does not say so.
- L60 lists "a scale trend" as a contribution.
- L448 (§12, contribution 2) says the discount "grows with size in Qwen3…", with no exploratory label.
- §6e (PREREG_L, sealed) found NO_TREND (Holm p 0.25). Neither the abstract nor the contributions mention this.
- *Fix:*
  - Label the Qwen3 trend as exploratory in the abstract, the contributions and §12.
  - Add one sentence to the abstract: "A sealed test across 15 models in four families found no size trend (NO_TREND); the rise is specific to the Qwen lineage."

**A-M4. The §4 title and conclusion claim more than the abstract allows.**
- L139: "## 4. Representation: no abstract "this is mine" tag…"
- L146: "Role and attribution are encoded separately."
- The abstract (L33) says "…this does not establish that none exists". `CONSOLIDATED_RESULTS.md` says the same: "does not establish the absence".
- *Fix:*
  - Retitle §4 "Representation: the tested probes found no transferable 'this is mine' tag".
  - Rewrite L146 as "A probe trained on role does not transfer to attribution, so in these probes the two are at least partly separate."

**A-M5 [split]. Limitations list the other paper's experiments.**
- L439: "That covers PREREG_S's edit, PILOT_V0, PREREG_V (H4), PREREG_X and Y (X5), the role-steering contrasts, PREREG_K and inj2."
- PREREG_S, PILOT_V0, PREREG_V, PREREG_X and PREREG_Y are now in Paper B.
- "inj2" (also at L440, "in inj2's setup") is never defined in Paper A, because §8 does not name its test.
- *Fix:*
  - List only Paper A's controls: the §5 and PREREG_C steering contrasts, PREREG_K, and the §8 injection test.
  - Name the §8 test once, in §8.

**A-M6. The text refers to a monitoring tool that the paper never proposes.**
- L491: "The proposed monitoring tool therefore needs a narrower, explicit comparison."
- Paper A proposes no monitoring tool. The sentence comes from a Codex planning note; `CONSOLIDATED_RESULTS.md` says "before proposing a new defence or monitor".
- *Fix:* Delete the sentence, or rewrite it as "Any monitoring use of the role direction would need this comparison."

### Should-fix

**A-S1. L8–13: the status legend is incomplete.**
- The legend lists PASS/FAIL, log gate, AMBIGUOUS, EXPL. and REPL.
- The paper also uses ONE AXIS, MIXED, PARTIAL, NO_TREND, INCONCLUSIVE and DOES_NOT_TRACK.
- The §6f heading (L352) and the §7 heading carry no status, although L8 says "Every claim carries its status".
- *Fix:* Add "or a named verdict of a sealed rule (for example ONE AXIS, MIXED, PARTIAL, NO_TREND)", as Paper B's legend does.

**A-S2. L10 vs L163: the Qwen3-32B steering row has the wrong status.**
- The legend says the "Qwen3-1.7B and 32B steering rows" have log gates. The 32B row reads "EXPL. (gate not met)".
- `CONSOLIDATED_RESULTS.md` calls this row "FAIL at this layer".
- The same row reports "0.02–0.10 per layer (2 of 10 layers n.s. against random)". `CONSOLIDATED_RESULTS.md` reports "same sign everywhere, 0.03–0.10 per layer".
- *Fix:* Label the row "FAIL (log gate)", and confirm the sweep numbers.

**A-S3. L22–23, L104, L111: two instruments are used but only one is defined.**
- The paper refers to a "sequential instrument" and a "fast instrument". §2 describes only one readout.
- The abstract puts "The gap passed a preregistered test in Qwen3-1.7B" (sequential instrument, +0.11 to +0.18) next to "+0.005 at 1.7B" (fast instrument). Without the distinction, these look contradictory.
- *Fix:* Define both instruments in §2, and in the abstract name the instrument behind each number.

**A-S4. L27: a log-gated pass is called preregistered.**
- "(one preregistered pass; …)"
- The 1.7B pass is a log gate (L10, L159). The legend keeps log gates separate from hash-sealed preregistrations.
- *Fix:* "one pass on a gate logged before data".

**A-S5. L43 and L367: the self-framing result is described the wrong way round.**
- L43: "semantic self-framing increased goal-choice probability in five of six models".
- L367: "Negative values mean that self-framing increased the mean goal-choice probability."
- The measure is other minus self. The paper's own follow-up pilot (L377) finds the contrast is "mainly a discount on a rival manager's plan … rather than a premium on self-framing".
- *Fix:* "Goal text framed as the model's own plan was followed more than the same text framed as another manager's."

**A-S6 [split]. L58–63: the contributions list is truncated.**
- The list ends with a semicolon, because its last two items moved to Paper B.
- It omits the paper's main sealed result, the one-axis ordering (§6b; item 4 in §12).
- *Fix:* Add the one-axis result, and end the list with a full stop.

**A-S7. L128, L136, L213: one quantity is given four different values.**
- OLMo-2-7B's gap in the native format appears as:
  - +0.079 in the table;
  - "+0.077" in the reading eight lines later;
  - +0.080 in the pilot;
  - +0.082 "all steps".
- *Fix:* At L136 write "(PREREG_D: 7B Instruct +0.077 vs 13B +0.008)", and label each of the other values with its experiment.

**A-S8. L30 and L213: the plain-label pilot is overstated.**
- The claims are "the discount disappears when roles are written as plain-text labels" and "The discount rides on the template's role tokens".
- Both rest on one exploratory pilot with a non-significant result (+0.013).
- The seed count ("20 seeds") appears only in the abstract.
- *Fix:* "was not detected (+0.013, n.s.; 20 seeds), suggesting that it depends on the template's role tokens". Add the seed count to §6.

**A-S9. L244 vs L484: the two sections disagree on reminder position.**
- §6b reports an exploratory "Position-matched check … With the reminder inserted at the same steps".
- §12 says "In our design the reminder's position is the same for every role."
- If positions were already matched, the check would not be needed.
- *Fix:* Say what differed in the main design (insertion step, header or token offset), or drop the L484 claim.

**A-S10. L255: "encodes" is stronger than the ablation supports.**
- "One learned, content-free direction encodes the authority order of all three chat roles".
- After the §6d ablation, the user − system gap "mostly survives" (L324). The direction predicts the order but does not carry all of it.
- *Fix:* Use "orders" or "predicts" instead of "encodes".

**A-S11. L258–259: a missing blank line breaks the layout.**
- There is no blank line before "**Generality (PASS, PREREG_I).**", so Markdown renders it as part of the "practical corollary" bullet above.
- *Fix:* Insert a blank line.

**A-S12. L265–277 (also L38 and L454): the comparison counts cannot be reproduced from the table.**
- The table shows two comparisons per model.
- The text counts three per model: 15 decided out of 18. The three undecided pairs are all system − own, so user − own is also being counted.
- "21 decided pairs" then adds PREREG_H's comparisons, which were counted at two per model.
- User − own follows from the other two pairs, so it is not independent evidence.
- *Fix:* State the counting rule, or report adjacent pairs only (user − system and system − own).

**A-S13. L293: "Control Illusion" has no citation at first mention.**
- "These are adapted from Control Illusion."
- Geng et al. (2026) is first cited at L474.
- *Fix:* Add "(Geng et al. 2026)" at L293.

**A-S14. L314: "Holm p (T1 / T2)" is never defined.**
- `CONSOLIDATED_RESULTS.md` says the two tests compare against plain and against random ablation.
- *Fix:* Write "Holm p (vs plain / vs random ablation)".

**A-S15. L330 and L350: the family count is wrong for the combined result.**
- "15 models in four families" counts Qwen3 and Qwen2.5 as separate families.
- L350 says "With PREREG_H/I, this is the study's broadest behavioural result: four families". The union of PREREG_H/I and PREREG_L is 17 models in six families: Qwen3, Qwen2.5, OLMo-2, Falcon3, SmolLM3 and Granite.
- *Fix:* Give the correct union, or drop "With PREREG_H/I".

**A-S16. L336: "goal holding (P)" and "source sensitivity (A)" are never defined.**
- *Fix:* Define both as specified in PREREG_L. For example, P might be p_goal in the system cell and A the role spread.

**A-S17. L340: a "collapse" is mentioned that was never introduced.**
- "**The Qwen3-32B collapse replicates on fresh seeds**"
- *Fix:* "Qwen3-32B's weak goal holding (system-turn p_goal 0.34, §6b) replicates…"

**A-S18. L352: the §6f heading gives no verdict.**
- "is distinct from" is the authors' reading of the sealed verdicts H1 MIXED, H2 MIXED and H3 DOES_NOT_TRACK.
- *Fix:* Append "(H1 MIXED, H2 MIXED, H3 DOES_NOT_TRACK; PREREG_M)".

**A-S19. L371, L377, L379: internal process wording.**
- L371: "predictions and a Codex bet hashed before launch".
- L377: "The details are in MPILOT_RESULTS.md."
- L379: "matched the archived agp19 bundle… Codex reran the sealed analysis… Sources: cloud_prereg_m/m.json and m_descriptive_check.json". The second file is actually in `cloud_prereg_m/`.
- *Fix:* Write "predictions from two AI systems were hashed before launch". Move file names to the data section.

**A-S20. L383: the deixis sentence is hard to parse.**
- The sentence reads: "under +vR "I'll…" payloads are suppressed as much as other payloads or more: the most in Qwen3-4B, while in Qwen3-1.7B's system placement "You will" drops more (−0.83 vs −0.69). So the dial is pronoun-blind."
- "payloads" and "the dial" are never defined.
- *Fix:* Rewrite. For example: "Steering suppressed first-person commitments ("I'll…") at least as much as other commitments; its effect did not depend on the pronoun."

**A-S21. L387–389: the §8 heading overstates the result.**
- The heading is "Injection: role steering blocks it".
- The section's own 32-draw check says +vR's effect is "at the floor" in two placements and "only modestly beyond random" in the third.
- The preregistered test is called "inj2" only in §11.
- *Fix:* Retitle "role steering reduces it in one model (replication)", and name the test in §8.

**A-S22. L425: a number with no source.**
- "against +0.08 for goal obedience in the same model."
- No +0.08 appears for Qwen3-1.7B in §3. The values there are +0.005 (fixed text), +0.107 (weak text) and +0.11 or +0.18 (sequential instrument).
- *Fix:* Name the cell the +0.08 comes from.

**A-S23 [split]. L428 and L443 (also L5): Paper B is cited by name or filename only.**
- *Fix:* Add Paper B to the reference list with its title and a DOI or URL.

**A-S24. L436: "Every gate decision is preregistered" is not accurate.**
- Stages 1–3 used log gates without seals (L10).
- *Fix:* "preregistered or logged before data".

**A-S25. L489–490: wrong citation style, and sentences that read as notes to self.**
- Full titles and URLs appear inline, breaking the author–year style.
- Two sentences read as notes to self: "A new defence must compare against established interventions." and "Probe performance alone is not evidence of control."
- *Fix:* Cite as Zeng et al. (2026) and Balp-Straffon et al. (2026), and state how this paper relates to each.

**A-S26. L15 and L495: there is no public location for the data.**
- The text says the data "are in `research_next/agent_goal_persistence/`", which is a local folder path. No public repository or DOI is given.
- "`PREREG*.md` with `.sha256`" misses the INJ2_PREREG and ADDR_PREREG seals, which are also in the folder.
- *Fix:* Give the repository URL or the Zenodo DOI, and list every seal file.

**A-S27 [split]. L497–501: the cost paragraph mixes log detail with a figure that overlaps Paper B.**
- It contains log detail: "read 2026-10-29 at about 02:55 +04:00 (it lags about one hour)".
- "$75.3 for all cloud work through the end of PILOT_V1" also covers Paper B's work. Paper B claims $38 of it, and PILOT_V1 is a Paper B pilot.
- *Fix:* State Paper A's own share, or give one combined figure, labelled the same way in both papers.

**A-S28. L505: the AI-use statement has five gaps.**
- **(i)** The scope of the rechecks of "168 numeric claims" and "32 references" is unclear. The reference list has 34 entries. Sections added on 28–29 October (PREREG_I–M, MPILOT and RNDCTL) may not be covered.
- **(ii)** It does not credit the believe-versus-obey framing used in §10. Paper B attributes that framing to "an AI-written plan the author commissioned".
- **(iii)** `CONSOLIDATED_RESULTS.md` (L9) says "the user set the questions and the direction". This statement says Claude proposed the direction. Confirm which is correct.
- **(iv)** "the author's earlier papers" are not cited.
- **(v)** It does not say who designed and ran the fix-test pilot in Appendix A. It says only that Codex "recovered and computationally rechecked" it.
- *Fix:* State the scope of the rechecks precisely, and resolve (ii)–(v).

**A-S29. L507–546: Appendix A is disconnected and still contains log notes.**
- The main text never points to Appendix A.
- The fix-test pilot's task is not described. A reader cannot tell what "Plain system success" measures.
- The condition codes are undefined: emph, oldR2, user2, user4, orth2, pair2, random2.
- "PREREG_N" is undefined, and "is therefore **not launched**" is written in the present tense.
- Log details remain:
  - L528: "one cached Qwen3-1.7B model";
  - L544: the interruption and checkpoint notes;
  - L546: "saved in decomposition_pilot_codex… verdicts remain unchanged."
- *Fix:*
  - Point to Appendix A from §6b or §12.
  - Add a three-sentence description of the design and a legend for the codes.
  - Remove the log notes.

**A-S30. L550: a process note heads the reference list.**
- "Verified 2026-10-28 (`REFERENCES_VERIFIED.md` and its addendum)."
- *Fix:* Delete it.

**A-S31. References: ten entries are never cited, and four model families have no reference.**
- The ten uncited entries are:
  - Allal 2025 (L552)
  - Bakouch 2025 (L555)
  - G. & Lindsey 2026 (L558)
  - Holm 1979 (L560)
  - Hu 2022, LoRA (L561)
  - Leong C. T. 2025 (L563)
  - Liu R. 2025, DRIP (L566)
  - Martins 2024 (L569)
  - Yang 2024, Qwen2.5 (L578)
  - Zhan 2024, InjecAgent (L582)
- Qwen3, OLMo-2, Granite and Falcon3 are used throughout but have no entry here. Their references exist only in Paper B.
- `CONSOLIDATED_RESULTS.md` marks "From Simulation to Enaction" (G. & Lindsey) as "Unread".
- *Fix:*
  - Cite the model and method references at first use: Holm in §2, the models in §3, Qwen2.5 and Falcon3 in §6e, LoRA in §9.
  - Add the missing model references.
  - Drop G. & Lindsey, C. T. Leong, R. Liu and Zhan unless the text cites them.

### Nice-to-have

**A-N1. L19.** The abstract opens with "In this task," before any task has been introduced.

**A-N2. L41.** "erases 27–44% of the order": write "of the user − own spread" instead.

**A-N3. Repeated text.**
- Leong v2 is described three times in nearly the same words (L69, L148, L463–465).
- Tsui is described three times (L68, L447, L462).

**A-N4. L100.** "(EXPL., found late)": "found late" is unnecessary.

**A-N5. L111.** "all three preregistered directions": name the three.

**A-N6. L153 and L176.**
- L153: "stage-2" is internal jargon.
- L176: "A preregistered depth sweep (exploratory, …)" reads as a contradiction.

**A-N7. Section numbering.** The sections run 6, 6b–6f with no 6a. Consider 6.1–6.6, or 7–11.

**A-N8. L224.** The PREREG_G own-voice discount is a reported contrast without a gate. `CONSOLIDATED_RESULTS.md` labels it "EXPL. → replicated in PREREG_H". Label it the same way here.

**A-N9. L305.** "That makes 8 disagreeing pairs": list the eight (model × cue × role) so readers can check the count.

**A-N10. L306.** "In larger models, status acts through another route." Write "may act".

**A-N11. L356.** "because one model significantly goes the other way": write "goes in the predicted direction".

**A-N12. L358–365 (table).**
- It uses "percentage points"; the rest of the paper uses probability differences.
- It uses an ASCII hyphen "-" instead of "−".
- It writes "OLMo-2-1124-7B-Instruct" where the rest of the paper writes "OLMo-2-7B".
- It sorts 14B before 4B.

**A-N13. L369.** "J": write "PREREG_J".

**A-N14. L404–406.**
- "n 240" and "n 16" are numbers of training examples; say so.
- Pilot E3 is skipped without comment.

**A-N15. L472 and L480.**
- L472: a full stop appears mid-list.
- L480: "earlier behavioural work" has no citation.

**A-N16. Citation and reference style.**
- The same paper is cited as "Ye, Cui & Hadfield-Menell (ICML 2026)", "Ye et al." and "Ye et al. 2026".
- arXiv IDs appear inline in the text (L477, L485, L486).
- In the reference list, "pp." is used only for Zhan.
- Venue names are written inconsistently, for example "ICLR 2025" vs "International Conference on Learning Representations (ICLR 2022)".
- "G., A." looks like a malformed author name.

**A-N17. L577.** The entry reads "Xu, S., et al.", but `CONSOLIDATED_RESULTS.md` gives "Xu & Daneshjou". Check the author list.

**A-N18. Layout.**
- There are double blank lines at L430, L524 and L541.
- There is no blank line before "## 12." (L444).
- Appendix A sits between the AI-use statement and the references.
- Heading timestamps use two different formats (L511, L526).

**A-N19. L505.** "The study's direction, how agents keep or lose a goal and goal text given to the agent versus written in its own voice, was proposed by Claude": set off the description with a colon or dashes.

---

## Paper B: "Who said this?"

### Must-fix

**B-M1 [split]. Draft and process notes are visible to readers.**
- L3: "Paper B of two, split 2026-10-29 from the full technical report (`PAPER_DRAFT.md`, Draft 8)."
- L9: "§3.8 is being rechecked." This note may be out of date:
  - `NUMBERS_RECHECK_Y.md` is in the folder (I did not open it);
  - `CONSOLIDATED_RESULTS.md` cites "the recheck" for PREREG_Y's cost.
- L101: "These are pod-time figures, not yet reconciled with the billing explorer."
- *Fix:*
  - Delete the split note at L3, and cite Paper A formally.
  - At L9 and in the AI-use statement, either cite the finished §3.8 recheck or state plainly that §3.8 was not rechecked.
  - Reconcile the cost figures, or simply call them a pod-time estimate.

**B-M2 [split]. The introduction misreports the PREREG_W verdict.**
- L59: "Two exploratory claims did not replicate, and we report that (§3.2, §3.3)."
- §3.3 (L196 and L216–222) says 4 of 5 sealed predictions were SUPPORTED.
  - One of them is "obeying is read later" (W3). It passed by a bare majority.
  - Only "attribution never draws on the statement's own words" failed.
- *Fix:* "One exploratory claim (that attribution never uses the statement's own tokens) was refuted, and the obey-later lag holds in only a bare majority (4 of 7)."

**B-M3. The "May be new" list in §5 misstates two results.**
- L429: "in five of six models including two held-out families". In §3.6 the held-out Phi-4 is NONE, so only one held-out family (Granite) is selective. The abstract (L27–28) states this correctly.
- L431 [split]: "Its benchmark advantage holds in Qwen3-8B but not across families or at the other Qwen3 sizes".
  - The Discussion (L413) says "It beats every prompt defence on both benchmarks at 8B and 14B".
  - At 14B, X1–X4 all hold. Only the single-draw random control fails.
- *Fix:*
  - L429: "…in five of six models, including one of the two held-out families".
  - L431: "It passes every sealed check on both benchmarks only in Qwen3-8B. At 14B it beats every prompt defence but not its single random draw on InjecAgent. At 32B it ties the reminder on SEP."

**B-M4. Two citation problems.**
- L162: "Leong (2026: no abstract provenance code)".
  - Paper A (L69, L148, L463) says Leong v2's test "halted without interpretable evidence either way; v1 had claimed absence".
  - Paper B states the v1 claim, so the two papers contradict each other about the same source.
- L454: "Trained defences (StruQ, SecAlign, TrustAttention) and V-Steer were cited, not re-run."
  - StruQ and SecAlign appear nowhere else in the paper and are not in the reference list.
  - "V-Steer" is never linked to a reference. If it is Zeng et al. 2026, say so.
- *Fix:*
  - L162: "Leong (2026, v2: source-format cues are decodable; its test for an abstract provenance code was inconclusive)".
  - Add references for StruQ and SecAlign and name the reference for V-Steer, or remove the names.

**B-M5 [split]. Limitations list the other paper's experiments.**
- L455: "Except PREREG_J (50 directions)… That covers … the role-steering contrasts, PREREG_K and inj2."
- L456: "(RNDCTL, Qwen3-4B, in inj2's setup)".
- PREREG_J, PREREG_K, the role-steering contrasts and inj2 are all Paper A experiments. H4 and X5 are never defined in Paper B.
- *Fix:*
  - List only Paper B's controls: the PREREG_S edit, PILOT_V0, PREREG_V H4, and PREREG_X and PREREG_Y X5.
  - Describe RNDCTL as "a 32-draw check in a related injection setup (Qwen3-4B, 4-bit; Paper A, §8)".

### Should-fix

**B-S1. L6–7: the legend does not fit the pilot verdicts.**
- The legend says named verdicts are "preregistered and hash-sealed". FIRST_TOKEN_VALID (L271) and LEVER_FOUND (L278) are pilot verdicts and were not sealed.
- "EXPL.: exploratory, with no gate" also fits the pilots badly, because their rules were fixed before data (L98).
- *Fix:* Add a legend line for pilot verdicts.

**B-S2 [split]. L9: the rechecks are described as independent, and the record files are incomplete.**
- "Independent rechecks…": the AI-use statement calls them AI rechecks.
- Only `NUMBERS_RECHECK.md` is named. The folder also holds `NUMBERS_RECHECK_STU.md` and `NUMBERS_RECHECK_Y.md` (seen by name only).
- *Fix:* Write "AI rechecks", and cite the correct record files.

**B-S3. Title and L17: "no single tag" is stated as universal.**
- "There is no single "who said this" tag."
- Phi-4 is UNIFIED (L224). Of the 13 models evaluated, 12 are not unified.
- *Fix:* Write "Most models show no single tag", and soften the title to match.

**B-S4. L21 and L428: the sealed criterion is quoted incompletely.**
- Both say behaviours "read it at different depths in 9 of 10".
- The sealed W1 criterion is "different depths **or carriers**" (L218), and Granite was UNCLEAR.
- *Fix:* Add "or carriers".

**B-S5. L30–36: the abstract uses undefined labels and omits a caveat.**
- Y1, Y2, SEP_EFFECTIVE, EFFECTIVE, NONE and PREREG_Y are undefined.
- SEP and InjecAgent are not glossed.
- It does not say that Y1 PARTIAL is fragile. The pass rests on one item in 300 and holds in about half of bootstrap reseeds (L381).
- *Fix:* Rewrite in plain language and add the fragility note.

**B-S6. L51: Johnson et al. are misdescribed.**
- "Human memory research distinguishes several source-monitoring judgements, such as whether something was said, by whom, and whether to act on it (Johnson, Hashtroudi & Lindsay 1993)".
- Deciding whether to act is not one of Johnson et al.'s source-monitoring judgements. Their framework covers reality monitoring, internal source monitoring and external source monitoring.
- *Fix:* Write "such as whether something was perceived or imagined, and who said it". Present "whether to act on it" as this paper's extension.

**B-S7 [split]. L60: the sentence on Qwen3-8B points at the wrong test.**
- "It beats the baselines in Qwen3-8B but not across families."
- The sentence follows the claims about synthetic items. On synthetic items, Qwen3-8B did not beat the prompt defences (L306: no / no / yes); only Qwen3-1.7B and SmolLM3 did.
- *Fix:* "On the public benchmarks it beats all baselines only in Qwen3-8B".

**B-S8. L99: the re-runs are not disclosed where the text says.**
- "three operational re-runs … are disclosed where they occur"
- They appear only in §6 (L459), not in §3.7.
- *Fix:* Add one line to §3.7, or point to §6.

**B-S9 [split]. L101: the cost figures cannot be traced and overlap Paper A's.**
- "$56 … about $38 through PILOT_V1": the $38 does not appear in `CONSOLIDATED_RESULTS.md` or the draft. Only PREREG_Y's $18 does.
- The figure overlaps Paper A's "$75.3 for all cloud work through the end of PILOT_V1".
- "from pod-time records in the log" is internal wording.
- *Fix:* Make the two papers' cost statements consistent.

**B-S10. L140: the J-space terms and rule are not explained.**
- "J-space", "J-lens", "J_l" and "the September WikiText J-lens fit" are undefined.
- The OUTSIDE rule is not stated. From `CONSOLIDATED_RESULTS.md`, the threshold appears to be twice the random floor (0.0625). Without it, "0.050 against a random floor of 0.031" reads as if the source variation were inside the workspace.
- *Fix:* Add a one-sentence definition and the rule, and drop "September".

**B-S11. L164, L194, L427, L428: internal process notes.**
- The notes are "(prior-art check, 2026-10-28)", "The prior-art checks of 10-28 found…" and "The prior-art check found…".
- *Fix:* Write "To our knowledge, no earlier work…".

**B-S12. L192: figures are given as file paths only.**
- "**Figure.** `figures/prereg_t_sys_to_usr.png` and `figures/prereg_t_own_to_usr.png`."
- There is no embedded image, figure number or caption.
- *Fix:* Embed them as Figures 1 and 2, with captions.

**B-S13. L224: the list attaches to the wrong sentence.**
- "The exceptions are Phi-4, which is unified, and Granite, whose dissociation is unclear:" is followed by the list of general claims.
- As written, the list reads as describing Granite.
- *Fix:* Put the list first, then the exceptions.

**B-S14. L230: "ρ = −0.54 over 7 points" is unclear.**
- According to `CONSOLIDATED_RESULTS.md`, the seven points are lags for individual pairs, spread across five Qwen3 sizes.
- *Fix:* Say so.

**B-S15. L258: "the half rule" is never defined.**
- "so it fails the half rule"
- *Fix:* Define the rule in the PREREG_U design: the loss in belief must be less than half the drop in obedience.

**B-S16 [split]. L272: renumbering made a claim too broad.**
- "The first-token readout behind §3.1–§3.4 tracks generated behaviour."
- After renumbering, §3.1–§3.4 includes §3.3 (PREREG_W, ten other models). The four-model audit did not cover those models.
- *Fix:* "behind §3.1, §3.2 and §3.4 (the four audited models)".

**B-S17. L278–285: the lever search table leaves out key details.**
- The LEVER_FOUND pass rule is not stated, so readers cannot tell why OLMo's −0.053 "fails".
- `CONSOLIDATED_RESULTS.md` notes that the random direction "also passes" in Qwen3-1.7B (−0.125). The paper does not mention this.
- The column header "Random direction with own−tool's norm" conflicts with `CONSOLIDATED_RESULTS.md`, which says the random direction had the "same norm and settings" as the winning tool − user direction.
- *Fix:* State the rule, report the random direction's pass, and correct the header.

**B-S18. Several labels are used without definition.**
- "H3" (L319) and "H4" (L455): PREREG_V's hypotheses are never listed.
- "X2" and "X5" (L370–374).
- "Net" (L390).
- The verdict ladders SCALES / PARTIAL / NONE and SEP_BEATS / SEP_EFFECTIVE are only partly defined (L363–364, L379, L383).
- *Fix:* Define the hypothesis labels in each design paragraph.

**B-S19. L321: "every model we tested" is too broad.**
- "…lowers obedience to injected tool instructions in every model we tested."
- This holds for the six PREREG_V models, but not for the later tests:
  - Phi-4 on SEP: not significant;
  - OLMo and Granite on InjecAgent: not significant;
  - OLMo-2-13B: NONE.
- *Fix:* "in all six models of this test".

**B-S20. L332–341: InjecAgent results rest on small samples that are not reported.**
- InjecAgent attack success is computed on valid replies only. The paper never says so.
- The number of valid replies is small for some models. `CONSOLIDATED_RESULTS.md` gives 30 for Qwen3-1.7B, 77 for Granite and 98 for OLMo.
- Qwen3-1.7B's "57% → 3%" therefore rests on about 30 replies.
- *Fix:* Add a column for the number of valid replies, or a note.

**B-S21. L382 and L440: RNDCTL is cited without its caveat.**
- L382 cites RNDCTL for Qwen3-14B. It omits the caveat in `CONSOLIDATED_RESULTS.md`: the check ran in a different setup (Qwen3-4B, 4-bit, Paper A's injection test), "so it does not settle the question here".
- L440 counts RNDCTL as "what we add" in this paper, but it is a Paper A experiment.
- *Fix:* Add the caveat, and cite Paper A §8.

**B-S22. L404 vs L386: the two sections disagree about Phi-4.**
- L404: "It transfers to InjecAgent's embedded observations only within Qwen".
- L386: InjecAgent attack success fell "in 5 of 8 (the four Qwen models and Phi-4)".
- *Fix:* Note that Phi-4's cut matched its random draw (12%).

**B-S23. L416: a comparison is claimed that was not run.**
- "…directions fitted on injection episodes (CounterSteer…) or trained defences remain the better choice"
- Neither was run here (L454).
- *Fix:* "may be the better choice; we did not compare against them".

**B-S24. L427: the model count is vague.**
- "These behaviours rank the sources differently in most of 14 models"
- Obey and believe rankings exist for 13 models (4 + 9), and they disagree in 11.
- *Fix:* Give the exact count.

**B-S25. L448: the pointer to §3.3 finds nothing.**
- "a few curves failed the sanity check and were excluded (§3.3)"
- §3.3 never mentions this.
- *Fix:* Add the exclusions to §3.3. `CONSOLIDATED_RESULTS.md` lists them:
  - OLMo-32B attribute, own→usr;
  - OLMo-13B obey, own→usr;
  - Yi obey and believe, own→usr.

**B-S26. L464: there is no public location for the data.**
- The data location is a local folder path, with no repository URL or DOI. This is the same problem as A-S26.

**B-S27 [split]. L492: the AI-use statement refers to an unpublished draft.**
- "…expanded the prior-art comparison in the earlier full draft".
- Paper A says Codex also "revised" that draft. If any of the revised text is now in Paper B, the statement should say so.
- *Fix:* Write "in the combined technical report (ref)", and state Codex's role in this text.

**B-S28 [split]. L495: a sentence fragment and a count that does not match.**
- "re-ran the sealed analysis, which reproduced (6 mismatches and 8 overstatements, all fixed)" is a sentence fragment.
- "About 193" claims differs from the draft's "about 177 matched; 6 mismatches and 8 overstatements", which totals about 191.
- *Fix:* "…; the analysis reproduced. Six mismatches and eight overstatements were fixed." Reconcile the count.

**B-S29. References: one uncited entry, and Paper A is cited by filename.**
- G. & Lindsey 2026 (L507) is never cited. `CONSOLIDATED_RESULTS.md` marks it "Unread".
- Paper A is referenced only by filename (L3, L492).
- *Fix:* Drop G. & Lindsey, and add Paper A as a formal reference.

### Nice-to-have

**B-N1. L36.** "its single same-size random-direction control": write "same-norm".

**B-N2. Repeated text.**
- L51 and L107 repeat the Johnson et al. definition.
- L65–82 and L114–121 repeat the five sources and the readouts.

**B-N3. L128.** Qwen3-8B's belief in tool output is 0.66 here but 0.67 in `CONSOLIDATED_RESULTS.md`. Confirm which is correct.

**B-N4. L158.** "will leave the others … unchanged": write "may leave".

**B-N5. Notation.** "usr" (L171, L176, L185) vs "user" everywhere else.

**B-N6. L201–208.** The table is indented inside a list item and may not render in some Markdown-to-PDF tools.

**B-N7. L262.** "A generation-based check is needed before calling this a backfire.": add "(§3.5 performs it)".

**B-N8. Citation style.**
- L327–328 put a comma before the year: "(Zverev et al., 2025; …)" and "(Zhan et al., 2024; …)".
- L427 writes "Johnson et al. 1993"; elsewhere it is "Johnson, Hashtroudi & Lindsay 1993".
- L194 writes "C. T. Leong et al. 2025"; L428 writes "Leong et al. 2025".

**B-N9. Number format.** Attack-success percentages are whole numbers in §3.7 but have one decimal place in §3.8.

**B-N10. Valid-reply rate.** It is "about 30%" at L356 but "30–45%" at L409 and L453.

**B-N11. L414.** "Its InjecAgent advantage … from −0.38 at 1.7B to −0.06 at 32B": an advantage given as a negative number reads oddly.

**B-N12. L437 and L442.** "with no injection data": the direction was fitted without injection data, but it was selected on synthetic injection items (PILOT_V0). Write "fitted without injection data".

**B-N13. L449.** "The lever (§3.5–§3.7)": write "§3.5–§3.8".

**B-N14. Reference list.**
- Korznikov lists all six authors (L513); other entries use "et al.".
- "pp." appears only for Hines and Zhan.
- "G., A." looks like a malformed author name.

**B-N15. Layout.** There are double blank lines at L392, L425, L444, L461 and L489.

**B-N16. L84.** "All are … run in bf16", but RNDCTL (cited in §3.8, §5 and §6) used a 4-bit model that is not in the list. Attributing RNDCTL to Paper A solves this.

---

## Limits of this review

- I did not open `NUMBERS_RECHECK*.md`, `REFERENCES_VERIFIED.md`, `PLAN_7DAY.md`, the PREREG files or the result JSON files. For these I checked only that the names exist.
- I did not check any reference against arXiv or the venue pages.
- I opened nothing under `[private path removed]`, `[private path removed]` or any `research_loop/` folder.
- I checked numbers against `PAPER_DRAFT.md` and `CONSOLIDATED_RESULTS.md` only. Where those files disagree with a paper, the entry above says "confirm".
