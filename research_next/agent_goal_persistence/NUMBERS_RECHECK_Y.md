# PREREG_Y numbers recheck (independent, adversarial)

Done 2026-10-29, 10:27–10:57 +04:00. Report only: no file in the research folder (RF) was edited. Nothing under `[private path removed]`, `[private path removed]` or `research_loop/` was opened. No GPU, network or installs were used.

RF = `C:\Users\caabm\AppData\Roaming\Claude\scratch-workspaces\2898f83d-79d0-4cb9-a017-7d323d549974\0c4963d8-51ed-4ceb-9445-28b8639f6fa1\scratch-2026-10-13-464f6a\research_next\agent_goal_persistence\`

**Versions checked.** The claim files were edited while I worked: the RNDCTL single-draw edit at 10:29:51, and a reference-line edit at 10:34:56. I checked the final versions, copied to `scratchpad\recheck_y\snap2\`. The md5s were unchanged at 10:56.

| File | md5 | mtime |
|---|---|---|
| `PAPER_B_SOURCE_MONITORING.md` | 37fd23bfc986bae69a42f1c3e0c33d5a | 10:34:56 |
| `PAPER_DRAFT.md` | b4435307f307016fbcbf2c45a7fdcf02 | 10:34:56 |
| `CONSOLIDATED_RESULTS.md` | 509b25b81b3b6fa6df63203a817f5129 | 10:29:51 |

Paper B §3.8 and PAPER_DRAFT §6n have identical text (diffed, ignoring blank lines). Their claims are counted once below, and each finding applies to both files.

## Summary

- **Seal: reproduced.** `sha256sum -c PREREG_Y.sha256` gives 18/18 OK from a clean extract of `agp30.tgz`. The RF working copies are also 18/18 OK.
- **Re-run: reproduced.** The sealed `y_analyze.py` output is byte-identical to the stored `y_analysis.json` (sha256 fcb53777…14a5; md5 8bd9a033…). `x_analyze.py` on the same data is byte-identical to `x_style_analysis.json`.
- **Independent recomputation:** I re-implemented the rates from the raw files with exact fractions. Every rate in `y_analysis.json` is reproduced: 8 conditions × 6 models on SEP, and 8 × 2 on InjecAgent.
- **Claims: 87 checked.** 69 MATCH, 7 ROUNDING, 5 MISMATCH (3 distinct issues), 6 UNVERIFIABLE.
- **Flags:** 6 overstatements, 4 wording or ambiguity notes, 1 labelling omission and 3 robustness notes.
- **No sealed verdict changes.** Y1 = PARTIAL, Y2 = SEP_EFFECTIVE, and every per-model verdict and hypothesis pass/fail is reproduced.
- **Robustness caveat:** Y1 = PARTIAL rests on a one-item margin (R1).

## 1. Seal and bundle log

```
bundle  RF\bundles\agp30.tgz  md5 28b86845a2ef96e451be2fe396a7d79b  sha256 3f997be600df99510fc3549907d5c6a8935da51c29fb387f1f8251b898458dc4
$ mkdir scratchpad\recheck_y && tar -xzf agp30.tgz -C scratchpad\recheck_y          (fresh, empty folder)
$ cd recheck_y\agp30 && mkdir cloud && cp code\rc33.sh code\ss33.sh code\rc34.sh code\ss34.sh cloud\
$ sha256sum -c PREREG_Y.sha256
PREREG_Y.md: OK            recipe.json: OK               code/bench.py: OK          code/x_analyze.py: OK
code/y_analyze.py: OK      cloud/rc33.sh: OK             cloud/ss33.sh: OK          cloud/rc34.sh: OK
cloud/ss34.sh: OK          data/injecagent_prompts.json: OK  code/lever_pilot.py: OK  code/src_defense.py: OK
code/src_patch_w.py: OK    code/src_patch.py: OK         code/src_monitor.py: OK    code/agp_batch.py: OK
code/agp_b.py: OK          code/chat_fmt.py: OK          -> 18/18, exit 0
```

- The bundle's `PREREG_Y.sha256` and `PREREG_Y.md` are byte-identical to the RF copies. The RF `cloud\rc33/ss33/rc34/ss34.sh` are byte-identical to the bundle's `code\` copies.
- **PREREG_X code byte-identical:** the 12 shared code and data files in `agp30` match `PREREG_X.sha256` (12/12 OK). They are also byte-identical to the `agp28` bundle. `rc31.sh` and `ss31.sh` are PREREG_X run scripts and are not reused.
- **RF working copies:** `sha256sum -c PREREG_Y.sha256` run inside RF (read-only) also gives 18/18 OK.

## 2. Re-run log

```
$ cd scratchpad\recheck_y\agp30\code
$ C:/Users/caabm/Documents/agp-env/.venv/Scripts/python.exe y_analyze.py --root RF/cloud_prereg_y_all/out_y > ..\..\y_rerun.json
  Python 3.12.14, numpy 2.5.4; exit 0; stderr empty; 0.8 s
  sha256 fcb5377792f2e8fc4508f4920fc92b3ec1dd065e600c46fee7bd17a532cd14a5  y_rerun.json
  sha256 fcb5377792f2e8fc4508f4920fc92b3ec1dd065e600c46fee7bd17a532cd14a5  RF\cloud_prereg_y_analysis\y_analysis.json   -> BYTE-IDENTICAL
