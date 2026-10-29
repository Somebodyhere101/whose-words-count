# Pre-publication skim: does the reasoning hold? (2026-10-29)

This is one sceptical first read of each paper, as an ML researcher who knows interpretability and prompt-injection work would read them. Findings are listed most serious first.

**Overlap with the earlier review.** Findings already in `prepub_review.md` are not repeated. A few entries below touch the same sentence as an earlier item but raise a different problem. Those entries are marked "complements X".

**Line numbers.** The files were being edited while I read them, and lines have already moved by up to about 20. Each entry is therefore located by section and quote, not by line number.

**Data opened.** I opened data files only to settle a specific doubt:
- `PREREG_S.md` and `cloud_prereg_s/s_analysis.json` (B3, B12);
- `PILOT_V0.md` (B1);
- `PREREG_X.md` (B2, B7);
- `cloud_prereg_k/k.json` (A1).

Tags: **ERROR**, **UNSUPPORTED**, **UNCLEAR**, **WEAK**.

## The five most serious findings

1. **B1. The "map-guided" lever was found by a search, not by the map.**
   - The lever came from a 280-configuration search.
   - The patching map never measured the tool-versus-user contrast that the lever uses.
   - The one defence actually built from the map (§3.4) failed.
2. **B2. "Tool output" is a user turn that starts with "Tool output:", and SEP was put into the same wrapper.**
   - "The SEP effect generalizes" therefore describes transfer within the format the direction was built from.
   - InjecAgent is the only benchmark run in its own format, and there the lever fails outside Qwen.
3. **B3 and B4. The "no single tag" headline overstates the evidence.**
   - Only 2 of 4 models are FRAGMENTED on the behaviour criterion.
   - Qwen3-1.7B is counted as FRAGMENTED only because the ×1 edit did nothing.
   - The τ values over five sources have no CIs.
   - The paper's own map shows one common carrier that each behaviour reads differently. That fits a single tag with behaviour-specific weights just as well.
4. **A1. The ablation's "27–44% of the order erased" partly reflects a general loss of the reminder's effect.**
   - Competence falls by 22–36%.
   - Per unit of competence, the spread falls about 25% in Qwen3-4B and 8B, and not at all in Qwen3-32B.
   - The random-direction control does not lose competence, so it does not control for this.
5. **A2. "The informative part is user versus system" follows from how the role direction vR is built.**
   - Because vR = assistant − mean(system, user), user text lands below system text whenever the system-turn states lie closer to the assistant-turn states.
   - The ablation leaves most of the user − system gap intact.
   - Every model has the same order.

---

## Paper B: "Who said this?"

### B1. Title, abstract, §3.6 Reading, §3.7 Reading, §5. UNSUPPORTED

**Quotes:**
- Title: "a map-guided lever against injected instructions".
- §3.6: "located by the map and transferred without tuning".
- §5: "Its contribution is the map that located it".

**What is wrong:**
- The lever came from a 280-configuration search in PILOT_V0, scored on the same four models. The search covered 7 directions, depths 0.35–0.75, scales 1–8 and both token sets.
- The map patched only system→user and own→user pairs. "Tool" and "user" are both user turns (§2), so the map never measured the tool-versus-user contrast that the winning direction uses.
- The one defence actually built from the map, the §3.4 splice at the map's obey layer, failed (NONE).

**Fix:**
- Title: "…and a steering lever against injected instructions found by search".
- Abstract heading: "A map-guided lever" → "A steering lever found by search".
- §3.6 and §3.7: replace "located by the (source) map" with "found by a pre-specified search over source directions (§3.5)".
- §5: "The map suggested acting on the statement's own tokens. The direction, depth and scale were chosen by a search on four models. The contribution is the selective obey-versus-believe evaluation and its sealed tests."

### B2. §2, §3.7, §3.8 and the CounterSteer comparison in §5. UNSUPPORTED

**Quotes:**
- §2: "a user turn holding a tool output ("Tool output: …")".
- §3.7: "On SEP, whose untrusted data sits in a tool-output turn like our synthetic items".
- §3.8: "The SEP effect generalizes".

