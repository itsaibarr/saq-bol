# Сақ бол: scam early warning for Kazakhstan, in Kazakh, Russian and the mix people actually type

Track: AI + Finance. Spec v0, written 2026-11-14 15:35 (UTC+5) before any model was trained. Amendments go at the bottom with a timestamp; nothing above the line changes after results exist.

## 1. Problem, user, moment

User: Gulnara apa, 67, a Kazakh-first pensioner in Astana. Secondary user: the grandchild who sets the tool up.
Moment: a message or call from "Kaspi security", "the KNB investigator" or "eGov" arrives, seconds before she reads out an SMS code, takes an online loan "to protect her money" or moves savings to a "safe account".
Why now (sources in research/30-finance.md): 27,892 internet-fraud cases in KZ in 2025 (record); phone scams are 22% of schemes (NBK); scammer-dictated loans cost 20.3 bn tenge in 2024 (ARDFM); since 1 Oct 2026 lenders must ask 7 anti-fraud questions before any online loan, two of which ("did someone calling as bank/police security contact you", "are you moving money to a safe account") are what this model detects. No public labelled Kazakh scam dataset exists (checked HF, Kaggle, GitHub on 2026-11-14).

## 2. Input and output

Input: one message (SMS, WhatsApp, Telegram) or a running call transcript, in Kazakh, Russian, mixed Kazakh-Russian, Kazakh typed with Russian look-alike letters ("keyboard Kazakh"), or English.
Output: risk band (safe / suspicious / scam) from a calibrated score, the phrase that drove it, the matched scheme, one line of advice in the user's language.

## 3. Scope

Must (core):
- Real KZ test set, hand-collected verbatim from public sources with URL and date (data/real_test/). Never used for training.
- Training mix: public RU/EN scam and spam data, EN/RU items machine-translated to Kazakh, synthetic KZ-scheme messages in kk / ru / mixed / keyboard-Kazakh (all marked synthetic).
- Baselines B0-B3 (section 5) and one fine-tuned multilingual encoder.
- Per-language results (kk, ru, mixed, kbd, en): recall, false-positive rate, PR-AUC, with bootstrap 95% CIs.
- One fairness intervention for the language gap, measured before and after.
- Failure analysis: at least 5 real misses and 5 real false alarms, explained.
- Gradio demo, Colab notebook with outputs, README write-up, credits.
Should (stretch, only after the core is frozen):
- Turn-by-turn early warning on dialogues (metric: share of scam dialogues flagged before the "ask" turn; FPR on legit dialogues).
- Zero-shot LLM comparison (B4).
- Model soup of the best fine-tunes.
Out: voice/ASR input, Telegram bot, deepfake audio, transaction data.

## 4. Data and splits

- REAL set = verbatim public items (scam + legit hard negatives). Split once, grouped by parallel_group and source page, stratified by language: 30% real-dev (model selection, thresholds), 70% real-test (reported numbers). Real-test is scored only for frozen candidates, logged in RUNS.md each time.
- Easy negatives for FPR: held-out slice of real Kazakh/Russian Telegram messages (kurumikz/telegram-corpus-russian-kazakh) never used in training.
- Synthetic generators never see real items. Synthetic items carry synthetic=true and are excluded from every headline number.
- Leakage control: drop any training item whose normalized text has char-5gram Jaccard ≥ 0.5 or embedding cosine ≥ 0.92 to any real item; report how many were dropped.
- Unseen-scheme check: schemes chosen from counts alone (before any prediction) are excluded from synthetic generation; their real items form a "new scheme" slice.
- Date slice: real items published in 2026 vs earlier, reported separately.

## 5. Models

- B0: label everything safe.
- B1: official red-flag keyword rule (kk + ru phrases from bank, NBK and ARDFM warnings, written before seeing the test set).
- B2: "generic team" model: TF-IDF + logistic regression trained only on English SMS Spam + Russian spam data.
- B3: TF-IDF char 1-5 grams + logistic regression on our full training mix.
- M: fine-tuned multilingual encoder (candidates xlm-roberta-base, intfloat/multilingual-e5-base, mdeberta-v3-base; a Kazakh-specific encoder if one passes a tokenizer check). HF Trainer, early stopping on real-dev PR-AUC.
- B4 (stretch): zero-shot instruction LLM with a fixed prompt.
- Calibration: temperature scaling on real-dev. Thresholds: "scam" at the score giving ≤1% FPR on dev negatives; "suspicious" band below it, set on dev.
- Soup (the CLI) is used only if an LLM arm is trained; the encoder uses HF Trainer (research/50-ml-pipeline.md, section 1).

