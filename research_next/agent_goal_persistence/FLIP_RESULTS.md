# FLIP results (2026-10-30): SAME/AGREE. gpt-oss-20b does not reverse the order; the lane stops

Rules: `FLIP.md`, sealed before data (`FLIP.sha256`). Analysis: `code/flip_analyze.py` → `cloud_flip/flip_analysis.json`.
Raw: `cloud_flip/out_flip/` (fetch md5 ed05827ad651029f1fae3ba7eea8214e; copy in `Documents/agp_res/flip`).
Run: pod agp-flip 4y6ff3khnsrge7, RTX PRO 6000 (A100 out of stock), $2.49/h, 03:54–04:04 UTC, about 9 min, about
$0.40 (estimate 25 min calibrated; ratio 0.28, the compute-ratio guess was far too high). 0 errors; terminated
(list-pods empty).
Execution note: the sealed script was run with `PYTHONUTF8=1` because Windows' default codec could not read the
gate log; no code or rule changed.

## Gate and validity

- FLIP_GATE PASS on the pod: G1 template match; G2 probed tokens identical across the four roles (19 tokens); G3
  cache total variation 0.014 (< 0.02).
- Readout mass 0.978–0.985 in every cell. Competence: every reminder raises p_goal by about 0.44 over no reminder
  (60/60 seeds, p < 0.001). Valid.

## Behaviour (60 seeds, 9100–9159)

| Cell | none | system (gF) | developer (dF) | user (uF) | own (oF) |
|---|---|---|---|---|---|
| p_goal | 0.531 | 0.965 | 0.967 | 0.974 | 0.949 |

- **Primary: D = dF − uF = −0.0075** (95% CI −0.013 to −0.003; 49 of 60 seeds negative; p < 0.001) → **SAME**.
  The user's mid-conversation reminder is followed slightly more than the developer's, as in the other 9 models.
- Secondary: system − user = −0.0095 (p < 0.001). Behaviour order user > developer ≥ system > own (developer vs
  system n.s., p 0.12).

## Axis (vR at layer 11)

- Projections: user −176.1; system −119.5; developer −118.1; own −117.8.
- **dP = user − developer = −58.1** (60/60 seeds), t = −234 vs random-direction null q95 |t| = 121 → **AGREE**
  (the user reminder sits lower, toward "given", and is followed more).
- PREREG_I-style pairs: 4 AGREE (u-d, u-g, u-o, g-o), 1 UNRESOLVED (d-o: behaviour +0.018, projection n.s.),
  1 UNDECIDED (d-g); 0 DISAGREE.
- vR quality at layer 11: T3 transfer R→A 0.91 (difference of means), 0.99 (logistic).

## Reading (fixed in FLIP.md: SAME → 10th model, no flip test)

- **No reversed model.** gpt-oss-20b was trained with an explicit system > developer > user order, yet a
  mid-conversation goal reminder works slightly *better* from the user than from the developer or system role. So
  the flip test cannot be run on this model, and by the stopping rule this lane stops (no 120b run).
- **The axis order matches again**, making gpt-oss a 10th model and a 5th family (OpenAI) where the role direction
  orders the reminder as behaviour does (4 agree, 0 disagree).
- **Caveats on that agreement:**
  - The random null is very high (q95 |t| 121): almost any direction separates user-turn tokens from developer-turn
    tokens. vR beats it about 2×, but the separation is mostly "user versus everything else". System, developer and
    own sit within 2 units of each other on vR, while the behavioural gaps are the reverse in size (user − developer
    0.0075 gets 58 units; developer − own 0.018 gets 0.3, n.s.). vR orders; it does not scale with behaviour (as in
    PREREG_I, Spearman 0.10).
  - The behavioural gaps are small (all reminder cells 0.95–0.97).
  - Mid-conversation developer/system turns never appear in the official template, so they may be out of
    distribution; the result may say that hierarchy training does not cover mid-conversation reminders, not that
    gpt-oss has no hierarchy.
- Bets: Claude gave P(SAME) 0.25 and P(FLIP) 0.35; SAME happened.
