# Numbers recheck: PAPER_DRAFT.md (Draft 6)

Independent recheck, 2026-10-28. The scope is the Abstract, §2–§10, "Fix-test pilot: NO-GO" and "Neutral-role decomposition diagnostic: NO-GO". §11, §12 and the Data section were only spot-checked (last group). `CONSOLIDATED_RESULTS.md` and `PLAN_7DAY.md` were used only to locate files and run names, never as evidence.

**Paths.** `WS/` = `research_next/agent_goal_persistence/`. `AR/` = `C:/Users/caabm/Documents/agp_res/` (short-path copies of the cloud outputs).

**Method.**
- Every sealed analysis script was first checked against its `PREREG*.sha256` hash (all OK).
- Each script was then re-run on CPU (`CUDA_VISIBLE_DEVICES=""`, `AGP_DEVICE=cpu`) on the stored outputs, from a scratch copy, so nothing was written into `WS/`. The output was diffed against the stored result JSON.
- Claims with no stored statistic were recomputed from the raw per-run files, using the sealed `signflip` functions.

**Status legend.**
- **MATCH:** the primary value, rounded half-up to the paper's displayed precision, equals the paper's value.
- **ROUNDING:** off by one unit in the last displayed digit, which the rounding of an already-rounded stored value can explain.
- **MISMATCH:** the primary data contradict the paper. Tagged [numeric], or [quantifier] for an "every / all / near zero / most" statement that the data do not support.
- **UNVERIFIABLE:** no primary file is available locally.

## Summary

**Counts, requested scope (168 numeric claims).**

| Status | Count |
|---|---|
| MATCH | 154 |
| ROUNDING | 2 |
| MISMATCH | 11 (3 numeric, 8 quantifier or wording) |
| UNVERIFIABLE | 1 |

The spot checks outside scope add 1 MISMATCH [quantifier], 1 MATCH and 1 UNVERIFIABLE.

**Every sealed re-run reproduced its stored output.** C, D, E2, E3 (PREREG_E), E4, F, G, H, J, K, L and M are byte-identical. I differs only by a trailing newline. The main run, run B, stage 1 and the fix pilot also reproduce (see the re-run log). No gate verdict changes.

### MISMATCH list, with exact evidence

1. **§4 heading "(FAIL, 9 models)" [numeric].**
   - 10 models were probed, and the §4 body itself names all 10: Qwen3-1.7B plus SmolLM2, EuroLLM, Qwen3-4B, 8B, 14B, 32B, SmolLM3, OLMo-2-7B and Granite. All 10 have a `probe_results.json` (`WS/stage2*/`, `WS/cloud_results*/out_stage2_*`, `WS/cloud_families/out_stage2_*`), and none passes.
   - The stage-2 gate was preregistered only for Qwen3-1.7B, so "FAIL" strictly applies to 1 model.
2. **§5 "In every Qwen3 size, about 0.2 depth gives nothing" [quantifier].**
   - In Qwen3-1.7B at layer 5 (depth 0.18, α 2, weak text): own→given 0.772 → 0.730 (shift +0.042, p 0.0002) and given→own 0.658 → 0.778 (+0.120, p < 0.0001).
   - Beyond random, these are **+0.060 (p 0.0001) and +0.142 (p < 0.0001)**. The given→own effect is larger than at the reported layer 13 (+0.072).
   - Sources: `WS/stage3/{oW,gW}_L5_*.json` (recomputed) and `WS/stage3_results.txt`.
   - Qwen3-8B at layer 7 also shows small raw shifts (+0.019 and +0.022, p ≤ 0.0003), though not beyond random.
   - Only 4B (layer 7), 14B (layer 8) and 32B (layer 13) are null.
3. **§5 "a sweep over 0.31–0.58 depth gives 0.03–0.10 per layer" [numeric, minor].**
   - The per-layer shifts run from **0.023** (layer 33, given→own) to 0.102 (layer 20, own→given).
   - Beyond random they run 0.027–0.108. 2 of the 10 contrasts are not significant: layer 23 given→own (p 0.074) and layer 26 own→given (p 0.52).
   - Source: raw files in `WS/cloud_sweep32/out_sweep_Qwen3-32B/`, which agree with `WS/sweep32_results.txt`.
4. **§6b "Contrarian picks stay near zero" (PREREG_G) [quantifier].**
   - This holds for Qwen3-8B and 14B (mean p_contra ≤ 0.0023).
   - In OLMo-2-7B, p_contra is **0.124 (system), 0.118 (own), 0.117 (user) and 0.110 (own, steered)**, against 0.042 with no reminder.
   - Source: `g_analyze.py` → `g.json` "means".
5. **§6b "projection and adherence correlate positively in Qwen" [quantifier, minor].**
   - Qwen3-8B's user placement has r = **−0.147** (system +0.211, own +0.117). Qwen3-14B is all positive and OLMo all negative.
   - So 5 of 6 Qwen cells are positive. Source: `h.json` `within_cell_corr_proj_goal`.
6. **§6c "In every model, the high-status header moves the text toward the 'own' end" [quantifier].**
   - In Granite-3.3-8B, CEO vs intern gives dp = proj(lo) − proj(hi) = **+0.0048 (55/5, p 5e-05) in the system turn and +0.0234 (60/0, p 5e-05) in the user turn**. The CEO text sits toward "given", the opposite direction.
   - The other 26 authority and consensus cells do move toward "own". Source: `j.json`.
7. **§6c list of disagreeing pairs ("Qwen3-14B (authority and consensus), Qwen3-8B (consensus) and OLMo-2-7B (authority and consensus)") [omission].**
   - The list covers 7 of the 8 disagreements.
   - The 8th is **Granite-3.3-8B's user-turn consensus pair: db +0.0075, p 0.00015, 47/13; dp −0.117**. Granite is not mentioned. Source: `j.json`.
8. **§6c Reading, "The role direction tracks evidence framing in every model" [quantifier, minor].**
   - Expertise is decided, and agrees, in 6 of the 7 models tested.
   - Both of Granite's expertise pairs are undecided: db −0.0004 (p 0.85) and −0.0042 (p 0.09). Source: `j.json`.
9. **§7 "'I'll…' payloads are suppressed the most under +vR" [quantifier].**
   - This is true only in Qwen3-4B (document placement): p1 0.882 → 0.050 (−0.833), against p3 −0.742, imperative −0.376 and p2 −0.334.
   - Qwen3-1.7B, document placement: p1 is at the floor (0.000 → 0.000), and the imperative drops most (−0.545).
   - Qwen3-1.7B, system placement: **p2 drops more than p1 (−0.826 vs −0.693)**.
   - Sources: `WS/inj3_q4b/inj3.json`, `WS/inj3_q17/inj3.json` and `WS/inj3_verdict.txt`.
10. **§9 "Small fine-tunes of either kind cut no-reminder drift by about three quarters" [quantifier, minor].**
    - True for the n 240 PREREG_F adapters: 0.842 → 0.206 (own) and 0.229 (given), cuts of 76% and 73%.
    - The n 16 PREREG_E adapters cut it by only about 20%: 0.838 → arm means 0.648 (own) and 0.681 (given).
    - The E4 n 48 adapters cut it by 21–38%: 0.858 → 0.534 and 0.678.
    - Sources: `e3.json`, `e4.json` and `f.json`.
11. **§9 "The training-data seed moved no-reminder drift between 0.08 and 0.35 within one arm" [numeric, minor].**
    - The own arm spans 0.079–0.323 and the given arm 0.105–0.353.
    - No single arm spans 0.08–0.35: the quoted range joins one arm's minimum to the other arm's maximum. Source: `f.json` `per_adapter` d1.