## 6. Metrics

Headline: on real-test, recall of scam at the frozen threshold, FPR on legit hard negatives and on Telegram negatives (reported separately), PR-AUC. Every number per language, with bootstrap 95% CI. Missed scams (FN) and false alarms (FP) reported separately, as the brief asks.
Fairness: language gap = max minus min recall across kk / ru / mixed / kbd.

## 7. Pre-registered predictions (written before training)

P1. B1 (keyword rule) has precision ≥ 0.9 but recall < 0.6 on real-test, lowest on kbd.
P2. B2 (generic spam model) recall on kk is at least 20 points below its recall on ru.
P3. M beats B3 on PR-AUC on real-test overall, with the biggest gain on mixed and kbd.
P4. Adding keyboard-Kazakh augmentation cuts M's kk-vs-kbd recall gap by at least half, at less than 1 point FPR cost.
P5. Unseen-scheme recall is lower than seen-scheme recall by 10+ points.

## 8. Timeline (UTC+5)

- Sat 18:00: real set collected and split; training mix built; B0-B3 scored on real-dev.
- Sun 02:00: first encoder fine-tunes done; council round 1 on results.
- Sun 12:00: fairness intervention measured; stretch items decided; council round 2.
- Sun 20:00: model freeze. Real-test scored once for the final model.
- Mon 02:00: notebook, README, demo, video ready; council round 3; first submission.
- Mon 09:59: hard deadline. Last resubmission by Mon 08:30.

## Amendments

### A1. 2026-11-14 16:00 UTC+5 (data facts, before any model was trained)
- Real set: 266 verbatim items from 40+ public KZ pages (179 scam, 87 legit), every text script-checked against the saved page. Evidence levels kept: reproduced (65), typical_example (60), quoted call phrase (kk, 132 incl. some lists), paraphrase (17, excluded from headline numbers).
- Real legit items are mostly official warnings (68 of 87), i.e. texts that describe scams. Transactional legit texts (OTP, notifications) are scarce (about 19). FPR on everyday messages comes from a separate real pool: 2,826 held-out Telegram chat lines (kk 811, mixed 279, kbd 36, ru 1,500, en 200), split 30/70 into dev/test.
- Split (build_real.py): grouped by source page and parallel_group, 30% of groups to real-dev. real-dev 59 scam / 29 legit; real-test 120 scam / 58 legit.
- Real mixed and keyboard-Kazakh scam texts are essentially absent from public sources. Replacements, fixed now: (a) a paired kk/ru test on the 47 items that have an official parallel version (same scam, two languages); (b) a controlled perturbation set: every real Kazakh item folded to keyboard-Kazakh (134 items, labels unchanged). Mixed recall is therefore reported only on synthetic items and labelled as such.
- Novel-scheme slice: 34 real scam items whose scheme is not in the synthetic generation taxonomy (8 held out by design: meter replacement/biometrics, eGov signature renewal; 26 naturally absent, e.g. voice "yes" capture, vote-link account takeover, fake census).
- Training-data decisions: dokster labels mapped dangerous -> scam, safe and needs_check -> legit, suspicious dropped, government_impersonation dropped (held-out scheme overlap). FraudLens anti-fraud posts are used as LEGIT hard negatives (they describe scams; they are not scams). anti_spam_ru (machine-translated email spam) is used only for the B2 "generic team" baseline. Telegram-spam label 1 (job and "easy income" offers) counts as scam.

