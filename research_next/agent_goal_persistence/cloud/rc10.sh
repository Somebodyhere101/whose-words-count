#!/bin/bash
# Pilot (exploratory, seeds 300-339) for the commitment-binding fine-tune on OLMo-2-7B-Instruct: LoRA adapters trained on
# own-arm and given-arm data (sft_data, n 240, 1 epoch); base, own and given evaluated on the held-out fund task
# (cells 1/gF/oF/uF, N_TEST 22) and on the injection test (n 120). Adapters stay on the pod; logs are fetched.
export HF_HOME=/root/hf
mkdir -p /root/hf
cd /workspace/agp/code
pip install -q "transformers==5.16.1" accelerate peft==0.21.2
M=allenai/OLMo-2-1124-7B-Instruct
python -c "from huggingface_hub import snapshot_download; snapshot_download('$M'); print('downloaded $M')"
for arm in own given; do
  python -u lora_train.py --model $M --arm $arm --n 240 --out ../lora/$arm 2>&1 | grep -v -i warn
  mkdir -p ../out_le/lora_$arm && cp ../lora/$arm/train_log.json ../out_le/lora_$arm/
done
for v in base own given; do
  if [ $v = base ]; then unset AGP_LORA; else export AGP_LORA=../lora/$v; fi
  AGP_NTEST=22 python -u agp_fast.py --model $M --conds 1,gF,oF,uF --seeds 300-339 --batch 20 --out ../out_le/fast_$v 2>&1 | grep -v -i warn
  python -u inj_eval.py --model $M --n 120 --batch 12 --out ../out_le/inj_$v.json 2>&1 | grep -v -i warn
done
echo CLOUD10_DONE