**What is wrong:**
- No model's own tool-message format is used anywhere. The "tool" source is a user turn that starts with "Tool output:".
- PREREG_X put SEP's data in exactly this wrapper: "the data in a user turn as 'Tool output:\n<data>'". The direction was computed from the same wrapper, so SEP tests new content in the training format. It is not a test of generalization.
- The InjecAgent contrast ("inside one long user message, not in a tool turn") is misleading, because SEP's data is in a user message too. The real difference is the wrapper.
- InjecAgent is the only benchmark run in its own format, and there the lever fails outside Qwen.
- The paper never says that SEP was rewrapped.
- §5 contrasts CounterSteer's "user-versus-tool role axis" with "our tool−user direction". This reads as if ours were also a role axis, but both of its ends are in the user role.

**Fix:**
- §2: "The tool-output and web-page sources are user turns that begin with a text prefix. No model's own tool-message format is used."
- §3.7: "For SEP we placed the data in the same 'Tool output:' user turn that was used to build the direction. InjecAgent keeps its own ReAct format."
- §3.8: "The SEP effect carries over to new content in the training wrapper. On InjecAgent, which keeps its own format, the effect is mostly confined to Qwen."
- Limitations: "Models' own tool-message formats were not tested."

### B3. Abstract and §3.1. UNSUPPORTED

**Quote:** "obeying and believing rank the five sources differently (Kendall τ 0.2–0.4). The sealed verdict is FRAGMENTED: 3 of 4 models, with OLMo PARTIAL."

**What is wrong:**
- Under the sealed rule (`s_analysis.json`), only Qwen3-8B and SmolLM3 are FRAGMENTED on the behaviour criterion (τ 0.2).
- Qwen3-1.7B (τ 0.4) is MIXED on that criterion. It counts as FRAGMENTED only because the ×1 edit moved nothing (rule d), a null that §3.2 attributes to the edit's depth and size.
- OLMo avoids FRAGMENTED by narrow margins: attribution 0.3245 against a cut-off of 0.30, plus a +0.004 shift in obedience.
- With five sources there are only ten pairs, so τ moves in steps of 0.2 when one pair changes order. FRAGMENTED, MIXED and UNIFIED are each one swapped pair apart, and no CI is reported.

**Fix:**
- §3.1: "Behaviour verdicts: FRAGMENTED in Qwen3-8B and SmolLM3 (τ = 0.2), MIXED in Qwen3-1.7B and OLMo (τ = 0.4). Qwen3-1.7B's FRAGMENTED headline comes from the null ×1 edit."
- Report an item-bootstrap CI for each τ.
- Abstract: "In two of four models the obey and believe source orders are nearly unrelated (τ = 0.2); in the other two they are weakly related (τ = 0.4)."

### B4. Title, abstract and §4 (also Paper A §10). UNSUPPORTED (complements B-S3)

**Quotes:**
- Abstract: "There is no single "who said this" tag."
- §4: "Provenance is several readouts, not one tag."
- §4: "The role-marker tokens are the common carrier, but each behaviour consults them differently."

**What is wrong:**
- Obeying and believing could rank the sources differently even if the model had one shared five-way source code that each behaviour weights differently. That is what the paper's own map shows: one common carrier, read differently. The test therefore rules out a single shared ordering of sources, not a single tag.
- Obeying and believing are measured on different items (instructions versus facts). An interaction between item content and source could produce the rank difference on its own.

**Fix:**
- Title: "Chat models weight a text's source differently for each behaviour".
- Abstract heading: "No single source ordering across behaviours".
- §4: "Provenance is one carrier read in several ways."
- Add to Limitations: "Obeying and believing are measured on different item types."
- Paper A §10: "which supports separate readouts" → "which shows that obeying and believing weight sources differently".

### B5. §3.2 and §4. UNSUPPORTED

**Quotes:**
- §3.2: "This may explain PREREG_S's null for obedience (untested). Its mean-vector edit was added at the decision layer, before the obey content phase, and at natural size."
- §4: "The lever acts on the statement's own tokens, near the depth where obeying draws on them."

**What is wrong:**
- In the Qwen models, PREREG_S's decision layer is at 0.46 depth (layer 13 of 28) and 0.47 (layer 17 of 36). That is the lever's depth (0.45), which is also below the obey content peak (0.5–0.8, §3.3).
- Depth therefore cannot explain why the ×1 edit failed and the lever works. What differs is size (×1 versus ×4) and direction, so the two explanations contradict each other.

**Fix:**
- §3.2: "The null may reflect the edit's size: in the Qwen models the lever (§3.5) acts at the same depth at four times the size (untested)."
- §4: "…at about 0.45 depth, below the obey content peak. Why the amplified vector works where the ×1 edit did not is untested."

