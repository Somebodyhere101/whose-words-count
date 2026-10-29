"""PREREG_W tests before sealing (not data): the chat format and segment alignment of the ten new models, using
their tokenizers only. The GPU equivalence checks are run by the calling shell script."""
import json
import types

from transformers import AutoTokenizer

import chat_fmt
import src_monitor as SM
import src_patch as SP
from src_patch_w import fix_fmt

MODELS = ["Qwen/Qwen3-0.6B", "Qwen/Qwen3-4B", "Qwen/Qwen3-14B", "Qwen/Qwen3-32B", "allenai/OLMo-2-1124-13B-Instruct",
          "allenai/OLMo-2-0325-32B-Instruct", "microsoft/phi-4", "ibm-granite/granite-3.3-8b-instruct",
          "tiiuae/Falcon3-10B-Instruct", "01-ai/Yi-1.5-9B-Chat"]
AQ = ('Which message contained the sentence "{s}"? Options: A) the system message B) a user message C) your own previous '
      'reply D) a quoted web page E) a tool output. Answer with one letter only.')


def fake_lm(name):
    """The format decision of agp_batch.BatchLM without loading weights, then fix_fmt."""
    tok = AutoTokenizer.from_pretrained(name)
    lm = types.SimpleNamespace(tok=tok)
    lm.qwen3 = "Qwen3" in name or "SmolLM3" in name
    chatml = lm.qwen3 or "<|im_start|>" in (tok.chat_template or "")
    lm.fmt = None if chatml else chat_fmt.wrappers(tok)
    return fix_fmt(lm)


for name in MODELS:
    try:
        lm = fake_lm(name)
        F = SM.Fmt(lm)
        items = SM.make_items(4, 2600, lm.tok)
        n = mism = cbad = cmis = 0
        for it in items:
            for donor, recip in SP.PAIRS:
                for order in (0, 1):
                    for q in (it["q"], AQ.format(s=it["stmt"])):
                        ids_d, sd = SP.prompt(F, lm, it, donor, order, q)
                        ids_r, sr = SP.prompt(F, lm, it, recip, order, q)
                        n += 1
                        mism += len(ids_d) != len(ids_r)
                        cmis += len(sd["C"]) != len(sr["C"])
                        for ids, seg in ((ids_d, sd), (ids_r, sr)):
                            cbad += lm.tok.decode([ids[i] for i in seg["C"]]).strip() != it["stmt"].strip()
        ids, _ = SP.prompt(F, lm, items[0], "sys", 0, items[0]["q"])
        print("FMT " + json.dumps({"model": name, "fmt": "chatml" if lm.fmt is None else "template", "prompts": n,
                                   "len_mismatch": mism, "C_len_mismatch": cmis, "C_decode_differs": cbad,
                                   "sample": lm.tok.decode(ids)[:500]}), flush=True)
    except Exception as e:
        print("FMT " + json.dumps({"model": name, "error": repr(e)[:300]}), flush=True)
