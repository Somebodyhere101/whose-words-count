#!/bin/bash
# REVPILOT 3 (exploratory, rules in REVPILOT.md "Pilot 3"): 4 hierarchy adapters (sys/usr x data seeds 4000/5000;
# n 48, no pressure lines, order-balanced conflicts) per model; base reused from pilot 1. Each adapter
# is evaluated with g_eval.py --plain on seeds 5000-5029. Adapters stay on the container disk (/root/lora_rev3);
# outputs and train logs go to /workspace/agprev3/out_rev. Labels use "rev".
export HF_HOME=/root/hf HF_HUB_DISABLE_XET=1
mkdir -p /root/hf /root/lora_rev3
cd /workspace/agprev3/code
pip install -q "transformers==5.16.1" accelerate peft==0.21.2
while read M NT; do
  [ -z "$M" ] && continue
  T=$(basename $M); O=../out_rev/$T
  python -c "from huggingface_hub import snapshot_download; snapshot_download('$M'); print('downloaded $M')" < /dev/null
  export AGP_NTEST=$NT
  for arm in sys usr; do
    for s0 in 4000 5000; do
      A=/root/lora_rev3/$T/$arm$s0
      python -u lora_train_h.py --model $M --data hier --arm $arm --n 48 --nopress --posbal --seed0 $s0 --out $A < /dev/null 2>&1 | grep -v -i warn
      mkdir -p $O/$arm$s0 && cp $A/train_log.json $O/$arm$s0/
      AGP_LORA=$A python -u g_eval.py --model $M --plain --seeds 5000-5029 --batch 20 --out $O/$arm$s0 < /dev/null 2>&1 | grep -v -i warn
    done
  done
  echo "done $T"; df -h /root | tail -1
  rm -rf /root/hf/hub/models--$(echo $M | sed 's#/#--#') /root/hf/xet < /dev/null
done <<'LIST'
Qwen/Qwen3-8B 30
allenai/OLMo-2-1124-7B-Instruct 22
LIST
echo CLOUD_REV3_DONE