$ ... x_analyze.py --root RF/cloud_prereg_y_all/out_y > ..\..\x_style_rerun.json   -> byte-identical to x_style_analysis.json (md5 bfbf6f16…)
```

### Provenance of the combined raw folder

- **Fetched archives:**
  - `results33.tgz` has md5 ee26efedb0e8f23847f6e2fa12628bab, and `results34.tgz` has md5 1d3acd950d7dbe47d2a1720e0f907f27.
  - Both match the PLAN_7DAY entries of 2026-10-29 at 09:55 and 10:30.
  - Both match the unpacked `cloud_prereg_y\out_y` and `cloud_prereg_y_b\out_y` folders.
- **Combined folder:** all 8 study JSONs in `cloud_prereg_y_all\out_y` are byte-identical to the archive members. Seven come from part A; `Qwen3-32B\injecagent.json` comes from part B. Part B's three log files were not copied into the combined folder; they are still in `cloud_prereg_y_b\out_y`.
- **Raw metadata** (all as sealed):
  - model ids as in the preregistration;
  - layer = round(0.45 × n_layers): 18/40, 29/64 and 22/48;
  - seed 2800; max_new 128 (SEP) and 160 (InjecAgent);
  - recipe tool-usr, depth 0.45, scale 4, tokens C;
  - 8 conditions; 300 items or cases; no missing SEP scores.
- **Same samples as PREREG_X:** the SEP item keys and InjecAgent case keys are identical to those in PREREG_X's raw Qwen3-8B files.
- **Run logs:**
  - `last_status` (A): every SEP run at batch 32, including Qwen3-32B; Qwen3-14B InjecAgent at batch 8; ERRS 0.
  - B: batch 8, ERRS 0.
  - No `*_oom_attempt1.txt` exists.
  - `bench.py` RND is one `torch.randn` draw, seeded 2800 + layer and scaled to ‖v‖: a single same-norm draw.

## 3. Mismatches

**M1. "It beats every prompt defence on both benchmarks only at 8B."**
- **Where:**
  - Paper B §4, line 409;
  - CONSOLIDATED line 581 ("It beats every prompt defence on both only at 8B").
- **Evidence:** Qwen3-14B passes both X2 and X4 (`y_analysis.json` y1.Qwen3-14B.hyp: X2 true, X4 true).

  | Benchmark | P | SPOT | REMIND | Other conditions |
  |---|---|---|---|---|
  | SEP, CI of Net(DEF) − Net(X) | [0.17, 0.3067] | [0.0167, 0.1567] | [0.11, 0.2133] | |
  | InjecAgent, CI of ASR(DEF) − ASR(X) | [−0.3071, −0.1985] | [−0.2481, −0.1489] | [−0.2167, −0.1255] | validity guards met |

  - Over PREREG_X and Y, the models with X2 and X4 both true are Qwen3-8B and Qwen3-14B.
  - 14B's only failure is X5, the single random draw on InjecAgent.
  - CONSOLIDATED contradicts itself at lines 568–570: "X1–X4 all hold … beating all three prompt defences".
- **Suggested wording:** "It beats every prompt defence on both benchmarks at 8B and at 14B; only at 8B does it also beat its single random draw on both (at 14B the draw matched it on InjecAgent)."

**M2. "… on InjecAgent in 4 of 8, all of them Qwen."**
- **Where:** Paper B §3.8 line 386, which is the same text as PAPER_DRAFT §6n line 672.
- **Evidence:**
  - Both counts are right. SEP X2 is 5 of 12 and InjecAgent X4 is 4 of 8.
  - "all of them Qwen" is true only for the InjecAgent four (Qwen3-1.7B, 8B, 14B, 32B).
  - The five SEP models are Qwen3-8B and Qwen3-14B plus three non-Qwen models: OLMo-2-7B, SmolLM3-3B and Granite-3.3-8B (`x_analysis.json` hyp.X2 true).
  - Read naturally, the sentence says the SEP advantage was Qwen-only, which is false.
- **Suggested wording:** "It beat all three prompt defences on SEP in 5 of 12 models (Qwen3-8B, Qwen3-14B, OLMo-2-7B, SmolLM3-3B and Granite-3.3-8B, but none of the four held-out models) and on InjecAgent in 4 of 8, all of them Qwen."

**M3 (minor, stale). Data and code lists omit PREREG_Y.**
- **Paper B line 460:** "sealed preregistrations (`PREREG_S` to `PREREG_X` …)". The table two lines below includes PREREG_Y.
- **Paper B line 462 and PAPER_DRAFT line 860:** "The PREREG_V, W and X analyses were run from the bundle's own copy, after the working files were checked against the seal". PREREG_Y's analysis was also run this way (`y_finish.sh`; reproduced here, with RF working files 18/18).
- **PAPER_DRAFT line 860** heads this block "(§6g–§6m)", which excludes §6n.
- **Suggested wording:**
  - "`PREREG_S` to `PREREG_Y`";
  - "The PREREG_V, W, X and Y analyses …";
  - "(§6g–§6n)".

## 4. Overstatements and labelling

**O1. Abstract (Paper B line 34): "In Qwen3-14B and Qwen3-32B the steering stayed effective and additive."**
- The lead-in is "A sealed follow-up … gave", but Qwen3-14B's sealed verdict is NONE.
- "Effective" reads as the EFFECTIVE verdict, which is the paper's own vocabulary, so the wording is stronger than the sealed result.
- Additive is right: both are ADDITIVE.
- **Suggested wording:** "In Qwen3-14B and Qwen3-32B the steering still cut attack success on both benchmarks and stacked with prompt defences (ADDITIVE). The sealed verdicts were EFFECTIVE at 32B and NONE at 14B, where it beat every prompt defence but not its single random draw on InjecAgent."

**O2. §1 contributions (Paper B line 60): "Larger Qwen3 models and four held-out models confirm the effect but not the advantage."**
- **"Confirm the effect":**
  - The drop in attack success replicates: X1 6/6 and X3 2/2.
  - The sealed effect verdicts hold in 4 of 6: 32B EFFECTIVE, and Falcon3, Yi and OLMo-2-32B SEP_EFFECTIVE.
  - 14B and OLMo-2-13B are NONE, because the single random draw did as well. Y1 is PARTIAL, not a confirmation.
- **"Not the advantage" is ambiguous (A1):**
  - It is right if "advantage" means beating all baselines. BEATS_BASELINES is 0 of 2 here, and SEP_BEATS is 0 of 4.
  - It is wrong if "advantage" means the advantage over prompt defences. That held at 14B on both benchmarks and at 32B on InjecAgent.
- **Suggested wording:** "Larger Qwen3 models and four held-out models reproduce the drop in attack success (SEP 6 of 6, InjecAgent 2 of 2). The sealed verdicts are Y1 PARTIAL and Y2 SEP_EFFECTIVE: no new model beats all baselines, and no held-out model beats all three prompt defences on SEP."
- The same ambiguity (A1) is in Paper B §5 line 427: "Its benchmark advantage holds in Qwen3-8B but not … at the other Qwen3 sizes". Write "its advantage over all baselines, including the single random draw".

**O3. Descriptive heading "The effect generalizes" (§3.8 line 385 = §6n line 671).**
- **SEP:** the heading is fine (11 of 12 models; the 11 come from 6 of the 7 families).
- **InjecAgent:**
  - The "5 of 8" are the four Qwen sizes and Phi-4.
  - In Phi-4 and in Qwen3-14B, the single random draw did as well (X5 InjecAgent fails).
  - §3.7 itself says the recipe carries over to InjecAgent "only in the family where it was found".
- **Suggested wording:** "**The SEP effect generalizes.** The steering lowered SEP attack success in 11 of 12 models from 7 families. On InjecAgent it lowered attack success in 5 of 8: the four Qwen sizes and Phi-4, where, as at Qwen3-14B, the single random draw did as well."

**O4. CONSOLIDATED line 577: "… so at 32B the effect is specific to the direction."**
- One isotropic draw cannot establish specificity. The RNDCTL section of the same file, 13 lines below, says Y X5 "should be reported as single-draw".
- The 32B pass on SEP is marginal (R1). The papers were already changed to "(one draw)"; CONSOLIDATED was not.
- **Suggested wording:** "It beats its single random draw on both benchmarks (InjecAgent RND 18.5%, CI [−0.16, −0.07]; SEP CI [0.003, 0.107], a one-item margin). One draw does not establish that the effect is specific to the direction."

**O5. CONSOLIDATED line 573: "RNDCTL (exploratory, Qwen3-4B, 32 draws) found random effects sign-varying and centred near zero, which argues against a generic disruption effect there."**
- RNDCTL used a different model and precision (Qwen3-4B in 4-bit), a different task (inj2) and a different readout (the first token). It cannot argue about Qwen3-14B on InjecAgent.
- "Centred near zero" holds in doc (+0.015) but not in sys, where the mean random shift is −0.101 (SD 0.195). That is a mean reduction of the kind a disruption account predicts.
- **Suggested fix:** delete "which argues against a generic disruption effect there". Keep the next sentence: "A multi-draw benchmark control would settle it here."

**O6. CONSOLIDATED line 563, "Reading, fixed in advance."**
- **"and up to 32B":** this is not in the preregistered SEP_EFFECTIVE reading. The text fixed in advance is: "the lever helps on SEP in held-out models but does not beat the prompt defences there."
- **The second sentence was not fixed in advance:** "PREREG_X's observed … does not replicate in new families: … about as good as the best prompt defence (usually the reminder)". Its numbers are right: the reminder is the unbeaten prompt in 3 of 4.
- **"New families":** two of the four held-out models are larger OLMo sizes, and OLMo-2-7B did beat all three prompt defences on SEP in PREREG_X.
- **Suggested fix:**
  - Quote the preregistered reading verbatim.
  - Label the rest "Descriptive:".
  - Write "in the held-out models (two new families and two larger OLMo sizes)".

**Wording notes (not overstatements):**
- **W1, abstract line 35: "beat the prompt defences in none of them".** This understates the result: in every held-out model the steering beat 2 of the 3 prompt defences. Write "beat all three prompt defences in none of them".
- **W2, "centred near zero"** (§3.8 line 381 = §6n line 667; Paper B line 452 = PAPER_DRAFT line 776). The RNDCTL means are +0.015 (doc), +0.051 (asst, at the floor) and −0.101 (sys). Write "centred near zero in doc; mean −0.10 in sys (SD 0.20)", or "small relative to their SD".
- **W3, §4 line 412: "On SEP in held-out families".** Write "in held-out models", because two of them are OLMo sizes.

**L1. The preregistered descriptive output is not reported (omission).**
- PREREG_Y fixes a "Descriptive, not gated" size trend:
  - SEP Net(DEF) − Net(best prompt);
  - InjecAgent ASR(DEF) − ASR(best prompt).
- CONSOLIDATED says "No size trend is claimed; this is reported, not tested", but the numbers appear nowhere.
- Recomputed, with best prompt = the highest Net or the lowest ASR among P, SPOT and REMIND:

  | Qwen3 size | SEP Net(DEF) − Net(best prompt) | InjecAgent ASR(DEF) − ASR(best prompt) |
  |---|---|---|
  | 1.7B | +0.047 | −0.380 |
  | 8B | +0.103 | −0.220 |
  | 14B | +0.087 | −0.176 |
  | 32B | +0.047 | −0.061 |

  The InjecAgent margin over the best prompt shrinks steadily with size. Report this, labelled descriptive.

**Labelling check (step 5):**
- **Labelled correctly:**
  - The §3.8/§6n "Reading" block ("descriptive tallies …, not a sealed claim").
  - The RNDCTL sentence ("exploratory").
  - The CONSOLIDATED size series ("reported, not tested").
- **Unlabelled descriptive or interpretive readings:**
  - the abstract's "stayed effective" (O1);
  - the §1 contribution (O2);
  - §4 "Practical upshot" (it contains M1);
  - CONSOLIDATED O4, O5 and O6.

## 5. Robustness notes (not mismatches; the sealed seed is fixed, so the sealed verdicts stand)

**R1. Y1 = PARTIAL hinges on one SEP item.**
- Qwen3-32B is EFFECTIVE only because its SEP X5 passes.
- The paired Net(DEF) − Net(RND) values are: 37 items at +1, 1 at +2, 23 at −1 and 239 at 0, for a mean of +0.0533.
- The sealed bootstrap CI (seed 0) is [0.0033, 0.1067]. Its lower bound clears 0 by 1/300.
- **Under other seeds:** over 200 bootstrap seeds, the lower bound is above 0 in 50.5% of them, exactly 0 in 49% and below 0 in 0.5%.
- **Under a sign-flip test** on the same differences, p = 0.057.
- **If X5 had failed,** 32B would be NONE and Y1 would be NONE.
- **Suggested text:** "Y1 = PARTIAL rests on Qwen3-32B passing the SEP random-draw check by one item (CI lower bound +0.003)."

**R2. A one-case validity margin at 32B.** On InjecAgent, X4's validity guard against the reminder passes by one case: V(DEF) is 278/300, against V(REMIND) − 0.05 = 277/300. The claim "At 32B … beats every prompt defence" rests on it. The verdict does not: EFFECTIVE does not need X4.

**R3. A one-item effect margin in OLMo-2-13B.** Its X1 effect is dE = −16/300 against the −0.05 threshold (−15/300), with p 0.0051. Its verdict is NONE anyway, because of X5.

**Every other Y decision is stable.** I tested each other borderline CI decision across 20 bootstrap seeds and none flips:

| Comparison | CI bound at seed 0 | Result |
|---|---|---|
| 14B SEP SPOT | lower 0.0167 | 20/20 |
| 14B SEP RND | lower 0.0233 | 20/20 |
| 14B InjecAgent RND | upper 0.0197 | fails in 20/20 |
| 32B SEP REMIND | lower −0.0167 | fails in 20/20 |
| 32B InjecAgent REMIND | upper −0.0295 | 20/20 |
| 32B InjecAgent RND | upper −0.0664 | 20/20 |
| Falcon3 SEP SPOT | lower −0.0233 | fails |
| Falcon3 SEP RND | lower 0.0133 | 20/20 |
| Yi SEP REMIND | — | fails |
| Yi SEP RND | — | 20/20 |
| OLMo-2-13B SEP RND | lower −0.01 | fails |
| OLMo-2-32B SEP P | lower 0.01 | 20/20 |
| OLMo-2-32B SEP RND | lower 0.0133 | 20/20 |

## 6. Claim table

Abbreviations:
- **B** = Paper B (`snap2` line numbers); **D** = PAPER_DRAFT; **C** = CONSOLIDATED.
- **§3.8 = §6n:** B lines 360–386 are the same text as D lines 646–672.
- **Rates:** SEP attack = E_data and utility = U, with counts out of 300. InjecAgent ASR = succ / (succ + unsucc), and valid = (succ + unsucc) / 300.

| # | Where | Claim | Evidence (recomputed) | Class | Flag |
|---|---|---|---|---|---|
| 1 | B 33; §3.8/§6n headings | Y1 PARTIAL, Y2 SEP_EFFECTIVE | y_analysis.json; re-run byte-identical | MATCH | R1 |
| 2 | B 34 | 14B and 32B "stayed effective and additive" | 14B NONE, 32B EFFECTIVE; both ADDITIVE; X1/X3 pass in both | MATCH | O1 |
| 3 | B 35 | SEP attack lowered in all four held-out models | X1 4/4 | MATCH | |
| 4 | B 35 | "beat the prompt defences in none of them" | X2 0/4; but 2 of 3 prompts beaten in each | MATCH | W1 |
| 5 | B 36 | 14B: the single random draw also cut InjecAgent attack success | RND 13/268 = 4.85% vs none 83/284 = 29.2%; DEF−RND CI [−0.0315, 0.0197] | MATCH | |
| 6 | B 60 | larger Qwen3 and held-out models "confirm the effect but not the advantage" | X1 6/6, X3 2/2; sealed effect verdicts 4/6; BEATS_BASELINES 0/2; SEP_BEATS 0/4; 14B beats all prompts on both benchmarks | MATCH (all-baselines reading) | O2, A1 |
| 7 | B 101 | $18.4 for PREREG_Y | 2.41 h × 3.99 + 2.75 h × 3.19 = 9.616 + 8.7725 = 18.39 | MATCH | |
| 8 | B 101 | $38 through PILOT_V1 | carried over from the pre-Y text; not recomputed here | UNVERIFIABLE | |
| 9 | B 101 | about $56 | 38 + 18.39 = 56.39 | ROUNDING | |
| 10 | B 101 | A100 and H100 | Y pods: H100 80GB HBM3 (launched33) and H100 NVL 95,830 MiB (launched34) | MATCH | |
| 11 | §3.8/§6n | PREREG_X code, recipe, conditions, samples and seeds unchanged; byte-identical | 12/12 shared files vs the PREREG_X seal and agp28; seed 2800; same SEP and InjecAgent keys | MATCH | |
| 12 | §3.8/§6n | Y1 design; SCALES requires both to be BEATS_BASELINES | y_analyze.py lines 28–54 | MATCH | |
| 13 | §3.8/§6n | Y2 design: SEP only, models never on a benchmark; SEP_BEATS needs ≥3 of 4 | y_analyze.py lines 41–60; absent from x_analysis; the rule also needs X1 and X5 (simplified) | MATCH | |
| 14 | §3.8/§6n | 14B SEP 37.0% → 18.3% | 111/300 → 55/300 | MATCH | |
| 15 | §3.8/§6n | 14B InjecAgent 29.2% → 4.6% | 83/284 → 13/280 | MATCH | |
| 16 | §3.8/§6n | 14B NONE: the single same-norm draw cut attack success to 4.9% (X5) | 13/268 = 4.85%; X5 InjecAgent fails | MATCH | |
| 17 | §3.8/§6n | 32B SEP 40.3% → 30.0% | 121 → 90 of 300 | MATCH | |
| 18 | §3.8/§6n | 32B InjecAgent 27.8% → 8.6% | 80/288 → 24/278 | MATCH | |
| 19 | §3.8/§6n | 32B EFFECTIVE; tied the reminder on SEP (X2) | DEF−REMIND CI [−0.0167, 0.11] | MATCH | R1 |
| 20 | §3.8/§6n | Falcon3-10B 48.7% → 33.0%, SEP_EFFECTIVE | 146 → 99 | MATCH | |
| 21 | §3.8/§6n | Yi-1.5-9B 47.3% → 30.7%, SEP_EFFECTIVE | 142 → 92 | MATCH | |
| 22 | §3.8/§6n | OLMo-2-13B 43.7% → 38.3%; NONE, did not beat the single draw (X5) | 131 → 115; RND CI [−0.01, 0.0933] | MATCH | R3 |
| 23 | §3.8/§6n | OLMo-2-32B 58.7% → 47.3%, SEP_EFFECTIVE | 176 → 142 | MATCH | |
| 24 | §3.8/§6n | "Utility held in every model" | SEP dU −1.00 to +1.33 pts; InjecAgent dV −1.33 and −3.33; all guards ≥ −5 pts | MATCH | |
| 25 | §3.8/§6n | largest change −3.3 pts, InjecAgent valid, 32B | 288 → 278 of 300 = −3.33; next largest is 1.33 | MATCH | |
| 26 | §3.8/§6n | both Qwen sizes cut attack success on both benchmarks | X1 and X3 pass in both | MATCH | |
| 27 | §3.8/§6n | ADDITIVE with P and SPOT | X6 P and SPOT true in both; SEP add CIs > 0; InjecAgent add CIs < 0; dV ≥ −0.03 | MATCH | |
| 28 | §3.8/§6n | 32B InjecAgent: beats every prompt and its single draw | X4 true; RND CI [−0.1587, −0.0664] | MATCH | R2 |
| 29 | §3.8/§6n | 14B InjecAgent: the one draw did as well | 4.85% vs 4.64%; CI spans 0 | MATCH | |
| 30 | §3.8/§6n | RNDCTL: 32-draw check, sign-varying, centred near zero | 16 × ±2; corr −0.85/−0.24/−0.59; means +0.015/+0.051/−0.101 | ROUNDING | W2 |
| 31 | §3.8/§6n | Y2: lowered in 4/4, beat all three prompts in 0/4 | X1 4/4, X2 0/4 | MATCH | |
| 32 | §3.8/§6n | "The reminder or the datamarking prompt matched it" | unbeaten prompt: Falcon3 SPOT; Yi, OLMo-2-13B and OLMo-2-32B REMIND | MATCH | |
| 33 | §3.8/§6n | SEP effect in 11 of 12 models from 7 families | X1: 5/6 (X, all but Phi-4) + 6/6 (Y) | MATCH | O3 |
| 34 | §3.8/§6n | InjecAgent effect in 5 of 8 | X3: Qwen3-1.7B, 8B, Phi-4, 14B, 32B | MATCH | O3 |
| 35 | §3.8/§6n | beat all prompts on SEP in 5 of 12 | X2: OLMo-2-7B, Qwen3-8B, SmolLM3, Granite, Qwen3-14B | MATCH | |
| 36 | §3.8/§6n | beat all prompts on InjecAgent in 4 of 8 | X4: Qwen3-1.7B, 8B, 14B, 32B | MATCH | |
| 37 | §3.8/§6n | "all of them Qwen" | true for InjecAgent; 3 of the 5 SEP models are not Qwen | **MISMATCH (M2)** | |
| 38 | §3.8/§6n | only Qwen3-8B passes every check on both benchmarks | only BEATS_BASELINES among the 8 two-benchmark models | MATCH | |
| 39 | B 401 | 14B 29% → 5%; 32B 28% → 9% | 29.23 → 4.64; 27.78 → 8.63 | ROUNDING | |
| 40 | B 401 | 14B: the single random control did as well | as row 29 | MATCH | |
| 41 | B 408 | Qwen3 1.7B–32B: cuts attack success on both benchmarks, stacks with prompts | X1 and X3 pass at all 4 sizes; ADDITIVE at all 4 | MATCH | |
| 42 | B 409 | "beats every prompt defence on both benchmarks only at 8B" | 14B also has X2 and X4 true | **MISMATCH (M1)** | |
| 43 | B 410 | 32B ties the reminder on SEP | as row 19 | MATCH | |
| 44 | B 411 | 14B: its one random control matched it on InjecAgent | as row 29 | MATCH | |
| 45 | B 412 | held-out SEP: about as good as the best prompt | best-Net prompt vs DEF: 0.290/0.350, 0.407/0.353, 0.303/0.317, 0.400/0.420; CIs span 0 | MATCH | W3 |
| 46 | B 427 | benchmark advantage only in 8B, not at the other Qwen3 sizes | right for BEATS_BASELINES; 14B beats all prompts on both | MATCH (all-baselines reading) | A1 |
| 47 | B 451 / D 775 | PREREG_X and Y X5 use single draws | bench.py lines 235–236 | MATCH | |
| 48 | B 452 / D 776 | RNDCTL: flips sign, centres near zero, SD 0.13–0.22 | SD 0.132/0.219/0.195; means as row 30 | ROUNDING | W2 |
| 49 | B 472 | PREREG_Y has 18 sealed files, bundle agp30 | 18 lines; md5 28b86845 | MATCH | |
| 50 | B 460, 462 | "PREREG_S to PREREG_X"; "PREREG_V, W and X analyses … bundle copy" | omits PREREG_Y | **MISMATCH (M3)** | |
| 51 | B 478–483 | analysis and raw paths; benchmark commits | `cloud_prereg_y*` and `cloud_prereg_y_analysis` match the patterns; rc33/rc34 pin and abort | MATCH | |
| 52 | D 858 | $9.62 (part A) | 2.41 h × $3.99 = 9.616; hours not in RF; records give ≥ 2.371 h (03:26:24–05:48:40) = ≥ $9.46 | UNVERIFIABLE (consistent) | |
| 53 | D 858 | $8.77 (part B) | 2.75 h × $3.19 = 8.7725; records give ≥ 2.726 h (03:38:26–06:21:58) = ≥ $8.69 | UNVERIFIABLE (consistent) | |
| 54 | D 858 | about $18.4 | sum 18.39 | MATCH | |
| 55 | D 870 | PREREG_Y has 18 sealed files, bundle agp30 | as row 49 | MATCH | |
| 56 | D 860 | "(§6g–§6m)"; "PREREG_V, W and X analyses …" | omits §6n and Y | **MISMATCH (M3)** | |
| 57 | C 549 | agp30 md5 28b86845…; seal 18/18 from a clean extract | reproduced | MATCH | |
| 58 | C 549 | PREREG_X code byte-identical | 12/12 | MATCH | |
| 59 | C 550 | part A: H100 SXM, US-NE-1, 03:25–05:48 UTC | launched33: H100 80GB, mfs us-ne-1, 03:26:24; last status 05:48:40 | ROUNDING | |
| 60 | C 550 | part A fetched with md5 ee26efed… | ee26efedb0e8… | MATCH | |
| 61 | C 550–551 | both pods terminated | not checkable offline; PLAN_7DAY says so | UNVERIFIABLE | |
| 62 | C 550 | benchmark commits verified on the pod | rc33 and rc34 abort on a mismatch; runs completed (run33.log not fetched) | MATCH (indirect) | |
| 63 | C 550 | no OOM retries; 32B SEP at batch 32 | last_status; ERRS 0; no oom_attempt1 file | MATCH | |
| 64 | C 551 | part B: H100 NVL with a network volume, batch 8, no OOM retry | launched34: H100 NVL 95,830 MiB, mfs us-ks-2; last_status B | MATCH | |
| 65 | C 551 | part B 03:38–06:18 UTC | the run window; the pod was alive until ≥ 06:21:58, and the cost uses 2.75 h | ROUNDING | |
| 66 | C 551 | part B fetched with md5 1d3acd95… | 1d3acd950d7d… | MATCH | |
| 67 | C 552 | y_analysis md5 8bd9a033…, run on both parts from a clean bundle | reproduced, byte-identical | MATCH | |
| 68 | C 554 | Y2: X1 4/4, X2 0/4 | as row 31 | MATCH | |
| 69 | C 558 | Falcon3: 48.7 → 33.0 (U 67.3 → 68.0); SPOT 28.3%; fails vs SPOT, CI [−0.02, 0.14]; X5 yes | 0.6733 → 0.68; 85/300; [−0.0233, 0.14]; RND [0.0133, …] | MATCH | |
| 70 | C 559 | Yi: 47.3 → 30.7 (66.7 → 66.0); SPOT 37.7%; fails vs REMIND, CI [−0.13, 0.03] | 113/300; [−0.13, 0.0267] | MATCH | |
| 71 | C 560 | OLMo-2-13B: 43.7 → 38.3 (69.3 → 70.0); SPOT 39.3%; X1 −0.053, p 0.005; fails vs REMIND; RND CI [−0.01, 0.09]; NONE | dE −0.0533, p 0.0051; [−0.01, 0.0933] | MATCH | R3 |
| 72 | C 561 | OLMo-2-32B: 58.7 → 47.3 (88.7 → 89.3); REMIND 49.3%; CI [−0.04, 0.08] | 148/300; [−0.04, 0.08] | MATCH | |
| 73 | C 563 | "Reading, fixed in advance" … "usually the reminder" | unbeaten prompt is REMIND in 3/4 | MATCH | O6 |
| 74 | C 565 | Y1 PARTIAL; 14B NONE failing X5 only; 32B EFFECTIVE failing X2 only; both ADDITIVE | hyp flags | MATCH | R1 |
| 75 | C 568–571 | 14B X1–X4: 37.0 → 18.3 (U 71.0 → 72.3); 29.2 → 4.6 (valid 94.7 → 93.3); beats all prompts on both; ADDITIVE | 0.71 → 0.7233; 284 → 280 of 300 | MATCH | |
| 76 | C 572 | 14B X5: RND 4.9% (valid 89.3%), CI [−0.03, 0.02]; SEP RND CI [0.02, 0.14] | 268/300; [−0.0315, 0.0197]; [0.0233, 0.1433] | MATCH | |
| 77 | C 573 | the RNDCTL facts and the "argues against a generic disruption effect there" inference | facts as row 30; the inference crosses setups | ROUNDING | O5 |
| 78 | C 575–578 | 32B: 40.3 → 30.0 (U 73.3 → 72.3); ties REMIND, CI [−0.02, 0.11]; 27.8 → 8.6 (valid 96.0 → 92.7); REMIND CI [−0.12, −0.03]; RND 18.5%, CI [−0.16, −0.07]; DEF+P 7.7% | 53/287 = 18.47%; 22/286 = 7.69% | MATCH | R2 |
| 79 | C 577 | "so at 32B the effect is specific to the direction" | X5 passes on both, but with a single draw and a marginal SEP pass | MATCH (X5 passes) | O4, R1 |
| 80 | C 580 | size series: 1.7B EFFECTIVE, 8B BEATS_BASELINES, 14B NONE (X5), 32B EFFECTIVE (X2); ADDITIVE at every size | x_analysis + y_analysis | MATCH | |
| 81 | C 581 | cuts attack success substantially at every Qwen3 size on both benchmarks | X1 and X3 pass at all 4; drops 10–54 pts | MATCH | |
| 82 | C 581 | "beats every prompt defence on both only at 8B" | 14B also has X2 and X4 | **MISMATCH (M1)** | |
| 83 | C 582 | 14B InjecAgent drop matched by the single draw | as row 29 | MATCH | |
| 84 | C 583 | "No size trend is claimed; this is reported, not tested" | labelled; but the preregistered descriptive numbers are absent | MATCH | L1 |
| 85 | C 586 | part A about $9.6 (2.41 h × $3.99) vs E33 $10.88 | arithmetic and E33 ✓; hours as row 52; C's own 03:25–05:48 gives 2.383 h = $9.51 | UNVERIFIABLE (consistent) | |
| 86 | C 587 | part B about $8.8 (2.75 h × $3.19) vs E34 $8.86 | arithmetic and E34 ✓; C's own 03:38–06:18 gives 2.667 h = $8.51 | UNVERIFIABLE (consistent) | |
| 87 | C 588 | PREREG_Y total about $18.4 | sum | MATCH | |

**Counts:** 87 claims, of which 69 MATCH, 7 ROUNDING, 5 MISMATCH and 6 UNVERIFIABLE.
- **Mismatch rows:** M1 in rows 42 and 82; M2 in row 37 (in both B and D); M3 in rows 50 and 56.
- **Costs:**
  - The record-derived minimum is $9.46 + $8.69 = $18.16. The claimed $18.39 needs about 2.3 min (A) and 1.5 min (B) of pod time outside the logged windows, which pod boot and the post-fetch self-stop plausibly cover.
  - The intervals written in CONSOLIDATED imply $18.02. Label them as run windows, or give the pod windows behind 2.41 h and 2.75 h.

## 7. Outside scope, noted only

- **PAPER_DRAFT's novelty block** (line 830, "(§6g–§6m)", and "Its benchmark advantage holds in Qwen3-8B but not across families (§6m)") was not updated for §6n. Paper B's equivalent was.
- **`RNDCTL_RESULTS.md` is stale on PREREG_K.** It says "PREREG_J (50 random directions) and K already use a distribution". The papers and the PLAN_7DAY 10:29 entry say K is a single draw.
- **The first versions of the claim files I read (10:25)** also had "so part of the effect there is disruption, not the direction" and "At 32B the effect is specific to the direction". The main agent backed these versions up in `scratchpad\pre_rndctl\`. The 10:29 RNDCTL edit removed both phrases from the papers; CONSOLIDATED still has the 32B one (O4).
- **`y_tables.md` "SEP best prompt"** means the lowest attack rate. X2 judges by Net, so for Qwen3-14B the table names REMIND, while SPOT is the best prompt by Net. No claim depends on this.
- **Part B's smoke test is InjecAgent-only.** That is by the sealed `rc34.sh` design, not a deviation.

## Files

- **Extract:** `C:\Users\caabm\AppData\Local\Temp\claude\C--Users-caabm-Downloads\b2d893aa-daa4-417d-a29a-85a40bff7760\scratchpad\recheck_y\agp30\` (with `cloud\` added).
- **Re-run outputs:**
  - `...\scratchpad\recheck_y\y_rerun.json`
  - `...\scratchpad\recheck_y\x_style_rerun.json`
- **Independent recomputation:**
  - `...\scratchpad\recheck_y\scripts\indep.py`
  - output: `...\scratchpad\recheck_y\indep_out.txt`
- **Seed robustness:**
  - `...\scratchpad\recheck_y\scripts\robust.py` and `robust2.py`
  - outputs: `...\scratchpad\recheck_y\robust_out.txt`, `robust2_out.txt` and `robust_32b_x5.txt`
- **Claim-file snapshots:** `...\scratchpad\recheck_y\snap1\` (10:29) and `snap2\` (10:34, the version checked).
- **Archive extracts used for the provenance check:** `...\scratchpad\recheck_y\tgzA\`, `tgzB\` and `agp28x\`.

(`...` = `C:\Users\caabm\AppData\Local\Temp\claude\C--Users-caabm-Downloads\b2d893aa-daa4-417d-a29a-85a40bff7760`)
