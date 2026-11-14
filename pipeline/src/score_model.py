"""Re-score a trained run's best checkpoint on a (new) eval table -> <run>/preds.jsonl (old preds kept as preds_prev.jsonl).

usage: python score_model.py <run_dir> <mix_dir>
"""
import json, os, shutil, sys
import numpy as np, pandas as pd, torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

run, mix = sys.argv[1], sys.argv[2]
cfg = json.load(open(f"{run}/config.json"))
pos = cfg.get("pos_idx", 1); max_len = cfg.get("max_len", 128); prefix = cfg.get("prefix", "")
dev = "cuda" if torch.cuda.is_available() else ("mps" if torch.backends.mps.is_available() else "cpu")
tok = AutoTokenizer.from_pretrained(f"{run}/best")
model = AutoModelForSequenceClassification.from_pretrained(f"{run}/best").to(dev).eval()
ev = pd.read_json(f"{mix}/eval.jsonl", lines=True)
scores = []
with torch.no_grad():
    for i in range(0, len(ev), 64):
        enc = tok([prefix + t for t in ev.text.iloc[i:i + 64]], padding=True, truncation=True, max_length=max_len, return_tensors="pt").to(dev)
        with torch.autocast("cuda", dtype=torch.float16, enabled=dev == "cuda"):
            logits = model(**enc).logits.float()
        scores.append(torch.softmax(logits, -1)[:, pos].cpu().numpy())
if os.path.exists(f"{run}/preds.jsonl"):
    shutil.copy(f"{run}/preds.jsonl", f"{run}/preds_prev.jsonl")
keep = [c for c in ["id", "set", "split", "label", "language", "text"] if c in ev.columns]
ev[keep].assign(score=np.concatenate(scores)).to_json(f"{run}/preds.jsonl", orient="records", lines=True, force_ascii=False)
cfg["rescored_on"] = mix; json.dump(cfg, open(f"{run}/config.json", "w"), indent=1)
print("rescored", run, "on", mix, len(ev))
