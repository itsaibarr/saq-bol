"""A6: build fresh test set B from round-3 collections (and the user's own SMS if provided).

Drops (blind to model scores): exact duplicates of any earlier real item; near-copies (LaBSE cosine >= 0.90 or char
5-gram Jaccard >= 0.5) of any v7 training row or dev item. Writes data/processed/testB.jsonl and
<mix>/eval_testB.jsonl = dev/chat rows of the mix eval + test B rows (set real_test) + keyboard-folded Kazakh copies.
usage: python build_testB.py data/processed/mix_v7
"""
import glob, json, os, re, sys
import numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(__file__))
from build_real import SEEN, HELD_OUT_BY_DESIGN
from embed import embed
from textnorm import lang_tag, normalize, to_kbd

mix = sys.argv[1]
files = [f for f in ["data/real_test/kk3_collected.jsonl", "data/real_test/ru3_collected.jsonl", "data/real_test/user_sms.jsonl"] if os.path.exists(f)]
b = pd.concat([pd.read_json(f, lines=True) for f in files], ignore_index=True)
b["text"] = b.text.map(normalize)
b = b[b.text.str.len() >= 3].drop_duplicates("text")
n0 = len(b)
old = pd.read_json("data/processed/real_all.jsonl", lines=True)
b = b[~b.text.isin(set(old.text))]
tr = pd.read_json(f"{mix}/train.jsonl", lines=True).drop_duplicates("text")
dev = old[old.split == "real_dev"]
ref_texts = list(tr.text) + list(dev.text)


def grams(s, n=5):
    s = re.sub(r"\s+", " ", s.lower())
    return {s[i:i + n] for i in range(max(1, len(s) - n + 1))}


rg = [grams(x) for x in dev.text]
Eb, Er = embed(b.text.tolist()), embed(ref_texts)
b["max_cos_ref"] = (Eb @ Er.T).max(1)
b["jacc_dev"] = [max((len(g & h) / max(1, len(g | h)) for h in rg), default=0) for g in map(grams, b.text)]
b["drop"] = (b.max_cos_ref >= 0.90) | (b.jacc_dev >= 0.5)
dropped = b[b["drop"]]
b = b[~b["drop"]].copy()
b["n_words"] = b.text.str.split().str.len()


def unit(x):
    if x.label == "scam":
        if x.get("kind") == "paraphrase":
            return "description"
        if x.n_words <= 4:
            return "fragment"
        return "call_phrase" if x.get("kind") == "call_quote" else "message"
    return "notification" if x.get("kind") in ("sms", "push") or x.get("source") == "user_sms" else "advice_text"


b["unit"] = b.apply(unit, axis=1)
b["headline"] = b.unit.isin(["message", "call_phrase"])
b["language"] = [l if l in ("kk", "ru", "mixed") else lang_tag(t) for l, t in zip(b.language, b.text)]
b["year"] = b.published_date.astype(str).str[:4] if "published_date" in b else ""
b["novel_scheme"] = (b.label == "scam") & ~b.scheme.isin(SEEN)
b["held_out_by_design"] = b.scheme.isin(HELD_OUT_BY_DESIGN)
b["evidence"] = "quoted"; b["split"] = "real_test"; b["set"] = "real_test"; b["label"] = (b.label == "scam").astype(int)
b["group"] = b.source_url.astype(str); b["pair_id"] = None
b.to_json("data/processed/testB.jsonl", orient="records", lines=True, force_ascii=False)
kb = b[b.language == "kk"].copy()
kb["text"] = [to_kbd(t, p=1.0) for t in kb.text]; kb["id"] = kb.id + "_kbd"; kb["set"] = "kbd_perturbed"; kb["language"] = "kbd_perturbed"
ev = pd.read_json(f"{mix}/eval.jsonl", lines=True)
ev = ev[ev.set.isin(["real_dev", "tg_dev", "tg_test"])]
pd.concat([ev, b, kb], ignore_index=True).to_json(f"{mix}/eval_testB.jsonl", orient="records", lines=True, force_ascii=False)
print(f"collected {n0} | new {n0 - len(dropped) - (n0 - len(b) - len(dropped))} | dropped as near-copies {len(dropped)} | kept {len(b)}")
print(pd.crosstab([b.label, b.unit], b.language))
print("headline scams by language:", b[(b.label == 1) & b.headline].language.value_counts().to_dict())
