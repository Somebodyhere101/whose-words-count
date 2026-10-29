#!/bin/bash
# PREREG_C: depth sweep (phase A, seeds 400-419) and confirmation at the selected layer (phase B, seeds 500-539)
# in OLMo-2-7B (fixed text, N_TEST 22 to fit its 4,096-token window), Granite-3.3-8B and SmolLM3-3B (weak text).
export HF_HOME=/root/hf
mkdir -p /root/hf
cd /workspace/agp/code
pip install -q "transformers==5.16.1" accelerate
for spec in "allenai/OLMo-2-1124-7B-Instruct gF,oF 22 2,4,6,8,10,12,15 olmo" \
            "ibm-granite/granite-3.3-8b-instruct gW,oW 30 3,5,8,10,13,15,18 granite" \
            "HuggingFaceTB/SmolLM3-3B gW,oW 30 2,4,7,9,11,14,17 smol3"; do
  set -- $spec; M=$1; C=$2; NT=$3; LS=$4; K=$5; T=$(basename $M)
  python -c "from huggingface_hub import snapshot_download; snapshot_download('$M'); print('downloaded $M')"
  AGP_NTEST=$NT python -u steer_run.py --model $M --cells $C --dirs ../dirs/dirs_$K.pt --layers $LS --alphas 2 \
    --seeds 400-419 --batch 16 --out ../out_cA_$T 2>&1 | grep -v -i warn
  SEL=$(python select_layer.py --dir ../out_cA_$T --cells $C)
  echo "SELECTED $T $SEL"
  if [ "$SEL" != "NONE" ]; then
    AGP_NTEST=$NT python -u steer_run.py --model $M --cells $C --dirs ../dirs/dirs_$K.pt --layers $SEL --alphas 2 \
      --seeds 500-539 --batch 16 --out ../out_cB_$T 2>&1 | grep -v -i warn
  fi
  rm -rf /root/hf/hub/models--$(echo $M | sed 's#/#--#')
done
echo CLOUD7_DONE
