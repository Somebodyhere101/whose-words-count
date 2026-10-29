#!/bin/bash
# Control Illusion fix pilot (before PREREG_N): system-vs-user conflicts, tasks 0-14 of both orders (180 prompts),
# conditions plain / emph / steer at alpha 2, 4, 8, on Qwen3-8B and OLMo-2-7B; chooses alpha per model. Greedy decoding.
export HF_HOME=/root/hf HF_HUB_DISABLE_XET=1
mkdir -p /root/hf
cd /workspace/agpn/code
pip install -q "transformers==5.16.1" accelerate langdetect nltk
python -c "import nltk; nltk.download('punkt_tab', quiet=True); print('punkt_tab ok')"
while read M DF L; do
  [ -z "$M" ] && continue
  T=$(basename $M)
  python -c "from huggingface_hub import snapshot_download; snapshot_download('$M'); print('downloaded $M')" < /dev/null
  python -u ci_eval.py --model $M --dirs ../dirs/$DF --layer $L --data ../data/ci/conflicting_instructions.jsonl,../data/ci/conflicting_instructions_reversed.jsonl --tasks 0-14 --conds plain,emph,steer2,steer4,steer8 --batch 32 --out ../out_np/$T < /dev/null 2>&1 | grep -v -i -E "warn|generation flag"
  python ci_score.py ../out_np/$T/plain.json ../out_np/$T/emph.json ../out_np/$T/steer2.json ../out_np/$T/steer4.json ../out_np/$T/steer8.json < /dev/null 2>&1 | grep -v -i warn
  rm -rf /root/hf/hub/models--$(echo $M | sed 's#/#--#') /root/hf/xet < /dev/null
done <<'LIST'
Qwen/Qwen3-8B dirs_q8.pt 17
allenai/OLMo-2-1124-7B-Instruct dirs_olmo.pt 10
LIST
echo CLOUD24P_DONE
