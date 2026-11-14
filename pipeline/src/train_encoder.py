"""Fine-tune a multilingual encoder for scam vs legit, with a per-epoch evaluation report.

Runs on CUDA (Kaggle T4, fp16) or Apple MPS (fp32). Writes runs/<name>/:
  epochs.jsonl  one line per epoch: losses, synthetic-val PR-AUC, real-dev PR-AUC, recall at 1% FPR, per-language recall
  preds.jsonl   scores for every eval row (real-test scored here but only reported by finalize.py for frozen models)
  best/         best checkpoint by dev selection score (real-dev scams vs real-dev legit + Telegram-dev chat)
usage: python train_encoder.py --mix data/processed/mix --model FacebookAI/xlm-roberta-base --name enc_xlmr_s1
"""
import argparse, json, math, os, sys, time
import numpy as np, pandas as pd, torch
from sklearn.metrics import average_precision_score, log_loss
from torch.utils.data import DataLoader
from transformers import AutoModelForSequenceClassification, AutoTokenizer, get_cosine_schedule_with_warmup
sys.path.insert(0, os.path.dirname(__file__))
from evaluate import operating_threshold, pick_threshold

ap = argparse.ArgumentParser()
ap.add_argument("--mix", default="data/processed/mix"); ap.add_argument("--model", default="FacebookAI/xlm-roberta-base")
ap.add_argument("--name", required=True); ap.add_argument("--lr", type=float, default=3e-5)
ap.add_argument("--epochs", type=int, default=4); ap.add_argument("--bs", type=int, default=32)
ap.add_argument("--max-len", type=int, default=128); ap.add_argument("--seed", type=int, default=1)
ap.add_argument("--scam-weight", type=float, default=2.0); ap.add_argument("--warmup", type=float, default=0.06)
ap.add_argument("--wd", type=float, default=0.01); ap.add_argument("--prefix", default="")
ap.add_argument("--out", default="runs")
ap.add_argument("--num-labels", type=int, default=2); ap.add_argument("--pos-idx", type=int, default=1)
a = ap.parse_args()
torch.manual_seed(a.seed); np.random.seed(a.seed)
dev = "cuda" if torch.cuda.is_available() else ("mps" if torch.backends.mps.is_available() else "cpu")
amp = dev == "cuda"
out = os.path.join(a.out, a.name); os.makedirs(out, exist_ok=True)
json.dump(vars(a) | {"device": dev}, open(f"{out}/config.json", "w"), indent=1)

tr = pd.read_json(f"{a.mix}/train.jsonl", lines=True).sample(frac=1, random_state=a.seed)
ev = pd.read_json(f"{a.mix}/eval.jsonl", lines=True)
tok = AutoTokenizer.from_pretrained(a.model)
model = AutoModelForSequenceClassification.from_pretrained(a.model, num_labels=a.num_labels).to(dev)


def batches(texts, labels=None, shuffle=False):
    idx = np.random.permutation(len(texts)) if shuffle else np.arange(len(texts))
    for i in range(0, len(idx), a.bs):
        j = idx[i:i + a.bs]
        enc = tok([a.prefix + texts[k] for k in j], padding=True, truncation=True, max_length=a.max_len, return_tensors="pt")
        yield {k: v.to(dev) for k, v in enc.items()}, (torch.tensor([labels[k] for k in j], device=dev) if labels is not None else None)


@torch.no_grad()
def score(texts):
    model.eval(); s = []
    for enc, _ in batches(list(texts)):
        with torch.autocast("cuda", dtype=torch.float16, enabled=amp):
            logits = model(**enc).logits.float()
        s.append(torch.softmax(logits, -1)[:, a.pos_idx].cpu().numpy())
    model.train()
    if dev == "mps":
        torch.mps.empty_cache()
    return np.concatenate(s) if s else np.array([])


