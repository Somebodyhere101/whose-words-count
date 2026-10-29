#!/bin/bash
# PREREG_Y part A (80 GB GPU): Qwen3-14B on SEP (300 items) and InjecAgent (300 cases), and SEP for Qwen3-32B,
# Falcon3-10B, Yi-1.5-9B, OLMo-2-13B and OLMo-2-32B, 8 conditions each. Part B (rc34.sh, >= 94 GB GPU) runs Qwen3-32B
# on InjecAgent. PREREG_X's sealed bench.py, recipe, samples and seeds are reused unchanged. The benchmark repositories
# are cloned at the PREREG_X commits and read as data only.
# A background loop downloads the models in run order; each model's cache is deleted after its run.
# Operational rule fixed before data: a run that ends in CUDA out-of-memory without BENCH_DONE is repeated once at half
# the batch size, and the first log is kept as *_oom_attempt1.txt. xet is off (L12). Runs from /workspace/agpy/code.
export HF_HOME=/root/hf HF_HUB_DISABLE_XET=1
cd "$(dirname "$0")"
mkdir -p /root/hf /root/bench ../out_y
pip install -q "transformers==5.16.1" accelerate
( cd /root/bench && git clone -q https://github.com/egozverev/Should-It-Be-Executed-Or-Processed.git sep && git -C sep checkout -q 7606c06 \
  && git clone -q https://github.com/uiuc-kang-lab/InjecAgent.git injecagent && git -C injecagent checkout -q f19c9f2 )
CS=$(git -C /root/bench/sep rev-parse HEAD); CI=$(git -C /root/bench/injecagent rev-parse HEAD)
echo "SEP commit $CS; InjecAgent commit $CI"
case "$CS $CI" in 7606c06*" "f19c9f2*) ;; *) echo COMMIT_MISMATCH; echo CLOUD33_DONE; exit 1 ;; esac
dl() { python -c "from huggingface_hub import snapshot_download; snapshot_download('$1')" < /dev/null > /dev/null 2>&1; }
ORDER="Qwen/Qwen3-14B tiiuae/Falcon3-10B-Instruct 01-ai/Yi-1.5-9B-Chat allenai/OLMo-2-1124-13B-Instruct Qwen/Qwen3-32B allenai/OLMo-2-0325-32B-Instruct"
( for M in $ORDER; do
    for t in 1 2 3; do dl $M && { touch /root/dl_$(basename $M).ok; break; }; sleep 30; done
    echo "$(date -u +%H:%M) $M ok=$([ -f /root/dl_$(basename $M).ok ] && echo 1 || echo 0) free=$(df -h /root | tail -1 | awk '{print $4}')"
  done ) > ../log_dl.txt 2>&1 &
# Smoke test on a non-study model: an environment check only, no study data.
dl Qwen/Qwen3-0.6B
python -u bench.py --bench sep --model Qwen/Qwen3-0.6B --recipe ../recipe.json --data /root/bench/sep/datasets/SEP_dataset.json --n 4 --batch 8 --conds none,DEF --out /root/smoke < /dev/null > ../log_smoke.txt 2>&1
python -u bench.py --bench injecagent --model Qwen/Qwen3-0.6B --recipe ../recipe.json --data /root/bench/injecagent/data --prompts ../data/injecagent_prompts.json --limit 4 --max_new 32 --batch 4 --conds none,DEF --out /root/smoke < /dev/null >> ../log_smoke.txt 2>&1
if [ "$(grep -c BENCH_DONE ../log_smoke.txt)" != "2" ]; then echo SMOKE_FAILED; tail -30 ../log_smoke.txt; cp ../log_smoke.txt ../out_y/; echo CLOUD33_DONE; exit 1; fi
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
drop() { rm -rf /root/hf/hub/models--$(echo $1 | sed 's#/#--#g'); }
both() { waitdl $(basename $1) || return; bench sep $1 32; bench injecagent $1 8 --prompts ../data/injecagent_prompts.json --max_new 160; drop $1; }
seponly() { waitdl $(basename $1) || return; bench sep $1 32; drop $1; }
both Qwen/Qwen3-14B
seponly tiiuae/Falcon3-10B-Instruct
seponly 01-ai/Yi-1.5-9B-Chat
seponly allenai/OLMo-2-1124-13B-Instruct
seponly Qwen/Qwen3-32B
seponly allenai/OLMo-2-0325-32B-Instruct
grep -h -E "Traceback|out of memory|DL_TIMEOUT" ../log_y_*.txt ../log_dl.txt | sort | uniq -c
cp ../log_*.txt ../out_y/ 2>/dev/null
echo CLOUD33_DONE
