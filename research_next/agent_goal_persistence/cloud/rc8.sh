#!/bin/bash
# Lineage pilot at 7B (PLAN_LINEAGE_FABLE.md, step 7): OLMo-2-1124-7B base in the plain transcript format, and
# OLMo-2-1124-7B-Instruct in plain and native formats. Cells 1/gF/oF, seeds 300-319, N_TEST 22 (4,096-token window).
export HF_HOME=/root/hf
mkdir -p /root/hf
cd /workspace/agp/code
pip install -q "transformers==5.16.1" accelerate
for spec in "allenai/OLMo-2-1124-7B plain" "allenai/OLMo-2-1124-7B-Instruct plain" "allenai/OLMo-2-1124-7B-Instruct native"; do
  set -- $spec; M=$1; F=$2; T=$(basename $M)
  python -c "from huggingface_hub import snapshot_download; snapshot_download('$M'); print('downloaded $M')"
  if [ $F = plain ]; then export AGP_FMT=plain; else unset AGP_FMT; fi
  AGP_NTEST=22 python -u agp_fast.py --model $M --conds 1,gF,oF --seeds 300-319 --batch 20 --out ../out_lp/${F}_$T 2>&1 | grep -v -i warn
done
echo CLOUD8_DONE