**Outside the requested scope.** §12 item 3, "Preference stages do not add to it" (OLMo-2-7B), is stronger than the data [quantifier].
- The gap rises 0.063 → 0.071 → 0.077 (+0.014, +22%).
- The step tests are DPO +0.0085 (p 0.16) and Instruct +0.0053 (p 0.031).
- The sealed rule supports only "no amplification at p < 0.01", which §6 states correctly.

### Gate verdicts

Every verdict the paper reports follows from its sealed rule applied to the stored data:
- main run H1/H2 PASS, and run B PASS;
- PREREG_C: 1 PASS + 2 PRESENT BUT WEAK, which the sealed table reads as family-dependent;
- PREREG_D AMBIGUOUS; E FAIL; F FAIL; G FAIL; H ONE AXIS; I PASS; J MIXED; K PARTIAL; L NO_TREND/NO_TREND;
- PREREG_M: MIXED / MIXED / DOES_NOT_TRACK;
- inj2 PASS; inj3 deixis refuted in both models; addressee INCONCLUSIVE;
- the fix pilot and the decomposition diagnostic: both NO-GO.

No verdict fails to follow from its rule. Two labelling issues remain:
- **The legend defines PASS/FAIL as "a preregistered gate, hash-sealed before data".**
  - The stage-1 "PASS" (§3), stage-2 "FAIL" (§4) and stage-3 "PASS" (Qwen3-1.7B) and "FAIL" (Qwen3-32B) (§5) rest on gates written into `PLAN_7DAY.md` before data. No `.sha256` seal exists for them.
  - inj2, inj3 and addr have code-only hashes.
- **Inconsistent labels in the same §5 table.** The 32B row is labelled "FAIL", but the same exploratory replication is labelled "EXPL. (gate met)" for 4B–14B.
- **One undisclosed caveat (§6b).** In PREREG_I, the Qwen3-4B direction came from the 4-bit stage-2 run while the pod ran bf16. This was logged at the seal but is not stated in §6b.

### Other notes (no status change)

- **The plain-label result is exploratory.** The Abstract states "The discount disappears when roles are written as plain-text labels" without the EXPL. tag. It is an exploratory pilot: one model, n 20 (+0.013, p 0.54).
- **§6e quotes the unadjusted p 0.126 (shown as "p 0.13").** The sealed verdict uses Holm p 0.253; both give NO_TREND.
- **§6b's "21 decided pairs" mixes counting units.** It counts 2 pairs per model in PREREG_H (A1, A2) and 3 per model in PREREG_I. H did not test user − own.
- **§5's Qwen3-32B "+0.04 beyond random" includes a non-significant value.** The given→own value (+0.039) has p 0.435.
- **The §7 refutation in the Qwen3-1.7B document placement is a floor result** (p1 base 0.000). The informative refutation in that model is the system placement.
- **The §3 scale table mixes notations.** "(40/40)" means 40 of 40 seeds positive, while other rows use pos/neg, such as 37/3.
- **`main_results.json`, cited in `RESULTS.md`, is not in `WS/`.** The main-run numbers were reproduced from the raw files in `WS/main/`.
- **`AR/bo_pilot/pilot_results.json` is a 0-byte file.** The pilot-1 value (Bg0 p_hi 0.936) was re-derived from the 20 raw run files.
- **The CPU re-runs never touched the GPU.** No downloads or network were used. The only file written to `WS/` is this one.

### Re-run log (all scripts' sha256 match the seals)

| Script | Data root | Result vs stored file |
|---|---|---|
| `analyze.py` | `WS/main` | Reproduces `RESULTS.md` (H1 +0.381, Holm 0.0001; H2 +0.178, p 0.0247). `main_results.json` is absent |
| `analyze_b.py` | `WS/main_b` | Identical to `WS/main_b_results.json` |
| `fast_analyze.py` | `WS/fast_val` (plus `--min-mass 0.5`) | Identical to `WS/fast_val_results.txt` and `fast_val_results_mm.txt` |
| `c_analyze.py` | `AR/prereg_c` | Identical to `c_results.json` |
| `d_analyze.py` | `AR/lineage/out_ld` | Identical to `d_results.json` |
| `e2_analyze.py`, `e3_analyze.py`, `e4_analyze.py`, `f_analyze.py` | `AR/binding_e2`, `AR/binding_e3`, `AR/binding_e4`, `AR/prereg_f` | Identical to `e2.json`, `e3.json`, `e4.json`, `f.json` |
| `g_analyze.py`, `h_analyze.py` | `AR/prereg_g`, `AR/prereg_h` | Identical to `g.json`, `h.json` |
| `i_analyze.py` | `AR/prereg_i/out_i` | Identical to `i.json` except the trailing newline |
| `j_analyze.py`, `k_analyze.py`, `l_analyze.py`, `m_analyze.py` | `AR/prereg_{j,k,l,m}` | Identical to `j.json`, `k.json`, `l.json`, `m.json` |
| `n_pilot.py` | Copy of `AR/ci_pilot/out_np` | NO-GO; best gain +0.023 (Qwen3-8B, α 2) |

---

## Claim table

### Abstract

| Section / # | Claim (brief) | Paper | Primary / recomputed | Primary file (script) | Status |
|---|---|---|---|---|---|
| Abs.1 | Own-turn gap passed a preregistered test in Qwen3-1.7B | PASS | Main H2 +0.178 (p 0.0247); run B H2 +0.107 (Holm 0.0368) | `WS/main`, `WS/main_b` (`analyze.py`, `analyze_b.py`) | MATCH |
| Abs.2 | Qwen3 gap grows from 1.7B to 32B | +0.005 → +0.144 | +0.0047 → +0.1437, monotonic over 1.7, 4, 8, 14, 32B | `WS/fast_val` … `WS/cloud_results32/out_fast_Qwen3-32B` (sealed `signflip`) | MATCH |
| Abs.3 | Gap clear in OLMo-2-7B, small in Granite, reversed in SmolLM3 | qualitative | +0.079 (35/5); +0.0056 (p 0.046; n.s. at mass ≥ 0.5); −0.0141 (p 0.030) | `WS/cloud_families/out_fast_*`, `WS/fast_SmolLM3-3B` | MATCH |
| Abs.4 | Strong steering in Qwen3 1.7B–14B: 1 preregistered pass, gate met at 3 more sizes | 1 + 3 | 1.7B gate pass at layer 13; 4B/8B/14B shifts ≥ 0.111 both ways, beyond random p < 0.0001; 32B fails | `WS/stage3*`, `WS/cloud_results*/out_stage3_*` (raw) | MATCH |
| Abs.5 | Three other families, same sign: 1 pass, 2 weak | 1 + 2 | SmolLM3 PASS; OLMo and Granite PRESENT BUT WEAK | `AR/prereg_c` (`c_analyze.py`) | MATCH |
| Abs.6 | OLMo-2: gap and direction present after SFT at 7B; combined verdict AMBIGUOUS; 13B gap tiny | — | 7B H-SFT (G_SFT +0.063); cos 0.994; 13B G ≤ 0.0081; AMBIGUOUS | `AR/lineage` (`d_analyze.py`) | MATCH |
| Abs.7 | Gap disappears with plain-text role labels | — | Plain +0.0132 (p 0.54) vs native +0.080 (p 0.00035); n 20, one model | `AR/lineage_pilot7b/pilot7b_results.json` | MATCH (exploratory; not tagged as such in the Abstract) |
| Abs.8 | user > system > own replicates under seal in 3 models, 2 families; ONE AXIS 3/3 | 3/3 | ONE AXIS in Qwen3-8B, Qwen3-14B, OLMo-2-7B | `AR/prereg_h` (`h_analyze.py`) | MATCH |
| Abs.9 | Six more models PASS: 4 families, 1.7B–32B; 15/15 decided agree, 0 against | 15/15 | 15 decided, 15 agree, 0 disagree; Qwen3, SmolLM3, Granite, OLMo-2 | `AR/prereg_i` (`i_analyze.py`) | MATCH |
| Abs.10 | Ablation erases 27–44% in three Qwen models, none in OLMo; PARTIAL | 27–44% | F 0.266 / 0.422 / 0.437; 14B 0.353 n.s.; OLMo −0.039; PARTIAL | `AR/prereg_k` (`k_analyze.py`) | MATCH |
| Abs.11 | Social cues move text along vR in every model; obedience follows only in small models; MIXED | 7/7 | All 28 authority/consensus projection contrasts significant (p 5e-05); agreement only in 1.7B, 4B, SmolLM3; MIXED | `AR/prereg_j` (`j_analyze.py`) | MATCH (non-directional; Granite authority moves the other way, see §6c.6) |
| Abs.12 | J: Nature < blog in 12/12 decided comparisons | 12/12 | 12 decided expertise pairs, all db < 0 and AGREE | `j.json` | MATCH |
| Abs.13 | M MIXED; self-framing raised goal-choice probability in 5/6; vR did not track it (4/11) | 5/6; 4/11 | OWN D < 0 in 5 models (Holm 0.0003), > 0 in 1; H3 4 agree / 3 disagree / 4 unresolved | `AR/prereg_m` (`m_analyze.py`) | MATCH |
| Abs.14 | Two preregistered fine-tuning fixes both failed | 2 FAIL | E FAIL (perm p 0.0714); F FAIL (P1, P2, gate) | `AR/binding_e3`, `AR/prereg_f` (`e3_analyze.py`, `f_analyze.py`) | MATCH |
| Abs.15 | Fine-tunes cut drift but not below plain reminders; partial shortcut; raise forged-assistant injection | — | F: own 0.206 vs base with system reminder 0.182; shortcut +0.072; injection +0.065 / +0.041 (F), +0.016 / +0.032 (E) | `f.json`, `e3.json` | MATCH |

