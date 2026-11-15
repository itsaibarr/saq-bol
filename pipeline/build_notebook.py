"""Build notebooks/saq_bol.ipynb (Colab-ready). Executed locally afterwards so outputs are visible.

usage: python pipeline/build_notebook.py <final_run_dir> <mix_dir> <hf_model_repo_or_empty>
"""
import sys
import nbformat as nbf

final_run, mix, hf_repo = sys.argv[1], sys.argv[2], (sys.argv[3] if len(sys.argv) > 3 else "")
REPO = "https://github.com/itsaibarr/saq-bol"
nb = nbf.v4.new_notebook()
md, code = nbf.v4.new_markdown_cell, nbf.v4.new_code_cell
C = []
C.append(md("""# Сақ бол: scam early warning for Kazakhstan, in Kazakh, Russian and the mix people actually type
**Track:** Finance. **This project is a prototype and is not financial advice.**

A model that reads a message or a call transcript and says whether it looks like a scam, which phrase made it think so, and what to do, in Kazakh or Russian.
Every number below comes from real Kazakhstan scam texts collected word for word from public pages, which the model never saw in training.

Run all cells top to bottom. Training ran on Kaggle T4 GPUs (scripts in `pipeline/`); this notebook loads the saved results and the trained model."""))
C.append(code(f"""# Setup: works on Colab and locally
import os, sys, json, subprocess
if not os.path.exists("pipeline"):
    if not os.path.exists("saq-bol"):
        subprocess.run(["git", "clone", "--depth", "1", "{REPO}"], check=True)
    os.chdir("saq-bol")
if "google.colab" in sys.modules:\n    subprocess.run([sys.executable, "-m", "pip", "install", "-q", "-r", "requirements.txt"], check=False)
sys.path.insert(0, "pipeline/src")
import pandas as pd, numpy as np
pd.set_option("display.max_colwidth", 120)
FINAL_RUN, MIX, HF_MODEL = "{final_run}", "{mix}", "{hf_repo}"\nREPORT, PREDS = "final_report_testC.json", "preds_final_testC.jsonl"  # v3 was scored on fresh test set C
print("ready")"""))
C.append(md("""## 1. The real test set
Hand-collected from banks, regulators, police and news outlets in Kazakhstan (URLs and dates in `data/processed/real_all.jsonl`). Each item has a **unit**:
- `message` and `call_phrase` (5+ words): the **headline** set;
- `fragment` (4 words or fewer) and `description` (third-person scheme descriptions): reported separately or excluded;
- legit `notification` (real bank SMS and push texts) and `advice_text` (official anti-fraud advice that quotes scams).

Split into real-dev (model selection) and real-test A (version 1, scored once), grouped so translations and near-duplicates never straddle the split. After version 1 was frozen, test A moved into training and a fresh test set B (195 texts from pages never used before, `data/processed/testB.jsonl`) was collected and scored once for versions 1 and 2. After version 2, test B moved into training and test C (306 texts from 204 new pages, `data/processed/testC.jsonl`) was collected, locked, and scored once for versions 2 and 3. Test C has a Kazakhstan stratum (Russian and Kazakh) and a Russian stratum from outside Kazakhstan whose publishers are never used in training."""))
C.append(code("""tc = pd.read_json("data/processed/testC.jsonl", lines=True); print(len(tc), "test-C items"); display(pd.crosstab([tc.stratum, tc.label, tc.unit], tc.language))
tb = pd.read_json("data/processed/testB.jsonl", lines=True); print(len(tb), "test-B items"); display(pd.crosstab([tb.label, tb.unit], tb.language))
real = pd.read_json("data/processed/real_all.jsonl", lines=True)
print(len(real), "real items")
display(pd.crosstab([real.split, real.unit], real.language))
display(real[(real.split == "real_test") & real.headline].sample(6, random_state=1)[["language", "unit", "scheme", "text", "publisher", "published_date"]])"""))
C.append(md("""## 2. Training data
No public labelled Kazakh scam data exists, so training combines: public Russian/English/multilingual scam corpora from Hugging Face, their Kazakh machine translations (NLLB-200 1.3B), synthetic Kazakhstan-specific messages and call phrases (generated with Claude under a fixed protocol, never shown the test set, two scheme types deliberately held out), ~27k real everyday Kazakh/Russian chat lines and ~5k rule-based bank/eGov notifications as negatives, and keyboard-Kazakh augmentation. Every training row was checked against the real set for leakage (char 5-gram Jaccard and LaBSE cosine). Version 3 adds the spent test-A and test-B texts, 651 more real Russian scam quotes from non-Kazakhstan publishers and 1,200 Russian-heavy synthetic rows, and counts Russian scams twice, because Russian legit rows outnumbered Russian scams 10 to 1."""))
C.append(code("""stats = json.load(open(f"{MIX}/stats.json"))
print("training rows:", stats["n_train"], "| scam / legit:", stats["train_label"], "| rows dropped as near-copies of real items:", stats["leak_dropped"])
pd.Series(stats["train_source"]).sort_values(ascending=False).head(20)"""))
C.append(md("""## 3. Baselines and the model
Every model gets the same rule (SPEC.md A4): its threshold is the stricter of "flags at most 1% of everyday chat messages" and "flags at most 5% of real bank notifications", both measured on dev. Then we count how many real test scams it catches. (B1_keyword_rule_natural is the keyword rule at its own setting: at least one red flag.)"""))
C.append(code("""from evaluate import summary_line
rows = []
for name in ["B2_generic_spam_model", "B1_keyword_rule", "B1_keyword_rule_natural", "B3_tfidf_our_mix", "B5_offshelf_scam_model"]:
    rep = json.load(open(f"runs/{name}/report.json"))["test"]
    print(summary_line(name, rep))
final = json.load(open(f"{FINAL_RUN}/{REPORT}"))
print("--- Above: baselines on test set A (254 scams). Version 1 was frozen and scored once on test A:")
v1A = json.load(open("runs/ens_v6c_e5s2s3_logit_z/final_report.json"))
print(summary_line("v1 on test A", v1A["test"]))
print("--- Then test A moved into training; a fresh test set B was collected and both versions were scored on it once:")
v1B = json.load(open("runs/ens_v6c_e5s2s3_testB/final_report_testB.json"))
print(summary_line("v1 on test B", v1B["test"]))
v2B = json.load(open("runs/ens_v7_e5x4_logit_z/final_report_testB.json"))
print(summary_line("v2 on test B", v2B["test"]))
print("--- Then test B moved into training; a fresh test set C was collected, locked, and both versions were scored on it once:")
v2C = json.load(open("runs/ens_v7_e5x4_testC/final_report_testC.json"))
print(summary_line("v2 on test C", v2C["test"]))
print(summary_line("v3 (final) on test C", final["test"]))
print(summary_line("v2 on test C, Russian outside KZ", v2C["test_cis"]))
print(summary_line("v3 on test C, Russian outside KZ", final["test_cis"]))
print("--- Tools in use today and version 1, scored once each on test C after v3 (SPEC.md A8; no model changed):")
for name in ["B2_generic_spam_model", "B1_keyword_rule_natural", "B5_offshelf_scam_model"]:
    print(summary_line(name + " on test C", json.load(open(f"runs/{name}/report_testC.json"))["test"]))
print(summary_line("v1 on test C", json.load(open("runs/ens_v6c_e5s2s3_testC/final_report_testC.json"))["test"]))"""))
C.append(md("## 4. Results by language, keyboard-Kazakh, and same-text pairs"))
C.append(code("""t = final["test"]
def fmt(r): return "n<10" if r.get("rate") is None else f"{r['rate']:.1%} [{r['wilson95'][0]:.0%}, {r['wilson95'][1]:.0%}] (n={r['n']})"
print("Headline recall:", fmt(t["headline"]["recall"]), "| everyday-chat false alarms:", fmt(t["headline"]["chat_fpr"]), "| real bank-SMS false alarms:", fmt(t["headline"]["notification_fpr"]))
sc = t["headline_self_contained"]
print("Scams recognizable from text alone (blind annotation):", fmt(sc["recall"]), {k: fmt(v) for k, v in sc["by_language"].items()})
for l, r in t["recall_by_language"].items(): print(f"  recall {l}:", fmt(r))
print("Keyboard-Kazakh (same scams, letters folded):", t.get("kbd_paired"))
print("Russian from outside Kazakhstan:", fmt(final["test_cis"]["headline"]["recall"]))
print("Secondary:", json.dumps({k: (v.get('rate'), v.get('n')) for k, v in t["secondary"].items()}, ensure_ascii=False, indent=1))"""))
C.append(code("""from IPython.display import Image, display
for f in ["reports/figures/fig_testC_main.png", "reports/figures/fig_keyboard_kazakh_testC.png", "reports/figures/fig_testB_v1_v2.png", "reports/figures/fig_recall_by_language.png"]:
    display(Image(f))"""))
