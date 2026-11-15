"""A8: existing tools on test C, scored once each (comparison only; no model is changed or selected).

B1 official red-flag keyword rule (A4 threshold and its own >=1-flag setting) | B2 generic spam filter (same fixed data
and seed as baselines.py) | B5 Horizon-Labs/phishing-scam-detector-base as is. Thresholds: A4 rule on dev.
usage: python baselines_testC.py data/processed/mix_v8
"""
import os, sys
import numpy as np, pandas as pd, torch
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from transformers import AutoModelForSequenceClassification, AutoTokenizer
sys.path.insert(0, os.path.dirname(__file__))
import keyword_rule
from evaluate import dev_report, operating_threshold, report, save, summary_line
from textnorm import normalize

mix = sys.argv[1]
ev = pd.read_json(f"{mix}/eval_testC.jsonl", lines=True)
rng = np.random.default_rng(0)


def finish(name, scores, thr=None):
    d = ev.assign(score=np.asarray(scores, dtype=float) + rng.uniform(0, 1e-9, len(ev)))  # tie-break for count-valued scores
    thr = operating_threshold(d) if thr is None else thr
    out = {"model": name, "threshold": thr, "dev": dev_report(d, thr), "test": report(d, thr), "test_cis": report(d, thr, split="real_test_cis")}
    os.makedirs(f"runs/{name}", exist_ok=True)
    d[["id", "set", "label", "language", "score", "text"]].to_json(f"runs/{name}/preds_testC.jsonl", orient="records", lines=True, force_ascii=False)
    save(out, f"runs/{name}/report_testC.json")
    print(f"thr {thr:.6f}", summary_line(name, out["test"]), "| outside KZ", out["test_cis"]["headline"]["recall"]["rate"])


kw = ev.text.map(keyword_rule.score).values
finish("B1_keyword_rule", kw)
finish("B1_keyword_rule_natural", kw, thr=1.0)

sms = pd.read_parquet("data/raw/sms_spam_en/plain_text/train-00000-of-00001.parquet")
ru = pd.read_csv("data/raw/anti_spam_ru/df.csv").dropna().sample(20000, random_state=0)
b2 = make_pipeline(TfidfVectorizer(analyzer="char_wb", ngram_range=(1, 5), min_df=2, sublinear_tf=True, max_features=300_000),
                   LogisticRegression(C=4.0, class_weight="balanced", max_iter=3000))
b2.fit([normalize(x) for x in list(sms.sms) + list(ru.text)], list(sms.label) + list(ru.is_spam))
finish("B2_generic_spam_model", b2.predict_proba(ev.text)[:, 1])

name = "Horizon-Labs/phishing-scam-detector-base"
dev = "mps" if torch.backends.mps.is_available() else ("cuda" if torch.cuda.is_available() else "cpu")
tok = AutoTokenizer.from_pretrained(name)
model = AutoModelForSequenceClassification.from_pretrained(name).to(dev).eval()
fraud = next(int(k) for k, v in model.config.id2label.items() if any(w in v.lower() for w in ("fraud", "scam", "phish")))
out = []
with torch.no_grad():
    for i in range(0, len(ev), 64):
        enc = tok(ev.text.iloc[i:i + 64].tolist(), padding=True, truncation=True, max_length=128, return_tensors="pt").to(dev)
        out.append(torch.softmax(model(**enc).logits.float(), -1)[:, fraud].cpu().numpy())
finish("B5_offshelf_scam_model", np.concatenate(out))
