#!/bin/bash
# PREREG_U: a selective defence against instructions in tool output. Splice the framed run's statement tokens
# into the plain tool run at every layer (sealed: the PREREG_T obey content-phase layer), against framing, a
# defensive system prompt and mean vectors. Same four models, fresh items (seed 2300). Runs from /workspace/agpu.
export HF_HOME=/root/hf HF_HUB_DISABLE_XET=1
mkdir -p /root/hf
cd /workspace/agpu/code
pip install -q "transformers==5.16.1" accelerate
while read M L; do
  [ -z "$M" ] && continue
  T=$(basename $M)
  python -c "from huggingface_hub import snapshot_download; snapshot_download('$M'); print('downloaded $M')" < /dev/null
  python -u src_defense.py --model $M --layer $L --n 48 --seed 2300 --batch 24 --out ../out_u/$T < /dev/null 2>&1 | grep -v -i warn
  rm -rf /root/hf/hub/models--$(echo $M | sed 's#/#--#') /root/hf/xet < /dev/null
  df -h /root | tail -1
done <<'LIST'
Qwen/Qwen3-1.7B 16
HuggingFaceTB/SmolLM3-3B 17
Qwen/Qwen3-8B 23
allenai/OLMo-2-1124-7B-Instruct 18
LIST
echo CLOUD27_DONE
