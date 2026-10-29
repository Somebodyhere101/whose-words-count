#!/bin/bash
# PREREG_Y part B (GPU with at least 94 GB): Qwen3-32B on InjecAgent (300 cases), 8 conditions. Part A (rc33.sh) runs
# everything else. PREREG_X's sealed bench.py, recipe, sample and seed are reused unchanged; InjecAgent is cloned at
# PREREG_X's commit and read as data only. Same out-of-memory rule as rc33.sh. xet is off (L12).
# Runs from /workspace/agpyb/code.
export HF_HOME=/root/hf HF_HUB_DISABLE_XET=1
cd "$(dirname "$0")"
mkdir -p /root/hf /root/bench ../out_y
pip install -q "transformers==5.16.1" accelerate
( cd /root/bench && git clone -q https://github.com/uiuc-kang-lab/InjecAgent.git injecagent && git -C injecagent checkout -q f19c9f2 )
CI=$(git -C /root/bench/injecagent rev-parse HEAD); echo "InjecAgent commit $CI"
case "$CI" in f19c9f2*) ;; *) echo COMMIT_MISMATCH; echo CLOUD34_DONE; exit 1 ;; esac
dl() { python -c "from huggingface_hub import snapshot_download; snapshot_download('$1')" < /dev/null > /dev/null 2>&1; }
( for t in 1 2 3; do dl Qwen/Qwen3-32B && { touch /root/dl_Qwen3-32B.ok; break; }; sleep 30; done
  echo "$(date -u +%H:%M) Qwen3-32B ok=$([ -f /root/dl_Qwen3-32B.ok ] && echo 1 || echo 0)" ) > ../log_dl.txt 2>&1 &
# Smoke test on a non-study model: an environment check only, no study data.
dl Qwen/Qwen3-0.6B
python -u bench.py --bench injecagent --model Qwen/Qwen3-0.6B --recipe ../recipe.json --data /root/bench/injecagent/data --prompts ../data/injecagent_prompts.json --limit 4 --max_new 32 --batch 4 --conds none,DEF --out /root/smoke < /dev/null > ../log_smoke.txt 2>&1
if ! grep -q BENCH_DONE ../log_smoke.txt; then echo SMOKE_FAILED; tail -30 ../log_smoke.txt; cp ../log_smoke.txt ../out_y/; echo CLOUD34_DONE; exit 1; fi
echo SMOKE_OK
waitdl() { for w in $(seq 1 240); do [ -f /root/dl_$1.ok ] && return 0; sleep 30; done; echo "DL_TIMEOUT $1"; return 1; }
bench() {  # benchmark, model, batch, extra arguments
  B=$1; M=$2; N=$3; shift 3; T=$(basename $M); L=../log_y_${B}_$T.txt
  if [ $B = sep ]; then D=/root/bench/sep/datasets/SEP_dataset.json; else D=/root/bench/injecagent/data; fi
  for try in 1 2; do
    python -u bench.py --bench $B --model $M --recipe ../recipe.json --data $D --n 300 --batch $N "$@" --out ../out_y/$T < /dev/null > $L 2>&1
    grep -q BENCH_DONE $L && { echo "$(date -u +%H:%M) $B $T done (batch $N)"; return 0; }
    if [ $try = 1 ] && grep -q "out of memory" $L; then mv $L ${L%.txt}_oom_attempt1.txt; N=$((N / 2)); echo "OOM_RETRY $B $T batch $N"; else echo "FAILED $B $T"; return 1; fi
  done
}
waitdl Qwen3-32B && bench injecagent Qwen/Qwen3-32B 8 --prompts ../data/injecagent_prompts.json --max_new 160
grep -h -E "Traceback|out of memory|DL_TIMEOUT" ../log_y_*.txt ../log_dl.txt | sort | uniq -c
cp ../log_*.txt ../out_y/ 2>/dev/null
echo CLOUD34_DONE
