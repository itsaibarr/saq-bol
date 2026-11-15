"""Kaggle job: re-save frozen members' weights in float16 (half the size) for the demo. usage: python convert_fp16.py <run_name> ..."""
import glob, json, os, shutil, sys
import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer
for name in sys.argv[1:]:
    src = [p for p in glob.glob(f"/kaggle/input/**/runs/{name}", recursive=True) if os.path.exists(f"{p}/best/config.json")][0]
    out = f"runs/{name}/best"; os.makedirs(out, exist_ok=True)
    AutoModelForSequenceClassification.from_pretrained(f"{src}/best", dtype=torch.float16).save_pretrained(out)
    AutoTokenizer.from_pretrained(f"{src}/best").save_pretrained(out)
    for f in ["config.json", "best_epoch.json"]:
        if os.path.exists(f"{src}/{f}"): shutil.copy(f"{src}/{f}", f"runs/{name}/{f}")
    print("converted", name, flush=True)
