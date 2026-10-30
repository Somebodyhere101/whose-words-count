#!/bin/bash
# PREREG_R: does the role axis follow a trained priority? Per model: base vR from src_probe.py (n 240); base and 6
# hierarchy adapters (sys/usr x data seeds 6000/7000/8000; n 48, no pressure lines, order-balanced) evaluated with
# g_eval.py --probe on the BASE vR plus 50 random directions, fresh seeds 6000-6029; each adapter's vR re-extracted
# (src_probe_lora.py) and its cosine with the base vR saved. Outputs to /workspace/agpr/out_r. Labels use "r".
export HF_HOME=/root/hf HF_HUB_DISABLE_XET=1
mkdir -p /root/hf /root/lora_r /root/probe_r
cd /workspace/agpr/code
pip install -q "transformers==5.16.1" accelerate peft==0.21.2
while read M NT L; do
  [ -z "$M" ] && continue
  T=$(basename $M); O=../out_r/$T
  python -c "from huggingface_hub import snapshot_download; snapshot_download('$M'); print('downloaded $M')" < /dev/null
  export AGP_NTEST=$NT
  python -u src_probe.py --model $M --n 240 --out /root/probe_r/$T/base < /dev/null 2>&1 | grep -v -i warn | tail -2
  B=/root/probe_r/$T/base/directions.pt
  mkdir -p $O && cp /root/probe_r/$T/base/probe_results.json $O/probe_base.json
  python -u g_eval.py --model $M --dirs $B --layer $L --probe --rand 50 --seeds 6000-6029 --batch 20 --out $O/base < /dev/null 2>&1 | grep -v -i warn
  for arm in sys usr; do
    for s0 in 6000 7000 8000; do
      A=/root/lora_r/$T/$arm$s0
      python -u lora_train_h.py --model $M --data hier --arm $arm --n 48 --nopress --posbal --seed0 $s0 --out $A < /dev/null 2>&1 | grep -v -i warn
      mkdir -p $O/$arm$s0 && cp $A/train_log.json $O/$arm$s0/
      AGP_LORA=$A python -u g_eval.py --model $M --dirs $B --layer $L --probe --rand 50 --seeds 6000-6029 --batch 20 --out $O/$arm$s0 < /dev/null 2>&1 | grep -v -i warn
      AGP_LORA=$A python -u src_probe_lora.py --model $M --n 240 --out /root/probe_r/$T/$arm$s0 < /dev/null 2>&1 | grep -v -i warn | tail -1
      python -c "
import json, torch
b = torch.load('$B')[$L]['vR'].float(); a = torch.load('/root/probe_r/$T/$arm$s0/directions.pt')[$L]['vR'].float()
json.dump({'layer': $L, 'cos': float(torch.nn.functional.cosine_similarity(a, b, 0)), 'norm_ratio': float(a.norm() / b.norm())}, open('$O/$arm$s0/cos.json', 'w'))
" < /dev/null
    done
  done
  echo "done $T"; df -h /root | tail -1
  rm -rf /root/hf/hub/models--$(echo $M | sed 's#/#--#') /root/hf/xet < /dev/null
done <<'LIST'
MODELS_GO_HERE
LIST
echo CLOUD_R_DONE
