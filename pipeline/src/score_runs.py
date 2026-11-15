"""Kaggle job: score frozen runs (weights mounted from earlier training kernels) on an eval file.

usage: python score_runs.py <eval_file> <run_name> [<run_name> ...]
Finds /kaggle/input/**/runs/<run_name>/best, writes runs/<run_name>/preds_<eval stem>.jsonl.
"""
import glob, json, os, sys
import numpy as np, pandas as pd, torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

eval_file, names = sys.argv[1], sys.argv[2:]
stem = os.path.splitext(os.path.basename(eval_file))[0]
ev = pd.read_json(eval_file, lines=True)
for name in names:
    hits = [p for p in glob.glob(f"/kaggle/input/**/runs/{name}", recursive=True) if os.path.exists(f"{p}/best/config.json")]
    assert hits, f"weights for {name} not mounted"
    src = hits[0]
    cfg = json.load(open(f"{src}/config.json"))
    tok = AutoTokenizer.from_pretrained(f"{src}/best")
    model = AutoModelForSequenceClassification.from_pretrained(f"{src}/best").cuda().eval()
    pos, prefix, max_len = cfg.get("pos_idx", 1), cfg.get("prefix", ""), cfg.get("max_len", 128)
    out = []
    with torch.no_grad():
        for i in range(0, len(ev), 64):
            enc = tok([prefix + t for t in ev.text.iloc[i:i + 64]], padding=True, truncation=True, max_length=max_len, return_tensors="pt").to("cuda")
            with torch.autocast("cuda", dtype=torch.float16):
                logits = model(**enc).logits.float()
            out.append(torch.softmax(logits, -1)[:, pos].cpu().numpy())
    os.makedirs(f"runs/{name}", exist_ok=True)
    ev[["id", "set", "label", "language", "text"]].assign(score=np.concatenate(out)).to_json(f"runs/{name}/preds_{stem}.jsonl", orient="records", lines=True, force_ascii=False)
    print("scored", name, len(ev), flush=True)
