# REVPILOT results (2026-10-29, exploratory): NO_REVERSAL, because both training arms taught pressure resistance

Rules: `REVPILOT.md` (written before data). Analysis: `code/rev_pilot_analyze.py` → `cloud_revpilot/rev_pilot.json`.
Raw: `cloud_revpilot/out_rev/` (fetch md5 aecfdfa780185b80a652a9fa57e50446).

**Run:** pod agp-revpilot a5ayyjl0dtnhsn, A100 SXM, US-MD-1, 15:34–16:34 UTC, about 60 min, about $1.79 (estimate 55
min calibrated; ratio 1.09). 0 errors. Terminated after the md5-verified fetch. Training took 134–149 s per adapter.

## Mean p_goal per cell (seeds 5000–5029)

| Model | Condition | none (1) | system (gF) | user (uF) | own (oF) | D = gF − uF |
|---|---|---|---|---|---|---|
| Qwen3-8B | base | 0.158 | 0.931 | 0.963 | 0.913 | −0.032 |
| | sys0 / sys1000 | 0.999 / 0.997 | 0.999 / 0.998 | 0.999 / 0.998 | 0.999 / 0.997 | ≈0 |
| | usr0 / usr1000 | 0.998 / 0.996 | 0.998 / 0.996 | 0.998 / 0.996 | 0.999 / 0.997 | ≈0 |
| OLMo-2-7B | base | 0.093 | 0.741 | 0.834 | 0.667 | −0.093 |
| | sys0 / sys1000 | 0.654 / 0.948 | 0.870 / 0.959 | 0.904 / 0.952 | 0.852 / 0.958 | −0.034 / +0.007 |
| | usr0 / usr1000 | 0.101 / 0.367 | 0.867 / 0.955 | 0.913 / 0.967 | 0.819 / 0.951 | −0.047 / −0.013 |

Base models replicate user > system > own (D < 0 in both).

## Verdict by the pre-written rules: NO_REVERSAL (BROKEN in both models)

- **Qwen3-8B:** every adapter, *both arms*, drives p_goal to about 0.998 in every cell, including with no reminder
  at all. Competence (gF − none) collapses to about 0, so D is uninterpretable (BROKEN).
- **OLMo-2-7B:** both arms raise p_goal; sys1000 also reaches ceiling with no reminder (competence 0.011, BROKEN).
  D moves toward zero in *both* arms (shift +0.06 / +0.10 sys, +0.05 / +0.08 usr), so OPPOSITE fails.

## Reading

The design taught the wrong thing. Every training round carried a third-party pressure line, and in both arms the
targets never follow pressure unless it happens to agree with the goal being followed. Both arms therefore learned
"ignore pressure", which is exactly what the fund world measures. That ceiling hides any role-order effect. This is
the same failure as PREREG_E/F (a shortcut shared by both arms; lessons L8 and L13), now through the training data's
pressure lines rather than through choice values.

No conclusion about the role axis follows. The question is untested, not answered.

## Fix for a second pilot (not run; needs credits)

- Training rounds without pressure lines (`hier_data.py --nopress`), so the arms differ only in which role wins a
  conflict.
- A lower dose (n 48, as in E2/E4) to stay off the ceiling, and the no-reminder cell as a guard: an adapter that
  raises p_goal(1) by more than 0.10 counts as BROKEN before D is read.
- A user-turn pressure check is then a *prediction*, not a confound: the sys arm should resist the user-turn
  pressure emails more, and the usr arm less.

# Pilot 2 (2026-10-29, exploratory): NO_REVERSAL; role was confounded with position

Run: pod agp-revpilot2 hp6lqv7ip3ftwi, A100 SXM, US-KS-2, 17:16–17:49 UTC, about 33 min, about $1.0 (estimate 33
min calibrated). 0 errors; terminated after the md5-verified fetch. Rules: REVPILOT.md "Pilot 2 amendment".
Analysis: `cloud_revpilot2/rev_pilot2.json` (base reused from pilot 1).

