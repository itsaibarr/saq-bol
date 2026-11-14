# 50 — ML training pipeline research (as of 2026-11-14)

Scope: the training stack, the per-epoch evaluation rubric, the techniques worth the time, Kaggle/Colab automation and experiment tracking. An autonomous agent runs it end to end. The case and data type are not chosen yet, so each data type gets a default.

Evidence levels: **[verified]** means checked today against a primary source or a live command. **[observed]** means seen in this user's own Kaggle runs on Nov 11–13. **[estimate]** means engineering judgment.

---

## 0. Decisions (read this first)

1. **Blocker to clear before any training:** the Kaggle token on this laptop (`~/.kaggle/access_token`) belongs to account **`aibarerzhuman`** [verified: `kaggle config view`]. Its three kernels from Nov 11 (`soup-env-probe`, `soup-task-smoke`, `soup-task-sweep`) were pushed with `enable_gpu: true`, `enable_internet: true` and `machine_shape: NvidiaTeslaT4`. They still ran on the **CPU image** (`torch 2.11.0+cpu`, `nvidia-smi: not found`) with **no DNS** (`Failed to resolve 'pypi.org'`) [observed]. `kaggle quota` reports 0.00 h of GPU used [verified]. The successful T4 runs from Nov 12–13 ran under a different slug owner, `itsaibarr`. The user's own README says "The account must be phone-verified, or kernels get no GPU and no internet." **Action:** either phone-verify `aibarerzhuman` at kaggle.com/settings, or replace the token with the verified account's token. Then run the 2-minute probe in §6.4 before anything else.
2. **"SOUP" = Soup (`soup-cli`)**, an LLM post-training CLI. Use it **only** if the project's model is an LLM, VLM or Whisper fine-tune, and override its defaults (see §1). For image, tabular and time-series work it does not apply.
3. **Default stacks:**
   - image: PyTorch + timm with a hand-written loop
   - tabular: LightGBM/CatBoost with k-fold
   - time series: seasonal-naive/persistence baseline, then LightGBM on lags vs Chronos-2 zero-shot
   - text classification: HF Transformers `Trainer` on a pretrained encoder
   - text generation: Soup or TRL+PEFT LoRA on a small instruct LLM
   - speech: Whisper via HF `Seq2SeqTrainer`, with optional PEFT, plus Omnilingual-ASR zero-shot as a comparison for low-resource languages
4. **Compute plan:** use Kaggle T4×2 as the primary lane, with **one experiment per GPU** (`CUDA_VISIBLE_DEVICES=0` / `1`), not DDP. Use the M5 for data prep, GBDT training, debugging on small subsets, and the demo. Colab CLI is a backup lane.
5. **Tracking:** plain JSONL/CSV files written to `/kaggle/working/runs/<run_id>/`, using the schema in §8. Trackio is optional, for local dashboards only.

---

## 1. "SOUP": what it is and the verdict

