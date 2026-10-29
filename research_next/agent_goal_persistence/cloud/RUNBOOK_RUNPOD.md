# RunPod runbook: larger-model replications

**Target:** one A100 80 GB pod (RunPod Secure Cloud), PyTorch template, with a 100 GB container or volume disk.
**Budget:** prepaid credit of $30–50; expected use is 10–20 GPU-hours.
**Rule:** stop the pod whenever nothing is running. A stopped pod keeps its disk and costs only storage.

## What runs (in order, each with its stage gate in `../PLAN_7DAY.md`)

| # | Job | Expected time on A100 |
|---|---|---|
| 1 | Fast instrument on Qwen3-8B and Qwen3-14B (bf16), cells 1/gF/oF/gN/oN/gW/oW, seeds 300-339 | ~1–2 h |
| 2 | Stage-2 probe on Qwen3-8B and 14B | ~15 min |
| 3 | Stage-3 steering on Qwen3-8B and 14B with their own vR, layers at about 0.2 and 0.46 of depth | ~2–4 h |
| 4 | Second family, if SmolLM3-3B (laptop) can do the task: the same at bf16, plus a larger family member if one exists | ~1 h |

## Setup (on the pod)

```bash
bash setup_pod.sh          # installs pinned transformers, clones nothing, copies code from /workspace/agp
cd /workspace/agp/code
bash run_cloud.sh          # runs jobs 1-3; results land in /workspace/agp/out_*
```

Copy results back with `runpodctl send` or `scp` (see `setup_pod.sh`).

## Notes

- Code is copied from `research_next/agent_goal_persistence/code/`. Nothing private is in it, and the models download from Hugging Face.
- Runs use `agp_fast.py` and `steer_run.py` unchanged, with `--batch 16` and the gpu_lock wrapper removed: the pod is ours alone.
