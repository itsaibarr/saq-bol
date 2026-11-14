# Council round 2 brief (2026-11-14 ~21:10 UTC+5). Read-only.

Project root: <repo root>
Round 1 results and what was fixed: council/round1_results.md. Spec with amendments A1-A4: SPEC.md (read A3 and A4 carefully).

## What changed since round 1
- Real set: 800 verbatim items (data/processed/real_all.jsonl), headline scams dev 114 / test 254; 38-68 kk/ru translation pairs; blind self-contained tags (data/processed/real_selfcontained.jsonl).
- Training mixes v5b (74k rows) and v6 (81k rows, adds rule-based legit notifications); stats in data/processed/mix_v6/stats.json; HF data report data/processed/hf_extra_report.md; synthetic protocols data/synthetic/GENERATION_PROTOCOL*.md; notification generator pipeline/src/gen_notifications.py.
- Models trained on Kaggle T4 (runs/kg_*/epochs.jsonl): XLM-R large, multilingual-e5-large, Horizon-Labs scam checkpoint fine-tune; baselines runs/B*/report.json (scored on real-test under A3; B5 off-the-shelf 0.64 recall, TF-IDF 0.56, keyword rule 0.27, generic spam 0.08).
- Dev results, chat-only threshold (old rule): e5-large v5b 0.85 recall (kk 0.88, ru 0.81), Horizon v5b 0.83, ensembles 0.82-0.84.
- Dev results under A4 (also <= 5% FPR on real bank notifications): the same models drop to 0.28-0.41. v6 (with notification negatives) is training now on Kaggle.
- The user (team member) asked for >= 90% recall on both Kazakh and Russian real scams, iterating until reached, with council evaluation.

## What I want from you (<= 450 words)
1. Score out of 10 for the current architecture, data and evaluation design through your lens.
2. Is A4 the right operating point and is the self-contained subset a legitimate way to report? Anything that would look like moving goalposts to a judge?
3. The most effective next 2-3 actions to raise dev recall under A4 toward 90% on both languages in the ~10 GPU-hours and ~30 wall-clock hours left, ranked by expected gain per hour. Concrete (data, model, threshold, ensembling, calibration).
4. How to communicate honestly if 90% is reached only on a subset or only at a looser operating point.
Do not edit files. Do not open runs/*/preds* for real-test rows (real-test stays sealed).
