# PREREG_Y: the lever at larger Qwen3 sizes, and its SEP advantage in held-out families

Written 2026-10-29 07:20 +04:00, after PREREG_X (NONE overall; BEATS_BASELINES in Qwen3-8B) and PILOT_V1 (NO_FORMAT_LEVER), and before any PREREG_Y data.

**The name.** "PREREG_Y" was reserved for a format-lever confirmation that PILOT_V1 did not trigger, and is reused here.

**Sealed** in `PREREG_Y.sha256`, together with:
- **PREREG_X's sealed code, byte-identical** (`PREREG_X.sha256` re-verified 15 of 15 OK on 2026-10-29):
  - `recipe.json`, `code/bench.py`, `code/x_analyze.py`, `data/injecagent_prompts.json`;
  - the helpers `code/lever_pilot.py`, `code/src_defense.py`, `code/src_patch_w.py`, `code/src_patch.py`, `code/src_monitor.py`, `code/agp_batch.py`, `code/agp_b.py`, `code/chat_fmt.py`.
- **New:** `code/y_analyze.py`, `cloud/rc33.sh`, `cloud/ss33.sh`, `cloud/rc34.sh`, `cloud/ss34.sh`.

## Why, after PREREG_X

In Qwen3-8B, the recipe beat every prompt defence on SEP and on InjecAgent, and it added to them when stacked. Across PREREG_X's six models:
- on SEP (the injection arrives in a tool-output turn), it beat all three prompt defences in 4 of 6 models from 4 families (X2);
- on InjecAgent (the injection is embedded in a ReAct message), it beat them only in the two Qwen models (X4).

Two questions decide how general this capability is:
1. **Y1:** does the Qwen3-8B result hold at 14B and 32B, the largest dense Qwen3 models? A risk stated now: earlier role steering was weak at 32B (PLAN_BIGGER, Risks).
2. **Y2:** does the SEP advantage hold in models never run with the lever on a benchmark? These are two families new to the benchmarks (Falcon3-10B, Yi-1.5-9B) and two larger sizes of a tested family (OLMo-2-13B and OLMo-2-32B).

## Design

**Unchanged from PREREG_X:** the code (`bench.py`), the recipe (tool−usr, depth 0.45, scale 4, tokens C), the conditions, the samples, the seeds and the token limits.
- **SEP:** 300 items, seed 2800, up to 128 new tokens.
- **InjecAgent:** 300 cases, seed 2800, up to 160 new tokens.
- **Benchmark commits:** pinned to PREREG_X's (SEP 7606c06, InjecAgent f19c9f2). The run aborts on a mismatch.
- **Depth:** the recipe's depth is relative, as in PREREG_X: layer = round(0.45 × the number of layers).

**Conditions:** none, DEF, RND, P, SPOT, REMIND, DEF+P, DEF+SPOT (defined in `PREREG_X.md`).

| Part | Models (Hugging Face ids) | Benchmarks |
|---|---|---|
| Y1 | `Qwen/Qwen3-14B`, `Qwen/Qwen3-32B` | SEP and InjecAgent |
| Y2 | `tiiuae/Falcon3-10B-Instruct`, `01-ai/Yi-1.5-9B-Chat`, `allenai/OLMo-2-1124-13B-Instruct`, `allenai/OLMo-2-0325-32B-Instruct` | SEP only |

**How it runs: two parts, the same design.**
- **Part A** (`rc33.sh`, one 80 GB H100 SXM): Qwen3-14B on both benchmarks, and SEP for Qwen3-32B and all four Y2 models.
- **Part B** (`rc34.sh`, one GPU with at least 94 GB): Qwen3-32B on InjecAgent.
- **Why the split.** The decode loop computes full-vocabulary logits over the prompt, so Qwen3-32B on InjecAgent at batch 8 needs about 81.6 GB (weights 65.6 GB, logits about 7.3 GB, KV cache about 6.6 GB). No 94 GB H100 NVL was in stock at 07:40, and an H200 for everything risked the balance.
- **When the verdicts are computed.** Y2 is computed after part A. Y1 is computed after part B, and only then.
- All models run in bf16. Batches: 32 for SEP and 8 for InjecAgent (as for Phi-4 in PREREG_X).
- Templates: the same handling as PREREG_W and X (Yi in ChatML, which keeps system turns).

**Smoke test (not study data).** Qwen3-0.6B on 4 SEP items and 4 InjecAgent cases, conditions none and DEF. It is an environment check only; the run aborts if it fails.

**Operational rule, fixed now.** A run that ends in CUDA out-of-memory without finishing is repeated once at half the batch size. The first log is kept (`*_oom_attempt1.txt`). Batch size changes only padding and numerics, not the items or the rules.

## Rules (`code/y_analyze.py`, fixed now)

