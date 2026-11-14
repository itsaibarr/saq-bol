"""Extra public HF training data -> data/processed/hf_extra.jsonl (+ report, + Kazakh-MT candidate pool).

usage: .venv/bin/python pipeline/src/build_hf_extra.py
Downloads (if missing) into data/raw/hf_extra/<name>/, maps each source to scam(1)/legit(0) with the
decisions documented in NOTES, filters 3-80 words, dedups, caps (15k/dataset, 20k/language; ru > en > rest),
drops leaks vs data/processed/real_all.jsonl (exact or char-5gram Jaccard >= 0.5).
"""
import glob, hashlib, json, os, random, re, sys
from collections import Counter, defaultdict
import pandas as pd
sys.path.insert(0, "pipeline/src")
from textnorm import lang_tag, normalize

RAW = "data/raw/hf_extra"
OUT = "data/processed"
rng = random.Random(11)
REPOS = {  # name: (repo, allow_patterns)
    "scambench": ("shaw/scambench-training", ["data/*", "README.md"]),
    "fredzhang_allscam": ("FredZhang7/all-scam-spam", None),
    "bothbosu_dialogue": ("BothBosu/scam-dialogue", None),
    "bothbosu_single": ("BothBosu/single-agent-scam-conversations", None),
    "bothbosu_multi": ("BothBosu/multi-agent-scam-conversation", None),
    "bothbosu_youtube": ("BothBosu/youtube-scam-conversations", None),
    "bothbosu_scammerconv": ("BothBosu/Scammer-Conversation", None),
    "anmol_india14": ("anmolshrivastav/scam_ham_india_14_languages", None),
    "ridham_indian": ("Ridham115/indian-scam-sms-synthetic-audited", None),
    "bektemir_uzru": ("Bektemir96az96/Uzbek_and_Russian_Phishing_dataset", None),
    "sms_multiling": ("dbarbedillo/SMS_Spam_Multilingual_Collection_Dataset", None),
    "scamguardbench": ("flowxai/scamguardbench", ["v0.2/*", "README.md"]),
    "hinglish_calls": ("ysangam/Indian_Cyber_Scam_PhoneCall_Hinglish_Dataset", None),
    "rasheq_sms": ("rasheq/scam-shield-sms", None),
    "smishing_az": ("VusalShahbazovAz/smishing-AZ-SC", None),
}
LICENSE = {"shaw/scambench-training": "cc-by-sa-4.0", "FredZhang7/all-scam-spam": "apache-2.0",
           "anmolshrivastav/scam_ham_india_14_languages": "mit", "Ridham115/indian-scam-sms-synthetic-audited": "cc-by-4.0",
           "Bektemir96az96/Uzbek_and_Russian_Phishing_dataset": "apache-2.0",
           "dbarbedillo/SMS_Spam_Multilingual_Collection_Dataset": "gpl", "flowxai/scamguardbench": "apache-2.0",
           "ysangam/Indian_Cyber_Scam_PhoneCall_Hinglish_Dataset": "apache-2.0", "rasheq/scam-shield-sms": "cc-by-4.0",
           "VusalShahbazovAz/smishing-AZ-SC": "cc-by-4.0", "DmitryKRX/anti_spam_ru": "apache-2.0"}
LICENSE.update({r: "apache-2.0" for r in ["BothBosu/scam-dialogue", "BothBosu/single-agent-scam-conversations",
                "BothBosu/multi-agent-scam-conversation", "BothBosu/youtube-scam-conversations", "BothBosu/Scammer-Conversation"]})


def fetch():
    from huggingface_hub import snapshot_download
    for name, (repo, pat) in REPOS.items():
        if not os.path.isdir(f"{RAW}/{name}") or not any(f.endswith((".csv", ".parquet", ".json", ".jsonl"))
                                                          for f in glob.glob(f"{RAW}/{name}/**/*", recursive=True)):
            snapshot_download(repo, repo_type="dataset", local_dir=f"{RAW}/{name}", allow_patterns=pat, max_workers=4)


rows = []


def add(text, label, source, kind, language=None):
    """language=None -> lang_tag (Cyrillic sources); otherwise the source's ISO code (Cyrillic text is still lang_tagged)."""
    t = normalize(text)
    t = re.sub(r"\s*\n\s*", " ", t).strip()
    if not 3 <= len(t.split()) <= 80:
        return
    if language is None:
        language = lang_tag(t)
    rows.append({"text": t, "label": int(label), "language": language, "source": source,
                 "license": LICENSE[source], "kind": kind})


# Social-engineering filter for corpora whose "spam" class is mostly advertising (pharma, watches, software, loans...).
SCAM_EN = re.compile(r"\b(you('ve| have)? (won(?!['’]t)|been selected)|winner|prize|lottery|jackpot|claim|award|urgent|"
                     r"account (has been |is |will be )?(suspended|locked|blocked|limited|compromised|closed|deactivated)|"
                     r"verify your|confirm your (account|identity|details|password|information)|update your (account|details|"
                     r"information|billing|payment)|password|login details|bank account|card details|social security|"
                     r"inheritance|beneficiary|next of kin|transfer (of )?(the )?(funds|sum)|million (us )?(dollars|usd|pounds|euros)|"
                     r"investment opportunity|guaranteed (return|profit|income)|double your|bitcoin|crypto|work from home|refund|"
                     r"tax rebate|irs|parcel|delivery (fee|failed|attempt)|customs|otp|security (alert|department)|"
                     r"suspicious (activity|login|transaction)|unusual activity|gift card|wire transfer|western union|moneygram)\b")
