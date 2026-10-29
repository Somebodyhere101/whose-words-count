# PREREG_D: which post-training stage installs the own-text discount (OLMo-2 lineage)

Written 2026-10-27, before any SFT or DPO data exists. Sealed in `PREREG_D.sha256` with:
- `code/d_analyze.py`;
- `cloud/rc9.sh`;
- `code/agp_fast.py`, `code/agp_batch.py`, `code/chat_fmt.py`;
- `code/src_probe.py`.

## Background

- **Origin.** The design comes from `PLAN_LINEAGE_FABLE.md` (a fresh Fable 5.1 agent), adapted after two pilots (`PLAN_7DAY.md`, 2026-10-27 15:08 and 15:18).
- **The base model cannot be tested.** OLMo-2-7B base does not respond to a goal reminder in a plain transcript (none − system +0.005, n.s.).
- **The plain format does not carry the gap.** In a plain transcript, OLMo-2-7B-Instruct shows no own-vs-given gap (+0.013, n.s.). In its native template the gap is +0.080 (p 0.0003).
- **So the stage question is asked where the gap exists:** the native template, across the three post-training checkpoints. All of them share a byte-identical chat template (md5 70bb224ce1).
- **Known neighbours:**
  - OLMo-3 sycophancy splits between SFT and DPO (Xu & Daneshjou, NeurIPS 2026), and DPO raises sycophantic agreement (arXiv 2608.31079);
  - Leong 2026 (arXiv 2608.28502) probes provenance in open models.
  - None measures goal adherence by role across stages.

## Design

- **Checkpoints:** allenai/OLMo-2-1124-7B-{SFT, DPO, Instruct} and allenai/OLMo-2-1124-13B-{SFT, DPO, Instruct}. Instruct is the final model, after RLVR.
- **Format and instrument:** native chat template, using the fast instrument `code/agp_fast.py`:
  - N_TEST 22, so every readout fits the 4,096-token window (checked from each step's recorded `ctx`);
  - temperature 0.7;
  - batch 20 for 7B, 10 for 13B (batching changes only floating-point noise).
- **Cells,** with the fixed goal text, reinserted every 3 steps:

  | Cell | Reminder |
  |---|---|
  | 1 | none |
  | gF | as a system turn |
  | oF | as the agent's own (assistant) turn |
  | uF | as a user turn |

- **Seeds:** 600–679 (n = 80), fresh: never used before.
- **Exploratory:** the 240-sentence role probe (`code/src_probe.py`) on the three 7B checkpoints.

## Measures and rules (coded in `code/d_analyze.py`)

**Per checkpoint:**
- **Competence gate:** p_hi(1) − p_hi(gF) ≥ 0.05 with sign-flip p < 0.01, and mean ticker mass ≥ 0.3.
- **G_s** = mean over seeds of p_hi(oF) − p_hi(gF), with its sign-flip p (two-sided, 20,000 permutations).

**Per size:**
- **Arrival stage A:** the first stage that passes the gate with G_s > 0 at p < 0.01 and G_s ≥ 0.5 × G_Instruct.
- **Amplification at stage s:** a paired sign-flip test on the per-seed difference gap_s − gap_{s−1} gives a mean > 0 at p < 0.01. The same seeds give the same worlds across stages.

**Verdicts per size:**

| Verdict | Condition |
|---|---|
| H-SFT | A = SFT, and no amplification at DPO or at Instruct. Supervised chat training installs the discount. |
| H-pref | A = DPO or Instruct; or A = SFT with amplification at DPO or Instruct and G_Instruct ≥ 2 × G_SFT. Preference or RL stages install most of it. |
| MIXED | A = SFT, with amplification, but G_Instruct < 2 × G_SFT. |
| NO GAP | G_Instruct is not > 0 at p < 0.01, so this size cannot locate the stage. |
| UNINTERPRETABLE | Some stage fails the competence gate. |
| INVALID | A readout exceeds 4,096 tokens. |

**Combined claim:** only when 7B and 13B give the same verdict. Otherwise AMBIGUOUS.

## Predictions stated now

- **The plan's primary hypothesis is H-pref,** with P(clean positive) 0.30 in the plan.
- **My own prior leans to H-SFT or MIXED.** The pilot shows the gap is tied to the chat template's role tokens, which SFT introduces. A prior is not a test; the rules above decide.
- **If H-SFT:**
  - the discount comes from supervised chat data, where system turns carry instructions and assistant turns carry responses;
  - the fix belongs in SFT data;
  - the sycophancy link is dropped.
- **If H-pref:** preference optimisation installs the self-discount. The cheapest fix is preference pairs that reward honouring self-commitments.

## Exploratory, not gated

- **User gap:** uF − gF.
- **Decomposition:** own − none and given − none.
- **Logit-scale gap.**
- **7B probes:** the best transfer layer, and cos(vR_s, vR_Instruct) at layers 10 and 15. Layer 10 is where PREREG_C confirmed the causal effect in OLMo-2-7B-Instruct.

## Cost and time

Computed from measured rates. A100 SXM 80 GB, $1.79/h.

**Inputs:**

| Input | Source | Value |
|---|---|---|
| boot to first result | measured | 2.4 min |
| download and load, per 16.3 GB | measured | 1.75 min |
| 7B batch of 20 seeds, N_TEST 22 | measured (7B pilot) | 14.6 s |
| OLMo-7B probe | measured | 3.2 min |
| fetch and stop | measured | 1.7 min |
| 13B batch of 10 | **guess**, scaled by parameter count | 14.6 × 13.7/7.3 = 27.4 s |

**Computation:**
- 7B: 3 stages × 4 cells × 4 batches × 14.6 s = 11.7 min.
- 13B: 3 × 4 × 8 × 27.4 s = 43.8 min.
- Probes: 3 × 3.2 = 9.6 min.
- Downloads:
  - 7B: 2 × 1.6 = 3.2 min (the first is inside boot);
  - 13B: 3 × 1.75 × 27.4/16.3 = 8.8 min.
- Loads: 2.8 min.
- Fetch: 1.7 min.

**Total about 84 min, so 84/60 × $1.79 = $2.51.** Past estimates have come in at 0.80×.
