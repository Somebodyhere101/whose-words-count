# Whose words count? Code, preregistrations and data for two studies of source and authority in chat models

Sam Ramdan ([ORCID 0009-0004-7723-4240](https://orcid.org/0009-0004-7723-4240))

This repository holds everything behind two companion preprints:

- **Paper A: Whose words count? Chat role and partial control of goal adherence**
  - PDF: [`paper/whose-words-count-paper-a.pdf`](paper/whose-words-count-paper-a.pdf)
  - Zenodo: [doi:10.5281/zenodo.23758885](https://doi.org/10.5281/zenodo.23758885)
- **Paper B: Who said this? Most chat models weigh a text's source differently for each behaviour, and a steering lever against injected instructions**
  - PDF: [`paper/who-said-this-paper-b.pdf`](paper/who-said-this-paper-b.pdf)
  - Zenodo: [doi:10.5281/zenodo.23758887](https://doi.org/10.5281/zenodo.23758887)

This is AI-run research: an AI system (Claude, Anthropic) designed, ran, analysed and wrote both studies. Each paper's AI-use statement says who proposed what. The author did not independently check the code, analyses or technical claims, and is responsible for the released content.

## What the studies ask

- **Paper A.** Does a chat model hold a goal less firmly when the goal text sits in its own (assistant) turn than when the same text is given in a system or user turn? And is that difference carried by a direction in the model's activations?
- **Paper B.** Do chat models carry one internal "who said this" tag that governs whether they obey a text, believe it and can say where it came from? Where in the network is a text's source read? Can that map guide a selective defence against instructions injected into tool output?

Every confirmatory claim rests on a preregistration that was written, hash-sealed (`*.sha256`) and bundled (`bundles/agpNN.tgz`) before its data existed. Exploratory results are labelled as such, and failures are reported in full.

## Sections and verdicts

Paper A:

| Section (verdict as stated in the paper) |
|---|
| 1. Introduction |
| 2. Instrument |
| 3. Behaviour: the same goal text is weaker in the agent's own voice |
| 4. Representation: the tested probes found no self-specific "this is mine" tag (FAIL, log gate, Qwen3-1.7B; the control transfers as well or better in 9 more models) |
| 5. Mechanism: one role direction moves adherence in both directions |
| 6. Origin: the discount is present at the first testable stage, supervised fine-tuning (AMBIGUOUS, PREREG_D) |
| 6b. One axis for all three roles (PASS, PREREG_H and PREREG_I) |
| 6c. Is the axis authority itself? Social cues within a role (MIXED, PREREG_J) |
| 6d. Is the axis necessary? Directional ablation (PARTIAL, PREREG_K) |
| 6e. Does size matter? (NO_TREND, PREREG_L) |
| 6f. Semantic self-attribution is distinct from chat-role placement (H1 MIXED, H2 MIXED, H3 DOES_NOT_TRACK; PREREG_M) |
| 7. Accounts that failed (deixis FAIL; addressee INCONCLUSIVE) |
| 8. Injection: role steering reduces it in one model (REPL.) |
| 9. An obvious fix fails: fine-tuning on own-voice goal practice (FAIL, PREREG_E and PREREG_F) |
| 10. Believe or obey? (EXPL., unfinished) |
| 11. Limitations |
| 12. What may be new, and what is not |

Paper B:

| Section (verdict as stated in the paper) |
|---|
| 3.1. No single source ordering across behaviours (FRAGMENTED, PREREG_S) |
| 3.2. Where each behaviour reads the source (H1 MIXED, H2 DISSOCIATED, PREREG_T) |
| 3.3. The map in ten more models, up to 32B (4 of 5 SUPPORTED, PREREG_W) |
| 3.4. A first defence attempt fails (NONE, PREREG_U) |
| 3.5. Checking the readout, and searching for a lever (EXPL., PILOT_V0) |
| 3.6. The lever, sealed (SELECTIVE, PREREG_V) |
| 3.7. Public prompt-injection benchmarks (NONE overall; strong in Qwen; PREREG_X and PILOT_V1) |
| 3.8. Larger Qwen3 models and held-out families (Y1 PARTIAL, Y2 SEP_EFFECTIVE, PREREG_Y) |

## Layout

| Path | Contents |
|---|---|
| `paper/` | The two papers as PDFs |
| `research_next/agent_goal_persistence/` | The study folder, kept at its workspace path so the seal files verify |
| `research_next/agent_goal_persistence/PREREG*.md`, `*.sha256` | Sealed preregistrations and their hash lists |
| `.../code/`, `.../cloud/` | Run and analysis code, and the cloud pod scripts (`rcNN.sh` runs a test, `ssNN.sh` stops its pod) |
| `.../bundles/` | The sealed code bundle of each test, exactly as it ran |
| `.../cloud_*/` | Raw outputs and analysis files for each test |
| `.../PAPER_A_GOAL_PERSISTENCE.md`, `PAPER_B_SOURCE_MONITORING.md`, `PAPER_DRAFT.md` | The papers' Markdown sources, and the full technical report they were split from |
| `.../CONSOLIDATED_RESULTS.md`, `PLAN_7DAY.md` | The results record, and the run log with pod times, costs and every deviation |
| `.../NUMBERS_RECHECK*.md`, `REFERENCES_VERIFIED.md` | Independent AI rechecks of every number and reference |
| `verify_seals.py` | Checks every seal against the files and bundles |
| `DATA.md` | What is not included, and the licences of third-party data |
| `strip_report.json` | What the release filter removed or redacted |

## Checking the seals

```
python verify_seals.py
```

Later tests extended some shared code files, so for the earlier tests the exact sealed versions are matched inside their bundles. The script prints one line per seal and ends with `ALL SEALS VERIFIED`.

## Re-running a test

Each bundle holds the code and the cloud script that ran its test. To re-run one, extract the bundle on a GPU machine and run its `rcNN.sh`. The scripts install their pinned `transformers` version and clone the benchmarks at the logged commits. Example cost, from the run log: PREREG_Y ran on one H100 SXM for about $9.6 and one H100 NVL for about $8.8.

## Licences

- **Code:** MIT (`LICENSE`).
- **Papers and data:** CC BY 4.0.
- **Third-party data:** see `DATA.md`.
