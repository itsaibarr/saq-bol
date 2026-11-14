"""FraudLens anti-fraud posts (they DESCRIBE scams) -> Kazakh with NLLB-600M, as legit hard negatives in Kazakh."""
import json, re, sys, time
import pandas as pd, torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
sys.path.insert(0, "pipeline/src")
from textnorm import normalize
N = int(sys.argv[1]) if len(sys.argv) > 1 else 700
dev = "mps" if torch.backends.mps.is_available() else ("cuda" if torch.cuda.is_available() else "cpu")
name = "facebook/nllb-200-distilled-600M"
tok = AutoTokenizer.from_pretrained(name, src_lang="rus_Cyrl"); model = AutoModelForSeq2SeqLM.from_pretrained(name).to(dev).eval()
fl = pd.read_json("data/raw/fraudlens_ru/fraudlens_v2_combined.jsonl", lines=True).sample(frac=1, random_state=99)  # different sample than the RU negatives
def first_sents(t, k=2):
    s = re.split(r"(?<=[.!?])\s+", re.sub(r"\s+", " ", str(t)).strip())
    return " ".join(s[:k])[:300]
import os
done = set()
if os.path.exists("data/processed/fraudlens_kk_nllb.jsonl"):
    for ln in open("data/processed/fraudlens_kk_nllb.jsonl"):
        try: done.add(json.loads(ln)["fraudlens_id"])
        except Exception: pass
sel = fl.head(N); sel = sel[~sel.id.astype(str).isin(done)]
texts = [first_sents(t) for t in sel.text_clean]
ids = sel.id.astype(str).tolist()
print("resuming; already done", len(done), "todo", len(texts), flush=True)
out = open("data/processed/fraudlens_kk_nllb.jsonl", "a"); t0 = time.time(); B = 16
for i in range(0, len(texts), B):
    enc = tok(texts[i:i + B], return_tensors="pt", padding=True, truncation=True, max_length=160).to(dev)
    with torch.no_grad():
        gen = model.generate(**enc, forced_bos_token_id=tok.convert_tokens_to_ids("kaz_Cyrl"), max_new_tokens=180, num_beams=2)
    for src, hyp, fid in zip(texts[i:i + B], tok.batch_decode(gen, skip_special_tokens=True), ids[i:i + B]):
        out.write(json.dumps({"text": normalize(hyp), "src_ru": src, "label": "legit", "language": "kk", "source": "fraudlens_ru->kk_nllb600m",
                              "fraudlens_id": fid, "translated": True}, ensure_ascii=False) + "\n")
    out.flush()
    if i % (B * 10) == 0:
        print(f"{i}/{len(texts)} {time.time() - t0:.0f}s", flush=True)
print("done", len(texts), f"{time.time() - t0:.0f}s")
