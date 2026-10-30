# PREREG_R: does the role axis follow a trained priority?

DRAFT, written 2026-10-29 during REVPILOT 3, before any PREREG_R data. It is sealed (hashed) only if REVPILOT 3
says GO; the model list is filled in from REVPILOT 3's GO models at sealing, and nothing else changes then.

## Question

PREREG_H/I found that one content-free direction vR (assistant minus mean of system and user, from neutral sentences)
orders the identical goal reminder user < system < own, exactly as models obey it (user > system > own), in 9
models from 4 families. Every model had the same order, so the axis was never tested against a *different* order
(Papers A/B, Limitations).

- **AXIS FOLLOWS:** priority training that makes the system win conflicts moves system-turn text toward the "given"
  end of the *pre-existing* axis relative to user-turn text, and user-wins training moves it the other way. Then vR
  carries priority, not just the role label.
- **LABEL ONLY:** behaviour moves but the reminder's position on vR does not. Then vR encodes the role label, and
  hierarchy training acts downstream of it.

Prior art (checked 2026-10-29): Balp-Straffon et al. 2608.28648 decode and steer the conflict outcome in Llama-3.1-8B,
with no training intervention; V-Steer 2607.26228 edits value vectors by attribution; Ye et al. App. K predicts
overrides from a Systemness/Userness probe ratio. No study found that compares role representations before and after
hierarchy training.

## Design (`cloud/rc_r.sh`)

- **Models:** the REVPILOT 3 GO models (filled in at sealing), bf16, with the layer used in PREREG_H
  (Qwen3-8B 17, OLMo-2-7B 10).
- **Axis:** base vR re-extracted in-pod by `src_probe.py` (n 240) and held fixed for every condition.
- **Adapters:** `lora_train_h.py --data hier --n 48 --nopress --posbal`, arms sys and usr, fresh data seeds 6000,
  7000 and 8000: 3 adapters per arm, inputs byte-identical between arms for each seed.
- **Evaluation:** `g_eval.py --probe --rand 50`, 3-way world, cells 1 / gF / uF / oF, fresh seeds 6000–6029,
  temperature 0.7, for the base model and each merged adapter. The probe averages the hidden state over the
  reminder's own tokens (byte-identical across roles) and projects it on unit base vR and 50 seeded random unit
  directions.
- **Secondary:** each adapter's vR re-extracted (`src_probe_lora.py`); cosine with base vR at the layer.

## Rules (`code/r_analyze.py`)

As in the script's docstring:
- R1 (manipulation) and R2 (axis follows), each with a seed-level sign-flip test, adapter-level separation
  (3 vs 3; permutation p = 0.05), and for R2 a random-direction null (|t| above the 95th percentile of 50 random
  directions).
- Per model: NO_MANIPULATION, AXIS_FOLLOWS, AXIS_AGAINST or LABEL_ONLY. Overall: AXIS_FOLLOWS, LABEL_ONLY, MIXED
  or NO_MANIPULATION.

A pass is the claim "hierarchy training moves goal text along a pre-existing, content-free role axis" for these
models, this task and this training recipe. It is not a claim about how commercial hierarchy training works.

## Limitations, stated now

One task; synthetic out-of-domain training data; LoRA rank 16, n 48; 30 seeds; 2 models at most; adapters as the
unit of replication with only 3 per arm.

## Bets

Recorded before launch: Codex (cross-family) and Claude.
