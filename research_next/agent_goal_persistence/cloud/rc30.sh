#!/bin/bash
# PREREG_V (Phase 1): the frozen PILOT_V0 recipe against prompt defences, generation readout, fresh items (seed 2700).
# Wave 1 runs the four pilot models concurrently; wave 2 runs the two held-out families (Granite-3.3-8B, phi-4).
# Runs from /workspace/agpv/code; xet is off (L12).
export HF_HOME=/root/hf HF_HUB_DISABLE_XET=1
mkdir -p /root/hf
cd /workspace/agpv/code
pip install -q "transformers==5.16.1" accelerate
run() {
  for M in "$@"; do
    python -c "from huggingface_hub import snapshot_download; snapshot_download('$M')" < /dev/null > /dev/null 2>&1
    python -u src_defense_v.py --model $M --recipe ../recipe.json --out ../out_v/$(basename $M) < /dev/null > ../log_v_$(basename $M).txt 2>&1 &
  done
  wait
}
run Qwen/Qwen3-1.7B HuggingFaceTB/SmolLM3-3B Qwen/Qwen3-8B allenai/OLMo-2-1124-7B-Instruct
run ibm-granite/granite-3.3-8b-instruct microsoft/phi-4
grep -h -E "DEFV_DONE|Traceback|Error" ../log_v_*.txt
cp ../log_v_*.txt ../out_v/ 2>/dev/null
echo CLOUD30_DONE
