cd "/c/Users/caabm/AppData/Roaming/Claude/scratch-workspaces/2898f83d-79d0-4cb9-a017-7d323d549974/0c4963d8-51ed-4ceb-9445-28b8639f6fa1/scratch-2026-10-13-464f6a/research_next/agent_goal_persistence/code"
export AGP_4BIT=1
for i in 1 2 3; do /c/Users/caabm/Documents/Codex/2026-09-06/co/work/qwen-cuda-env/Scripts/python.exe /c/Users/caabm/AppData/Roaming/Claude/scratch-workspaces/2898f83d-79d0-4cb9-a017-7d323d549974/0c4963d8-51ed-4ceb-9445-28b8639f6fa1/scratch-2026-10-13-464f6a/tools/gpu_lock.py --max-min 90 --label agp-stage3-smol3w -- /c/Users/caabm/Documents/agp-env/.venv/Scripts/python.exe -u steer_run.py --model HuggingFaceTB/SmolLM3-3B --cells gW,oW --dirs ../stage2_SmolLM3-3B/directions.pt --layers 7,15 --batch 2 --out ../stage3w_SmolLM3-3B && break; done
echo CHAIN7_DONE
