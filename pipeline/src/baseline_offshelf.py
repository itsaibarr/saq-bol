"""B5: an existing multilingual scam detector used as-is (no Kazakh in its training languages).

Horizon-Labs/phishing-scam-detector-base (Apache-2.0, mmBERT-base): labels fraud / spam / legitimate.
Score = P(fraud). Threshold: <=1% FPR on dev negatives, same rule as every other model.
usage: python baseline_offshelf.py <mix_dir>
"""
import json, os, sys
import numpy as np, pandas as pd, torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer
sys.path.insert(0, os.path.dirname(__file__))
from evaluate import dev_report, pick_threshold, report, save

mix = sys.argv[1] if len(sys.argv) > 1 else "data/processed/mix_v1"
name, rid = "Horizon-Labs/phishing-scam-detector-base", "B5_offshelf_scam_model"
ev = pd.read_json(f"{mix}/eval.jsonl", lines=True)
dev = "mps" if torch.backends.mps.is_available() else ("cuda" if torch.cuda.is_available() else "cpu")
tok = AutoTokenizer.from_pretrained(name)
model = AutoModelForSequenceClassification.from_pretrained(name).to(dev).eval()
lab = {v.lower(): int(k) for k, v in model.config.id2label.items()}
fraud = next(i for l, i in lab.items() if "fraud" in l or "scam" in l or "phish" in l)
print("labels", model.config.id2label, "fraud idx", fraud)
scores = []
with torch.no_grad():
    for i in range(0, len(ev), 64):
        enc = tok(ev.text.iloc[i:i + 64].tolist(), padding=True, truncation=True, max_length=128, return_tensors="pt").to(dev)
        scores.append(torch.softmax(model(**enc).logits.float(), -1)[:, fraud].cpu().numpy())
d = ev.assign(score=np.concatenate(scores))
neg = d[(d.set == "tg_dev") | ((d.set == "real_dev") & (d.label == 0))].score
out = {"model": rid}
for tag, thr in [("at_1pct_dev_fpr", pick_threshold(neg, 0.01)), ("at_default_0.5", 0.5)]:
    out[tag] = {"threshold": thr, "dev": dev_report(d, thr), "test": report(d, thr)}
os.makedirs(f"runs/{rid}", exist_ok=True)
d[["id", "set", "label", "language", "score", "text"]].to_json(f"runs/{rid}/preds.jsonl", orient="records", lines=True, force_ascii=False)
save(out, f"runs/{rid}/report.json")
from evaluate import summary_line
for tag in ["at_1pct_dev_fpr", "at_default_0.5"]:
    print(tag, summary_line(rid, out[tag]["test"]))
