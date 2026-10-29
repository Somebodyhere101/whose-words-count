#!/bin/bash
# PREREG_L: size sweep. Does holding a given goal (P = p_goal with system reminders) and deferring to its source
# (A = user - own) change with model size within four families? Plain cells 1/gF/uF/oF, 3-way world, fresh seeds
# 1900-1959 (32B models: 1900-1939, batch 6). Runs from /workspace/agpl so it can share the volume.
export HF_HOME=/root/hf
mkdir -p /root/hf
cd /workspace/agpl/code
pip install -q "transformers==5.16.1" accelerate
# model | N_TEST | seeds | batch
while read M NT SD B; do
  [ -z "$M" ] && continue
  T=$(basename $M)
  python -c "from huggingface_hub import snapshot_download; snapshot_download('$M'); print('downloaded $M')" < /dev/null
  AGP_NTEST=$NT python -u g_eval.py --model $M --plain --seeds $SD --batch $B --out ../out_l/$T < /dev/null 2>&1 | grep -v -i warn
  rm -rf /root/hf/hub/models--$(echo $M | sed 's#/#--#') < /dev/null
done <<'LIST'
Qwen/Qwen3-1.7B 30 1900-1959 20
Qwen/Qwen3-4B 30 1900-1959 20
Qwen/Qwen3-8B 30 1900-1959 20
Qwen/Qwen3-14B 30 1900-1959 20
Qwen/Qwen3-32B 30 1900-1939 6
Qwen/Qwen2.5-3B-Instruct 30 1900-1959 20
Qwen/Qwen2.5-7B-Instruct 30 1900-1959 20
Qwen/Qwen2.5-14B-Instruct 30 1900-1959 20
Qwen/Qwen2.5-32B-Instruct 30 1900-1939 6
allenai/OLMo-2-1124-7B-Instruct 22 1900-1959 20
allenai/OLMo-2-1124-13B-Instruct 22 1900-1959 10
allenai/OLMo-2-0325-32B-Instruct 22 1900-1939 6
tiiuae/Falcon3-3B-Instruct 30 1900-1959 20
tiiuae/Falcon3-7B-Instruct 30 1900-1959 20
tiiuae/Falcon3-10B-Instruct 30 1900-1959 20
LIST
echo CLOUD22_DONE
