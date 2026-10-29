#!/bin/bash
# PREREG_E: commitment-binding confirmation on OLMo-2-7B-Instruct. Base, then 6 adapters per arm (own/given; n 16
# conversations; fresh data seeds 1000..6000), each evaluated once-loaded on fresh seeds 900-939 (fund task and
# swapped-growth test) and 120 fresh injection cases (seed 11). Adapters stay on the pod; logs are fetched.
export HF_HOME=/root/hf
mkdir -p /root/hf
cd /workspace/agp/code
pip install -q "transformers==5.16.1" accelerate peft==0.21.2
M=allenai/OLMo-2-1124-7B-Instruct
python -c "from huggingface_hub import snapshot_download; snapshot_download('$M'); print('downloaded $M')"
export AGP_NTEST=22
python -u e_eval.py --model $M --tag base --seeds 900-939 --swap --inj_seed 11 --out ../out_le3 2>&1 | grep -v -i warn
for k in 1 2 3 4 5 6; do
  for arm in own given; do
    python -u lora_train.py --model $M --arm $arm --n 16 --seed0 $((k * 1000)) --out ../lora/${arm}_k$k 2>&1 | grep -v -i warn
    mkdir -p ../out_le3/lora_${arm}_k$k && cp ../lora/${arm}_k$k/train_log.json ../out_le3/lora_${arm}_k$k/
    AGP_LORA=../lora/${arm}_k$k python -u e_eval.py --model $M --tag ${arm}_k$k --seeds 900-939 --swap --inj_seed 11 --out ../out_le3 2>&1 | grep -v -i warn
  done
done
echo CLOUD12_DONE
