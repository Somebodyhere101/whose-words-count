set -e
/c/Users/caabm/Documents/Codex/2026-09-06/co/work/qwen-cuda-env/Scripts/python.exe -u agp.py --conds 1 --seeds 0-3 --n-drift 0 --n-a 1 --no-pressure --out ../calib/a1np
/c/Users/caabm/Documents/Codex/2026-09-06/co/work/qwen-cuda-env/Scripts/python.exe -u agp.py --conds 1 --seeds 0-3 --n-drift 0 --n-a 2 --no-pressure --out ../calib/a2np
/c/Users/caabm/Documents/Codex/2026-09-06/co/work/qwen-cuda-env/Scripts/python.exe -u agp.py --conds 1 --seeds 3-6 --n-drift 0 --n-a 0 --out ../calib/base_p
/c/Users/caabm/Documents/Codex/2026-09-06/co/work/qwen-cuda-env/Scripts/python.exe -u agp.py --conds 1 --seeds 0-3 --n-drift 0 --n-a 1 --out ../calib/a1p