All statistics are `x_analyze.py`'s own functions, unchanged: paired tests, 2,000 bootstrap resamples, 20,000 sign flips.

**Y1, larger Qwen3 (both benchmarks).**
- **Per model:** PREREG_X's verdicts.
  - BEATS_BASELINES if X1–X5 all hold; EFFECTIVE if X1, X3 and X5 hold; NONE otherwise.
  - ADDITIVE, PARTLY_ADDITIVE or NOT_ADDITIVE from X6.
- **Y1 = SCALES** if both models are BEATS_BASELINES.
- **PARTIAL** if not SCALES, and at least one model is BEATS_BASELINES or EFFECTIVE.
- **NONE** otherwise.

**Y2, held-out families and sizes (SEP only).**
- **Per model:**
  - SEP_BEATS if X1, X2 and the SEP half of X5 hold;
  - SEP_EFFECTIVE if X1 and the SEP half of X5 hold;
  - NONE otherwise.
- **Y2 = SEP_BEATS** if at least 3 of 4 models are SEP_BEATS.
- **SEP_EFFECTIVE** if at least 3 of 4 are SEP_BEATS or SEP_EFFECTIVE.
- **NONE** otherwise.

A model whose result file is missing counts as NONE, and is reported.

**Pre-seal tests (`y_test.py`, scratchpad), 40 of 40 passed:**
- On PREREG_X's own data, `y_analyze`'s per-model logic reproduces every stored PREREG_X verdict and SEP hypothesis (6 models).
- The Y1 and Y2 threshold rules give the right verdict on planted verdict lists.
- An empty results folder gives NONE everywhere, with every model listed as missing.

## Readings fixed now

**Y1:**
- **SCALES:** in the Qwen3 family, the training-free lever beats prompt defences on both public benchmarks at every size tested from 8B to 32B. This is still one family.
- **PARTIAL:** the capability depends on size; we report which sizes keep it.
- **NONE:** the Qwen3-8B result does not extend to larger Qwen3 models.

**Y2:**
- **SEP_BEATS:** beating prompt defences on tool-turn injections generalizes to held-out families and up to 32B. With PREREG_X, this claim then rests on a held-out confirmation. It is a single-turn benchmark, not an agent benchmark.
- **SEP_EFFECTIVE:** the lever helps on SEP in held-out models but does not beat the prompt defences there.
- **NONE:** PREREG_X's SEP pattern does not generalize.

**Descriptive, not gated:** the size trend in Qwen3 (1.7B and 8B from PREREG_X; 14B and 32B here) of:
- SEP Net(DEF) − Net(best prompt);
- InjecAgent ASR(DEF) − ASR(best prompt).

## Limits fixed now

- **Same samples as PREREG_X,** chosen for comparability across sizes.
- **Selection overlap:**
  - The recipe was selected (PILOT_V0) on Qwen3-1.7B, Qwen3-8B, SmolLM3-3B and OLMo-2-7B.
  - Y1's models are new sizes of a family used in selection.
  - Y2's OLMo models are new sizes of a family used in selection. Falcon3 and Yi were in PREREG_W's map but never in the lever's selection or in a benchmark.
- **Benchmark scope:** SEP is single-turn, and InjecAgent scores one agent step. A multi-turn agent benchmark (AgentDojo) comes next, after a pilot.
- **Baselines not re-run:** trained defences and V-Steer are cited, not re-run.

## Cost (anchor, computed from measured rates)

| Part | Estimate | Computed | Calibrated (× 0.83) | Basis |
|---|---|---|---|---|
| A, H100 SXM at $3.99/h | E33 | $10.88 | $9.07 | Phi-4's measured 3,805 s (both benchmarks) and 594 s (SEP) in PREREG_X, scaled by parameters; the 14B download at the measured throttled rate |
| B, H100 NVL at $3.19/h | E34 | $8.86 | $7.39 | Phi-4's 3,211 s InjecAgent, scaled to 32.8B; the 32B download not overlapped |
| **Total** | | **$19.74** | **$16.46** | |

E31 and E32 assumed one NVL for everything and are superseded. The balance was $24.68, read at 07:00 +04:00.

## Operations

**Part A.**
- **Pod:** one H100 SXM, secure cloud. `/workspace` is the pod's volume disk; if the laptop sleeps, the results wait on the stopped pod (recovery as in L10).
- **Self-stop:** `ss33.sh`. It stops the pod after packing plus up to 6 min, after 15 idle minutes, or at a 7-hour cap.

**Part B.**
- **Pod:** an H100 NVL, or another secure GPU with at least 94 GB, once one is in stock and affordable.
- **Self-stop:** `ss34.sh`, with a 4-hour cap.

**Fetch.** The laptop watcher fetches `results33.tgz` and `results34.tgz` with md5 checks.
