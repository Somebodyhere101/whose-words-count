# Data notes

**Not included:**
- **Fetched result archives (`cloud_*/results*.tgz`).** Their contents are included, already extracted beside where they were. `strip_report.json` lists every removed file.
- **Model weights.** All models are public on Hugging Face under the ids named in the papers and scripts, and the scripts download them.
- **Benchmark data.** It is not redistributed; the scripts clone it at pinned commits.
  - SEP (Zverev et al., ICLR 2025; https://github.com/egozverev/Should-It-Be-Executed-Or-Processed): code under MIT, dataset under CC BY 4.0. Commit 7606c06.
  - InjecAgent (Zhan et al., Findings of ACL 2024; https://github.com/uiuc-kang-lab/InjecAgent): MIT. Commit f19c9f2.
  - `research_next/agent_goal_persistence/data/injecagent_prompts.json` holds InjecAgent's prompt templates, extracted from that repository by parsing, under its MIT licence.
  - Some raw output files quote benchmark items in model generations. They are shared under the benchmarks' licences, with attribution.

**Redactions.** Mentions of two private local folders were replaced with `[private path removed]` in text files, as listed in `strip_report.json`. No result was changed.
