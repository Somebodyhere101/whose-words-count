#!/bin/bash
# PREREG_W pre-seal tests on a pod: tokenizer formats of the 10 models; GPU equivalence on Qwen3-0.6B (not data).
export HF_HOME=/root/hf HF_HUB_DISABLE_XET=1
cd "$(dirname "$0")"
python -u w_pretest.py 2>&1 | grep "^FMT"
rm -rf /root/wt; M=Qwen/Qwen3-0.6B
python -u src_patch.py --model $M --layer 14 --n 2 --seed 2600 --out /root/wt/A/Qwen3-0.6B 2>&1 | grep -E "done|DONE|Error"
python -u src_patch_w.py --model $M --layer 14 --n 2 --seed 2600 --stride 1 --out /root/wt/B/Qwen3-0.6B 2>&1 | grep -E "DONE|Error"
python -u src_patch_w.py --model $M --layer 14 --n 2 --seed 2600 --stride 2 --out /root/wt/C/Qwen3-0.6B 2>&1 | grep -E "DONE|Error"
python -u s_beh.py --model $M --n 2 --out /root/wt/C/Qwen3-0.6B 2>&1 | grep -E "DONE|Error"
python - <<'PY'
import json
A=json.load(open('/root/wt/A/Qwen3-0.6B/patch.json')); B=json.load(open('/root/wt/B/Qwen3-0.6B/patch.json')); C=json.load(open('/root/wt/C/Qwen3-0.6B/patch.json'))
print('EQ stride1 == src_patch:', A['pairs']==B['pairs'])
bad=0; alls=[]
for p in B['pairs']:
    for k in ('beh','attr'):
        for s in ('M','C','D'):
            for l in C['swept']:
                if C['pairs'][p][k]['patched'][s][l-1]!=B['pairs'][p][k]['patched'][s][l-1]: bad+=1
        for l,v in C['pairs'][p][k]['all'].items():
            d=C['pairs'][p][k]['donor']; r=C['pairs'][p][k]['recip']
            alls.append(max(abs(x-y) for x,y in zip(v,d)))
print('EQ stride2 swept layers == stride1:', bad==0, 'swept', len(C['swept']), 'of', C['n_layers'], '| ALL patch vs donor max abs diff', round(max(alls),5))
PY
python -u w_analyze.py --root /root/wt/C 2>&1 | head -5
echo PRETEST_DONE
