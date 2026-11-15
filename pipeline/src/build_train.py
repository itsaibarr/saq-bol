"""Assemble train / synthetic-val / eval tables.

usage: python build_train.py [--kbd-aug 0|1] [--out data/processed/mix_kbd1]
Outputs train.jsonl, val.jsonl (synthetic/public held-out, for early stopping), eval.jsonl (all real and
held-out pools, with `set` column), stats.json.
"""
import argparse, glob, json, random, re, sys
from collections import Counter
import pandas as pd
sys.path.insert(0, "pipeline/src")
from textnorm import lang_tag, normalize, to_kbd

ap = argparse.ArgumentParser()
ap.add_argument("--kbd-aug", type=int, default=1)
ap.add_argument("--out", default="data/processed/mix")
ap.add_argument("--seed", type=int, default=7)
ap.add_argument("--dokster-kk", type=int, default=0)
ap.add_argument("--clips", type=int, default=0)
ap.add_argument("--hf-extra", type=int, default=0)
ap.add_argument("--chat-big", type=int, default=0)  # ~30k real chat negatives instead of 5.5k
ap.add_argument("--tg-spam-cap", type=int, default=1500)
ap.add_argument("--drop-pound", type=int, default=0)
ap.add_argument("--hfkk-frac", type=float, default=1.0)
ap.add_argument("--ru-rf", type=int, default=0)  # real Russian-language scam texts from non-KZ sources (training only)
ap.add_argument("--real-train-split", default="")  # A6: e.g. real_test -> spent test items become training rows
ap.add_argument("--real-weight", type=int, default=4)
ap.add_argument("--notif", type=int, default=0)  # rule-based legit service notifications
ap.add_argument("--hf-cap", type=int, default=8000)  # max rows per language from hf_extra  # add single-clause clips of synthetic messages  # A2: dropped (noisy NLLB, US content)
args = ap.parse_args()
rng = random.Random(args.seed)
rows = []


def add(text, label, language, source, scheme=None, group=None, **kw):
    t = normalize(text)
    if len(t) < 3:
        return
    rows.append({"text": t, "label": int(label), "language": language or lang_tag(t), "source": source,
                 "scheme": scheme, "group": group or f"{source}:{len(rows)}", **kw})


REASSURE = re.compile(r"(ничего не (говорите|сообщайте)|не (сообщайте|называйте) (мне |нам )?(код|sms|смс|данн)|"
                      r"мы не (спрашиваем|запрашиваем|просим)|никаких (данных|кодов) не|жеке дерек\w* сұрамаймыз|"
                      r"код\w* сұрамаймыз|ештеңе айтпаңыз|ешқандай (код|дерек)\w* сұрамай)")
n_reassure = 0
# 1. Synthetic KZ data (Claude generators, protocol in data/synthetic/GENERATION_PROTOCOL.md)
for f in sorted(glob.glob("data/synthetic/gen_G*.jsonl")):
    for i, ln in enumerate(open(f)):
        try:
            r = json.loads(ln)
        except json.JSONDecodeError:
            continue
        txt = r["text"]
        if r["label"] != "scam" and REASSURE.search(txt.lower()):
            n_reassure += 1
            continue  # A2: legit-only reassurance lines are a shortcut (real scammers say them too)
        if r["label"] != "scam" and r.get("channel") in ("sms", "messenger") and "[LINK]" not in txt and rng.random() < 0.2:
            txt = txt + rng.choice([" Подробнее: <url>", " Толығырақ: <url>", " <url>", " Детали в приложении: <url>"])
        add(txt, r["label"] == "scam", r.get("language"), f"synthetic_{r.get('group', 'G')}", r.get("scheme"),
            group=f"syn:{r.get('group')}:{i}", channel=r.get("channel"), synthetic=True)

