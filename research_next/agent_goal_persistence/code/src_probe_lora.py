"""src_probe.py on a LoRA-adapted model: with AGP_LORA set, the adapter is merged into the weights right after
loading (as agp_batch does for evaluation), so vR is re-extracted inside the trained model. src_probe.py is unchanged.

Usage: AGP_LORA=<adapter dir> python src_probe_lora.py --model Qwen/Qwen3-8B --n 240 --out <dir>
"""
import os

import src_probe

_load = src_probe.AutoModelForCausalLM.from_pretrained


def _load_merged(*args, **kw):
    m = _load(*args, **kw)
    if os.environ.get("AGP_LORA"):
        from peft import PeftModel
        m = PeftModel.from_pretrained(m, os.environ["AGP_LORA"]).merge_and_unload()
    return m


src_probe.AutoModelForCausalLM.from_pretrained = _load_merged

if __name__ == "__main__":
    src_probe.main()
