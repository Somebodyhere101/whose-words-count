"""Per-role chat wrappers taken from a model's own chat template, so the instrument works beyond Qwen/ChatML.

Segments are obtained by rendering growing conversations and taking string differences:
  system    = render([S])
  user      = render([S, U]) - render([S])
  assistant = render([S, U, A]) - render([S, U])
  header    = render([S, U], add_generation_prompt) - render([S, U])
Each segment is split around its placeholder content into (prefix, suffix). The first system segment may carry a
BOS token; `first_system` keeps it, and later system inserts use the same wrapper without the BOS.
Mid-conversation system messages reuse the system wrapper even where a template would not render them.
"""
P = {"system": "QQSYSQQ", "user": "QQUSRQQ", "assistant": "QQASTQQ"}


def wrappers(tok):
    r = lambda m, gen=False: tok.apply_chat_template(m, tokenize=False, add_generation_prompt=gen)
    S = [{"role": "system", "content": P["system"]}]
    SU = S + [{"role": "user", "content": P["user"]}]
    SUA = SU + [{"role": "assistant", "content": P["assistant"]}]
    s0, s1, s2 = r(S), r(SU), r(SUA)
    g = r(SU, True)
    for a, b in ((s0, s1), (s1, s2), (s1, g)):
        if not b.startswith(a):
            raise ValueError("chat template is not prefix-stable; cannot derive segments")
    segs = {"system": s0, "user": s1[len(s0):], "assistant": s2[len(s1):]}
    out = {}
    for role, seg in segs.items():
        pre, suf = seg.split(P[role])
        out[role] = (pre, suf)
    out["header"] = g[len(s1):]
    bos = tok.bos_token or ""
    sys_pre = out["system"][0]
    out["first_system"] = out["system"]
    if bos and sys_pre.startswith(bos):
        out["system"] = (sys_pre[len(bos):], out["system"][1])
    return out


def plain(tok):
    """Plain-text transcript labels with no special tokens, so a base model and its post-trained checkpoints read
    the same format (lineage study). The episode starts with the tokenizer's BOS, as a pretraining document does.
    'readout' ends every decision prompt and is tokenized as one string, so ' ALLOCATE' keeps its leading space."""
    bos = tok.bos_token or ""
    out = {r: (f"{r.upper()}: ", "\n\n") for r in ("system", "user", "assistant")}
    out["first_system"] = (bos + "SYSTEM: ", "\n\n")
    out["header"] = "ASSISTANT:"
    out["readout"] = "ASSISTANT: ALLOCATE:"
    return out


def render(w, role, text, first=False):
    pre, suf = w["first_system"] if (first and role == "system") else w[role]
    return pre + text + suf
