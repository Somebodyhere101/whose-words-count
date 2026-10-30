# Release checklist: paper and code (PLAN_BIGGER Phase 4)

Prepared 2026-10-29. Nothing here is published until the user approves. Outreach stays on hold until the user says so.

## Needs the user

- [x] **Author name:** Sam Ramdan (ORCID 0009-0004-7723-4240), as on papers 3, 5 and 9. No affiliation is listed.
- [ ] **OK to publish:**
  - a Zenodo DOI (as for papers 3/5/9);
  - optionally arXiv (cs.LG or cs.CL; first-time submitters may need an endorsement).
- [ ] **OK to push a public GitHub repository** with the code and results.
- [ ] **OK for outreach**, emails to authors this work builds on. Suggested, not sent:
  - Zeng / Hockenmaier (V-Steer);
  - Zverev / Lampert (SEP, ASIDE);
  - Shilov / de Montjoye (TrustAttention);
  - Ye / Hadfield-Menell (role confusion).

## Claude can do once approved

- [ ] Remove the draft annotations and status notes from `PAPER_DRAFT.md`, and freeze it as v1.
- [ ] Build the release repository with this structure:
  - code: `code/`, `cloud/`;
  - sealed preregistrations with their `.sha256` files and bundles;
  - analyses: `cloud_*_analysis/`;
  - figures;
  - a README covering how to reproduce one sealed test from its bundle in about 15 minutes on one GPU, and the cost.
- [ ] License: the same as the earlier repositories (check papers 3/5/9).
- [ ] Zenodo metadata: title, abstract, keywords (prompt injection, source monitoring, activation patching, steering, chat roles), related identifiers (the earlier DOIs).
- [ ] A one-page summary with the two figures, for outreach.

## Open science items still to do before a v1 freeze

- [x] **Numbers recheck coverage: complete for every results section.**
  - Draft 6's Abstract, §2–§10 and the two interim notes: 168 claims, 2026-10-28.
  - §6j–§6m: about 193 claims, 2026-10-29.
  - §6g–§6i (PREREG_S, T, U; Paper B §3.1, §3.2, §3.4): 97 claims, 2026-10-29 (b). 4 mismatches and 12 overstatements were fixed, and no verdict changed.
  - An earlier version of this line wrongly said "§1–§6i" was done.
  - Still not separately rechecked: the new PREREG_Y results, when they arrive.
- [x] Split done 2026-10-29: `PAPER_B_SOURCE_MONITORING.md` (lead paper, about 6,300 words), `PAPER_A_GOAL_PERSISTENCE.md` (about 8,000 words), and `PAPER_DRAFT.md` kept as the full technical report.

## Decision 2026-10-29 (user): "Publish the papers, wait on the emails"

1. **Freeze** (no external action). A fresh-eyes consistency pass is running (`scratchpad/prepub_review.md`). Then: fix, remove draft notes, and hash v1.
2. **Packages** for Paper A and Paper B, as for paper 9: PDF (MiKTeX/LaTeX; pandoc is not installed), source zip, code-and-data zip with the sealed preregistrations, seals and bundles, CITATION.cff, METADATA.md with the approved AI-use statement, and MD5SUMS.
3. **Zenodo drafts** in the user's signed-in Chrome session, as two records cross-linked to each other. The user looks at them, then they are published, and ORCID picks them up through DataCite.
4. **GitHub repo:** the user's choice; the user creates it, and Claude pushes.
5. **Emails wait** for the user's signal. Drafts are prepared, not sent.

## Done 2026-10-29 14:06 +04:00