### §2 Instrument

| Section / # | Claim (brief) | Paper | Primary / recomputed | Primary file (script) | Status |
|---|---|---|---|---|---|
| §2.1 | 3 history quarters; 30 test quarters (22 for 4,096-token models) | 3 / 30 / 22 | `N_HIST = 3`; `AGP_NTEST` default 30; OLMo runs use 22 | `WS/code/agp_fast.py`, `WS/cloud/rc7–rc23.sh` | MATCH |
| §2.2 | Reminder every 3 test steps | 3 | `INSERT_AT = range(0, 30, 3)` | `WS/code/agp_fast.py` | MATCH |
| §2.3 | Swapped world: OLMo-2-7B system reminder raises high-emission picks | 0.088 → 0.277 | Base swapped cell 1 0.0875 → gF 0.2772 | `AR/binding_e2` (`e2_analyze.py`) | MATCH |
| §2.4 | Context length recorded; OLMo window forced shorter episodes | — | Max readout context 3,611 (C) and 3,668 (D) with N_TEST 22; at N_TEST 30, steps 23–29 fall outside the window (min-mass median 0.0007 vs 0.584 inside) | `c_results.json`, `d_results.json`, `AR/cloud_families/olmo_results_*.json` | MATCH |

### §3 Behaviour

| Section / # | Claim (brief) | Paper | Primary / recomputed | Primary file (script) | Status |
|---|---|---|---|---|---|
| §3.1 | Main 2×2, H1 (notes − fixed) | p 0.0001 | +0.381; raw p 0.00005, Holm 0.0001 | `WS/main` (`analyze.py`) | MATCH |
| §3.2 | Main H2, own − given (fixed text) | +0.18, p 0.025 | +0.1778, p 0.0247 | Same | MATCH |
| §3.3 | Run B, H1 | p_Holm 0.0001 | 0.0001 | `WS/main_b` (`analyze_b.py`) | MATCH |
| §3.4 | Run B, H2 | +0.11, p_Holm 0.037 | +0.1071, 0.0368 | Same | MATCH |
| §3.5 | Run B: own worse in 26 of 35 non-tied seeds | 26/35 | 26 worse, 9 better, 5 tied | `WS/main_b` (per-seed recount) | MATCH |
| §3.6 | Run B, S1 not detected | n.s. | +0.057, p 0.36 | Same | MATCH |
| §3.7 | Fast-instrument p_hi: 1 / gF / oF / gN / oN | 0.96 / 0.041 / 0.046 / 0.82 / 0.84 | 0.9594 / 0.0413 / 0.0460 / 0.8249 / 0.8421 | `WS/fast_val` (`fast_analyze.py`) | MATCH |
| §3.8 | Reproduces all three preregistered directions (stage-1 PASS) | 3/3 | notes − fixed +0.790; oF − gF +0.0047 (p 0.0038); 1 − gF +0.918; all p < 0.05 | Same | MATCH |
| §3.9 | Qwen3-1.7B own − given; weak text | +0.005; +0.107 (40/40) | +0.0047; +0.1067 (40 pos / 0 neg) | `WS/fast_val` | MATCH |
| §3.10 | Qwen3-4B (4-bit) | +0.021 (37/3) | +0.0207 (37/3); 4-bit set by `AGP_4BIT=1` in `code/chain2.sh` (not recorded in the outputs) | `WS/fast_Qwen3-4B` | MATCH |
| §3.11 | Qwen3-8B | +0.028 (33/7) | +0.0283 (33/7) | `WS/cloud_results/out_fast_Qwen3-8B` | MATCH |
| §3.12 | Qwen3-14B | +0.110 (40/40) | +0.1100 (40/0) | `WS/cloud_results/out_fast_Qwen3-14B` | MATCH |
| §3.13 | Qwen3-32B | +0.144 (37/3) | +0.1437 (37/3) | `WS/cloud_results32/out_fast_Qwen3-32B` | MATCH |
| §3.14 | OLMo-2-7B in window (post hoc); all steps | +0.079 (35/5); +0.082 | +0.0790 (35/5) on steps k ≤ 22; +0.0822 (37/3) on all steps | `WS/cloud_families/out_fast_OLMo-…`, `AR/cloud_families/olmo_results_k23.json` | MATCH |
| §3.15 | OLMo-2-13B (PREREG_D, 80 seeds) | +0.008 | +0.0081 (53/27, p 0.0086) | `AR/lineage` (`d_analyze.py`) | MATCH |
| §3.16 | Granite-3.3-8B; n.s. without low-mass steps | +0.006 (p 0.046) | +0.0056 (p 0.0461); at mass ≥ 0.5, +0.0039 (p 0.164) | `WS/cloud_families/out_fast_granite-…` | MATCH |
| §3.17 | SmolLM3-3B, reversed | −0.014 (p 0.03) | −0.0141 (p 0.0296) | `WS/fast_SmolLM3-3B` | MATCH |
| §3.18 | SmolLM2, EuroLLM and OLMo-2-1B do not respond to the goal | — | 1 − gF: −0.005 (p 0.51); +0.002 (p 0.78); −0.007 (p 0.51, base) | `WS/fast_SmolLM2-…`, `WS/fast_EuroLLM-…`, `AR/lineage_pilot/pilot_results.json` | MATCH |
| §3.19 | OLMo-2 does not grow: 7B vs 13B | +0.077 vs +0.008 | +0.0767 vs +0.0081 | `d_results.json` | MATCH |
| §3.20 | In every capable model, own notes drift far more than a fixed reminder | 8/8 | oN − oF from +0.13 (32B) to +0.80 (1.7B); positive in 8/8 | Fast dirs (raw) | MATCH |
| §3.21 | In Qwen3 the gap grows steadily with size | — | 0.0047 < 0.0207 < 0.0283 < 0.1100 < 0.1437 | Fast dirs (raw) | MATCH |

### §4 Representation

