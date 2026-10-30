# Pre-publication review of the v2 changes to Papers A and B (2026-10-30)

Two Claude sessions reviewed the v2 changes before release, read-only.
- **Numbers and consistency:** checked every changed number and claim against the primary files. It recomputed the FLIP, AUTHPILOT, REVPILOT and TAGSTYLE values from the raw outputs.
- **Sceptical reader:** read the changed passages in context, as an outside reviewer would.

The release session checked each finding against the records before applying it.

Separately, AI prior-art searches in the session that ran the follow-ups found three related papers missing from v1. They were checked against the papers themselves (`REFERENCES_VERIFIED.md`, addendum 2026-10-30) and added. That session also pointed out a channel confound in the fund task; it was checked in the code and added as a limitation.

## Numbers and consistency review: 13 findings (5 must-fix, 8 should-fix)

| # | Finding | Disposition |
|---|---|---|
| 1 | Paper B §2 still gave $95.37 and listed only A100 and H100 GPUs | Fixed: about $101.6, $95.37 of it before v2; RTX PRO 6000 for FLIP |
| 2 | AI-use statement: AUTHPILOT's design was proposed by a Codex session (`AUTH_PRED.md`), and both sets of bets were hashed together | Fixed |
| 3 | Paper B §6: the web-page and tool sources differ by a prefix inside a user turn, not only by the role tag | Fixed |
| 4 | This file did not exist yet | Fixed |
| 5 | Paper A §2 and §11: FLIP also uses a 50-direction random null | Fixed |
| 6 | FLIP's axis match was overstated: the full orders differ (behaviour u > d > g > o, projection u, g, d, o), developer versus own is unresolved, and system versus developer differs on the axis but not in behaviour | Fixed in §6b's reading, §1 and §12 |
| 7 | REVPILOT: Qwen was BROKEN by the pilot's rule in pilot 3; "every adapter" holds for point estimates only (significant in 10 of 16); pilot 2's shortcut reading is post hoc | Fixed |
| 8 | §6e: FLIP adds an 18th model and a seventh family; §11 should say "with an axis test" | Fixed |
| 9 | Abstract: the AUTHPILOT sentence was not marked exploratory; §6f's reading went beyond the written rule | Fixed |
| 10 | TAGSTYLE: the fact items used a reference-data register, not a policy; Paper A §6's contrast with Ye et al. needs a pointer to §11 | Fixed |
| 11 | FLIP limits omitted the prefilled final channel and two deviations (RTX PRO 6000 instead of the sealed A100; PYTHONUTF8=1); no FLIP bundle was archived | Fixed. `bundles/fl.tgz` copied in from the running session's scratchpad: all 9 sealed files match `FLIP.sha256` |
| 12 | Cost paragraphs: Paper B's "a follow-up for Paper A"; no pod times in `PLAN_7DAY.md` for the v2 runs; REVPILOT's figure and the storage share | Fixed. REVPILOT is kept at about $3.7, the sum of its three pilots' run-log figures ($1.79 + $1.0 + $0.95) |
| 13 | Paper B data section: the "provenance hashes" lead-in contradicted TAGSTYLE's "without a hash" | Fixed |

## Sceptical review: 10 findings (6 must-fix, 4 should-fix)

