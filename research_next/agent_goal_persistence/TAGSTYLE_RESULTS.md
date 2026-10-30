# TAGSTYLE pilot results (2026-10-29, exploratory): OUTCOME NONE by rule; style moves behaviour far more than the tag

Rules: `TAGSTYLE.md` (written before data). Analysis: `code/ts_analyze.py` → `cloud_tagstyle/ts_analysis.json`.
Raw: `cloud_tagstyle/out_ts/` (fetch md5 fa65f09f3c3f02f010b515543bb0cd24).
Run: pod agp-tagstyle 10oorb9k1mq5o0, A100 SXM, 18:31–18:39 UTC, about 8 min, about $0.25 (estimate 25 min; downloads
were faster than the 0.113 GB/s rate). 0 errors; terminated (list-pods empty).

## Effects (item as unit, 60 obey and 60 believe items; T = system tag − user tag, S = system register − casual register)

| Model | Valid | obey T | obey S | believe T | believe S | attr T | attr S | Pattern |
|---|---|---|---|---|---|---|---|---|
| Qwen3-1.7B | yes | +0.070 | +0.042 (n.s.) | +0.114 | +0.053 | +0.334 | +0.697 | DISSOCIATION |
| SmolLM3-3B | no (attr mass 0.46) | −0.099 | +0.032 (n.s.) | −0.002 (n.s.) | +0.196 | +0.127 | +0.060 | INVALID |
| Qwen3-8B | yes | −0.022 (n.s.) | +0.641 | +0.086 | +0.278 | +0.600 | +0.447 | MIXED |
| OLMo-2-7B | no (attr mass 0.41) | −0.025 | +0.049 | +0.024 (n.s.) | +0.332 | +0.155 | +0.559 | INVALID |
| Granite-3.3-8B | yes | −0.082 | +0.452 | +0.069 | +0.339 | +0.027 | +0.804 | STYLE_BOTH |
| phi-4 | yes | +0.085 | +0.374 | +0.155 | +0.578 | +0.558 | +0.586 | STYLE_BOTH |

Unless marked n.s., p < 0.01 (sign-flip over items), except Qwen3-1.7B believe S (p 0.039). Valid models: 4. Counts: DISSOCIATION 1, STYLE_BOTH 2,
MIXED 1. No pattern reaches 4 valid models, so **OUTCOME NONE** and, by the rule fixed before data, this lane stops
here (no sealed confirmation).

## Descriptive reading (not a sealed claim)

- **Style dominates obedience and belief.** The style effect on obedience is larger than the tag effect in 4 of 6
  models (3 of the 4 valid ones), by a wide margin in three (Qwen3-8B +0.64 vs −0.02; Granite +0.45 vs −0.08; phi-4 +0.37 vs +0.09). For
  belief it is larger in 5 of 6 (3 of the 4 valid ones). Per cell, most of S comes from the casual register *lowering* following and belief
  (e.g. Qwen3-8B obey in a system turn: system register 0.79, plain 0.48, casual 0.04).
- **Perceived source also follows style** in 3 of the 4 models with a valid attribution readout (attr S > T; only
  narrowly in phi-4, +0.586 vs +0.557), in line with Ye et al.'s probe result; Qwen3-8B reads the tag more.
- **Consequence for Papers A/B:** the role-token (tag) effects these papers study are small next to how the text is
  written. The tag effects are real (most p < 0.01), but in three models the pre-defined register contrast moves
  obedience far more (Qwen3-8B S +0.64 vs T −0.02). S compares two rewrites (policy vs casual), a bigger change
  than one tag switch; with plain wording in a user turn the tag and a single rewrite are about equal in some
  models (phi-4 obey, Qwen3-8B belief). No ratio is claimed. This should be stated as a limitation and as consistent with Ye et al. (REFERENCES_VERIFIED W1).
- **Caveat:** the registers carry cue words ("Required response", "lol"), so "style" here mixes register with
  credibility and authority cues. The casual register may lower belief by sounding unserious rather than by sounding
  like a user. The pilot cannot separate these.
