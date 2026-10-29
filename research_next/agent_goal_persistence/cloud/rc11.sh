#!/bin/bash
# Binding pilot E2 (exploratory, seeds 300-339, rules in PLAN_7DAY.md 2026-10-27 18:10): OLMo-2-7B-Instruct.
# Base, then LoRA adapters for arms own/given at n 16, 48, 240; each evaluated once-loaded on the fund task, the
# swapped-growth shortcut test (base and n 240 only) and the injection test. Adapters stay on the pod.
export HF_HOME=/root/hf
mkdir -p /root/hf
cd /workspace/agp/code
pip install -q "transformers==5.16.1" accelerate peft==0.21.2
M=allenai/OLMo-2-1124-7B-Instruct
python -c "from huggingface_hub import snapshot_download; snapshot_download('$M'); print('downloaded $M')"
export AGP_NTEST=22
python -u e_eval.py --model $M --tag base --seeds 300-339 --swap --out ../out_le2 2>&1 | grep -v -i warn
for n in 16 48 240; do
  for arm in own given; do
    python -u lora_train.py --model $M --arm $arm --n $n --out ../lora/$arm$n 2>&1 | grep -v -i warn
    mkdir -p ../out_le2/lora_$arm$n && cp ../lora/$arm$n/train_log.json ../out_le2/lora_$arm$n/
    SW=""; [ $n = 240 ] && SW="--swap"
    AGP_LORA=../lora/$arm$n python -u e_eval.py --model $M --tag $arm$n --seeds 300-339 $SW --out ../out_le2 2>&1 | grep -v -i warn
  done
done
echo CLOUD11_DONE
