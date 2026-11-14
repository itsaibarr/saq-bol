"""Real everyday Kazakh/Russian Telegram chat -> disjoint negative pools (tg_neg_train / tg_neg_test)."""
import collections, json, random, re, sys
sys.path.insert(0, "pipeline/src")
from textnorm import WORD_RE, lang_tag, normalize

lines = open("data/raw/tg_ru_kk/telegram_data.txt", encoding="utf-8", errors="ignore").read().split("\n")
seen, rows = set(), []
for ln in lines:
    t = ln.strip()
    if not t or "t.me/" in t or "http" in t or re.match(r"^[\W\d]*\d+[.)]", t) or re.search(r"—\s*\d", t):
        continue
    w = WORD_RE.findall(t)
    if len(w) < 4 or len(t) > 600:
        continue
    k = re.sub(r"\W+", " ", t.lower()).strip()
    if k in seen:
        continue
    seen.add(k)
    rows.append(t)
random.seed(13); random.shuffle(rows)
by = collections.defaultdict(list)
for t in rows:
    by[lang_tag(t)].append(t)
print("tags over all candidates:", {k: len(v) for k, v in by.items()})
quota_test = {"ru": 1500, "kk": 1000, "mixed": 1000, "kbd": 600, "en": 200}
quota_train = {"ru": 3000, "kk": 3000, "mixed": 3000, "kbd": 1500, "en": 300}
test, train = [], []
for l in quota_test:
    pool = by.get(l, [])
    n_test = min(quota_test[l], len(pool) // 3)
    test += [{"text": normalize(t), "label": "legit", "language": l, "source": "tg_ru_kk", "split": "tg_test"} for t in pool[:n_test]]
    train += [{"text": normalize(t), "label": "legit", "language": l, "source": "tg_ru_kk", "split": "train"} for t in pool[n_test:n_test + quota_train[l]]]
for name, rs in [("tg_neg_test", test), ("tg_neg_train", train)]:
    with open(f"data/processed/{name}.jsonl", "w") as f:
        for r in rs:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(name, len(rs), dict(collections.Counter(r["language"] for r in rs)))
for l in ["kk", "mixed", "kbd"]:
    print("\n", l, ":", " || ".join(x[:70] for x in by[l][:6]))