ADS_EN = re.compile(r"viagra|cialis|pharm|\bpills?\b|\bmeds\b|medication|prescription|rolex|replica|watch(es)?\b|software|"
                    r"\boem\b|adobe|\bsex|porn|xxx|adult|dating|singles|penis|enlarg|weight|diet|casino|mortgage|refinanc|"
                    r"\bloans?\b|stock|ringtone|\btones?\b|chat ?line|horny|babe")
SCAM_RU = re.compile(r"выигр|приз[ауоеы ]|призов|розыгрыш|победител|лотере|джекпот|наследств|компенсац|выплат|"
                     r"заблокир|взлом|приостановл|подтвердите (свои |ваши )?(данные|личность|пароль|учетн|аккаунт)|пароль|"
                     r"код из (смс|sms)|персональн\w* данн|данн\w* (вашей )?карт|номер\w* карт|cvv|служб\w* безопасности|"
                     r"подозрительн\w* (операци|транзакц|активн)|инвестиц|гарантированн\w* (доход|прибыл)|пассивн\w* доход|"
                     r"разбогате|удво|криптовалют|биткоин|перевед\w* (деньги|средства)|безопасн\w* сч[её]т|предоплат|"
                     r"посылк|штраф|госуслуг")
ADS_RU = re.compile(r"виагр|сиали|аптек|лекарств|таблет|секс|порно|эроти|знакомств|похуд|диет|казино|кредит|займ|скидк|"
                    r"распродаж|подписчик|лайк|реклам|акци[ия] |товар|шанс|\bstop\b|\bстоп\b|поделит|поделив|#\w")
# Fred's spam e-mails: only unmistakable phishing / 419 / prize mails count as scam
STRONG_EN = re.compile(r"account (has been |is |will be )?(suspended|locked|blocked|limited|compromised|closed)|verify your|"
                       r"confirm your|password|bank account|inheritance|beneficiary|next of kin|million|lottery|winner|prize")
EN_WORDS = re.compile(r"(?i)\b(the|you|your|to|and|is|for|of|in|it|me|my|we|are|this|have)\b")
AZ_SCAM = re.compile(r"mükafat|mukafat|qazan|təcili|tecili|hesab|kart|şifr|sifr|təsdiq|tesdiq|çatdırılma|catdirilma|vergi|"
                     r"cərimə|cerime|bank|kapital|azərpoçt|azerpoct|\bkod|giriş|giris|blok|<url>")
AZ_ADS = re.compile(r"zəng ton|zeng ton|dəqiqə|deqiqe|video telefon|endirim|kupon")


def is_scam_en(t):
    t = t.lower()
    return bool(SCAM_EN.search(t)) and not ADS_EN.search(t)


def turns(text, speakers):
    parts = re.split(r"(?i)\b(" + "|".join(speakers) + r")\s*:", str(text))
    return [(parts[i].lower(), parts[i + 1].strip()) for i in range(1, len(parts) - 1, 2)]


