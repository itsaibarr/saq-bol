"""A7: build fresh test set C (Kazakhstan: ru4, ru4b, kk4; non-Kazakhstan Russian stratum: rucis).

Drops (blind to model scores): exact copies of any earlier real item (real_all, test B); near-copies (LaBSE >= 0.90 or
char 5-gram Jaccard >= 0.5) of any earlier real item, dev item or v2 (mix_v7) training row; cross-file near-duplicates
within test C (first kept). Writes data/processed/testC.jsonl and <mix>/eval_testC.jsonl = dev/chat rows of the mix eval
+ test C (set real_test, or real_test_cis for the non-KZ stratum) + keyboard-folded Kazakh copies.
usage: python build_testC.py data/processed/mix_v8
"""
import glob, hashlib, json, os, re, sys
import numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(__file__))
from build_real import SEEN, HELD_OUT_BY_DESIGN
from embed import embed
from textnorm import lang_tag, normalize, to_kbd

mix = sys.argv[1]
files = [f for f in ["data/real_test/ru4_collected.jsonl", "data/real_test/ru4b_collected.jsonl",
                     "data/real_test/kk4_collected.jsonl", "data/real_test/rucis_collected.jsonl"] if os.path.exists(f)]
c = pd.concat([pd.read_json(f, lines=True).assign(file=os.path.basename(f)) for f in files], ignore_index=True)
EXCLUDE = {"rucis_075": "prize SMS a regulator ruled misleading advertising, not fraud (label ambiguous; excluded before scoring)"}
c = c[~c.id.isin(EXCLUDE)]
c["text"] = c.text.map(normalize)
c = c[c.text.str.len() >= 3].drop_duplicates("text")
n0 = len(c)
old = pd.concat([pd.read_json("data/processed/real_all.jsonl", lines=True), pd.read_json("data/processed/testB.jsonl", lines=True)])
c = c[~c.text.isin(set(old.text))]
n_exact = n0 - len(c)
norm_url = lambda u: str(u).strip().rstrip("/").replace("://www.", "://").lower()
own = set(c.source_url.map(norm_url))  # used_urls.txt lists test C's own pages since the 15:41 lock (that build found 0 items on earlier pages)
used = ({norm_url(u) for u in open("data/real_test/used_urls.txt").read().split()} - own) | {norm_url(u) for u in old.get("source_url", pd.Series(dtype=str)).dropna()}
on_used_page = c.source_url.map(norm_url).isin(used)
print("items from pages used in earlier sets (dropped):", int(on_used_page.sum()))
c = c[~on_used_page]
v7 = pd.read_json("data/processed/mix_v7/train.jsonl", lines=True).drop_duplicates("text")
ref = list(dict.fromkeys(list(old.text) + list(v7.text)))


def grams(s, n=5):
    s = re.sub(r"\s+", " ", s.lower())
    return {s[i:i + n] for i in range(max(1, len(s) - n + 1))}


cg = [grams(x) for x in c.text]
Ec, Er = embed(c.text.tolist()), embed(ref)
c["max_cos_ref"] = (Ec @ Er.T).max(1)
c["max_jacc_ref"] = 0.0
for j, g in enumerate(map(grams, ref)):  # one pass over the reference, vectorised over test C
    jac = np.array([len(g & h) / max(1, len(g | h)) for h in cg])
    c["max_jacc_ref"] = np.maximum(c.max_jacc_ref.values, jac)
c["drop"] = (c.max_cos_ref >= 0.90) | (c.max_jacc_ref >= 0.5)
# cross-file near-duplicates inside test C: keep the first
S = Ec @ Ec.T
keep = np.ones(len(c), bool)
for i in range(len(c)):
    if keep[i]:
        for j in range(i + 1, len(c)):
            if keep[j] and (S[i, j] >= 0.92 or len(cg[i] & cg[j]) / max(1, len(cg[i] | cg[j])) >= 0.5):
                keep[j] = False
c["drop_internal"] = ~keep
dropped = c[c["drop"] | c.drop_internal]
c = c[~(c["drop"] | c.drop_internal)].copy()
c["n_words"] = c.text.str.split().str.len()


def unit(x):
    if x.label == "scam":
        if x.get("kind") == "paraphrase":
            return "description"
        if x.n_words <= 4:
            return "fragment"
        return "call_phrase" if x.get("kind") == "call_quote" else "message"
    return "notification" if x.get("kind") in ("sms", "push") else "advice_text"


c["unit"] = c.apply(unit, axis=1)
c["headline"] = c.unit.isin(["message", "call_phrase"])
c["language"] = [l if l in ("kk", "ru", "mixed") else lang_tag(t) for l, t in zip(c.language, c.text)]
c["year"] = c.published_date.astype(str).str[:4]
c["novel_scheme"] = (c.label == "scam") & ~c.scheme.isin(SEEN)
c["held_out_by_design"] = c.scheme.isin(HELD_OUT_BY_DESIGN)
c["evidence"] = "quoted"; c["label"] = (c.label == "scam").astype(int)
c["stratum"] = np.where(c.file == "rucis_collected.jsonl", "cis", "kz")
c["split"] = np.where(c.stratum == "cis", "real_test_cis", "real_test"); c["set"] = c.split
c["group"] = c.source_url.astype(str); c["pair_id"] = None
if os.path.exists("data/processed/testC_selfcontained.jsonl"):  # blind annotation, done without model scores
    t = {json.loads(l)["id"]: json.loads(l)["self_contained"] for l in open("data/processed/testC_selfcontained.jsonl")}
    c["self_contained"] = c.id.map(t)
c.to_json("data/processed/testC.jsonl", orient="records", lines=True, force_ascii=False)
kb = c[(c.language == "kk") & (c.stratum == "kz")].copy()
kb["text"] = [to_kbd(t, p=1.0) for t in kb.text]; kb["id"] = kb.id + "_kbd"; kb["set"] = "kbd_perturbed"; kb["language"] = "kbd_perturbed"
if os.path.exists(f"{mix}/eval.jsonl"):
    ev = pd.read_json(f"{mix}/eval.jsonl", lines=True)
    ev = ev[ev.set.isin(["real_dev", "tg_dev", "tg_test"])]
    pd.concat([ev, c, kb], ignore_index=True).to_json(f"{mix}/eval_testC.jsonl", orient="records", lines=True, force_ascii=False)
print(f"collected {n0} | exact repeats of earlier items {n_exact} | near-copies of earlier real/dev/v2-train {int(dropped['drop'].sum())} "
      f"| internal near-duplicates {int(dropped.drop_internal.sum() - (dropped['drop'] & dropped.drop_internal).sum())} | kept {len(c)}")
print(pd.crosstab([c.stratum, c.label, c.unit], c.language))
print("headline scams:", c[(c.label == 1) & c.headline].groupby(["stratum", "language"]).size().to_dict())
print("publishers per stratum:", c.groupby("stratum").publisher.nunique().to_dict(), "| max items per publisher:", c.publisher.value_counts().head(3).to_dict())
print("sha256 testC.jsonl:", hashlib.sha256(open("data/processed/testC.jsonl", "rb").read()).hexdigest()[:16])
