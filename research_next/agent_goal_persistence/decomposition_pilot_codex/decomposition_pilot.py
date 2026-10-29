"""Small, explicitly exploratory source-axis decomposition pilot; see decomposition_plan.txt."""
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import random
import re
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "scoring_deps"))
from research_bridge import STUDY
sys.path.insert(0, str(STUDY / "code"))
import torch
import agp_batch as AB
from ci_eval import load_rows, prompts
from ci_score import met, degenerate, words
import nltk

OUT = HERE / "decomposition_pilot"
OUT.mkdir(exist_ok=True)
MODEL = "Qwen/Qwen3-1.7B"
LAYER = 13
CONDS = ("plain", "emph", "oldR2", "user2", "user4", "orth2", "pair2", "random2")
MAX_NEW = 512
DEADLINE = dt.datetime(2026, 10, 28, 15, tzinfo=dt.timezone(dt.timedelta(hours=4))).timestamp()


def check_stop():
    deadline = min(DEADLINE, float(os.environ.get("GPU_LOCK_DEADLINE", DEADLINE)))
    if time.time() > deadline:
        raise TimeoutError("Research/GPU deadline reached; partial results saved")
    r = subprocess.run(["tasklist", "/FI", "IMAGENAME eq RobloxPlayerBeta.exe", "/FO", "CSV", "/NH"], capture_output=True)
    if b"RobloxPlayerBeta.exe" in r.stdout:
        raise InterruptedError("Roblox started; local GPU pilot paused")


