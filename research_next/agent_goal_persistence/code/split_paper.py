"""Split PAPER_DRAFT.md (the full technical report) into Paper A (goal persistence) and Paper B (source monitoring).
Usage: python split.py <in PAPER_DRAFT.md> <out dir>"""
import re
import sys

src, outdir = sys.argv[1], sys.argv[2]
text = open(src, encoding="utf-8").read()
lines = text.split("\n")


def sections(ls):
    """[(header or '' for the preamble, [lines])] split at '## ' headers."""
    out, cur, head = [], [], ""
    for l in ls:
        if l.startswith("## "):
            out.append((head, cur))
            head, cur = l, [l]
        else:
            cur.append(l)
    out.append((head, cur))
    return out


S = sections(lines)
get = {h.split(".")[0].replace("## ", "") if h else "": (h, b) for h, b in S}
by_head = {h: b for h, b in S}


def find(prefix):
    for h, b in S:
        if h.startswith(prefix):
            return b
    raise KeyError(prefix)


def cut_block(body, start_marker, end_marker=None):
    """Remove lines from the one starting with start_marker up to (not including) the one starting with end_marker."""
    out, skip = [], False
    for l in body:
        if l.startswith(start_marker):
            skip = True
            continue
        if skip and end_marker is not None and l.startswith(end_marker):
            skip = False
        if not skip:
            out.append(l)
    return out


# ----------------------------------------------------------------------------------------------- Paper A
B_SECTIONS = ("## 6g.", "## 6h.", "## 6i.", "## 6j.", "## 6k.", "## 6l.", "## 6m.")
INTERIM = ("## Fix-test pilot", "## Neutral-role decomposition")
A = []
appendix = []
for h, b in S:
    if h.startswith(B_SECTIONS):
        continue
    if h.startswith(INTERIM):
        appendix.append([("### " + l[3:]) if l.startswith("## ") else l for l in b])
        continue
    if h == "":
        b = [l for l in b if not l.startswith("- Draft 8 adds") and not l.startswith("- The numbers in §6j")]
    if h.startswith("## Abstract"):
        b = cut_block(b, "**Where does the text come from?", "We report the negative results in full.")
    if h.startswith("## 1. Introduction"):
        b = [l for l in b if not l.startswith("- a source-monitoring account") and not l.startswith("- a map-guided, training-free lever")]
    if h.startswith("## 11. Limitations"):
        out, skip = [], False
        for l in b:
            if l.startswith("- **Source-monitoring items") :
                skip = True
            if skip and l.startswith("- **") and not (l.startswith("- **Source-monitoring items") or l.startswith("- **The map is a patching map")
                                                      or l.startswith("- **The lever (") or l.startswith("- **Operational re-runs")):
                skip = False
            if not skip:
                out.append(l)
        b = out
    if h.startswith("## 12."):
        b = cut_block(b, "**The source-monitoring line (§6g–§6m): what may be new")
    if h.startswith("## Data, code"):
        b = cut_block(b, "**The source-monitoring line (§6g–§6m).**", "**Cloud cost.**")
    if h.startswith("## References"):
        A.append(("## Appendix A. Interim pilot notes", ["## Appendix A. Interim pilot notes", "",
                  "These two notes were written during the study and are kept as they were, apart from the heading level."]
                  + sum(([""] + x for x in appendix), [])))
    A.append((h, b))
a_text = "\n".join(sum((b for _, b in A), []))
a_text = a_text.replace("**Draft 8, 2026-10-28.**", "**Paper A of two, split 2026-10-29 from the full technical report (`PAPER_DRAFT.md`, Draft 8).** The source-monitoring work (former §6g–§6m) is now Paper B (`PAPER_B_SOURCE_MONITORING.md`).")
a_text = re.sub(r"\(§6g\)", "(Paper B)", a_text)
a_text = a_text.replace("PREREG_S addresses believing versus obeying on synthetic items (§6g).",
                        "Paper B addresses believing versus obeying on synthetic items.")

# ----------------------------------------------------------------------------------------------- Paper B
renum = {"6g": "3.1", "6h": "3.2", "6l": "3.3", "6i": "3.4", "6j": "3.5", "6k": "3.6", "6m": "3.7"}
order = ["6g", "6h", "6l", "6i", "6j", "6k", "6m"]
titles = {"6g": "No single source tag (FRAGMENTED, PREREG_S)",
          "6h": "Where each behaviour reads the source (H1 MIXED, H2 DISSOCIATED, PREREG_T)",
          "6l": "The map in ten more models, up to 32B (4 of 5 SUPPORTED, PREREG_W)",
          "6i": "A first defence attempt fails (NONE, PREREG_U)",
          "6j": "Checking the readout, and searching for a lever (EXPL., PILOT_V0)",
          "6k": "The lever, sealed (SELECTIVE, PREREG_V)",
          "6m": "Public prompt-injection benchmarks (NONE overall; strong in Qwen; PREREG_X and PILOT_V1)"}