| Section / # | Claim (brief) | Paper | Primary / recomputed | Primary file (script) | Status |
|---|---|---|---|---|---|
| §4.1 | Gate: transfer AUC ≥ 0.8 both ways, ≥ 0.15 above the system-vs-user control | 0.8 / 0.15 | Same text in the stage-2 gate (fixed before data; not hash-sealed) | `WS/PLAN_7DAY.md` (2026-10-26) | MATCH |
| §4.2 | Qwen3-1.7B fails | 0.80 / 0.796, gap 0.12 | Layer 5: R→A 0.802, A→R 0.796, control 0.679 (gap 0.117) | `WS/stage2/probe_results.json` | MATCH |
| §4.3 | Control transfers as well or better in the 9 other models | 9/9 | At each model's best min(R→A, A→R) layer, control ≥ min in 9/9: SmolLM2 0.524 = 0.524; EuroLLM 0.624 > 0.509; Q4B 0.820 > 0.731; Q8B 0.890 > 0.765; Q14B 0.861 > 0.725; Q32B 0.918 > 0.705; SmolLM3 0.885 > 0.745; OLMo 0.953 > 0.713; Granite 0.753 > 0.691 | 9 × `probe_results.json` | MATCH (against the weaker direction, as the gate uses; R→A alone beats control in Q14B (0.920) and SmolLM3 (0.967)) |
| §4.4 | Heading: "FAIL, 9 models" | 9 | 10 models probed (the §4 body names all 10); none passes; the sealed gate applied to Qwen3-1.7B only | 10 × `probe_results.json` | **MISMATCH** [numeric] |

### §5 Mechanism

| Section / # | Claim (brief) | Paper | Primary / recomputed | Primary file (script) | Status |
|---|---|---|---|---|---|
| §5.1 | Qwen3-1.7B, weak text, layer 13 (0.46): own→given; given→own | 0.772 → 0.634; 0.658 → 0.815 | 0.7721 → 0.634; 0.6577 → 0.815 | `WS/stage3` (raw, seeds 400–419) | MATCH |
| §5.2 | Qwen3-1.7B beyond random; Holm p | +0.086 / +0.072; 0.0001 | +0.086 / +0.072; Holm over 3 layers = 3 × 5e-05 = 0.00015 (printed as 0.0001 in `stage3_results.txt`) | `WS/stage3`, `WS/stage3_results.txt` | ROUNDING |
| §5.3 | Qwen3-4B, layer 17 (0.47) | 0.386 → 0.276; 0.347 → 0.482; +0.170 / +0.116 | Same (base oF 0.386 per the original 3-dp output) | `WS/stage3_Qwen3-4B` | MATCH |
| §5.4 | Qwen3-8B, layer 17 | 0.306 → 0.154; 0.258 → 0.580; +0.21 to +0.30 | Same; +0.205 / +0.295 | `WS/cloud_results/out_stage3_Qwen3-8B` | MATCH |
| §5.5 | Qwen3-14B, layer 18 (0.45) | 0.302 → 0.133; 0.179 → 0.434; +0.27 to +0.32 | Same; +0.269 / +0.321 | `WS/cloud_results/out_stage3_Qwen3-14B` | MATCH |
| §5.6 | Qwen3-32B, layer 29 (0.45): FAIL | 0.881 → 0.838; 0.747 → 0.770; +0.04 | Same; beyond random +0.040 (p < 0.0001) / +0.039 (p 0.435, n.s.); own shift 0.044 < 0.05 | `WS/cloud_results32/out_stage3_Qwen3-32B` | MATCH |
| §5.7 | 32B sweep over 0.31–0.58 depth | 0.03–0.10 per layer | Shifts 0.023–0.102; beyond random 0.027–0.108, 2/10 n.s. | `WS/cloud_sweep32/out_sweep_Qwen3-32B` (raw) | **MISMATCH** [numeric, minor] |
| §5.8 | Depths 13/28, 17/36, 17/36, 18/40, 29/64 | 0.46, 0.47, 0.47, 0.45, 0.45 | 0.464, 0.472, 0.472, 0.450, 0.453 (layer counts from the probe files) | `probe_results.json` | MATCH |
| §5.9 | "In every Qwen3 size, about 0.2 depth gives nothing" | every | 1.7B layer 5: beyond random +0.060 / +0.142 (p ≤ 0.0001); 8B layer 7 raw shifts p ≤ 0.0003 | `WS/stage3/*_L5_*`, `WS/stage3_results.txt` | **MISMATCH** [quantifier] |
| §5.10 | α = 1 gives about half the effect | ~0.5 | α1/α2 shift ratio at the mid layer: 0.56 / 0.59 (1.7B), 0.55 / 0.51 (4B), 0.70 / 0.35 (8B), 0.58 / 0.34 (14B) | Stage-3 raw files | MATCH (approximate) |
| §5.11 | Ticker mass unchanged | — | Mass ratio 0.996–1.003 | Stage-3 results | MATCH |
| §5.12 | 14B: steered own text vs real system text | 0.133 vs 0.179 | 0.133 vs 0.179 | `out_stage3_Qwen3-14B` | MATCH |
| §5.13 | Other families at Qwen depths: small at ~0.2, none at ~0.45 | — | Beyond random at ~0.2: Granite layer 8 +0.007 / +0.025 (fixed text), +0.015 / +0.040 (weak); OLMo layer 6 +0.029 / +0.041; SmolLM3 layer 7 +0.010 / +0.013. At ~0.45 (Granite layer 18, OLMo layer 15, SmolLM3 layer 17), |beyond random| ≤ 0.012 with no two-way effect. SmolLM3 weak text at layer 15 (0.42) is mixed: +0.027 / −0.007 | `AR/cloud_families/granite_results.json`, `olmo_results_k23.json`; `WS/stage3_smol3_results.txt`, `stage3w_smol3_results.txt` | MATCH (approximate) |
| §5.14 | Depth sweep on seeds 400–419; confirmation on 40 fresh seeds | — | Phase A 400–419 (n 20); phase B 500–539 (n 40) | `AR/prereg_c/out_cA_*`, `out_cB_*` | MATCH |
| §5.15 | SmolLM3, layer 7 (0.19), weak text: PASS | −0.053 / +0.127; +0.065 / +0.126 | −0.0527 / +0.1265; +0.0651 / +0.1257 | `c_results.json` (`c_analyze.py`) | MATCH |
| §5.16 | OLMo-2-7B, layer 10 (0.31): present but weak | −0.047 / +0.075; +0.053 / +0.074 | −0.0470 / +0.0755; +0.0532 / +0.0744 | Same | ROUNDING (0.0755 shown as 0.075) |
| §5.17 | Granite, layer 10 (0.25): present but weak | −0.018 / +0.035; +0.038 / +0.038 | −0.0179 / +0.0347; +0.0379 / +0.0384 | Same | MATCH |
| §5.18 | Every non-Qwen beyond-random test | p_Holm 0.00015 | All 6 at 0.00015 | Same | MATCH |
| §5.19 | 1 PASS of 3 → family-dependent | 1/3 | The PREREG_C table maps 1 to "family-dependent" | `WS/PREREG_C.md` | MATCH |
| §5.20 | Best depth: Qwen ~0.46, OLMo 0.31, Granite 0.25, SmolLM3 0.19 | — | 10/32, 10/40, 7/36 | `c_results.json` selection | MATCH |

### §6 Origin (PREREG_D)

