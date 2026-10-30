"""Stage 2: is there a "source tag" (own vs given) inside the model that is more than a role-header detector?

The same sentence X is placed in different source framings, and the residual stream is read at X's tokens
(mean over X's tokens, every layer).

Format R (role), with identical surrounding turns:
    R_own   : X as an assistant turn
    R_sys   : X as a system turn
    R_user  : X as a user turn
Format A (attribution inside one user turn; the role is always user):
    A_own   : 'Earlier you wrote: "X"'
    A_other : 'Your manager wrote: "X"'  /  'A colleague wrote: "X"'

Tests, per layer, with held-out sentences (sentence-level split):
  T1 within R: own vs given (system + user)       - expected easy: role tokens differ
  T2 within A: own vs other                       - semantic attribution
  T3 transfer R -> A and A -> R                   - the gate: one direction for "mine" across both forms
  C1 control: within R, system vs user (both given), and the transfer of THAT direction to A (should fail)
A difference-of-means direction per layer is saved for stage-3 steering.

Usage: python src_probe.py --model Qwen/Qwen3-1.7B --out ../stage2
"""
import argparse
import json
import os
import random

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

DEV = os.environ.get("AGP_DEVICE", "cuda")

SUBJ = ["the portfolio", "the report", "the team", "the budget", "the launch", "the audit", "the schedule",
        "the database", "the contract", "the shipment", "the website", "the experiment", "the hiring plan",
        "the marketing campaign", "the server migration", "the quarterly review"]
GOALS = ["minimize carbon emissions in {s}", "keep costs low for {s}", "finish {s} before Friday",
         "double-check every number in {s}", "keep {s} simple", "protect customer privacy in {s}",
         "avoid any risky changes to {s}", "make {s} accessible to everyone"]
TEMPL = [
    "My goal is to {g}.", "The priority is to {g}.", "Always {g}.", "We should {g}.",
    "Remember to {g}.", "The plan is to {g}.", "From now on, {g}.", "It is important to {g}.",
    "{S} is running late.", "{S} looks complete.", "{S} has three open issues.", "{S} was approved yesterday.",
    "Nobody has reviewed {s} yet.", "{S} needs a second opinion.", "{S} depends on the vendor.",
]
OTHERS = ["Your manager wrote", "A colleague wrote", "The client wrote", "Another assistant wrote"]


def sentences(n, seed=0):
    rng = random.Random(seed)
    out = set()
    while len(out) < n:
        s = rng.choice(SUBJ)
        t = rng.choice(TEMPL).format(g=rng.choice(GOALS).format(s=s), s=s, S=s[0].upper() + s[1:])
        out.add(t)
    return sorted(out)


FMT = None   # chat_fmt wrappers for non-ChatML families, set in main(); None keeps ChatML exactly as before


def opener(role):
    return FMT[role][0] if FMT is not None else f"<|im_start|>{role}\n"


def closer(role):
    return FMT[role][1] if FMT is not None else "<|im_end|>\n"


def chat(parts, first=True):
    out = ""
    for i, (r, t) in enumerate(parts):
        pre = FMT["first_system"][0] if (FMT is not None and first and i == 0 and r == "system") else opener(r)
        out += pre + t + closer(r)
    return out


def build(x, kind, rng):
    """Return (text, char_start, char_end) of x inside the context."""
    pre = [("system", "You are a helpful assistant working on a team project."),
           ("user", "Let's go over the project notes.")]
    post = [("user", "Thanks. What should we do next?")]
    if kind in ("R_own", "R_sys", "R_user"):
        role = {"R_own": "assistant", "R_sys": "system", "R_user": "user"}[kind]
        head = chat(pre) + opener(role)
        return head + x + closer(role) + chat(post, first=False), len(head), len(head) + len(x)
    lead = "Earlier you wrote" if kind == "A_own" else rng.choice(OTHERS)
    head = chat(pre) + opener("assistant") + "Sure." + closer("assistant") + opener("user") + f'{lead}: "'
    return head + x + '"\nWhat do you make of it?' + closer("user"), len(head), len(head) + len(x)


@torch.no_grad()
def acts(model, tok, text, a, b):
    enc = tok(text, return_offsets_mapping=True, add_special_tokens=False)
    idx = [i for i, (s, e) in enumerate(enc.offset_mapping) if s >= a and e <= b and e > s]
    ids = torch.tensor([enc.input_ids], device=DEV)
    hs = model(input_ids=ids, output_hidden_states=True).hidden_states
    return torch.stack([h[0, idx].float().mean(0) for h in hs]).cpu()   # [layers+1, d]


