#!/bin/bash
# PREREG_S: source monitoring. Five sources (system, user, own turn, quoted web page, tool output) for identical text;
# obey / believe / attribute behaviour, a 5-way source readout, and a usr<->own tag-transplant edit with random
# controls. Four models, two families. Runs from /workspace/agps on the shared volume; xet off (lesson L12).
export HF_HOME=/root/hf HF_HUB_DISABLE_XET=1
mkdir -p /root/hf
cd /workspace/agps/code
pip install -q "transformers==5.16.1" accelerate
# model | decision layer
while read M L; do
  [ -z "$M" ] && continue
  T=$(basename $M)
  python -c "from huggingface_hub import snapshot_download; snapshot_download('$M'); print('downloaded $M')" < /dev/null
  python -u src_monitor.py --model $M --layer $L --n 60 --seed 2100 --batch 32 --out ../out_s/$T < /dev/null 2>&1 | grep -v -i warn
  rm -rf /root/hf/hub/models--$(echo $M | sed 's#/#--#') /root/hf/xet < /dev/null
done <<'LIST'
Qwen/Qwen3-1.7B 13
HuggingFaceTB/SmolLM3-3B 7
Qwen/Qwen3-8B 17
allenai/OLMo-2-1124-7B-Instruct 10
LIST
echo CLOUD25_DONE
