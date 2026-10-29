"""Independent recomputation of the PREREG_S rule (b) fractions (source / content / floor) for Qwen3-1.7B, following
s_jspace.py exactly but WITHOUT model weights (the J-lens token readings, which need W_U, are not recomputed).
Both files are loaded with weights_only=True (safe unpickler). Writes nothing in RF.
"""
import json
import sys

import torch

K = 64


def frac(V, P):
    return float(((V @ P) ** 2).sum() / (V ** 2).sum())


reps_path, jlens_path = sys.argv[1], sys.argv[2]
R = torch.load(reps_path, weights_only=True)
JL = torch.load(jlens_path, map_location="cpu", weights_only=True)
meta = {k: (type(v).__name__ if not isinstance(v, (int, float, str)) else v) for k, v in JL.items() if k != "J"}
J = JL["J"]
src = list(R["sources"])
out = {"jlens_meta": meta, "jlens_layers": sorted(J.keys())[:3] + ["..."] + sorted(J.keys())[-2:], "reps_layers": R["layers"], "layers": {}}
for l in R["layers"]:
    if l not in J:
        continue
    X = R["reps"][l].float()
    C = X.mean(0)
    Vs = C - C.mean(0)
    Sm = X.mean(1)
    Vc = Sm - Sm.mean(0)
    Jl = J[l].float()
    _, _, Vh = torch.linalg.svd(Jl)
    P = Vh[:K].T
    pair = {f"{s}-usr": round(frac((C[src.index(s)] - C[src.index('usr')])[None], P), 4) for s in src if s != "usr"}
    X1 = R["reps_set1"][l].float()
    C1, S1 = X1.mean(0), X1.mean(1)
    out["layers"][l] = {"source": round(frac(Vs, P), 4), "content": round(frac(Vc, P), 4), "floor": round(K / Jl.shape[0], 4),
                        "pairs": pair, "set1_source": round(frac(C1 - C1.mean(0), P), 4), "set1_content": round(frac(S1 - S1.mean(0), P), 4),
                        "J_shape": list(Jl.shape), "J_dtype": str(J[l].dtype), "X_shape": list(X.shape)}
v = out["layers"][13]
out["verdict_L13"] = "OUTSIDE" if v["source"] <= 2 * v["floor"] else "INSIDE" if v["source"] >= v["content"] else "BETWEEN"
print(json.dumps(out, indent=1))
