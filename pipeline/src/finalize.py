"""Score a FROZEN model on real-test. The only script that reports real-test numbers for trained models (A2 rules).

Thresholds come from everyday-chat dev only: "scam" at <=1% FPR, "suspicious" at <=5% FPR. Temperature scaling is
fitted on dev (real-dev headline scams + chat dev) for the demo's displayed risk score only; it does not change any
metric. Writes runs/<name>/final_report.json and appends one line to RUNS.md.
usage: python finalize.py runs/<name> [--note "why this model"] [--compare runs/B5_offshelf_scam_model]
"""
import argparse, datetime, json, os, sys
import numpy as np, pandas as pd
from scipy.optimize import minimize_scalar
sys.path.insert(0, os.path.dirname(__file__))
from evaluate import compare, dev_report, operating_threshold, pick_threshold, report, save, summary_line

ap = argparse.ArgumentParser(); ap.add_argument("run"); ap.add_argument("--note", default="")
ap.add_argument("--mix", default=None); ap.add_argument("--compare", nargs="*", default=[])
ap.add_argument("--eval-file", default="eval.jsonl"); ap.add_argument("--preds-name", default="preds.jsonl"); ap.add_argument("--tag", default="")
a = ap.parse_args()
cfg = json.load(open(f"{a.run}/config.json")) if os.path.exists(f"{a.run}/config.json") else {}
mix = a.mix or cfg.get("mix", "data/processed/mix_v4")
ev = pd.read_json(f"{mix}/{a.eval_file}", lines=True)


def load_scores(run):
    pr = pd.read_json(f"{run}/{a.preds_name}", lines=True)[["id", "set", "score"]].drop_duplicates(["id", "set"])
    d = ev.drop(columns=[c for c in ["score"] if c in ev.columns]).merge(pr, on=["id", "set"], how="left")
    real = d.set.isin(["real_dev", "real_test", "kbd_perturbed", "tg_dev", "tg_test"])
    assert d[real].score.notna().all(), f"{run}: missing scores on real/chat rows"
    return d


d = load_scores(a.run)
dv = d[((d.set == "real_dev") & (d.label == 1) & d.headline.fillna(False).astype(bool)) | (d.set == "tg_dev")]
logit = lambda p: np.log(np.clip(p, 1e-6, 1 - 1e-6) / (1 - np.clip(p, 1e-6, 1 - 1e-6)))
def nll(T):
    q = 1 / (1 + np.exp(-logit(dv.score.values) / T))
    return -np.mean(dv.label * np.log(np.clip(q, 1e-9, 1)) + (1 - dv.label) * np.log(np.clip(1 - q, 1e-9, 1)))
T = float(minimize_scalar(nll, bounds=(0.05, 20), method="bounded").x)
chat_dev = d[d.set == "tg_dev"].score
thr = operating_threshold(d)
thr_low = operating_threshold(d, max_chat_fpr=0.05, max_notif_fpr=0.15)
out = {"run": a.run, "mix": mix, "temperature": T, "thr_scam": thr, "thr_suspicious": thr_low,
       "dev": dev_report(d, thr), "test": report(d, thr, thr_low=thr_low),
       "finalized_at": datetime.datetime.now().isoformat(timespec="minutes"), "note": a.note, "comparisons": {}}
for other in a.compare:
    o = load_scores(other)
    out["comparisons"][os.path.basename(other)] = compare(d, o, thr, operating_threshold(o))
save(out, f"{a.run}/final_report{a.tag}.json")
keep = [c for c in ["id", "set", "split", "label", "language", "unit", "headline", "score", "text"] if c in d.columns]
d[keep].to_json(f"{a.run}/preds_final{a.tag}.jsonl", orient="records", lines=True, force_ascii=False)
t = out["test"]; h = t["headline"]
line = (f"| {out['finalized_at']} | {os.path.basename(a.run)}{a.tag} | {h['recall']['rate']:.3f} [{h['recall']['wilson95'][0]:.2f}, {h['recall']['wilson95'][1]:.2f}] "
        f"| {h['chat_fpr']['rate']:.4f} | {h['pr_auc_vs_chat']:.3f} | "
        f"{t['recall_by_language'].get('kk', {}).get('rate', float('nan')):.2f} / {t['recall_by_language'].get('ru', {}).get('rate', float('nan')):.2f} | {a.note} |\n")
if not os.path.exists("RUNS.md"):
    open("RUNS.md", "w").write("# Real-test log: each line is one frozen model, scored once (A2 rules)\n\n"
                               "| when | run | headline recall [Wilson 95%] | chat FPR | PR-AUC vs chat | recall kk / ru | note |\n|---|---|---|---|---|---|---|\n")
open("RUNS.md", "a").write(line)
print(summary_line(os.path.basename(a.run), t)); print(json.dumps(out["comparisons"], indent=1))
