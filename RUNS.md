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