### 1.1 Soup (`soup-cli`), the intended meaning [verified]
- Repo: https://github.com/MakazhanAlpamys/Soup. PyPI: https://pypi.org/project/soup-cli/. Apache-2.0, about 10.5k stars.
- Release history: first release v0.1.0 on 2026-03-02; latest **v0.77.2 on 2026-11-05** (https://github.com/MakazhanAlpamys/Soup/releases/tag/v0.77.2). That is 77 minor versions in 8 months, and releases are still changing behaviour: v0.75 rejects unknown config keys, and v0.77 refuses configs that v0.76 accepted.
- Requirements: Python 3.11–3.13 (`<3.14`). The `[train]` extra pulls torch≥2.6, `transformers>=5.16.1,<6`, `peft>=0.20,<1`, `trl>=0.29,<1` and bitsandbytes.
- **What it is:** a YAML+CLI layer over HF Transformers / TRL / PEFT. It is not a new training algorithm. It has optional `unsloth` and `mlx` backends (MLX runs on Apple Silicon, so the M5 can do LoRA SFT/DPO/GRPO locally).
- **Task types**, from `config/schema.py`:
  - `sft`, `dpo`, `grpo`, `ppo`, `reward_model`, `kto`, `orpo`, `simpo`, `ipo`, `bco`, `preference`, `pretrain`, `embedding`, `prm`, `tts`
  - `classifier`, `reranker`, `cross_encoder`: `AutoModelForSequenceClassification` heads, single- or multi-label, reporting `eval_accuracy` and `eval_f1_macro`, with an optional frozen encoder + LoRA
  - `distill`, `unlearn`, `moe_lora_routing`, `online_dpo`
  - `asr`: Whisper only, full fine-tune or `asr_lora: true`, reporting WER/CER through `soup infer --task asr`
- Modalities: `text`, `vision` (VLM SFT: Llama-3.2-Vision, Qwen2-VL, Pixtral; LLaVA/ShareGPT4V formats), `audio` (Qwen2-Audio, Whisper) and `audio_out` (TTS).
- Not supported: CNN/ViT image classification, detection, segmentation, tabular data, time series.
- **Evidence of gains:** the headline claim is about **memory**, not accuracy: layer streaming trains an 8B model with LoRA in a 3.32 GB peak on a 4 GB GPU. That comes from the author's own benchmarks and a Zenodo preprint (https://doi.org/10.5281/zenodo.21918325), which is not peer-reviewed. There is no claim that Soup trains more accurate models than the HF/TRL code it wraps. Accuracy is whatever the underlying trainer and your hyperparameters produce.
- **Gotchas from the user's own source audit**, in `<local path>` and `SPEC.md`:
  - The defaults barely train: lr 2e-5; LoRA r=64/alpha=16 with `target_modules: auto`, which resolves to q_proj/v_proj only on Qwen2; and QLoRA 4-bit.
  - `val_split` takes the **last 10% of the file, unshuffled**. There is no separate val-file field, so shuffle and order the file yourself, putting your own group- or time-aware validation rows last.
  - The VRAM pre-flight is **skipped silently** when `batch_size: auto`.
  - A mid-run NaN is tolerated; only the last logged loss is checked.
  - T4 runs in fp16, since there is no bf16 field.
  - On Colab: `pip uninstall -y torchao`.
  - `soup quantize` and `soup export` have a case bug (`q4_K_M`).
  - `soup ship` evaluates base+adapter in bf16, not the shipped artifact.

**Verdict.** Soup is a convenient front end for **LLM, VLM and Whisper fine-tuning**, and the user already has a working Kaggle notebook generator for it (`<local path>`). It is not "the best training framework" in general. Per data type:

| Case | Use Soup? | Instead / alongside |
|---|---|---|
| Text generation / instruction tuning (e.g. a Kazakh or Russian assistant, a domain QA bot) | **Yes**, if a fine-tuned LLM is truly the core model. Pin `soup-cli==0.77.2`. Set `lr` (1e-4 to 2e-4 for LoRA), `target_modules` (all linear projections) and `batch_size` explicitly. Order the val rows last. Add your own NaN check. | TRL `SFTTrainer` + PEFT directly, or Unsloth, when you need control |
| Text classification | Optional (`task: classifier`, which reports acc and macro-F1) | HF `Trainer` gives per-class, calibration and threshold control more easily. **Prefer `Trainer`** |
| Speech (ASR) | Optional (`task: asr`, Whisper only) | HF `Seq2SeqTrainer` + PEFT; Omnilingual ASR for low-resource languages |
| VLM image→text | Possible (`modality: vision`) | Usually unnecessary for a 30 h hackathon |
| Image classification / segmentation | **No** | PyTorch + timm |
| Tabular | **No** | LightGBM / CatBoost |
| Time series | **No** | Persistence → LightGBM lags / Chronos-2 |

Judges score honesty and a baseline comparison. A Soup run must still report the base model vs. the fine-tuned model on the same held-out test set.

### 1.2 Model soups (Wortsman et al., ICML 2022) [verified]
- A **technique**, not a framework: average the *weights* of several models fine-tuned from the same pretrained checkpoint with different hyperparameters. The "greedy soup" adds a model only if held-out accuracy improves.
- Inference cost is unchanged. In the paper, a ViT-G soup reached 90.94% ImageNet top-1, the state of the art at the time; the method also helps OOD and NLP tasks (arXiv 2203.05482; code at https://github.com/mlfoundations/model-soups).
- The 2026 follow-up "Self-Soupervision" applies it to self-supervised models (PMLR v306, https://proceedings.mlr.press/v306/fuller26a.html).
- Here: worth it only late, if 3 or more fine-tunes of the same backbone already exist. Build a greedy soup on validation (§5, rank 10). Soup's `soup adapters merge --strategy linear|ties|dare` does the same for LoRA adapters.

### 1.3 SOAP optimizer (Vyas et al., 2024) [verified]
- "ShampoO with Adam in the Preconditioner's eigenbasis" (arXiv 2409.11321; code at https://github.com/nikhilvyas/SOAP).
- The paper reports more than 40% fewer iterations and more than 35% less wall-clock time than AdamW on **large-batch language-model pretraining**. The authors say the benefit grows with batch size.
- **Skip it here:** small-batch fine-tuning on T4s is the regime where it helps least, and it adds risk.

### 1.4 Other "SOUP" names (irrelevant)
- SOUP, a token-level mix-policy RL method for LLMs (arXiv 2601.21476, Jan 2026): research only.
- Soup-of-Experts (2025): a pretraining architecture.

---

## 2. Compute facts

### Kaggle [verified unless marked]
- **Quota:** live `kaggle quota` shows GPU 30.00 h/week and TPU 20.00 h/week, refreshing **2026-11-21 00:00 UTC**. Kaggle's GPU tips page also says "up to 30 hours per week of GPU".
- **Session limits** (https://www.kaggle.com/docs/notebooks): 12 h execution for CPU and GPU sessions (9 h for TPU), 20 GB auto-saved in `/kaggle/working`, extra scratch disk, 4 CPU cores and **29 GB RAM** on T4×2, and a 20-minute idle timeout for interactive sessions only. Batch runs from `push` are not affected by the idle timeout.
- **Accelerators:**
  - `NvidiaTeslaT4` = **GPU T4×2**, 2×15,360 MiB [observed nvidia-smi]. A single T4 is no longer offered (kaggle-cli issue #1196, maintainer answer).
  - **P100 is retired.** CLI 2.2.5 warns and the server substitutes another accelerator. The default image's PyTorch (cu128 and later) has no sm_60 kernels anyway (issues #1151 and #1196; CHANGELOG).
  - The CLI docs list `NvidiaL4`, `NvidiaTeslaA100`, `NvidiaH100` and `NvidiaRtxPro6000`, but "some are only available to participants of specific competitions … or admins". Plan for T4×2.
- **T4 = Turing (sm_75):** no bf16 → use **fp16 autocast + GradScaler**; no FlashAttention-2; PyTorch SDPA works.
- **Kaggle GPU image on 2026-11-13** [observed in `<local path>`]:
  - Python 3.13.18, NVIDIA driver 580.178.04 / CUDA 13.0
  - torch 2.11.0+cu130 (CPU image: 2.11.0+cpu), transformers 5.20.2, timm 1.0.30, peft 0.21.2, accelerate 1.15.0, datasets 4.8.5
  - lightgbm 4.6.0, xgboost 3.4.1, catboost 1.2.10, scikit-learn 1.6.1 (old), optuna 5.0.0
  - keras 3.13.2, tensorflow 2.21.0, jax 0.11.1, fastai 2.8.12, pytorch-lightning 2.6.6
  - librosa 0.11.0, soundfile 0.14.0, albumentations 2.0.8, wandb 0.28.1
  - **Not preinstalled:** trackio, mlflow, unsloth, soup-cli, jiwer, evaluate, chronos-forecasting, timesfm, tabpfn. These need internet plus a pinned `pip install`.
  - Kaggle updates the image about every two weeks, so pin versions and save `pip freeze` with every run.
- **Input mount paths changed:**
  - Output of a previous kernel attached through `kernel_sources` mounts at `/kaggle/input/notebooks/<owner>/<slug>/...`, not `/kaggle/input/<slug>/` [observed].
  - Dataset paths are probably similar but unverified. **Always discover inputs with `glob('/kaggle/input/**', recursive=True)`.**

### Apple M5 16 GB laptop
Use it for:
- data preparation and EDA
- LightGBM/CatBoost/sklearn (CPU)
- quick overfit-one-batch and smoke tests through PyTorch MPS
- MLX (`mlx` 0.32.4, `mlx-lm` 0.32.2), or Soup `backend: mlx` for LoRA on small LLMs
- demo inference

Do not run long GPU training here.

The local Python is 3.14.5. Soup needs <3.14 and torch wheels may lag, so create a 3.12 or 3.13 env with `uv venv --python 3.13`.

### Latest library versions on PyPI, checked 2026-11-14 [verified]

| Package | Version | Released |
|---|---|---|
| torch | 2.15.0 | 10-28 |
| torchvision | 0.29.2 | |
| timm | 1.0.31 | 11-03 |
| transformers | 5.23.0 | 11-13 |
| accelerate | 1.15.0 | |
| peft | 0.21.3 | |
| trl | 1.18.0 | |
| unsloth | 2026.11.4 | |
| lightning | 2.6.6 | |
| keras | 3.15.1 | |
| fastai | 2.8.12 | |
| scikit-learn | 1.9.1 | |
| lightgbm | 4.7.0 | |
| xgboost | 3.4.1 | |
| catboost | 1.2.10 | |
| autogluon | 1.6.3 | |
| tabpfn | 10.0.0 (model TabPFN-3.5) | |
| chronos-forecasting | 2.3.2 | |
| timesfm | 3.0.2 | |
| uni2ts (Moirai) | 2.0.0 | |
| neuralforecast | 3.3.1 | |
| mlforecast | 1.1.0 | |
| statsforecast | 2.1.1 | |
| trackio | 0.45.1 | |
| mlflow | 3.18.0 | |
| wandb | 0.31.0 | |
| kaggle | 2.2.5 | |
| google-colab-cli | 0.8.0 | |
| soup-cli | 0.77.2 | |

**Recommendation:** inside Kaggle, use the preinstalled versions unless a feature requires an upgrade. Fewer installs means fewer breakages.

---

## 3. Recommended stack per data type

| Data type | Default (why) | Strong cheap baseline | Upgrade if time | Avoid |
|---|---|---|---|---|
| **Image** classification | **PyTorch + timm** in a plain ~150-line loop. timm has 1000+ pretrained backbones, `create_model(..., num_classes=k)` and `ModelEmaV3`. The agent owns every line, so per-class, calibration and threshold logging is trivial. | Frozen pretrained features (DINOv2/DINOv3 or a ConvNeXt via timm) + logistic regression. About 20 minutes, and often within a few points of fine-tuning on small data [estimate]. | Full fine-tune, e.g. ConvNeXt-V2/EfficientNetV2 at 224–384 px with fp16, AdamW, cosine and EMA; then TTA (hflip). | Training from scratch; Keras/fastai (fine, but the ecosystem mismatch adds friction); Lightning (extra abstraction, little gain at this scale) |
| **Tabular** | **LightGBM** (or **CatBoost** when there are many categoricals) with 5-fold CV and early stopping. Trees remain the state of the art on medium tabular data (Grinsztajn et al., arXiv 2207.08815). Runs on the M5 CPU. | Logistic/linear regression; majority-class or mean baseline | TabPFN-3.5 for ≤50k rows (non-commercial weights license; first use requires a browser login to accept the license, so **pre-cache the weights** or skip it for headless runs); simple averaging of LGBM and CatBoost | Deep tabular nets |
| **Time series** | **Persistence / seasonal-naive baseline** (the Climate track requires it), then **LightGBM on lag/rolling/calendar features** (mlforecast or hand-written) and **Chronos-2 zero-shot** (`amazon/chronos-2`, 120M, Apache-2.0, supports covariates; best pretrained model on fev-bench and GIFT-Eval per its README). All with a **rolling-origin, time-based split**. | Seasonal naive; ETS/ARIMA (statsforecast) | TimesFM 2.5 (200M, Apache-2.0, 16k context). TimesFM **3.0 weights are non-commercial**, which is fine for a hackathon but must be credited. PatchTST (arXiv 2211.14730) only if series are long and plentiful. | Random K-fold on time series (leakage) |
| **Text** classification | **HF Transformers `Trainer`** on a pretrained encoder (multilingual for KZ/RU). Use `eval_strategy="epoch"`, `save_strategy="best"`, `load_best_model_at_end=True`, `metric_for_best_model=<task metric>` and `EarlyStoppingCallback` [Context7: transformers v5.19 docs]. PEFT LoRA only if the model is over ~1B parameters. | TF-IDF + logistic regression (5 minutes) | Soup `task: classifier` if you are already using Soup; a soup of 3 seeds | Prompting a big LLM as the "model" without a baseline |
| **Text** generation | **Soup** (`task: sft`, QLoRA/LoRA) or **TRL `SFTTrainer` + PEFT** on a 0.5–3B instruct model; Unsloth backend for speed on T4. | Base model zero-shot / few-shot | DPO/ORPO only if you have preference pairs | Full fine-tuning of more than 1B parameters on a T4 |
| **Speech** (ASR) | **Whisper** (small/medium; large-v3-turbo if VRAM allows) via HF `Seq2SeqTrainer`, fp16, optional PEFT LoRA (q/v), SpecAugment-style masking, WER/CER. | Zero-shot Whisper; **zero-shot Omnilingual ASR** (Meta, 1600+ languages, `omniASR_CTC_300M/1B` need ~2–3 GiB VRAM; the 7B LLM-ASR reports **Kazakh CER 2.6**, trained on 407 h) | Fine-tune on the target accent or language; report per-language/accent WER | Clips over 40 s for Omnilingual (unsupported) |

Notes:
- **T4×2 usage:** run two independent configs at once, `CUDA_VISIBLE_DEVICES=0 python train.py --cfg a &` and `CUDA_VISIBLE_DEVICES=1 python train.py --cfg b`. This doubles experiment throughput with zero DDP debugging. The user's earlier runs already pinned one T4.
- **Mixed precision on T4:** in plain PyTorch use `torch.autocast("cuda", dtype=torch.float16)` + `torch.amp.GradScaler`. In HF use `fp16=True`. Never `bf16=True` on a T4.
- Lightning, Keras 3 and fastai are all preinstalled and usable, but none beats plain PyTorch/timm or HF Trainer for an agent that must log custom per-group metrics and reason about every line.

---

## 4. EPOCH-REPORT RUBRIC (standalone; the agent runs this after every epoch and every run)

### 4.1 What to log every epoch (one JSON line → `runs/<run_id>/epochs.jsonl`)

```json
{"run_id": "img-cnx-s0", "epoch": 3, "step": 1200, "wall_s": 812.4,
 "lr": 2.1e-4, "train_loss": 0.412, "val_loss": 0.538,
 "train_metric_evalmode": 0.91, "val_metric": 0.874, "primary_metric": "macro_f1",
 "val_metrics": {"acc": 0.88, "macro_f1": 0.874, "auroc": 0.95, "recall_pos": 0.83, "precision_pos": 0.79},
 "per_class": {"benign": {"recall": 0.92, "precision": 0.90, "n": 410}, "malignant": {"recall": 0.83, "precision": 0.79, "n": 90}},
 "per_group": {"sex=F": {"macro_f1": 0.88, "n": 260}, "sex=M": {"macro_f1": 0.86, "n": 240}},
 "ece_15bin": 0.061, "nll": 0.53, "brier": 0.09,
 "grad_norm_mean": 0.84, "grad_norm_max": 3.1, "clip_frac": 0.02, "nonfinite_steps": 0, "amp_scale": 65536,
 "samples_per_s": 412, "gpu_mem_gb": 9.8, "ema_val_metric": 0.881}
```

Rules for those fields:
- `train_metric_evalmode` is computed on a fixed 1–2k-sample **train subset in eval mode** (no augmentation, no dropout). Without it, train-vs-val comparisons are meaningless.
- Per-class and per-group metrics include `n`. Any group with n < 30 is flagged "too small to conclude".
- Regression and forecasting use MAE, RMSE, sMAPE and the **skill vs. persistence**, 1 − MAE_model/MAE_persistence.
- ASR uses WER/CER per language or accent.
- Generation uses held-out NLL/perplexity plus a fixed 20-prompt side-by-side.

### 4.2 Checks and decision rules ("if X, then Y")

Evaluate them in order. The first matching **STOP** rule ends the run.

| # | Signal (checkable) | Diagnosis | Action |
|---|---|---|---|
| C1 | Any `nonfinite_steps > 0`, NaN/Inf loss, or `amp_scale` collapsing below 1 | Divergence or fp16 overflow | **STOP.** Re-run with LR ÷3, grad-clip 1.0 and warmup ≥5% of steps; check inputs for NaN; keep the loss computation in fp32 |
| C2 | Epoch 1: train loss fell by less than 5% from step 0, or `train_metric_evalmode` ≤ the trivial baseline | LR too low, frozen backbone by mistake, label bug, or data-pipeline bug | Run the **overfit-one-batch test** (32 samples, 200 steps, must reach ~0 loss). If it fails, it is a bug. If it passes, raise LR ×3 |
| C3 | Train loss rises more than 1.5× between consecutive logs, or `clip_frac > 0.5` | LR too high | LR ÷3 to ÷10; add or lengthen warmup |
| C4 | `val_loss` rises for **2 consecutive epochs** while `train_loss` falls, and the val metric has not improved for 2 epochs | Overfitting | **STOP** (early stop, patience 2–3). Keep the best checkpoint. Next run: more augmentation or weight decay, fewer epochs, or a smaller or frozen backbone |
| C5 | `train_metric_evalmode − val_metric` > 10 pp at the best epoch | High variance | More data or augmentation, stronger regularization, EMA, smaller model |
| C6 | `train_metric_evalmode` and `val_metric` are within 2 pp and both below target | Underfitting | Bigger or better pretrained model, more epochs, higher LR, less regularization, higher resolution / longer context |
| C7 | `val_metric > train_metric_evalmode` + 2 pp, **or** val is near-perfect on a hard task (AUROC > 0.99, acc > 0.98), **or** epoch 1 already beats the baseline by an implausible margin | **Possible leakage** (val loss below *augmented* train loss alone is normal) | **Freeze results** and run the §4.4 leakage checklist before any further tuning |
| C8 | Epoch-to-epoch std of `val_metric` over the last 3 epochs > half the improvement you are chasing, or the bootstrap 95% CI half-width > 2 pp | Noisy val (too small) | Report the bootstrap CI; use EMA weights; enlarge val or use k-fold; decide only on differences larger than the CI |
| C9 | `ece_15bin > 0.05` at the best epoch | Miscalibrated | Fit **temperature scaling** on val (single T, LBFGS on NLL); re-report ECE. Never fit on test |
| C10 | Any class with recall < 0.5 × macro recall, or a class with 0 predictions | Imbalance collapse | Class-weighted loss or a balanced sampler; logit adjustment (arXiv 2007.07314); tune the threshold on val (§4.3) |
| C11 | Worst-group metric < best-group − 5 pp, with both groups n ≥ 30 and the gap larger than the CI | Subgroup gap (Health and Finance judges check this) | Report it as a finding. Try group-balanced sampling or reweighting, and re-check both groups |
| C12 | `samples_per_s` drops more than 30% vs epoch 1, or GPU util < 60% (from nvidia-smi) | Input pipeline bottleneck (4 CPU cores) | Pre-resize or cache images or features, `num_workers=4`, `pin_memory=True`, persistent workers |
| C13 | Projected wall time (epochs left × epoch time) > the remaining `--timeout`, the 12 h cap, or the weekly budget | Budget overrun | Cut epochs, image size or model, or take the best checkpoint now |
| C14 | `lr` logged ≠ the planned schedule value | Scheduler bug, e.g. stepped per epoch vs per step | Fix before trusting any curve |

### 4.3 Checkpoint selection, thresholds, test-set discipline
- **Checkpoint selection:** choose the best epoch on the **primary val metric**. Break ties with lower val NLL. Keep exactly two checkpoints, `best.pt` and `last.pt`, with no optimizer state, to stay well inside 20 GB. When using EMA, evaluate the raw and EMA weights each epoch and keep whichever is better on val. Record the choice in `summary.json`.
- **Early stopping:** patience 3 epochs on the primary metric (2 for runs of 10 epochs or fewer), min-delta = max(0.1 pp, half the val CI).
- **Threshold selection (binary and multilabel) on validation only:** pick the operating point to match the use case and record it.
  - Health screening: maximize specificity subject to sensitivity ≥ 0.90.
  - Fraud: maximize F1, or minimize expected cost with stated FP/FN costs.
  - Freeze the threshold, then apply it once to test. Report FN and FP separately (Health judges require this).
- **Selective prediction / abstain:**
  - On val, compute the risk–coverage curve using max-softmax probability after temperature scaling, or margin.
  - Choose the confidence cut that yields the target risk (e.g. ≤5% error) and report the coverage reached.
  - Optionally use split conformal prediction for guaranteed coverage (Angelopoulos & Bates, arXiv 2107.07511).
  - The demo shows "abstain → refer to human" cases.
- **Test set:** touch it **once per final candidate** (at most 3 in total), log every access in `test_access.log`, and never tune anything after looking. Use a time-based split for Finance and Climate, and a patient- or subject-grouped split where applicable.

### 4.4 Leakage checklist (run on C7, and once before the first real run)
After Kapoor & Narayanan (arXiv 2207.07048):
1. **Duplicates:** exact duplicates (hashes) and near-duplicates across train/val/test. Images: perceptual hash. Text: normalized string or MinHash. Audio: same speaker or session ID.
2. **Group overlap:** the same patient, user, location, speaker or ticker on both sides of a split.
3. **Time:** any train timestamp ≥ the earliest val or test timestamp. Features computed with future data (rolling windows not shifted, target encoding fit on all rows).
4. **Preprocessing:** scalers, imputers, PCA, vocabularies or SMOTE fit before the split.
5. **Proxy targets:** a single feature with AUROC > 0.95 alone. File paths, IDs or metadata that encode the label.

### 4.5 Per-run report (`runs/<run_id>/summary.json` + a 10-line `REPORT.md`)
Each run's report records:
- config hash, git SHA, data version, seed, `pip freeze` hash
- baseline metric(s) vs. best val metric with 95% bootstrap CI
- best epoch and why (EMA or raw)
- per-class and per-group table
- ECE before and after temperature scaling
- threshold and its rationale; coverage at the target risk
- 5 worst errors with one-line explanations (a judge requirement)
- GPU-hours used
- **Decision:** `KEEP` / `DISCARD` / `PROMOTE-TO-TEST`, with one reason

### 4.6 When to stop iterating (the whole project)
- **Stop tuning** when 3 consecutive experiments each change the val metric by less than the val CI half-width, **or** the model beats the baseline by more than the CI and the failure analysis is written.
- **Hard model freeze at T−10 h.** The deadline is Sun Nov 15 23:59 ET = Mon Nov 16 04:59 UTC, so freeze at about Sun Nov 15 18:59 UTC. After the freeze: test evaluation once, calibration, failure examples, write-up and demo. No new training.
- Change one variable per experiment. Never compare runs that used different splits.

---

## 5. Techniques ranked by expected gain per hour (30 h hackathon, T4)

Gain estimates are typical magnitudes from the cited papers and practice [estimate]; they are not guarantees.

| Rank | Technique | Cost | Expected gain | Notes / source |
|---|---|---|---|---|
| 1 | **Transfer learning / pretrained foundation model** + correct split + trivial baseline | 1–2 h | Largest single gain, often tens of pp over training from scratch on small data | timm, HF Hub, Chronos-2, Whisper (arXiv 2212.04356); LoRA (2106.09685) / QLoRA (2305.14314) for LLMs |
| 2 | **Sane optimization defaults:** AdamW + warmup (~5%) + cosine decay; a 3-point LR sweep (e.g. 1e-4 / 3e-4 / 1e-3 for heads, 1e-5 to 5e-5 for full fine-tunes); grad clip 1.0 | 0.5 h | Avoids the most common failure (wrong LR); a few pp | LR range test (Smith, 1506.01186); one-cycle / super-convergence (1708.07120, 1803.09820); Google Deep Learning Tuning Playbook (github.com/google-research/tuning_playbook) |
| 3 | **Mixed precision fp16** (T4) + right batch size + cached or pre-resized inputs | 0.25 h | 2–3× throughput → 2–3× more experiments | Micikevicius et al. (1710.03740) |
| 4 | **Threshold tuning on val + class-imbalance handling** (weighted loss / balanced sampler / logit adjustment / focal loss) | 0.5 h | Often large on F1, recall or PR-AUC for imbalanced health and finance data | 2007.07314; focal loss 1708.02002 |
| 5 | **Light, domain-appropriate augmentation:** TrivialAugment / RandAugment + flips for images; SpecAugment for speech; none for tabular; jitter/scaling for time series only with care | 0.5 h | Moderate; reduces overfitting on small data | 2103.10158, 1909.13719, 1904.08779; mixup / CutMix (1710.09412, 1905.04899) only for longer schedules |
| 6 | **EMA of weights** (timm `ModelEmaV3`, decay ~0.999–0.9998, with warmup) | 0.25 h | Small (≈0.2–1 pp) and smoother val curves, which helps C8 | timm (`sw`/`ra` recipe tags use EMA) |
| 7 | **Temperature scaling + selective prediction (abstain)** | 1 h | Accuracy unchanged; ECE typically drops sharply; adds an honest "abstain" story the judges reward | Guo et al. (1706.04599); Geifman & El-Yaniv (1705.08500); conformal (2107.07511) |
| 8 | **k-fold CV** | Tabular: cheap (minutes) → **always 5-fold**. DL: k× cost → only if data is under ~5k samples | Better model selection plus an OOF ensemble | Use grouped or time-series folds when needed |
| 9 | **TTA** (hflip, ±small scale) | 0.25 h | Small (≈0.3–1 pp) for images; ×N inference cost | Do last |
| 10 | **Model soups (greedy, on val) / SWA** | 1–2 h, needs 3+ fine-tunes | Small to moderate (≈0.5–1.5 pp) at zero inference cost | 2203.05482; SWA 1803.05407 (`torch.optim.swa_utils`) |
| — | SOAP / exotic optimizers, NAS, big HPO sweeps | High | Low at this scale | Skip |

---

## 6. Kaggle automation recipe (exact commands)

### 6.1 One-time setup on the M5
```bash
uv tool install kaggle --with six   # kaggle 2.2.5 crashed with "No module named 'six'" in a fresh venv [observed]
kaggle --version                    # Kaggle CLI 2.2.5
kaggle config view                  # shows username + auth_method: ACCESS_TOKEN
kaggle quota                        # GPU used/remaining/total + refreshAt
```

Auth options, in CLI docs order (https://github.com/Kaggle/kaggle-cli/blob/main/docs/README.md):
- `kaggle auth login` (OAuth)
- `export KAGGLE_API_TOKEN=...`
- the token in `~/.kaggle/access_token` (present on this machine)
- legacy `~/.kaggle/kaggle.json` / `KAGGLE_USERNAME` + `KAGGLE_KEY`

Kaggle Secrets in kernels can only be created in the web UI: Add-ons → Secrets, then read with `kaggle_secrets.UserSecretsClient().get_secret("HF_TOKEN")`.

### 6.2 Upload a private dataset
```bash
mkdir -p pkg/hk-data && cp -r data/* pkg/hk-data/
kaggle datasets init -p pkg/hk-data        # writes dataset-metadata.json
# edit: {"title":"hk-data","id":"<user>/hk-data","licenses":[{"name":"CC0-1.0"}]}
kaggle datasets create -p pkg/hk-data -r zip -q          # private by default; -r zip uploads subfolders
kaggle datasets status <user>/hk-data                    # wait for "ready"
kaggle datasets version -p pkg/hk-data -m "v2: dedup" -r zip -q   # later updates
```

### 6.3 Kernel folder: `kernels/exp01/{train.py, kernel-metadata.json}`
```json
{
  "id": "<user>/hk-exp01",
  "title": "hk-exp01",
  "code_file": "train.py",
  "language": "python",
  "kernel_type": "script",
  "is_private": true,
  "enable_gpu": true,
  "enable_internet": true,
  "machine_shape": "NvidiaTeslaT4",
  "dataset_sources": ["<user>/hk-data"],
  "competition_sources": [],
  "kernel_sources": [],
  "model_sources": []
}
```

Metadata rules:
- **Do not add `docker_image`.** `kaggle kernels pull -m` writes a pinned image SHA, and a stale CPU pin can override the accelerator image (issue #1197).
- For `.ipynb` kernels, also drop `metadata.kaggle.dockerImageVersionId`. The user's builder sets `nb.metadata.kaggle = {"accelerator":"nvidiaTeslaT4","isInternetEnabled":true,"isGpuEnabled":true}`.
- Use one slug per concurrent experiment. Re-pushing the same slug creates a new version, and `status`/`output` default to the latest version; `<slug>/<version>` addresses old ones.
- `kernel_type: "notebook"` executes through papermill with a 43,200 s (12 h) timeout [observed].

### 6.4 Push, poll, stream logs, fetch outputs
```bash
K=<user>/hk-exp01
kaggle kernels push -p kernels/exp01 --accelerator NvidiaTeslaT4 -t 14400   # -t: run-time cap in seconds
kaggle kernels status $K          # prints e.g. KernelWorkerStatus.QUEUED|RUNNING|COMPLETE|ERROR
kaggle kernels logs $K --follow   # live log stream (SSE), CLI ≥2.2.3
# poll loop (run in background; the agent waits on it):
until kaggle kernels status $K | grep -qE 'COMPLETE|ERROR|CANCEL'; do sleep 60; done
kaggle kernels output $K -p runs/exp01 -o -q                                 # all outputs + <slug>.log (JSON stream)
kaggle kernels output $K -p runs/exp01 -o --file-pattern '.*\.(json|jsonl|csv|png|md)$'   # just reports
kaggle kernels list --mine --format json        # inventory
```

**First run = probe** (2 minutes). Put this at the top of every `train.py` so a misconfigured account fails loudly instead of silently training on CPU:
```python
import torch, socket, subprocess, sys
print(sys.version, torch.__version__, torch.version.cuda)
assert torch.cuda.is_available() and torch.cuda.device_count() >= 1, \
    "NO GPU: phone-verify the Kaggle account / remove docker_image pin / check --accelerator"
print(subprocess.run(["nvidia-smi", "--query-gpu=name,memory.total", "--format=csv"], capture_output=True, text=True).stdout)
try: socket.create_connection(("pypi.org", 443), timeout=5); print("internet OK")
except OSError: print("NO INTERNET — pip installs and HF downloads will fail", file=sys.stderr)
import glob; print("\n".join(sorted(glob.glob("/kaggle/input/**", recursive=True))[:50]))  # discover mount paths
subprocess.run("pip freeze > /kaggle/working/pip_freeze.txt", shell=True)
```

### 6.5 Chaining, limits, gotchas
- **Chaining:** use a previous kernel's outputs by adding `"kernel_sources": ["<user>/hk-exp01"]`. They mount under `/kaggle/input/notebooks/<user>/hk-exp01/` [observed]; locate them with glob.
- **Concurrency:** the user ran several kernels the same week. The number of simultaneous GPU sessions is not documented, so test with 2 [unverified]. One Kaggle account per person; do not create extra accounts to multiply quota.
- **Budget math:** at 30 GPU h/week, the window from Sat 09:50 UTC to Mon 04:59 UTC can use the whole fresh quota, which reset Sat Nov 14 00:00 UTC. With two configs per T4×2 session, that is about 60 single-GPU experiment-hours.
- **Outputs:** only `/kaggle/working` (20 GB) persists. Save `best.pt` and reports only. Write logs incrementally and flush, because a run killed at the 12 h cap still keeps what is on disk.
- **Deliverable:** the hackathon wants a public Colab notebook or GitHub repo with outputs visible. Run the final pipeline as a `kernel_type: notebook` kernel, then commit the executed notebook and the `runs/` reports to GitHub, or re-run that notebook on Colab. Whether `kaggle kernels output` returns the executed `.ipynb` is unverified, so check on the first notebook run.

### 6.6 Google Colab programmatic execution (backup lane)
- **Google Colab CLI** (official; https://github.com/googlecolab/google-colab-cli; PyPI `google-colab-cli` 0.8.0, released 2026-11-10; Python ≥3.12; Linux/macOS):
  ```bash
  uv tool install google-colab-cli
  colab run --gpu T4 --timeout 0 train.py --cfg b     # provision → run → fetch → tear down
  # or a session:
  colab new -s t4 --gpu T4 && colab install -s t4 -r requirements.txt && colab exec -s t4 -f train.py
  colab download -s t4 runs/b/summary.json ./runs/b/summary.json && colab stop -s t4
  ```
  - Auth is OAuth with a **one-time copy-paste code**, so a human must do it once; or use `--auth adc`.
  - Its docs call T4 the "standard free-tier GPU". They also say accelerator provisioning is "gated by per-account quota", and their own demos use CPU, so free GPU availability is not guaranteed.
  - `--timeout` is an **idle** limit (default 30 s without output). Print progress or pass `--timeout 0`.
  - **Viable as a second lane** for parallel experiments when Kaggle quota or queues bind. Not the primary lane.
- **Colab MCP server** (official; https://github.com/googlecolab/colab-mcp, v1.0.2): it "bridges your local agent to a Colab session **in the browser**". It needs an open notebook tab and a local client, so it is less suited to unattended runs. **Skip it**; the CLI covers the need.

---

## 7. Speech, time-series and tabular specifics worth knowing
- **Whisper on T4:**
  - Use fp16 with gradient checkpointing; small and medium fit for a full or LoRA fine-tune.
  - Keep clips ≤30 s and set `language`/`task` explicitly.
  - Report WER and CER per language/accent (Languages track requirement); `jiwer` needs a `pip install`.
  - Soup's `task: asr` normalizer is "not leaderboard-comparable", so compute your own metrics.
- **Omnilingual ASR** (https://github.com/facebookresearch/omnilingual-asr):
  - Per-language CER for the 7B LLM-ASR, from the repo CSV: kaz_Cyrl 2.6, kir_Cyrl 2.6, rus_Cyrl 1.5, uzn_Latn 5.7.
  - The CTC 300M/1B models are the T4-friendly baselines.
  - Fine-tuning recipes are fairseq2-based, so they cost more setup than Whisper+HF.
- **Chronos-2:** `Chronos2Pipeline.from_pretrained("amazon/chronos-2", device_map="cuda").predict_df(df, prediction_length=H, quantile_levels=[0.1,0.5,0.9], ...)` produces quantile forecasts, which give intervals for "trust".
- **TabPFN-3.5:** up to 1M rows and 20k features. GPU recommended; CPU handles at most 5,000 samples. Non-commercial weights with a license-acceptance login on first use. Treat it as optional.

---

## 8. Experiment tracking: recommendation = plain JSONL/CSV (no accounts, no installs)

**Layout**, written inside `/kaggle/working`, so it is downloaded by `kaggle kernels output`:
```
runs/<run_id>/config.json          # full config + seed + git SHA + data version + pip freeze hash
runs/<run_id>/epochs.jsonl         # one line per epoch (schema §4.1), flushed every epoch
runs/<run_id>/summary.json         # best epoch, val CI, test (if promoted), decision, GPU-hours
runs/<run_id>/val_preds.parquet    # ids, labels, logits/probs, group cols → offline threshold/calibration/soups
runs/<run_id>/REPORT.md            # §4.5, ≤10 lines + 5 failure examples
runs/<run_id>/curves.png           # train/val loss + metric + lr
leaderboard.csv (local, M5)        # appended by the agent after each download: run_id, primary, CI, decision
```

Why JSONL:
- it works offline, with internet off, inside any framework
- an agent can parse it with `jq` or pandas
- it adds no dependency to the Kaggle image, where trackio and mlflow are not installed

Alternatives:
- **trackio** (0.45.1, Hugging Face, https://github.com/gradio-app/trackio) [Context7 + PyPI verified]:
  - local-first SQLite, no account
  - `import trackio as wandb` is a drop-in replacement
  - HF `TrainingArguments(report_to="trackio")`
  - CLI with `--json` and `trackio query project --project P --sql "SELECT ..."`, which suits agents
  - On Kaggle it needs internet and a pip install. Set `TRACKIO_DIR=/kaggle/working/trackio` so the database is saved as output.
  - Good for a local dashboard on the M5. Optional.
- **W&B offline** (`WANDB_MODE=offline`): viewing or syncing requires an account. No.
- **MLflow file store:** heavier, not preinstalled, no advantage here. No.

---

## 9. Sources (primary)

**Soup and the other "SOUP" meanings**
- Soup: https://github.com/MakazhanAlpamys/Soup (README, `docs/training.md`, `docs/backends-and-ops.md`, `docs/adapters-and-governance.md`, `src/soup_cli/config/schema.py` @ v0.77.2); https://pypi.org/project/soup-cli/; preprint https://doi.org/10.5281/zenodo.21918325
- User's audit: `<local path>`, `SPEC.md`, `README.md`, `notebook/build_kaggle.py`, `outputs/*/logs/`
- Model soups: arXiv 2203.05482; https://github.com/mlfoundations/model-soups; PMLR v306 https://proceedings.mlr.press/v306/fuller26a.html
- SOAP: arXiv 2409.11321; https://github.com/nikhilvyas/SOAP
- SOUP (RL method): arXiv 2601.21476

**Kaggle**
- Kaggle CLI: https://github.com/Kaggle/kaggle-cli (`docs/kernels.md`, `docs/kernels_metadata.md`, `docs/datasets.md`, `docs/README.md`, `docs/output_format.md`, `CHANGELOG.md`); issues #1151, #1196, #1197
- Kaggle notebooks docs: https://www.kaggle.com/docs/notebooks
- Kaggle GPU tips: https://www.kaggle.com/page/GPU-tips-and-tricks
- Live checks today: `kaggle quota`, `kaggle config view`, `kaggle kernels status/output` on the user's Nov 11 kernels

**Colab**
- Colab CLI: https://github.com/googlecolab/google-colab-cli (README, `docs/01_session_management.md`, `docs/04_automation_and_utility.md`, `docs/05_run_command.md`, `docs/demos.md`)
- Colab MCP: https://github.com/googlecolab/colab-mcp

**Libraries and models**
- Transformers Trainer callbacks and recipes (v5.19 docs via Context7): https://github.com/huggingface/transformers/blob/v5.19.0/docs/source/en/trainer_callbacks.md, `trainer_recipes.md`
- timm: https://github.com/huggingface/pytorch-image-models (README, hfdocs hparams)
- trackio: https://github.com/gradio-app/trackio (README, `docs/source/storage_schema.md`, `ml_agents.md`)
- Chronos / Chronos-2: https://github.com/amazon-science/chronos-forecasting; arXiv 2403.07815, 2510.15821
- TimesFM: https://github.com/google-research/timesfm; arXiv 2310.10688
- Moirai: arXiv 2402.02592
- PatchTST: arXiv 2211.14730
- TabPFN: https://github.com/PriorLabs/TabPFN
- Omnilingual ASR: https://github.com/facebookresearch/omnilingual-asr (`per_language_results_table_7B_llm_asr.csv`)
- Unsloth: https://github.com/unslothai/unsloth
- Whisper: arXiv 2212.04356
- LoRA / QLoRA: arXiv 2106.09685, 2305.14314

**Methods papers**
- Tabular trees vs DL: arXiv 2207.08815
- CatBoost: arXiv 1706.09516
- Calibration: arXiv 1706.04599
- SWA: arXiv 1803.05407
- LR range test / one-cycle: arXiv 1506.01186, 1708.07120, 1803.09820
- Mixed precision: arXiv 1710.03740
- Augmentation: arXiv 1909.13719, 2103.10158, 1710.09412, 1905.04899, 1904.08779
- Imbalance: arXiv 2007.07314, 1708.02002
- Selective prediction / conformal: arXiv 1705.08500, 2107.07511
- Leakage: arXiv 2207.07048
- Tuning playbook: https://github.com/google-research/tuning_playbook

**Versions:** PyPI JSON API (https://pypi.org/pypi/<pkg>/json), queried 2026-11-14.
