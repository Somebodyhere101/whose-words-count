#!/bin/bash
# Pilot (exploratory, seeds 1200-1219): goal authority by steering on the 3-way world (AGP_WORLD=3way) in Qwen3-8B
# (stage-2 vR at layer 17) and Qwen3-14B (layer 18). g_eval.py runs base 1/gF/oF, own note pushed toward given
# (-2 vR) and its random control, system note boosted (-2 vR) and its random control.
export HF_HOME=/root/hf
mkdir -p /root/hf
cd /workspace/agp/code
pip install -q "transformers==5.16.1" accelerate
for spec in "Qwen/Qwen3-8B dirs_q8.pt 17" "Qwen/Qwen3-14B dirs_q14.pt 18"; do
  set -- $spec; M=$1; DF=$2; L=$3; T=$(basename $M)
  python -c "from huggingface_hub import snapshot_download; snapshot_download('$M'); print('downloaded $M')"
  python -u g_eval.py --model $M --dirs ../dirs/$DF --layer $L --seeds 1200-1219 --batch 20 --out ../out_g/$T 2>&1 | grep -v -i warn
  rm -rf /root/hf/hub/models--$(echo $M | sed 's#/#--#')
done
echo CLOUD15_DONE
