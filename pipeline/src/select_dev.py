"""Dev-only comparison of candidate runs (real-test is never read here).

usage: python select_dev.py <mix_dir> <run_dir> [<run_dir> ...]
"""
import os, sys
import pandas as pd
sys.path.insert(0, os.path.dirname(__file__))
from evaluate import dev_report, operating_threshold

mix = sys.argv[1]
ev = pd.read_json(f"{mix}/eval.jsonl", lines=True)
ev = ev[ev.set.isin(["real_dev", "tg_dev", "kbd_perturbed"])]
for run in sys.argv[2:]:
    p = pd.read_json(f"{run}/preds.jsonl", lines=True)[["id", "set", "score"]].drop_duplicates(["id", "set"])
    d = ev.merge(p, on=["id", "set"], how="left")
    thr = operating_threshold(d)
    r = dev_report(d, thr); h = r["headline"]; s = r["secondary"]
    kb = r.get("kbd_paired", {})
    nf = h["notification_fpr"].get("rate")
    print(f"{os.path.basename(run):28s} notifFPR {nf} | dev recall {h['recall']['rate']:.3f} ({h['recall']['k']}/{h['recall']['n']}) AP-vs-chat {h['pr_auc_vs_chat']:.3f} "
          f"| kk {r['recall_by_language'].get('kk', {}).get('rate')} ru {r['recall_by_language'].get('ru', {}).get('rate')} "
          f"| frag {s['fragment_recall (<=4 words)'].get('rate')} | advice {s['advice_text_flag_rate (anti-fraud advice that quotes scams; stress test)'].get('rate')} "
          f"| kbd {kb.get('folded_recall', {}).get('rate')}")
