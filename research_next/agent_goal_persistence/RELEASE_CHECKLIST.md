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
