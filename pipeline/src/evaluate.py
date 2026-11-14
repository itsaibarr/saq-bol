"""Evaluation (amendment A2, after council round 1).

Headline: threshold at <=1% false-positive rate on everyday-chat dev (tg_dev). Recall on real-test HEADLINE scams
(full messages + call phrases of 5+ words), FPR on everyday-chat test, PR-AUC of those scams against chat test
(realistic prevalence). Intervals: Wilson for every proportion, plus a cluster bootstrap over source pages for the
headline recall. Paired comparisons (keyboard folding, kk/ru translation pairs, model vs model) report discordant
counts and an exact McNemar p-value. Slices with n < 10 are reported as counts only.
"""
import json
import numpy as np
import pandas as pd
from scipy.stats import binomtest
from sklearn.metrics import average_precision_score

RNG = np.random.default_rng(0)


def wilson(k, n, z=1.96):
    if n == 0:
        return (float("nan"), float("nan"))
    p = k / n; d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d; h = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (float(max(0, c - h)), float(min(1, c + h)))


def rate(pred, min_n=10):
    pred = np.asarray(pred, dtype=int); n, k = len(pred), int(pred.sum())
    if n < min_n:
        return {"n": n, "k": k, "rate": None, "note": f"n<{min_n}, count only"}
    return {"n": n, "k": k, "rate": k / n, "wilson95": wilson(k, n)}


def cluster_ci(df, col="pred", group="group", n=2000):
    g = df.groupby(group)[col].agg(["sum", "count"]).values
    if len(g) < 2:
        return (float("nan"), float("nan"))
    stats = []
    for _ in range(n):
        s = g[RNG.integers(0, len(g), len(g))]
        stats.append(s[:, 0].sum() / s[:, 1].sum())
    return (float(np.percentile(stats, 2.5)), float(np.percentile(stats, 97.5)))


def mcnemar(a, b):
    """a, b: aligned 0/1 arrays. Returns discordant counts and exact two-sided p."""
    a, b = np.asarray(a, int), np.asarray(b, int)
    only_a, only_b = int(((a == 1) & (b == 0)).sum()), int(((a == 0) & (b == 1)).sum())
    p = binomtest(only_a, only_a + only_b, 0.5).pvalue if only_a + only_b else 1.0
    return {"n": int(len(a)), "both": int(((a == 1) & (b == 1)).sum()), "only_first": only_a, "only_second": only_b,
            "neither": int(((a == 0) & (b == 0)).sum()), "mcnemar_p": float(p)}


def pick_threshold(neg_scores, max_fpr=0.01):
    """Smallest threshold whose false-positive rate on the given negatives is <= max_fpr."""
    s = np.sort(np.asarray(neg_scores))[::-1]
    k = int(np.floor(max_fpr * len(s)))
    return float(s[k] + 1e-9) if k < len(s) else float(s[-1])


def operating_threshold(d, split="real_dev", chat="tg_dev", max_chat_fpr=0.01, max_notif_fpr=0.05):
    """A4: the stricter of <=1% FPR on everyday chat and <=5% FPR on real legit notifications (both from dev)."""
    t_chat = pick_threshold(d[d.set == chat].score, max_chat_fpr)
    notif = d[(d.set == split) & (d.label == 0) & (d.get("unit") == "notification")].score if "unit" in d else []
    t_notif = pick_threshold(notif, max_notif_fpr) if len(notif) else t_chat
    return float(max(t_chat, t_notif))


def _prep(df, thr):
    d = df.copy()
    d["pred"] = (d.score >= thr).astype(int)
    for c, v in [("headline", False), ("novel_scheme", False)]:
        d[c] = d[c].fillna(v).astype(bool) if c in d else v
    d["year"] = d["year"].astype(str).str[:4] if "year" in d else ""
    return d


