#!/bin/bash
# FLIP (rules in FLIP.md): gpt-oss-20b. Format gate first (nothing else runs unless FLIP_GATE PASS), then vR in-pod
# (src_probe, n 240), then g_eval --probe --dev at layer 11 on seeds 9100-9159. Outputs to /workspace/agpfl/out_flip.
export HF_HOME=/root/hf HF_HUB_DISABLE_XET=1
mkdir -p /root/hf
cd /workspace/agpfl/code
pip install -q "transformers==5.16.1" accelerate
M=openai/gpt-oss-20b
python -c "from huggingface_hub import snapshot_download; snapshot_download('$M', ignore_patterns=['original/*', 'metal/*']); print('downloaded $M')" < /dev/null
mkdir -p ../out_flip
python -u flip_gate.py --model $M < /dev/null 2>&1 | grep -v -i warn | tee ../out_flip/gate.log
if ! grep -q "FLIP_GATE PASS" ../out_flip/gate.log; then echo GATE_FAILED; echo CLOUD_FLIP_DONE; exit; fi
python -u src_probe.py --model $M --n 240 --out ../out_flip/probe_gpt-oss-20b < /dev/null 2>&1 | grep -v -i warn | tail -4
python -u g_eval.py --model $M --dirs ../out_flip/probe_gpt-oss-20b/directions.pt --layer 11 --seeds 9100-9159 \
  --batch 20 --probe --dev --rand 50 --out ../out_flip/gpt-oss-20b < /dev/null 2>&1 | grep -v -i warn
echo CLOUD_FLIP_DONE