def hashfile(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def extract(lm):
    cache = OUT / "directions.pt"
    if cache.exists():
        return torch.load(cache, map_location="cpu", weights_only=True)
    subjects = ("The blue folder", "The wooden chair", "The garden gate", "The old clock", "The green bicycle", "The kitchen window")
    endings = ("was moved yesterday.", "is beside the wall.", "looks different today.", "needs a small repair.", "was mentioned in a letter.", "has a simple design.")
    sentences = [f"{s} {e}" for s in subjects for e in endings]
    H = {r: [] for r in ("assistant", "system", "user")}
    pre = lm.enc("system", "You are a helpful assistant.", first=True) + lm.enc("user", "Please read the next sentence.")
    for j, x in enumerate(sentences):
        check_stop()
        token_spans = []
        for role in H:
            # The current model is ChatML; verify rather than silently applying this to another family.
            assert lm.fmt is None
            text = f"<|im_start|>{role}\n{x}<|im_end|>\n"
            start = text.index(x)
            enc = lm.tok(text, add_special_tokens=False, return_offsets_mapping=True)
            ix = [i for i, (a, b) in enumerate(enc.offset_mapping) if a >= start and b <= start + len(x) and b > a]
            tokids = [enc.input_ids[i] for i in ix]
            positions = [len(pre) + i for i in ix]
            token_spans.append((tokids, positions))
            ids = torch.tensor([pre + enc.input_ids], device=AB.DEV)
            with torch.no_grad():
                hs = lm.m(input_ids=ids, output_hidden_states=True, use_cache=False).hidden_states
                H[role].append(hs[LAYER][0, positions].float().mean(0).cpu())
            del hs, ids
        assert token_spans[0] == token_spans[1] == token_spans[2], (x, token_spans)
        if j % 6 == 5:
            print(f"EXTRACT {j + 1}/{len(sentences)}", flush=True)
    mu = {r: torch.stack(v).mean(0) for r, v in H.items()}
    R = mu["assistant"] - (mu["system"] + mu["user"]) / 2
    U = mu["user"] - mu["system"]
    orth = U - (U @ R) / (R @ R) * R
    gen = torch.Generator().manual_seed(271828)
    rnd = torch.randn(R.shape, generator=gen)
    dirs = {"R": R, "U": U / U.norm() * R.norm(), "O": orth / orth.norm() * R.norm(), "rand": rnd / rnd.norm() * R.norm()}
    torch.save(dirs, cache)
    (OUT / "extraction.json").write_text(json.dumps({
        "model": MODEL, "layer": LAYER, "sentences": sentences, "content_token_and_position_checks": len(sentences),
        "norm_R": R.norm().item(), "norm_U_raw": U.norm().item(), "norm_orth_raw": orth.norm().item(),
        "cos_R_U": torch.nn.functional.cosine_similarity(R, U, dim=0).item(),
        "max_norm_mismatch": max(abs(v.norm().item() - R.norm().item()) for v in dirs.values())}, indent=2))
    return dirs


class SignedSteer:
    def __init__(self, lm, vector):
        self.vector = vector.to(AB.DEV, lm.m.dtype)
        self.layer = lm.m.model.layers[LAYER - 1]
        self.mask = None

    def __enter__(self):
        def apply(mod, inp, out):
            h = out[0] if isinstance(out, tuple) else out
            if self.mask is None or h.shape[1] != self.mask.shape[1]:
                return out
            h = h + self.mask.unsqueeze(-1).to(h.dtype) * self.vector
            return (h,) + tuple(out[1:]) if isinstance(out, tuple) else h
        self.handle = self.layer.register_forward_hook(apply)
        return self

    def __exit__(self, *args):
        self.handle.remove()


def utility_rows():
    cases = [
        ("What is 17 plus 26?", "43"), ("What is 9 times 8?", "72"),
        ("What is 91 minus 37?", "54"), ("What is 144 divided by 12?", "12"),
        ("What is the capital of France?", "paris"), ("What is the capital of Japan?", "tokyo"),
        ("Repeat this code exactly: ZEBRA-731", "ZEBRA-731"), ("Repeat this code exactly: KITE-482", "KITE-482")]
    return [{"task": 1000 + i, "order": 0, "conflict": "utility", "base_instruction": task,
             "constraint1": "Answer the user's question accurately in English.", "constraint2": "",
             "kwargs": [{"language": "en"}, {}], "expected": expected} for i, (task, expected) in enumerate(cases)]


def run(lm, dirs, cond, rows):
    dest = OUT / (cond + ".json")
    if dest.exists():
        return
    vector = {"oldR2": -2 * dirs["R"], "user2": 2 * dirs["U"], "user4": 4 * dirs["U"],
              "orth2": 2 * dirs["O"], "pair2": 2 * dirs["U"], "random2": 2 * dirs["rand"]}.get(cond)
    hook = SignedSteer(lm, vector) if vector is not None else None
    if hook:
        hook.__enter__()
    recs, t0 = [], time.time()
    try:
        for i in range(0, len(rows), 2):
            check_stop()
            chunk = rows[i:i + 2]
            seqs, nsys, nuser = [], [], []
            for r in chunk:
                s, u = prompts("emph" if cond == "emph" else "plain", r)
                si, ui = lm.enc("system", s, first=True), lm.enc("user", u)
                seqs.append(si + ui + lm.header())
                nsys.append(len(si)); nuser.append(len(ui))
            T = max(map(len, seqs))
            ids = torch.full((len(chunk), T), lm.pad, dtype=torch.long, device=AB.DEV)
            am = torch.zeros_like(ids)
            mask = torch.zeros_like(ids, dtype=torch.float32)
            for b, seq in enumerate(seqs):
                pos = T - len(seq)
                ids[b, pos:] = torch.tensor(seq, device=AB.DEV)
                am[b, pos:] = 1
                mask[b, pos:pos + nsys[b]] = 1
                if cond in ("pair2", "random2"):
                    mask[b, pos + nsys[b]:pos + nsys[b] + nuser[b]] = -1
            if hook:
                hook.mask = mask
            with torch.no_grad():
                out = lm.m.generate(input_ids=ids, attention_mask=am, max_new_tokens=MAX_NEW,
                                    do_sample=False, pad_token_id=lm.pad)
            for b, r in enumerate(chunk):
                new = out[b, T:].tolist()
                while new and new[-1] == lm.pad:
                    new.pop()
                answer = lm.tok.decode(new, skip_special_tokens=True).strip()
                row = {**r, "response": answer, "n_new": len(new), "words": len(words(answer)), "degenerate": degenerate(answer)}
                if r["conflict"] == "utility":
                    row["utility_ok"] = bool(re.search(r"(?<!\w)" + re.escape(r["expected"]) + r"(?!\w)", answer, re.I))
                else:
                    row["met1"] = bool(met(answer, r["constraint1"], r["kwargs"][0]))
                    row["met2"] = bool(met(answer, r["constraint2"], r["kwargs"][1]))
                recs.append(row)
            (OUT / (cond + ".partial.json")).write_text(json.dumps({"records": recs}))
            print(f"RUN {cond} {min(i + 2, len(rows))}/{len(rows)} {time.time() - t0:.1f}s", flush=True)
    finally:
        if hook:
            hook.__exit__()
    dest.write_text(json.dumps({"model": MODEL, "condition": cond, "layer": LAYER, "records": recs,
                               "seconds": time.time() - t0}, indent=1))


if __name__ == "__main__":
    check_stop()
    nltk.data.path.insert(0, str(HERE / "nltk_data"))
    nltk.download("punkt_tab", download_dir=str(HERE / "nltk_data"), quiet=True)
    paths = [str(STUDY / "data/ci" / n) for n in ("conflicting_instructions.jsonl", "conflicting_instructions_reversed.jsonl")]
    rows = load_rows(paths, "65-66") + utility_rows()
    assert len(rows) == 32
    (OUT / "manifest.json").write_text(json.dumps({"model": MODEL, "conditions": CONDS, "tasks": "65-66", "layer": LAYER,
        "plan_sha256": hashfile(HERE / "decomposition_plan.txt"), "script_sha256": hashfile(Path(__file__)),
        "dependency_sha256": {n: hashfile(STUDY / "code" / n) for n in ("agp_batch.py", "ci_eval.py", "ci_score.py")}}, indent=2))
    lm = AB.BatchLM(MODEL, .7)
    dirs = extract(lm)
    print("EXTRACTION_DONE", flush=True)
    for condition in CONDS:
        run(lm, dirs, condition, rows)
    print("DECOMPOSITION_PILOT_DONE", flush=True)