# 2. dokster RU (+ its NLLB Kazakh translations share the group, so a pair never straddles train/val)
d = pd.read_json("data/raw/dokster_scam_ru_en/data/train_0.jsonl", lines=True)
d = d[d.language == "ru"]
for _, r in d.iterrows():
    m = re.search(r"Analyze this message for scam risk:\s*(.*?)\s*Return only the JSON object", str(r.user), re.S)
    rl = re.search(r'"risk_level":\s*"(\w+)"', str(r.assistant)); st = re.search(r'"scam_type":\s*"([^"]+)"', str(r.assistant))
    if not (m and rl) or rl.group(1) == "suspicious" or (st and st.group(1) == "government_impersonation"):
        continue
    text = re.sub(r"\s*(Ref|Note)\s*\d+\.?$", "", m.group(1).strip())
    add(text, rl.group(1) == "dangerous", "ru", "dokster_ru", st.group(1) if st else None, group=f"dok:{r.id}", synthetic=True)
try:
    for ln in (open("data/processed/dokster_kk_nllb.jsonl") if args.dokster_kk else []):
        try:
            r = json.loads(ln)
        except json.JSONDecodeError:
            continue  # last line may still be being written
        add(r["text"], r["label"] == "scam", "kk", "dokster_kk_nllb", r.get("scheme"), group=f"dok:{r['dokster_id']}",
            synthetic=True, translated=True)
except FileNotFoundError:
    pass

# 3. Real Russian Telegram spam (job / easy-income offers) and its ham (tech chat)
t = pd.read_parquet("data/raw/telegram_spam/data/train-00000-of-00001.parquet").sample(frac=1, random_state=1)
for _, r in t[t.label == 1].head(args.tg_spam_cap).iterrows():
    add(r.text, 1, None, "telegram_spam", "easy_income_offer")
for _, r in t[t.label == 0].head(1500).iterrows():
    add(r.text, 0, None, "telegram_ham")

# 4. FraudLens anti-fraud posts = texts that DESCRIBE scams -> legit hard negatives
fl = pd.read_json("data/raw/fraudlens_ru/fraudlens_v2_combined.jsonl", lines=True).sample(frac=1, random_state=2)
for _, r in fl.head(1500).iterrows():
    add(str(r.text_clean)[:600], 0, "ru", "fraudlens_warning", r.fraud_type)

# 4b. The same kind of warning posts machine-translated to Kazakh (legit hard negatives in Kazakh)
try:
    for ln in open("data/processed/fraudlens_kk_nllb.jsonl"):
        try:
            r = json.loads(ln)
        except json.JSONDecodeError:
            continue
        add(r["text"], 0, "kk", "fraudlens_kk_nllb", group=f"flkk:{r['fraudlens_id']}", translated=True)
except FileNotFoundError:
    pass

# 5. Real everyday KZ Telegram chat (train pool only; tg_neg_test is held out)
for ln in open("data/processed/tg_neg_train_big.jsonl" if args.chat_big else "data/processed/tg_neg_train.jsonl"):
    r = json.loads(ln)
    add(r["text"], 0, r["language"], "tg_chat")

# 6. Larger public scam/legit corpora from Hugging Face (hf_extra.jsonl, built by the ingestion step) and
#    their Kazakh machine translations (kk_tr_*_out.jsonl, NLLB-1.3B on Kaggle). Capped so they do not swamp KZ data.
if args.hf_extra:
    import os as _os
    if _os.path.exists("data/processed/hf_extra.jsonl"):
        hx = pd.read_json("data/processed/hf_extra.jsonl", lines=True)
        if args.drop_pound:
            hx = hx[~hx.text.str.contains("£|фунт|GBP", regex=True)]
        hx = pd.concat([g.sample(min(len(g), args.hf_cap), random_state=1) for _, g in hx.groupby("language")])
        for _, r in hx.iterrows():
            add(r.text, int(r.label), r.language if r.language in ("ru", "kk", "mixed", "kbd") else "en" if r.language == "en" else "other",
                f"hf:{r.source}", group=f"hf:{r.source}:{_}")
    for f in sorted(glob.glob("data/processed/kk_tr_*_out.jsonl")):
        for ln in open(f):
            try:
                r = json.loads(ln)
            except json.JSONDecodeError:
                continue
            if "£" in r.get("src_text", "") or "фунт" in r.get("src_text", "") or rng.random() > args.hfkk_frac:
                continue
            add(r["text"], int(r["label"]), "kk", f"hf_kk_nllb13b:{r.get('source')}", group=f"hftr:{r.get('id')}", translated=True)