| Section / # | Claim (brief) | Paper | Primary / recomputed | Primary file (script) | Status |
|---|---|---|---|---|---|
| §6.1 | Cells 1/gF/oF/uF; 80 fresh seeds; competence gate ≥ 0.05 at p < 0.01 | 80 | Seeds 600–679 in all 6 checkpoints; gate as in `d_analyze.py` | `AR/lineage/out_ld` | MATCH |
| §6.2 | All 6 checkpoints share a byte-identical chat template | — | Stated only in `PREREG_D.md` and the log (md5 70bb224ce1); no tokenizer files among the local results | — | UNVERIFIABLE |
| §6.3 | 7B own − given: SFT / DPO / Instruct | +0.063 (69/11) / +0.071 (76/4) / +0.077 (75/5) | +0.0628 / +0.0714 / +0.0767, same seed counts | `d_analyze.py` | MATCH |
| §6.4 | 7B H-SFT; amplification at DPO, Instruct | +0.009 (p 0.16); +0.005 (p 0.031) | +0.0085 (p 0.161); +0.0053 (p 0.0306) | Same | MATCH |
| §6.5 | 13B gaps; H-pref by threshold; only the final stage at p < 0.01 | +0.0075 / +0.0066 / +0.0081 | Same; p 0.028 / 0.027 / 0.0086 | Same | MATCH |
| §6.6 | Combined verdict | AMBIGUOUS | AMBIGUOUS | Same | MATCH |
| §6.7 | Share of the final 7B gap present at SFT | 82% | 0.0628 / 0.0767 = 81.9% | Same | MATCH |
| §6.8 | Layer-10 cosine, SFT vs Instruct | 0.994 | 0.994 | `d_results.json` probes_7B | MATCH |
| §6.9 | Relative discount, SFT vs DPO | 0.133 vs 0.106 | R = 0.1326 / 0.1063 (Instruct 0.1128) | Raw recompute | MATCH |
| §6.10 | OLMo-2 base 1B and 7B do not respond | — | 1 − gF −0.0073 (p 0.51); +0.0046 (p 0.69) | `AR/lineage_pilot`, `AR/lineage_pilot7b` | MATCH |
| §6.11 | Plain labels vs native template | +0.013 n.s. vs +0.080 | +0.0132 (p 0.54) vs +0.0800 (p 0.00035) | `pilot7b_results.json` | MATCH |
| §6.12 | user > system > own at every stage and size; uF − gF | −0.05 to −0.12, p 0.0001 | −0.0546 to −0.1208 (all p 5e-05); own − given > 0 in 6/6 | `d_results.json` | MATCH |

### §6b One axis (PREREG_G, H, I)

| Section / # | Claim (brief) | Paper | Primary / recomputed | Primary file (script) | Status |
|---|---|---|---|---|---|
| §6b.1 | PREREG_G (60 fresh seeds): system − own | +0.030 / +0.058 / +0.089, p 0.0001 | +0.0303 / +0.0583 / +0.0892, p 5e-05 each; seeds 1300–1359 | `AR/prereg_g` (`g_analyze.py`) | MATCH |
| §6b.2 | "Contrarian picks stay near zero" | ~0 | Qwen ≤ 0.0023; OLMo 0.110–0.124 in every reminder cell | `g.json` means | **MISMATCH** [quantifier] |
| §6b.3 | PREREG_H user − system / system − own; Holm | +0.045 / +0.022 / +0.108; +0.024 / +0.061 / +0.061; ≤ 0.00025 | +0.0449 / +0.0219 / +0.1080; +0.0239 / +0.0606 / +0.0609; max Holm 0.00025 | `AR/prereg_h` (`h_analyze.py`) | MATCH |
| §6b.4 | Projections system − user; own − system | +2.12 (58/2), +1.74, +0.38; +1.34, +1.33, +0.12 (60/0) | 2.1171 (58/2), 1.7387, 0.3766; 1.3383, 1.3275, 0.1200 (60/0) | Same | MATCH |
| §6b.5 | ONE AXIS | 3/3 | 3/3 | Same | MATCH |
| §6b.6 | Within-placement correlation positive in Qwen, negative in OLMo | — | Q8B +0.211 / +0.117 / **−0.147**; Q14B +0.267 / +0.267 / +0.424; OLMo −0.251 / −0.415 / −0.313 | `h.json` | **MISMATCH** [quantifier, minor] |
| §6b.7 | A user reminder beats the steered own note (G FAIL); a system boost beats user in 14B only | — | C2: 8B −0.022 (Holm 0.0001), 14B −0.011 (n.s.); boost vs user: 14B +0.010 (p 5e-05), 8B −0.008, OLMo −0.056 | `g.json` | MATCH |
| §6b.8 | PREREG_I seeds | 1500–1559 (32B 1500–1539) | Same | `AR/prereg_i/out_i` | MATCH |
| §6b.9 | PASS rule | ≥ 8 decided, ≥ 80% agree | As in `i_analyze.py` | `WS/code/i_analyze.py` | MATCH |
| §6b.10 | Qwen3-1.7B row | 0.871 / 0.854 / 0.848; +0.017 (46/14); +0.006 (38/22); +3.29 / +1.96 | 0.8711 / 0.8540 / 0.8478; +0.0171; +0.0062; 3.2873 / 1.9627 | `i.json` (`i_analyze.py`) | MATCH |
| §6b.11 | SmolLM3 row | 0.785 / 0.772 / 0.771; +0.013 (44/16); +0.000; +0.11 / +0.05 | 0.7846 / 0.7715 / 0.7711; +0.0132; +0.0003 (p 0.94); 0.1114 / 0.0534 | Same | MATCH |
| §6b.12 | Qwen3-4B row | 0.864 / 0.808 / 0.777; +0.056 (60/0); +0.031 (56/3); +1.31 / +0.55 | 0.8639 / 0.8083 / 0.7768; +0.0557; +0.0314; 1.3122 / 0.5501 | Same | MATCH |
| §6b.13 | Granite row | 0.901 / 0.892 / 0.888; +0.009 (38/22); +0.005; +0.17 / +0.36 | 0.9009 / 0.8924 / 0.8878; +0.0085; +0.0046 (p 0.074); 0.1738 / 0.3589 | Same | MATCH |
| §6b.14 | OLMo-2-13B row | 0.853 / 0.818 / 0.814; +0.035 (56/4); +0.004; +0.48 / +0.05 | 0.8527 / 0.8176 / 0.8141; +0.0351; +0.0035 (p 0.30); 0.4789 / 0.0454 | Same | MATCH |
| §6b.15 | Qwen3-32B row (n 40) | 0.587 / 0.342 / 0.184; +0.245 (35/5); +0.157 (37/3); +4.68 / +1.25 | 0.5867 / 0.3415 / 0.1843; +0.2451; +0.1572; 4.6799 / 1.2529 | Same | MATCH |
| §6b.16 | All 6 pass the competence gate | 6/6 | 6/6 (lowest: 32B +0.279, p 5e-05) | Same | MATCH |
| §6b.17 | 15 decided, all agree; undecided = system − own in SmolLM3, Granite, OLMo-13B | 15/15 | Same | Same | MATCH |
| §6b.18 | Every projection difference has the same sign on every seed | 60/0; 40/0 | 18/18 pairs | Same | MATCH |
| §6b.19 | With H: 9 models, 4 families, 21 decided pairs, all agree | 21 | 15 (I) + 6 (H: A1, A2 × 3 models) | `h.json`, `i.json` | MATCH (H counts 2 pairs per model, I counts 3) |
| §6b.20 | vR places user further toward "given" in 9/9; user obeyed more than system in 9/9 | 9/9 | P1 > 0 in 3/3 (H); u − g projection > 0 in 6/6 (I); behaviour u − g decided > 0 in 9/9 | Same | MATCH |
| §6b.21 | Spearman of gap ratios across 9 models | 0.10 | ρ = 0.100 | Computed from `h.json` + `i.json` | MATCH |
| §6b.22 | SmolLM3: system ≈ own, user highest | — | g − o +0.0003 (p 0.94); user highest | `i.json` | MATCH |
| §6b.23 | Qwen3-32B has the largest role gaps (user − own) | +0.40 | +0.4024 (largest of the 9) | `i.json` | MATCH |

### §6c Social cues (PREREG_J)

