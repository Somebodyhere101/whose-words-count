#!/bin/bash
# PREREG_D: OLMo-2 lineage in the native template. 7B and 13B at SFT, DPO and Instruct; cells 1/gF/oF/uF;
# fresh seeds 600-679; N_TEST 22 (4,096-token window). 7B stages also get the 240-sentence probe (exploratory).
export HF_HOME=/root/hf
mkdir -p /root/hf
cd /workspace/agp/code
pip install -q "transformers==5.16.1" accelerate
for M in allenai/OLMo-2-1124-7B-SFT allenai/OLMo-2-1124-7B-DPO allenai/OLMo-2-1124-7B-Instruct \
         allenai/OLMo-2-1124-13B-SFT allenai/OLMo-2-1124-13B-DPO allenai/OLMo-2-1124-13B-Instruct; do
  T=$(basename $M); B=20; case $M in *13B*) B=10;; esac
  python -c "from huggingface_hub import snapshot_download; snapshot_download('$M'); print('downloaded $M')"
  AGP_NTEST=22 python -u agp_fast.py --model $M --conds 1,gF,oF,uF --seeds 600-679 --batch $B --out ../out_ld/fast_$T 2>&1 | grep -v -i warn
  case $M in *-7B-*) python -u src_probe.py --model $M --n 240 --out ../out_ld/probe_$T 2>&1 | grep -v -i warn;; esac
  rm -rf /root/hf/hub/models--$(echo $M | sed 's#/#--#')
done
echo CLOUD9_DONE
