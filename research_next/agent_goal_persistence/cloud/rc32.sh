#!/bin/bash
# PILOT_V1 (exploratory; rules in PILOT_V1.md): the format-matched lever on 60 InjecAgent dev cases, for Qwen3-8B,
# OLMo-2-7B, Granite-3.3-8B and phi-4 in sequence. The next model downloads while the current one runs.
# xet is off (L12). Runs from /workspace/agpv1/code.
export HF_HOME=/root/hf HF_HUB_DISABLE_XET=1
mkdir -p /root/hf /root/bench
cd "$(dirname "$0")"
pip install -q "transformers==5.16.1" accelerate
( cd /root/bench && git clone --depth 1 -q https://github.com/uiuc-kang-lab/InjecAgent.git injecagent )
echo "InjecAgent commit $(git -C /root/bench/injecagent rev-parse HEAD)"
dl() { python -c "from huggingface_hub import snapshot_download; snapshot_download('$1')" < /dev/null > /dev/null 2>&1; }
set -- Qwen/Qwen3-8B:12 allenai/OLMo-2-1124-7B-Instruct:8 ibm-granite/granite-3.3-8b-instruct:12 microsoft/phi-4:8
dl ${1%%:*}
while [ $# -gt 0 ]; do
  IFS=: read M B <<< "$1"; shift
  NEXT=
  if [ $# -gt 0 ]; then dl ${1%%:*} & NEXT=$!; fi
  python -u ia_pilot.py --model $M --data /root/bench/injecagent/data --prompts ../data/injecagent_prompts.json --batch $B --out ../out_v1/$(basename $M) < /dev/null 2>&1 | grep -v -i warn
  rm -rf /root/hf/hub/models--$(echo $M | sed 's#/#--#')
  if [ -n "$NEXT" ]; then wait $NEXT; fi
done
python -u ia_pilot_analyze.py --root ../out_v1 > ../out_v1/v1_analysis.json 2>&1
head -c 300 ../out_v1/v1_analysis.json; echo
echo CLOUD32_DONE
