"""A5 rule: rank candidate runs by real-dev AP of headline scams vs chat-dev + real-dev notifications (threshold-free)."""
import os, sys
import numpy as np, pandas as pd
from sklearn.metrics import average_precision_score
mix = sys.argv[1]
ev = pd.read_json(f"{mix}/eval.jsonl", lines=True)
ev = ev[ev.set.isin(["real_dev", "tg_dev"])]
rows = []
for run in sys.argv[2:]:
    p = pd.read_json(f"{run}/preds.jsonl", lines=True)[["id", "set", "score"]].drop_duplicates(["id", "set"])
    d = ev.merge(p, on=["id", "set"], how="left")
    pos = d[(d.set == "real_dev") & (d.label == 1) & (d.headline == True)]
    neg = d[(d.set == "tg_dev") | ((d.set == "real_dev") & (d.label == 0) & (d.unit == "notification"))]
    ap = average_precision_score(np.r_[np.ones(len(pos)), np.zeros(len(neg))], np.r_[pos.score, neg.score])
    import json
    cfg = json.load(open(f"{run}/config.json")) if os.path.exists(f"{run}/config.json") else {}
    rows.append((ap, len(cfg.get("members", [run])), os.path.basename(run)))
for ap, n, name in sorted(rows, reverse=True):
    print(f"{ap:.4f}  models={n}  {name}")