| Model | Condition | none | gF | uF | oF | D | label inputs |
|---|---|---|---|---|---|---|---|
| Qwen3-8B | base | 0.158 | 0.931 | 0.963 | 0.913 | −0.032 | |
| | sys2000 / sys3000 | 0.390 / 0.526 | 0.568 / 0.774 | 0.619 / 0.787 | 0.547 / 0.721 | −0.050 / −0.013 (n.s.) | none > 0.50 in sys3000 |
| | usr2000 / usr3000 | 0.416 / 0.368 | 0.971 / 0.947 | 0.987 / 0.977 | 0.958 / 0.928 | −0.016 / −0.030 | |
| OLMo-2-7B | base | 0.093 | 0.741 | 0.834 | 0.667 | −0.093 | |
| | sys2000 / sys3000 | 0.072 / 0.198 | 0.128 / 0.448 | 0.132 / 0.614 | 0.129 / 0.486 | −0.004 / −0.166 | competence 0.057 in sys2000 |
| | usr2000 / usr3000 | 0.067 / 0.045 | 0.657 / 0.589 | 0.857 / 0.770 | 0.589 / 0.464 | −0.201 / −0.181 | |

Labels: both models BROKEN (Qwen sys3000 follows the goal 0.526 with no reminder; OLMo sys2000 competence 0.057);
neither REVERSED nor SHIFTED. NO_REVERSAL.

**Reading.** The sys adapters lowered the following of *every* mid-conversation reminder, system and user alike
(Qwen gF 0.931 → 0.568/0.774), and the usr adapters widened the user advantage in OLMo (D −0.093 → −0.20/−0.18).
In the training data the system always spoke first and the user's directive always came later, so "sys" taught
"keep the first instruction, ignore later ones" and "usr" taught "the latest instruction wins". Role and position
were confounded. Exploratory and post hoc; the usr-arm widening in OLMo fits a recency rule, not only a role rule.

**Pilot 3 (last attempt for this lane):** balance order in the training data (system-first and user-first conflicts
in equal numbers), so the arms can only learn which role wins. Stopping rule, fixed now: if pilot 3 also gives
NO_REVERSAL, the reversal lane is closed and the push moves to the next audit path.

# Pilot 3 (2026-10-29, exploratory): NO_REVERSAL; the reversal lane is closed by the stopping rule

Run: pod agp-revpilot3 h2pa97n9e7b0xt, A100 SXM, US-KS-2, 17:51–18:23 UTC, about 32 min, about $0.95. 0 errors;
fetch md5 c8a1fe785f5718aaa29defb65509a596; terminated (list-pods empty). Rules: REVPILOT.md "Pilot 3 amendment"
(order-balanced conflicts). Analysis: `cloud_revpilot3/rev_pilot3.json`. (Pilot 2's fetch md5 was
616295cbf6c36f9cf3cb40d4480ca031.)

| Model | Condition | none | gF | uF | oF | D |
|---|---|---|---|---|---|---|
| Qwen3-8B | base | 0.158 | 0.931 | 0.963 | 0.913 | −0.032 |
| | sys4000 / sys5000 | 0.551 / 0.505 | 0.811 / 0.877 | 0.878 / 0.912 | 0.814 / 0.847 | −0.067 / −0.035 |
| | usr4000 / usr5000 | 0.630 / 0.419 | 0.918 / 0.848 | 0.944 / 0.931 | 0.876 / 0.766 | −0.026 / −0.083 |
| OLMo-2-7B | base | 0.093 | 0.741 | 0.834 | 0.667 | −0.093 |
| | sys4000 / sys5000 | 0.196 / 0.081 | 0.681 / 0.446 | 0.798 / 0.687 | 0.662 / 0.448 | −0.117 / −0.241 |
| | usr4000 / usr5000 | 0.209 / 0.100 | 0.707 / 0.576 | 0.856 / 0.834 | 0.725 / 0.597 | −0.149 / −0.258 |

Labels: Qwen BROKEN (no-reminder following above 0.50 in three adapters), OLMo not broken but neither REVERSED nor
SHIFTED (OPPOSITE true). NO_REVERSAL.

**Reading (exploratory).** With order balanced, the arms no longer differ: mean D over each arm's two adapters is
sys − usr = +0.004 in Qwen and +0.024 in OLMo, far smaller than the spread between data seeds within an arm (OLMo
sys4000 −0.117 vs sys5000 −0.241). Out-of-domain priority training (n 48, rank 16) did not transfer to which chat
role's goal reminder the agent follows; the user > system order survived every adapter in both models (D < 0 in all
16 pilot-2/3 adapters, including the 11 not labelled BROKEN). Count corrected after a check by the peer session. Lesson L8 holds again: the data seed matters more than the arm.

**Stopping rule applied:** the reversal lane is closed. No PREREG_R was sealed or run (`PREREG_R.md` stays a draft).
REVPILOT total: about $3.8 for three pilots.
