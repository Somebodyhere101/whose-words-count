#!/bin/bash
# Binding pilot E4 (exploratory; rules in PLAN_7DAY.md 2026-10-27 20:10): OLMo-2-7B-Instruct, balanced training data
# (half the rounds have pressure that agrees with the goal). Base, then own/given adapters at n 48 and 240, each
# evaluated once-loaded on fresh seeds 1000-1039 (fund task, swapped-growth test) and the injection test (seed 11).
export HF_HOME=/root/hf
mkdir -p /root/hf
cd /workspace/agp/code
pip install -q "transformers==5.16.1" accelerate peft==0.21.2
M=allenai/OLMo-2-1124-7B-Instruct
python -c "from huggingface_hub import snapshot_download; snapshot_download('$M'); print('downloaded $M')"
export AGP_NTEST=22
python -u e_eval.py --model $M --tag base --seeds 1000-1039 --swap --inj_seed 11 --out ../out_le4 2>&1 | grep -v -i warn
for n in 48 240; do
  for arm in own given; do
    python -u lora_train.py --model $M --arm $arm --n $n --balanced --out ../lora/${arm}${n}b 2>&1 | grep -v -i warn
    mkdir -p ../out_le4/lora_${arm}${n}b && cp ../lora/${arm}${n}b/train_log.json ../out_le4/lora_${arm}${n}b/
    AGP_LORA=../lora/${arm}${n}b python -u e_eval.py --model $M --tag ${arm}${n}b --seeds 1000-1039 --swap --inj_seed 11 --out ../out_le4 2>&1 | grep -v -i warn
  done
done
echo CLOUD13_DONE
