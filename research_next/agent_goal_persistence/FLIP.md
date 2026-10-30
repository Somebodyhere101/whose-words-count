# FLIP: does the role axis follow gpt-oss's trained priority? (sealed before data)

Written 2026-10-30, before any FLIP data. Chosen by the user ("Run gpt-oss flip"), with a stopping rule.

## Why

- In 9 models from 4 families (PREREG_H/I), one content-free direction vR (assistant minus mean of system and user,
  from neutral sentences) orders the same goal reminder user < system < own, which is also how the models obey it
  (user > system > own). Every model had that same order, so the axis was never tested on a model whose order
  differs (Papers A/B, Limitations). REVPILOT tried to create a reversed model with LoRA and failed (3 pilots).
- gpt-oss-20b was trained with an explicit priority order (system > developer > user). If it obeys a developer
  reminder over a user one, it is the reversed model REVPILOT could not build. Then the question is whether the
  axis reverses with behaviour (it carries priority) or keeps the role-label order (it carries the label).
- Prior art: Ye et al. (ICML 2026) App. K find, on gpt-oss-20b, that a Systemness/Userness probe ratio predicts
  user-over-system overrides (AUC .74) and that position, not tags, sets Systemness. Our reminders sit at matched
  positions, and vR is a different, content-free direction; no study found tests whether a role axis reverses
  with a trained priority.

## Design (`cloud/rc_flip.sh`)

- **Model:** openai/gpt-oss-20b, MXFP4 experts dequantized to bf16, on one A100 80 GB.
- **Format:** the harmony wrappers in `chat_fmt.harmony`, written by hand because the official template drops
  mid-conversation system and developer messages. The task prompt renders exactly as the official template renders
  a system prompt (a fixed date). Assistant turns and the readout use the final channel, so the readout skips the
  analysis channel.
- **Gate (`code/flip_gate.py`, must PASS before any data):** G1 the wrappers match `apply_chat_template`; G2 the
  probed tokens of the reminder are byte-identical in all four roles and ticker first tokens are distinct (G1 and
  G2 passed locally with the tokenizer on 2026-10-30); G3 the batched, left-padded cache gives the same next-token
  distribution as a plain forward pass (total variation < 0.02). If the gate fails, nothing else runs.
- **Axis:** vR re-extracted in-pod by `src_probe.py --n 240`, with the harmony system role as "system". **Layer 11**
  (depth 0.46 of 24, the depth used for the Qwen models in PREREG_I; also the layer used on gpt-oss-20b in "Steering
  Role Confusion"). No other layer is analysed.
- **Cells (`g_eval.py --probe --dev --rand 50`, 3-way world, N_TEST 30, temperature 0.7):** 1 (no reminder), gF
  (the fixed goal text as a harmony system turn), dF (developer turn), uF (user turn), oF (the agent's own final-
  channel turn). Fresh seeds **9100–9159** (n 60), batch 20. The probe averages the hidden state at layer 11 over
  the reminder's own tokens and projects it on unit vR and on 50 seeded random unit directions.

## Rules (`code/flip_analyze.py`)

**Validity.** Gate PASS; mean readout mass ≥ 0.5 in every cell; competence: at least one of gF, dF, uF exceeds
cell 1 in p_goal by ≥ 0.10 with sign-flip p < 0.05. Otherwise the verdict is INVALID.

**Behaviour (primary pair: developer vs user).** D = p_goal(dF) − p_goal(uF) per seed, sign-flip test over seeds.
- FLIP: D > 0, p < 0.05 (the developer reminder is followed more, the reverse of the 9 models).
- SAME: D < 0, p < 0.05.
- TIE: otherwise.

The developer role is primary because that is where the official template puts a deployer's system prompt; it is
the counterpart of the system turn in the other 9 models. The harmony system role (gF vs uF) is secondary.

**Axis (layer 11).** dP = proj(uF) − proj(dF) per seed (higher authority should sit lower on vR, i.e. more "given").
t = mean / (sd / √n). Null: the same t on each of the 50 random directions; q95 = 95th percentile of their |t|.
- AGREE: dP has the sign of D, sign-flip p < 0.05 and |t| > q95.
- AGAINST: dP has the opposite sign, p < 0.05 and |t| > q95.
- NULL: otherwise.

**Reported, not gating:** the full behaviour and projection orders over system, developer, user and own; the six
pairs scored as in PREREG_I (decided / agree / disagree / unresolved); the secondary system-vs-user pair.

## Readings fixed now

| Behaviour | Axis | Reading |
|---|---|---|
| FLIP | AGREE | The axis reverses with the trained priority: it carries priority, not the role label (one model, one task; a natural experiment, not a controlled intervention). |
| FLIP | AGAINST | Behaviour reverses but the axis keeps the label order: the axis carries the role label; the "authority axis" claim narrows to models whose order is user > system. |
| FLIP | NULL | Behaviour reverses; the axis test is inconclusive. |
| SAME | any | gpt-oss also follows the user's mid-conversation reminder over the developer's, despite hierarchy training. No reversed model, so no flip test; reported as a 10th model, with agreement scored as in PREREG_I. |
| TIE | any | No order to test. |

**Stopping rule.**
- FLIP (any axis result): one follow-up is allowed, a replication on gpt-oss-120b. Its cost is computed before
  launch.
- SAME, TIE or INVALID: this lane stops. No further spending on priority reversals; the result goes into the
  11-02 consolidation.

## Limitations, stated now

- Mid-conversation developer and system messages never appear in the official template, so they may be out of
  distribution for gpt-oss. A SAME result may mean "hierarchy training does not cover mid-conversation reminders"
  rather than "no hierarchy".
- The final channel is prefilled, skipping the analysis channel the model would normally write first.
- One model, one task, one layer; vR is built from the harmony system role and the user role.
- Ceiling risk: if gpt-oss holds the goal near p = 1 without any reminder, competence fails (INVALID).

## Bets (recorded before launch)

- **Claude:** P(FLIP) 0.35, P(SAME) 0.25, P(TIE or INVALID, mostly ceiling) 0.40. Given FLIP: AGREE 0.40,
  AGAINST 0.30, NULL 0.30.
- Codex was not asked this time.

## Cost (computed before launch, anchor estimate E35)

3 + 13.8 GB / 0.113 GB/s / 60 + 3 loads × 1.5 + 1200 × 0.1 s / 60 + 5 cells × 45 s × 2.4 × 2 / 60 = 29.5 min, calibrated
×0.86 → about 25 min, about $0.75 at $1.79/h (A100 SXM). Guessed inputs: load time, probe forward time, the 2.4×
compute ratio. Hard cap 90 min ($2.69) by the self-stop.
