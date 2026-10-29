"""PREREG_T: where is the source signal that the model uses? Activation patching between two runs that differ only in
the role of the statement's turn (donor 'own' or 'sys', recipient 'usr'). Fresh items, seed 2200.

For each item, order and readout (the behaviour prompt and the attribution prompt of PREREG_S), the donor run is
cached at every layer. The recipient run is then repeated with the residual stream at one layer replaced by the
donor's on one position set:
  M   = the turn's marker tokens (the role prefix and the end tokens);
  C   = the statement's content tokens;
  D   = every position after the turn (the competing message, the question and the answer header);
  ALL = M + C + D, a sanity check at the first, the decision and the last layer; it must reproduce the donor.
Positions are aligned segment by segment: the prefix and the content from the start, the end tokens and D from the
end. (OLMo's 'assistant' turn ends in its EOS token while user turns end in a newline that can merge with the last
character of the statement, so the two can differ by a token there.)
Readouts as in PREREG_S: obey / believe score P(A) / (P(A) + P(B)), and attribution P(letter of the donor's source)
among the five letters.
Usage: python src_patch.py --model Qwen/Qwen3-1.7B --layer 13 --out ../out_t/Qwen3-1.7B [--n 48] [--seed 2200]
"""
import argparse
import json
import os
import time

import torch

import agp_batch as AB
import src_monitor as SM

PAIRS = (("own", "usr"), ("sys", "usr"))     # (donor, recipient)
SETS = ("M", "C", "D")


def prompt(F, lm, it, src, order, q):
    """Token ids of the full prompt and its segments: pre (role prefix), C, suf (end tokens), D (after the turn)."""
    msgs = SM.contexts(it, src, order) + [("user", q)]
    turn = 1 if order == 0 else 2
    s = ""
    for i, (role, text) in enumerate(msgs):
        m = F.msg(role, text, first=(i == 0))
        if i == turn:
            k = m.index(text)
            t0, c0, c1, t1 = len(s), len(s) + k, len(s) + k + len(text), len(s) + len(m)
        s += m
    enc = lm.tok(s + F.header(), return_offsets_mapping=True, add_special_tokens=False)
    seg = {"pre": [], "C": [], "suf": [], "D": []}
    for i, (a, b) in enumerate(enc.offset_mapping):
        if a < t0:
            continue
        seg["D" if a >= t1 else "suf" if a >= c1 else "C" if a >= c0 else "pre"].append(i)
    return enc.input_ids, seg


def align(sd, sr):
    """Pairs (donor position, recipient position) per patch set, unpadded."""
    z = lambda a, b, end: list(zip(a[-len(b):] if end and len(a) > len(b) else a, b[-len(a):] if end and len(b) > len(a) else b))
    m = z(sd["pre"], sr["pre"], False) + z(sd["suf"], sr["suf"], True)
    out = {"M": m, "C": z(sd["C"], sr["C"], False), "D": z(sd["D"], sr["D"], True)}
    out["ALL"] = out["M"] + out["C"] + out["D"]
    return out


class Patcher:
    def __init__(self, lm):
        self.lm, self.hs, self.cap = lm, [], {}

    def capture(self):
        for l in range(1, len(self.lm.m.model.layers) + 1):
            def hook(mod, inp, out, l=l):
                self.cap[l] = (out[0] if isinstance(out, tuple) else out).detach()
            self.hs.append(self.lm.m.model.layers[l - 1].register_forward_hook(hook))

    def patch(self, l, bi, ri, vals):
        def hook(mod, inp, out):
            h = (out[0] if isinstance(out, tuple) else out).clone()
            h[bi, ri] = vals.to(h.dtype)
            return (h,) + tuple(out[1:]) if isinstance(out, tuple) else h
        self.hs.append(self.lm.m.model.layers[l - 1].register_forward_hook(hook))

    def clear(self):
        for h in self.hs:
            h.remove()
        self.hs = []


