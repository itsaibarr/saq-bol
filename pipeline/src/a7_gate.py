"""A7 gate (dev only): does the A5-picked v3 candidate replace v2?

Replace iff (i) dev AP vs chat + notifications >= v2 AP - 0.005 and (ii) Russian dev headline scams caught at the
candidate's own A4 threshold >= v2's. usage: python a7_gate.py <mix> <v2_run> <candidate_run>
"""
import os, sys
import numpy as np, pandas as pd
from sklearn.metrics import average_precision_score
sys.path.insert(0, os.path.dirname(__file__))
from evaluate import operating_threshold

mix, runs = sys.argv[1], sys.argv[2:]
ev = pd.read_json(f"{mix}/eval.jsonl", lines=True)
ev = ev[ev.set.isin(["real_dev", "tg_dev"])]
res = {}
for run in runs:
    p = pd.read_json(f"{run}/preds.jsonl", lines=True)[["id", "set", "score"]].drop_duplicates(["id", "set"])
    d = ev.merge(p, on=["id", "set"], how="left")
    assert d.score.notna().all(), run
    pos = d[(d.set == "real_dev") & (d.label == 1) & (d.headline == True)]
    neg = d[(d.set == "tg_dev") | ((d.set == "real_dev") & (d.label == 0) & (d.unit == "notification"))]
    ap = average_precision_score(np.r_[np.ones(len(pos)), np.zeros(len(neg))], np.r_[pos.score, neg.score])
    thr = operating_threshold(d)
    ru = pos[pos.language == "ru"]
    res[run] = (ap, int((ru.score >= thr).sum()), len(ru), int((pos.score >= thr).sum()), len(pos))
    print(f"{os.path.basename(run)}: dev AP {ap:.4f} | A4 thr {thr:.10f} | Russian dev caught {res[run][1]}/{res[run][2]} | all dev headline {res[run][3]}/{res[run][4]}")
v2, cand = res[runs[0]], res[runs[1]]
ok_ap, ok_ru = cand[0] >= v2[0] - 0.005, cand[1] >= v2[1]
print(f"A7 gate: AP {'pass' if ok_ap else 'FAIL'} ({cand[0]:.4f} vs {v2[0]:.4f} - 0.005), Russian {'pass' if ok_ru else 'FAIL'} ({cand[1]} vs {v2[1]})"
      f" -> {'v3 replaces v2' if ok_ap and ok_ru else 'v2 stays'}")
