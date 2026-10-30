# Reference verification for PAPER_DRAFT.md (Draft 6)

Checked 2026-10-28. `PAPER_DRAFT.md` was not edited. Line numbers below refer to it as of today.

**How each record was checked**
- arXiv entries: the arXiv API (export.arxiv.org) for title, authors, versions, comments and journal-ref. Where an in-text claim depends on the body of a paper, the arXiv HTML full text was searched.
- DOIs, volumes and pages: Crossref.
- LessWrong post: the LessWrong GraphQL API (byline, date, text).
- Venue checks: neurips.cc (including the NeurIPS 2026 poster/oral data file), icml.cc, iclr.cc, cvpr.thecvf.com, ojs.aaai.org, proceedings.mlr.press, transformer-circuits.pub and anthropic.com.
- Sites I could not open:
  - OpenReview: browser challenge;
  - PubMed: reCAPTCHA;
  - DBLP: bot check;
  - CVF Open Access: HTTP 403;
  - Semantic Scholar: rate limit.

  I did not try to get past any of these checks. The three OpenReview-only papers were confirmed through their official NeurIPS 2026 pages, which link the OpenReview IDs.

**Status rules**
- **VERIFIED:** everything the draft (or the request) states is correct. "(completed)" means fields the draft left out were filled from the record.
- **CORRECTED:** something stated was wrong or truncated (title, authors, venue or year). The note says exactly what changed.
- **UNVERIFIED:** no primary record was found.

**Conventions in the clean list**
- **Authors:** all of them if there are three or fewer; otherwise the first author followed by "et al."
- **Year:** the year of the published version that is cited (conference or journal); for arXiv-only works, the year of arXiv v1.

**Counts:** 32 distinct works. That is 24 in the draft's list plus 8 newly cited ones; "Steering Role Confusion" and "Reducing Role Confusion via Activation Steering" are on both lists and counted once.
- VERIFIED: 22
- CORRECTED: 10
- UNVERIFIED: 0

---

## 1. Status table

