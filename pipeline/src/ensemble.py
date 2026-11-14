"""Average of chat-percentiles: each model's score -> fraction of everyday-chat dev messages it scores below.

So 0.995 means "more suspicious than 99.5% of normal chat" for that model; the ensemble averages these.
Thresholds are then set exactly as for any model (<=1% FPR on chat dev). No weights are tuned.
usage: python ensemble.py <out_run_dir> <mix_dir> <run_a> <run_b> [...]
"""
import json, os, sys
import numpy as np, pandas as pd

args = sys.argv[1:]
method = "pct"
if args[0].startswith("--method="):
    method = args.pop(0).split("=", 1)[1]
out, mix, runs = args[0], args[1], args[2:]
ev = pd.read_json(f"{mix}/eval.jsonl", lines=True)[["id", "set", "label", "language", "text"]]
acc = np.zeros(len(ev))
for r in runs:
    p = pd.read_json(f"{r}/preds.jsonl", lines=True)[["id", "set", "score"]].drop_duplicates(["id", "set"])
    s = ev[["id", "set"]].merge(p, on=["id", "set"], how="left").score.fillna(0).values
    if method == "logit_z":  # z-scored logits, statistics from chat-dev (council round 2)
        z = np.log(np.clip(s, 1e-7, 1 - 1e-7) / (1 - np.clip(s, 1e-7, 1 - 1e-7)))
        ref = z[(ev.set == "tg_dev").values]
        acc += (z - ref.mean()) / (ref.std() + 1e-9)
    else:
        ref = np.sort(s[(ev.set == "tg_dev").values])
        acc += np.searchsorted(ref, s, side="right") / len(ref) + 1e-6 * s  # tiny raw-score term breaks ties above chat max
acc /= len(runs)
os.makedirs(out, exist_ok=True)
ev.assign(score=(1 / (1 + np.exp(-acc))) if method == 'logit_z' else acc).to_json(f"{out}/preds.jsonl", orient="records", lines=True, force_ascii=False)
json.dump({"mix": mix, "members": runs, "method": method}, open(f"{out}/config.json", "w"), indent=1)
print("wrote", out)
