# Council round 1 brief (2026-11-14 ~16:15 UTC+5). Read-only review.

Project root: <repo root>

## What exists
- Hackathon facts and judging rubric: research/00-context.md, full brief text research/00-hackathon-briefs.txt.
- Case choice and evidence: research/30-finance.md (candidate C1), research/40-languages.md, open-source scan research/60-github.md (section 0), ML stack research/50-ml-pipeline.md (sections 1 and 4).
- Spec with pre-registered predictions and amendment A1: SPEC.md. Task plan: PLAN.md.
- Real test set (verbatim public items with URL/date): data/processed/real_all.jsonl (266 items; split column real_dev / real_test). Raw collector logs: data/real_test/*_sources.md.
- Synthetic training data protocol + 2,000 rows: data/synthetic/GENERATION_PROTOCOL.md, data/synthetic/gen_G*.jsonl.
- Training mix builder, leakage filter, kbd augmentation: pipeline/src/build_train.py; stats: data/processed/mix_v1/stats.json.
- Language tagger, normalization: pipeline/src/textnorm.py. Keyword-rule baseline: pipeline/src/keyword_rule.py.
- Evaluation code: pipeline/src/evaluate.py, finalize.py. Encoder trainer: pipeline/src/train_encoder.py. Explanations: pipeline/src/explain.py. Demo: app.py.
- Baseline results on real-test (fixed hyper-parameters, threshold at <=1% FPR on dev negatives): runs/B0_all_safe, B1_keyword_rule, B2_generic_spam_model, B3_tfidf_our_mix (report.json each). Off-the-shelf model B5 may be in runs/B5_offshelf_scam_model when you read this.
  Summary: B1 keyword rule recall 0.25, false alarms on official warnings 26%; B2 generic spam model recall 0.05 (Kazakh 0.00); B3 TF-IDF on our mix recall 0.31, PR-AUC 0.75 (prevalence 0.66), false alarms on warnings 17%, everyday chat FPR 0.2%.
- Running now: XLM-R base fine-tune on mix_v2 (adds Kazakh translations of anti-fraud warning posts as legit negatives), on a local Apple M5 (Kaggle GPU queue has been stuck >1h).

## Time left
Deadline Mon Nov 16 09:59 UTC+5 (about 41 h). Model freeze planned Sun 20:00, first submission Mon 02:00. The human teammate (Astana, fluent kk/ru/en, passion Finance + Languages) must explain every part live at the finals, so complexity has a cost.

## What I want from you
Return (<= 500 words):
1. Score out of 10 for the current architecture and evaluation design, through your lens.
2. The 5 issues that most affect the final hackathon score, ranked, each with a concrete fix and its cost in hours. Flag anything that is wrong or would mislead a judge.
3. What to cut. Fight scope creep: do not propose new big components unless one replaces something.
Do not edit any files.
