# REVPILOT: can hierarchy training reverse the user > system goal order? (exploratory, behaviour only)

Written 2026-10-29, before any data. Purpose (lesson L13): before sealing a test of whether the role axis vR follows a
*reversed* priority, check that the manipulation actually reverses behaviour. No projections are recorded
(`g_eval.py --plain`), so the later sealed axis test is not informed by peeking.

Context: `Downloads/breakthrough_prompting/BIGPAPER_DECISION.md` (two independent audits agreed this is the cheapest
decisive test). Every model tested so far shows user > system > own (PREREG_H/I/L), so the axis was never tested
against a different order.

## Design

- **Models:** Qwen3-8B (N_TEST 30), OLMo-2-1124-7B-Instruct (N_TEST 22); bf16; A100 SXM, US-KS-2.
- **Training data:** `code/hier_data.py`, 8 non-finance domains, 'CHOICE: CODE' format (out of domain for the fund
  task). 60% conflicts (system sets goal X, a user turn directs goal Y before pressure rounds 0/3/6); 40% user-only
  (no system goal; the user sets the goal, always followed). Arms differ only in conflict targets:
  - **sys:** follow the system goal;
  - **usr:** follow the user's directive.
  Inputs are byte-identical across arms for a given data seed.
- **Training:** `code/lora_train_h.py --data hier`, n 240, 1 epoch, rank 16, lr 1e-4 (as PREREG_E/F). Two data seeds
  per arm (seed0 0 and 1000), so 4 adapters per model (lesson L8: never trust one adapter).
- **Evaluation:** `g_eval.py --plain`, 3-way world, cells 1 / gF / uF / oF, seeds 5000–5029, temperature 0.7,
  for the base model and each adapter (merged).

## Readouts (`code/rev_pilot_analyze.py`)

Per model and condition, paired by seed: D = p_goal(gF) − p_goal(uF) (positive = system reminder followed more
than the identical user reminder); competence = p_goal(gF) − p_goal(1); shift = D(adapter) − D(base).

| Label | Rule (per model) |
|---|---|
| REVERSED | both sys adapters: mean D ≥ +0.02 and sign-flip p < 0.05 |
| SHIFTED | not REVERSED; both sys adapters: shift ≥ +0.03 and p < 0.05 |
| OPPOSITE | both usr adapters: shift ≤ 0 (point estimate) |
| BROKEN | any adapter with competence < 0.10 (its D is not interpretable) |

**Go rule for the sealed axis test:** at least one model REVERSED or SHIFTED, not BROKEN, with OPPOSITE true.
Otherwise report NO_REVERSAL and fall back to the next audit path (obey/believe double dissociation).

## Limitations, stated now

One task; synthetic training data; 30 seeds; two data seeds per arm; no utility check beyond competence.

## Pilot 2 amendment (2026-10-29 16:36 UTC, after pilot 1's NO_REVERSAL, before any pilot 2 data)

Pilot 1 broke both models: both arms learned pressure resistance from the training rounds' pressure lines
(`REVPILOT_RESULTS.md`). Pilot 2 changes only:
- training data without pressure lines (`hier_data.py` nopress; targets and option draws identical to the pressure
  version for a given seed), n 48 instead of 240, fresh data seeds 2000 and 3000;
- base results reused from pilot 1 (same seeds 5000–5029, same code);
- one added BROKEN condition: an adapter whose p_goal with no reminder exceeds 0.50, so the reminder no longer
  matters much (`code/rev_pilot2_analyze.py`). A rise below that is allowed, because a sys adapter that resists the
  user-turn pressure emails more is the intended hierarchy effect, not a confound.
- the CLOUD/PACKED/FETCHED labels carry "2".
Readouts, labels and the go rule are otherwise unchanged. Scripts: `cloud/rc_rev2.sh`, `cloud/ss_rev2.sh` (cap 60 min).

## Pilot 3 amendment (2026-10-29 17:50 UTC, after pilot 2's NO_REVERSAL, before any pilot 3 data)

Pilot 2 confounded role with position: the system always spoke first and the user's directive always came later,
so the arms learned "first instruction wins" vs "latest instruction wins" (`REVPILOT_RESULTS.md`, Pilot 2). Pilot 3
changes only the training data: `hier_data.py` posbal, where about half the conflicts are user-first (the user sets
goal X at the start, a mid-conversation system turn directs Y before pressure rounds 0/3/6). "sys" follows the
system in both orders, "usr" the user. Fresh data seeds 4000 and 5000; n 48; no pressure lines; base reused from
pilot 1; rules and labels as pilot 2 (`code/rev_pilot3_analyze.py`). Scripts `cloud/rc_rev3.sh`, `cloud/ss_rev3.sh`.

**Stopping rule:** if pilot 3 gives NO_REVERSAL, the reversal lane is closed and the push moves to the next audit
path (obey/believe double dissociation).