### B6. Abstract, §3.7 and §3.8. UNSUPPORTED

**Quotes:**
- Abstract: "In Qwen3-8B the lever beat every prompt defence on SEP (attack success 30% → 14%) and InjecAgent (39% → 12%)".
- §3.8: "Only Qwen3-8B passes every check".

**What is wrong:**
- Qwen3-8B is one of the four models the recipe was selected on (PILOT_V0).
- In PREREG_X, the only two models that did not get NONE (Qwen3-8B and Qwen3-1.7B) are both selection models. Both held-out families (Granite, Phi-4) got NONE.
- The abstract's lead benchmark result is therefore in-sample. Only §6 says so, and only in general terms.

**Fix:**
- Abstract: "In Qwen3-8B, one of the four models the recipe was chosen on, the lever beat…".
- §3.7 Reading: "The two models that did not get NONE were both selection models; both held-out families got NONE."

### B7. §3.7 heading, "What generalizes" and the results table. UNSUPPORTED

**Quotes:**
- "**What generalizes.**"
- Table row: "| SmolLM3-3B | 42% → 25% | 4% → 1% (floor) | none |".

**What is wrong:**
- PREREG_X fixed in advance how an overall NONE would be read: "the effect on synthetic items does not carry over to real injections". The paper leaves this out and leads with "What generalizes".
- The table gives "none" for SmolLM3, Granite and OLMo-2-7B. Yet these three models beat every prompt defence on SEP, and the table does not explain the label.
  - The per-model verdict required X1, X3 and X5 on both benchmarks.
  - SmolLM3's InjecAgent baseline is 4%, too close to the floor for it to pass.

**Fix:**
- Add: "PREREG_X fixed the reading of NONE before data: the effect on synthetic items does not carry over to real injections. The SEP results below are descriptive."
- Rename the column to "Sealed verdict (requires both benchmarks and the random control)".
- Add a footnote on SmolLM3's floor.

### B8. §4, practical upshot. ERROR (complements B-S23)

**Quote:** "In other families, prompt defences, directions fitted on injection episodes (CounterSteer; Russinovich 2026) or trained defences remain the better choice, and some prompt defences backfire."

**What is wrong:**
- On SEP the lever beat all three prompt defences in three non-Qwen models (OLMo-2-7B, SmolLM3 and Granite; §3.8). It matched the best prompt defence in the four PREREG_Y held-out models.
- The backfires the paper reports are all in Qwen models (§3.4, §3.6), not in other families.

**Fix:** "In other families the lever matches or beats prompt defences on SEP but does little on InjecAgent, where prompt defences are at least as good. The prompt defences that backfired did so in Qwen."

### B9. Abstract and §3.5. UNSUPPORTED

**Quotes:**
- Abstract: "Prompt defences did as well in some families and backfired in others."
- §3.5: "This confirms the §3.4 first-token observation, so it is not a readout artifact."

**What is wrong:**
- The §3.5 "confirmation" is untested pilot data (Qwen3-8B: 0.417 → 0.479).
- The sealed PREREG_V rerun found Qwen3-8B's rise non-significant (+0.062, §3.6).
- Under the generation readout, a significant backfire is shown in one model of one family (Qwen3-1.7B), not "in others".

**Fix:**
- Abstract: "…did as well in some families and raised obedience in Qwen3-1.7B."
- §3.5: "The generation readout shows the same sign in both Qwen models (untested here). In the sealed test the rise was significant only in Qwen3-1.7B (§3.6)."

### B10. Abstract and §3.6. WEAK

**Quote:** "It was selective, keeping belief in the tool's facts, in 5 of 6."

**What is wrong:**
- The selectivity rule lets belief fall by up to half as much as obedience.
- Belief fell by 0.090 in Qwen3-8B and by 0.097 in SmolLM3, which is 38% and 27% of their obedience drops. "Keeping belief" overstates this.

**Fix:** "It was selective in 5 of 6: belief in the tool's facts fell by at most 0.10, less than half the drop in obedience."

### B11. §1 contributions and §3.1. UNSUPPORTED

**Quote:** "behaviour does not track reportable source knowledge"

**What is wrong:**
- The only evidence is that two models with a mean attribution of 0.32 (above chance) still show source effects. No per-source relation between attribution and behaviour is tested.
- The five-way lettered attribution readout was never validated: the §3.5 audit covered only obeying and believing. Small models are weak at lettered multiple-choice questions, so low scores may reflect the format.

