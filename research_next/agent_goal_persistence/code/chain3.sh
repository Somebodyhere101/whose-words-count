cd "/c/Users/caabm/AppData/Roaming/Claude/scratch-workspaces/2898f83d-79d0-4cb9-a017-7d323d549974/0c4963d8-51ed-4ceb-9445-28b8639f6fa1/scratch-2026-10-13-464f6a/research_next/agent_goal_persistence/code"
L="/c/Users/caabm/Documents/Codex/2026-09-06/co/work/qwen-cuda-env/Scripts/python.exe /c/Users/caabm/AppData/Roaming/Claude/scratch-workspaces/2898f83d-79d0-4cb9-a017-7d323d549974/0c4963d8-51ed-4ceb-9445-28b8639f6fa1/scratch-2026-10-13-464f6a/tools/gpu_lock.py --max-min 90"
for i in 1 2 3; do $L --label agp-stage3 -- /c/Users/caabm/Documents/Codex/2026-09-06/co/work/qwen-cuda-env/Scripts/python.exe -u steer_run.py --seeds 400-419 --out ../stage3 && break; done; echo "STEP stage3 n=$(ls ../stage3 | wc -l)"
export AGP_4BIT=1
$L --label agp-probe-q4b -- /c/Users/caabm/Documents/agp-env/.venv/Scripts/python.exe -u src_probe.py --model Qwen/Qwen3-4B --n 240 --out ../stage2_Qwen3-4B; echo "STEP probe q4b rc=$?"
for i in 1 2 3 4; do n=$(ls ../fast_Qwen3-4B 2>/dev/null | grep -c json); [ "$n" -ge 280 ] && break; $L --label agp-fast-q4b -- /c/Users/caabm/Documents/agp-env/.venv/Scripts/python.exe -u agp_fast.py --model Qwen/Qwen3-4B --conds 1,gF,oF,gN,oN,gW,oW --seeds 300-339 --batch 2 --out ../fast_Qwen3-4B; done; echo "STEP fast q4b n=$(ls ../fast_Qwen3-4B | grep -c json)"
unset AGP_4BIT
for i in 1 2 3 4; do n=$(ls ../fast_SmolLM2-1.7B-Instruct 2>/dev/null | grep -c json); [ "$n" -ge 280 ] && break; $L --label agp-fast-smol -- /c/Users/caabm/Documents/Codex/2026-09-06/co/work/qwen-cuda-env/Scripts/python.exe -u agp_fast.py --model HuggingFaceTB/SmolLM2-1.7B-Instruct --conds 1,gF,oF,gN,oN,gW,oW --seeds 300-339 --batch 1 --out ../fast_SmolLM2-1.7B-Instruct; done; echo "STEP fast smol n=$(ls ../fast_SmolLM2-1.7B-Instruct | grep -c json)"
echo CHAIN3_DONE
