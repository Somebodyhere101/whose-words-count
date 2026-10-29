#!/bin/bash
# PREREG_X, one pod's share (bash rc31.sh 1|2): per model, SEP (300 items), then InjecAgent (300 cases), 8 conditions.
# The benchmark data are cloned from the public repositories at run time and read as data only; commits are logged.
# xet is off (L12). Runs from /workspace/agpx<n>/code.
export HF_HOME=/root/hf HF_HUB_DISABLE_XET=1
mkdir -p /root/hf /root/bench
cd "$(dirname "$0")"
pip install -q "transformers==5.16.1" accelerate
( cd /root/bench && git clone --depth 1 -q https://github.com/egozverev/Should-It-Be-Executed-Or-Processed.git sep && git clone --depth 1 -q https://github.com/uiuc-kang-lab/InjecAgent.git injecagent )
echo "SEP commit $(git -C /root/bench/sep rev-parse HEAD); InjecAgent commit $(git -C /root/bench/injecagent rev-parse HEAD)"
run() {  # model, SEP batch, InjecAgent batch
  M=$1; T=$(basename $M)
  python -c "from huggingface_hub import snapshot_download; snapshot_download('$M')" < /dev/null > /dev/null 2>&1
  python -u bench.py --bench sep --model $M --recipe ../recipe.json --data /root/bench/sep/datasets/SEP_dataset.json --n 300 --batch $2 --out ../out_x/$T < /dev/null > ../log_x_sep_$T.txt 2>&1
  python -u bench.py --bench injecagent --model $M --recipe ../recipe.json --data /root/bench/injecagent/data --prompts ../data/injecagent_prompts.json --n 300 --max_new 160 --batch $3 --out ../out_x/$T < /dev/null > ../log_x_ia_$T.txt 2>&1
}
case $1 in
  1) run Qwen/Qwen3-1.7B 48 16 & run HuggingFaceTB/SmolLM3-3B 48 16 & run Qwen/Qwen3-8B 32 16 & wait ;;
  2) run allenai/OLMo-2-1124-7B-Instruct 32 16 & run ibm-granite/granite-3.3-8b-instruct 32 16 & wait; run microsoft/phi-4 32 8 ;;
esac
grep -h -E "BENCH_DONE|Traceback|Error" ../log_x_*.txt
cp ../log_x_*.txt ../out_x/ 2>/dev/null
echo CLOUD31_DONE