| # | Entry (as given) | Status | Note |
|---|---|---|---|
| 1 | Zeng, Lee, Zhao & Hockenmaier 2026, Steering Instruction Hierarchies at Inference Time, COLM 2026, arXiv 2607.26228 | VERIFIED | The title, the 4 authors (Siqi Zeng, Sewoong Lee, Han Zhao, Julia Hockenmaier) and COLM 2026 all match; the arXiv comment reads "Published as a conference paper at COLM '26". The in-text claim at line 491 (a training-free intervention that edits cached value vectors at heads selected by attribution) matches the abstract. |
| 2 | Balp-Straffon et al. 2026, How Language Models Choose Sides: Internal Representations of Instruction Hierarchy, arXiv 2608.28648 | VERIFIED | All 6 authors and the ICML 2026 Mechanistic Interpretability workshop match. The in-text claim at line 492 is supported: directions chosen for separability steer poorly, so steering depends on how the readout is shaped, not on probe accuracy. |
| 3 | Arike et al. 2025: goal drift in language-model agents | VERIFIED (completed) | Published as "Evaluating Goal Drift in Language Model Agents", AIES 2025, Proc. AIES 8(1):192–203, doi:10.1609/aies.v8i1.36541 (Crossref). Authors: Arike, Donoway, Bartsch, Hobbhahn. On arXiv (2505.02709) the title begins "Technical Report:". See §4 N1: §2 uses this paper's environment without saying so. |
| 4 | Wallace et al. 2024: The Instruction Hierarchy | CORRECTED | The title was truncated. Full title: "The Instruction Hierarchy: Training LLMs to Prioritize Privileged Instructions". Added arXiv 2404.13208 (no venue). |
| 5 | Ye, Cui & Hadfield-Menell 2026: Prompt Injection as Role Confusion (ICML; arXiv 2603.12277) | VERIFIED | ICML 2026, PMLR 306:148172–148202 (arXiv journal-ref). Three in-text claims about its content are wrong or unsupported (§3, W1–W3). The Appendix K claim at line 493 is supported (§4 N6). |
| 6 | Steering Role Confusion (LessWrong, 2026); also on the new list as Zhang, Lee, Park, Aug 2026 | VERIFIED (completed) | The byline is Kevin Zhang, Daniel Lee and Jaewoo Park, as reported; posted 20 Aug 2026 (LessWrong API). URL added. The post steers gpt-oss-20b along a user-vs-tool difference of means; steering toward "tool" brings attack success close to 0. |
| 7 | Reducing Role Confusion via Activation Steering (NeurIPS 2026); also on the new list as Liu, OpenReview aJceCDuUjM | CORRECTED | Single author: Ethan Liu. **The venue is a NeurIPS 2026 workshop, not the main conference:** it is a poster in "The Third Workshop on Agents in the Wild: Safety, Security, and Beyond" (neurips.cc/virtual/2026/168203, which links OpenReview aJceCDuUjM). No main-track NeurIPS 2026 title contains "role confusion". |
| 8 | Chen et al. 2026: The Self-Correction Illusion (arXiv 2606.05976) | CORRECTED | The title was truncated. Added ": Role Relabeling Gates Explicit Error Flagging in Large Language Models". First author Kuan-Yen Chen (5 authors). arXiv only. |
| 9 | Tsui 2025: Self-Correction Bench (arXiv 2507.02778) | CORRECTED | Full title: "Self-Correction Bench: Uncovering and Addressing the Self-Correction Blind Spot in Large Language Models". Venue added: COLM 2026 (arXiv comment "Accepted to COLM 2026"). Under the year rule the year becomes 2026 (arXiv v1 is from 2025). Not cited in the text; see §4 N2. |
| 10 | Leong 2026: Instruction Self-Arbitration Is Not a Trust Boundary (arXiv 2608.28502) | CORRECTED | The title was truncated. The v2 title (17 Oct 2026) adds ": Configuration-Dependent Tool Calls and External Enforcement in LLM Agents". Author: Jun Wen Leong. v1 (28 Aug 2026) was titled "Recognition Without Enforcement: Configuration-Dependent Failures in LLM Agent Instruction Arbitration and External Control". In-text claims are overstated (§3, W5–W6). |
| 11 | Arditi et al. 2024: refusal is mediated by a single direction | VERIFIED (completed) | "Refusal in Language Models Is Mediated by a Single Direction", NeurIPS 2024 (Advances in NeurIPS 37, 136037–136083; Crossref), arXiv 2406.11717. Not cited in the text; see §4 N2. |
| 12 | Xu & Daneshjou 2026: sycophantic follow-through across post-training stages (NeurIPS 2026) | CORRECTED | **Real record:** "Behaving Better, Thinking Worse: Sycophancy Across Post-Training Stages", NeurIPS 2026 poster, OpenReview IUAXqLsMTC (neurips.cc/virtual/2026/poster/153819). Not on arXiv.<br>**Authors:** Sonnet Xu, Kritika Singh, Sheharbano Jafry, Roxana Daneshjou and Sanmi Koyejo, so the citation is "Xu et al.", not "Xu & Daneshjou".<br>**Description:** the abstract does not mention "follow-through". It studies factual sycophancy and finds that after post-training, flip rates fall while log-probability shifts rise.<br>Not cited in the text. |
| 13 | Menon et al. 2026: inherited goal drift | VERIFIED (completed) | "Inherited Goal Drift: Contextual Pressure Can Undermine Agentic Goals", arXiv 2603.03258, ICLR 2026 Lifelong Agents Workshop (6 authors). It uses Arike et al.'s stock-trading environment. Not cited in the text. |
| 14 | Penman 2026: Semantic Overlays… (arXiv 2608.23873) | VERIFIED | The title and author (Joshua Penman) match. arXiv only (v3). The in-text "nearly eliminates" is overstated (§3, W7). |
| 15 | Lu et al. 2025: ARGUS… (arXiv 2512.05745) | CORRECTED | Venue added: CVPR 2026 main conference, oral (cvpr.thecvf.com/virtual/2026/oral/40371). The year becomes 2026 for the CVPR version, so the in-text "ARGUS 2025" should become "Lu et al. 2026". Pages are not confirmed because the CVF page returned 403. |
| 16 | Stolfo et al. 2025 (ICLR; arXiv 2410.12877) | VERIFIED | ICLR 2025 poster (iclr.cc/virtual/2025/poster/27819). The in-text description ("instruction-specific vectors") matches. |
| 17 | Neural Procedural Memory… (arXiv 2606.29824) | VERIFIED (completed) | Authors added: Chengfeng Zhao et al. (6), 2026, arXiv only. The in-text description (skills stored as steering vectors) matches. |
| 18 | Remember When It Matters… (arXiv 2607.08716) | VERIFIED (completed) | Authors added: Yifan Wu et al. (8), 2026, arXiv only. The paper's own term is "behavioral state decay". |
| 19 | Geng et al. 2026: Control Illusion… (AAAI; arXiv 2502.15851) | VERIFIED | AAAI-26: Proc. AAAI 40(36):30816–30824, doi:10.1609/aaai.v40i36.40339 (Crossref). Checked in HTML v4: the six models (Qwen-7B, Llama-8B, Llama-70B, Claude 3.5 Sonnet, GPT-4o-mini, GPT-4o) and the step that removes conflict acknowledgements before scoring (cited at line 415). The GitHub URL resolves. |
| 20 | Zeng 2025: Who is In Charge?… (arXiv 2510.01228) | VERIFIED | Single author Siqi Zeng, the same person who is first author of entry 1. Venue: NeurIPS 2025 Mechanistic Interpretability Workshop, poster. One in-text sentence is imprecise (§3, W8). |
| 21 | Reasoning Up the Instruction Ladder… (ACL Findings 2026 / ICML 2026) | CORRECTED | Authors added: Zishuo Zheng et al. (5).<br>Venue: Findings of ACL 2026, 39332–39354, doi:10.18653/v1/2026.findings-acl.1960; arXiv 2511.04694.<br>**Drop "/ ICML 2026":** at ICML 2026 it is only a workshop poster (Trustworthy AI for Good Workshop, icml.cc/virtual/2026/76907).<br>The abstract has now been read; its "~20% absolute improvement in conflict setups" supports the number at line 485. |
| 22 | Wang, Jiang, Yu & Huang 2025: The Illusion of Role Separation… (ICML; arXiv 2505.00626) | CORRECTED | The title lacks its ending, "(and How to Fix Them)". ICML 2025, PMLR 267:63200–63210. The in-text claim at line 486 matches. |
| 23 | Joswin, Medicherla & Mammen 2026 (arXiv 2607.00415) | VERIFIED | Title and authors match. The draft's note says only the abstract was read. Two in-text details at line 487 come from the body (RQ4), not the abstract: the effect is entangled with question content, and the mean authority vector has a negligible effect. The body supports both. |
| 24 | Maczan 2026 (arXiv 2609.25021) | VERIFIED | Author: Jędrzej Maczan. Venue added: accepted to the COLM 2026 Workshop on Efficient Reasoning and to the KONVENS 2026 Eval4SD workshop. The claim at line 488 matches the abstract. |
| 25 | NEW: arXiv 2605.12991, "Not Just RLHF…" | VERIFIED | "Not Just RLHF: Why Alignment Alone Won't Fix Multi-Agent Sycophancy", Adarsh Kumarappan and Ananya Mujoo, 2026 (v3, Aug 2026), arXiv only. The patching swaps the clean run's residual-stream hidden state into the pressured run, layer by layer (window L14–L18). |
| 26 | NEW: Leong et al., arXiv 2502.13946 | VERIFIED | "Why Safeguarded Ships Run Aground? Aligned Large Language Models' Safety Mechanisms Tend to Be Anchored in The Template Region", Chak Tou Leong et al. (4), ACL 2025 (Long), 15212–15229, doi:10.18653/v1/2025.acl-long.738.<br>It patches value states from harmless into harmful inputs, region by region (template versus instruction), and scores compliance (Fig. 4, §3.3).<br>The author is not the J. W. Leong of entry 10. |
| 27 | NEW: G. & Lindsey, arXiv 2605.25459 | VERIFIED | "From Simulation to Enaction: Post-trained language models recognize and react to their own generations", Asvin G. and Jack Lindsey, 2026 (an Anthropic Fellows project), arXiv only. KV patching at the user-token positions for explicit prefill detection is in §3.3, Fig. 15. |
| 28 | NEW: Ackerman & Panickssery, arXiv 2410.02064 | VERIFIED | "Inspection and Control of Self-Generated-Text Recognition Ability in Llama3-8b-Instruct", ICLR 2025 (iclr.cc poster 27838). It finds a residual-stream vector tied to self-authorship; steering with it makes the model claim or disclaim authorship. |
| 29 | NEW: TrustAttention (Shilov … de Montjoye; NeurIPS 2026; OpenReview GPritQr2Ve) | CORRECTED | **Title:** "Separating instructions from data as an attention problem". TrustAttention is the method's name, not the title.<br>**Authors:** Igor Shilov, Xiaoxue Yang, Alexander Panfilov, Matthieu Meeus, Peter Romov, Jonas Geiping, Yves-Alexandre de Montjoye.<br>**Venue:** a poster at the same NeurIPS 2026 workshop as entry 7, not the main conference.<br>The OpenReview ID is confirmed on neurips.cc/virtual/2026/168253. See §4 N4. |
| 30 | NEW: DRIP, arXiv 2511.00447 | VERIFIED | Current (v2) title: "DRIP: Defending Prompt Injection via Token-wise Representation Editing and Residual Instruction Fusion". v1 was titled "…via De-instruction Training and Residual Fusion Model Architecture". Ruofan Liu et al. (4), 2025. No venue found. |
| 31 | NEW: Johnson, Hashtroudi & Lindsay 1993, "Source monitoring", Psychological Bulletin | VERIFIED | Psychological Bulletin 114(1):3–28, doi:10.1037/0033-2909.114.1.3 (Crossref). |
| 32 | NEW: Anthropic's July 2026 J-space / Jacobian lens paper | VERIFIED | **Title:** "Verbalizable Representations Form a Global Workspace in Language Models". Wes Gurnee, Nicholas Sofroniew, … Jack Lindsey (16 authors), Transformer Circuits Thread, 6 July 2026.<br>**URL:** https://transformer-circuits.pub/2026/workspace/index.html<br>The paper defines the Jacobian lens (J-lens) and the J-space. Anthropic's companion post is "A global workspace in language models" (https://www.anthropic.com/research/global-workspace). |

---

## 2. Clean reference list (alphabetized, ready to paste)

- Ackerman, C., and Panickssery, N. 2025. Inspection and Control of Self-Generated-Text Recognition Ability in Llama3-8b-Instruct. *ICLR 2025*. arXiv:2410.02064.
- Arditi, A., et al. 2024. Refusal in Language Models Is Mediated by a Single Direction. *Advances in Neural Information Processing Systems 37 (NeurIPS 2024)*, 136037–136083. arXiv:2406.11717.
- Arike, R., et al. 2025. Evaluating Goal Drift in Language Model Agents. *Proceedings of the AAAI/ACM Conference on AI, Ethics, and Society (AIES 2025)* 8(1): 192–203. doi:10.1609/aies.v8i1.36541. arXiv:2505.02709.
- Balp-Straffon, E., et al. 2026. How Language Models Choose Sides: Internal Representations of Instruction Hierarchy. *ICML 2026 Mechanistic Interpretability Workshop*. arXiv:2608.28648.
- Chen, K.-Y., et al. 2026. The Self-Correction Illusion: Role Relabeling Gates Explicit Error Flagging in Large Language Models. *arXiv preprint*. arXiv:2606.05976.
- G., A., and Lindsey, J. 2026. From Simulation to Enaction: Post-trained language models recognize and react to their own generations. *arXiv preprint*. arXiv:2605.25459.
- Geng, Y., et al. 2026. Control Illusion: The Failure of Instruction Hierarchies in Large Language Models. *Proceedings of the AAAI Conference on Artificial Intelligence (AAAI-26)* 40(36): 30816–30824. doi:10.1609/aaai.v40i36.40339. arXiv:2502.15851.
- Gurnee, W., et al. 2026. Verbalizable Representations Form a Global Workspace in Language Models. *Transformer Circuits Thread* (Anthropic), 6 July 2026. https://transformer-circuits.pub/2026/workspace/index.html
- Johnson, M. K., Hashtroudi, S., and Lindsay, D. S. 1993. Source monitoring. *Psychological Bulletin* 114(1): 3–28. doi:10.1037/0033-2909.114.1.3.
- Joswin, E., Medicherla, S., and Mammen, P. M. 2026. A Mechanistic View of Authority Hierarchy in LLM Sycophancy. *arXiv preprint*. arXiv:2607.00415.
- Kumarappan, A., and Mujoo, A. 2026. Not Just RLHF: Why Alignment Alone Won't Fix Multi-Agent Sycophancy. *arXiv preprint*. arXiv:2605.12991.
- Leong, C. T., et al. 2025. Why Safeguarded Ships Run Aground? Aligned Large Language Models' Safety Mechanisms Tend to Be Anchored in The Template Region. *Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (ACL 2025), Volume 1: Long Papers*, 15212–15229. doi:10.18653/v1/2025.acl-long.738. arXiv:2502.13946.
- Leong, J. W. 2026. Instruction Self-Arbitration Is Not a Trust Boundary: Configuration-Dependent Tool Calls and External Enforcement in LLM Agents. *arXiv preprint* (v2, 17 October 2026). arXiv:2608.28502.
- Liu, E. 2026. Reducing Role Confusion via Activation Steering. *NeurIPS 2026 Workshop: The Third Workshop on Agents in the Wild: Safety, Security, and Beyond*. https://openreview.net/forum?id=aJceCDuUjM
- Liu, R., et al. 2025. DRIP: Defending Prompt Injection via Token-wise Representation Editing and Residual Instruction Fusion. *arXiv preprint*. arXiv:2511.00447.
- Lu, W., et al. 2026. ARGUS: Defending Against Multimodal Indirect Prompt Injection via Steering Instruction-Following Behavior. *CVPR 2026*. arXiv:2512.05745.
- Maczan, J. 2026. "As a Language Model...": Chat Template Switches LLM Self-Referential Voice and Activation Steering Reproduces It. *COLM 2026 Workshop on Efficient Reasoning; KONVENS 2026 Workshop on Evaluating LLMs for Specialized Domains (Eval4SD)*. arXiv:2609.25021.
- Menon, A., et al. 2026. Inherited Goal Drift: Contextual Pressure Can Undermine Agentic Goals. *ICLR 2026 Lifelong Agents Workshop*. arXiv:2603.03258.
- Penman, J. 2026. Semantic Overlays: Mitigating Prompt Injection with Annotations Beyond Tokens and Steering Vectors. *arXiv preprint*. arXiv:2608.23873.
- Shilov, I., et al. 2026. Separating instructions from data as an attention problem. *NeurIPS 2026 Workshop: The Third Workshop on Agents in the Wild: Safety, Security, and Beyond*. https://openreview.net/forum?id=GPritQr2Ve
- Stolfo, A., et al. 2025. Improving Instruction-Following in Language Models through Activation Steering. *ICLR 2025*. arXiv:2410.12877.
- Tsui, K. 2026. Self-Correction Bench: Uncovering and Addressing the Self-Correction Blind Spot in Large Language Models. *COLM 2026*. arXiv:2507.02778.
- Wallace, E., et al. 2024. The Instruction Hierarchy: Training LLMs to Prioritize Privileged Instructions. *arXiv preprint*. arXiv:2404.13208.
- Wang, Z., et al. 2025. The Illusion of Role Separation: Hidden Shortcuts in LLM Role Learning (and How to Fix Them). *ICML 2025*, PMLR 267: 63200–63210. arXiv:2505.00626.
- Wu, Y., et al. 2026. Remember When It Matters: Proactive Memory Agent for Long-Horizon Agents. *arXiv preprint*. arXiv:2607.08716.
- Xu, S., et al. 2026. Behaving Better, Thinking Worse: Sycophancy Across Post-Training Stages. *NeurIPS 2026*. https://openreview.net/forum?id=IUAXqLsMTC
- Ye, C., Cui, J., and Hadfield-Menell, D. 2026. Prompt Injection as Role Confusion. *ICML 2026*, PMLR 306: 148172–148202. arXiv:2603.12277.
- Zeng, S. 2025. Who is In Charge? Dissecting Role Conflicts in Instruction Following. *NeurIPS 2025 Mechanistic Interpretability Workshop*. arXiv:2510.01228.
- Zeng, S., et al. 2026. Steering Instruction Hierarchies at Inference Time. *COLM 2026*. arXiv:2607.26228.
- Zhang, K., Lee, D., and Park, J. 2026. Steering Role Confusion. *LessWrong*, 20 August 2026. https://www.lesswrong.com/posts/uz9pFutDAT7trygM9/steering-role-confusion
- Zhao, C., et al. 2026. Neural Procedural Memory: Empowering LLM Agents with Implicit Activation Steering. *arXiv preprint*. arXiv:2606.29824.
- Zheng, Z., et al. 2026. Reasoning Up the Instruction Ladder for Controllable Language Models. *Findings of the Association for Computational Linguistics: ACL 2026*, 39332–39354. doi:10.18653/v1/2026.findings-acl.1960. arXiv:2511.04694.

---

## 3. In-text claims found wrong or unsupported

Ordered by severity. Source quotes are kept short; everything else is paraphrased.

**W1. Ye et al. do not find that role is judged from format (§6 Pilots, line 198). Wrong.**
- **Draft:** "The discount rides on the template's role tokens. This fits Ye et al.'s finding that role is judged from format."
- **Source:** Ye et al. (arXiv v6), Fig. 7 caption: "Role perception is determined by style, not tags." Fig. 11 adds that inserting system tags "has no effect on model perception".
- **Problem:** Ye et al. find that role tags matter little next to style and position. A discount that depends on the template's role tokens therefore does not fit their result. At most it is a contrast, and the measures differ: they probe internal role perception, while this draft measures a behavioural discount.
- **Suggested fix:** "Unlike Ye et al., who find that role perception follows style and position rather than tags, the behavioural discount here depends on the template's role tokens."

**W2. "Decided by format" misstates Ye et al. (§1, line 61). Misleading.**
- **Draft:** "show that role confusion drives prompt injection and is decided by format."
- **Source:** Ye et al., abstract: models perceive a text's source "from how it sounds, not its labeled role".
- **Problem:** Line 198 uses "format" to mean the template's role tokens, which is the opposite of this finding.
- **Suggested fix:** "…and that models infer a text's role from how it sounds rather than from its role tag."

**W3. Ye et al. contain no steering experiment, so §8's result does not replicate them (§8, line 366; also line 465). Unsupported.**
- **Draft:** "This replicates Ye, Cui & Hadfield-Menell (2026) and 'Steering Role Confusion' (2026)". Line 465 reads "…and steering it (Ye et al.; …)".
- **Source:** Ye et al. v6 has no activation-steering experiment. The only steering text is Appendix L.1, "Subconscious Steering", which the authors call "speculative and not empirically validated in this work". The LessWrong post describes Ye et al.'s evidence as probe correlations and adds the steering itself.
- **Problem:** The steering precedents are:
  - Zhang, Lee & Park (2026): steering toward "tool" "decreases the attack success rate to nearly 0";
  - Liu (2026): "Role Steering decreases prompt injection attack success".

  Ye et al. supply the role-confusion account and the probes.
- **Suggested fix:** "This replicates the steering results of Zhang, Lee & Park (2026) and Liu (2026), which build on Ye et al.'s role-confusion account."

**W4. Liu (2026) is a workshop paper (lines 61 and 465). Wrong venue.**
- **Draft:** "'Reducing Role Confusion via Activation Steering', NeurIPS 2026" and "(Ye et al.; Steering Role Confusion; NeurIPS 2026)".
- **Source:** neurips.cc lists it as a poster in "The Third Workshop on Agents in the Wild: Safety, Security, and Beyond". It is not in the main track.
- **Suggested fix:** "Liu (2026; NeurIPS 2026 workshop)".

**W5. Leong v2 does not report that no abstract provenance representation exists (lines 61, 138 and 466). Overstated.**
- **Draft:**
  - line 61: "Leong (2026) finds no abstract provenance representation."
  - line 138: "reports source-format cues that are linearly decodable but no abstract provenance representation, so this negative result is not new on its own."
  - line 466: "no abstract provenance code (Leong 2026, v2)".
- **Source:** In v2 the pre-specified crossed-probe test "halted and gives no interpretable evidence of an abstract provenance representation" (abstract). The body calls this "a halt, not a demonstration of absence". The stronger wording, that crossed-probe controls show there is no unified abstract trust representation, was in v1, and v2 narrowed it.
- **Problem:** v2 finds no interpretable evidence either way. That also weakens §4's statement that the draft's own negative result "is not new on its own".
- **Suggested fix:** "Leong (2026, v2) finds source-format cues linearly decodable; its pre-specified test for an abstract provenance representation halted without interpretable evidence either way."

**W6. Leong's 0/1,895 steering null is narrower than "did not change behaviour" (line 467). Overstated.**
- **Draft:** "its v2 also reports that steering a provenance direction did not change behaviour (0/1,895), which contrasts with our role direction".
- **Source:** Leong v2, abstract: steering "did not move tool mention (0 of 1,895 trials, mention-scored)". The body says this scoring "cannot certify the absence of an execution-to-refusal effect". It also says the null on Qwen2.5-32B cannot be interpreted, and that the causal role of provenance in execution remains open. The steered direction is the "source-format direction".
- **Suggested fix:** "steering along its source-format direction did not move tool-name mention (0/1,895, mention-scored; the author notes this cannot rule out an effect on execution)". The contrast with the draft's role direction should be softened to match.

**W7. Penman (2026) does not nearly eliminate injection on all five benchmarks (line 472). Overstated relative to the source.**
- **Draft:** "nearly eliminates injection on five benchmarks".
- **Source:** Penman (2026), abstract and §7. The five benchmarks are SEP, TensorTrust, PIArena, AlpacaFarm and Quadrat-IPI. The abstract reports:
  - SEP separation rising from 24.3% to 99.0%;
  - TensorTrust attack success falling from 34.8% to 6.2%;
  - AlpacaFarm attack success falling from 99.0% to 0%;
  - on PIArena, beating every published defence that leaves the model able to answer.

  The abstract gives no Quadrat-IPI figure.
- **Suggested fix:** "strongly reduces injection on five benchmarks (e.g., AlpacaFarm 99.0% to 0%, TensorTrust 34.8% to 6.2%)".

**W8. Zeng (2025) gets the distinct-subspace finding from probes alone (line 481). Imprecise; minor.**
- **Draft:** "Linear probes, direct logit attribution and steering show that system–user conflicts and social-cue conflicts occupy distinct subspaces."
- **Source:** Zeng (2025), abstract. Linear probing shows system–user and social conflicts "forming distinct subspaces". Direct logit attribution shows stronger conflict detection for system–user conflicts but consistent resolution only for social cues. Steering with social-cue vectors amplifies instruction following regardless of role. The abstract presents the claim at line 482 (models obey social cues while ignoring the hierarchy) as earlier behavioural work, which Zeng extends.
- **Suggested fix:** attribute each finding to its own method.

**W9. Control Illusion says "stronger", not "far more" (line 478). Minor.**
- **Draft:** "social framings (authority, expertise, consensus) shift priority far more than roles do."
- **Source:** Geng et al., abstract: these framings "show stronger influence on model behavior than system/user roles".
- **Suggested fix:** "far more" is not in the source. Check it against their societal-hierarchy results, or write "more strongly".

The other in-text claims about cited papers matched the abstract or full text. These are the claims at lines 48–49, 61 (Chen et al.), 138 (decodability part), 289, 415, 469–470, 474–475, 477, 479, 485–488 and 491–493.

---

## 4. Other findings (not errors in a cited claim)

- **N1. §2 does not credit the environment's source (line 68).** The fund-manager environment comes from Arike et al.: §3.1 of their paper places the agent as portfolio manager at "Apex Capital", with a system goal to minimise the carbon emissions caused by the portfolio's companies, under email and news pressure. Cite Arike et al. in §2, not only in §1. Menon et al. (2026) use the same environment.
- **N2. Four entries in the list are never cited in the text:** Tsui, Arditi et al., Xu et al. and Menon et al. Either cite them or remove them. Two have natural places:
  - **Arditi et al., in §6d:** removing a unit direction from every layer is their directional ablation.
  - **Tsui (2026), in §12:** it reports "a transferable conversational-role direction in representation space that causally gates self-correction". That is a close precedent for candidate contribution 1, and §12 does not discuss it.
- **N3. In-text labels to change when switching to author–year:**
  - "Neural Procedural Memory 2026" → Zhao et al. 2026
  - "arXiv 2607.08716" → Wu et al. 2026
  - "ARGUS 2025" → Lu et al. 2026
  - "Steering Role Confusion" → Zhang, Lee & Park 2026
  - "Reducing Role Confusion…" → Liu 2026
  - TrustAttention → Shilov et al. 2026
  - "Reasoning Up the Instruction Ladder" → Zheng et al. 2026

  Keep the following apart:
  - C. T. Leong et al. 2025 versus J. W. Leong 2026;
  - E. Liu 2026 versus R. Liu et al. 2025 (DRIP);
  - Zeng 2025 versus Zeng et al. 2026 (same first author).
- **N4. A possible later version of TrustAttention exists.** On 27 Oct 2026 the same group posted "Heads of Security: Learned Attention Gates Improve Prompt Injection Robustness" (arXiv 2610.37657, Shilov et al., 9 authors). It uses the same two models and the same SecAlign++ baseline, but it does not use the name TrustAttention. I did not treat it as the same work. Check which version you mean before citing.
- **N5. Leong v1 versus v2.** v1 contains an OLMo-2 post-training lineage analysis (the provenance direction is already decodable in the base model). v2 lists it under material excluded from this version and calls the exclusion a narrowing of scope, not a retraction. The draft's line 468 is therefore correct. If the paper ever uses that result, cite v1 under its v1 title.
- **N6. Ye et al. Appendix K (line 493) is supported.** A probe ratio of Systemness to Userness predicts whether the user instruction overrides the system one (AUC .74 against baselines of .59–.60). This was on gpt-oss-20b, with 160 conflicts drawn from Geng et al. Appendix K also finds that token position, not tags, determines Systemness. That bears on the position control at line 486.
- **N7. Things used but not cited (not verified here):**
  - technical reports for Qwen3, Qwen2.5, OLMo 2, Granite 3.3, SmolLM2, SmolLM3, EuroLLM and Falcon3;
  - LoRA;
  - Holm's step-down procedure.
- **N8. The draft's list annotations should be removed in the release version.** These are notes such as "Abstract read." and "Search summary only; read before citing numbers". The clean list in §2 drops them.

## Addendum 2026-10-28 (evening): model reports, methods and benchmarks

These references were checked by a separate subagent against arXiv abstract pages, the ICLR, NeurIPS and ACL Anthology pages, the CEUR Vol-3920 index, Hugging Face blog posts and model cards, and a JSTOR listing. SmolLM2 and EuroLLM were checked directly on arXiv.

Notes:
- **Holm (1979):** JSTOR blocks automated access. Vol. 6, No. 2, pp. 65–70 comes from JSTOR's search listing plus agreeing secondary sources (MR 0538597). There is no DOI.
- **OLMo 2:** the short version is at COLM 2025; arXiv v1 is dated 31 Dec 2024, and v3 adds the 32B results.
- **Granite:** there is no Granite 3.3 report. We cite the Granite 3.0 report (paper.pdf in the archived GitHub repo) plus the granite-3.3-8b-instruct model card.
- **Falcon 3:** the canonical citation is the blog post. The model card's technical report says "Coming soon".
- **SEP:** the ICLR 2025 version. Do not confuse it with the 4-author ICLR 2024 SeT LLM workshop version.
- **InjecAgent:** ACL Anthology 2024.findings-acl.624. The exact title says "Large Language Model Agents".
- **Spotlighting:** CAMLIS 2024, CEUR Vol. 3920, pp. 48–62. The PDF has 14 pages against a 15-page range, a small inconsistency.

## Addendum 2026-10-29: steering defences on AgentDojo (prior art missed until now)

Found by a research subagent (`scratchpad/agentdojo_research.md`). Claude then checked each against the primary page:

- **CounterSteer (CORRECT AS CITED).** Russinovich, M. 2026. *CounterSteer: Suppressing Indirect Prompt Injection with Activation Steering.* arXiv:2609.36570, submitted 29 September 2026; abstract and HTML read.
  - **Method:** a per-model residual direction, fitted from paired episodes in which an injection was followed or resisted, and kept only if it passes causal and capability gates. It is subtracted from every tool-result token during prefill, with no fine-tuning.
  - **Models:** gpt-oss-20b, Qwen3-30B-A3B-Thinking-2507, Gemma-4-31B-it, GLM-4.5-Air and Llama-3.1-8B-Instruct.
  - **Results:** on a fixed 180-episode subset of AgentDojo's 629 pairs, compromise fell from 0.10–0.49 to 0.006–0.079, with benign utility at 93–100%.
  - **Role axis (§VI-A/B):** "the Qwen3-30B user-role axis … does not move ASR at matched dose"; on gpt-oss-20b the role axis composes with the behavioural direction.
- **Readable Before Actionable (CORRECT AS CITED).** Yu, Z., Xing, W., Yang, X., and Han, M. 2026. *Readable Before Actionable: Causal Tracing of Indirect Prompt Injection.* arXiv:2610.05295, submitted 4 October 2026; abstract read.
  - **What it is:** diagnostic. Directions estimated from hijacked-versus-resisted AgentDojo trajectories reduce attack success.
  - **Transfer:** effective intervention directions "transfer poorly across the tested channels".
- **Zhang, Lee & Park 2026 (re-read; already cited).** *Steering Role Confusion*, LessWrong, 20 August 2026.
  - **Method:** a difference of means between the same injected command declared as "user" and as "tool", on the command tokens, at layer 11 of gpt-oss-20b.
  - **Results:** steering toward tool cut ASR to about 0 (n = 50); utility was not reported.

**Consequence.** Training-free steering across families on AgentDojo is published (CounterSteer). Paper B §5 and the full report §12 now list it as not new. Our remaining differences:
- a direction from neutral text, with no injection data;
- measured selectivity (obey versus believe);
- the patching map;
- sealed tests.
- **The Rogue Scalpel (CORRECT AS CITED; added 2026-10-29).** Korznikov, A., Galichin, A., Dontsov, A., Rogov, O. Y., Oseledets, I., and Tutubalina, E. *The Rogue Scalpel: Activation Steering Compromises LLM Safety.* arXiv:2509.22067 (v1 26 September 2025, v2 15 February 2026).
  - **Venue:** the iclr.cc virtual page (https://www.iclr.cc/virtual/2026/10019314) lists it as a poster in the ICLR 2026 Workshop on Principled Design for Trustworthy AI. It is not a main-conference paper.
  - **Claim checked:** steering along random directions raised harmful compliance from 0% to 1–13% across model families (abstract).

## Addendum 2026-10-29 (b): references checked before release

Before release, Claude matched each cited reference of Paper A and Paper B to this record. Three entries had no record yet, and four were covered only by category in the 2026-10-28 evening addendum, so each was checked against its primary page:
- **Abdin, M., et al. 2024. Phi-4 Technical Report.** arXiv:2412.08905; v1 12 Dec 2024; first author Marah Abdin; no venue. Correct as cited.
- **Young, A., et al. 2024. Yi: Open Foundation Models by 01.AI.** arXiv:2403.04652; v1 7 Mar 2024; first author Alex Young; no venue. Correct as cited.
- **Debenedetti, E., et al. 2024. AgentDojo.** arXiv:2406.13352, v1 19 Jun 2024. NeurIPS 2024 Datasets and Benchmarks Track, per the proceedings.neurips.cc listing (paper 97091a5177d8dc64b1da8bf3e1f6fb54) and OpenReview m1YYAQjO3w. Correct as cited.
- **Yang, A., et al. 2025. Qwen3 Technical Report.** arXiv:2505.09388; v1 14 May 2025; first author An Yang. Correct as cited.
- **Qwen2.5 Technical Report.** arXiv:2412.15115; v1 19 Dec 2024; the author list starts with "Qwen", then An Yang. "Yang, A., et al. (Qwen Team)" is acceptable.
- **Bakouch, E., et al. 2025. SmolLM3: smol, multilingual, long-context reasoner.** Hugging Face blog, 8 July 2025; first author Elie Bakouch. Correct as cited.
- **Hu, E. J., et al. 2022. LoRA.** arXiv:2106.09685; v1 17 Jun 2021; first author Edward J. Hu. The arXiv page lists no venue; ICLR 2022 is the published version.

The two papers also cite each other (Ramdan 2026), with the DOIs reserved on Zenodo.

## Addendum 2026-10-30: references added in v2

AI prior-art searches in the session that ran the v2 follow-ups ("Do tests for the next era") found three papers missing from v1. The release session checked each against its arXiv abstract page and full HTML text before citing it:
- **Pan, X., Fan, J., Xiong, Z., Hahami, E., Overwiening, J., and Xie, Z. 2025. User-Assistant Bias in LLMs.** arXiv:2508.15815; v1 16 Aug 2025, v3 19 Apr 2026. It introduces the UserAssist benchmark, in which user and assistant turns give conflicting information about the same entities, and tests 52 models (26 API, 26 open-weight; the tables list 49). Most instruction-tuned models show a strong user bias, and base and reasoning models are near neutral (§4.1). Human-preference DPO increases the bias and reasoning SFT reduces it, in Llama-3.1-8B-Instruct and Qwen2.5-7B-Instruct (§4.2). No system role, no agents. Cited in Paper A §12 and Paper B §5.
- **Laddha, A., Pradhan, N., and Srivastava, G. 2026. Position, Role or Label? A Controlled Study of Instruction Conflicts in LLM Agents.** arXiv:2610.33201; v1 23 Oct 2026. 14 open models (Qwen3 0.6B–14B, Qwen3.5 0.8B–122B-A10B, gpt-oss-20b and 120b), 26 model-modes (thinking on and off). In tool and file-write tasks, an operator line sent first in the real system message wins less often than the same labelled text sent first in a user message, by 6.41 to 48.75 points, in all 26 model-modes (§4.3, Table 3); in format tasks, in none. For gpt-oss, the real role helps in format, ordering and refusal tasks. The authors say their contrast does not fully separate role from position (§4.3, Limitation 4). Cited in Paper A §6b, §11 and §12, and Paper B §5.
- **Liu, N. G., Jang, H., Jun, Y., and Lee, H. 2026. IHDec: Divergence-Steered Contrastive Decoding for Securing Multi-Turn Instruction Hierarchies.** arXiv:2606.29960; v1 29 Jun 2026, v2 17 Sep 2026; Findings of EMNLP 2026 per the arXiv listing. It reports a role-influence inversion in multi-turn conflicts, in which subordinate inputs override superior roles, and a decoding-time defence. The abstract does not name the roles, so the papers cite it only for the inversion and the defence. Cited in Paper A §12 and Paper B §5.

Two of the searching session's summaries were narrower in the sources: Laddha et al.'s "all 26 settings" holds for tool and file-write tasks only, and IHDec's abstract does not say that the user turn outweighs the system prompt. The papers cite only what the sources state.