| Section / # | Claim (brief) | Paper | Primary / recomputed | Primary file (script) | Status |
|---|---|---|---|---|---|
| §6c.1 | 7 models, fresh seeds, 50 random-direction null | 7 | 7 models, seeds 1700–1759 (n 60) | `AR/prereg_j/out_j` | MATCH |
| §6c.2 | 20 of 28 decided agree; null 95th percentile; < 0.8; MIXED | 0.71; 0.64 | 0.714; 0.643; MIXED | `j.json` (`j_analyze.py`) | MATCH |
| §6c.3 | Expertise: 12/12 decided, 6 models, both roles; Nature obeyed less | 12/12 | 12 decided expertise pairs, all db < 0 and AGREE; Granite undecided | Same | MATCH |
| §6c.4 | Nature text sits higher on vR | — | dp < 0 in all 14 expertise cells | Same | MATCH |
| §6c.5 | Prediction stated before data; not a gate | — | `PREREG_J.md`, line 75 | `WS/PREREG_J.md` | MATCH |
| §6c.6 | "In every model, the high-status header moves the text toward 'own'" | 7/7 | Granite authority dp +0.0048 (55/5) and +0.0234 (60/0) → toward "given" | `j.json` | **MISMATCH** [quantifier] |
| §6c.7 | Small models (1.7B, 4B, SmolLM3): high status obeyed less, pairs agree | — | All 8 decided authority/consensus pairs in these models AGREE (3 + 3 + 2) | Same | MATCH |
| §6c.8 | Disagreements: 14B (authority and consensus), 8B (consensus), OLMo (authority and consensus) | 7 implied | 8 disagree: 14B × 4, 8B × 1, OLMo × 2, plus Granite user-turn consensus (db +0.0075, p 0.00015) | Same | **MISMATCH** [omission] |
| §6c.9 | Reading: vR tracks evidence framing in every model | 7/7 | 6/7 (Granite expertise undecided) | Same | **MISMATCH** [quantifier, minor] |

### §6d Ablation (PREREG_K)

| Section / # | Claim (brief) | Paper | Primary / recomputed | Primary file (script) | Status |
|---|---|---|---|---|---|
| §6d.1 | Qwen3-4B / 8B / 14B / 32B and OLMo-2-7B on fresh seeds | 5 models | Seeds 1800–1859 (32B 1800–1839) | `AR/prereg_k/out_k` | MATCH |
| §6d.2 | Spread removed; Holm T1/T2 | 42% (0.017/0.016), 44% (0.021/0.016), 27% (0.047/0.003); 14B 35% n.s.; OLMo none | F 0.422 (0.0165/0.0156), 0.437 (0.0212/0.0156), 0.266 (0.0470/0.0033); 14B 0.353 (0.229/0.614); OLMo −0.039 | `k.json` (`k_analyze.py`) | MATCH |
| §6d.3 | Competence retained | 64–95% of plain | 0.641 (32B) to 0.949 (OLMo) | Same | MATCH |
| §6d.4 | PARTIAL; no model reaches 50% | — | Max F 0.437; PARTIAL | Same | MATCH |
| §6d.5 | system − own under ablation | 8B 0.020 → 0.003; 32B 0.151 → 0.044 | 0.0204 → 0.0026; 0.1508 → 0.0435 | Same | MATCH |
| §6d.6 | user − system mostly survives | — | Ablated/plain u − g: 0.63 (4B), 0.71 (8B), 0.56 (14B), 1.12 (32B) | Same | MATCH |

### §6e Size (PREREG_L)

| Section / # | Claim (brief) | Paper | Primary / recomputed | Primary file (script) | Status |
|---|---|---|---|---|---|
| §6e.1 | 15 models, 4 families, sizes as listed | 15 | 15 folders as listed; seeds 1900–1959 (32B 1900–1939) | `AR/prereg_l/out_l` | MATCH |
| §6e.2 | Goal holding: no trend; larger hold better in 3 of 4 families | p 0.13; 3/4 | T 2.0, p 0.126 (Holm 0.253); ρ −0.3 / +0.8 / +1.0 / +0.5 | `l.json` (`l_analyze.py`) | MATCH (unadjusted p quoted) |
| §6e.3 | Qwen3-32B collapse replicates | P 0.34 vs 0.89 | 0.3376 vs 0.8876; anomaly test p 5e-05 | Same | MATCH |
| §6e.4 | Qwen2.5-32B and OLMo-2-32B among the most persistent | 0.90; 0.96 | 0.8975 (3rd of 15); 0.9639 (1st) | Same | MATCH |
| §6e.5 | Source sensitivity: no trend; monotonic in Qwen3 and Qwen2.5; OLMo the other way | p 0.13 | p 0.126; Qwen3 0.017 → 0.376 and Qwen2.5 0.151 → 0.327, both monotonic; OLMo 0.182 → 0.049 → 0.062 (ρ −0.5) | Same | MATCH |
| §6e.6 | user > system significant 15/15; system > own 13/15, other 2 positive; none the other way | 15/15; 13/15 | 15/15; 13/15 (Qwen3-1.7B +0.0032, p 0.079; OLMo-2-13B +0.0046, p 0.26) | Raw `out_l` (`l_analyze.signflip`) | MATCH |

### §6f Semantic self-attribution (PREREG_M)

| Section / # | Claim (brief) | Paper | Primary / recomputed | Primary file (script) | Status |
|---|---|---|---|---|---|
| §6f.1 | 6 models, 60 fresh seeds, 20 conditions | 6 / 60 / 20 | 6 × 20 files, seeds 2000–2059 | `AR/prereg_m/out_m` | MATCH |
| §6f.2 | H1 MIXED (1 / 5); H2 MIXED (4 / 1 / 1); H3 DOES_NOT_TRACK (4/11, 3, 4); SELF_DISCOUNT not met | — | Same | `m.json` (`m_analyze.py`) | MATCH |
| §6f.3 | OWN table (pp): OLMo, 1.7B, 14B, 4B, 8B, SmolLM3; Holm | −5.185, +0.357, −7.707, −2.255, −8.985, −0.978; 0.0003 / 0.0198 | Same values | Same | MATCH |
| §6f.4 | MIXED rather than REVERSED because one model goes the other way | — | Rule requires no D > 0; Qwen3-1.7B D > 0 (Holm 0.0198) | `m_analyze.py` | MATCH |
| §6f.5 | Plain role order user > system > assistant in all six | 6/6 | Mean order "ugo" × 6 | `m.json`, `m_descriptive_check.json` | MATCH |
| §6f.6 | Nature < blog same sign in 11/12; reversal in Qwen3-8B user turn | 11/12 | 11/12; Qwen3-8B user −0.0235 | `m.json` pairs | MATCH |
| §6f.7 | Six sealed hashes match agp19 or the preregistration | 6/6 | 6/6 (bundle extracted to scratch; `agp19.tgz` md5 b1215514…) | `WS/bundles/agp19.tgz`, `PREREG_M.sha256` | MATCH |
| §6f.8 | 120 files, each with 60 unique seeds | 120 | 120/120 | `out_m` | MATCH |
| §6f.9 | Transfer MD5 | 2ceefa5a… | 2ceefa5a34f4f7762a233f6024b06f73 | `WS/cloud_prereg_m/results23.tgz` | MATCH |

### §7 Accounts that failed

| Section / # | Claim (brief) | Paper | Primary / recomputed | Primary file (script) | Status |
|---|---|---|---|---|---|
| §7.1 | Deixis refuted (preregistered) in Qwen3-4B and 1.7B | FAIL × 2 | "DIAL/ADDRESSEE (deixis refuted)" in both | `WS/inj3_verdict.txt`, `inj3.json` | MATCH (the 1.7B document placement is a floor case) |
| §7.2 | "'I'll…' payloads are suppressed the most under +vR" | most | True only in Qwen3-4B; 1.7B system p2 −0.826 > p1 −0.693; 1.7B document p1 at floor | `WS/inj3_q4b/inj3.json`, `WS/inj3_q17/inj3.json` | **MISMATCH** [quantifier] |
| §7.3 | Addressee INCONCLUSIVE; fraction of the role gap | −0.22, −0.15 | −1.289 / 5.795 = −0.222; −2.506 / 17.188 = −0.146 | `WS/addr_verdict.txt`, `addr_*/addr.json` | MATCH |

