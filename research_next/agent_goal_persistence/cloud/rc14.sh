#!/bin/bash
# PREREG_F: own-voice goal practice and reminder-free goal persistence, OLMo-2-7B-Instruct. Base, then 6 adapters per
# arm (own/given; balanced data, n 240; fresh data seeds 10000..60000), each evaluated once-loaded on fresh seeds
# 1100-1139 (fund task, swapped growth) and 120 fresh injection cases (seed 13). Adapters stay on the pod.
export HF_HOME=/root/hf
mkdir -p /root/hf
cd /workspace/agp/code
pip install -q "transformers==5.16.1" accelerate peft==0.21.2
M=allenai/OLMo-2-1124-7B-Instruct
python -c "from huggingface_hub import snapshot_download; snapshot_download('$M'); print('downloaded $M')"
export AGP_NTEST=22
python -u e_eval.py --model $M --tag base --seeds 1100-1139 --swap --inj_seed 13 --out ../out_lf 2>&1 | grep -v -i warn
for k in 1 2 3 4 5 6; do
  for arm in own given; do
    python -u lora_train.py --model $M --arm $arm --n 240 --balanced --seed0 $((k * 10000)) --out ../lora/${arm}_k$k 2>&1 | grep -v -i warn
    mkdir -p ../out_lf/lora_${arm}_k$k && cp ../lora/${arm}_k$k/train_log.json ../out_lf/lora_${arm}_k$k/
    AGP_LORA=../lora/${arm}_k$k python -u e_eval.py --model $M --tag ${arm}_k$k --seeds 1100-1139 --swap --inj_seed 13 --out ../out_lf 2>&1 | grep -v -i warn
  done
done
echo CLOUD14_DONE
