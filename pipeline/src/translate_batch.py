"""Batch-translate rows to Kazakh (augmentation only) with NLLB-200 1.3B. Shardable across GPUs.

usage: python translate_batch.py --inp data/processed/hf_extra_to_translate.jsonl --out data/processed/kk_tr_0_out.jsonl --shard 0 --nshards 2
Input rows need: id, text, label, language (ru|en), source.
"""
import argparse, json, time
import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

ap = argparse.ArgumentParser()
ap.add_argument("--inp", required=True); ap.add_argument("--out", required=True)
ap.add_argument("--shard", type=int, default=0); ap.add_argument("--nshards", type=int, default=1)
ap.add_argument("--model", default="facebook/nllb-200-distilled-1.3B"); ap.add_argument("--bs", type=int, default=32)
a = ap.parse_args()
dev = "cuda" if torch.cuda.is_available() else ("mps" if torch.backends.mps.is_available() else "cpu")
tok = AutoTokenizer.from_pretrained(a.model)
model = AutoModelForSeq2SeqLM.from_pretrained(a.model, torch_dtype=torch.float16 if dev == "cuda" else torch.float32).to(dev).eval()
rows = [json.loads(l) for l in open(a.inp)]
rows = [r for i, r in enumerate(rows) if i % a.nshards == a.shard]
SRC = {"ru": "rus_Cyrl", "en": "eng_Latn"}
out = open(a.out, "w"); t0 = time.time(); done = 0
for lang in ["ru", "en"]:
    sub = [r for r in rows if r.get("language") == lang]
    tok.src_lang = SRC[lang]
    for i in range(0, len(sub), a.bs):
        b = sub[i:i + a.bs]
        enc = tok([r["text"] for r in b], return_tensors="pt", padding=True, truncation=True, max_length=160).to(dev)
        with torch.no_grad():
            gen = model.generate(**enc, forced_bos_token_id=tok.convert_tokens_to_ids("kaz_Cyrl"), max_new_tokens=180, num_beams=3)
        for r, hyp in zip(b, tok.batch_decode(gen, skip_special_tokens=True)):
            out.write(json.dumps({**r, "src_text": r["text"], "text": hyp, "language": "kk", "translated": True,
                                  "mt_model": a.model, "src_language": lang}, ensure_ascii=False) + "\n")
        done += len(b); out.flush()
        if (i // a.bs) % 20 == 0:
            print(f"{lang} {done}/{len(rows)} {time.time() - t0:.0f}s", flush=True)
print("done", done, f"{time.time() - t0:.0f}s")