def load_all():
    # --- Russian first (priority language) ---
    # DmitryKRX/anti_spam_ru (already in data/raw/anti_spam_ru via fetch_raw.py)
    a = pd.read_csv("data/raw/anti_spam_ru/df.csv")
    for t, y in zip(a.text.fillna("").astype(str), a.is_spam):
        lo = t.lower()
        if y == 1 and not (SCAM_RU.search(lo) and not ADS_RU.search(lo)):
            continue  # advertising spam dropped
        if y == 1 and "разбогате" in lo and rng.random() > 0.25:
            continue  # ~600 near-identical "get rich quick" posts: keep a quarter
        n = len(rows); add(t, y, "DmitryKRX/anti_spam_ru", "message")
        if len(rows) > n and rows[-1]["language"] not in ("ru", "mixed", "kk"):
            rows.pop()  # Latin-only / junk rows

    # shaw/scambench-training: only the hand-built culture-specific subset; scam payload = last user turn,
    # legit = inquiry turns (filler small talk shared with scam conversations is skipped)
    sb = pd.concat([pd.read_parquet(f) for f in glob.glob(f"{RAW}/scambench/data/*/*.parquet")])
    sb = sb[sb.source_dataset.str.startswith("generated-culture")]
    users = [[m["content"] for m in json.loads(x) if m["role"] == "user"] for x in sb.messages]
    filler = {u for us, y in zip(users, sb.should_trigger_scam_defense) if y for u in us[:-1]}
    for us, y, lang, sv in zip(users, sb.should_trigger_scam_defense, sb.language, sb.style_variant):
        sv = sv.lower()
        kind = ("sms" if any(k in sv for k in ("sms", "смс", "एसएमएस", "نصية")) else "call_turn" if "звонок" in sv else
                "email" if any(k in sv for k in ("почта", "email", "ईमेल", "بريد")) else "message")
        lng = None if lang == "ru" else lang
        if y:
            add(us[-1], 1, "shaw/scambench-training", kind, lng)
        else:
            for u in us:
                if u not in filler:
                    add(u, 0, "shaw/scambench-training", kind, lng)

    # Bektemir96az96 Uzbek+Russian phishing: NOTE label is inverted in the source (0 = phishing, 1 = legitimate)
    b = pd.read_csv(f"{RAW}/bektemir_uzru/phishing_legitimate_dataset.csv")
    for t, y in zip(b.text, b.label):
        cyr = bool(re.search(r"[А-Яа-я]", t))
        add(t, 1 - y, "Bektemir96az96/Uzbek_and_Russian_Phishing_dataset", "sms", None if cyr else "uz")

    # dbarbedillo SMS Spam Multilingual (UCI SMS, M2M100 machine translation): Russian column only.
    # spam -> scam only if the English original is a fake prize / account / claim message; ad spam dropped.
    s = pd.read_csv(f"{RAW}/sms_multiling/data-augmented.csv")
    for en, ru, y in zip(s.text.fillna("").astype(str), s.text_ru.fillna("").astype(str), s.labels):
        if y == "spam" and not is_scam_en(en):
            continue
        if ru.strip().lower() == en.strip().lower() or len(set(ru.split())) < 0.5 * len(ru.split()):
            continue  # untranslated or degenerate MT repetition
        n = len(rows); add(ru, y == "spam", "dbarbedillo/SMS_Spam_Multilingual_Collection_Dataset", "sms")
        if len(rows) > n and rows[-1]["language"] != "ru":
            rows.pop()
    # MT ham is low quality: keep at most 3x the scam count so "broken Russian" does not become a legit cue
    mt = [r for r in rows if r["source"].startswith("dbarbedillo")]
    n_scam = sum(r["label"] for r in mt)
    drop = {id(r) for r in rng.sample([r for r in mt if not r["label"]], max(0, len(mt) - 4 * n_scam))}
    rows[:] = [r for r in rows if id(r) not in drop]

    # --- English + others ---
    # BothBosu dialogues: caller turns only (scam dialogue -> scammer turns = 1; legit dialogue -> caller turns = 0)
    for f, col, spk, caller in [("bothbosu_dialogue/scam-dialogue_all.csv", "label", ["caller", "receiver"], "caller"),
                                ("bothbosu_single/single-agent-scam-dialogue_all.csv", "labels", ["suspect", "innocent"], "suspect"),
                                ("bothbosu_multi/agent_conversation_all.csv", "labels", ["suspect", "innocent"], "suspect"),
                                ("bothbosu_youtube/youtube_scam_conversations.csv", "labels", ["suspect", "innocent"], "suspect"),
                                ("bothbosu_scammerconv/gen_conver_noIdentifier_1000.csv", "label", ["person a", "person b"], "person a")]:
        d = pd.read_csv(f"{RAW}/{f}")
        repo = {"bothbosu_dialogue": "BothBosu/scam-dialogue", "bothbosu_single": "BothBosu/single-agent-scam-conversations",
                "bothbosu_multi": "BothBosu/multi-agent-scam-conversation", "bothbosu_youtube": "BothBosu/youtube-scam-conversations",
                "bothbosu_scammerconv": "BothBosu/Scammer-Conversation"}[f.split("/")[0]]
        for dlg, y in zip(d.iloc[:, 0], d[col]):
            for who, t in turns(dlg, spk):
                if who == caller and (repo != "BothBosu/youtube-scam-conversations" or len(t.split()) >= 8):
                    add(t, y, repo, "call_turn", "en")

    # rasheq/scam-shield-sms: IMC-2025 real smishing reports (scam) + Mishra&Soni ham + synthetic safe service SMS.
    # Its masks are mapped onto our placeholders; masking-glitch rows ("<URL>ease") are dropped.
    for f in ["train", "val", "test"]:
        d = pd.read_csv(f"{RAW}/rasheq_sms/{f}.csv")
        for t, y in zip(d.text.fillna("").astype(str), d.label):
            if re.search(r"\w<URL>|<URL>\w", t):
                continue
            if y == "scam" and re.search(r"(?i)(do not|don't|never) share (it|this|the|your)? ?(otp|code|it|this)", t):
                continue  # IMC reports that are genuine OTP notices
            t = t.replace("<URL>", " <url> ").replace("<PHONE_NUMBER>", "[PHONE]").replace("<EMAIL_ADDRESS>", "<url>")
            t = re.sub(r"<NUMBER>", lambda m: str(rng.randint(10**5, 10**6 - 1)), t)
            add(t, y == "scam", "rasheq/scam-shield-sms", "sms", "en")

    # flowxai/scamguardbench v0.2: standard + hard (scam_likely=1, no_indicators=0); ambiguous 'suspicious' subset skipped
    for f in ["standard", "hard"]:
        for ln in open(f"{RAW}/scamguardbench/v0.2/{f}.jsonl"):
            r = json.loads(ln)
            if r.get("confusable_class") in ("family_money_request", "marketing_promo"):
                continue
            if r["verdict"] in ("scam_likely", "no_indicators"):
                add(r["text"], r["verdict"] == "scam_likely", "flowxai/scamguardbench",
                    {"sms": "sms", "email": "email"}.get(r.get("channel"), "message"), r["language"])

    # Ridham115 Indian scam SMS (audited labels)
    d = pd.read_csv(f"{RAW}/ridham_indian/data/synthetic_audited.csv")
    lmap = {"en": "en", "hi": "hi", "hinglish": "hi-Latn", "bn_en": "bn-Latn", "mr_en": "mr-Latn", "te_en": "te-Latn", "ta_en": "ta-Latn"}
    for t, y, l in zip(d.text, d.label, d.language):
        add(t, y == "scam", "Ridham115/indian-scam-sms-synthetic-audited", "sms", lmap[l])

    # anmolshrivastav 14 Indian languages (template SMS)
    d = pd.read_csv(f"{RAW}/anmol_india14/scam_ham_india_14_languages.csv")
    lmap = {"Assamese": "as", "Bengali": "bn", "English": "en", "Gujarati": "gu", "Hindi": "hi", "Hinglish": "hi-Latn",
            "Kannada": "kn", "Kashmiri": "ks", "Malayalam": "ml", "Marathi": "mr", "Odia": "or", "Punjabi": "pa",
            "Tamil": "ta", "Telugu": "te"}
    for t, y, l in zip(d.text, d.label, d.language):
        add(t, y == "scam", "anmolshrivastav/scam_ham_india_14_languages", "sms", lmap[l])

    # ysangam Hinglish call lines
    d = pd.read_csv(f"{RAW}/hinglish_calls/India_Cyber_Scam_Hinglish_Dataset.csv")
    for t, y in zip(d.text, d.label):
        add(t, y, "ysangam/Indian_Cyber_Scam_PhoneCall_Hinglish_Dataset", "call_turn", "hi-Latn")

    # VusalShahbazovAz Azerbaijani SMS: smishing -> 1, ham -> 0, spam (advertising) dropped
    d = pd.read_csv(f"{RAW}/smishing_az/dataset.csv")
    for t, y in zip(d.message.fillna("").astype(str), d.label):
        lo = t.lower()
        if y == "smishing" and (not AZ_SCAM.search(lo) or AZ_ADS.search(lo)):
            continue
        if y != "spam":
            add(t, y == "smishing", "VusalShahbazovAz/smishing-AZ-SC", "sms", "az")

    # FredZhang7/all-scam-spam (UCI SMS + Enron + SpamAssassin + small chat set): English/Cyrillic only;
    # spam -> scam only if social-engineering (prize/claim/account/419...), advertising spam dropped; ham -> legit
    d = pd.read_csv(f"{RAW}/fredzhang_allscam/junkmail_dataset.csv")
    for t, y in zip(d.text.fillna("").astype(str), d.is_spam):
        cyr = bool(re.search(r"[А-Яа-яЁё]", t))
        if not cyr and (not re.fullmatch(r"[\x00-\x7f£€üÜ’‘“”…–—]*", t) or not EN_WORDS.search(t)):
            continue  # other languages: no reliable language code
        if y == 1 and not (SCAM_RU.search(t.lower()) and not ADS_RU.search(t.lower()) if cyr else is_scam_en(t)):
            continue
        kind = "message" if cyr else "email" if ("\n\n" in t or re.search(r" [,.'] ", t)) else "sms"
        if y == 1 and kind == "email" and not STRONG_EN.search(t.lower()):
            continue
        add(t, y, "FredZhang7/all-scam-spam", kind, None if cyr else "en")