**Fix:**
- "Source effects on behaviour occur even in models that attribute sources poorly in a five-way lettered question (OLMo and SmolLM3: 0.32; chance 0.20)."
- Add to Limitations: "The attribution readout was not checked against generation."

### B12. §3.1 results. UNCLEAR

**Quote:** "Qwen3-8B obeys the user most (0.53) and its own earlier turn least (0.25)"

**What is wrong:**
- The competing message is always a user turn (§2; PREREG_S). The user cell is therefore user against user, with both orders averaged, and sits at about 0.5 by construction.
- Readers will take 0.53 as weak obedience to the user. Every score is measured against this 0.5 baseline, and the paper never says so.

**Fix:**
- In §2 Readouts: "The competing message is always a user turn, so 0.5 means the statement and the competitor are followed equally often. The user cell is about 0.5 by construction."
- Rewrite the result as: "In Qwen3-8B no source beats a competing user message (all scores < 0.5); its own earlier turn loses most often (0.25)."

### B13. Abstract and §3.2. UNCLEAR

**Quotes:**
- Abstract: "the role-marker tokens carry the source (92% of informative curves)".
- §3.2: "maximum C transfer 0.38–1.33".

**What is wrong:**
- In a role-word minimal pair, the role word is the only difference in the input, so at early layers the marker must carry the source. Stated on its own, the 92% figure reads as trivial.
- The non-trivial finding is that the difference stays on the role-marker tokens and is not copied onto the statement's own tokens before the handoff.
- Transfer values above 1 (1.33) are not explained.

**Fix:**
- Abstract: "Until mid-depth the source difference stays on the role-marker tokens rather than being copied onto the statement's own words (92% of informative curves)."
- §3.2: define transfer, and add "Values above 1 mean that patching only the statement's tokens overshoots the donor."

### B14. §1, the problem. WEAK

**Quote:** "Most of them implicitly treat a span's source as one label that the model carries and a defence can strengthen or rewrite."

**What is wrong:**
- This is the paper's motivating premise, asserted about "most" defences without evidence.
- Datamarking and hierarchy training do not presuppose a single internal label, so the sentence reads as a straw man.

**Fix:** "Several steering defences act along a single role or user-versus-tool direction (Liu 2026; Zhang, Lee & Park 2026). This presumes that one internal source signal drives obedience."

### B15. §3.8 results. WEAK

**Quote:** "Utility held in every model. The largest change was −3.3 points in InjecAgent's valid-reply rate"

**What is wrong:**
- InjecAgent's valid-reply rate measures output format, not usefulness.
- Per-model SEP utility is shown only for Qwen3-8B (65% → 68%).

**Fix:**
- "SEP utility and InjecAgent's valid-reply rate fell by at most 3.3 points in every model."
- Add a SEP-utility column to the §3.7 and §3.8 tables.

---

## Paper A: "Whose words count?"

### A1. Abstract and §6d. UNSUPPORTED

**Quotes:**
- Abstract: "Removing the direction erases 27–44% of the order in three Qwen models".
- §6d: "while the goal is still pursued: competence stays at 64–95% of plain".

**What is wrong:**
- The ablation also weakens the reminder overall, and that alone shrinks every gap. From `cloud_prereg_k/k.json`:

  | Model | Competence lost | Spread lost | Spread per unit of competence |
  |---|---|---|---|
  | Qwen3-4B | 22% | 42% | falls about 25% |
  | Qwen3-8B | 24% | 44% | falls about 25% |
  | Qwen3-32B | 36% | 27% | rises 14% (0.97 → 1.11) |

- The random-direction ablation leaves competence unchanged (0.553, 0.706 and 0.332, against 0.562, 0.706 and 0.338 without ablation), so it does not control for this.

**Fix:**
- Report the spread as a share of competence next to the raw figure.
- Reword: "Removing the direction narrows the user − own spread by 42–44% in Qwen3-4B and 8B, about 25% beyond the general loss of the reminder's effect. In Qwen3-32B it narrows the spread by 27%, but the reminder's overall effect falls by more (36%)."

### A2. §6b and §12 contribution 4. UNSUPPORTED (complements A-S10)

**Quotes:**
- "The direction was built only from own-vs-given neutral sentences, so it carries no built-in user-versus-system difference."
- "**The informative part is user versus system.**"

**What is wrong:**
- Let a, s and u be the mean states of neutral sentences in the assistant, system and user turns. The direction is vR = a − (s + u)/2, and for these means:
  - proj(s) − proj(u) = (|a − u|² − |a − s|²)/2.
