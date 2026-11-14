# Plan (from SPEC.md v0 + A1). Times UTC+5.

Each task lists what proves it is done. Status: [x] done, [~] running, [ ] open.

## Data
- [x] T1 Real set: 266 verbatim items, split real-dev/real-test by source page. Done when build_real.py prints the split and every item has URL + date. 
- [x] T2 Everyday-chat negatives from real KZ Telegram, disjoint train/test pools. Done when tg_neg_test has kk/ru/mixed rows and no overlap with tg_neg_train.
- [x] T3 Synthetic KZ data, 2,000 rows (G1-G4), protocol frozen first, held-out schemes excluded.
- [~] T4 dokster RU -> KK translation with NLLB-600M (about 1,040 rows).
- [x] T5 build_train.py: mix + leakage filter (0 rows dropped at Jaccard 0.5) + kbd augmentation switch.

## Models
- [x] T6 Baselines B0-B3 (fixed hyper-parameters). Done when runs/B*/report.json exist.
- [~] T7 Encoder v1: xlm-roberta-base on mix_v1, per-epoch report. Done when epochs.jsonl has 4 epochs and best/ exists.
- [ ] T8 Encoder sweep: multilingual-e5-base, mdeberta-v3-base; lr {2e-5, 3e-5, 5e-5}; select on dev `select` score only.
- [ ] T9 Ablation P4: same config with --kbd-aug 0. Done when kbd-folded recall is compared at matched FPR.
- [ ] T10 Calibration: temperature scaling on real-dev + tg-dev; thresholds "scam" (1% FPR) and "suspicious" band.
- [ ] T11 Freeze: pick final model on dev; run finalize.py once on real-test; log in RUNS.md.

## Explanations and demo
- [ ] T12 Trigger phrase: occlusion (drop each word, measure score drop) + matched red-flag category from keyword_rule; advice line in kk / ru by detected language.
- [ ] T13 Gradio app (message mode; conversation mode if stretch is done). Runs locally and in Colab.

## Stretch (only after T11)
- [ ] S1 Turn-by-turn early warning on translated scam dialogues.
- [ ] S2 Zero-shot LLM baseline (B4).
- [ ] S3 Greedy model soup of the best fine-tunes.

## Deliverables
- [ ] D1 Colab notebook with outputs (data -> baselines -> model -> evaluation -> demo), runs top to bottom.
- [ ] D2 README write-up in the brief's template (one page) + credits + "prototype, not financial advice" line.
- [ ] D3 Results figures: per-language recall, paired kk/ru, kbd-folded, novel scheme, failure table.
- [ ] D4 2-minute demo video (screen recording + captions).
- [ ] D5 Public GitHub repo; submission form after the user confirms team details.

## Council rounds (Opus only)
- R1 after T7/T8 first results (architecture + results critique).
- R2 after T10/T11 freeze (honesty, metrics, judging fit).
- R3 on the final repo, notebook and write-up before submission.
