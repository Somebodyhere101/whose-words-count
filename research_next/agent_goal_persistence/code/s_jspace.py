"""PREREG_S (b), fixed before data: does the source tag of Qwen3-1.7B lie inside or outside the J-space?

Usage: python s_jspace.py --reps <out_s/Qwen3-1.7B/reps.pt> --jlens <Qwen3-1.7B_jacobian_lens.pt> --model Qwen/Qwen3-1.7B
J-space proxy at layer l, as in the September CED work: the span of the top K = 64 right singular vectors of the
fitted Jacobian J_l (the user's WikiText J-lens, 466 prompts). For each stored layer:
  source  = fraction of the variance of the 5 source centroids around their mean (a 4-dim subspace) in the proxy;
  content = the same fraction for the sentence-to-sentence variation of the 40 neutral sentences (source-averaged);
  floor   = K / d for a random direction (64 / 2048 = 0.031).
Rule at the decision layer 13: OUTSIDE if source <= 2 x floor; INSIDE if source >= content; BETWEEN otherwise.
Also reported: the J-lens reading of each source direction (top tokens of W_U J_l c, c = centroid - mean), and
the fraction of each pairwise source direction (own - usr, sys - usr, doc - usr, tool - usr).
"""
import argparse
import json

import torch

K = 64


def frac(V, P):
    """Fraction of the total squared norm of the rows of V inside the subspace with orthonormal columns P."""
    return float(((V @ P) ** 2).sum() / (V ** 2).sum())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--reps", required=True)
    ap.add_argument("--jlens", required=True)
    ap.add_argument("--model", required=True)
    ap.add_argument("--out", default="s_jspace.json")
    a = ap.parse_args()
    R = torch.load(a.reps)
    J = torch.load(a.jlens, map_location="cpu", weights_only=False)["J"]
    from transformers import AutoModelForCausalLM, AutoTokenizer
    tok = AutoTokenizer.from_pretrained(a.model)
    WU = AutoModelForCausalLM.from_pretrained(a.model, dtype=torch.float32).lm_head.weight.detach()
    res, src = {}, R["sources"]
    seen = {}
    if "reps_set1" in R:                                   # set 1 was seen before sealing (CPU smoke); reported only
        for l in R["layers"]:
            if l in J:
                X1 = R["reps_set1"][l].float()
                C1, Sm1 = X1.mean(0), X1.mean(1)
                _, _, Vh1 = torch.linalg.svd(J[l].float())
                seen[l] = {"source": round(frac(C1 - C1.mean(0), Vh1[:K].T), 4), "content": round(frac(Sm1 - Sm1.mean(0), Vh1[:K].T), 4)}
    for l in R["layers"]:
        if l not in J:
            continue
        X = R["reps"][l].float()                           # [sentences, sources, d], fresh set 2 (sealed)
        C = X.mean(0)                                      # source centroids
        Vs = C - C.mean(0)                                 # source variation
        Sm = X.mean(1)
        Vc = Sm - Sm.mean(0)                               # content variation
        Jl = J[l].float()
        _, _, Vh = torch.linalg.svd(Jl)
        P = Vh[:K].T                                       # top-K right singular vectors, [d, K]
        pair = {f"{s}-usr": frac((C[src.index(s)] - C[src.index('usr')])[None], P) for s in src if s != "usr"}
        read = {}
        for i, s in enumerate(src):
            lg = WU @ (Jl @ Vs[i])
            read[s] = [tok.decode([t]) for t in lg.topk(8).indices.tolist()]
        res[l] = {"source": round(frac(Vs, P), 4), "content": round(frac(Vc, P), 4), "floor": round(K / Jl.shape[0], 4),
                  "pairs": {k: round(v, 4) for k, v in pair.items()}, "jlens_reading": read}
        print(l, res[l]["source"], res[l]["content"], res[l]["floor"], flush=True)
    L = 13
    v = res[L]
    verdict = "OUTSIDE" if v["source"] <= 2 * v["floor"] else "INSIDE" if v["source"] >= v["content"] else "BETWEEN"
    json.dump({"decision_layer": L, "verdict": verdict, "layers": res, "set1_seen_before_sealing": seen}, open(a.out, "w"), indent=1)
    print("verdict", verdict)


if __name__ == "__main__":
    main()
