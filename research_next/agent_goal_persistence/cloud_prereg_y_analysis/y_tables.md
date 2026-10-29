**Y1: PARTIAL. Y2: SEP_EFFECTIVE.**

| Model | Source | SEP attack none → steering (utility) | SEP best prompt | InjecAgent ASR none → steering (valid) | InjecAgent best prompt | Verdict / X6 |
|---|---|---|---|---|---|---|
| Qwen3-1.7B | PREREG_X | 28.3% → 5.7% (U 45.7% → 47.0%) | SPOT 12.3% | 56.8% → 3.2% (valid 27.0% → 31.0%) | REMIND 41.2% | EFFECTIVE / ADDITIVE |
| Qwen3-8B | PREREG_X | 30.0% → 13.7% (U 64.7% → 67.7%) | SPOT 27.3% | 39.2% → 11.9% (valid 86.7% → 89.3%) | REMIND 34.0% | BEATS_BASELINES / ADDITIVE |
| Qwen3-14B | PREREG_Y | 37.0% → 18.3% (U 71.0% → 72.3%) | REMIND 34.0% | 29.2% → 4.6% (valid 94.7% → 93.3%) | REMIND 22.2% | NONE / ADDITIVE |
| Qwen3-32B | PREREG_Y | 40.3% → 30.0% (U 73.3% → 72.3%) | REMIND 37.7% | 27.8% → 8.6% (valid 96.0% → 92.7%) | REMIND 14.7% | EFFECTIVE / ADDITIVE |

| Held-out model (Y2, SEP only) | SEP attack none → steering (utility) | SEP best prompt | X1 | X2 | X5 (SEP) | Verdict |
|---|---|---|---|---|---|---|
| Falcon3-10B-Instruct | 48.7% → 33.0% (U 67.3% → 68.0%) | SPOT 28.3% | True | False | True | SEP_EFFECTIVE |
| Yi-1.5-9B-Chat | 47.3% → 30.7% (U 66.7% → 66.0%) | SPOT 37.7% | True | False | True | SEP_EFFECTIVE |
| OLMo-2-1124-13B-Instruct | 43.7% → 38.3% (U 69.3% → 70.0%) | SPOT 39.3% | True | False | False | NONE |
| OLMo-2-0325-32B-Instruct | 58.7% → 47.3% (U 88.7% → 89.3%) | REMIND 49.3% | True | False | True | SEP_EFFECTIVE |
