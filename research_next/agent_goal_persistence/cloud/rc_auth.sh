#!/bin/bash
# AUTHPILOT (authorship x authority, exploratory; predictions in AUTH_PRED.md): Qwen3-8B then OLMo-2-7B-Instruct, bf16,
# 3-way world, 59 cells x seeds 4000-4029. Runs from /workspace/agpauth; labels use "auth" to avoid the lab's run-NN markers.
export HF_HOME=/root/hf HF_HUB_DISABLE_XET=1
mkdir -p /root/hf
cd /workspace/agpauth/code
pip install -q "transformers==5.16.1" accelerate
while read M NT; do
  [ -z "$M" ] && continue
  T=$(basename $M)
  python -c "from huggingface_hub import snapshot_download; snapshot_download('$M'); print('downloaded $M')" < /dev/null
  AGP_NTEST=$NT python -u authpilot.py --cells all --seeds 4000-4029 --batch 20 --model $M --out ../out_auth/$T < /dev/null 2>&1 | grep -v -i warn
  echo "done $T files $(ls ../out_auth/$T | wc -l) of 1770"
  rm -rf /root/hf/hub/models--$(echo $M | sed 's#/#--#') /root/hf/xet < /dev/null
done <<'LIST'
Qwen/Qwen3-8B 30
allenai/OLMo-2-1124-7B-Instruct 22
LIST
echo CLOUD_AUTH_DONE