def report(df: pd.DataFrame, thr: float, split="real_test", chat="tg_test", thr_low=None) -> dict:
    d = _prep(df, thr)
    rt = d[d.set == split]
    hs = rt[(rt.label == 1) & rt.headline]
    tg = d[d.set == chat]
    out = {"threshold": thr}
    rec = rate(hs.pred); rec["cluster_bootstrap95"] = cluster_ci(hs)
    pool = pd.concat([hs, tg])
    nt = rt[(rt.label == 0) & (rt.unit == "notification")]
    out["headline"] = {"recall": rec, "missed_scams_FN": int((hs.pred == 0).sum()),
                       "notification_fpr": rate(nt.pred, min_n=5), "notification_false_alarms": int(nt.pred.sum()),
                       "chat_fpr": rate(tg.pred), "chat_false_alarms_FP": int(tg.pred.sum()),
                       "pr_auc_vs_chat": float(average_precision_score(pool.label, pool.score)) if len(hs) and len(tg) else None,
                       "chat_prevalence": float(len(hs) / max(1, len(pool)))}
    out["recall_by_language"] = {l: rate(g.pred) for l, g in hs.groupby("language")}
    if "self_contained" in hs:
        sc = hs[hs.self_contained.isin(["yes", "maybe"])]
        out["headline_self_contained"] = {"recall": rate(sc.pred), "by_language": {l: rate(g.pred) for l, g in sc.groupby("language")},
                                          "recall_yes_only": rate(hs[hs.self_contained == "yes"].pred),
                                          "recall_not_self_contained": rate(hs[hs.self_contained == "no"].pred)}
    out["chat_fpr_by_language"] = {l: rate(g.pred) for l, g in tg.groupby("language")}
    out["secondary"] = {
        "fragment_recall (<=4 words)": rate(rt[(rt.label == 1) & (rt.unit == "fragment")].pred),
        "advice_text_flag_rate (anti-fraud advice that quotes scams; stress test)": rate(rt[rt.unit == "advice_text"].pred),
        "notification_flag_rate (real legit notifications)": rate(rt[rt.unit == "notification"].pred, min_n=5),
        "recall_novel_scheme": rate(hs[hs.novel_scheme].pred), "recall_seen_scheme": rate(hs[~hs.novel_scheme].pred),
        "recall_2026": rate(hs[hs.year == "2026"].pred), "recall_before_2026": rate(hs[hs.year != "2026"].pred)}
    # keyboard-Kazakh: same real Kazakh headline scams, original vs folded (paired)
    kb = d[(d.set == "kbd_perturbed") & (d.split == split.replace("real_", "real_"))]
    kk = hs[hs.language == "kk"].set_index("id")
    kbm = kb.assign(orig=kb.id.str.replace("_kbd", "", regex=False)).set_index("orig")
    common = kk.index.intersection(kbm.index)
    if len(common):
        out["kbd_paired"] = {"original_recall": rate(kk.loc[common].pred), "folded_recall": rate(kbm.loc[common].pred),
                             "test": mcnemar(kk.loc[common].pred.values, kbm.loc[common].pred.values)}
    # kk/ru official translation pairs (scam pairs only)
    pr = rt[(rt.label == 1) & rt.pair_id.notna()] if "pair_id" in rt else rt.iloc[:0]
    if len(pr):
        pv = pr.pivot_table(index="pair_id", columns="language", values="pred", aggfunc="max").dropna()
        if {"kk", "ru"} <= set(pv.columns):
            out["kk_ru_pairs"] = {"pairs": int(len(pv)), "test": mcnemar(pv.kk.values, pv.ru.values),
                                  "note": "only_first = caught in Kazakh only; only_second = caught in Russian only"}
    if thr_low is not None:
        band = pd.concat([hs, tg])
        band = band[(band.score >= thr_low) & (band.score < thr)]
        out["suspicious_band"] = {"n": int(len(band)), "scams_in_band": int(band.label.sum())}
    return out


def dev_report(df, thr):
    return report(df, thr, split="real_dev", chat="tg_dev")


def compare(df_a, df_b, thr_a, thr_b, split="real_test"):
    """Paired McNemar on headline scams and on chat negatives for two models (each at its own threshold)."""
    a, b = _prep(df_a, thr_a), _prep(df_b, thr_b)
    key = ["id", "set"]
    m = a[key + ["pred", "label", "headline"]].merge(b[key + ["pred"]], on=key, suffixes=("_a", "_b"))
    hs = m[(m.set == split) & (m.label == 1) & m.headline]
    tg = m[m.set == "tg_test"]
    return {"headline_scams": mcnemar(hs.pred_a, hs.pred_b), "chat_negatives": mcnemar(tg.pred_a, tg.pred_b)}


def summary_line(name, rep):
    h = rep["headline"]; r = h["recall"]
    lang = {k: (round(v["rate"], 2) if v.get("rate") is not None else f"{v['k']}/{v['n']}") for k, v in rep["recall_by_language"].items()}
    kb = rep.get("kbd_paired", {})
    kbs = f"kk {kb['original_recall'].get('rate') and round(kb['original_recall']['rate'], 2)} -> kbd {kb['folded_recall'].get('rate') and round(kb['folded_recall']['rate'], 2)}" if kb else "-"
    fr = rep["secondary"]["advice_text_flag_rate (anti-fraud advice that quotes scams; stress test)"]
    nf = h.get("notification_fpr", {}).get("rate")
    return (f"{name:30s} recall {r['rate']:.3f} [{r['wilson95'][0]:.2f},{r['wilson95'][1]:.2f}] FN={h['missed_scams_FN']} | chatFPR {h['chat_fpr']['rate']:.4f} notifFPR {nf if nf is None else round(nf, 3)} "
            f"| AP-vs-chat {h['pr_auc_vs_chat']:.3f} | by lang {lang} | {kbs} | advice-flag {fr.get('rate') and round(fr['rate'], 2)}")


def save(obj, path):
    with open(path, "w") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2, default=float)