- **Published:** Paper A, doi:10.5281/zenodo.23758885 (https://zenodo.org/records/23758885); Paper B, doi:10.5281/zenodo.23758887 (https://zenodo.org/records/23758887).
- **Repository:** https://github.com/Somebodyhere101/whose-words-count, commit 33d2aeab. A fresh clone verifies all 27 seals.
- **Before release:** a consistency review and a sceptical skim were applied (`PREPUB_REVIEW.md`, `PREPUB_SKIM.md`, `PREPUB_FIXES_A.md`, `PREPUB_FIXES_B.md`). Paper B's title dropped "map-guided". Both papers now carry one cost figure ($95.37) and verified references.
- **Open:** the ORCID pickup check; outreach emails (on the user's signal); deleting network volume rt9jwj49za when the peer session no longer needs it.
- 2026-10-29 14:17 +04:00: ORCID pickup confirmed: both works are listed, added by DataCite, 11 works in total and no duplicates.

## Pending for v2 of Paper A, and now Paper B (publishing needs the user's OK)

- **AUTHPILOT** (peer session, 2026-10-29, exploratory; numbers checked against `cloud_authpilot/auth_analysis.json` on 2026-10-29 17:06 +04:00). v1 is not wrong: it calls the effect "a discount on another manager's plan", never a source tag. The new result says what that discount is in Qwen.
  - §6f, after the MPILOT paragraph, add: "**Second follow-up (EXPL., AUTHPILOT; Qwen3-8B and OLMo-2-7B-Instruct, 30 paired seeds; predictions from two AI systems hashed before launch).** When the plan is explicitly assigned ("which you have adopted as your binding objective", three paraphrases), the discount on another manager's plan vanishes in Qwen3-8B: +0.000 [−0.011, 0.013], against +0.126 [0.096, 0.161] without the assignment. By the rule written before launch, the discount in this model reflects whether the plan is the model's to carry out (applicability), not a lower authority for text from another author. Assigned conditions sit near ceiling (0.88–0.92), so a smaller discount could be masked, and no check confirmed how the model read the header. OLMo-2-7B keeps a small discount under assignment (+0.036 [0.029, 0.042], 29 of 30 seeds); no paired cross-model test was preregistered, so the model difference is untested. Framing the plan as background only did not remove the discount (+0.171 in Qwen, +0.094 in OLMo). Both forecasters had predicted that the discount would survive assignment in Qwen (0.64 and 0.55)."
  - Summary bullet (§1, "An exploratory follow-up in one model traces most of the difference to a discount on another manager's plan."): add "A second follow-up finds that this discount disappears in that model once the plan is explicitly assigned, which points to applicability rather than authorship."
  - Data section: add `AUTH_PRED.md` / `AUTH_PRED.sha256` to the hashed predictions, and `AUTH_RESULTS.md` and `cloud_authpilot/auth_analysis.json` to the results.
  - Cloud cost: keep $95.37 as the v1 figure and add AUTHPILOT (about $1.9; re-read the RunPod billing before release).
  - AI-use statement: a separate Claude session designed and ran AUTHPILOT, Codex and that session placed hashed bets, and this session checked the numbers against the analysis file.
  - Release mechanics: the sealed bundle is kept at `bundles/auth.tgz` (copied 2026-10-29, sha256 c19c6a44…, matching the seal). `AUTH_PRED.sha256` names it by a private scratchpad path, as `MPILOT_PRED.sha256` does for its bundle, so check how `verify_seals.py` handles that line. Then rebuild with `finalize_release.py`, push the repo, and publish a new Zenodo version of Paper A. (Paper B now also gets a v2 if the user agrees; see TAGSTYLE below.)
- **TAGSTYLE** (peer session, 2026-10-29, exploratory; rules in `TAGSTYLE.md`, written before data; outcome NONE by rule).
  - **Checked** on 2026-10-29 22:45 +04:00 against `cloud_tagstyle/ts_analysis.json`, with cell means recomputed from `cloud_tagstyle/out_ts/*/tagstyle.json`.
  - **Design:** Paper B's 60 obey and 60 believe items (PREREG_S/W kind, seed 2800); the statement in a system or a user turn × plain, policy register or casual register; 6 models. 4 are valid: OLMo-2-7B and SmolLM3 fail the attribution-mass check.
  - **Why it is owed:** v1 of both papers is not wrong, because every effect holds the wording fixed, and Paper A already contrasts its role-token result with Ye et al. But neither paper says how large role effects are next to wording, so a limitation is owed in both.
  - **Corrections to the peer's summary (do not carry these into the papers):**
    - "Perceived source follows style in 4 of 6" counts OLMo, whose attribution readout is INVALID. Among valid models it is 3 of 4, and only narrowly in phi-4 (S +0.586 vs T +0.557).
    - `TAGSTYLE_RESULTS.md` says "Unless marked n.s., p < 0.01", but Qwen3-1.7B believe S (+0.053) has p 0.039.
    - The pre-defined S compares two rewrites (policy vs casual), a bigger change than one tag switch. A plain-wording comparison depends on the turn:
      - In a system turn, a casual rewrite moves following more than the plain-wording tag effect does in 3 of 4 valid models.
      - In a user turn, the two are about equal for phi-4 obey (−0.135 vs +0.141) and Qwen3-8B belief (−0.193 vs +0.201).
      - So the text below uses the pre-defined T and S plus one example cell, and makes no ratio claims (the peer's "3–20 times").
  - **Paper A, §11 Limitations, new bullet after "One-axis generality":**
    ```
    - **Wording can outweigh role (EXPL., TAGSTYLE).** Every role effect in this paper holds the wording of the text fixed.
      - An exploratory pilot on Paper B's 60 obey and 60 believe items varied both (six models, four with valid readouts). The register effect (the same statement phrased as a policy rather than casually, averaged over turns) was larger than the role effect (a system rather than a user turn, averaged over wordings) for both following and belief in three of the four valid models. Qwen3-1.7B was the exception.
      - Example: Qwen3-8B followed a system-turn instruction 0.48 as written, 0.79 when phrased as a policy and 0.04 when phrased casually. Averaged over wordings, a system rather than a user turn changed its following by −0.02 (n.s.).
      - Asked which message a sentence came from, three of the four valid models also went more by register than by role (narrowly in phi-4), in line with Ye et al. (2026). Qwen3-8B went more by role.
      - The registers carry cue words ("Required response", "lol"), so the pilot cannot separate style from credibility or authority cues. Its rule, fixed before data, needed one pattern in at least four valid models and gave no outcome (NONE), so these readings are descriptive.
    ```
  - **Paper B, §6 Limitations, new bullet after the first one (synthetic items):**
    ```
    - **The source contrasts hold the wording fixed, and wording can matter more (EXPL., TAGSTYLE).**
      - Every item pair in §3 differs only in the role tag. An exploratory pilot on the same 60 obey and 60 believe items also varied the register (six models, four with valid readouts).
      - The register effect (the same statement phrased as a policy rather than casually, averaged over turns) was larger than the tag effect (a system rather than a user turn, averaged over wordings) for both obeying and believing in three of the four valid models. Qwen3-1.7B was the exception. In Qwen3-8B, a system-turn instruction was followed 0.48 as written, 0.79 as a policy and 0.04 when phrased casually.
      - Attribution also went more by register than by tag in three of the four (narrowly in phi-4; Qwen3-8B went more by tag). This is in line with Ye et al. (2026), whose probes find that role perception follows style rather than tags.
      - The registers carry cue words ("Required response", "lol"), so style is not separated from credibility cues. The pilot's rule, fixed before data, gave no outcome (NONE), so these readings are descriptive.
    ```
  - **Paper B References:** add "Ye, C., Cui, J., and Hadfield-Menell, D. 2026. Prompt Injection as Role Confusion. *ICML 2026*, PMLR 306: 148172–148202. arXiv:2603.12277." This is copied from Paper A's list and verified in `REFERENCES_VERIFIED.md`, item 5.
  - **Not recommended:** a summary-line change. The pilot is exploratory, its rule gave NONE, and register is confounded with cue words, so a limitation is the proportionate place (L3).
  - **Data sections (both papers):** add `TAGSTYLE.md`, `TAGSTYLE_RESULTS.md`, `cloud_tagstyle/ts_analysis.json` and `cloud_tagstyle/out_ts/`.
  - **Cost:** about $0.25 (the peer's figure; re-read billing before release).
  - **AI-use statements:** a separate Claude session designed and ran TAGSTYLE, and this session checked the numbers.
- **REVPILOT** (peer session, 2026-10-29, exploratory; three pilots; checked against `REVPILOT_RESULTS.md` and `cloud_revpilot3/rev_pilot3.json`). Optional, for Paper A only.
  - **Why it fits:** "One-axis generality" says the axis has only been shown to match the one order every model shares. REVPILOT tried to train a different order and could not.
  - **Paper A, §11, as a sub-bullet of "One-axis generality":**
    ```
      - An exploratory attempt to train a different order did not change it (REVPILOT; Qwen3-8B and OLMo-2-7B; LoRA training on system-versus-user priority conflicts outside the fund task, two data seeds per arm, three pilots). The first two pilots taught shortcuts: resisting pressure, then keeping the first or the latest instruction. In the third, with the order balanced, the two arms did not differ in the system-minus-user gap in goal following (difference between arms: +0.004 in Qwen, +0.024 in OLMo), while data seeds within an arm differed by up to 0.12. A user-turn reminder was still followed more than a system-turn one in every adapter of pilots 2 and 3. A model with a different order, the test the axis needs, is still missing.
    ```
  - **Data section:** add `REVPILOT.md`, `REVPILOT_RESULTS.md` and `cloud_revpilot*/`.
  - **Cost:** about $3.8 (the peer's figure; re-read billing before release).
- **Timing (recommended):** one batch (A v2, and B v2 for TAGSTYLE) before the outreach emails, with any further results from the peer session.
