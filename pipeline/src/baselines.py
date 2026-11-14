"""Baselines (hyper-parameters fixed in advance, never tuned), scored under amendment A2.

B0 all-safe | BL length-only (shorter = more suspicious) | B1 official red-flag keyword rule
B2 generic spam model (English SMS Spam + Russian spam corpus) | B3 TF-IDF char 1-5 + LR on our mix
B5 off-the-shelf multilingual scam model (scores reused from runs/B5_offshelf_scam_model/preds.jsonl)
Every model's threshold: <=1% FPR on everyday-chat dev. B1 is also shown at its natural rule (>=1 red flag).
usage: python baselines.py <mix_dir>
"""
import os, sys
import numpy as np, pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
sys.path.insert(0, os.path.dirname(__file__))
import keyword_rule
from evaluate import dev_report, operating_threshold, pick_threshold, report, save, summary_line
from textnorm import normalize

mix = sys.argv[1] if len(sys.argv) > 1 else "data/processed/mix_v3"
ev = pd.read_json(f"{mix}/eval.jsonl", lines=True)
tr = pd.read_json(f"{mix}/train.jsonl", lines=True)
rng = np.random.default_rng(0)


def tfidf_lr():
    return make_pipeline(TfidfVectorizer(analyzer="char_wb", ngram_range=(1, 5), min_df=2, sublinear_tf=True, max_features=300_000),
                         LogisticRegression(C=4.0, class_weight="balanced", max_iter=3000))


def finish(name, scores, thr=None):
    d = ev.assign(score=np.asarray(scores, dtype=float) + rng.uniform(0, 1e-9, len(ev)))  # tie-break for count-valued scores
    thr = operating_threshold(d) if thr is None else thr
    out = {"model": name, "threshold": thr, "dev": dev_report(d, thr), "test": report(d, thr)}
    os.makedirs(f"runs/{name}", exist_ok=True)
    d[["id", "set", "label", "language", "score", "text"]].to_json(f"runs/{name}/preds.jsonl", orient="records", lines=True, force_ascii=False)
    save(out, f"runs/{name}/report.json")
    print(summary_line(name, out["test"]))
    return out


finish("B0_all_safe", np.zeros(len(ev)), thr=0.5)
finish("BL_length_only", 1.0 / (1 + ev.text.str.split().str.len()))
kw = ev.text.map(keyword_rule.score).values
finish("B1_keyword_rule", kw)
finish("B1_keyword_rule_natural", kw, thr=1.0)

sms = pd.read_parquet("data/raw/sms_spam_en/plain_text/train-00000-of-00001.parquet")
ru = pd.read_csv("data/raw/anti_spam_ru/df.csv").dropna().sample(20000, random_state=0)
b2 = tfidf_lr().fit([normalize(x) for x in list(sms.sms) + list(ru.text)], list(sms.label) + list(ru.is_spam))
finish("B2_generic_spam_model", b2.predict_proba(ev.text)[:, 1])

b3 = tfidf_lr().fit(tr.text, tr.label)
finish("B3_tfidf_our_mix", b3.predict_proba(ev.text)[:, 1])
# P4 ablation on the cheap model: same mix without keyboard-Kazakh augmentation rows
tr0 = tr[~tr.source.astype(str).str.endswith("+kbd_aug")]
b3n = tfidf_lr().fit(tr0.text, tr0.label)
finish("B3_tfidf_no_kbd_aug", b3n.predict_proba(ev.text)[:, 1])

b5p = "runs/B5_offshelf_scam_model/preds.jsonl"
if os.path.exists(b5p):
    p5 = pd.read_json(b5p, lines=True)[["id", "set", "score"]].drop_duplicates(["id", "set"])
    m = ev[["id", "set"]].merge(p5, on=["id", "set"], how="left")
    if m.score.isna().any():  # rows not scored before (e.g. a new synthetic_val): neutral score, excluded from real metrics anyway
        m["score"] = m.score.fillna(0.0)
    finish("B5_offshelf_scam_model", m.score.values)
