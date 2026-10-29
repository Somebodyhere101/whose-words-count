"""Descriptive analysis of the fixed exploratory pilot, after all conditions finish."""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE / "decomposition_pilot"
CONDITIONS = ("plain", "emph", "oldR2", "user2", "user4", "orth2", "pair2", "random2")

def analyze():
    manifest = json.loads((ROOT / "manifest.json").read_text())
    for path, expected in ((HERE / "decomposition_pilot.py", manifest["script_sha256"]),
                           (HERE / "decomposition_plan.txt", manifest["plan_sha256"])):
        assert hashlib.sha256(path.read_bytes()).hexdigest() == expected, str(path)
    results, sets = {}, []
    for cond in CONDITIONS:
        p = ROOT / f"{cond}.json"
        if not p.exists():
            return {"ready": False, "missing": [c for c in CONDITIONS if not (ROOT / f"{c}.json").exists()]}
        d = json.loads(p.read_text())
        recs = d["records"]
        assert len(recs) == 32
        keys = [(r["task"], r["order"], r["conflict"]) for r in recs]
        assert len(set(keys)) == 32
        sets.append(set(keys))
        conflicts = [r for r in recs if r["conflict"] != "utility"]
        utility = [r for r in recs if r["conflict"] == "utility"]
        assert len(conflicts) == 24 and len(utility) == 8
        assert {r["task"] for r in conflicts} == {65, 66}
        results[cond] = {"n_conflicts": 24, "base_tasks": 2,
                         "system_successes": sum(r["met1"] for r in conflicts),
                         "system_rate": sum(r["met1"] for r in conflicts) / 24,
                         "user_rate": sum(r["met2"] for r in conflicts) / 24,
                         "degenerate": sum(r["degenerate"] for r in conflicts) / 24,
                         "mean_words": sum(r["words"] for r in conflicts) / 24,
                         "at_cap": sum(r["n_new"] >= 512 for r in conflicts),
                         "utility_successes": sum(r["utility_ok"] for r in utility),
                         "seconds": d["seconds"],
                         "by_base_task": {str(t): sum(r["met1"] for r in conflicts if r["task"] == t) / 12 for t in (65, 66)}}
    assert all(s == sets[0] for s in sets)
    # Fixed tie order: lowest alpha, system-only before paired; original U before orthogonal U.
    eligible = []
    for cond in ("user2", "orth2", "pair2", "user4"):
        r = results[cond]
        gain_plain = r["system_rate"] - results["plain"]["system_rate"]
        gain_emph = r["system_rate"] - results["emph"]["system_rate"]
        passes = gain_plain >= .10 and gain_emph >= .10 and r["degenerate"] <= results["plain"]["degenerate"] + .05 and r["utility_successes"] >= results["plain"]["utility_successes"]
        r.update({"gain_plain": gain_plain, "gain_emph": gain_emph, "screening_pass": passes})
        if passes:
            eligible.append(cond)
    report = {"ready": True, "status": "GO" if eligible else "NO_GO", "selected": eligible[0] if eligible else None,
              "conditions": results, "limits": "Two base tasks; exploratory screen only. A capability claim requires held-out tasks, stronger published baselines, and another family."}
    (ROOT / "analysis.json").write_text(json.dumps(report, indent=2))
    return report

if __name__ == "__main__":
    print(json.dumps(analyze(), indent=2))
