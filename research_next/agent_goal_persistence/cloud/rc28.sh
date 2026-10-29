#!/bin/bash
# PLAN_BIGGER Phase 0 (exploratory pilot; rules in PILOT_V0.md): readout audit and lever search on the four models.
# Speed: the four models download in parallel and run as concurrent processes on the one GPU (batch 48).
# Stage 1 screens every configuration (first-token readout); v0_rank.py picks 8 recipes + 2 random controls across
# models; stage 2 runs the audit conditions and those recipes with generation. Runs from /workspace/agpv0; xet off (L12).
export HF_HOME=/root/hf HF_HUB_DISABLE_XET=1
mkdir -p /root/hf
cd /workspace/agpv0/code
pip install -q "transformers==5.16.1" accelerate
MODELS="Qwen/Qwen3-1.7B HuggingFaceTB/SmolLM3-3B Qwen/Qwen3-8B allenai/OLMo-2-1124-7B-Instruct"
for M in $MODELS; do
  python -c "from huggingface_hub import snapshot_download; snapshot_download('$M'); print('downloaded $M')" < /dev/null &
done
wait
for M in $MODELS; do
  python -u lever_pilot.py --mode screen --model $M --batch 48 --out ../out_v0/$(basename $M) < /dev/null > ../log_screen_$(basename $M).txt 2>&1 &
done
wait
grep -h -E "SCREEN_DONE|Traceback|Error" ../log_screen_*.txt
python -u v0_rank.py --root ../out_v0 --out ../out_v0/recipes.json < /dev/null 2>&1
for M in $MODELS; do
  python -u lever_pilot.py --mode gen --model $M --batch 48 --recipes ../out_v0/recipes.json --out ../out_v0/$(basename $M) < /dev/null > ../log_gen_$(basename $M).txt 2>&1 &
done
wait
grep -h -E "GEN_DONE|Traceback|Error" ../log_gen_*.txt
cp ../log_*.txt ../out_v0/ 2>/dev/null
echo CLOUD28_DONE