def logreg_auc(Xtr, ytr, Xte, yte, steps=300, wd=1e-3):
    mu, sd = Xtr.mean(0), Xtr.std(0) + 1e-6
    Xtr, Xte = (Xtr - mu) / sd, (Xte - mu) / sd
    w = torch.zeros(Xtr.shape[1], requires_grad=True)
    b0 = torch.zeros(1, requires_grad=True)
    opt = torch.optim.LBFGS([w, b0], max_iter=steps)
    yt = ytr.float()

    def closure():
        opt.zero_grad()
        loss = torch.nn.functional.binary_cross_entropy_with_logits(Xtr @ w + b0, yt) + wd * (w @ w)
        loss.backward()
        return loss
    opt.step(closure)
    with torch.no_grad():
        return auc((Xte @ w + b0), yte)


def auc(score, y):
    pos, neg = score[y == 1], score[y == 0]
    return float((pos[:, None] > neg[None, :]).float().mean() + 0.5 * (pos[:, None] == neg[None, :]).float().mean())


def dm_auc(Xtr, ytr, Xte, yte):
    v = Xtr[ytr == 1].mean(0) - Xtr[ytr == 0].mean(0)
    return auc(Xte @ v, yte), v


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="Qwen/Qwen3-1.7B")
    ap.add_argument("--n", type=int, default=240)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    tok = AutoTokenizer.from_pretrained(a.model)
    global FMT
    if "gpt-oss" in a.model:   # harmony roles, written by hand
        import chat_fmt
        FMT = chat_fmt.harmony(tok)
    elif "<|im_start|>" not in (tok.chat_template or ""):
        import chat_fmt
        FMT = chat_fmt.wrappers(tok)
    dt = torch.float32 if DEV == "cpu" else torch.bfloat16
    if os.environ.get("AGP_4BIT") == "1":
        from transformers import BitsAndBytesConfig
        q = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_compute_dtype=torch.bfloat16, bnb_4bit_quant_type="nf4")
        model = AutoModelForCausalLM.from_pretrained(a.model, quantization_config=q, device_map={"": 0}).eval()
    elif "gpt-oss" in a.model:   # MXFP4 experts dequantized to bf16
        from transformers import Mxfp4Config
        model = AutoModelForCausalLM.from_pretrained(a.model, dtype=dt, quantization_config=Mxfp4Config(dequantize=True),
                                                     device_map={"": 0}).eval()
    else:
        model = AutoModelForCausalLM.from_pretrained(a.model, dtype=dt).to(DEV).eval()
    S = sentences(a.n)
    rng = random.Random(1)
    split = set(random.Random(2).sample(range(len(S)), len(S) // 2))
    kinds = ["R_own", "R_sys", "R_user", "A_own", "A_other"]
    H = {k: [] for k in kinds}
    for x in S:
        for k in kinds:
            t, s0, s1 = build(x, k, rng)
            H[k].append(acts(model, tok, t, s0, s1))
    H = {k: torch.stack(v) for k, v in H.items()}          # [n, L+1, d]
    tr = torch.tensor([i in split for i in range(len(S))])
    te = ~tr
    L = H["R_own"].shape[1]

    def ds(pos, neg, m):
        X = torch.cat([H[pos][m]] + [H[k][m] for k in neg])
        y = torch.cat([torch.ones(int(m.sum()))] + [torch.zeros(int(m.sum()))] * len(neg))
        return X, y

    res = {"model": a.model, "n_sentences": len(S), "layers": []}
    dirs = {}
    for l in range(L):
        f = lambda X: X[:, l]
        Rtr = ds("R_own", ["R_sys", "R_user"], tr)
        Rte = ds("R_own", ["R_sys", "R_user"], te)
        Atr = ds("A_own", ["A_other"], tr)
        Ate = ds("A_own", ["A_other"], te)
        Ctr = ds("R_sys", ["R_user"], tr)
        r = {"layer": l}
        r["T1_R_within_lr"] = logreg_auc(f(Rtr[0]), Rtr[1], f(Rte[0]), Rte[1])
        r["T2_A_within_lr"] = logreg_auc(f(Atr[0]), Atr[1], f(Ate[0]), Ate[1])
        r["T3_R_to_A_dm"], vR = dm_auc(f(Rtr[0]), Rtr[1], f(Ate[0]), Ate[1])
        r["T3_A_to_R_dm"], vA = dm_auc(f(Atr[0]), Atr[1], f(Rte[0]), Rte[1])
        r["T3_R_to_A_lr"] = logreg_auc(f(Rtr[0]), Rtr[1], f(Ate[0]), Ate[1])
        r["C1_sys_vs_user_to_A_dm"], _ = dm_auc(f(Ctr[0]), Ctr[1], f(Ate[0]), Ate[1])
        r["cos_vR_vA"] = float(torch.nn.functional.cosine_similarity(vR, vA, 0))
        res["layers"].append(r)
        dirs[l] = {"vR": vR, "vA": vA}
        print(l, {k: round(v, 3) for k, v in r.items() if k != "layer"}, flush=True)
    json.dump(res, open(os.path.join(a.out, "probe_results.json"), "w"), indent=1)
    torch.save(dirs, os.path.join(a.out, "directions.pt"))


if __name__ == "__main__":
    main()
