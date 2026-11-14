"""Large real-chat negative pool for training (tg_neg_train_big.jsonl). The held-out chat pool (tg_neg_test.jsonl,
which supplies tg_dev / tg_test) is read only to EXCLUDE its lines, so evaluation data is unchanged."""
import collections, json, random, re, sys
sys.path.insert(0, "pipeline/src")
from textnorm import WORD_RE, lang_tag, normalize
held = {json.loads(l)["text"] for l in open("data/processed/tg_neg_test.jsonl")}
held_keys = {re.sub(r"\W+", " ", t.lower()).strip() for t in held}
caps = {"ru": 24000, "kk": 4000, "mixed": 2000, "kbd": 400, "en": 1500, "other": 1500}
by = collections.defaultdict(list); seen = set()
lines = open("data/raw/tg_ru_kk/telegram_data.txt", encoding="utf-8", errors="ignore").read().split("\n")
random.Random(77).shuffle(lines)
for ln in lines:
    t = ln.strip()
    if not t or len(t) > 600 or len(WORD_RE.findall(t)) < 3:
        continue
    n = normalize(t); k = re.sub(r"\W+", " ", n.lower()).strip()
    if k in seen or k in held_keys or n in held:
        continue
    seen.add(k)
    l = lang_tag(n)
    if len(by[l]) < caps.get(l, 0):
        by[l].append(n)
with open("data/processed/tg_neg_train_big.jsonl", "w") as f:
    for l, ts in by.items():
        for t in ts:
            f.write(json.dumps({"text": t, "label": "legit", "language": l, "source": "tg_chat_big"}, ensure_ascii=False) + "\n")
print({l: len(v) for l, v in by.items()})
