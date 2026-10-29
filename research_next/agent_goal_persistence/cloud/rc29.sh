#!/bin/bash
# PREREG_W, one pod's share: for each model, the behaviour-only fragmentation test (s_beh.py), then the source map
# (src_patch_w.py; the 32B models at stride 2). The next model downloads while the current one runs, and each model
# is removed after use. xet is off (L12). Usage: bash rc29.sh A|B|C, from /workspace/agpw<a|b|c>/code.
export HF_HOME=/root/hf HF_HUB_DISABLE_XET=1
mkdir -p /root/hf
cd "$(dirname "$0")"
pip install -q "transformers==5.16.1" accelerate
case $1 in
  A) LIST="Qwen/Qwen3-32B:32:2:24 01-ai/Yi-1.5-9B-Chat:24:1:48 Qwen/Qwen3-4B:18:1:48 Qwen/Qwen3-0.6B:14:1:48" ;;
  B) LIST="allenai/OLMo-2-0325-32B-Instruct:32:2:24 allenai/OLMo-2-1124-13B-Instruct:20:1:48" ;;
  C) LIST="Qwen/Qwen3-14B:20:1:48 microsoft/phi-4:20:1:48 tiiuae/Falcon3-10B-Instruct:20:1:48 ibm-granite/granite-3.3-8b-instruct:20:1:48" ;;
esac
dl() { python -c "from huggingface_hub import snapshot_download; snapshot_download('$1'); print('downloaded $1')" < /dev/null; }
set -- $LIST
dl ${1%%:*}
while [ $# -gt 0 ]; do
  IFS=: read M L S B <<< "$1"; shift
  NEXT=
  if [ $# -gt 0 ]; then dl ${1%%:*} > /tmp/dl_next.log 2>&1 & NEXT=$!; fi
  T=$(basename $M)
  python -u s_beh.py --model $M --batch $B --out ../out_w/$T < /dev/null 2>&1 | grep -v -i warn
  python -u src_patch_w.py --model $M --layer $L --stride $S --batch $B --out ../out_w/$T < /dev/null 2>&1 | grep -v -i warn
  rm -rf /root/hf/hub/models--$(echo $M | sed 's#/#--#') /root/hf/xet
  df -h /root | tail -1
  if [ -n "$NEXT" ]; then wait $NEXT; cat /tmp/dl_next.log; fi
done
echo CLOUD29_DONE
