#!/bin/bash
# Jobs 1-3 of RUNBOOK_RUNPOD.md. Resumable: every runner skips results that already exist.
export HF_HOME=/workspace/hf
cd /workspace/agp/code
for M in Qwen3-8B Qwen3-14B; do
  python -u agp_fast.py --model Qwen/$M --conds 1,gF,oF,gN,oN,gW,oW --seeds 300-339 --batch 16 --out ../out_fast_$M 2>&1 | grep -v -i warn
  python -u src_probe.py --model Qwen/$M --n 240 --out ../out_stage2_$M 2>&1 | grep -v -i warn
done
# Stage-3 steering: layers at about 0.2 and 0.46 of depth (Qwen3-8B: 36 layers -> 7,17; Qwen3-14B: 40 -> 8,18).
python -u steer_run.py --model Qwen/Qwen3-8B --cells gF,oF --dirs ../out_stage2_Qwen3-8B/directions.pt --layers 7,17 --batch 16 --out ../out_stage3_Qwen3-8B
python -u steer_run.py --model Qwen/Qwen3-14B --cells gF,oF --dirs ../out_stage2_Qwen3-14B/directions.pt --layers 8,18 --batch 16 --out ../out_stage3_Qwen3-14B
echo CLOUD_DONE
