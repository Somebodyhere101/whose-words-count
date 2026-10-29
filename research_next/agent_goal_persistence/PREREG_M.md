# PREREG_M: do models obey what sounds least like themselves?

Written 2026-10-28, before any data on seeds 2000–2059. PREREG_J and PREREG_K were already analysed; PREREG_L was not.

Sealed in `PREREG_M.sha256` with:
- `code/m_analyze.py`;
- `cloud/rc23.sh`;
- `code/g_eval.py`, `code/agp_fast.py`, `code/agp_batch.py`.

## Background

**PREREG_J (MIXED) produced one unexpected regularity.**
- Under "Instruction based on a peer-reviewed study in Nature:", the identical goal text was obeyed *less* than under "… based on a post on a personal blog:".
- The Nature-framed text also sat higher on the role direction vR, toward the model's own (assistant) end.
- This held in 12 of 12 decided comparisons, across 6 models and both roles.
- It was the non-obvious prediction stated in PREREG_J before data, but it was not a gate there.

**Hypothesis.** Text that sounds like the model's own voice or knowledge is represented nearer the "own" end of vR and is obeyed less. Text attributed to another person is obeyed more. This fits the study's central finding that the agent's own turn carries the least authority.

**The competing account is credibility.** Control Illusion (Geng et al., AAAI 2026) found that expert or credible framing *raises* priority in conflicts between formatting constraints.

## Design

**Minimal pairs** (`agp_fast.FRAMESETS["m"]`). Each pair is one header line before the identical goal reminder, in a system turn and in a user turn. `s_` is the self-like header and `o_` the other-like one.

| Family | Pair | s_ (self-like) | o_ (other-like) |
|---|---|---|---|
| OWN | analysis | As your own earlier analysis concluded: | As a colleague's earlier analysis concluded: |
| OWN | plan | Your own plan for this fund: | Another manager's plan for this fund: |
| KNOW | fact | As is well established in climate science: | As one person on a forum insists: |
| KNOW | source | Based on a peer-reviewed study in Nature: | Based on a post on a personal blog: |

**What the two families separate:**
- **OWN** holds credibility fixed and varies only whose analysis or plan it is.
- **KNOW** pits self-likeness (established knowledge) against credibility: credibility predicts the opposite sign.
- The `source` pair repeats PREREG_J's expertise pair without the word "Instruction".

**Cells.** None, gF, uF, oF, plus 2 roles × 8 headers, so 20 per model.

**Probe.**
- **What is projected:** the goal text's own tokens onto unit vR. The probed tokens are byte-identical to the plain message's for all headers in all six tokenizers (checked).
- **Null:** 50 random unit directions seeded 2000 + layer.
- **Sampling:** framed cells share their role's plain sampling stream.

**Models** (layers as in PREREG_J), with seeds 2000–2059, n = 60, batch 20:

| Model | Layer | N_TEST |
|---|---|---|
| Qwen3-1.7B | 13 | 30 |
| SmolLM3-3B | 7 | 30 |
| Qwen3-4B | 17 | 30 |
| Qwen3-8B | 17 | 30 |
| OLMo-2-7B | 10 | 22 |
| Qwen3-14B | 18 | 30 |

**Why Granite is left out:** no header moved its behaviour in PREREG_J (0 of 6 high-vs-low pairs decided), so it cannot inform a behaviour-based test.

## Rules (`code/m_analyze.py`)

**Competence gate per model:** gF − none ≥ 0.10, p < 0.05.

**Measures.** Per model and family, per seed, averaged over the family's pairs and both roles:
- **D** = p_goal(o_) − p_goal(s_). D > 0 means self-like text is obeyed less.
- **P** = proj(s_) − proj(o_) on vR. P > 0 means self-like text sits toward "own".

**H1 (OWN) and H2 (KNOW), behaviour.** A sign-flip test of D per model, Holm across the models within each family.

| Verdict | Condition |
|---|---|
| SUPPORTED | ≥ 4 models with D > 0 and none with D < 0 (Holm p < 0.05) |
| REVERSED | ≥ 4 models with D < 0 and none with D > 0 |
| NOT_SUPPORTED | at most 1 model significant either way |
| MIXED | otherwise |

**H3, does the representation track behaviour?** For each (model, family) whose D is significant in either direction:
- **Agrees:** P has the sign of D with p < 0.05, and |t(P)| exceeds the 95th percentile of |t| over the 50 random directions.
- **Disagrees:** P has the opposite sign with p < 0.05.
- **Unresolved:** otherwise.

| H3 verdict | Condition |
|---|---|
| TRACKS | ≥ 4 such cells, and agree/cells ≥ 0.8 |
| DOES_NOT_TRACK | agree/cells < 0.5 |
| UNINFORMATIVE | fewer than 4 cells |
| MIXED | otherwise |

**Headline:** SELF_DISCOUNT if H1 is SUPPORTED and H3 TRACKS. Otherwise the three verdicts are reported as they stand.

**Reported, not gating:**
- per pair and role, D and P;
- the plain-role order;
- whether J's Nature < blog replicates (pair `source`).

**Analysis check.** `m_analyze.py` returns the intended verdict on five planted cases:

| Planted case | Result |
|---|---|
| Self-discount with tracking | SELF_DISCOUNT |
| Behaviour only, no axis | H3 DOES_NOT_TRACK |
| Nothing | NOT_SUPPORTED, H3 UNINFORMATIVE |
| OWN reversed | H1 REVERSED |
| Anti-axis | H3 DOES_NOT_TRACK |

## Readings fixed now

- **SELF_DISCOUNT.** Framing an instruction as the model's own analysis, plan or established knowledge lowers obedience, relative to attributing the same words to another person. The role direction files such text nearer the model's own voice.
  - So "own" carries less authority not only as a chat role but as a framing: models obey what sounds least like themselves.
  - If KNOW is also SUPPORTED, credibility does not explain the "Nature < blog" result.
- **H1 SUPPORTED, H3 not TRACKS.** The behavioural self-discount is real, but our role direction does not carry it.
- **H1 NOT_SUPPORTED, H2 SUPPORTED.** The effect is about knowledge or evidence framing, not about the self. A "weigh it, don't obey it" account then fits better.
- **REVERSED.** Self-framed goals are obeyed more, the human-like pattern. This would rule out the "obey the least self-like" reading.

## Infrastructure

The run shares the network volume `rt9jwj49za`:
- **Folder:** `/workspace/agpm`.
- **Run-23 markers:** `run23.log`, `PACKED23`, `FETCHED23` and `results23.tgz`.
- **Self-stop:** `cloud/ss23.sh`, 6 minutes after packing.
- **Download fix (lesson L12):** Hugging Face xet downloads are disabled, and the caches are cleared after each model.

## Cost and time

Anchor E26, computed from measured per-cell times (PREREG_L log, PREREG_I and the pilot):
- **Arithmetic:** 2.4 boot + 20 cells × 297.5 s/60 + 8.5 download + 1.7 fetch = 111.8 min.
- Calibrated: 94.5 min. About $2.8–3.3 at $1.79/h.
