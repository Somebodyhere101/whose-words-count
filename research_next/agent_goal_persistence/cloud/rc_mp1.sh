#!/bin/bash
# MPILOT (anomaly #1 pilot, exploratory; predictions in MPILOT_PRED.md): Qwen3-8B bf16, 3-way world, 71 cells x seeds
# 3000-3039, all framed reminders at PREREG_M's insert steps. Runs from /workspace/agpmp1. Labels use "mp1", not a run
# number, so they cannot collide with the lab session's run-NN markers on the shared volume.
export HF_HOME=/root/hf HF_HUB_DISABLE_XET=1
mkdir -p /root/hf
cd /workspace/agpmp1/code
pip install -q "transformers==5.16.1" accelerate
python -c "from huggingface_hub import snapshot_download; snapshot_download('Qwen/Qwen3-8B'); print('downloaded')" < /dev/null
AGP_NTEST=30 python -u mpilot.py --cells all --seeds 3000-3039 --batch 20 --model Qwen/Qwen3-8B --out ../out_mp < /dev/null 2>&1 | grep -v -i warn
echo "files $(ls ../out_mp | wc -l) of 2840"
echo CLOUD_MP1_DONE
