# 60: Open-source scout for "Сақ бол" (C1: KZ scam early warning)

Researched 2026-11-14. Stars, licenses and last-push dates come from the GitHub API (`gh api repos/...`); model metadata comes from the Hugging Face API, and package versions from PyPI, all on that day. Tags used below:
- **[RUN]**: executed locally on the Apple M5 today.
- **[API]**: metadata only.
- **[DOC]**: read the README, model card or docs.

Verdicts:
- **REUSE**: install it or copy the data.
- **REF**: read it and reimplement the idea (usually because the license is missing or restrictive, or the code is too heavy).
- **SKIP**: don't use it.

Non-commercial licenses are acceptable for the hackathon. They are flagged anyway.

---

## 0. Recommended stack (one pick per component)

| # | Component | Pick | Runner-up / ablation | Why |
|---|---|---|---|---|
| 1 | Existing scam detectors / data | **Off-the-shelf baseline: `Horizon-Labs/phishing-scam-detector-base`** (Apache-2.0, 307M). **Data:** BothBosu dialogues (Apache-2.0) + RU sets from 30-finance | `ayaudildabekyzy-spec/kazakh_fraud_dataset` (10.9k synthetic KK SMS, **no license**: use only with the author's permission) | Fair "does an existing multilingual model already solve it?" baseline. **[RUN] It already flags kk, keyboard-kk and Latin-kk scam SMS (0.78–0.98) and clears legit OTP texts, but it missed a RU loan+code scam (0.34) and false-alarmed on benign code-switched chat (0.56).** This is a strong baseline to beat, and also a scam-aware checkpoint worth fine-tuning (§11). No licensed Kazakh scam data exists. |
| 2 | Turn-level early warning | **Reimplement PreScam's `AT@FPR` + a position-only baseline**, plus ERDE_o / F_latency | BothBosu "accuracy vs #turns" plots | PreScam (COLM 2026) is the only public code that does prefix-level scam prediction with an earliness metric. It has no license, and its metric file is about 100 lines. |
| 3 | Encoder | **`FacebookAI/xlm-roberta-base`** (fine-tune) + **`intfloat/multilingual-e5-base`** (frozen-embedding + LR baseline) | **`kz-transformers/kaz-roberta-conversational`** (83.5M, Kazakh + Beeline call-centre dialogues) as the "small Kazakh-native" arm; `issai/Qwen3.5-4B-Kazakh` as the zero-shot LLM arm | XLM-R tokenises Kazakh well: 2.13 tokens/word, all 18 letters, exact round-trip [RUN]. Backbone choice moved Kazakh F1 by only ±0.01 on KazSAnDRA. |
| 4 | Keyboard-Kazakh restoration | **Port `Bexull/YX_KazQwerty` dictionary lookup to Python** (data CC BY-SA 4.0, code MIT) | Own 30-line translit maps + 20-entry homoglyph map | Ready-made corpus-built dictionary. The author reports 97.5–99.5% with the full Swift logic. **[RUN] A naive 40-line Python port gets 86% of words on the author's unseen holdout and keeps 17/20 Russian phrases unchanged.** Port `endings.tsv` to close the gap. |
| 5 | EN/RU→KK translation | **`issai/tilmash`** (NLLB-1.3B fine-tuned on KazParC; gated, so click "Agree" first) via **CTranslate2** | `facebook/nllb-200-distilled-600M` (second system for the "report both" table) | Tilmash beats NLLB on RU→KK chrF (0.54 vs 0.49). Both are CC BY-NC. |
| 6 | Calibration / conformal / threshold | **sklearn 1.9 `CalibratedClassifierCV(FrozenEstimator(m), method="temperature")`** + **`crepes`** (Mondrian conformal by language → abstain band) + **MAPIE `BinaryClassificationController(risk="fpr")`** | torchmetrics `BinarySensitivityAtSpecificity` for recall at 1% FPR | All BSD/MIT. crepes works on precomputed probabilities and supports per-language bins. MAPIE gives an FPR-guaranteed threshold. |
| 7 | Explanations + rules | **Word-level occlusion (≈15 lines, batched)** for the demo highlight, **Captum 0.9 `LayerIntegratedGradients`** for the report figure; rules = **`re` on diacritic-folded text** (+ `pyahocorasick` if the list grows) | `shap` 0.54 Text masker (slow on CPU) | Occlusion works on whole words, so Cyrillic subword merging is not needed. `transformers-interpret` (last release 2023) and `ferret` (pins `transformers<5`) are stale. |
| 8 | Demo / serving | **Gradio 6.32 locally on the M5** (`gr.HighlightedText` with `(word, float)` + `gr.Label`) + `share=True` link; hosted copy on a **ZeroGPU Gradio Space** | **aiogram 3.31** echo-bot pattern for "forward the SMS to the bot" | **New constraint: Gradio and Docker Spaces now require a paid plan.** Free accounts can host only 2 ZeroGPU Spaces, and only if the account is more than 30 days old with a verified email. |
| 9 | Experiment loop | `run_classification.py` **pinned at transformers v5.19.0** (removed from `main` on 2026-10-13) + HF task guide + `EarlyStoppingCallback` + **fairlearn `MetricFrame`** for per-language metrics; JSON from `trainer.state.log_history` | SetFit 1.2 for few-shot, model2vec for a CPU baseline | Clean, official, Apache-2.0. Per-group metrics take one line with fairlearn. |

**Competitor alert.** A Kazakhstan school team (NIS Taraz) already published a kk/ru/en fraud-message detector: `Ordalinnn/AI-Fraud-Detector` (pushed 2026-11-04, **"All rights reserved"**). It is a char-n-gram + LR stacker with an obfuscation normaliser and an Android app. Only 121 of its 1,398 training texts are Kazakh. The C1 angle still differentiates on these points:
- call transcripts plus turn-level early warning;
- a Kazakh-heavy real test set;
- per-language fairness, including keyboard Kazakh and translit;
- conformal abstention.

Say this explicitly in the write-up ("prior KZ work exists; we differ by …"). Do **not** copy its code or data.

---

## 1. Scam / spam detectors and datasets

**Off-the-shelf models**

| Candidate | URL | License | Popularity | Last update | Size | Verdict |
|---|---|---|---|---|---|---|
| Horizon-Labs phishing-scam-detector-base | https://huggingface.co/Horizon-Labs/phishing-scam-detector-base | Apache-2.0 | 491 dl/mo | 2026-10-31 | 307M (mmBERT-base); int8 ONNX 641 MB | **REUSE as zero-shot baseline.** Labels: fraud / spam / legitimate. Trained on 98k synthetic messages in ~70 languages (Qwen3.8-27B teacher) + FineWeb negatives. Card: real-smishing AUC 0.925; machine-translated SMS AUC ru 0.958; FPR 0.11 at 0.5. **kk is not in its language list**, so the Kazakh result is itself a finding. [DOC] Local test: §11. |
| RUSpam/spam_deberta_v4 | https://huggingface.co/RUSpam/spam_deberta_v4 | MIT | 341 dl | 2024-09-07 | 82M | SKIP. Russian Telegram ad-spam, not social-engineering scripts. |
| ruSpamModels/ruSpam_big | HF | **CC BY-NC-ND** | 6 dl | 2026-01-14 | DistilBERT | SKIP (no-derivatives license, spam). |
| BothBosu/*-caller-dialogue-scam-classifier | https://huggingface.co/BothBosu | (repo MIT) | <10 dl | 2024-05-31 | BERT/LSTM | SKIP. English only, trained on 1.6k synthetic dialogues. |

**Repos and datasets**

| Candidate | URL | License | Stars | Last push | Verdict and why |
|---|---|---|---|---|---|
| BothBosu: Synthetic-Data-for-Scam-Detection | https://github.com/BothBosu/Synthetic-Data-for-Scam-Detection-Leveraging-LLMs-to-Train-Deep-Learning-Models | MIT | 7 | 2025-05-20 | **REUSE (data) + REF (method).** Single-agent generator scripts (`code/generator/single_agent/scam_generator_*.py`) and multi-agent AutoGen notebooks. CSVs for 1,600 + 1,600 dialogues. Evaluation of **accuracy vs number of turns** and **suspect-only** turns, i.e. the EN version of the early-warning plot. Use the generator prompts as the template for KZ-scheme dialogues. [DOC] |
| BothBosu/youtube-scam-conversations | https://huggingface.co/datasets/BothBosu/youtube-scam-conversations | Apache-2.0 | 150 dl | 2024-08-13 | **REUSE** as a real EN out-of-domain check (<1k). |
| **ayaudildabekyzy-spec/kazakh_fraud_dataset** | https://github.com/ayaudildabekyzy-spec/kazakh_fraud_dataset | **none** | 0 | 2026-04-07 | **REF / training only with written permission.** 10,928 Kazakh Cyrillic SMS (8,582 fraud / 2,346 safe), 22 fine classes (otp_request, official_impersonation, family_emergency, …), 1,087 "seed" items, 10,035 unique normalised texts. The texts look LLM/template-generated, short and formal [RUN: sampled]. Two problems: no license (all rights reserved by default), and it was uploaded in one day. Its 16-class scam taxonomy is a useful checklist. Never put it in the test set. |
| KiteFlyKid/PreScam | https://github.com/KiteFlyKid/PreScam | none | 1 | 2026-10-06 | See §2. |
| kaustpradalab/Fraud-R1 | https://github.com/kaustpradalab/Fraud-R1 | none on GitHub (HF dataset card: MIT, gated) | 38 | 2025-06-29 | **REF.** EN/ZH only. It measures LLMs *as victims* of multi-round inducement (different task). Its "level-up" rewrites are a template for an adversarial test slice. |
| JimmyMa99/TeleAntiFraud (TeleAntiFraud-28k) | https://github.com/JimmyMa99/TeleAntiFraud | Apache-2.0 (LICENSE file) | 94 | 2026-04-17 | SKIP. Chinese audio-text, heavy. Cite as related work. |
| ChangMianRen/Telecom_Fraud_Texts_5 | https://github.com/ChangMianRen/Telecom_Fraud_Texts_5 | GPL-3.0 | 36 | 2025-01-07 | SKIP (Chinese). |
| rizzesh/Sachet | https://github.com/rizzesh/Sachet | none | 1 | 2026-10-23 | **REF.** Hindi/Hinglish real-time call-risk detector, "warn, never block". 17 scam + **14 genuine-control scenarios**: legit bank call *with* OTP warning, doorstep delivery code, polite telemarketing. Copy the idea of hard-negative scenarios for KZ (legit Kaspi/Halyk calls, legit collection reminders). |
| Ordalinnn/AI-Fraud-Detector | https://github.com/Ordalinnn/AI-Fraud-Detector | **All rights reserved** (custom) | 0 | 2026-11-04 | **Do not reuse.** Competitor awareness (see §0). Its obfuscation eval idea is worth reproducing independently: Latin look-alikes, invisible chars, spelled-out words, fullwidth. |
| umputun/tg-spam | https://github.com/umputun/tg-spam | MIT | 457 | 2026-11-14 | SKIP. Go Telegram anti-spam bot, mostly EN ad spam. |
| VusalShahbazovAz/smishing-AZ-SC | https://huggingface.co/datasets/VusalShahbazovAz/smishing-AZ-SC | CC BY 4.0 | 68 dl | 2026-05-08 | Optional. Azerbaijani (Turkic, Latin script) smishing, 1k–10k. Closest licensed Turkic scam data. |
| sukhrobnurali/uzbek_spam_dataset | HF | MIT | 42 dl | 2025-12-18 | Optional (Uzbek spam, 1k–10k). |

Already in 30-finance and confirmed:
- `dokster/adaption-scam-dataset-ru-en-v1` (Apache-2.0)
- `Abdurohman/fraudlens-ru-v1` (CC BY 4.0)
- `DmitryKRX/anti_spam_ru` (Apache-2.0)
- `alt-gnome/telegram-spam` (CC0)

**Gap re-confirmed [API]:** HF dataset filters `language:kk` × {spam, scam, fraud, phishing} return **0**. GitHub search for Kazakh scam/fraud returns only the unlicensed set above and the all-rights-reserved competitor.

---

## 2. Turn-level / streaming early warning

| Candidate | URL | License | Stars | Last push | Verdict |
|---|---|---|---|---|---|
| **PreScam** (COLM 2026, arXiv 2605.12243) | https://github.com/KiteFlyKid/PreScam | **none** | 1 | 2026-10-06 | **REF, the closest match.** "Real-time termination prediction" from conversation prefixes over 11,573 real scam conversations (full data on request; `data/demo.json` = 100). Baselines: `position_only`, `tfidf`, `mlp_*`, `lstm`, `transformer`, `hierarchical`, `bert`, `llm`. `termination_prediction/rt_detect/metrics.py` defines **AT@FPR**: pick τ so that FPR ≤ 10% via `roc_curve`, then alert time = `total_rounds − first_round_with_score ≥ τ`. Also reports firing rate. Reimplement it (no license). Copy the **position-only baseline**: risk = f(turn index). It is the honest check that the model isn't just learning "later turns are scammier". [DOC] |
| BothBosu repo | (§1) | MIT | 7 | 2025-05-20 | **REF.** Accuracy vs number of turns; suspect-only input. |
| eRisk ERDE / F_latency implementation (jmloyola/unsl_erisk_2022) | https://github.com/jmloyola/unsl_erisk_2022 (`src/utils/performance_metrics.py`: `erde`, `f_latency`, `speed`) | **GPL-3.0** | 3 | 2023-01-02 | **REF only** (GPL). The formulas take about 20 lines (below). |
| pyss3 (SS3 early text classifier) | https://github.com/sergioburdisso/pyss3 | MIT | 352 | 2025-10-16 | SKIP. A whole model family; not needed. |
| Papers without code | "It Warned Me Just at the Right Moment" arXiv 2502.03964 (per-turn LLM detection; recall vs timeliness trade-off); "Anatomy of Scam Scenarios"/EARS arXiv 2606.16052 (detects the scenario 1–2 turns after first evidence); SCRIPTMIND arXiv 2601.13581 (EACL 2026 Industry) | — | — | — | Cite as related work. Searched GitHub by title: no code found. |

**Metric recipe (reimplement, cite eRisk and PreScam):**
- `first_alert_turn` = first turn whose calibrated score ≥ τ, with τ fixed on validation at **1% FPR over benign conversations**. That FPR is counted per conversation (any alert in a benign conversation counts as an FP).
- **Lead time** = `ask_turn − first_alert_turn`, where `ask_turn` is the hand-annotated turn with the first request for a code, transfer, loan, app install or biometrics. Report the median and the share of scams warned **before** the ask.
- **ERDE_o** (Losada & Crestani 2016), per conversation:
  - cost = `c_fp` for an FP, `c_fn = 1` for an FN, `lc_o(k)` for a TP, 0 for a TN;
  - `lc_o(k) = 1 − 1/(1+e^{k−o})`;
  - `c_fp` = share of positives;
  - use o = 3 (dialogues have about 8–12 turns, not hundreds of posts).
- **F_latency** (Sadeque et al. 2018):
  - F_latency = `F1 × (1 − median_TP penalty(k))`, with `penalty(k) = −1 + 2/(1+e^{−p(k−1)})`;
  - choose `p = ln 3 / (k_half − 1)` so that the penalty is 0.5 at turn `k_half` (e.g. 5).

---

## 3. Kazakh-capable encoders and tokenizers

**Measured tokenizer behaviour [RUN].** The same sentence was written five ways: Kazakh, keyboard Kazakh (Russian letters only), chat Latin, Russian, and mixed KK-RU. Values are tokens per whitespace word, so lower is better.

| Tokenizer (model) | vocab | kk | kk keyboard | kk Latin | ru | mixed | 18 KK letters OK | round-trip exact |
|---|---|---|---|---|---|---|---|---|
| xlm-roberta-base (also mE5-*, bge-m3) | 250k | **2.13** | 3.07 | 3.07 | 1.47 | 2.46 | 18/18, 0 UNK | yes |
| LaBSE | 501k | 2.20 | 2.87 | 2.93 | 1.42 | 2.38 | 18/18 | yes |
| mdeberta-v3-base | 250k | 2.73 | 3.00 | 3.40 | 1.79 | 2.54 | 18/18 | yes (**needs `sentencepiece`**; it failed to load without it under transformers 5.9) |
| **kaz-roberta-conversational** | 52k byte-BPE | **1.80** | 2.73 | 4.13 | 1.47 | **1.69** | 18/18 | yes |
| KazBERT | 32k | 2.33 | 2.93 | 4.27 | 1.84 | 2.62 | 18/18 | — |
| mBERT cased | 120k | 3.53 | 3.67 | 3.53 | 1.95 | 3.08 | 18/18 | — |
| mmBERT-base (Gemma tokenizer) | 256k | **4.33** | 3.67 | 3.13 | 1.58 | 3.00 | 18/18 | yes, but it splits `Сіздің` → `Сі`,`з`,`ді`,`ң` |
| NLLB-200 (Tilmash's tokenizer) | 256k | 2.20 | 3.00 | 2.93 | 1.58 | 2.38 | 18/18 | — |
| Qwen3-Embedding-0.6B | 152k | 5.53 | 4.33 | 3.60 | 1.84 | 4.08 | 18/18 | — |
| issai/Qwen3.5-4B-Kazakh (+16k KK vocab) | 264k | 2.20 | 2.93 | 3.33 | 2.05 | 2.46 | 18/18 | — |

What this shows:
- No modern tokenizer produces UNK on Kazakh letters. The real differences are fertility, and the **keyboard-Kazakh penalty**: XLM-R +44% tokens, which means the word forms are out of distribution. That is the measurable reason the restoration step (§4) should help. Report it.
- None of the tested tokenizers lowercases or strips accents. The Kazakh letters have no Unicode decomposition anyway, but `й` and `ё` would be damaged by uncased BERTs. Avoid `*-uncased` models.

| Model | URL | License | Params | Last update | Verdict |
|---|---|---|---|---|---|
| **xlm-roberta-base** | https://huggingface.co/FacebookAI/xlm-roberta-base | MIT | 278M | 2024-02 | **REUSE: main fine-tune backbone.** Fits a T4 at fp16, batch 32, max_len 256. |
| **multilingual-e5-base** | https://huggingface.co/intfloat/multilingual-e5-base | MIT | 278M | 2026-04 | **REUSE: frozen embeddings + LR baseline** (prefix `query: `). On Kazakh retrieval mE5-base Hits@1 = 25.9% vs LaBSE 7.5% (`shyngys879/kazakh-e5-rag-embedding` card). `-small` (118M) is the fast CPU option. |
| xlm-roberta-large / multilingual-e5-large | HF | MIT | 560M | — | Only if time remains. About 3× slower; on KazSAnDRA the gain was ≤0.01 F1. |
| **kaz-roberta-conversational** | https://huggingface.co/kz-transformers/kaz-roberta-conversational | Apache-2.0 | **83.5M** (6 layers) | 2025-10-03 | **REUSE as ablation.** Pretrained on MDBKD (24.9M texts) + **Beeline KZ customer-support dialogues**, i.e. call-centre domain. Best kk/mixed fertility. Weak on Latin translit (4.13). A clean "small Kazakh-native vs big multilingual" fairness comparison. |
| mdeberta-v3-base | https://huggingface.co/microsoft/mdeberta-v3-base | MIT | 278M | 2023-04 | SKIP. Worse Kazakh fertility and extra tokenizer dependencies. |
| LaBSE | https://huggingface.co/sentence-transformers/LaBSE | Apache-2.0 | 471M | 2025-03 | SKIP (weak on Kazakh retrieval; large). |
| bge-m3 | https://huggingface.co/BAAI/bge-m3 | MIT | 568M | 2024-07 | REF. Only for very long transcripts (8k context). |
| mmBERT-base | https://huggingface.co/jhu-clsp/mmBERT-base | MIT | 307M | 2025-10 | SKIP as a backbone (fragments Kazakh). |
| KazBERT | https://huggingface.co/Eraly-ml/KazBERT | Apache-2.0 | 111M | 2026-07 | SKIP (kaz-roberta is better on every tokenisation measure). |
| nur-dev/roberta-kaz-large | HF | AFL-3.0 | 355M | 2024-08 | SKIP. |
| **issai/Qwen3.5-4B-Kazakh** | https://huggingface.co/issai/Qwen3.5-4B-Kazakh | Apache-2.0 | 4.58B | 2026-08-19 | **REUSE as the zero-shot LLM arm.** KazMMLU 78.5 vs 72.5 for base Qwen3.5-4B (card). M5: `mradermacher/Qwen3.5-4B-Kazakh-GGUF` Q4_K_M via llama.cpp / LM Studio. T4: fp16 (~9 GB). It is a thinking model, so disable thinking or cap tokens for classification. |
| issai/LLama-3.1-KazLLM-1.0-8B | HF | **CC BY-NC 4.0**, gated | 8B | 2024-12 | Optional, older. |
| inception42/Llama-3.1-Sherkala-8B-Chat | HF | **CC BY-NC-SA 4.0**, gated | 8B | 2025-03 | Optional. The org was renamed: `inceptionai/…` now redirects (307) to `inception42/…`. |
| shyngys879/kazakh-e5-rag-embedding | HF | "other" | 278M | 2026-08 | REF (license unclear; retrieval-tuned). |

Evidence that backbone choice is second-order: on KazSAnDRA polarity (imbalanced), macro-F1 is mBERT 0.80, XLM-R 0.81, RemBERT 0.81 (https://github.com/IS2AI/KazSAnDRA README). Spend time on data, not backbone search.

---

## 4. Keyboard-Kazakh restoration, transliteration, homoglyphs, language ID

| Candidate | URL | License | Stars | Last push | Verdict |
|---|---|---|---|---|---|
| **YX_KazQwerty** | https://github.com/Bexull/YX_KazQwerty | Code **MIT**; data `Resources/kazakh/*` **CC BY-SA 4.0** | 0 | 2026-11-02 | **REUSE (data) + port the logic.** It is a macOS/Windows keyboard with on-device autocorrect: Kazakh typed with Russian letters → proper Kazakh, Russian left alone ("салеметсизбе" → "Сәлеметсіз бе"). Files: `dictionary.tsv` (5.6 MB), `context.tsv`, `endings.tsv`, `pairs.tsv`, and test sets `Tools/TypingTests/{chat-phrases,colloquial,holdout-kazakh,holdout-russian}.tsv`. Built from Leipzig kaz_newscrawl (CC BY), OpenSubtitles frequency lists (CC BY-SA) and KazSAnDRA (CC BY). Author-reported: colloquial 203/204 (99.5%), unseen holdout 39/40 (97.5%); any change to Russian counts as an error. Its research doc gives the useful rule: **don't replace a typed word that is itself frequent Kazakh (≥15% of the best form)**, e.g. сал/сәл, кен/кең. Format [RUN]: `аак<TAB>аақ:26<TAB>a`, i.e. folded form → candidates with counts. Swift and Go only, so write a ~40-line Python lookup. Share-alike covers only the dictionary. |
| danatussupbekova/Kazakh-Text-Normalization | https://github.com/danatussupbekova/Kazakh-Text-Normalization | none | 0 | 2025-03-26 | REF. Word-pair CSV (тилеймин→тілеймін) + Keras char seq2seq. Use the pairs only as an extra eval list, with attribution. |
| daniyar51/kazroberta-kazakh-spelling-detector | HF | — | 35 dl | 2026-10-28 | SKIP. A detector, not a restorer. |
| nurzhankanatzhanov/latinKazakh | https://github.com/nurzhankanatzhanov/latinKazakh | MIT | 0 | 2023-07-15 | REF for Cyrillic↔Latin tables. |
| talgautb/qazlatyn-db | https://github.com/talgautb/qazlatyn-db | MIT | 19 | 2024-04-16 | REF (raw Latin-alphabet data). |
| PyPI Kazakh transliterators | — | — | — | — | **None maintained**: `kaz-translit`, `qazlatyn`, `kazakh-latin` etc. don't exist; `cyrtranslit` 1.2.0 has no Kazakh. Write two maps yourself: official 2021 Latin (á ǵ ı ń ó ú ý …) and informal chat Latin (q, gh, sh, ch, j, y, i). |
| confusable-homoglyphs | https://pypi.org/project/confusable-homoglyphs/ | MIT | — | 2024-01 | REF. A hand map of ~20 Latin↔Cyrillic look-alikes is enough. **Caution:** Kazakh `і` (U+0456) is a real letter that looks like Latin `i`. Map Latin `i` → `і` inside Cyrillic words, and never `і` → `и`. `unidecode` is GPL, so SKIP it; `ftfy` (Apache-2.0) fixes mojibake. |
| **lingua-language-detector** 2.2.0 | https://github.com/pemistahl/lingua-py | Apache-2.0 | 1,819 | 2026-07-20 | **REUSE as tie-breaker** for language-group tags. It supports Kazakh and mixed-language spans. Local test: §11. |
| GlotLID / OpenLID-v3 | https://huggingface.co/cis-lmu/glotlid ; HPLT/OpenLID-v3 | "other" / **GPL-3.0** | — | — | SKIP (license; fastText-level only). |

**Recommended language-group tagger:**
- `kk`: any of ә ғ қ ң ө ұ ү һ і present.
- `kk_keyboard`: Cyrillic, no KK letters, and ≥2 hits from a Kazakh function-word list after folding (мен, сен, жок, бар, кой, гой, ушин, бул, кандай, рахмет …).
- `kk_latin`: Latin script plus a Kazakh translit word list.
- `ru` / `mixed`: lingua.
- Every test item is hand-checked anyway.

**Rule-matcher trick:** fold *both* the pattern list and the input with the keyboard map (қ→к, ғ→г, ү/ұ→у, ө→о, ә→а, і→и, ң→н, һ→х) plus the homoglyph map. One pattern then matches proper, keyboard and look-alike spellings.

---

## 5. Translation for augmentation (EN/RU → KK)

| Candidate | URL | License | Size | Verdict |
|---|---|---|---|---|
| **issai/tilmash** | https://huggingface.co/issai/tilmash | Not stated in API metadata. Fine-tuned from `facebook/nllb-200-distilled-1.3B` (KazParC `scripts/train.py` line 13), so treat it as **CC BY-NC 4.0** | 1.3B (m2m_100, `pytorch_model.bin`) | **REUSE (primary).** FLORES chrF RU→KK 0.54 vs NLLB 0.49; EN→KK 0.60 vs 0.49 (KazParC paper, see 40-languages.md). **Gated (auto-approve): the local HF token got 403 "not in the authorized list" today, so click "Agree" on the model page before Kaggle needs it.** Gotcha: KazParC `predict.py` uses `tokenizer.lang_code_to_id[...]`, which **no longer exists in transformers 5.9** [RUN: grep]. Use `forced_bos_token_id=tok.convert_tokens_to_ids("kaz_Cyrl")`. |
| facebook/nllb-200-distilled-600M | https://huggingface.co/facebook/nllb-200-distilled-600M | **CC BY-NC 4.0** | 600M; CT2-int8 copy `JustFrederik/nllb-200-distilled-600M-ct2-int8` 623 MB | **REUSE (second system).** |
| facebook/nllb-200-distilled-1.3B | HF | CC BY-NC 4.0 | 1.3B | Optional (Tilmash's base; isolates the KazParC fine-tune effect). |
| **CTranslate2** 4.9.0 | https://github.com/OpenNMT/CTranslate2 | MIT | — | **REUSE** for speed. Run `ct2-transformers-converter --model <tilmash_dir> --output_dir tilmash-ct2 --quantization int8_float16`, then `Translator(..., device="cuda")` and `translate_batch(src_tokens, target_prefix=[["kaz_Cyrl"]]*n, beam_size=2, max_batch_size=32)`. |
| tencent/Hy-MT2-1.8B | https://huggingface.co/tencent/Hy-MT2-1.8B | Apache-2.0 | 1.8B, GGUF available | Optional permissive alternative. kk is supported, but there is no Kazakh benchmark on the card. |
| google/madlad400-3b-mt | HF | Apache-2.0 | 3B (T5) | SKIP. Slow; T5-family models are fragile in fp16 and the T4 has no bf16. |
| google/translategemma-4b-it | HF | Gemma, manual gate | 4B | SKIP (manual gate). |

**Speed.**
- No published T4 throughput for NLLB/Tilmash exists. Search found only vague "~100 ms/sentence" claims and "CT2 is 2–5× faster".
- Local M5 CPU measurement: §11.
- Plan a 200-sentence pilot on the Kaggle T4 before translating everything. The BothBosu corpus is ≈1,600 dialogues × ~10 turns ≈ 16k segments per target language.

---

## 6. Calibration, conformal prediction, selective prediction, threshold at fixed FPR

| Candidate | URL | License | Stars | Latest | Verdict |
|---|---|---|---|---|---|
| **scikit-learn 1.9.1** `CalibratedClassifierCV(FrozenEstimator(est), method="temperature")` | https://scikit-learn.org | BSD-3 | — | 2026-09-10 | **REUSE.** Temperature scaling was added in 1.8; `cv="prefit"` is deprecated in favour of `FrozenEstimator` [Context7]. `calibration_curve` covers the reliability diagram. `roc_curve` covers threshold at FPR. `TunedThresholdClassifierCV` is available. |
| **crepes** 0.9.1 | https://github.com/henrikbostrom/crepes | BSD-3 | 586 | 2026-06-12 | **REUSE for the abstain band.** `ConformalClassifier().fit(hinge(P_cal, classes, y_cal), bins=lang_cal)` then `predict_set(hinge(P_test), bins=lang_test, confidence=0.9)`. Set {scam} → warn, {legit} → ok, {scam, legit} → **abstain**, Mondrian **per language group** [Context7]. It works on precomputed probabilities, so no sklearn wrapper is needed. |
| **MAPIE** 1.6.0 | https://github.com/scikit-learn-contrib/mapie | BSD-3 | 1,679 | 2026-11-10 | **REUSE for the guaranteed threshold.** `BinaryClassificationController(predict_function=f, risk=<fpr>, target_level=…, confidence_level=0.9).calibrate(X_conf, y_conf)` (Learn-Then-Test). Supported risks: precision, recall, accuracy, **false-positive rate**, predicted-positive fraction. MAPIE has **no dedicated Mondrian estimator**, which is why crepes handles the per-language part. Use the string name of the FPR risk from the MAPIE docs. |
| netcal 1.4.0 | https://github.com/EFS-OpenSource/calibration-framework | Apache-2.0 | 383 | 2026-04-16 | Optional. ECE + reliability diagrams with confidence intervals. |
| torchmetrics 1.9.0 | https://github.com/Lightning-AI/torchmetrics | Apache-2.0 | 2,483 | 2026-03 | **REUSE (utility).** `BinarySensitivityAtSpecificity(min_specificity=0.99)` = recall at 1% FPR; `BinaryRecallAtFixedPrecision`. |
| TorchCP 1.2.1 | https://github.com/ml-stat-Sustech/TorchCP | **LGPL-3.0** | 484 | 2025-10 | SKIP (research toolbox; overkill). |
| aangelopoulos/conformal-prediction | https://github.com/aangelopoulos/conformal-prediction | MIT | 1,112 | 2025-11 | REF. Notebooks for the "gentle intro" paper, including selective classification. Good for the write-up citation. |
| gpleiss/temperature_scaling | https://github.com/gpleiss/temperature_scaling | MIT | 1,182 | 2025-07 | REF. Superseded by sklearn 1.8+. |
| apple ml-calibration (relplot) | https://github.com/apple-aiml-research/ml-calibration | custom (Apple) | 191 | 2026-09 | Optional (smooth ECE). |

**Caveat to state in the write-up:** conformal guarantees hold only if the calibration data is exchangeable with the test data. Calibrating on synthetic/translated validation data and testing on real KZ messages breaks that assumption. Use repeated random 50/50 calibration/test splits **of the real set**, report mean ± sd coverage and abstain rate, and show the synthetic-calibrated version as the "what goes wrong" contrast.

---

## 7. Explanations and rule matchers

| Candidate | URL | License | Stars | Latest release | Verdict |
|---|---|---|---|---|---|
| **Word-level occlusion** (own code) | — | — | — | — | **REUSE (demo).** Split on whitespace, drop one word at a time, score the n variants in one batch, highlight = drop in P(scam). Model- and tokenizer-agnostic, so no Cyrillic subword merging is needed. Feeds straight into `gr.HighlightedText([(word, score), …])`. [RUN on mmBERT model, §11.] |
| **Captum** 0.9.0 | https://github.com/meta-pytorch/captum | BSD-3 | 5,722 | 2026-04-17 | **REUSE (report figure).** `LayerIntegratedGradients(forward_fn, model.roberta.embeddings)`. Sum attributions over the subwords of each word using `tokenizer(..., return_offsets_mapping=True)` / `word_ids()`. |
| shap 0.54.1 | https://github.com/shap/shap | MIT | 25,862 | 2026-10-16 | Optional. `shap.Explainer(pipeline)` with the Text masker needs a fast tokenizer (XLM-R has one), but it needs hundreds of forward passes per text, so it is slow on CPU. |
| transformers-interpret 0.10.0 | https://github.com/cdpierse/transformers-interpret | Apache-2.0 | 1,417 | **2023-04** | SKIP. Unmaintained; untested on transformers 5.x. |
| ferret-xai 0.4.2 | https://github.com/g8a9/ferret | MIT | 216 | 2024-01 | SKIP. **Pins `transformers<5` and `captum<0.8`.** |
| lime 0.2.0.1 | https://github.com/marcotcr/lime | BSD-2 | 12,170 | 2020 | SKIP (stale; occlusion is simpler). |
| pyahocorasick 2.3.1 | https://github.com/WojciechMula/pyahocorasick | BSD-3 | 1,136 | 2026-04-27 | Optional. Use it if the phrase list exceeds a few hundred entries. |
| flashtext 2.7 | https://github.com/vi3k6i5/flashtext | MIT | 5,710 | release 2018 | SKIP. Word-boundary logic is Latin-centric and it is unmaintained. |
| RapidFuzz | https://github.com/rapidfuzz/RapidFuzz | MIT | 4,203 | 2026-11-09 | Optional. Fuzzy phrase match for typos ("кодты"/"кодын"). |

**Rule baseline design:** one `re` pattern per official red flag. Kazakh is agglutinative, so use stems with `\w*` (e.g. `код\w*`, `қауіпсіз\w* (шот|қызмет)\w*`, `безопасн\w* сч[её]т`, `anydesk|rustdesk|эни ?деск`). Match on the folded text (§4). The pattern name doubles as the scheme label and the trigger highlight.

---

## 8. Demo and serving

| Candidate | URL | License | Stars | Latest | Verdict |
|---|---|---|---|---|---|
| **Gradio** 6.32.0 | https://github.com/gradio-app/gradio | Apache-2.0 | 44,054 | 2026-11-12 | **REUSE.** `gr.HighlightedText` accepts `list[(word, float)]` for importance colouring and `(span, "SCHEME")` for rule hits [Context7]. Use `gr.Label` for scheme probabilities, `gr.LinePlot` for per-turn risk, and `gr.Chatbot` or a "next turn" button to simulate a running call. Starting points: `demo/text_analysis`, `demo/highlightedtext_component` in the Gradio repo. |
| HF Spaces (free) | https://huggingface.co/docs/hub/spaces-overview | — | — | — | **Changed policy [DOC]:** "Gradio and Docker Spaces run on compute and require a paid plan to create". CPU Basic is 2 vCPU / 16 GB / 50 GB non-persistent and sleeps when unused. Static Spaces are free. **Free personal accounts can host up to 2 ZeroGPU Gradio Spaces**, but only if the account is more than 30 days old with a verified email. ZeroGPU details: Python 3.12.12 / 3.10.13, torch 2.8–2.13, daily visitor GPU quota 2 min unauthenticated / 5 min free account, `@spaces.GPU` (`spaces` 0.52.0). A 278M classifier needs well under 1 s of GPU per call. |
| Gradio share link | — | — | — | — | `demo.launch(share=True)`. The sharing guide says links expire after **1 week**; the quickstart still says 72 h, so plan for 72 h. Fine as a backup for judging. |
| **aiogram** 3.31.0 | https://github.com/aiogram/aiogram | MIT | 5,936 | 2026-08-26 | **REUSE.** Start from `examples/echo_bot.py` and replace the echo with `score(message.text)`. Forwarded messages arrive as normal text. Voice notes would need ASR (stretch). |
| python-telegram-bot 22.8 | https://github.com/python-telegram-bot/python-telegram-bot | **LGPL-3.0** (GitHub shows GPL-3.0 because of the LICENSE file pair) | 29,592 | 2026-06-12 | Alternative. aiogram is lighter. |
| wakaree/aiogram_bot_template | https://github.com/wakaree/aiogram_bot_template | MIT | 167 | 2026-07-19 | SKIP (Postgres + alembic is overkill). |
| bogkonstantin/android_income_sms_gateway_webhook | https://github.com/bogkonstantin/android_income_sms_gateway_webhook | MIT | 709 | 2026-06-13 | Optional stretch. Android app that POSTs incoming SMS to a URL, giving a real "SMS arrives → warning" demo without copy-paste. `capcom6/android-sms-gateway` (Apache-2.0, 6,012★) is the heavier alternative. |

---

## 9. Experiment-loop references

| Candidate | URL | License | Verdict |
|---|---|---|---|
| **transformers `run_classification.py` @ v5.19.0** | https://github.com/huggingface/transformers/blob/v5.19.0/examples/pytorch/text-classification/run_classification.py | Apache-2.0 | **REF / copy at a pinned tag.** The whole `examples/pytorch` folder was **removed from `main` on 2026-10-13** (PR #49357), so unpinned links 404. Latest release is v5.23.0 (2026-11-13). |
| HF task guide "Text classification" | https://github.com/huggingface/transformers/blob/main/docs/source/en/tasks/sequence_classification.md | Apache-2.0 | **REUSE as skeleton** (~60 lines): `AutoModelForSequenceClassification` + `Trainer` + `compute_metrics`. Add `EarlyStoppingCallback(early_stopping_patience=2)` with `load_best_model_at_end=True`, `metric_for_best_model="pr_auc"`, `eval_strategy="epoch"`, `save_strategy="epoch"`, `report_to="none"`, `fp16=True`. Dump `trainer.state.log_history` to JSON. |
| **fairlearn** 0.15.0 `MetricFrame` | https://github.com/fairlearn/fairlearn | MIT | **REUSE.** Use `MetricFrame(metrics={"recall": recall_score, "fpr": fpr_fn, "n": count}, y_true, y_pred, sensitive_features=df.lang_group)`; `.by_group`, `.difference()` and `.ratio()` give the per-language fairness table in one call. |
| SetFit 1.2.0 | https://github.com/huggingface/setfit | Apache-2.0 | Optional. Few-shot arm (e.g. 8–32 real KZ examples per class, on mE5) if the real data is tiny. |
| model2vec 0.10.0 | https://github.com/MinishLab/model2vec | MIT | Optional. Static-embedding CPU baseline. Its distill extra pins `transformers<5.4`. |
| trackio | https://github.com/gradio-app/trackio | — | Covered in 50-ml-pipeline.md. Plain JSON is enough here. |

**Per-group plus CI recipe:** bootstrap over conversations (`scipy.stats.bootstrap` or 1,000 resamples), stratified by language group. Report recall@1%FPR, PR-AUC, median lead time, abstain rate and coverage per group, each with a 95% CI.

---

## 10. License flags

| Item | License | Consequence |
|---|---|---|
| issai/tilmash, NLLB-200 (all sizes), CT2 copies | CC BY-NC 4.0 (Tilmash inferred from its NLLB base) | Non-commercial. Fine for the hackathon; translated training data inherits "research use". |
| KazLLM-8B | CC BY-NC 4.0 | Non-commercial. |
| Sherkala-8B | CC BY-NC-SA 4.0 | Non-commercial + share-alike. |
| YX_KazQwerty dictionary | CC BY-SA 4.0 | Attribution; a redistributed modified dictionary must stay CC BY-SA. |
| kazakh_fraud_dataset, PreScam, Sachet, Fraud-R1 (GitHub), Kazakh-Text-Normalization | **No license** | Default "all rights reserved". Read and cite; don't redistribute; reimplement metrics yourself. |
| Ordalinnn/AI-Fraud-Detector | Custom "All rights reserved" | Don't copy anything. |
| ruSpam_big | CC BY-NC-ND | No derivatives, so you can't fine-tune and share. |
| OpenLID-v3, jmloyola eRisk code | GPL-3.0 | Don't vendor the code. |
| python-telegram-bot | LGPL-3.0 | Fine as a dependency. |
| TorchCP | LGPL-3.0 | Fine as a dependency (not picked). |

---

## 11. Local verification [RUN] (Apple M5, 2026-11-14)

**A. Tokenizers:** the table in §3. Scripts: `transformers` 5.9 global env, plus a uv env (`transformers<5`, `sentencepiece`) for mdeberta.

**B. Off-the-shelf multilingual scam model on hand-written KZ examples** (`Horizon-Labs/phishing-scam-detector-base`, fp32 on MPS; 12 texts written by me, so this is illustrative, **not** an evaluation):

| true | lang | P(fraud) | text (truncated) |
|---|---|---|---|
| scam | kk | 0.777 | Сіздің атыңызға кредит рәсімделіп жатыр. Тоқтату үшін SMS-кодты айтыңыз… |
| scam | kk keyboard | 0.843 | Сиздин атыныза кредит расимделип жатыр… SMS-кодты айтыныз… |
| scam | kk Latin | 0.942 | Sizdin atynyzga kredit rasimdelip jatyr… |
| scam | **ru** | **0.336 (miss at 0.5)** | На ваше имя оформляется кредит. Чтобы отменить, продиктуйте код из SMS… |
| scam | mixed | 0.983 | Сәлеметсіз бе, мен Kaspi службы безопасности… кодты срочно айтыңызшы |
| scam | ru | 0.894 | Это следователь КНБ… оформите кредит… безопасный счёт |
| scam | kk | 0.981 | Мама, телефоным бұзылды… Шұғыл 50 000 теңге аударып жіберші |
| legit | ru | 0.003 | Код подтверждения: 4821. Никому не сообщайте этот код… |
| legit | kk | 0.005 | Растау коды: 4821. Бұл кодты ешкімге… айтпаңыз |
| legit | ru | 0.170 | Напоминаем: платёж по кредиту 25 400 ₸… |
| legit | kk | 0.001 | Сәлем апа, кешке үйге барамын… |
| legit | **mixed** | **0.562 (false alarm)** | Мен кеше Kaspi-ге перевод жасадым, но деньги әлі түскен жоқ… |

Word-occlusion on the first text ranks `айтыңыз` (0.51 drop), `жатыр`, `SMS-кодты` and `Сіздің` as the top contributors. The trigger highlight works without subword handling.

**Implication.** This is a **strong, free baseline that already transfers to Kazakh** on easy single messages:
- It separates legit OTP texts from code-theft texts in both languages.
- Its two errors are a Russian "credit + SMS code" scam it rated low, and a false alarm on benign code-switched chat.

The project has to beat it honestly on the real KZ test set, ideally on **early turns of dialogues**, where a message-level model has not been trained. Add a fourth arm: **fine-tune this Apache-2.0 checkpoint** on the KZ data (scam-aware initialisation) alongside xlm-roberta-base. Ignore the 48 s wall time, which was dominated by first-call MPS warm-up.

**C. Keyboard-Kazakh restoration: a naive 40-line Python port of the YX_KazQwerty dictionary** (`dictionary.tsv` only, best form unless the Russian flag `R`/`x` is set or the typed form is ≥15% as frequent; plus a phrase gate that skips phrases with more Russian-flagged than Kazakh-only words), scored on the repo's own test files:

| file | phrases exact | words correct |
|---|---|---|
| holdout-kazakh.tsv (unseen by author) | 28/40 | 101/117 (86.3%) |
| chat-phrases.tsv | 119/204 | 300/394 (76.1%) |
| holdout-russian.tsv (must stay unchanged) | 17/20 | 66/69 (95.7%). The changed ones are Kazakh names inside Russian phrases (Нурлан→Нұрлан, Айгерим→Әйгерім, Казан→Қазан). |

Example: "Ешкимге айтпаныз, бул оте манызды" → "Ешкімге айтпаңыз, бұл өте маңызды" (perfect). Example: "сиздин атыныза кредит расимделип жатыр" → "сіздің **атыныза** кредит рәсімделіп жатыр" (inflected form missed). The author's Swift app reaches 97.5–99.5% by also using `endings.tsv` (suffix rules), `context.tsv` (bigrams) and joins. **Porting `endings.tsv` is the next 1–2 h** if restoration becomes a reported component. Otherwise the naive port is enough for training-time augmentation and as a "+restore" ablation.

---

## Sources
GitHub repo pages as listed (metadata via `gh api repos/<owner>/<repo>`). Hugging Face model and dataset pages as listed (via `https://huggingface.co/api/...`). PyPI JSON API for versions. Hugging Face Spaces docs https://huggingface.co/docs/hub/spaces-overview and https://huggingface.co/docs/hub/spaces-zerogpu. Gradio docs (Context7 `/gradio-app/gradio`, `/websites/gradio_app`). MAPIE docs (Context7 `/scikit-learn-contrib/mapie`). crepes docs (Context7 `/henrikbostrom/crepes`). scikit-learn 1.9.1 docs (Context7 `/scikit-learn/scikit-learn/1.9.1`). Papers: PreScam arXiv 2605.12243; 2502.03964; 2606.16052; 2601.13581; Fraud-R1 2502.12904; KazParC 2403.19399.