- So user text lands further toward "given" exactly when system-turn states lie closer to assistant-turn states. That is a fact about how the roles are laid out in activation space, not an independent prediction.
- §6d shows that removing the direction leaves most of the user − system gap. Every model also shows the same order, so a constant would "predict" it equally well. (A-S10 proposes the word "predicts".)

**Fix:**
- §6b: "The direction also places user text further from the assistant end than system text, as it must whenever system-turn states lie closer to assistant-turn states. This matches the behavioural order in all 9 models. But every model shares that order, and removing the direction leaves most of the user − system gap (§6d), so the match is correlational."
- §12: "predicts" → "matches".

### A3. §4. UNSUPPORTED

**Quotes:**
- "Role and attribution are encoded separately."
- Heading: "no abstract "this is mine" tag (FAIL, log gate, Qwen3-1.7B; no transfer in 9 more models)".

**What is wrong:**
- In Qwen3-1.7B the probe transferred at AUC 0.80 and 0.796 (the bar is 0.8). It beat the control by 0.12 (the bar is 0.15). That shows substantial shared structure that is not specific to the self, not separate encoding.
- In the other nine models the control transferred as well or better, which is not the same as "no transfer".
- The abstract's hedge ("does not establish that none exists") is the right reading. §4 contradicts it.

**Fix:**
- Replace the sentence with: "The shared signal is not specific to own-versus-given: a system-vs-user probe transfers about as well."
- Heading: "no evidence for a self-specific 'this is mine' tag (FAIL, log gate, Qwen3-1.7B; the control transfers as well in 9 more models)".

### A4. §1 and §6. UNSUPPORTED

**Quotes:**
- §6 heading: "the discount arrives with chat fine-tuning".
- §1: "a training-stage origin".
- §6: "No result supports a preference-tuning origin."

**What is wrong:**
- Base models could not do the task ("a pretraining origin could not be tested"), so SFT is the first checkpoint that can be tested. Presence at SFT does not show that the discount arrived at SFT.
- The sealed 13B verdict was H-pref (a preference-tuning origin). "No result supports" overrides it without saying so.

**Fix:**
- Heading: "Origin: the discount is present at the first testable stage (SFT)".
- §1: "its presence at the earliest testable training stage".
- §6: "The 13B verdict (H-pref) rests on a flat gap of 0.007–0.008 that crossed p < 0.01 only at the last stage. We do not read it as a preference-tuning origin."

### A5. Abstract, §3 and §6b. UNSUPPORTED (complements A-M3 and A-S3)

**Quotes:**
- §3: "| Qwen3-1.7B | +0.005 | weak text: +0.107 (40/40) |".
- §6b: "in line with the Qwen scale trend in §3", against §6e: "it is a property of that model".

**What is wrong:**
- Even as an exploratory observation, the trend is confounded by how much room each model leaves for a gap.
  - At 1.7B the fixed reminder drives p_hi to the floor (gF 0.041, oF 0.046). With the weak text, the same model's gap is +0.107, close to 14B's +0.110.
  - The top of the trend is Qwen3-32B, which §6e calls idiosyncratic but §6b cites as support.
- Qwen3-4B was run in 4-bit, so the series also mixes precisions.

**Fix:**
- Report each gap together with its given-cell level, or as a share of p(1) − p(gF).
- Drop "in line with the Qwen scale trend in §3" from §6b, or reconcile it with §6e.
- §3 reading: "At 1.7B the fixed text is at the floor; with the weak text the gap is +0.107."

### A6. §2, construct caveat. UNSUPPORTED

**Quote:** "All own-vs-given comparisons hold the reminder text fixed and vary only its role, so they remain comparisons of authority."

**What is wrong:**
- Holding the text fixed shows that the role matters. It does not show that the mechanism is authority.
- The measure partly captures resistance to pressure: OLMo's reminder raised high-emission picks from 0.088 to 0.277 when the pressure agreed with the goal. The role could therefore change how strongly the reminder pushes against pressure, rather than the goal's authority.

**Fix:** "…so they compare the same text across roles. Whether the role changes the goal's authority or the reminder's push against pressure is separated only in the cleaner world of §6b."

### A7. §5, reading. UNSUPPORTED

**Quote:** "The causal *sign* holds in all four families, with every beyond-random test at p_Holm 0.00015."