### A2. 2026-11-14 16:35 UTC+5 (AFTER baselines B0-B5 were scored on real-test; triggered by council round 1)
Written after baseline numbers were seen. No trained encoder had been scored on real-test at this point.
- Bugs found by council and fixed: (a) official kk/ru translations of the same text sat on both sides of the dev/test split (different publishers, so URL grouping missed them). Fix: LaBSE mutual-best cross-lingual matches at cosine >= 0.85 are linked as pairs, any two items at cosine >= 0.90 share a group, split re-done stratified by language (build_real.py). 22 kk/ru pairs (13 scam, 9 legit). (b) Training shortcuts: link/placeholder tokens only on scam rows, markdown in translated warnings, reassurance lines only in legit synthetic calls. Fix: all URL forms -> "<url>", markdown stripped, 12 reassurance legit rows dropped, 740 real chat lines with links added as legit, 20% of legit synthetic SMS/messenger rows get a link. (c) NLLB-translated dokster rows dropped (translation errors, US content). (d) LaBSE cosine leakage check (>= 0.92) added: 0 training rows dropped.
- Unit of every real item, decided from text and kind only: message, call_phrase (5+ words), fragment (<= 4 words, often not judgeable without the call), description (third-person scheme description; removed from scam metrics), advice_text (official anti-fraud advice), notification (real legit SMS). Headline scams = message + call_phrase (real-dev 30, real-test 68).
- Headline metric changed: threshold at <= 1% FPR on everyday-chat dev only; recall on headline scams; FPR on everyday-chat test; PR-AUC of headline scams vs chat test (prevalence about 3%). The old PR-AUC over real items (66% scam) is dropped because it starts at 0.66 by chance and rewards text length. Advice-text flag rate is a stress test, not a user-facing FPR. Intervals: Wilson + cluster bootstrap over source groups; paired results use exact McNemar.
- Length-only baseline added (BL). Under the new headline it scores 0 recall, so the length shortcut no longer drives the headline.
- Known limitation: the chat pools drop lines with links, numbered lists and bot leaderboards, so chat FPR is optimistic for texts with links.

Status of the pre-registered predictions (honest scoring):
- P1 (keyword rule precision >= 0.9, recall < 0.6, lowest on kbd): FALSIFIED. Recall 0.37 < 0.6 holds, but precision on the original real set was about 0.65, and kbd cannot be lowest because the rule folds keyboard-Kazakh before matching (0.28 both).
- P2 (generic spam model: kk recall >= 20 points below ru): FALSIFIED narrowly. kk 0.00 vs ru 0.18 (18 points).
- P3 restated (mixed has n=1 in real-test): the fine-tuned encoder beats B3 on PR-AUC vs chat, and its gain is largest on keyboard-folded Kazakh. Tested on the frozen model only.
- P4 for TF-IDF: NOT SUPPORTED. Without augmentation B3 already scores 0.64 on folded Kazakh (vs 0.59 original); augmentation did not help (headline 0.53 vs 0.56). Caveat: augmentation and the test perturbation use the same letter mapping, so this test is weak. Encoder ablation only if time allows.
- P5 (unseen-scheme recall 10+ points lower): pending the frozen model (baselines: B3 0.20 vs 0.59, B5 0.40 vs 0.50).

### A3. 2026-11-14 18:45 UTC+5 (after council round 1 and the user's request for >= 90% recall; no trained encoder scored on real-test yet)
- Real set extended with round-2 collection (kk2: 283 items; ru2: 251 items, finished 18:50 before any model was evaluated on this split, so all are included). Note: 75 of ru2's 84 legit items are real bank SMS/push formats from the public GitHub collection zenmoney/sms-formats (not a bank page; dates are commit dates). Re-split with the A2 rules (LaBSE pair/near-duplicate grouping, language-stratified 30% dev). Split counts: see build_real.py output logged in council/round2_brief.md. Baselines are re-scored on this split.
- Disclosure: the v2 call-phrase generation prompts (data/synthetic/GENERATION_PROTOCOL_v2.md, groups G5-G7) were written after the round-1 real set's scheme NAMES had been seen (e.g. voice "yes" capture, SIM expiry, vote-link account takeover). No real texts were shown to the generators, but those schemes are no longer "unseen". The novel-scheme slice is redefined as schemes absent from all G1-G7 prompts (71 scam items; headline dev 17, test 21). Truly held out by design, excluded from every generator: meter replacement / biometrics and eGov signature (ЭЦП) renewal (22 items; headline dev 2, test 6).
- Training data added: 2,850 synthetic call phrases (G5-G7, protocol v2), ~30k extra real everyday chat lines (disjoint from the chat test pool), 46,697 rows from open Hugging Face scam/legit corpora (licences and label decisions in data/processed/hf_extra_report.md), 6,000 of those translated to Kazakh with NLLB-200 1.3B.
- Target set by the user: >= 90% recall on both Kazakh and Russian real scams. Reported at the pre-registered operating point (<= 1% FPR on everyday chat) and, separately labelled, at the "suspicious" operating point (<= 5% FPR). Model selection uses real-dev only; real-test is scored once per frozen candidate and every scoring is logged in RUNS.md.

