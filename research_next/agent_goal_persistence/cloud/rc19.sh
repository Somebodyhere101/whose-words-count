#!/bin/bash
# Framing pilot before PREREG_J: social-authority headers (agp_fast.FRAMES) on the goal reminder, in system and user
# turns. 3-way world, probe mode with 50 seeded random null directions, pilot seeds 1600-1619, Qwen3-8B (layer 17) and
# OLMo-2-7B-Instruct (layer 10, N_TEST 22). Behaviour is analysed (j_pilot_analyze.py); projection values are not read
# before PREREG_J is sealed.
export HF_HOME=/root/hf
mkdir -p /root/hf
cd /workspace/agp/code
pip install -q "transformers==5.16.1" accelerate
for spec in "Qwen/Qwen3-8B dirs_q8.pt 17 30" "allenai/OLMo-2-1124-7B-Instruct dirs_olmo.pt 10 22"; do
  set -- $spec; M=$1; DF=$2; L=$3; NT=$4; T=$(basename $M)
  python -c "from huggingface_hub import snapshot_download; snapshot_download('$M'); print('downloaded $M')" < /dev/null
  AGP_NTEST=$NT python -u g_eval.py --model $M --dirs ../dirs/$DF --layer $L --seeds 1600-1619 --batch 20 --probe --frames --rand 50 --out ../out_jp/$T < /dev/null 2>&1 | grep -v -i warn
  rm -rf /root/hf/hub/models--$(echo $M | sed 's#/#--#')
done
echo CLOUD19_DONE