# 8. Real Russian-language scam texts from non-Kazakhstan sources (T-J, Belarus/Uzbekistan banks), training only
if args.ru_rf:
    for i, ln in enumerate(open("data/train_extra/ru_rf_collected.jsonl")):
        r = json.loads(ln)
        add(r["text"], r["label"] == "scam", "ru", "ru_rf_real", r.get("scheme"), group=f"rurf:{i}")

# 9. A6: spent real items as training rows (descriptions dropped; fragments only if blind-tagged recognizable)
real_train_ids = set()
if args.real_train_split:
    _r = pd.read_json("data/processed/real_all.jsonl", lines=True)
    _r = _r[_r.split == args.real_train_split]
    for _, x in _r.iterrows():
        if x.unit == "description" or (x.unit == "fragment" and x.get("self_contained") not in ("yes", "maybe")):
            continue
        add(x.text, x.label == "scam", x.language, f"real_{args.real_train_split}", x.get("scheme"), group=f"real:{x.id}")
        real_train_ids.add(x.id)

# 7. Rule-based legit service notifications (bank OTP/transactions, eGov, delivery, telecom, civil defence)
if args.notif:
    for i, ln in enumerate(open("data/processed/notif_synth.jsonl")):
        r = json.loads(ln)
        add(r["text"], 0, r["language"], "notif_gen", group=f"notif:{i}", synthetic=True)
    if args.notif >= 2:  # scam twins: same formats, scam ask
        for i, ln in enumerate(open("data/processed/notif_scam_twins.jsonl")):
            r = json.loads(ln)
            add(r["text"], 1, r["language"], "notif_scam_twin", group=f"twin:{i}", synthetic=True)

# 5b. Real chat lines that contain links (excluded from the chat test pool), so "<url>" is not a scam-only token
seen_link = 0
for ln in open("data/raw/tg_ru_kk/telegram_data.txt", encoding="utf-8", errors="ignore"):
    t_ = ln.strip()
    if ("http" in t_ or "t.me/" in t_) and 20 <= len(t_) <= 400 and rng.random() < 0.08:
        add(t_, 0, None, "tg_chat_links"); seen_link += 1
        if seen_link >= 1000:
            break

df = pd.DataFrame(rows)

# Leakage filter vs every real item: char 5-gram Jaccard >= 0.5 -> drop the training row
def grams(s, n=5):
    s = re.sub(r"\s+", " ", s.lower())
    return {s[i:i + n] for i in range(max(1, len(s) - n + 1))}
real = pd.read_json("data/processed/real_all.jsonl", lines=True)
if args.real_train_split:
    real = real[real.split != args.real_train_split]  # protect only items still held out
rg = [grams(x) for x in real.text]
def leaks(s):
    g = grams(s)
    return any(len(g & h) / max(1, len(g | h)) >= 0.5 for h in rg)
df["leak"] = df.text.map(leaks)
n_leak = int(df.leak.sum())
leak_examples = df[df.leak].text.head(10).tolist()
from embed import embed
import numpy as np
Er = embed(real.text.tolist()); Et = embed(df.text.tolist())
df["max_cos_real"] = (Et @ Er.T).max(1)
df["leak"] = df.leak | (df.max_cos_real >= 0.92)
n_leak = int(df.leak.sum())
leak_examples = df[df.leak].text.head(15).tolist()
df = df[~df.leak].drop(columns=["leak"])
df = df.drop_duplicates("text")

