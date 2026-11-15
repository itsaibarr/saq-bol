"""Freeze a model, record everything needed to audit it, then score real-test ONCE (via finalize.py).

usage: python freeze.py <run_dir> --note "why"   (run_dir = a single run or an ensemble dir with config.json "members")
Writes a freeze block to RUNS.md before real-test is scored. Refuses to run twice for the same run.
"""
import argparse, datetime, glob, hashlib, json, os, subprocess, sys

ap = argparse.ArgumentParser(); ap.add_argument("run"); ap.add_argument("--note", default=""); ap.add_argument("--compare", nargs="*", default=[]); ap.add_argument("--record-only", action="store_true")
a = ap.parse_args()
if os.path.exists(f"{a.run}/final_report.json"):
    sys.exit(f"{a.run} already finalized; real-test is scored once per frozen model.")
cfg = json.load(open(f"{a.run}/config.json"))
members = cfg.get("members", [a.run])
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()[:16]
tried = sorted({os.path.basename(p) for p in glob.glob("runs/kg_*") + glob.glob("runs/enc_*") + glob.glob("runs/ens_*") if os.path.exists(f"{p}/preds.jsonl")})
block = [f"\n## Freeze {datetime.datetime.now().isoformat(timespec='minutes')}: {os.path.basename(a.run)}",
         f"- Note: {a.note}", f"- Mix: {cfg.get('mix')}; ensemble method: {cfg.get('method', 'single model')}",
         f"- Selection rule: SPEC.md A5 (dev AP vs chat + notifications); operating point: A4.",
         f"- Dev configurations evaluated before this freeze (trained runs and ensembles with dev preds): {len(tried)}"]
for m in members:
    mc = json.load(open(f"{m}/config.json"))
    block.append(f"  - member {os.path.basename(m)}: model {mc.get('model')}, lr {mc.get('lr')}, epochs {mc.get('epochs')}, seed {mc.get('seed')}, "
                 f"best epoch {json.load(open(f'{m}/best_epoch.json')).get('epoch') if os.path.exists(f'{m}/best_epoch.json') else '?'}, "
                 f"preds sha256 {sha(f'{m}/preds.jsonl')}")
block.append(f"- Ensemble preds sha256: {sha(f'{a.run}/preds.jsonl')}")
if not os.path.exists("RUNS.md"):
    open("RUNS.md", "w").write("# Real-test log (each line = one frozen model, scored once)\n")
open("RUNS.md", "a").write("\n".join(block) + "\n")
print("\n".join(block))
if a.record_only:
    sys.exit(0)
subprocess.run([sys.executable, "pipeline/src/finalize.py", a.run, "--mix", cfg.get("mix"), "--note", a.note] + (["--compare"] + a.compare if a.compare else []), check=True)
