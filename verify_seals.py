"""Check every preregistration seal (*.sha256) in research_next/agent_goal_persistence/.

Shared code files were extended by later tests, so a seal's code files are matched against the working copy OR the
files inside the archived bundles (bundles/*.tgz), which hold the exact sealed versions. A seal file that lists
the same path twice (an amendment before data) passes if any listed hash matches. Lines that are not SHA-256 entries
(a note such as a bundle's md5) are skipped.
Usage, from the repository root: python verify_seals.py"""
import glob
import hashlib
import os
import re
import sys
import tarfile

STUDY = os.path.join(os.path.dirname(os.path.abspath(__file__)), "research_next", "agent_goal_persistence")


def sha(b):
    return hashlib.sha256(b).hexdigest()


bundled = set()
for b in glob.glob(os.path.join(STUDY, "bundles", "*.tgz")):
    with tarfile.open(b) as t:
        for m in t.getmembers():
            if m.isfile():
                bundled.add((os.path.basename(m.name), sha(t.extractfile(m).read())))

bad_total = 0
for s in sorted(glob.glob(os.path.join(STUDY, "*.sha256"))):
    wanted = {}
    for line in open(s, encoding="utf-8"):
        parts = line.split(None, 1)
        if len(parts) == 2 and re.fullmatch(r"[0-9a-f]{64}", parts[0]):
            wanted.setdefault(parts[1].strip().lstrip("*"), []).append(parts[0])
    ok, how = 0, set()
    missing = []
    for path, hashes in wanted.items():
        p = os.path.join(STUDY, *path.split("/"))
        if not os.path.exists(p):           # a bundle named by an absolute path at seal time is shipped in bundles/
            p = os.path.join(STUDY, "bundles", os.path.basename(path))
        here = sha(open(p, "rb").read()) if os.path.exists(p) else None
        if here in hashes:
            ok += 1
            how.add("working copy")
        elif any((os.path.basename(path), h) in bundled for h in hashes):
            ok += 1
            how.add("bundle")
        else:
            missing.append(path)
    bad_total += len(missing)
    status = "OK" if not missing else "MISSING " + ", ".join(missing)
    print(f"{os.path.basename(s):22s} {ok:2d}/{len(wanted):2d} files  ({' + '.join(sorted(how))})  {status}")
print("ALL SEALS VERIFIED" if bad_total == 0 else f"{bad_total} sealed files could not be matched")
sys.exit(1 if bad_total else 0)