**What is wrong:**
- Each p-value compares the direction with one fixed random draw. It reflects seed noise, not variation across random directions.
- The paper's own RNDCTL check (in a different task) found that random draws vary with a standard deviation of 0.13–0.22. That is larger than the margins over random outside Qwen (Granite +0.038; OLMo +0.053 and +0.074).
- This caveat appears only in Limitations, not where the claim is made.

**Fix:** "The predicted sign holds in all four families. Each beyond-random test uses one random draw (p_Holm 0.00015 against that draw). Outside Qwen the margins (+0.04 to +0.13) are within the spread of random directions seen in RNDCTL, so specificity there is untested."

### A8. Abstract, §7 and §12. WEAK (complements A-S20)

**Quote:** "A first-person (deixis) account is refuted."

**What is wrong:**
- The test used two small Qwen3 models and one direction.
- §7 never describes the design, for example what a "payload" is or what is measured.
- The result is mixed: "I'll" is suppressed most in Qwen3-4B, but "You will" drops more in one placement in Qwen3-1.7B.

**Fix:**
- "A first-person (deixis) account was not supported in two small Qwen3 models."
- Add one sentence on the design to §7.

### A9. §3, reading. UNSUPPORTED

**Quote:** "In every model that can do the task, the agent's own notes drift far more than a fixed reminder."

**What is wrong:**
- Note-cell values are shown only for Qwen3-1.7B (gN 0.82 and oN 0.84, against gF 0.041).
- The comparison changes the content as well as the role: the agent-written notes lack the action rule. It therefore says nothing about whose voice the text is in.

**Fix:** Give the note-cell values for each model, or write: "In Qwen3-1.7B, the agent's own notes (a different text) drift far more than the fixed reminder."

### A10. §3–§6f, sign conventions. UNCLEAR

**Quotes:**
- §6: "uF − gF is between −0.05 and −0.12, p 0.0001".
- §6b: "projection and adherence correlate positively in Qwen3-14B … and negatively in OLMo".

**What is wrong:**
- The outcome measure changes direction without warning:
  - p_hi (lower = more adherent) up to §6;
  - p_goal (higher = more adherent) from §6b;
  - percentage points of "other minus self" in §6f.
- The §6b correlation sentence never says which sign the axis predicts, so readers cannot tell whether OLMo agrees or disagrees.

**Fix:**
- Put the measure and its direction in every table header, for example "own − given in p_hi (positive = own followed less)".
- §6b: "…correlate in the predicted direction in Qwen3-14B…".

### A11. §6c. WEAK

**Quote:** "**Authority and consensus split by model size.**"

**What is wrong:** The test used seven models. The "small" group (Qwen3-1.7B, Qwen3-4B and SmolLM3) is mostly Qwen, while the "larger" group contains the only OLMo and Granite models, so size and family are confounded.

**Fix:** "Authority and consensus split between the three smallest models and the four larger ones. With seven models, size and family cannot be separated."

### A12. Abstract and §9. WEAK

**Quote:** "and they raise susceptibility to forged assistant-turn injections."

**What is wrong:** The increases (+0.012 to +0.085 in the pilots, +0.04 to +0.07 in PREREG_F) come with no test or interval, yet the abstract presents them as a finding.

**Fix:** Give a CI or p-value, or write: "and in every adapter tested, forged assistant-turn injections succeeded slightly more often (+0.01 to +0.09; not tested for significance)."

### A13. §6, descriptive reading. UNCLEAR

**Quote:** "Relative to the reminder's effect, the discount is *largest* after SFT: 0.133, against 0.106 after DPO."

**What is wrong:** The raw gap rises across stages (0.063 → 0.071 → 0.077), while the relative gap falls. The paper reports only the measure that supports "largest after SFT", and leaves out the value after Instruct.

**Fix:** "The raw gap rises slightly (0.063 → 0.071 → 0.077), while the gap relative to the reminder's effect falls (0.133 after SFT, 0.106 after DPO, [value] after Instruct)."

### A14. §9, reading. UNCLEAR

**Quote:** "The cut is about three quarters with 240 training examples and 20–38% with 16–48."

**What is wrong:** The E1–E2 pilots with 240 examples cut drift from 0.857 to 0.03–0.06, about 95%. "About three quarters" matches only PREREG_F (0.206–0.229).

**Fix:** "about three quarters in PREREG_F (balanced data, 240 examples). The unbalanced pilots reached the floor by learning to oppose the pressure."
