#!/bin/bash
# PREREG_M: do models obey what sounds least like themselves? Minimal-pair headers (agp_fast.FRAMESETS["m"]) on the goal
# reminder in system and user turns; 3-way world, probe mode with 50 seeded random null directions, fresh seeds
# 2000-2059. Runs from /workspace/agpm on the shared volume. xet disabled and caches cleared per model (lesson L12).
export HF_HOME=/root/hf HF_HUB_DISABLE_XET=1
mkdir -p /root/hf
cd /workspace/agpm/code
pip install -q "transformers==5.16.1" accelerate
# model | direction file | layer | N_TEST
while read M DF L NT; do
  [ -z "$M" ] && continue
  T=$(basename $M)
  python -c "from huggingface_hub import snapshot_download; snapshot_download('$M'); print('downloaded $M')" < /dev/null
  AGP_NTEST=$NT python -u g_eval.py --model $M --dirs ../dirs/$DF --layer $L --seeds 2000-2059 --batch 20 --probe --frames --frameset m --rand 50 --out ../out_m/$T < /dev/null 2>&1 | grep -v -i warn
  rm -rf /root/hf/hub/models--$(echo $M | sed 's#/#--#') /root/hf/xet < /dev/null
  df -h /root | tail -1
done <<'LIST'
Qwen/Qwen3-1.7B dirs_q17.pt 13 30
HuggingFaceTB/SmolLM3-3B dirs_smol3.pt 7 30
Qwen/Qwen3-4B dirs_q4.pt 17 30
Qwen/Qwen3-8B dirs_q8.pt 17 30
allenai/OLMo-2-1124-7B-Instruct dirs_olmo.pt 10 22
Qwen/Qwen3-14B dirs_q14.pt 18 30
LIST
echo CLOUD23_DONE
