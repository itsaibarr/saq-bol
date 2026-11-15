# Council round 7 brief (2026-11-15 ~20:20 UTC+5). Read-only. README restructured around tools in use today vs ours.

Project root: <repo root>. The user asked for the README and figures to show the largest honest gap: existing tools and our first version vs our final model. To keep it on one test set, the existing tools (B1 keyword rule, B2 generic spam filter, B5 existing multilingual scam model) and version 1 were scored once each on test C after v3 (SPEC.md A8, "Results A8"; no model changed).
Read: README.md (rewritten), reports/figures/fig_testC_main.png, reports/figures/fig_keyboard_kazakh_testC.png, SPEC.md (A7, Results v3, A8, Results A8), RUNS.md tail, runs/B1_keyword_rule_natural/report_testC.json, runs/B2_generic_spam_model/report_testC.json, runs/B5_offshelf_scam_model/report_testC.json, runs/ens_v6c_e5s2s3_testC/final_report_testC.json, runs/kg_e5L_v8b_s1/final_report_testC.json, pipeline/src/baselines_testC.py, council/round6_results.md.
Do not suggest retraining, new data, re-scoring or new features. Deadline Mon 09:59 UTC+5.

Give (<= 200 words):
1. Score out of 10 through your lens.
2. Is the comparison fair (same texts, same threshold rule, keyword rule at its own setting, A8 added after v3 was scored)? Does any sentence overclaim, e.g. "tools available today", "anyone could deploy"?
3. Every README sentence or table cell that does not match the reports, quoted with the exact fix.
4. "satisfied" or "not satisfied".
Do not edit files.