def readout(lp, jobs, kind, letters, donor):
    out = []
    for j, (it, order) in enumerate(jobs):
        if kind == "beh":
            pa, pb = lp[j, it["fa"]].exp().item(), lp[j, it["fb"]].exp().item()
            out.append(pa / (pa + pb) if pa + pb > 0 else 0.5)
        else:
            pl = lp[j, letters].exp()
            out.append(float(pl["ABCDE".index(SM.LETTER[donor])] / pl.sum()))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--layer", type=int, required=True)
    ap.add_argument("--n", type=int, default=48)
    ap.add_argument("--seed", type=int, default=2200)
    ap.add_argument("--batch", type=int, default=24)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    lm = AB.BatchLM(a.model, 0.7)
    F = SM.Fmt(lm)
    nl = len(lm.m.model.layers)
    check = sorted({1, a.layer, nl})
    items = SM.make_items(a.n, a.seed, lm.tok)
    letters = [lm.tok(x, add_special_tokens=False).input_ids[0] for x in "ABCDE"]
    P = Patcher(lm)
    t0 = time.time()
    res = {"model": a.model, "layer": a.layer, "n_layers": nl, "check_layers": check, "seed": a.seed,
           "items": [{"id": it["id"], "kind": it["kind"]} for it in items], "pairs": {}}
    jobs_all = [(it, order) for it in items for order in (0, 1)]
    for donor, recip in PAIRS:
        pr = {}
        for kind in ("beh", "attr"):
            rec = {"jobs": [[it["id"], order] for it, order in jobs_all], "donor": [], "recip": [],
                   "patched": {s: [[] for _ in range(nl)] for s in SETS}, "all": {str(l): [] for l in check},
                   "mismatch": 0}
            for i in range(0, len(jobs_all), a.batch):
                jobs = jobs_all[i:i + a.batch]
                sd, sr, maps = [], [], []
                for it, order in jobs:
                    q = it["q"] if kind == "beh" else (
                        f'Which message contained the sentence "{it["stmt"]}"? Options: A) the system message B) a user '
                        f'message C) your own previous reply D) a quoted web page E) a tool output. Answer with one letter only.')
                    ids_d, seg_d = prompt(F, lm, it, donor, order, q)
                    ids_r, seg_r = prompt(F, lm, it, recip, order, q)
                    rec["mismatch"] += int(len(ids_d) != len(ids_r))
                    sd.append(ids_d)
                    sr.append(ids_r)
                    maps.append(align(seg_d, seg_r))
                Td, Tr = max(map(len, sd)), max(map(len, sr))
                pd = [Td - len(x) for x in sd]
                prr = [Tr - len(x) for x in sr]
                P.capture()
                lp, _ = SM.forward(lm, sd)
                P.clear()
                cap = P.cap
                P.cap = {}
                rec["donor"] += readout(lp, jobs, kind, letters, donor)
                lp, _ = SM.forward(lm, sr)
                rec["recip"] += readout(lp, jobs, kind, letters, donor)
                for l in range(1, nl + 1):
                    for s in SETS + (("ALL",) if l in check else ()):
                        bi = [b for b, mp in enumerate(maps) for _ in mp[s]]
                        di = [pd[b] + x for b, mp in enumerate(maps) for x, _ in mp[s]]
                        ri = [prr[b] + y for b, mp in enumerate(maps) for _, y in mp[s]]
                        dev = cap[l].device
                        vals = cap[l][torch.tensor(bi, device=dev), torch.tensor(di, device=dev)]
                        P.patch(l, torch.tensor(bi, device=dev), torch.tensor(ri, device=dev), vals)
                        lp, _ = SM.forward(lm, sr)
                        P.clear()
                        r = readout(lp, jobs, kind, letters, donor)
                        if s == "ALL":
                            rec["all"][str(l)] += r
                        else:
                            rec["patched"][s][l - 1] += r
                del cap
            for key in ("donor", "recip"):
                rec[key] = [round(x, 5) for x in rec[key]]
            for s in SETS:
                rec["patched"][s] = [[round(x, 5) for x in row] for row in rec["patched"][s]]
            for l in rec["all"]:
                rec["all"][l] = [round(x, 5) for x in rec["all"][l]]
            pr[kind] = rec
            print(f"{donor}->{recip} {kind} done {time.time() - t0:.0f} s, length mismatches {rec['mismatch']}", flush=True)
        res["pairs"][f"{donor}->{recip}"] = pr
    json.dump(res, open(os.path.join(a.out, "patch.json"), "w"))
    print("PATCH_DONE", flush=True)


if __name__ == "__main__":
    main()