### §8 Injection

| Section / # | Claim (brief) | Paper | Primary / recomputed | Primary file (script) | Status |
|---|---|---|---|---|---|
| §8.1 | Compliance under +vR; random control | 0.209 → 0.000; 0.642 | 0.209 → 0.000 (n 120); random 0.642 | `WS/inj2_q4b/inj2.json` | MATCH |
| §8.2 | Legitimate instruction | 0.79 → 1.00 | 0.791 → 1.000 | Same | MATCH |
| §8.3 | Steered replies on task | 24/24 | 24/24 topic word, 0/24 codeword | Same | MATCH |
| §8.4 | PASS on Qwen3-4B | PASS | GATE PASS (document placement eligible) | `WS/inj2_q4b_verdict.txt` | MATCH |

### §9 Fine-tuning fix

| Section / # | Claim (brief) | Paper | Primary / recomputed | Primary file (script) | Status |
|---|---|---|---|---|---|
| §9.1 | LoRA r 16; 8 non-financial domains; reminder every 3 rounds; "CHOICE:" | — | rank 16; 8 DOMAINS; REMIND_AT (0, 3, 6) | `WS/code/lora_train.py`, `sft_data.py` | MATCH |
| §9.2 | E1, n 240: drift without reminders; cells at floor | 0.857 → 0.03–0.06 | 0.8565 → 0.0319 / 0.0620; gF, oF ≤ 0.017 | `AR/binding_pilot/e_pilot.json` | MATCH |
| §9.3 | E2, n 16: own-trained vs given-trained gap | 0.009 vs 0.023 | 0.0090 vs 0.0229 | `e2.json` (`e2_analyze.py`) | MATCH |
| §9.4 | Shortcut, n 240 | +0.08 to +0.10 | own +0.1005, given +0.0759 | Same | MATCH |
| §9.5 | Every dose raises forged-assistant injection | +0.012 to +0.085 | +0.0122 to +0.0851, all p 5e-05 (E1 +0.055 / +0.054) | `e2.json`, `e_pilot.json` | MATCH |
| §9.6 | PREREG_E: own vs given gap; exact p | 0.0150 vs 0.0229 (−0.008), p 0.071 | 0.01497 vs 0.02286 (−0.0079), p 0.0714 | `e3.json` (`e3_analyze.py`) | MATCH |
| §9.7 | Shortcut present even at n 16 | — | own +0.117 (SHORTCUT); given +0.100 (UNCLEAR) | Same | MATCH |
| §9.8 | E4: own adapter removes drift without a shortcut; its given twin fails | 0.858 → 0.050 | own240b 0.0501 (swap −0.0015); given240b swap +0.0631 | `e4.json` (`e4_analyze.py`) | MATCH |
| §9.9 | PREREG_F no-reminder drift, own vs given | 0.206 vs 0.229 (p 0.64) | 0.2058 vs 0.2293, p 0.643 | `f.json` (`f_analyze.py`) | MATCH |
| §9.10 | Does not beat the untrained model with system reminders | 0.182 | Base gF 0.1818; seed-level +0.024 (p 0.10) | Same | MATCH |
| §9.11 | Shortcut | +0.072 | +0.0720 | Same | MATCH |
| §9.12 | Injection cost | +0.04 to +0.07 | given +0.0410, own +0.0650 | Same | MATCH |
| §9.13 | "Small fine-tunes of either kind cut no-reminder drift by about three quarters" | ~75% | n 240 (F) −76% / −73%; n 16 (E) about −20% (0.838 → 0.648 / 0.681); E4 n 48 −21% to −38% | `f.json`, `e3.json`, `e4.json` | **MISMATCH** [quantifier, minor] |
| §9.14 | Data seed moves drift within one arm | 0.08–0.35 | own 0.079–0.323; given 0.105–0.353 | `f.json` per_adapter | **MISMATCH** [numeric, minor] |
| §9.15 | The pilots shared one data seed | — | rc10 (E1), rc11 (E2) and rc13 (E4) call `lora_train.py` without `--seed0` (default 0) | `WS/cloud/rc10.sh`, `rc11.sh`, `rc13.sh` | MATCH |

### §10 Believe or obey

| Section / # | Claim (brief) | Paper | Primary / recomputed | Primary file (script) | Status |
|---|---|---|---|---|---|
| §10.1 | Repaired pilot fails calibration; validity r | r = 0.46 | Calibration fails at doses 1–3; r = 0.456 (< 0.5) | `AR/bo_pilot2/pilot2_results.json` | MATCH |
| §10.2 | First pilot confounded (goal drifted) | — | Bg0 (no counter-claims) p_hi 0.936 over 20 raw runs; the summary file is 0 bytes | `AR/bo_pilot/Bg0_s300–319.json` | MATCH |
| §10.3 | Repeating the fact sheet protects belief | — | p_believe_c none vs given: 0.248 / 0.115, 0.548 / 0.247, 0.785 / 0.396 | `pilot2_results.json` | MATCH |
| §10.4 | Own vs given changes belief ≤ 0.03, against +0.08 for obedience | ≤ 0.03; +0.08 | p_believe_c own − given −0.004 / +0.026 / +0.006; obey gap +0.081 (20/0) | Same | MATCH |

### Appended: Fix-test pilot (NO-GO)

| Section / # | Claim (brief) | Paper | Primary / recomputed | Primary file (script) | Status |
|---|---|---|---|---|---|
| Fix.1 | Transfer MD5 (pod ilrvy2lnddoirw) | 3499116f… | 3499116f7d203e1abbff84c093cb9bd8; host field names the pod | `WS/cloud_ci_pilot/results24p.tgz`, `transfer.json` | MATCH |
| Fix.2 | 20 raw/scored files; 180 prompts each; matched; 15 base tasks × 12 variants | — | 10 raw + 10 scored, 180 each; 15 × 12; keys identical across conditions | `AR/ci_pilot/out_np` | MATCH |
| Fix.3 | Qwen3-8B: plain; α 2; gain; emphasis | 8/180; 12/180; +2.22 pp; 13/180 | 8; 12; +2.22 pp; 13 | Scored files (`n_pilot.py`) | MATCH |
| Fix.4 | OLMo-2-7B: plain; α 2; gain; emphasis | 42/180; 42/180; 0; 43/180 | 42; 42; 0; 43 | Same | MATCH |
| Fix.5 | α 8 | 4/180 (Qwen); 6/180 (OLMo) | 4; 6 | Same | MATCH |
| Fix.6 | No setting meets the +3 pp gate → NO-GO | NO-GO | Max gain +2.22 pp; NO-GO | `n_pilot.py` | MATCH |

### Appended: Neutral-role decomposition diagnostic (NO-GO)

