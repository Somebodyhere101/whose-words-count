#!/bin/bash
# Run once on a fresh RunPod PyTorch pod (A100 80 GB). Expects the code folder uploaded to /workspace/agp/code.
set -e
python -c "import torch;print('torch',torch.__version__,'cuda',torch.cuda.is_available(),torch.cuda.get_device_name(0))"
pip install -q "transformers==5.16.1" accelerate
export HF_HOME=/workspace/hf
mkdir -p /workspace/hf /workspace/agp
python - <<'EOF'
from huggingface_hub import snapshot_download
for m in ["Qwen/Qwen3-8B", "Qwen/Qwen3-14B"]:
    snapshot_download(m)
    print("downloaded", m)
EOF
echo "setup done"