| # | Finding | Disposition |
|---|---|---|
| 1 | Abstract: FLIP's AGREE read as support, although every reminder scored 0.95–0.97 and random directions also separate user text | Fixed with the reviewer's wording, lightly edited |
| 2 | TAGSTYLE: the register comparison spans two rewrites and favours register; at the plain wording the system tag still raised belief by 0.20–0.41 in 3 of 4 valid models; phi-4's attribution is a tie (overlapping intervals) | Fixed in both papers |
| 3 | REVPILOT pilot 3: Qwen BROKEN, and "did not change it" is too strong | Fixed ("did not produce one") |
| 4 | Abstract AUTHPILOT sentence: unlabelled, and it omitted the ceiling, the 30 seeds and OLMo's +0.036 | Fixed |
| 5 | AI-use statement: Codex proposed AUTHPILOT's design and reading rule | Fixed (same as review 1, #2) |
| 6 | Paper B §2's cost was stale; "Of the 29 October total" itemised only $20.04 of $25.90 | Fixed in both papers |
| 7 | FLIP's gate G1 cannot check mid-conversation system or developer turns; prefill limitation; Ye et al. (2026, Appendix K) studied the same model | Fixed |
| 8 | TAGSTYLE in Paper A: state the pilot's scope, note Paper A's own header effect, give the score scale | Fixed (scope, header comparison, 0.5 = parity). A Geng et al. pointer was not added, because §12 already cites it for this point |
| 9 | Paper B: prefix sources; the patching map shows a fixed-wording difference; the abstract was silent on wording | Fixed, including one sentence in Paper B's abstract |
| 10 | Rechecks paragraphs should say how findings were handled, and FLIP's sealed analysis should be re-run | Fixed. The re-run (`code/flip_analyze.py` on `cloud_flip/out_flip/`) reproduced `cloud_flip/flip_analysis.json` exactly |

## Added from the prior-art search

- Pan et al. 2025, *User-Assistant Bias in LLMs*: Paper A §12, Paper B §5.
- Laddha et al. 2026, *Position, Role or Label?*: Paper A §6b, §11 (channel) and §12; Paper B §5.
- N. G. Liu et al. 2026, *IHDec*: Paper A §12, Paper B §5.
- The channel confound, Paper A §11. In `code/agp_fast.py`, the quarterly data and the pressure lines go into user turns, and no run used the option that moves the pressure into another turn.

## Build notes

- `verify_seals.py` now skips lines that are not SHA-256 entries (`AUTH_PRED.sha256` ends with an md5 note). It also matches sealed files against every archived bundle, not only `agp*.tgz`. The second change is needed because shared code that FLIP sealed was later extended for the CHANNEL test, so FLIP's exact sealed versions now sit only in `bundles/fl.tgz`.
- `bundles/mp1.tgz` was copied into the study folder from the running session's scratchpad. Its SHA-256 matches `MPILOT_PRED.sha256`.

## CHANNEL passages: third check, 8 findings (2 must-fix, 6 should-fix)

The sealed CHANNEL test (USER_PRIMACY) finished after the two reviews above. Before it was used:
- its seal was verified;
- its sealed analysis was re-run from the raw outputs and reproduced `cloud_chan/chan_analysis.json` exactly;
- its contrasts were recomputed independently from the per-seed files.

A third Claude session then checked the CHANNEL passages and the rewritten cost lines, read-only. It reproduced the analysis in memory and recomputed every contrast. Its findings, all fixed:

| # | Finding | Disposition |
|---|---|---|
| 1 | §11: only the pressure moved. The quarterly data stayed in user turns. The placebo rise holds without a reminder only (with reminders, OLMo-2-7B fell). The placebo added a system-role turn, so position and role are confounded | Fixed with the reviewer's wording |
| 2 | §6b: Qwen3-8B's advantage also shrank, not significantly (+0.115 to +0.083) | Fixed |
| 3 | §6b placebo: OLMo-2-7B's rise is n.s. (+0.010, p 0.067); same confound as #1 | Fixed |
| 4 | Abstract: give CHANNEL's scope (its 10 models differ from the 10 with an axis test) | Fixed: 7B–32B, five lineages, one task |
| 5 | §12: CHANNEL tested only the user > system step, with no own turns and no axis | Fixed |
| 6 | §11 "One-axis generality": CHANNEL was also an attempt at a reversed condition, run after FLIP's stopping rule, at the author's request | Fixed |
| 7 | The PRIMACY rule's paraphrase lacked the Holm criterion and the 60% verdict threshold | Fixed |
| 8 | The rechecks sentence gave no outcome or record | Fixed: points to this file |

The release session verified the cited p-values before applying them: OLMo-2-7B's placebo is +0.010 (p 0.067), and with reminders it is −0.042 (system) and −0.014 (user).