### A4. 2026-11-14 21:10 UTC+5 (no trained encoder scored on real-test yet)
- Finding on real-dev: at "<=1% FPR on everyday chat" the best models (e5-large, Horizon fine-tune) set thresholds near 0.003 and flag real bank SMS/push notifications (OTP codes, transfers, top-ups) at 0.9+. Chat FPR alone hides the false alarms a user would actually see.
- Operating point changed (A4): threshold = the stricter of (a) <= 1% FPR on everyday-chat dev and (b) <= 5% FPR on real-dev legit notifications (45 items). Notification FPR is now reported on real-test (69 items) next to chat FPR. Under A4 the v5b models drop to 0.28-0.41 dev recall.
- Fix: rule-based generator of legit service notifications (pipeline/src/gen_notifications.py; bank OTP/transactions incl. transliterated Latin and "<#>" retriever codes, eGov codes, delivery, telecom, civil-defence alerts) in ru/kk/translit/mixed. Disclosure: templates were written after inspecting real-DEV false alarms (real-test notifications never opened). The leakage filter dropped 171 generated rows as near-copies of real items. The zenmoney/sms-formats collection has no licence, so it is used only for the 75 evaluation items, never for training.
- Blind annotation (data/processed/real_selfcontained.jsonl): an independent agent with no access to model outputs tagged every real scam item as recognizable from text alone (yes / maybe / no). Headline scams: real-dev yes 61, maybe 32, no 21; real-test yes 125, maybe 91, no 38. Results are reported on all headline scams and on the self-contained subset (yes + maybe); "no" items are reported separately as a ceiling on what any text-only model can do.

### A4b. 2026-11-14 21:05 UTC+5 (council round 2; no trained encoder scored on real-test yet)
- Normalization: official bank/government/operator domains map to "<url_official>" (lookalikes such as bonus-kaspi.kz or kaspi.kz.secure-login.com stay "<url>"). The real set was re-normalized with its split, groups and pairs locked by id (data/processed/split_lock.json); headline counts unchanged.
- Training mix v6b: notifications regenerated (more Kazakh templates, stacked kk/ru bilingual, hotline numbers and official links on 26% of rows), 2,500 scam twins in the same formats (pipeline/src/gen_notifications.py, built from the scheme list), Telegram job spam capped at 400, GBP prize SMS dropped, NLLB Kazakh rows halved. 147 rows dropped as near-copies of real items.
- Epoch/checkpoint selection: average precision of real-dev headline scams against chat-dev + real-dev notifications (threshold-free). The A4 threshold rule itself is unchanged.
- Blind tag reliability: second annotator, 80 items, kappa 0.76 (3-class), 0.73 (self-contained vs not). The first annotator's tags are used, frozen.
- Freeze: Sun 15 Nov 10:00 UTC+5. Before unsealing real-test, RUNS.md records the frozen threshold, weights and the number of dev configurations tried.

### A5. 2026-11-14 23:40 UTC+5 (final-model selection rule, written before the last training round finished)
- Candidates: every single run and ensemble trained on mix v6c (including the 3-epoch seeds now training).
- Rule: pick the highest real-dev average precision of headline scams against chat-dev + real-dev notifications (threshold-free). If two candidates are within 0.005, pick the one with fewer models. Ensembles are mean z-scored logits ("logit_z") or mean chat-percentiles ("pct"), as implemented in pipeline/src/ensemble.py.
- Then freeze (record members, threshold, checkpoint hashes, and the number of dev configurations tried in RUNS.md), and score real-test exactly once with finalize.py.

## Results (frozen 2026-11-15 03:20 UTC+5; real-test scored once; full numbers in runs/ens_v6c_e5s2s3_logit_z/final_report.json and RUNS.md)
Frozen model: mean z-scored logits of two multilingual-e5-large fine-tunes (seeds 2, 3; 2 epochs) on mix v6c. A4 threshold from dev.
- Headline recall 80.7% [75, 85] (205/254); Kazakh 83.6% [77, 89]; Russian 76.9% [68, 84]. Target >= 90% on both languages: NOT met.
- Self-contained subset (blind tags, kappa 0.76): 89.4% [85, 93]; Kazakh 89.9%; Russian 88.5%. "Yes"-tagged: 96.8%. "No"-tagged: 31.6%.
- False alarms: everyday chat 0.30% (6/1978); real bank notifications 14.5% [8, 25] (10/69), above the 5% dev target (dev 2/45). The threshold rests on 45 dev notifications and templates informed by dev errors; it did not transfer.
- Same rule, baselines: keyword rule 27.2% (natural setting, same 14.5% notification FPR), off-the-shelf scam model 30.3%, TF-IDF on our data 43.7%, generic spam model 4.7% (Kazakh 0%).
Pre-registered predictions, final status: P1 falsified; P2 falsified (narrowly); P3 (encoder beats TF-IDF on PR-AUC vs chat, biggest gain on keyboard-Kazakh): first part supported (0.960 vs 0.838), second part falsified (gain is larger on standard Kazakh than on keyboard-folded); P4 inconclusive (encoder still loses 10 points on keyboard-folded Kazakh, p = 0.0015; TF-IDF ablation mixed); P5 supported (unseen schemes 68.8% vs seen 82.4%).

