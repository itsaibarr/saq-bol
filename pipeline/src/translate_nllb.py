"""Translate Russian dokster messages to Kazakh with NLLB-200-distilled-600M (augmentation only; marked translated)."""
import json, re, sys, time
import pandas as pd, torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
sys.path.insert(0, "pipeline/src")
from textnorm import normalize

LIMIT = int(sys.argv[1]) if len(sys.argv) > 1 else 10**9
dev = "mps" if torch.backends.mps.is_available() else ("cuda" if torch.cuda.is_available() else "cpu")
name = "facebook/nllb-200-distilled-600M"
tok = AutoTokenizer.from_pretrained(name, src_lang="rus_Cyrl")
model = AutoModelForSeq2SeqLM.from_pretrained(name).to(dev).eval()

d = pd.read_json("data/raw/dokster_scam_ru_en/data/train_0.jsonl", lines=True)
d = d[d.language == "ru"].copy()
def msg(u):
    m = re.search(r"Analyze this message for scam risk:\s*(.*?)\s*Return only the JSON object", str(u), re.S)
    return m.group(1).strip() if m else None
def field(s, k):
    m = re.search(rf'"{k}":\s*"([^"]+)"', str(s)); return m.group(1) if m else None
d["text"] = d.user.map(msg); d["rl"] = d.assistant.map(lambda s: field(s, "risk_level")); d["st"] = d.assistant.map(lambda s: field(s, "scam_type"))
d = d[d.text.notna() & d.rl.isin(["dangerous", "safe", "needs_check"]) & (d.st != "government_impersonation")].head(LIMIT)
out = open("data/processed/dokster_kk_nllb.jsonl", "w")
t0 = time.time(); B = 16; texts = d.text.tolist(); meta = d[["rl", "st", "id"]].to_dict("records")
for i in range(0, len(texts), B):
    batch = [re.sub(r"\s*(Ref|Note)\s*\d+\.?$", "", t) for t in texts[i:i + B]]
    enc = tok(batch, return_tensors="pt", padding=True, truncation=True, max_length=200).to(dev)
    with torch.no_grad():
        gen = model.generate(**enc, forced_bos_token_id=tok.convert_tokens_to_ids("kaz_Cyrl"), max_new_tokens=220, num_beams=2)
    for src, hyp, m in zip(batch, tok.batch_decode(gen, skip_special_tokens=True), meta[i:i + B]):
        out.write(json.dumps({"text": normalize(hyp), "src_ru": src, "label": "scam" if m["rl"] == "dangerous" else "legit",
                              "language": "kk", "scheme": m["st"], "source": "dokster_ru->kk_nllb600m", "translated": True,
                              "synthetic": True, "dokster_id": str(m["id"])}, ensure_ascii=False) + "\n")
    out.flush()
    if i % (B * 10) == 0:
        print(f"{i + len(batch)}/{len(texts)} {time.time() - t0:.0f}s", flush=True)
print("done", len(texts), f"{time.time() - t0:.0f}s")
