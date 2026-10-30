#!/bin/bash
# TAGSTYLE pilot (exploratory, rules in TAGSTYLE.md): tagstyle.py on 6 models; the next model downloads while the
# current one runs; each model is removed after use; xet off (L12). Outputs to /workspace/agpts/out_ts.
export HF_HOME=/root/hf HF_HUB_DISABLE_XET=1
mkdir -p /root/hf
cd /workspace/agpts/code
pip install -q "transformers==5.16.1" accelerate
dl() { python -c "from huggingface_hub import snapshot_download; snapshot_download('$1'); print('downloaded $1')" < /dev/null; }
set -- Qwen/Qwen3-1.7B:48 HuggingFaceTB/SmolLM3-3B:48 Qwen/Qwen3-8B:48 allenai/OLMo-2-1124-7B-Instruct:48 ibm-granite/granite-3.3-8b-instruct:48 microsoft/phi-4:24
dl ${1%%:*}
while [ $# -gt 0 ]; do
  IFS=: read M B <<< "$1"; shift
  NEXT=
  if [ $# -gt 0 ]; then dl ${1%%:*} > /tmp/dl_next.log 2>&1 & NEXT=$!; fi
  T=$(basename $M)
  python -u tagstyle.py --model $M --batch $B --out ../out_ts/$T < /dev/null 2>&1 | grep -v -i warn
  rm -rf /root/hf/hub/models--$(echo $M | sed 's#/#--#') /root/hf/xet
  df -h /root | tail -1
  if [ -n "$NEXT" ]; then wait $NEXT; cat /tmp/dl_next.log; fi
done
echo CLOUD_TS_DONE