def dedup(df):
    n0 = len(df)
    df = df.drop_duplicates("text")
    df["k"] = df.text.str.lower().str.replace(r"[\W_]+", " ", regex=True).str.strip()
    # template skeleton: digits, and the name after a salutation, masked
    df["sk"] = (df.k.str.replace(r"\d+", "0", regex=True)
                .str.replace(r"\b(dear|hi|hello|hey|namaste|namaskar)\s+\w+", r"\1 X", regex=True))
    conflict = df.groupby("sk").label.transform("nunique") > 1
    n_conf = int(conflict.sum())
    df = df[~conflict].drop_duplicates("k").drop_duplicates("sk")
    return df, {"exact_or_norm_or_template_dups": n0 - len(df) - n_conf, "label_conflicts": n_conf}


def take(g, q, seed):
    """q rows from g: each label gets up to q/2, leftover from the bigger label."""
    if len(g) <= q:
        return g
    parts, left = [], q
    by = sorted(g.groupby("label"), key=lambda x: len(x[1]))
    for i, (_, gl) in enumerate(by):
        k = min(len(gl), left // (len(by) - i))
        parts.append(gl.sample(k, random_state=seed)); left -= k
    return pd.concat(parts)


LANG_PRI = lambda l: 0 if l in ("ru", "mixed", "kk", "kbd") else 1 if l == "en" else 2


def cap(df, ds_cap=15000, lang_cap=20000):
    out = []
    for src, g in df.groupby("source"):  # dataset cap, filling ru -> en -> other
        left, kept = ds_cap, []
        for pri in (0, 1, 2):
            gg = g[g.language.map(LANG_PRI) == pri]
            kept.append(take(gg, left, 1)); left -= len(kept[-1])
        out.append(pd.concat(kept))
    df = pd.concat(out)
    out = []
    for lang, g in df.groupby("language"):  # language cap: weighted water-filling across sources
        sizes = g.source.value_counts()
        order = sorted(sizes.index, key=lambda s: sizes[s] / CAP_WEIGHT.get(s, 1))
        left, w_left, quota = lang_cap, sum(CAP_WEIGHT.get(s, 1) for s in order), {}
        for s in order:
            w = CAP_WEIGHT.get(s, 1)
            quota[s] = min(sizes[s], int(left * w / w_left)); left -= quota[s]; w_left -= w
        out += [take(g[g.source == s], q, 2) for s, q in quota.items()]
    return pd.concat(out)


CAP_WEIGHT = {"rasheq/scam-shield-sms": 4}  # real reported smishing: larger share of the English budget


def grams(s, n=5):
    s = re.sub(r"\s+", " ", s.lower())
    return {s[i:i + n] for i in range(max(1, len(s) - n + 1))}


def leak_filter(df):
    """Final leakage check only: exact normalized match or char-5gram Jaccard >= 0.5 vs real_all (contents never printed)."""
    real = [normalize(json.loads(l)["text"]) for l in open(f"{OUT}/real_all.jsonl")]
    exact = {re.sub(r"\s+", " ", r.lower()).strip() for r in real}
    rg = [grams(r) for r in real]
    inv = defaultdict(list)
    for j, g in enumerate(rg):
        for x in g:
            inv[x].append(j)
    def leaks(t):
        if re.sub(r"\s+", " ", t.lower()).strip() in exact:
            return True
        g, c = grams(t), Counter()
        for x in g:
            for j in inv.get(x, ()):
                c[j] += 1
        return any(k / (len(g) + len(rg[j]) - k) >= 0.5 for j, k in c.items())
    bad = df.text.map(leaks)
    return df[~bad], bad.groupby(df.source).sum().astype(int).to_dict()


TOPIC = re.compile(r"bank|card|account|police|officer|arrest|court|warrant|prize|won\b|winner|lottery|reward|parcel|package|"
                   r"deliver|courier|customs|\bmom\b|\bmum\b|\bdad\b|\bson\b|daughter|grand(son|ma|daughter)|relative|accident|"
                   r"hospital|invest|crypto|profit|\bjob\b|salary|hiring|vacanc|work from home|support|microsoft|computer|virus|"
                   r"remote|refund|\botp\b|\bcode\b|\bpin\b|password|verify|social security|\btax|\bloan|credit|transfer|"
                   r"банк|карт|сч[её]т|полици|мвд|следовател|прокурат|фсб|арест|приз|выигр|розыгрыш|подар|посылк|доставк|"
                   r"курьер|почт|таможн|мам[аы]|пап[аы]|сын|доч|внук|бабушк|родствен|авари|больниц|инвест|крипт|доход|прибыл|"
                   r"работ|ваканси|зарплат|поддержк|компьютер|вирус|код|смс|пароль|госуслуг|налог|кредит|займ|перев[её]?д")


def translate_pool(df, n=6000):
    p = df[df.language.isin(["en", "ru"]) & df.text.str.split().str.len().between(4, 30)
           & (df.source != "dbarbedillo/SMS_Spam_Multilingual_Collection_Dataset") & (df.kind != "email")].copy()
    p["score"] = (2 * p.text.str.lower().str.contains(TOPIC).astype(float)
                  + p.kind.map({"call_turn": 2, "sms": 1.5, "message": 1}).fillna(0)
                  + [rng.random() * 0.5 for _ in range(len(p))])
    out = []
    for y in (1, 0):
        g = p[p.label == y].sort_values("score", ascending=False)
        per_src = Counter(); per_cap = int(0.35 * n / 2); sel = []
        for _, r in g.iterrows():
            if per_src[r.source] < per_cap:
                sel.append(r); per_src[r.source] += 1
            if len(sel) >= n // 2:
                break
        out.append(pd.DataFrame(sel))
    m = min(len(out[0]), len(out[1]))  # balanced
    t = pd.concat([o.head(m) for o in out])
    t["id"] = ["hfx_" + hashlib.sha1(x.encode()).hexdigest()[:12] for x in t.text]
    return t[["id", "text", "label", "language", "source"]]


NOTES = {  # what it is | label mapping | quality notes
    "DmitryKRX/anti_spam_ru": (
        "Russian anti-spam corpus (66k): real Russian tech-chat (ODS-style) + machine-translated Enron/SpamAssassin/UCI SMS + LLM-written spam posts.",
        "ham -> 0. spam -> 1 ONLY if it matches a social-engineering cue (prize/win, account blocked, password/card data, fake investment / get-rich-quick, fines, parcels) and no advertising cue (pharma, adult, loans, discounts, products, 'chance to win' competitions, hashtags); all other spam (advertising) dropped. 'Get rich quick' posts thinned to 1/4 (near-paraphrases). Latin-only rows dropped.",
        "Scam side is mostly UK premium-rate prize SMS (machine-translated, '£', 'фунтов') and LLM get-rich-quick posts: style differs from KZ scams. Legit side is real Russian chat + MT e-mails/SMS; topically off-domain (ML/data-science chat). 95% legit."),
    "shaw/scambench-training": (
        "Agent-safety corpus (37k multi-turn chats to an AI agent, 14 languages). Only the hand-built 'generated-culture-*' subset (1.3k, culture-specific scams per language: FSB/Sberbank calls, Avito, GIBDD fines, Gosuslugi, PIX, Enkeltrick...) is used.",
        "scam conversation -> its last user turn (the scam payload) = 1. legit conversation -> its user inquiry turns (e.g. 'How do I check GIBDD fines on Gosuslugi?') = 0. Small-talk filler that also appears in scam conversations is skipped. The rest of ScamBench (prompt injection, jailbreaks, agent-addressed boilerplate, leetspeak) dropped: turn text does not carry the label.",
        "Templated (many repeats removed by dedup). Legit side is mostly questions ABOUT scams (hard negatives). CC BY-SA: derived data inherits ShareAlike."),
    "Bektemir96az96/Uzbek_and_Russian_Phishing_dataset": (
        "Uzbek + Russian SMS phishing (UzPhishNet), 100k rows.",
        "SOURCE LABEL IS INVERTED: 0 = phishing -> 1, 1 = legitimate -> 0.",
        "Only 14 templates (random URLs/numbers): collapses to 14 rows after template dedup."),
    "dbarbedillo/SMS_Spam_Multilingual_Collection_Dataset": (
        "UCI SMS Spam Collection machine-translated (M2M100-418M) into 20 languages; only the Russian column used.",
        "spam -> 1 only if the English original is a fake prize/claim/account message (else advertising, dropped). ham -> 0, but capped at 3x the scam count. Untranslated / degenerate-repetition MT rows dropped.",
        "Poor MT quality (broken Russian, leftover English); UK premium-rate scams. Excluded from the translation pool. GPL licence."),
    "BothBosu/scam-dialogue": (
        "1.6k synthetic English phone dialogues (caller/receiver), 8 types (ssn, refund, support, reward, delivery, insurance, telemarketing, wrong number).",
        "Split into turns; only caller turns kept. Scam dialogue -> caller(scammer) turns = 1; legit dialogue -> caller turns = 0; receiver turns dropped.",
        "Turn labels inherit the dialogue label: some scammer turns are generic ('Let me check that for you'). Legit side includes telemarketing sales calls (kept as legit: harmless)."),
    "BothBosu/single-agent-scam-conversations": (
        "1.6k synthetic English dialogues (Suspect/Innocent), same 8 types.",
        "Suspect turns only: scam -> 1, legit -> 0.",
        "92% of its scam turns duplicate BothBosu/scam-dialogue (removed by dedup), hence fewer scam rows. In a few legit dialogues the 'Suspect' is the customer."),
    "BothBosu/multi-agent-scam-conversation": (
        "1.6k synthetic English dialogues between two LLM agents (victim personality varied).",
        "Suspect turns only: scam -> 1, legit -> 0.",
        "Longer, more natural turns than the other BothBosu sets."),
    "BothBosu/youtube-scam-conversations": (
        "20 real scam-baiting call transcripts (YouTube: Scammer Payback etc.).",
        "Suspect (scammer) turns with >= 8 words -> 1 (all dialogues are scams). Shorter turns dropped as label noise ('Yes, open it').",
        "Real speech, but many turns are procedural (remote-access instructions)."),
    "BothBosu/Scammer-Conversation": (
        "1k synthetic 'Person A / Person B' conversations; scam = Person A impersonates bank/insurance/tax; legit = friends' small talk.",
        "Person A turns only: scam -> 1, legit -> 0.",
        "Very templated ('this is X from the bank's fraud department...'); legit side is hobby small talk."),
    "rasheq/scam-shield-sms": (
        "English SMS: IMC-2025 public smishing reports (real), Mishra & Soni SMS ham (UCI-like), synthetic safe service messages from 21 countries (OTP, bank alerts, deliveries).",
        "scam -> 1, safe -> 0 (source already drops advertising spam). Masks mapped: <URL> -> <url>, <PHONE_NUMBER> -> [PHONE], <EMAIL_ADDRESS> -> <url>, <NUMBER> -> random 6-digit number. Rows with masking glitches ('<URL>ease') and IMC 'scam' rows that are genuine OTP notices ('do not share this code') dropped.",
        "Some IMC reports are benign messages people reported (label noise). Given 4x weight in the English language cap (real data)."),
    "flowxai/scamguardbench": (
        "Scam-detection benchmark v0.2 (EN/RO, synthetic) with a hard-legit subset (OTP, bank alerts, courier, utility...).",
        "standard + hard: scam_likely -> 1, no_indicators -> 0. 'suspicious' subset dropped (ambiguous). Legit items of class family_money_request ('new number, send money') and marketing_promo ('you won a voucher') DROPPED: in KZ these are scam patterns.",
        "It is someone else's test set: do not report results on it after training."),
    "Ridham115/indian-scam-sms-synthetic-audited": (
        "1.6k LLM-written Indian scam SMS and genuine look-alikes (en, hi, Hinglish, Roman-script bn/mr/ta/te), label-audited.",
        "scam -> 1, safe -> 0 (audited labels used).",
        "Good hard negatives (real bank/courier/bill SMS). Generated with Gemini / gpt-oss: provider terms may apply."),
    "anmolshrivastav/scam_ham_india_14_languages": (
        "14k template SMS (7k scam / 7k ham) in 14 Indian languages.",
        "scam -> 1, ham -> 0.",
        "Heavily templated (names/numbers swapped): template dedup keeps ~5k. Non-English rows are translations of the same templates."),
    "ysangam/Indian_Cyber_Scam_PhoneCall_Hinglish_Dataset": (
        "10k Hinglish call lines (police / 'digital arrest' / KYC / lottery vs. family, office, delivery calls).",
        "label 1 -> 1, 0 -> 0.",
        "Random opener + body templates; scam_category often mismatches the body. Collapses to ~700 rows after template dedup."),
    "VusalShahbazovAz/smishing-AZ-SC": (
        "4.5k Azerbaijani SMS (ham / spam / smishing); partly translated UCI SMS.",
        "smishing -> 1 only if it has a scam cue (prize, urgent, account, card, password, delivery, tax/fine, bank, link) and is not a translated premium-rate ad (ringtones, minutes, video phones, coupons). spam (advertising) dropped. ham -> 0.",
        "Turkic language (Latin script); mix of real local SMS and translations."),
    "FredZhang7/all-scam-spam": (
        "42k English spam/ham: UCI SMS, Enron + SpamAssassin e-mails, ~1k hand-collected multilingual chat.",
        "ham -> 0. spam -> 1 only if SMS with a social-engineering cue (prize/claim/account/refund...) without advertising cues, or an e-mail with an unmistakable phishing/419 cue; everything else (pharma, watches, software, loans, stocks) dropped. Non-English Latin rows dropped (no language code).",
        "Legit side is mostly Enron/mailing-list e-mail: off-domain."),
}
SKIPPED = [
    ("vichetkao/Scam_Message_9_Language", "MIT", "Gated (manual approval) - not accessible with the current HF token."),
    ("M-Arjun/SpamShield-Datasets", "CC BY 4.0", "Gated (auto-approval needs accepting terms and sharing contact info in the browser) - not done on the user's behalf. Card: mostly generic/advertising 'spam' (72k 'spam' vs ~1k phishing/job_scam), 636 Russian spam rows."),
    ("Nachammai41/fraud-detection-underserved-20k (+ persona_conditioned v2/v3/v4)", "CC BY 4.0", "Not messages: first-person victim narratives attached to synthetic transactions; is_fraud is a transaction label that contradicts the text (is_fraud=0 narratives describe being defrauded). Mostly >80 words."),
    ("Aleksandr505/PhishingDatasetExtended", "none", "No licence on the card -> skipped per rules (770 clean ru/en phishing vs legit service messages; would be useful if the author adds a licence)."),
    ("shakeleoatmeal/phone-scam-detection-synthetic", "MIT", "Legit SSA calls ask for SSN/identity verification in 77% of cases: harmful hard negatives."),
    ("jencyyy/fraudcall", "MIT", "Bengali-only MT of Chinese fraud calls; labels visibly inconsistent (shopping enquiries labelled fraud, loan pitches legit); not split by speaker."),
    ("oscarwu/ScamWorld, ruSpamModels/russian-spam-detection, AugustLight/telegram_spam_ru, BLISS-e-V/SCAM, Scam-AI/*", "CC BY-NC*", "Non-commercial licences."),
    ("useKled/*, DominicTWHV/Discord-Scams", "other", "No open licence."),
]


def write_report(df, stats):
    L = ["# hf_extra: public Hugging Face training data", "",
         f"Built by `pipeline/src/build_hf_extra.py` on 2026-11-14. Output `data/processed/hf_extra.jsonl`: **{len(df)} rows** "
         f"(scam {int((df.label == 1).sum())} / legit {int((df.label == 0).sum())}).", "",
         "Pipeline: textnorm.normalize -> 3-80 words -> dedup (exact; normalized-lowercase; template skeleton with digits and "
         "salutation names masked; skeletons seen with both labels dropped) -> cap 15k rows/dataset (ru first, then en, then others; "
         "each label up to half) -> cap 20k rows/language (water-filling across datasets; rasheq weight 4) -> leakage check vs "
         "real_all.jsonl (exact normalized text or char-5gram Jaccard >= 0.5).", "",
         f"- Dedup removed {stats['dedup']['exact_or_norm_or_template_dups']} rows; {stats['dedup']['label_conflicts']} rows dropped as label conflicts.",
         f"- Leakage check dropped {sum(stats['leak_dropped'].values())} rows (filter verified with a positive control: all real items and lightly edited copies are caught).",
         "- `language`: lang_tag() for Cyrillic text (ru / mixed / kk); ISO code from the source otherwise "
         "(hi-Latn etc. = romanised code-mixed text). `kind`: sms | message | email | call_turn.",
         "- Licences: CC BY-SA (scambench) and GPL (dbarbedillo) rows carry share-alike/copyleft terms; filter by `license` if that matters.", "",
         "## Totals by language", "", "| language | scam | legit |", "|---|---|---|"]
    t = df.groupby(["language", "label"]).size().unstack(fill_value=0).reindex(columns=[0, 1], fill_value=0)
    for l, r in t.sort_values(0, ascending=False).iterrows():
        L.append(f"| {l} | {r[1]} | {r[0]} |")
    L += ["", "## Datasets used", ""]
    for src in sorted(df.source.unique(), key=lambda s: -len(df[df.source == s])):
        g = df[df.source == src]
        what, mapping, quality = NOTES[src]
        bl = g.groupby(["language", "label"]).size().unstack(fill_value=0).reindex(columns=[0, 1], fill_value=0)
        langs = ", ".join(f"{l} {r[1]}/{r[0]}" for l, r in bl.sort_values(0, ascending=False).iterrows())
        L += [f"### {src}", "", f"- **What:** {what}", f"- **Licence:** {LICENSE[src]}",
              f"- **Kept:** {len(g)} rows - scam {int((g.label == 1).sum())} / legit {int((g.label == 0).sum())}; "
              f"by language (scam/legit): {langs}; kinds: {dict(Counter(g.kind))}",
              f"- **Label mapping:** {mapping}", f"- **Quality notes:** {quality}", "", "Samples:", ""]
        smp = pd.concat([g[g.label == 1].sample(min(3, int((g.label == 1).sum())), random_state=1),
                         g[g.label == 0].sample(min(2, int((g.label == 0).sum())), random_state=1)]).head(5)
        L += [f"- `{r.label}` [{r.language}, {r.kind}] {r.text[:220].replace('|', '/')}" for r in smp.itertuples()] + [""]
    L += ["## Checked and skipped", "", "| dataset | licence | reason |", "|---|---|---|"]
    L += [f"| {a} | {b} | {c} |" for a, b, c in SKIPPED]
    tp = stats["translate_pool"]
    L += ["", "## hf_extra_to_translate.jsonl", "",
          f"{tp['n']} rows for later MT into Kazakh, balanced {tp['label']}; languages {tp['lang']}. English/Russian rows of 4-30 words "
          "from hf_extra, excluding e-mails and the low-quality MT source (dbarbedillo). The file is frozen (already sent to MT); "
          "note it still contains some UK premium-rate prize SMS in Russian MT ('фунтов', 'Txt') from anti_spam_ru - low value for KZ, can be filtered after MT. "
          "Ranked by topic cue (banks, cards, police/courts, prizes, parcels/customs, relatives, investments/crypto, jobs, tech support, "
          "OTP/passwords, Gosuslugi/tax/fines) + kind (call_turn > sms > message), max 35% of each label from one source.",
          f"Sources: {tp['source']}"]
    open(f"{OUT}/hf_extra_report.md", "w").write("\n".join(L) + "\n")


if __name__ == "__main__":
    fetch()
    load_all()
    df = pd.DataFrame(rows)
    raw_counts = df.groupby(["source", "label"]).size().unstack(fill_value=0)
    df, dd = dedup(df)
    df = cap(df)
    df, leak = leak_filter(df)
    df = df.sample(frac=1, random_state=3).drop(columns=["k", "sk"])
    df.to_json(f"{OUT}/hf_extra.jsonl", orient="records", lines=True, force_ascii=False)
    tp_path = f"{OUT}/hf_extra_to_translate.jsonl"
    if os.path.exists(tp_path):  # frozen: already sent to machine translation
        tp = pd.read_json(tp_path, lines=True)
        assert tp.text.isin(set(df.text)).all(), "translate pool no longer a subset of hf_extra"
    else:
        tp = translate_pool(df)
        tp.to_json(tp_path, orient="records", lines=True, force_ascii=False)
    stats = {"n": len(df), "label": df.label.value_counts().to_dict(), "dedup": dd, "leak_dropped": leak,
             "raw_after_filters": {s: r.to_dict() for s, r in raw_counts.iterrows()},
             "by_source_label": {f"{s}|{y}": int(n) for (s, y), n in df.groupby(["source", "label"]).size().items()},
             "by_lang_label": {f"{l}|{y}": int(n) for (l, y), n in df.groupby(["language", "label"]).size().items()},
             "translate_pool": {"n": len(tp), "label": tp.label.value_counts().to_dict(), "lang": tp.language.value_counts().to_dict(),
                                "source": tp.source.value_counts().to_dict()}}
    json.dump(stats, open(f"{OUT}/hf_extra_stats.json", "w"), ensure_ascii=False, indent=1, default=int)
    write_report(df, stats)
    print(json.dumps(stats, ensure_ascii=False, indent=1, default=int))