C.append(md("## 5. Where it fails (real-test examples)"))
C.append(code("""p = pd.read_json(f"{FINAL_RUN}/{PREDS}", lines=True)
thr = final["thr_scam"]
print(f"Operating threshold (frozen, set on dev): {thr:.5f}. Scores below it are not flagged.")
# Recompute the headline numbers from raw predictions (no saved metrics used)
rt_ = p[p.set == "real_test"]; hs_ = rt_[(rt_.label == 1) & (rt_.headline == True)]
print("recomputed: recall", round((hs_.score >= thr).mean(), 4), "| kk", round((hs_[hs_.language == "kk"].score >= thr).mean(), 4), "| ru", round((hs_[hs_.language == "ru"].score >= thr).mean(), 4),
      "| chat FPR", round((p[p.set == "tg_test"].score >= thr).mean(), 4))
nt_ = rt_[(rt_.label == 0) & (rt_.unit == "notification")]
print(f"Kazakhstan service SMS in this test set: {len(nt_)} (flagged {int((nt_.score >= thr).sum())}); too few to estimate a rate on test C")
from evaluate import mcnemar
v2p = pd.read_json("runs/ens_v7_e5x4_testC/preds_final_testC.jsonl", lines=True)
m_ = p.merge(v2p, on=["id", "set"], suffixes=("", "_v2"))
for st in ["real_test", "real_test_cis"]:
    hs2 = m_[(m_.set == st) & (m_.label == 1) & (m_.headline == True)]
    print(f"paired on {st} scams, v3 vs v2 (McNemar):", mcnemar((hs2.score >= thr).astype(int), (hs2.score_v2 >= v2C["thr_scam"]).astype(int)))
rt = p[p.set == "real_test"]
print("Missed real scams (lowest scores):")
display(rt[(rt.label == 1) & rt.headline & (rt.score < thr)].sort_values("score")[["language", "unit", "score", "text"]].head(8))
print("Real legit texts flagged as scam:")
display(rt[(rt.label == 0) & (rt.score >= thr)].sort_values("score", ascending=False)[["language", "unit", "score", "text"]].head(8))
tg = p[p.set == "tg_test"]
print("Everyday chat flagged as scam:")
display(tg[tg.score >= thr].sort_values("score", ascending=False)[["language", "score", "text"]].head(5))"""))
C.append(md("""## 6. Try it
On Colab (Runtime > Change runtime type > T4 GPU) this downloads the fine-tuned model from Hugging Face, if published, and opens the demo with a public link. Locally, run `python app.py runs/kg_e5L_v8b_s1` with the model file in `runs/kg_e5L_v8b_s1/best/`."""))
C.append(code("""import os
IN_COLAB = "google.colab" in sys.modules
cfg = json.load(open(f"{FINAL_RUN}/config.json"))
ready = all(os.path.exists(f"{m}/best/model.safetensors") for m in cfg.get("members", [FINAL_RUN]))
if IN_COLAB and HF_MODEL and not ready:
    from huggingface_hub import snapshot_download
    try:
        targets = [(m, f"{HF_MODEL}-{os.path.basename(m).split('_')[-1]}") for m in cfg["members"]] if "members" in cfg else [(FINAL_RUN, HF_MODEL)]
        for m, repo in targets:
            snapshot_download(repo, local_dir=f"{m}/best")
        ready = True
    except Exception as e:
        print("Model weights are not published on Hugging Face yet (", type(e).__name__, "). All results above are computed from saved predictions.")
if IN_COLAB and ready:
    os.environ["SAQBOL_SHARE"] = "1"
    sys.argv = ["app.py", FINAL_RUN]
    exec(open("app.py").read().replace('if __name__ == "__main__":', 'if True:'))
elif not IN_COLAB:
    print("Demo launches on Colab. Locally: python app.py", FINAL_RUN)"""))
nb["cells"] = C
nbf.write(nb, "notebooks/saq_bol.ipynb")
print("wrote notebooks/saq_bol.ipynb")
