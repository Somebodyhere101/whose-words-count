# Agent goal persistence, main run: results

Run 2026-10-26, 12:12–18:17, under `PREREG.md`. The hashes in `PREREG.sha256` verified after the run, so code and analysis are unchanged. 160/160 runs completed and 40/40 seeds were analysable. The job hit its 90-minute GPU slot twice (exit 3) and resumed as planned. Raw runs are in `main/`; numbers are in `main_results.json`.

## Numbers

Mean drift score (the share of steps with a high-emission pick; lower = more on goal), Qwen3-1.7B, 40 seeds per cell:

| | given (system turn) | own (assistant turn) |
|---|---|---|
| fixed on-goal reminder | 2: **0.18** | 3f: **0.36** |
| agent's own note | 2′: **0.57** | 3: **0.73** |

| Test | Mean paired difference | 95% CI | p (Holm) | Verdict |
|---|---|---|---|---|
| H1 text (notes − fixed) | +0.38 | 0.31 to 0.45 | 0.0001 | **SUPPORTED** |
| H2 framing, fixed text (own − given) | +0.18 | 0.03 to 0.32 | 0.025 | **SUPPORTED** |
| S1 framing, notes (own − given) | +0.16 | 0.05 to 0.27 | 0.007 (uncorrected) | same direction |
| S2 interaction | +0.02 | −0.14 to 0.18 | 0.81 | none |

- **Control:** the fixed-given cell was on goal in 95% of seeds, so the study is informative.
- **Note content:** condition-3 notes contained pressure words in at least 5 of 10 notes in 62.5% of seeds.

## Reading

1. **What the reminder says matters most.** The agent's own goal notes take in the pressure ("...while maximizing returns") and keep it on goal far less well than a fixed on-goal reminder.
2. **Who appears to say it also matters, and in the predicted direction.** The same text placed in the agent's own turn is followed less than when the system gives it. The effect is about the same size for on-goal text and for the agent's drifted notes (no interaction). This is the agent-level counterpart of the small-model finding that a model obeys given text more than its own.

## Limits, stated plainly

- **The effect is in the averages, not a consistent per-seed shift.** Per seed, own was worse than given in 20/40 seeds and better in 17 (fixed text), and 22 vs 15 (notes). The mean difference comes mainly from own-framed runs that collapse fully into drift.
- **Framing is not the only difference between cells.** The "own" cells also contain the "Goal check" request that precedes the note; the "given" cells do not. That extra turn is a confound for H2 and S1 and must be removed in a follow-up, for example by adding the same request to the given cells.
- **The setting is narrow:** one small model (Qwen3-1.7B), one simplified environment, and adversarial pressure without the goal-switch phase.
- **Pilot hints did not all hold.** Pilot 2's "given makes drifted notes worse" did not replicate. Here given was better for both kinds of text.

## Next

1. Remove the confound: put the "Goal check" request in all four cells and rerun.
2. Batch the generation, 5–10x faster.
3. Repeat on Qwen3-8B in 4-bit and on a second family.
4. If the framing effect holds, redesign the recap and director arms, and try the steering-direction idea.

# Run B: confound-free framing test (`PREREG_B.md`)

Run 2026-10-26 18:42 to 2026-10-27 00:1x. The hashes verified. 160/160 runs, 40/40 seeds analysable. There was one out-of-memory crash while other GPU apps were running, and one slowed process was restarted at the user's OK. Neither changes any saved run. The automatic analysis step failed (`python -I` hid the module path) and was rerun by hand on unchanged files. Numbers are in `main_b_results.json`, which uses the alias names 2 = gF, 3f = oF, 2p = gN, 3 = oN.

Identical text in every pair; only the role differs:

| | given (system) | own (assistant) |
|---|---|---|
| fixed goal text | gF **0.27** | oF **0.37** |
| agent's own note | gN **0.52** | oN **0.58** |

| Test | Mean | 95% CI | p (Holm) | Verdict |
|---|---|---|---|---|
| H1 text | +0.23 | 0.14 to 0.32 | 0.0001 | **SUPPORTED** |
| H2 framing, fixed text (oF − gF) | +0.11 | 0.01 to 0.21 | 0.037 | **SUPPORTED** |
| S1 framing, notes (oN − gN) | +0.06 | −0.06 to 0.18 | 0.36 | not detected |
| S2 interaction | +0.05 | −0.11 to 0.21 | 0.56 | none |

- **Per seed,** oF was worse than gF in 26 seeds and better in 9. That is more consistent than in the main run (20 vs 17).
- **Control:** gF was on goal in 87.5% of seeds.

**Reading.** With the "Goal check" request removed, identical goal text is still followed less when it sits in the agent's own turn than when the system gives it. The main-run framing effect was not produced by the confound. For the agent's own notes, the framing difference is smaller and not detected at n = 40.
