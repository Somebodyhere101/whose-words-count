# Chain 2 (understanding the stage-2 failure + replication): probes and fast runs on more models, via gpu_lock.
cd "/c/Users/caabm/AppData/Roaming/Claude/scratch-workspaces/2898f83d-79d0-4cb9-a017-7d323d549974/0c4963d8-51ed-4ceb-9445-28b8639f6fa1/scratch-2026-10-13-464f6a/research_next/agent_goal_persistence/code"
L="/c/Users/caabm/Documents/Codex/2026-09-06/co/work/qwen-cuda-env/Scripts/python.exe /c/Users/caabm/AppData/Roaming/Claude/scratch-workspaces/2898f83d-79d0-4cb9-a017-7d323d549974/0c4963d8-51ed-4ceb-9445-28b8639f6fa1/scratch-2026-10-13-464f6a/tools/gpu_lock.py --max-min 90"
run() { # label outdir expected cmd...
  lab=$1; out=$2; want=$3; shift 3
  for i in 1 2 3 4; do n=$(ls $out 2>/dev/null | grep -c json); [ "$n" -ge "$want" ] && break; $L --label $lab -- "$@"; done
  echo "STEP $lab n=$(ls $out 2>/dev/null | grep -c json)"
}
run agp-fast-weak ../fast_val 280 /c/Users/caabm/Documents/Codex/2026-09-06/co/work/qwen-cuda-env/Scripts/python.exe -u agp_fast.py --conds gW,oW --seeds 300-339 --batch 4 --out ../fast_val
for m in HuggingFaceTB/SmolLM2-1.7B-Instruct utter-project/EuroLLM-1.7B-Instruct; do
  tag=$(echo $m | sed 's#.*/##')
  run agp-probe-$tag ../stage2_$tag 0 true
  $L --label agp-probe-$tag -- /c/Users/caabm/Documents/Codex/2026-09-06/co/work/qwen-cuda-env/Scripts/python.exe -u src_probe.py --model $m --n 240 --out ../stage2_$tag; echo "STEP probe $tag rc=$?"
  run agp-fast-$tag ../fast_$tag 280 /c/Users/caabm/Documents/Codex/2026-09-06/co/work/qwen-cuda-env/Scripts/python.exe -u agp_fast.py --model $m --conds 1,gF,oF,gN,oN,gW,oW --seeds 300-339 --batch 4 --out ../fast_$tag
done
export AGP_4BIT=1
$L --label agp-probe-q4b -- /c/Users/caabm/Documents/agp-env/.venv/Scripts/python.exe -u src_probe.py --model Qwen/Qwen3-4B --n 240 --out ../stage2_Qwen3-4B; echo "STEP probe q4b rc=$?"
run agp-fast-q4b ../fast_Qwen3-4B 280 /c/Users/caabm/Documents/agp-env/.venv/Scripts/python.exe -u agp_fast.py --model Qwen/Qwen3-4B --conds 1,gF,oF,gN,oN,gW,oW --seeds 300-339 --batch 2 --out ../fast_Qwen3-4B
echo CHAIN2_DONE
