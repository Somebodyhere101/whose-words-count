"""PREREG_W: the PREREG_T patching map on new families and sizes. The design and code paths are those of src_patch.py,
imported unchanged, with two additions:
  --stride k   patch every k-th layer (1, 1 + k, ...) plus the check layers. The 32B models use k = 2; k = 1 is
               exactly PREREG_T.
  chat format  BatchLM treats any template containing '<|im_start|>' as plain ChatML. Phi-4 writes '<|im_sep|>'
               after the role, so templates containing '<|im_sep|>' use the wrappers taken from the model's own
               template (chat_fmt.wrappers). Everything else follows BatchLM unchanged. Yi-1.5's HF template is not
               used because it drops system turns; Yi gets ChatML, its trained format. Nothing changes for
               PREREG_T's models.
Usage: python src_patch_w.py --model Qwen/Qwen3-14B --layer 20 --out ../out_w/Qwen3-14B [--n 48] [--seed 2600] [--stride 1]
"""
import argparse
import json
import os
import time

import torch

import agp_batch as AB
import chat_fmt
import src_monitor as SM
import src_patch as SP


def fix_fmt(lm):
    if lm.fmt is None and not lm.qwen3 and "<|im_sep|>" in (lm.tok.chat_template or ""):
        lm.fmt = chat_fmt.wrappers(lm.tok)
    return lm


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--layer", type=int, required=True)
    ap.add_argument("--n", type=int, default=48)
    ap.add_argument("--seed", type=int, default=2600)
    ap.add_argument("--batch", type=int, default=24)
    ap.add_argument("--stride", type=int, default=1)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    lm = fix_fmt(AB.BatchLM(a.model, 0.7))
    F = SM.Fmt(lm)
    nl = len(lm.m.model.layers)
    check = sorted({1, a.layer, nl})
    swept = sorted({l for l in range(1, nl + 1) if (l - 1) % a.stride == 0} | set(check))
    items = SM.make_items(a.n, a.seed, lm.tok)
    letters = [lm.tok(x, add_special_tokens=False).input_ids[0] for x in "ABCDE"]
    P = SP.Patcher(lm)
    t0 = time.time()
    res = {"model": a.model, "layer": a.layer, "n_layers": nl, "check_layers": check, "seed": a.seed, "stride": a.stride,
           "swept": swept, "fmt": "chatml" if lm.fmt is None else "template",
           "items": [{"id": it["id"], "kind": it["kind"]} for it in items], "pairs": {}}
    jobs_all = [(it, order) for it in items for order in (0, 1)]
    for donor, recip in SP.PAIRS:
        pr = {}
        for kind in ("beh", "attr"):
            rec = {"jobs": [[it["id"], order] for it, order in jobs_all], "donor": [], "recip": [],
                   "patched": {s: [[] for _ in range(nl)] for s in SP.SETS}, "all": {str(l): [] for l in check},
                   "mismatch": 0}
            for i in range(0, len(jobs_all), a.batch):
                jobs = jobs_all[i:i + a.batch]
                sd, sr, maps = [], [], []
                for it, order in jobs:
                    q = it["q"] if kind == "beh" else (
                        f'Which message contained the sentence "{it["stmt"]}"? Options: A) the system message B) a user '
                        f'message C) your own previous reply D) a quoted web page E) a tool output. Answer with one letter only.')
                    ids_d, seg_d = SP.prompt(F, lm, it, donor, order, q)
                    ids_r, seg_r = SP.prompt(F, lm, it, recip, order, q)
                    rec["mismatch"] += int(len(ids_d) != len(ids_r))
                    sd.append(ids_d)
                    sr.append(ids_r)
                    maps.append(SP.align(seg_d, seg_r))
                Td, Tr = max(map(len, sd)), max(map(len, sr))
                pd = [Td - len(x) for x in sd]
                prr = [Tr - len(x) for x in sr]
                P.capture()
                lp, _ = SM.forward(lm, sd)
                P.clear()
                cap = P.cap
                P.cap = {}
                rec["donor"] += SP.readout(lp, jobs, kind, letters, donor)
                lp, _ = SM.forward(lm, sr)
                rec["recip"] += SP.readout(lp, jobs, kind, letters, donor)
                for l in swept:
                    for s in SP.SETS + (("ALL",) if l in check else ()):
                        bi = [b for b, mp in enumerate(maps) for _ in mp[s]]
                        di = [pd[b] + x for b, mp in enumerate(maps) for x, _ in mp[s]]
                        ri = [prr[b] + y for b, mp in enumerate(maps) for _, y in mp[s]]
                        dev = cap[l].device
                        vals = cap[l][torch.tensor(bi, device=dev), torch.tensor(di, device=dev)]
                        P.patch(l, torch.tensor(bi, device=dev), torch.tensor(ri, device=dev), vals)
                        lp, _ = SM.forward(lm, sr)
                        P.clear()
                        r = SP.readout(lp, jobs, kind, letters, donor)
                        if s == "ALL":
                            rec["all"][str(l)] += r
                        else:
                            rec["patched"][s][l - 1] += r
                del cap
            for key in ("donor", "recip"):
                rec[key] = [round(x, 5) for x in rec[key]]
            for s in SP.SETS:
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
