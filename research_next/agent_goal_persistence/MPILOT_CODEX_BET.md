I’ll verify the cited baselines, then give the blind probabilities and flag any ambiguity that would affect scoring.

**The main design issue is that O7 is a crossover, not an interaction test.** An interaction could exist even if assistant placement remains worse than system placement. Also, Dana being neutral would not establish that the literal word “another” causes the penalty; named and unnamed third parties differ in other ways.

These are **judgmental probabilities conditional on the calibration gate passing**, using your supplied baseline summaries. I couldn’t independently verify the cited papers here. Without sample sizes, I’m betting on the underlying effects meeting the thresholds; probabilities for noisy observed estimates would depend on precision.

For scoring, I interpret O2 and O4 as averaged over system/user placements, O3 as requiring the threshold in **both** placements, and O6 as using each paraphrase set’s system/user average.

| Outcome | P | Reasoning |
|---|---:|---|
| **O1: other penalty** | **0.78** | The original Qwen3-8B self–other separation is substantial, and “another manager” explicitly distances the plan from the acting agent. However, without a neutral baseline, that separation does not identify how much is an other penalty. |
| **O2: self bonus** | **0.50** | Self-label effects against blind baselines, as reported for Chae et al., make this plausible. But the original −0.090 difference is equally compatible with neutral ≈ self and a substantial other penalty. |
| **O3: Your > My** | **0.62** | “Your” consistently addresses the model in system/user messages; “My” attributes the plan to those messages’ speaker. That predicts the stated direction, but neither supplied baseline directly establishes a ≥0.02 effect in both placements. |
| **O4: Dana ≈ neutral** | **0.35** | Third-party attribution itself could reduce adoption, so removing “another” need not eliminate the penalty. The reported judge studies make effects from attribution beyond one particular word plausible. |
| **O5: turn gap survives** | **0.80** | Qwen3-8B already shows a +0.024 system–own gap, and the supplied authorship study supports effects carried by turns. The threshold is close to that baseline, while OLMo’s template sensitivity weakens confidence in generalization. |
| **O6: ≥8/10 matching signs** | **0.80** | The original direction appears across five of six models, including a sizable Qwen3-8B effect. That supports semantic robustness, although cross-model replication is weaker evidence for paraphrase robustness than direct paraphrase data. |
| **O7: My own assistant > system** | **0.18** | Speaker congruence could improve first-person wording in assistant messages. An absolute reversal must additionally overcome the existing system advantage; the supplied baselines do not demonstrate that. |

**The single outcome that would most change my view is O5.** A precisely estimated zero or reversed gap with no header and matched position would directly weaken the central placement claim. Merely obtaining a gap just below 0.02 would change my view much less.

**If O1 is true and O2 is false**, I would conclude that the wording result is primarily evidence for **discounting another manager’s plan**, with no demonstrated self bonus at the specified threshold. I would soften “self-attribution increases goal-following” accordingly. That result alone would not explain the separate assistant-turn disadvantage.

One calibration caution: reproducing only **D < 0** is a weak gate if the estimate is noisy. Record its magnitude and uncertainty; an arbitrarily small negative estimate does not establish that the original effect survived quantization.

---
session_id: 01a1866b-bd3f-7b00-882c-81d7267fd9aa