def dev_metrics(d):
    """A2 selection rule: threshold at <=1% FPR on everyday-chat dev; recall on real-dev headline scams
    (full messages + call phrases of 5+ words); PR-AUC of those scams against chat-dev (realistic prevalence)."""
    sv = d[d.set == "synthetic_val"]; rd = d[d.set == "real_dev"]; tg = d[d.set == "tg_dev"]
    hd = rd[(rd.label == 1) & (rd.headline == True)]
    thr = operating_threshold(d)
    m_notif = rd[(rd.label == 0) & (rd.unit == "notification")]
    pool = pd.concat([hd, tg])
    m = {"syn_pr_auc": average_precision_score(sv.label, sv.score), "syn_logloss": log_loss(sv.label, sv.score.clip(1e-6, 1 - 1e-6)),
         "dev_pr_auc_vs_chat": average_precision_score(pool.label, pool.score), "dev_thr_A4": thr, "dev_notif_fpr": float((m_notif.score >= thr).mean()) if len(m_notif) else None,
         "dev_recall_at_1pct": float((hd.score >= thr).mean()),
         "dev_fragment_recall": float((rd[(rd.label == 1) & (rd.unit == "fragment")].score >= thr).mean()),
         "dev_advice_text_flag_rate": float((rd[rd.unit == "advice_text"].score >= thr).mean()),
         "dev_recall_by_lang": {l: round(float((g.score >= thr).mean()), 3) for l, g in hd.groupby("language")},
         "syn_recall_by_lang_at_thr": {l: round(float((g[g.label == 1].score >= thr).mean()), 3) for l, g in sv.groupby("language")},
         "syn_fpr_by_lang_at_thr": {l: round(float((g[g.label == 0].score >= thr).mean()), 3) for l, g in sv.groupby("language")}}
    neg2 = pd.concat([tg, rd[(rd.label == 0) & (rd.unit == "notification")]])
    m["dev_ap_vs_chat_notif"] = average_precision_score(np.r_[np.ones(len(hd)), np.zeros(len(neg2))], np.r_[hd.score.values, neg2.score.values])
    m["select"] = m["dev_ap_vs_chat_notif"]  # threshold-free (council round 2): no single dev item decides the epoch
    return m


sel = ev[ev.set.isin(["synthetic_val", "real_dev", "tg_dev"])].copy()
w = torch.ones(a.num_labels, device=dev); w[a.pos_idx] = a.scam_weight
opt = torch.optim.AdamW(model.parameters(), lr=a.lr, weight_decay=a.wd)
steps = a.epochs * math.ceil(len(tr) / a.bs)
sch = get_cosine_schedule_with_warmup(opt, int(a.warmup * steps), steps)
scaler = torch.amp.GradScaler("cuda", enabled=amp)
texts, labels = tr.text.tolist(), [a.pos_idx if y == 1 else 0 for y in tr.label]
best, log = -1.0, open(f"{out}/epochs.jsonl", "a")
for ep in range(1, a.epochs + 1):
    t0, losses, gnorms, nan = time.time(), [], [], 0
    for enc, y in batches(texts, labels, shuffle=True):
        with torch.autocast("cuda", dtype=torch.float16, enabled=amp):
            loss = torch.nn.functional.cross_entropy(model(**enc).logits.float(), y, weight=w)
        if not torch.isfinite(loss):
            nan += 1; opt.zero_grad(); continue
        scaler.scale(loss).backward(); scaler.unscale_(opt)
        gnorms.append(float(torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)))
        scaler.step(opt); scaler.update(); sch.step(); opt.zero_grad(); losses.append(float(loss.detach()))
    sel["score"] = score(sel.text)
    m = dev_metrics(sel)
    rec = {"epoch": ep, "train_loss": float(np.mean(losses)), "train_loss_last10pct": float(np.mean(losses[-max(1, len(losses) // 10):])),
           "grad_norm_mean": float(np.mean(gnorms)), "grad_norm_max": float(np.max(gnorms)), "nan_steps": nan,
           "lr_end": sch.get_last_lr()[0], "sec": round(time.time() - t0, 1), **{k: (round(v, 4) if isinstance(v, float) else v) for k, v in m.items()}}
    log.write(json.dumps(rec, ensure_ascii=False) + "\n"); log.flush()
    print(json.dumps(rec, ensure_ascii=False), flush=True)
    if m["select"] > best:
        best = m["select"]; model.save_pretrained(f"{out}/best"); tok.save_pretrained(f"{out}/best")
        json.dump(rec, open(f"{out}/best_epoch.json", "w"), indent=1)

# reload best and score every eval row
model = AutoModelForSequenceClassification.from_pretrained(f"{out}/best").to(dev)
ev["score"] = score(ev.text)
keep = [c for c in ["id", "set", "split", "label", "language", "score", "text"] if c in ev.columns]
ev[keep].to_json(f"{out}/preds.jsonl", orient="records", lines=True, force_ascii=False)
print("BEST", json.load(open(f"{out}/best_epoch.json")))
