# Candidate next experiment: where the self-discount is installed (OLMo-2 lineage)

**Source.** On 2026-10-27, at the user's request, a fresh Fable 5.1 agent was asked for the single experiment with the best odds of a breakthrough. It was given only the brief in `C:/Users/caabm/Downloads/one_experiment_prompt.md`: no conversation history and no file access, with at most 6 web searches. Below is a summary of its answer, then Claude's verification notes. This plan is **not adopted**: it is waiting for the user's decision.

## The plan, in brief

- **Bottom line from the agent.** "Nothing you can run in 22 A100-hours on open models up to 32B has a real chance of a paradigm shift": 1–2% for any design. This one is chosen for the highest expected information. A positive would be "a strong paper … not a paradigm shift."
- **Claim.** In OLMo-2, which had no hierarchy or system-prompt training, the own-vs-given authority gap is absent in the pretrained model. Ordinary post-training installs it, with preference optimisation (DPO/RLVR) contributing more of it than SFT.
- **Odds:**
  - P(clean positive) 0.30, with a positive defined as DPO/RLVR adding more than SFT, at both 7B and 13B;
  - P(informative negative) 0.42;
  - P(ambiguous) 0.28.
- **Rejected alternatives**, with the agent's P(clean positive):
  - a four-channel authority ladder, 0.40;
  - chain-of-thought authority, 0.20;
  - a controlled LoRA mini-training, 0.35. The agent calls this the natural follow-up.
- **Design:**
  - **Models:** OLMo-2-1124-7B and 13B, each at base, SFT, DPO and Instruct. Secondary: the same stages of OLMo-2-0425-1B and OLMo-2-0325-32B, plus Qwen3-8B-Base vs Qwen3-8B.
  - **Cells:** the reminder is placed as system / user / own / none.
  - **Format:** plain-text transcript labels (SYSTEM:/USER:/ASSISTANT:) at every stage, so base models can be compared. The readout is taken at "ASSISTANT: ALLOCATE:" over the ticker set. Post-SFT stages are also run in the native template.
- **Controls:**
  - a competence gate per stage: given − none ≥ 0.05 at p < 0.01, and ticker mass ≥ 0.3;
  - the gap decomposed into own − none and given − none;
  - a logit-scale secondary measure;
  - random-direction controls for steering;
  - agreement between native and plain-text runs.
- **Outcomes:**
  - G_s = own − given per stage;
  - vR probe accuracy and cos(vR_s, vR_Instruct);
  - causal coupling (±2·vR_s against random) at the best OLMo layer.
- **Decision rules:**
  - arrival stage = the first stage that passes the gate with G_s > 0 (p < 0.01) and G_s ≥ 0.5·G_Instruct;
  - H-pref (preference stage) vs H-SFT vs H-pre (pretraining).
- **Sample:** 80 seeds per cell. The SD of the paired gap is at most 0.07 (Qwen3-14B), so the SE is 0.008 and a between-stage difference of 0.04 is about 3.6 SE.
- **Compute:** about 11.3 GPU-hours, about $20. Without the 32B lineage it is 9.5 h.
- **First step (free):** a laptop pilot on OLMo-2-1B base vs 1B-Instruct, 20 seeds × own/given/none, testing three things:
  - (a) ticker mass ≥ 0.3 in base;
  - (b) the competence gate in base;
  - (c) the plain-text gap has the same sign as the native one.
  - If 1B is too weak, run 7B base vs Instruct on an A100 (about 0.3 GPU-h).
- **Outside validation:**
  - publish the sealed prereg plus a one-command script, so a 7B lineage rerun costs under $3;
  - have an independent session run the fresh-seed confirmation;
  - ask the Ai2 authors about self-commitment data in the SFT and DPO mixes;
  - replicate in the OLMo-3 lineage.

## Verification notes (Claude, 2026-10-27)

- **Confirmed.** The OLMo-2-1124-7B-Instruct model card says "The model has not been trained with a specific system prompt in mind." The stages are public: `-SFT`, `-DPO`, and `-Instruct` (the final model, after RLVR).
- **Overstated.**
  - arXiv 2608.25390 exists: Labunets, "Refusal geometry reflects refusal training…", Aug/Sep 2026. Its abstract covers one model (OLMo-2-0425-1B-Instruct).
  - The abstract does **not** describe the base → SFT → DPO → RLVR stage profile that the plan attributes to it.
  - The plan's other prior-art entries (the OLMo-3 sycophancy stages at NeurIPS 2026, arXiv 2602.01002, 2609.03887, 2609.00608, the MATS and LessWrong posts, a blog) are **unverified leads**. Read them before sealing.
- **Missed constraint.**
  - All OLMo-2 models have a 4,096-token window. Episodes must be shortened (N_TEST 22, as in PREREG_C), and every readout must be checked with `max_ctx`. The brief did not mention this.
  - Plain-text labels add tokens, so recompute the safe N_TEST with `code/ctx_positions.py` before sealing.
- **Estimates.** The speed factors for 13B (×1.8) and 32B (×3.5) are scaled guesses. The 32B factor is consistent with our measured 95 s vs about 27 s per 20-seed condition.
- **Fit to G1.** It adds the developmental origin of the mechanism, with every stage open, so outside validation is easy. It does **not** supply the "capability or defence that beats baselines". That would be the follow-up: preference data that rewards honouring self-commitments, or the goal register.
