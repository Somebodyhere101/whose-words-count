#!/bin/bash
# PREREG_L completion run: the 7 models of rc22.sh whose downloads failed (a hf_xet write error, then a full disk from
# its chunk cache). Same sealed code (/workspace/agpl/code from agp18), models, seeds, batches and commands as rc22.sh;
# adds HF_HUB_DISABLE_XET=1 and clears the hub and xet caches after every model.
export HF_HOME=/root/hf HF_HUB_DISABLE_XET=1
mkdir -p /root/hf
cd /workspace/agpl/code
pip install -q "transformers==5.16.1" accelerate
while read M NT SD B; do
  [ -z "$M" ] && continue
  T=$(basename $M)
  python -c "from huggingface_hub import snapshot_download; snapshot_download('$M'); print('downloaded $M')" < /dev/null
  AGP_NTEST=$NT python -u g_eval.py --model $M --plain --seeds $SD --batch $B --out ../out_l/$T < /dev/null 2>&1 | grep -v -i warn
  rm -rf /root/hf/hub/models--$(echo $M | sed 's#/#--#') /root/hf/xet < /dev/null
  df -h /root | tail -1
done <<'LIST'
Qwen/Qwen2.5-32B-Instruct 30 1900-1939 6
allenai/OLMo-2-1124-7B-Instruct 22 1900-1959 20
allenai/OLMo-2-1124-13B-Instruct 22 1900-1959 10
allenai/OLMo-2-0325-32B-Instruct 22 1900-1939 6
tiiuae/Falcon3-3B-Instruct 30 1900-1959 20
tiiuae/Falcon3-7B-Instruct 30 1900-1959 20
tiiuae/Falcon3-10B-Instruct 30 1900-1959 20
LIST
echo CLOUD22B_DONE
