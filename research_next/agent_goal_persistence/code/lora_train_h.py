"""lora_train.py copied for REVPILOT (lora_train.py itself stays as sealed for PREREG_E/F): adds --data hier, which
trains on hier_data.py conversations (arms sys / usr: which role wins a system-user conflict).

Original description: LoRA fine-tune for the commitment-binding test: train on sft_data conversations of one arm (own or given).

Conversations are encoded exactly as the evaluation instrument encodes turns (agp_batch wrappers, native template):
context turns with enc(role, text); each target decision turn as header() + 'CHOICE: CODE' + close, with the loss on
'CHOICE: CODE' + close only. Reminder turns are never trained on, so arm 'own' learns from goal text it did not have
to write.

Usage: python lora_train.py --model Qwen/Qwen3-1.7B --arm own --n 240 --out ../lora/own_q17
"""
import argparse
import json
import os
import random
import time

import torch
from peft import LoraConfig, get_peft_model
from transformers import AutoModelForCausalLM

import ctx_positions as CP
import hier_data
import sft_data

TARGETS = ["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"]


def encode(lm, conv, max_len):
    ids, labels = [], []
    first = True
    for role, text, tgt in conv:
        if tgt:
            h = lm.header()
            body = lm.tok(text + lm.close_str, add_special_tokens=False).input_ids
            ids += h + body
            labels += [-100] * len(h) + body
        else:
            t = lm.enc(role, text, first=first and role == "system")
            ids += t
            labels += [-100] * len(t)
        first = False
    return ids[:max_len], labels[:max_len]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--arm", required=True, choices=["own", "given", "sys", "usr"])
    ap.add_argument("--data", default="binding", choices=["binding", "hier"], help="hier: hier_data.py (arms sys/usr)")
    ap.add_argument("--n", type=int, default=240)
    ap.add_argument("--seed0", type=int, default=0)
    ap.add_argument("--epochs", type=int, default=1)
    ap.add_argument("--lr", type=float, default=1e-4)
    ap.add_argument("--rank", type=int, default=16)
    ap.add_argument("--accum", type=int, default=4)
    ap.add_argument("--max_len", type=int, default=2048)
    ap.add_argument("--balanced", action="store_true", help="half the rounds aligned (pressure agrees with the goal)")
    ap.add_argument("--nopress", action="store_true", help="hier data without pressure lines (REVPILOT 2)")
    ap.add_argument("--posbal", action="store_true", help="hier data with system-first and user-first conflicts (REVPILOT 3)")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    torch.manual_seed(0)
    lm = CP.TokOnly(a.model)
    convs = (hier_data.make(a.arm, a.n, a.seed0, a.nopress, a.posbal) if a.data == "hier"
             else sft_data.make(a.arm, a.n, a.seed0, a.balanced))
    data = [encode(lm, c, a.max_len) for c in convs]
    data = [d for d in data if any(t != -100 for t in d[1])]   # a truncated example without targets would give a NaN loss
    random.Random(0).shuffle(data)
    dev = os.environ.get("AGP_DEVICE", "cuda")
    model = AutoModelForCausalLM.from_pretrained(a.model, dtype=torch.bfloat16 if dev == "cuda" else torch.float32).to(dev)
    model.gradient_checkpointing_enable()
    model.enable_input_require_grads()
    model = get_peft_model(model, LoraConfig(r=a.rank, lora_alpha=2 * a.rank, lora_dropout=0.05,
                                             target_modules=TARGETS, task_type="CAUSAL_LM"))
    opt = torch.optim.AdamW([p for p in model.parameters() if p.requires_grad], lr=a.lr, weight_decay=0.0)
    model.train()
    log, t0, step = [], time.time(), 0
    for ep in range(a.epochs):
        for i, (ids, lab) in enumerate(data):
            x = torch.tensor([ids], device=dev)
            y = torch.tensor([lab], device=dev)
            loss = model(input_ids=x, labels=y).loss / a.accum
            loss.backward()
            if (i + 1) % a.accum == 0 or i == len(data) - 1:
                opt.step()
                opt.zero_grad()
                step += 1
            log.append(round(float(loss) * a.accum, 4))
            if i % 40 == 0:
                print(f"ep {ep} ex {i}/{len(data)} loss {log[-1]:.4f} {time.time() - t0:.0f}s", flush=True)
    os.makedirs(a.out, exist_ok=True)
    model.save_pretrained(a.out)
    json.dump({"model": a.model, "arm": a.arm, "n": a.n, "seed0": a.seed0, "epochs": a.epochs, "lr": a.lr,
               "rank": a.rank, "steps": step, "tokens": sum(len(d[0]) for d in data),
               "target_tokens": sum(sum(1 for t in d[1] if t != -100) for d in data),
               "loss_first20": sum(log[:20]) / len(log[:20]), "loss_last20": sum(log[-20:]) / len(log[-20:]),
               "sec": round(time.time() - t0, 1), "losses": log}, open(os.path.join(a.out, "train_log.json"), "w"))
    print("saved", a.out, "loss first/last 20:", round(sum(log[:20]) / len(log[:20]), 4), round(sum(log[-20:]) / len(log[-20:]), 4))


if __name__ == "__main__":
    main()
