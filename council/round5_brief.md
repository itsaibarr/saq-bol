# Council round 5 brief (2026-11-15 ~19:00 UTC+5). Read-only. Third-model (v3, Russian focus) iteration.

Project root: <repo root> (this directory).
Read: SPEC.md (A7 protocol written 15:20, "Results v3", deviations), RUNS.md (test C lock block at 15:41, freeze block at 18:12, two test-C lines), README.md (rewritten for v3), CREDITS.md, data/real_test/COLLECTION_PROTOCOL_C.md, data/synthetic/GENERATION_PROTOCOL_v3.md, pipeline/src/build_testC.py, pipeline/src/a7_gate.py, the diff of pipeline/src/build_train.py and train_encoder.py (`git diff`), runs/kg_e5L_v8b_s1/final_report_testC.json, runs/ens_v7_e5x4_testC/final_report_testC.json, data/processed/testC.jsonl, data/processed/mix_v8/stats.json, reports/figures/fig_testC_v2_v3.png, notebooks/saq_bol.ipynb (executed), council/round4_results.md.
Do not suggest retraining. Do not re-score any test set. Deadline Mon 09:59 UTC+5.

Context: the user asked for >= 90% recall in both Kazakh and Russian. v2 had Russian 65% on test B. v3 added Russian training data, moved test B into training, and was scored on a fresh test C.

Give (<= 250 words):
1. Score out of 10 through your lens.
2. Is the v3 iteration valid (A7 written before data, test C locked before the v3 mix, train-side and test-side near-copy drops, A5 pick of a single model, A7 gate, freeze before scoring, v2 re-scored on C for a paired comparison)? Anything a judge would call goalpost moving, cherry-picking or leakage?
3. Every README sentence that does not match the reports, quoted with the fix.
4. The single most valuable remaining fix.
Do not edit files.
