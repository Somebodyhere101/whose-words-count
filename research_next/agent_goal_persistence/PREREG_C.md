# PREREG_C: depth sweep and confirmation of the role dial in three non-Qwen families

Written 2026-10-27 14:15 AST, before any data from this run. Hashed in `PREREG_C.sha256` together with `code/select_layer.py`, `code/c_analyze.py` and `cloud/rc7.sh`.

## Why

- The stage-3 gate failed in SmolLM3-3B, Granite-3.3-8B and OLMo-2-7B at the layers chosen by analogy to Qwen: about 0.2 and 0.45 of depth.
- Each family shows a small same-sign effect at about 0.2 depth and nothing at about 0.45 depth (`PLAN_7DAY.md`, entry 2026-10-27 13:50).
- In Qwen the effect sits at about 0.46 depth and is null at 0.2.
- **Question:** is the dial weak outside Qwen, or does it sit at another depth?

## Models and cells

| Model | Layers | Cells | N_TEST | Direction file (stage-2 vR, unchanged; only these layers copied) |
|---|---|---|---|---|
| allenai/OLMo-2-1124-7B-Instruct | 32 | gF / oF (the weak text is at ceiling in OLMo) | 22, so every readout fits the 4,096-token window (all 280 families-run episodes fit through step 22) | `cloud_families/out_stage2_OLMo-2-1124-7B-Instruct/directions.pt` |
| ibm-granite/granite-3.3-8b-instruct | 40 | gW / oW (more headroom than the fixed text, base 0.11 vs 0.06) | 30 | `cloud_families/out_stage2_granite-3.3-8b-instruct/directions.pt` |
| HuggingFaceTB/SmolLM3-3B | 36 | gW / oW | 30 | `stage2_SmolLM3-3B/directions.pt` |

**Steering, as in stage 3:**
- the own cell gets −alpha·vR and the given cell +alpha·vR, while the inserted goal text is fed;
- alpha = 2;
- the control is a random direction with the same norm (fixed seed per layer);
- runner `code/steer_run.py`, batch 16, temperature 0.7.

## Phase A (exploratory selection)

- **Seeds:** 400–419.
- **Layers** (about 0.06, 0.12, 0.19, 0.25, 0.31, 0.38 and 0.46 of depth):
  - OLMo: 2, 4, 6, 8, 10, 12, 15;
  - Granite: 3, 5, 8, 10, 13, 15, 18;
  - SmolLM3: 2, 4, 7, 9, 11, 14, 17.
- **Per layer:** dir and random runs for both cells, plus both base cells.

**Selection rule** (`code/select_layer.py`):
- At each layer compute:
  - b_own = mean over seeds of (own_rand − own_dir), the drop in p_hi beyond random;
  - b_given = mean of (given_dir − given_rand), the rise beyond random.
- Select the layer with the largest min(b_own, b_given). Ties go to the shallower layer.
- If that maximum is ≤ 0, there is no phase B for that model, and it is reported as NOT FOUND.

## Phase B (confirmatory)

- **Design:** the selected layer, fresh seeds 500–539 (n = 40), alpha 2. Runs: base, dir and random for both cells.

**Gate per model** (`code/c_analyze.py`). All of these must hold:
- **(a)** own text pushed toward given lowers p_hi against the own base by ≥ 0.05 (mean). Its drop beyond the random control must be > 0, with a sign-flip p (two-sided, 20,000 permutations) < 0.05 after Holm across the models that reach phase B.
- **(b)** given text pushed toward own raises p_hi against the given base by ≥ 0.05, and beats random in the same way.
- **(c)** the mean ticker mass of each steered cell is ≥ 80% of its base.
- **(d)** OLMo only: every readout's logical context is ≤ 4,096 tokens. Otherwise the model is INVALID.

**Verdicts per model:**
- **PASS:** (a) to (c) hold.
- **PRESENT BUT WEAK:** both beyond-random tests pass, but a shift is under 0.05.
- **NOT FOUND:** otherwise.

## Readings fixed now

- **PASS in a family:** the role direction causally sets goal adherence in that family, at a family-specific depth.
- **Across families:**

  | PASS count (of 3) | Reading |
  |---|---|
  | ≥ 2 | the dial generalises beyond Qwen; its depth and strength are family-specific |
  | 1 | family-dependent |
  | 0 | "strong only in Qwen"; the other families show at most the weak version |

- The Qwen results stand as they are. This run tests only the non-Qwen families.
- Phase-A curves are reported in full as exploratory.

## Cost and time

Computed from the families run measured 2026-10-27 (A100 SXM 80 GB, $1.79/h):

| Item | Source | Value |
|---|---|---|
| boot to first result | measured | 2.4 min |
| model switch | measured | 1.75 min |
| extra model load | measured | 0.33 min |
| fetch and stop | measured | 1.7 min |

Per 20-seed condition:
- OLMo: 31.3 s at N_TEST 30, so 31.3 × 22/30 = 23.0 s;
- Granite: 24.5 s;
- SmolLM3: 24.5 s, a **guess** (no A100 timing for SmolLM3).

Per 40-seed condition:
- OLMo: 50.8 × 22/30 = 37.3 s;
- Granite: 47.4 s;
- SmolLM3: 47.4 s, a **guess**.

Phase A has 30 conditions per model, phase B 6.

**Compute:**
- OLMo: 30 × 23.0 + 6 × 37.3 = 914 s;
- Granite: 30 × 24.5 + 6 × 47.4 = 1,019 s;
- SmolLM3: 1,019 s;
- total 49.2 min.

**Total:** 2.4 + 2 × 1.75 + 3 × 0.33 + 49.2 + 1.7 = **57.8 min**, so 57.8/60 × $1.79 = **$1.72**, plus disk.
