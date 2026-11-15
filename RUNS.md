# Real-test log (each line = one frozen model, scored once)

## Freeze 2026-11-15T03:20: ens_v6c_e5s2s3_logit_z
- Note: A5 pick: 2x e5-large (seeds 2,3; 2 epochs) logit_z; within 0.005 of the top dev AP with fewest models. Seeds 2 and 3 were the top-2 dev singles (disclosed).
- Mix: data/processed/mix_v6c; ensemble method: logit_z
- Selection rule: SPEC.md A5 (dev AP vs chat + notifications); operating point: A4.
- Dev configurations evaluated before this freeze (trained runs and ensembles with dev preds): 40
  - member kg_e5L_v6c_s2: model intfloat/multilingual-e5-large, lr 1e-05, epochs 2, seed 2, best epoch 2, preds sha256 5abc78bd9a8246a3
  - member kg_e5L_v6c_s3: model intfloat/multilingual-e5-large, lr 1e-05, epochs 2, seed 3, best epoch 2, preds sha256 4fd0a74927e37978
- Ensemble preds sha256: a8ecb9e69ce58d30
| 2026-11-15T03:20 | ens_v6c_e5s2s3_logit_z | 0.807 [0.75, 0.85] | 0.0030 | 0.960 | 0.84 / 0.77 | A5 pick: 2x e5-large (seeds 2,3; 2 epochs) logit_z; within 0.005 of the top dev AP with fewest models. Seeds 2 and 3 were the top-2 dev singles (disclosed). |

## Freeze 2026-11-15T12:32: ens_v7_e5x4_logit_z
- Note: v2 (A6): A5 pick on mix v7 = all 4 e5-large seeds, logit_z; dev AP 0.978 vs v1 0.962, so v2 replaces v1. Frozen before test B is scored.
- Mix: data/processed/mix_v7; ensemble method: logit_z
- Selection rule: SPEC.md A5 (dev AP vs chat + notifications); operating point: A4.
- Dev configurations evaluated before this freeze (trained runs and ensembles with dev preds): 46
  - member kg_e5L_v7_s1: model intfloat/multilingual-e5-large, lr 1e-05, epochs 2, seed 1, best epoch 2, preds sha256 fe5e20c289b4187e
  - member kg_e5L_v7_s2: model intfloat/multilingual-e5-large, lr 1e-05, epochs 2, seed 2, best epoch 2, preds sha256 aec3c7866a64e16d
  - member kg_e5L_v7_s3: model intfloat/multilingual-e5-large, lr 1e-05, epochs 2, seed 3, best epoch 2, preds sha256 cbf4f817b383d8ef
  - member kg_e5L_v7_s4: model intfloat/multilingual-e5-large, lr 1e-05, epochs 2, seed 4, best epoch 2, preds sha256 649e73b9582108bd
- Ensemble preds sha256: c5d6d83ddfb40ca0
| 2026-11-15T12:46 | ens_v7_e5x4_logit_z_testB | 0.822 [0.75, 0.88] | 0.0005 | 0.977 | 0.87 / 0.65 | test B, scored once (A6) |
| 2026-11-15T12:46 | ens_v6c_e5s2s3_testB_testB | 0.713 [0.63, 0.78] | 0.0030 | 0.920 | 0.72 / 0.65 | test B, scored once (A6) |

## Test C locked 2026-11-15T15:41 (A7)
- data/processed/testC.jsonl, sha256 63e9da830ec1815d (copy: testC_locked.jsonl): 306 items from 4 collections (ru4, ru4b, kk4, rucis), 204 pages (corrected 18:40; first written as 98). Built blind to any model score.
- Headline scams: Kazakhstan Russian 103, Kazakhstan Kazakh 48, non-Kazakhstan Russian 76. Legit: Kazakhstan 50 (46 official-channel and bank texts, 4 SMS), non-Kazakhstan 6 SMS.
- Dropped at build: 26 near-copies of earlier real items, dev or v2 training rows (LaBSE >= 0.90 or char-5gram Jaccard >= 0.5); 2 internal near-duplicates; 1 excluded label (rucis_075, misleading advertising rather than fraud).
- The v3 mix is built after this, with training rows near any test-C item dropped (--protect).

## Freeze 2026-11-15T18:12: kg_e5L_v8b_s1
- Note: v3 (A7): A5 pick among v3 singles and logit_z ensembles = kg_e5L_v8b_s1 (dev AP 0.9805; the 4-model ensemble 0.9814 and the v3b pair 0.9809 are within 0.005, fewer models wins). A7 gate vs v2: AP 0.9805 >= 0.978-0.005, Russian dev 42/48 >= 40/48, so v3 replaces v2. Frozen before test C is scored. Single model (one 560M encoder) instead of four.
- Mix: data/processed/mix; ensemble method: single model
- Selection rule: SPEC.md A5 (dev AP vs chat + notifications); operating point: A4.
- Dev configurations evaluated before this freeze (trained runs and ensembles with dev preds): 53
  - member kg_e5L_v8b_s1: model intfloat/multilingual-e5-large, lr 1e-05, epochs 2, seed 1, best epoch 2, preds sha256 4c88d158b2eccbcb
- Ensemble preds sha256: 4c88d158b2eccbcb
| 2026-11-15T18:32 | ens_v7_e5x4_testC_testC | 0.801 [0.73, 0.86] | 0.0005 | 0.977 | 0.73 / 0.83 | v2 on test C, scored once (A7) |
| 2026-11-15T18:32 | kg_e5L_v8b_s1_testC | 0.901 [0.84, 0.94] | 0.0025 | 0.986 | 0.88 / 0.91 | v3 on test C, scored once (A7) |
| 2026-11-15T20:14 | ens_v6c_e5s2s3_testC_testC | 0.801 [0.73, 0.86] | 0.0030 | 0.957 | 0.75 / 0.83 | v1 on test C, scored once (A8, comparison only) |

## A8 comparison on test C (scored once each, after v3; no model changed)
| model | headline recall | chat FPR | recall kk / ru | note |
|---|---|---|---|---|
| B2_generic_spam_model | 0.066 | 0.0025 | 0.00 / 0.10 | A4 threshold, refit |
| B1_keyword_rule (A4 / own setting) | 0.013 / 0.225 | 0.0000 / 0.0015 | 0.00 / 0.02 ; 0.13 / 0.27 | |
| B5_offshelf_scam_model | 0.377 | 0.0005 | 0.31 / 0.41 | A4 threshold |
