#!/bin/bash
# PREREG_H: is authority one axis? 3-way world, fresh seeds 1400-1459, cells 1/gF/oF/uF with the projection probe on
# unit vR, in Qwen3-8B (layer 17), Qwen3-14B (layer 18) and OLMo-2-7B-Instruct (layer 10, N_TEST 22).
export HF_HOME=/root/hf
mkdir -p /root/hf
cd /workspace/agp/code
pip install -q "transformers==5.16.1" accelerate
for spec in "Qwen/Qwen3-8B dirs_q8.pt 17 30" "Qwen/Qwen3-14B dirs_q14.pt 18 30" "allenai/OLMo-2-1124-7B-Instruct dirs_olmo.pt 10 22"; do
  set -- $spec; M=$1; DF=$2; L=$3; NT=$4; T=$(basename $M)
  python -c "from huggingface_hub import snapshot_download; snapshot_download('$M'); print('downloaded $M')"
  AGP_NTEST=$NT python -u g_eval.py --model $M --dirs ../dirs/$DF --layer $L --seeds 1400-1459 --batch 20 --probe --out ../out_h/$T 2>&1 | grep -v -i warn
  rm -rf /root/hf/hub/models--$(echo $M | sed 's#/#--#')
done
echo CLOUD17_DONE
