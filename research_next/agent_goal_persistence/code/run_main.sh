# Runs the preregistered main run; restarts after each gpu_lock deadline until all 160 runs exist.
cd "/c/Users/caabm/AppData/Roaming/Claude/scratch-workspaces/2898f83d-79d0-4cb9-a017-7d323d549974/0c4963d8-51ed-4ceb-9445-28b8639f6fa1/scratch-2026-10-13-464f6a/research_next/agent_goal_persistence/code"
for i in 1 2 3 4 5 6 7 8; do
  n=$(ls ../main 2>/dev/null | grep -c json)
  [ "$n" -ge 160 ] && break
  /c/Users/caabm/Documents/Codex/2026-09-06/co/work/qwen-cuda-env/Scripts/python.exe /c/Users/caabm/AppData/Roaming/Claude/scratch-workspaces/2898f83d-79d0-4cb9-a017-7d323d549974/0c4963d8-51ed-4ceb-9445-28b8639f6fa1/scratch-2026-10-13-464f6a/tools/gpu_lock.py --label agp-main --max-min 90 -- /c/Users/caabm/Documents/Codex/2026-09-06/co/work/qwen-cuda-env/Scripts/python.exe -u agp.py --conds 3,2p,2,3f --seeds 100-139 --n-drift 0 --n-a 0 --out ../main
done
echo DONE $(ls ../main | grep -c json)
