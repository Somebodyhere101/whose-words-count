#!/bin/bash
# CHANNEL (rules in CHANNEL.md): does the user > system reminder order follow the channel the pressure arrives in?
# 1) manipulation check on held-out seeds 9390-9399 (cell 1 only, Qwen3-8B and OLMo-2-7B); STOP unless the moved
#    pressure bites; 2) g_eval --chan on 10 models, seeds 9300-9359 (Qwen3-32B 9300-9339). The next model downloads
#    while the current one runs; xet off and caches cleared after each model (L12). Outputs: /workspace/agpch/out_chan.
export HF_HOME=/root/hf HF_HUB_DISABLE_XET=1
mkdir -p /root/hf
cd /workspace/agpch/code
pip install -q "transformers==5.16.1" accelerate
dl() { python -c "from huggingface_hub import snapshot_download; snapshot_download('$1', ignore_patterns=['original/*', 'metal/*']); print('downloaded $1')" < /dev/null; }
mkdir -p ../out_chan ../out_chan_pilot
dl Qwen/Qwen3-8B; dl allenai/OLMo-2-1124-7B-Instruct
AGP_NTEST=30 python -u g_eval.py --model Qwen/Qwen3-8B --chanpilot --seeds 9390-9399 --batch 10 --out ../out_chan_pilot/Qwen3-8B < /dev/null 2>&1 | grep -v -i warn
AGP_NTEST=20 python -u g_eval.py --model allenai/OLMo-2-1124-7B-Instruct --chanpilot --seeds 9390-9399 --batch 10 --out ../out_chan_pilot/OLMo-2-1124-7B-Instruct < /dev/null 2>&1 | grep -v -i warn
python chan_pilot.py --root ../out_chan_pilot | tee ../out_chan/pilot.log
if ! grep -q "CHAN_PILOT PROCEED" ../out_chan/pilot.log; then echo PILOT_STOP; echo CLOUD_CHAN_DONE; exit; fi
# model:N_TEST:seeds:batch:extra (extra uses + for spaces)
set -- Qwen/Qwen3-8B:30:9300-9359:20: allenai/OLMo-2-1124-7B-Instruct:20:9300-9359:20: \
  Qwen/Qwen2.5-7B-Instruct:30:9300-9359:20: tiiuae/Falcon3-7B-Instruct:30:9300-9359:20: \
  allenai/OLMo-2-1124-13B-Instruct:20:9300-9359:10: Qwen/Qwen2.5-14B-Instruct:30:9300-9359:20: \
  tiiuae/Falcon3-10B-Instruct:30:9300-9359:20: ibm-granite/granite-3.3-8b-instruct:30:9300-9359:20: \
  openai/gpt-oss-20b:30:9300-9359:20:--dev+--srole+developer \
  Qwen/Qwen3-32B:30:9300-9339:6:
while [ $# -gt 0 ]; do
  IFS=: read M NT SD B X <<< "$1"; shift
  NEXT=
  if [ $# -gt 0 ]; then N1=${1%%:*}; [ -d /root/hf/hub/models--$(echo $N1 | sed 's#/#--#') ] || { dl $N1 > /tmp/dl_next.log 2>&1 & NEXT=$!; }; fi
  [ -d /root/hf/hub/models--$(echo $M | sed 's#/#--#') ] || dl $M
  T=$(basename $M)
  if [ "$T" = gpt-oss-20b ]; then
    python -u flip_gate.py --model $M < /dev/null 2>&1 | grep -v -i warn | tee ../out_chan/gate_gptoss.log
    grep -q "FLIP_GATE PASS" ../out_chan/gate_gptoss.log || { echo "gpt-oss gate failed, skipped"; rm -rf /root/hf/hub/models--$(echo $M | sed 's#/#--#'); if [ -n "$NEXT" ]; then wait $NEXT; fi; continue; }
  fi
  AGP_NTEST=$NT python -u g_eval.py --model $M --chan ${X//+/ } --seeds $SD --batch $B --out ../out_chan/$T < /dev/null 2>&1 | grep -v -i warn
  rm -rf /root/hf/hub/models--$(echo $M | sed 's#/#--#') /root/hf/xet
  df -h /root | tail -1
  if [ -n "$NEXT" ]; then wait $NEXT; cat /tmp/dl_next.log | tail -1; fi
done
echo CLOUD_CHAN_DONE