def renumber(t):
    t = re.sub(r"§6([g-m])–§6([g-m])", lambda m: f"§{renum['6' + m.group(1)]}–§{renum['6' + m.group(2)]}", t)
    t = re.sub(r"§6([g-m])\b", lambda m: "§" + renum["6" + m.group(1)], t)
    return t


results = []
for k in order:
    body = find(f"## {k}.")[1:]
    if k == "6g":
        body = [l.replace("**Question.** The role results above concern goal text. In cognitive science",
                          "**Question.** In cognitive science") for l in body]
    results += [f"### {renum[k]}. {titles[k]}"] + body
res_text = renumber("\n".join(results))

lim = find("## 11. Limitations")
b_lim, keep = [], False
for l in lim:
    if l.startswith("- **Source-monitoring items") or l.startswith("- **The map is a patching map") or l.startswith("- **The lever (") or l.startswith("- **Operational re-runs"):
        keep = True
    elif l.startswith("- **"):
        keep = False
    if keep:
        b_lim.append(l)
b_lim_text = renumber("\n".join(b_lim))

d = find("## Data, code")
b_data, keep = [], False
for l in d:
    if l.startswith("**The source-monitoring line (§6g–§6m).**"):
        keep = True
    if keep:
        b_data.append(l)
b_data_text = renumber("\n".join(b_data)).replace("**The source-monitoring line (§3.1–§3.7).**", "**Seals and bundles.**")

twelve = find("## 12.")
b12, keep = [], False
for l in twelve:
    if l.startswith("**The source-monitoring line (§6g–§6m): what may be new"):
        keep = True
        continue
    if keep:
        b12.append(l)
b12_text = renumber("\n".join(b12))

ai = "\n".join(find("## AI-use statement")[1:]).strip()
refs = find("## References")
ref_lines = [l for l in refs if l.startswith("- ")]

PB = open(outdir + "/paper_b_frame.md", encoding="utf-8").read()
pb = (PB.replace("@@RESULTS@@", res_text).replace("@@LIMITATIONS@@", b_lim_text).replace("@@NEW@@", b12_text)
        .replace("@@DATA@@", b_data_text).replace("@@AIUSE@@", ai))

# references: keep those cited in each paper's body
OVERRIDE = {"Yang, A., et al. 2025": ["Qwen3 Technical", "Yang et al. 2025"], "Yang, A., et al. (Qwen Team)": ["Qwen2.5"],
            "Allal": ["SmolLM2"], "Martins": ["EuroLLM"], "Hu, E. J.": ["LoRA"], "Bakouch": ["SmolLM3", "Bakouch"],
            "Walsh": ["Walsh", "OLMo 2 Furious"], "Abdin": ["Abdin", "Phi-4 Technical"], "IBM Granite Team. 2024": ["IBM Granite Team"],
            "IBM Granite Team. 2025": ["IBM Granite Team"], "Falcon-LLM": ["Falcon-LLM"], "Young": ["Young et al."]}


def keys(ref):
    for k, v in OVERRIDE.items():
        if ref[2:].startswith(k):
            return v
    sur = ref[2:].split(",")[0].split(".")[0].strip()
    return [sur]


def ref_block(body):
    kept = [r for r in ref_lines if any(k in body for k in keys(r))]
    return "\n".join(kept), len(kept)


a_body = a_text.split("## References")[0]
a_refs, na = ref_block(a_body)
a_text = a_text.split("## References")[0] + "## References\n\nVerified 2026-10-28 (`REFERENCES_VERIFIED.md` and its addendum).\n\n" + a_refs + "\n"
pb_body = pb.split("@@REFS@@")[0]
b_refs, nb = ref_block(pb_body)
pb = pb.replace("@@REFS@@", b_refs)
open(outdir + "/PAPER_A_GOAL_PERSISTENCE.md", "w", encoding="utf-8").write(a_text)
open(outdir + "/PAPER_B_SOURCE_MONITORING.md", "w", encoding="utf-8").write(pb)
print("A words", len(a_text.split()), "refs", na, "| B words", len(pb.split()), "refs", nb)
left = re.findall(r"§6[g-m]", pb)
print("B leftover §6g-m refs:", len(left), "| A leftover §6g-m refs:", len(re.findall(r"§6[g-m]", a_text)))
