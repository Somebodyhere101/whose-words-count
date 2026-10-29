"""PILOT_V1 (exploratory; rules in PILOT_V1.md): a format-matched steering direction for injections embedded in a message.

InjecAgent dev cases: 60 base cases (seed 2900) outside the 300 PREREG_X test cases (seed 2800 sample, as in bench.py).
Directions, each a difference of mean sentence-token states over the 40 PREREG_S set-2 sentences, at the chosen layer:
  tool-usr   the PREREG_X recipe direction (lever_pilot.means: separate tool and user turns)
  obs-input  format-matched: the sentence as the scratchpad Observation, minus the sentence as the User Input (with a
             neutral observation '{"status": "ok"}'), both inside the InjecAgent prompt of the first dev case
Grid: obs-input at depths 0.35/0.45/0.55/0.65 x scales 4/8, and tool-usr at 0.45 x 4/8, applied to the observation's own
tokens; plus no defence. Readout: bench.ia_eval (the repository's evaluator, re-implemented).
Usage: python ia_pilot.py --model Qwen/Qwen3-8B --data <injecagent data dir> --prompts <prompts.json> --out ../out_v1/Qwen3-8B
"""
import argparse
import json
import os
import random
import time

import torch

import agp_batch as AB
import bench as BE
import lever_pilot as LP
import src_monitor as SM
import src_patch as SP
from src_patch_w import fix_fmt

CONFIGS = ([("obs-input", d, s) for d in (0.35, 0.45, 0.55, 0.65) for s in (4, 8)] +
           [("tool-usr", 0.45, s) for s in (4, 8)])
NEUTRAL_OBS = '{"status": "ok"}'


def dev_cases(cases, n_test=300, seed_test=2800, n_dev=60, seed_dev=2900):
    test = set(random.Random(seed_test).sample(range(len(cases)), n_test))
    rest = [i for i in range(len(cases)) if i not in test]
    return [cases[i] for i in sorted(random.Random(seed_dev).sample(rest, n_dev))]


def fmt_means(lm, F, P, nl, tools, case, prompts, batch=5):
    """Mean sentence-token state at every layer, for each placement ('obs', 'input'), inside one case's prompt."""
    sysp, userp = prompts
    att = BE.ast.literal_eval(case["Attacker Tools"]) if isinstance(case["Attacker Tools"], str) else case["Attacker Tools"]
    names = [case["User Tool"]] + att
    desc = json.dumps([tools[t] for t in names], indent=True)
    out = {}
    for place in ("obs", "input"):
        acc = torch.zeros(nl + 1, lm.m.config.hidden_size)
        sents = SM.NEUTRAL2
        for i in range(0, len(sents), batch):
            seqs, segs = [], []
            for sent in sents[i:i + batch]:
                obs = sent if place == "obs" else NEUTRAL_OBS
                inp = case["User Instruction"] if place == "obs" else sent
                scratch = f"\n{case['Thought']}\nAction: {case['User Tool']}\nAction Input: {case['Tool Parameters']}\nObservation: {obs}\n"
                user = userp.format(available_tool_descriptions=desc, input=inp, available_tool_names=names,
                                    agent_scratchpad=scratch)
                ids, seg = BE.span_prompt(F, lm, [("system", sysp), ("user", user)], 1, sent)
                seqs.append(ids)
                segs.append(seg["C"])
            P.capture()
            _, pads = SM.forward(lm, seqs)
            P.clear()
            for l in range(1, nl + 1):
                h = P.cap[l]
                for b, ix in enumerate(segs):
                    acc[l] += h[b, [pads[b] + k for k in ix]].float().mean(0).cpu()
            P.cap = {}
        out[place] = acc / len(sents)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--data", required=True)
    ap.add_argument("--prompts", required=True)
    ap.add_argument("--batch", type=int, default=12)
    ap.add_argument("--max_new", type=int, default=160)
    ap.add_argument("--n_dev", type=int, default=60, help="tests only: fewer dev cases")
    ap.add_argument("--n_cfg", type=int, default=0, help="tests only: first N configurations")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    lm = fix_fmt(AB.BatchLM(a.model, 0.7))
    F = SM.Fmt(lm)
    nl = len(lm.m.model.layers)
    P = SP.Patcher(lm)
    LP.GEN = a.max_new
    t0 = time.time()
    tools, cases, prompts = BE.ia_load(a.data, json.load(open(a.prompts, encoding="utf-8")))
    dev = dev_cases(cases)[:a.n_dev]
    configs = CONFIGS[:a.n_cfg] if a.n_cfg else CONFIGS
    mu = LP.means(lm, F, P, nl)
    fm = fmt_means(lm, F, P, nl, tools, dev[0], prompts)
    print(f"{a.model}: {nl} layers, {len(dev)} dev cases, means {time.time() - t0:.0f} s", flush=True)
    maxpos = getattr(lm.m.config, "max_position_embeddings", None) or 10 ** 9
    jobs = BE.ia_jobs(F, lm, tools, dev, prompts, "none")
    order = sorted(range(len(jobs)), key=lambda j: len(jobs[j]["ids"]))
    res, norms = {}, {}
    for cfg in [None] + configs:
        rows = [None] * len(jobs)
        vec, layer = None, None
        if cfg is not None:
            nm, d, sc = cfg
            layer = max(1, min(nl, round(d * nl)))
            base = (fm["obs"][layer] - fm["input"][layer]) if nm == "obs-input" else LP.direction(nm, mu, layer)
            vec = float(sc) * base
            norms[f"{nm}|{d}|{sc}"] = round(float(vec.norm()), 3)
        live = []
        for j in order:
            if len(jobs[j]["ids"]) + a.max_new > maxpos:
                rows[j] = [jobs[j]["key"], "toolong", ""]
            else:
                live.append(j)
        for i in range(0, len(live), a.batch):
            chunk = [jobs[j] for j in live[i:i + a.batch]]
            steer = None if vec is None else (layer, [LP.tokset(x["seg"], "C") for x in chunk], vec)
            _, toks = LP.generate(lm, [x["ids"] for x in chunk], steer)
            for j, x, tk in zip(live[i:i + a.batch], chunk, toks):
                txt = LP.text_of(lm, tk)
                rows[j] = [x["key"], BE.ia_score(x, txt), txt[:300]]
        key = "none" if cfg is None else f"{cfg[0]}|{cfg[1]}|{cfg[2]}"
        res[key] = rows
        print(f"{key} done {time.time() - t0:.0f} s", flush=True)
    json.dump({"model": a.model, "n_layers": nl, "configs": [f"{n}|{d}|{s}" for n, d, s in configs], "norms": norms,
               "res": res}, open(os.path.join(a.out, "ia_pilot.json"), "w"))
    print("PILOT_DONE", flush=True)


if __name__ == "__main__":
    main()