### A6. 2026-11-15 11:15 UTC+5: second model (v2) protocol, written before any v2 data or training
- Test set A (the 575 items scored once for v1) is spent. It moves into TRAINING for v2: headline scams, self-contained fragments, legit notifications and advice texts (descriptions dropped), real rows upweighted x4. v1's reported result stays as it is.
- Dev stays the same 225 items (selection and A4 threshold, unchanged rule).
- Test set B: new real items collected from pages not used in rounds 1-2, frozen before any v2 model is scored on it. Items that are near-copies (LaBSE >= 0.90 or char-5gram Jaccard >= 0.5) of any training row or dev item are dropped at build time, blind to model scores. If the user provides their own bank/eGov SMS (with consent, anonymised), they are split 50/50 into threshold calibration (added to dev notifications) and test B.
- Candidates: e5-large fine-tunes on the v2 mix (same recipe, seeds 1-3), single and logit_z ensembles. Selection rule A5 on dev. v2 replaces v1 as the reported headline model only if its dev AP (vs chat + notifications) is higher than v1's; otherwise v1 stays. This is decided before test B is scored.
- Test B is scored once for the frozen v2 AND for the frozen v1 (fair before/after). Both test A (v1) and test B (v1, v2) results are reported.
- Hard freeze: Sun 16:00 UTC+5.

## Results v2 (A6; frozen 2026-11-15 12:32 UTC+5; test B scored once for v1 and v2; runs/*/final_report_testB.json)
Frozen v2: mean z-scored logits of four multilingual-e5-large fine-tunes (seeds 1-4, 2 epochs) on mix v7 (v6c + the spent test-A items as training, weight x4). Dev AP vs chat + notifications 0.978 (v1 0.962), so v2 replaced v1 under the A6 rule.
Test B: 195 real items from 127 pages never used before (129 headline scams: Kazakh 93, Russian 31, mixed 5; only 2 real service SMS, so SMS false alarms cannot be measured on test B).
- v2: recall 82.2% [75, 88] (106/129); Kazakh 87.1% [79, 92]; Russian 64.5% [47, 79] (20/31); chat FPR 0.05% (1/1978); anti-fraud advice flagged 8.1%; recognizable-from-text subset 88.4% (Kazakh 90.2%, Russian 80%); keyboard-folded Kazakh 76.3% vs 87.1% (p = 0.03).
- v1 on the same test B: recall 71.3% [63, 78]; Kazakh 72.0%; Russian 64.5%; chat FPR 0.30%; advice flagged 18.9%.
- Paired on the 129 scams: v2 caught 16 that v1 missed, v1 caught 2 that v2 missed (McNemar p = 0.0013).
- The novel-scheme slice is not reported for test B (its scheme names were not mapped to the training taxonomy).

- Disclosure (found after the v2 freeze): the 43 zenmoney/sms-formats notifications in test A (collection states no licence; earlier rule: evaluation only) were included in v2's training when test A moved into training. Not retrained, to avoid a second look at test B. The training mix is not published.

A6 deviations (found in council round 4, disclosed, nothing re-scored):
- A6 named seeds 1-3; four seeds (1-4) were trained, all launched together before any v2 result existed, and the A5 rule picked the 4-seed ensemble.
- build_testB.py ran the char-5gram Jaccard check against dev only, not against training. 5 test-B items exceed 0.5 against training (2 headline scams, both caught by both models). Excluding them: v2 81.9%, v1 70.9%, Russian 63%.
- The everyday-chat negatives (1,978) are the same pool used for test A, so the chat false-alarm rate is not fresh.
- v1 was re-scored on Kaggle in fp16 for test B; its dev threshold was re-derived (0.99994270 vs 0.99994208 frozen) with no change in any decision.
- Test B's 37 "advice_text" legit items are mostly real Otbasy Bank service notices (build_testB labels every legit web text advice_text); the README reports them as real bank/eGov notices.
