# PREREG_W: the source map at scale (PLAN_BIGGER Phase 2)

Written 2026-10-28, after PREREG_T and before any PREREG_W data. Sealed in `PREREG_W.sha256` together with:
- `code/src_patch_w.py`, `code/s_beh.py`, `code/w_analyze.py`;
- `cloud/rc29*.sh`, `cloud/ss29*.sh`;
- the helpers `code/src_patch.py`, `code/src_monitor.py`, `code/t_analyze.py`, `code/s_analyze.py`, `code/agp_batch.py`, `code/agp_b.py`, `code/chat_fmt.py`.

## Question

Does the PREREG_T map hold beyond the four models it was found in, across new families and up to 32B? The map says:
- behaviours read "who said this" at different depths, with obeying read later than attributing;
- the role markers are the main carrier;
- obeying passes through a content phase on the statement's own tokens, and attributing does not.

PREREG_S found that obey and believe rank sources differently. Does that also hold at scale?

## Models

Ten new models, none gated. With PREREG_T's four, that makes 7 families from 0.6B to 32B.

| Family | Models (layers) |
|---|---|
| Qwen3 | 0.6B (28), 4B (36), 14B (40), 32B (64) |
| OLMo-2 | 1124-13B-Instruct (40), 0325-32B-Instruct (64) |
| Phi | phi-4, 14.7B (40) |
| Granite | granite-3.3-8b-instruct (40) |
| Falcon | Falcon3-10B-Instruct (40) |
| Yi | Yi-1.5-9B-Chat (48) |

**Dropped before data:** gpt-oss-20b. Its harmony format renders our system turns as developer turns, and replies start with an analysis channel, so the first-token readout does not apply without a new format layer. This is reported as a limit.

## Design

**Map (`code/src_patch_w.py`).** The PREREG_T design and code paths, with these settings:
- fresh items: seed 2600, 48 facts and 48 instructions;
- pairs own→usr and sys→usr, both orders;
- position sets M, C and D at every layer; ALL at layers 1, round(n/2) and n.

There are two additions:
- **Stride.** The 32B models patch every 2nd layer (layers 1, 3, 5, …, plus the check layers). This halves their cost. Stride 1 is exactly PREREG_T.
- **Chat format.** Templates that contain `<|im_sep|>` (Phi-4) use the role wrappers taken from the model's own template, because BatchLM's plain-ChatML shortcut would get them wrong. Everything else follows BatchLM unchanged, so nothing changes for PREREG_T's models.
  - Yi-1.5's HF template drops system turns and appends an assistant header after every user turn. Yi therefore gets plain ChatML, its trained format. This was found in the tokenizer check before sealing.

**Fragmentation (`code/s_beh.py`).** The PREREG_S behaviour stage alone, with fresh items (seed 2650, n 60): obey, believe and attribute over the five sources.

## Rules (`code/w_analyze.py`)

Per model, PREREG_T's rules (H1, H2, handoff, carrier, sanity) are applied unchanged. For strided sweeps they work on the swept layers.

**Check before sealing:** run on PREREG_T's own data, `w_analyze.py` reproduces every sealed PREREG_T verdict, handoff, carrier and comparison (0 mismatches).

**Hypotheses over the 10 new models** (a majority is n // 2 + 1 of the models the rule applies to):

| | Hypothesis | Rule | PREREG_T data under the same rule (post hoc, for reference only) |
|---|---|---|---|
| W1 | Dissociation | PREREG_T's H2 is DISSOCIATED in a majority | 4/4 |
| W2 | Markers carry | at least 60% of informative, sane curves (obey, believe, attribute; both pairs) have carrier MARKER | 14/16 |
| W3 | Obeying is read later | OBEY_LATER in a majority of the models that have an informative obey–attribute pair. OBEY_LATER means the obey handoff is later than the attribute handoff, with the bootstrap 95% CI of the difference above 0, in some pair, and below 0 in none | 3/3 |
| W4 | No single tag | under the PREREG_S behaviour rule, a majority of informative verdicts are not UNIFIED. The number FRAGMENTED is reported | not run in PREREG_T |
| W5 | Content phase | in a majority of the models with an informative obey curve, some obey curve reaches max T_C ≥ 0.5; and in a majority of the models with an informative attribute curve, every attribute curve stays below 0.2 | 3/3 and 3/4 |

**Reported, not gating:**
- the relative obey lag, (h_obey − h_attribute) / n_layers, against log size within the Qwen3 ladder (6 sizes, including PREREG_T's 1.7B and 8B) and the OLMo-2 ladder (7/13/32B), with a Spearman correlation;
- the relative depth of the obey content peak, against the 0.45–0.75 band used in PREREG_U;
- every per-model verdict.

## Readings fixed now

- **W1–W3 supported:** the map is general across 7 families and up to 32B. It becomes a property of chat models, not of four models.
- **W5 supported:** obeying, unlike attributing, routes through the statement's own tokens at mid-to-late depth. That is where a selective defence should act (Phase 1).
- **A rule not supported:** the claim narrows to where it held, and we say so. If the dissociation fails from 14B up, the paper says the map is a small-model property.

## Limits fixed now

- The first-token readout is used, as in PREREG_T. Phase 0's audit (PILOT_V0) decides whether it is valid. If the audit says GENERATION_NEEDED, these results are reported with that caveat, and a generation re-run of the map is planned.
- The two 32B models have 2-layer resolution.
- gpt-oss is excluded (see above).

## Speed and cost

The run is split across 3 pods by the measured rate (PREREG_T: 3.40 s per B-param × layer swept on an A100; the H100 NVL is faster):
- **Pod A:** Qwen3-32B, Qwen3-0.6B, Qwen3-4B.
- **Pod B:** OLMo-2-32B, OLMo-2-13B.
- **Pod C:** Qwen3-14B, phi-4, Granite-8B, Falcon3-10B, Yi-1.5-9B.

Each pod downloads its next model while the current one runs.

**Estimate.** 5,131 B·layers × 3.40 s ≈ 291 min of A100 compute, plus the behaviour runs (about 20 min) and downloads (about 260 GB). That is about $10 in all.

## Tests before sealing (done 2026-10-28, no PREREG_W data)

- **Regression on PREREG_T's data:** `w_analyze.py` reproduces every sealed PREREG_T verdict, informativeness flag, handoff, carrier, A_M, A_C, sanity flag and comparison (0 mismatches).
- **Regression on PREREG_S's data:** the W4 rule reproduces PREREG_S's behaviour verdicts, Kendall τ, mean attribution and authority tables (0 mismatches).
- **Tokenizers of all 10 models**, 64 prompts each:
  - in every prompt, the statement's C segment decodes to the statement;
  - donor and recipient C segments have equal length;
  - the OLMo-2 and Yi own→usr prompts differ by one token in the role marker, handled by segment alignment as in PREREG_T.
  - Yi-1.5's template problem was found here (see Design).
- **GPU (Qwen3-0.6B, seed 2600, n 2, on the Phase 0 pod):**
  - `src_patch_w.py` at stride 1 equals `src_patch.py` exactly;
  - stride 2 equals stride 1 on all 16 swept layers;
  - the ALL patch reproduces the donor (maximum difference 0.0);
  - `s_beh.py` and `w_analyze.py` run.
