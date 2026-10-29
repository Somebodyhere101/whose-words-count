#!/bin/bash
# PREREG_I: does the role direction predict the authority order across families and sizes? 3-way world, probe mode,
# fresh seeds 1500-1559 (Qwen3-32B: 1500-1539). OLMo-2-13B gets its vR from a stage-2 probe run first (layer 12).
export HF_HOME=/root/hf
mkdir -p /root/hf
cd /workspace/agp/code
pip install -q "transformers==5.16.1" accelerate
# model | direction file (or "probe") | layer | N_TEST | seeds | batch
while read M DF L NT SD B; do
  [ -z "$M" ] && continue
  T=$(basename $M)
  python -c "from huggingface_hub import snapshot_download; snapshot_download('$M'); print('downloaded $M')" < /dev/null
  if [ "$DF" = probe ]; then
    python -u src_probe.py --model $M --n 240 --out ../out_i/probe_$T < /dev/null 2>&1 | grep -v -i warn | tail -3
    DIRS=../out_i/probe_$T/directions.pt
  else
    DIRS=../dirs/$DF
  fi
  AGP_NTEST=$NT python -u g_eval.py --model $M --dirs $DIRS --layer $L --seeds $SD --batch $B --probe --out ../out_i/$T < /dev/null 2>&1 | grep -v -i warn
  rm -rf /root/hf/hub/models--$(echo $M | sed 's#/#--#') < /dev/null
done <<'LIST'
Qwen/Qwen3-1.7B dirs_q17.pt 13 30 1500-1559 20
HuggingFaceTB/SmolLM3-3B dirs_smol3.pt 7 30 1500-1559 20
Qwen/Qwen3-4B dirs_q4.pt 17 30 1500-1559 20
ibm-granite/granite-3.3-8b-instruct dirs_granite.pt 10 30 1500-1559 20
allenai/OLMo-2-1124-13B-Instruct probe 12 22 1500-1559 10
Qwen/Qwen3-32B dirs_q32.pt 20 30 1500-1539 6
LIST
echo CLOUD18_DONE
