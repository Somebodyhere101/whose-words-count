# Write-up outline (G2, due 2026-11-02)

**Working title:** *Whose words count? A learned role direction sets how firmly language-model agents hold their goals*

**Rule for every claim:**
- each claim carries its status: PASS / FAIL / AMBIGUOUS / EXPLORATORY / REPLICATION OF PRIOR ART;
- numbers come only from the result files named in `CONSOLIDATED_RESULTS.md`;
- negative results stay in.

## Abstract (draft, to finalise last)

Agents keep their goals in text, and the same sentence can arrive as a system instruction, a user message or the agent's own note.

**Behaviour.** In a simulated portfolio manager under pressure, the identical goal reminder is followed less when it sits in the agent's own turn than in a system turn:
- preregistered in Qwen3-1.7B;
- the gap grows with scale to +0.144 at 32B;
- it is clear in OLMo-2-7B, weak in Granite-3.3-8B and reversed in SmolLM3-3B.

**Mechanism.** One role direction, taken from neutral sentences, causally moves adherence in both directions:
- strongly in Qwen3 1.7B–14B (one preregistered pass);
- with the same sign in three other families: one preregistered pass and two weak.

**What it is not.**
- No abstract "this is mine" representation exists.
- A pronoun-based account is refuted.

**Origin.** In the open OLMo-2 lineage the discount is present after supervised chat fine-tuning at 7B. The combined preregistered verdict is ambiguous, because the 13B gap is tiny. In OLMo-2-7B-Instruct the discount disappears when roles are written as plain-text labels.

**Prior art.** Injection-side uses of the direction replicate prior work.

**Capability (exploratory).** A small LoRA fine-tune removes goal drift on the held-out task, at a measurable cost in injection safety. It is reported with a shortcut control.

## Sections

1. **Introduction.** Goal drift in agents (Arike et al. 2025). Text authority by role: the instruction hierarchy (Wallace et al. 2024), role confusion (Ye et al. 2026). The question: is the same goal text weaker in the agent's own voice, and why?
2. **Instrument.** The fund-manager environment and the fast probability readout; cells 1/gF/oF/gN/oN/gW/oW/uF; batching; the context-window checks.
3. **Behaviour.**
   - Main 2×2 and run B (PREREG, PREREG_B: PASS).
   - Scale trend (EXPLORATORY).
   - Families: OLMo-2 (window-restricted, labelled), Granite, SmolLM3, and the uninformative small models.
4. **Representation.** The stage-2 probe gate FAILS in 9 models. Parallel finding: Leong 2026.
5. **Mechanism.**
   - Stage-3 PASS at 1.7B; the gate is met at 4B, 8B and 14B (EXPLORATORY gates); 32B is weak and distributed.
   - PREREG_C across families: 1 PASS, 2 present but weak, so strength is family-dependent and the sign is general.
6. **Origin.**
   - PREREG_D AMBIGUOUS: 7B H-SFT; 13B tiny and flat; the rule's missing minimum effect size is noted.
   - Plain-label pilot: the gap rides on the template's role tokens.
   - Authority order user > system > own in OLMo-2 (EXPLORATORY).
7. **Accounts that failed.** Deixis refuted (preregistered); addressee inconclusive; the three-model-agreement lesson.
8. **Injection.** Role steering blocks in-document injection (inj2 PASS), but this is a replication of Ye et al. and Steering Role Confusion.
9. **Capability (EXPLORATORY).**
   - The commitment-binding LoRA: E1 removes drift but hits the floor; the injection cost is +0.055.
   - E2: dose series and the shortcut test (pending). A sealed confirmation follows if E2 permits.
10. **Limitations.**
    - one task family; synthetic pressure;
    - Qwen-centred strength; sizes ≤ 32B;
    - an AI-run study with a non-specialist author: the AI-use statement;
    - the believe-or-obey scope test is unfinished (pilots only).
11. **What may be new, and what is not.** From `CONSOLIDATED_RESULTS.md` sections 6–7, updated.

**Appendices:** preregistration hashes, seeds, every deviation from `PLAN_7DAY.md`, the cost and runtime record (anchor calibration), code and data availability.