# Clip augmentation (optional): real call phrases are single clauses, synthetic scams are whole messages.
# Scam clips must carry an official red flag (keyword_rule); legit clips must not, so no clip contradicts its parent label.
if args.clips:
    import keyword_rule
    clips = []
    syn = df[df.source.str.startswith("synthetic_") | (df.source == "dokster_ru")]
    for _, r in syn.iterrows():
        parts = [p.strip(" -–—•") for p in re.split(r"(?<=[.!?;])\s+|\n+", r.text) if p.strip()]
        if len(parts) < 2:
            continue
        for ptxt in parts:
            nw = len(ptxt.split())
            if not 4 <= nw <= 16:
                continue
            flagged = keyword_rule.score(ptxt) >= 1
            if (r.label == 1 and flagged) or (r.label == 0 and not flagged):
                clips.append({**r.to_dict(), "text": ptxt, "source": r.source + "+clip"})
    cdf = pd.DataFrame(clips)
    if len(cdf):
        cdf = cdf.drop_duplicates("text")
        cdf["max_cos_real"] = (embed(cdf.text.tolist()) @ Er.T).max(1)
        bad = cdf.text.map(leaks) | (cdf.max_cos_real >= 0.92)
        n_leak += int(bad.sum()); leak_examples += cdf[bad].text.head(10).tolist()
        cdf = cdf[~bad]
        print("clips added:", dict(Counter(cdf.label)), "clip leaks dropped:", int(bad.sum()))
        df = pd.concat([df, cdf], ignore_index=True).drop_duplicates("text")

# train / val split by group (val = 12% of groups)
groups = sorted(df.group.unique()); rng.shuffle(groups)
val_groups = set(groups[: int(0.12 * len(groups))])
df["split"] = df.group.map(lambda g: "val" if g in val_groups and not str(g).startswith("real:") else "train")

# Keyboard-Kazakh augmentation (train only): folded copy of 60% of Kazakh rows
if args.kbd_aug:
    kk = df[(df.split == "train") & (df.language.isin(["kk", "mixed"]))]
    aug = kk.sample(frac=0.6, random_state=args.seed).copy()
    aug["text"] = [to_kbd(x, p=rng.uniform(0.7, 1.0), seed=rng.randint(0, 10**9)) for x in aug.text]
    aug["language"] = aug.language.map(lambda l: "kbd" if l == "kk" else "mixed")
    aug["source"] = aug.source + "+kbd_aug"
    df = pd.concat([df, aug], ignore_index=True).drop_duplicates("text")

if args.real_train_split and args.real_weight > 1:
    _rr = df[(df.split == "train") & df.source.astype(str).str.startswith("real_")]
    df = pd.concat([df] + [_rr] * (args.real_weight - 1), ignore_index=True)
import os
os.makedirs(args.out, exist_ok=True)
df[df.split == "train"].to_json(f"{args.out}/train.jsonl", orient="records", lines=True, force_ascii=False)
val = df[df.split == "val"].assign(set="synthetic_val")

# Eval table: real-dev, real-test, kbd-perturbed real, Telegram chat dev/test, synthetic val
real = real.assign(label=(real.label == "scam").astype(int), set=real.split)
kb = pd.read_json("data/processed/real_kbd_perturbed.jsonl", lines=True)
kb = kb.assign(label=(kb.label == "scam").astype(int), set="kbd_perturbed")
tg = pd.read_json("data/processed/tg_neg_test.jsonl", lines=True).sample(frac=1, random_state=3).reset_index(drop=True)
tg = tg.assign(label=0, set=["tg_dev" if i < 0.3 * len(tg) else "tg_test" for i in range(len(tg))], id=[f"tg_{i}" for i in range(len(tg))])
ev = pd.concat([real, kb, tg, val], ignore_index=True)
ev["id"] = ev["id"].fillna(pd.Series([f"val_{i}" for i in range(len(ev))]))
ev.to_json(f"{args.out}/eval.jsonl", orient="records", lines=True, force_ascii=False)
val.to_json(f"{args.out}/val.jsonl", orient="records", lines=True, force_ascii=False)

tr = df[df.split == "train"]
stats = {"reassure_dropped": n_reassure, "kbd_aug": args.kbd_aug, "n_train": len(tr), "n_val": len(val), "leak_dropped": n_leak, "leak_examples": leak_examples,
         "train_label": dict(Counter(tr.label)), "train_lang_x_label": {f"{l}|{y}": int(n) for (l, y), n in tr.groupby(["language", "label"]).size().items()},
         "train_source": dict(Counter(tr.source)), "eval_sets": dict(Counter(ev.set))}
json.dump(stats, open(f"{args.out}/stats.json", "w"), ensure_ascii=False, indent=1)
print(json.dumps({k: v for k, v in stats.items() if k != "leak_examples"}, ensure_ascii=False, indent=1))
