#!/bin/bash
# PREREG_T: where is the source signal each behaviour uses? Activation patching (own->usr, sys->usr) of the marker
# tokens, the content tokens and everything after the turn, at every layer, for obey / believe / attribute.
# Same four models and decision layers as PREREG_S, fresh items (seed 2200). Runs from /workspace/agpt; xet off (L12).
export HF_HOME=/root/hf HF_HUB_DISABLE_XET=1
mkdir -p /root/hf
cd /workspace/agpt/code
pip install -q "transformers==5.16.1" accelerate
while read M L; do
  [ -z "$M" ] && continue
  T=$(basename $M)
  python -c "from huggingface_hub import snapshot_download; snapshot_download('$M'); print('downloaded $M')" < /dev/null
  python -u src_patch.py --model $M --layer $L --n 48 --seed 2200 --batch 24 --out ../out_t/$T < /dev/null 2>&1 | grep -v -i warn
  rm -rf /root/hf/hub/models--$(echo $M | sed 's#/#--#') /root/hf/xet < /dev/null
  df -h /root | tail -1
done <<'LIST'
Qwen/Qwen3-1.7B 13
HuggingFaceTB/SmolLM3-3B 7
Qwen/Qwen3-8B 17
allenai/OLMo-2-1124-7B-Instruct 10
LIST
echo CLOUD26_DONE
