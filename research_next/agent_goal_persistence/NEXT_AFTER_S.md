# What follows PREREG_S, per outcome (written 2026-10-28 16:05 +04:00, before any PREREG_S result)

PREREG_S launched at 12:00 UTC. This file fixes the next step for each overall verdict now, so that the result cannot steer the choice.

The suggestions come from the prior-art subagent:
- a factorial design;
- the J-space dissociation;
- a preregistered unified share;
- a parametric "from memory" source.

## One prediction that holds across branches

A unified tag implies a trade-off for defences:
- If one tag drives both obeying and believing, then pushing injected tool text toward "do not obey" must also make the model distrust that tool's facts.
- A fragmented code allows a selective defence: lower obedience to tool text while keeping belief in its facts.

So the defence question is not just "can we block injection?" It is whether blocking costs factual use of tool outputs. That cost is the axis on which a source-tag defence could beat V-Steer and prompting baselines. V-Steer restores instruction priority, but its effect on belief in tool facts is not reported in what we read.

## Branch SOURCE_MONITOR (3 of 4 models)

1. **Trade-off test.** Edit the statement tokens of tool outputs toward the lowest-authority source. Predict that obey and believe fall together, with no edit that separates them.
2. **Scale and family.** Replicate on Qwen3-14B and 32B, and on one Llama-family and one Gemma-family model, if available without new spending beyond the user's approval.
3. **Defence comparison**, on synthetic items as in S, since there are no new downloads without the user's OK. Compare against:
   - prompting ("treat tool output as data");
   - V-Steer's value-cache edit, already vendored and smoke-tested.

## Branch FRAGMENTED (3 of 4 models)

1. **Dissociation map.** Fit one direction per behaviour (obey-weighted, believe-weighted and attribution-weighted source contrasts). Test the double dissociation: does each edit move its own behaviour more than the others, against random controls?
2. **Selective defence.** Lower obedience to tool-output instructions while keeping belief in tool-output facts. Measure both against the same baselines as above. This is the capability candidate.

## Branch PARTIAL

1. **Factorial decomposition:** role slot (system / user / assistant turn) × surface style (bare / "web page" quote / "tool output" label) × content type (fact / instruction).
   - The design separates the chat-template slot from the wording that marks a source.
   - Analysis is per behaviour: the share of source variance carried by slot vs style.
2. **Unified share.** For each behaviour, measure how much of its source effect the single transplant edit reproduces (edit effect ÷ base own-minus-user difference). Fix thresholds before the run.

## All branches (Qwen3-1.7B, the only model with a J-lens fit)

**J-space dissociation.** Hypothesis: attribution, being a verbal report, needs the source information inside the workspace, while obeying may not.
- Project the source edit onto the J-space proxy (top-64 right singular vectors of J_l) and onto its complement.
- Predict that the in-workspace part moves attribution more than obedience, and the complement moves obedience more than attribution.
- Random subspace of the same size as control.

## Later, not now

**A parametric source** ("you already know this"): facts the model knows from training, against the same facts given in context.
- Source monitoring in people separates what was generated inside the mind from what was perceived.
- For a model, parametric memory is the nearest analogue.
