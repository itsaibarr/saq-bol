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