| Section / # | Claim (brief) | Paper | Primary / recomputed | Primary file (script) | Status |
|---|---|---|---|---|---|
| Dec.1 | Qwen3-1.7B, layer 13, 36 neutral sentences | 36 | layer 13; 36 sentences | `WS/decomposition_pilot_codex/extraction.json` | MATCH |
| Dec.2 | 2 base tasks × 12 variants; 8 utility controls per condition | — | Tasks 65, 66 × 12; 8 utility each | Condition JSONs | MATCH |
| Dec.3 | Vectors norm-matched | — | Max norm mismatch 9.5e-07 | `extraction.json`, `diagnostic_integrity_audit.json` | MATCH |
| Dec.4 | System successes (plain, emph, oldR2, user2, user4, orth2, pair2, random2); utility 8/8 | 4, 3, 3, 3, 4, 3, 4, 3 of 24 | Identical counts; utility 8/8 everywhere | Condition JSONs, `analysis.json` | MATCH |
| Dec.5 | No targeted condition beats plain; none meets the +10 pp gate | — | Max gain vs plain 0.0 | `analysis.json` | MATCH |
| Dec.6 | 256 outputs (192 conflict + 64 utility) | 256 | 8 × 24 + 8 × 8 | Condition JSONs | MATCH |
| Dec.7 | Plan and script hashes match the manifest | — | Plan 8880991…, script 3c3a682… match `manifest.json` | `WS/decomposition_pilot_codex` | MATCH |

### Outside requested scope (spot checks; not in the counts above)

| Section / # | Claim (brief) | Paper | Primary / recomputed | Primary file (script) | Status |
|---|---|---|---|---|---|
| X.1 | §12.3: "Preference stages do not add to it" (OLMo-2-7B) | — | Gap 0.063 → 0.071 → 0.077; step tests p 0.16 and 0.031 | `d_results.json` | **MISMATCH** [quantifier] |
| X.2 | §11, §12.4: 9 models, 4 families, 21/21 decided agree | 21/21 | As §6b.19 | `h.json`, `i.json` | MATCH |
| X.3 | Data section: $17.43 billing reading, 2026-10-27 21:50 AST | $17.43 | Appears only in the `PLAN_7DAY.md` log; no billing export among the primary files | — | UNVERIFIABLE |

## Addendum 2026-10-29: §6j–§6m and the source-monitoring abstract (Draft 8)

**Method.** An independent subagent checked about 193 numeric claims against `v0_analysis.json`, `v_analysis.json`, `w_analysis.json` and `x_analysis.json`. It also recomputed the main §6j, §6k and §6m values from the raw files, and re-ran `w_analyze.py`, which gave identical output.

**Result.** About 177 MATCH, 0 ROUNDING, 6 distinct MISMATCH, 1 UNVERIFIABLE (that the PREREG_T/S reproduction happened before sealing; the log says it did, at 20:20), and 8 overstatements. All were fixed in Draft 8.

**Mismatches:**
- "10 new models from 7 families" should be 6 (7 with PREREG_T's).
- "7 directions" should be 6 plus a random control.
- The pilot's random direction has own−tool's norm, not the recipe's.
- W3 "4 of 7 decided" should be 4 of 7 with a comparable pair (4 of 5 decided).
- The Qwen lag "about 0.2–0.25" should be 0.14–0.25.
- "Peaks at 0.5–0.8, where the lever acts" should be "6 of 8 peaks at 0.5–0.8; the lever is just below, at 0.45".

**Overstatements, now softened:**
- "each behaviour at its own depth";
- "lag shrinking with size" (it is not monotone);
- "8 of 9 rank differently" (8 of 9 are not unified; the rankings disagree in 7);
- "hold across seven families" (exceptions: Phi-4, Granite);
- Falcon "reverses it" (Phi-4's pairs also disagree);
- "Qwen models raise obedience" (significant only in Qwen3-1.7B);
- "a prompt can win the selectivity test" (it ties);
- SEP "carries over across families" (it beats the random control in 4 of 6).

## Addendum 2026-10-29 (b): §6g–§6i (PREREG_S, T and U; Paper B §3.1, §3.2 and §3.4)

**Why.** These sections were added after the Draft 6 recheck and fell outside the §6j–§6m addendum, so until now they had never been rechecked. The full report is `NUMBERS_RECHECK_STU.md`; the recompute scripts and outputs are in `recheck_stu/`.

**Method.** An independent subagent:
- verified all three seals (28/28) and bundles agp21–23;
- checked that the 20 raw result files are byte-identical to the pod archives;
- re-ran `s_analyze.py`, `t_analyze.py` and `u_analyze.py` on CPU, with output byte-identical to the stored JSON;
- recomputed `s_jspace.py`'s fractions without model weights (identical; still OUTSIDE);
- checked 97 claims against the primary files.

Claude spot-checked M1, O1 and O10 against the JSON (all confirmed).

**Result.** 92 MATCH, 1 ROUNDING, 4 MISMATCH and 0 UNVERIFIABLE, plus 12 overstatements. **No verdict changes.**

**Mismatches:**
- M1: the curve count is 14 of 16 informative curves, not 11 of 13; 8 of the 10 obey and believe curves.
- M2: "all edit effects ≤ 0.03" holds only for the sealed user→own ×1 edit. The reverse arm reaches 0.04 at ×1 and 0.09 at ×2.
- M3: names come from a fixed pool of 576, so they recur across tests (at least 72 shared S–T and S–U).
- M4: the S–U analyses live in `cloud_prereg_{s,t,u}/`, not in `cloud_*_analysis/`.

**Rounding.** Qwen3-8B believing tool output is 0.66, not 0.67.

**Overstatements, now softened:**
- O1: FRAGMENTED holds in 3 of 4 models (OLMo PARTIAL), and τ ≤ 0.2 in only 2.
- O2: attribution of 0.32 is above chance; "poorly reported", not "no reportable knowledge".
- O3: the transplant null holds only for the sealed direction at natural size.
- O4: Qwen3-1.7B's obedience does move (+0.01 and +0.03).
- O5: Qwen3-1.7B misses the READABLE rule (0.69 < 0.8).
- O6: OLMo own→usr is off by one token; patching all positions is within 10% there.
- O7: attribution "never" uses the content is wrong; it routes little.
- O8: "explains PREREG_S's null" is untested.
- O9: Qwen3-8B's −0.017 was significant.
- O10: the reported-only ×4 mean vector (M4) met all four sealed criteria in Qwen3-1.7B after the fact, and cut obedience by 0.113 in Qwen3-8B. It is now reported in §6i and in Paper B §3.4.
- O11: the splice is belief-selective in only 2 of 4 models.
- O12: the abstract's counts are for the 10 replication models.

All are fixed in `PAPER_DRAFT.md`, `PAPER_B_SOURCE_MONITORING.md` and `CONSOLIDATED_RESULTS.md`.

## Addendum 2026-10-29 (c): PREREG_Y (Paper B §3.8 and the full report's §6n)

The full report is `NUMBERS_RECHECK_Y.md`.

**Method.** An independent subagent:
- checked the agp30 seal (18/18 from a clean extract);
- re-ran `y_analyze.py`, with output byte-identical to the stored `y_analysis.json`;
- recomputed every rate from the raw files;
- checked 87 claims.

**Result.** 69 MATCH, 7 ROUNDING, 5 MISMATCH (3 distinct issues) and 6 UNVERIFIABLE (mostly pod-time costs). **No sealed verdict changes.**

**Mismatches, fixed:**
- "beats every prompt defence on both benchmarks only at 8B": Qwen3-14B also passes X2 and X4, and fails only X5.
- "all of them Qwen": true only for the 4 InjecAgent models; 3 of the 5 SEP models are not Qwen.
- The data sections omitted PREREG_Y.

**Overstatements, now softened:**
- "14B and 32B stayed effective" (14B is sealed NONE);
- "confirm the effect" (4 of 6 are at least effective);
- "the effect generalizes" (on InjecAgent it is mostly Qwen);
- "at 32B the effect is specific to the direction" (one random draw);
- the RNDCTL inference (a different setup);
- "Reading, fixed in advance" text that had not been fixed in advance.

**Added:**
- the preregistered size trend (InjecAgent margin over the best prompt: −0.38, −0.22, −0.18, −0.06);
- the fragility of Y1 (Qwen3-32B passes the SEP random control by one item in 300; the pass holds in about half of bootstrap reseeds).

**Costs.** Now labelled as pod-time figures awaiting reconciliation with billing.
