# Night-1 chain: run-B analysis, then stage-1 fast validation, then stage-2 probe (all GPU work via gpu_lock).
cd "/c/Users/caabm/AppData/Roaming/Claude/scratch-workspaces/2898f83d-79d0-4cb9-a017-7d323d549974/0c4963d8-51ed-4ceb-9445-28b8639f6fa1/scratch-2026-10-13-464f6a/research_next/agent_goal_persistence/code"
until grep -q "^DONE" ../main_b.log; do sleep 60; done
/c/Users/caabm/Documents/Codex/2026-09-06/co/work/qwen-cuda-env/Scripts/python.exe -I analyze_b.py ../main_b > ../main_b_analysis.txt 2>&1; echo "STEP runB_analysis rc=$?"
for i in 1 2 3 4; do
  n=$(ls ../fast_val 2>/dev/null | grep -c json); [ "$n" -ge 200 ] && break
  /c/Users/caabm/Documents/Codex/2026-09-06/co/work/qwen-cuda-env/Scripts/python.exe /c/Users/caabm/AppData/Roaming/Claude/scratch-workspaces/2898f83d-79d0-4cb9-a017-7d323d549974/0c4963d8-51ed-4ceb-9445-28b8639f6fa1/scratch-2026-10-13-464f6a/tools/gpu_lock.py --label agp-fastval --max-min 90 -- /c/Users/caabm/Documents/Codex/2026-09-06/co/work/qwen-cuda-env/Scripts/python.exe -u agp_fast.py --conds 1,gF,oF,gN,oN --seeds 300-339 --batch 4 --out ../fast_val
done
echo "STEP fast_val n=$(ls ../fast_val | grep -c json)"
/c/Users/caabm/Documents/Codex/2026-09-06/co/work/qwen-cuda-env/Scripts/python.exe /c/Users/caabm/AppData/Roaming/Claude/scratch-workspaces/2898f83d-79d0-4cb9-a017-7d323d549974/0c4963d8-51ed-4ceb-9445-28b8639f6fa1/scratch-2026-10-13-464f6a/tools/gpu_lock.py --label agp-stage2 --max-min 90 -- /c/Users/caabm/Documents/Codex/2026-09-06/co/work/qwen-cuda-env/Scripts/python.exe -u src_probe.py --model Qwen/Qwen3-1.7B --n 240 --out ../stage2; echo "STEP stage2 rc=$?"
echo CHAIN_DONE
