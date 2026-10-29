#!/bin/bash
# PREREG_K: is the role direction necessary for the authority order? Unit vR is projected out of the embedding and every
# layer output while the goal reminder is read; cells 1/gF/uF/oF plain, gF/uF/oF ablated and random-ablated; 3-way world;
# fresh seeds 1800-1859 (Qwen3-32B: 1800-1839, batch 6). Runs from /workspace/agpk so it can share the volume.
export HF_HOME=/root/hf
mkdir -p /root/hf
cd /workspace/agpk/code
pip install -q "transformers==5.16.1" accelerate
# model | direction file | layer | N_TEST | seeds | batch
while read M DF L NT SD B; do
  [ -z "$M" ] && continue
  T=$(basename $M)
  python -c "from huggingface_hub import snapshot_download; snapshot_download('$M'); print('downloaded $M')" < /dev/null
  AGP_NTEST=$NT python -u g_eval.py --model $M --dirs ../dirs/$DF --layer $L --seeds $SD --batch $B --ablate --out ../out_k/$T < /dev/null 2>&1 | grep -v -i warn
  rm -rf /root/hf/hub/models--$(echo $M | sed 's#/#--#') < /dev/null
done <<'LIST'
Qwen/Qwen3-4B dirs_q4.pt 17 30 1800-1859 20
Qwen/Qwen3-8B dirs_q8.pt 17 30 1800-1859 20
allenai/OLMo-2-1124-7B-Instruct dirs_olmo.pt 10 22 1800-1859 20
Qwen/Qwen3-14B dirs_q14.pt 18 30 1800-1859 20
Qwen/Qwen3-32B dirs_q32.pt 20 30 1800-1839 6
LIST
echo CLOUD21_DONE
