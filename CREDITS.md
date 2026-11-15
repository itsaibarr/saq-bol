# Credits

Everything used in this project, with licences as stated by each source on 2026-11-14.

## Evaluation data
- **Test set C (version 3's test):** 306 texts copied word for word from 204 pages not used before: Kazakhstan news, police, bank, ЕНПФ/eGov pages and official Telegram channels (`data/real_test/ru4_sources.md`, `ru4b_sources.md`, `kk4_sources.md`), plus a Russian set from publishers in Russia, Belarus, Kyrgyzstan, Uzbekistan and Moldova that are never used in training (`rucis_sources.md`). Items in `data/processed/testC.jsonl`.
- **Test set B (version 2's test, then version 3's training):** 195 texts copied word for word from Kazakhstan pages not used before; sources in `data/real_test/kk3_sources.md` and `ru3_sources.md`, items in `data/processed/testB.jsonl`.
- **Real Kazakhstan set A:** 800 texts (578 scam, 222 legit) copied word for word from 389 public pages: banks (Kaspi, Halyk, BCC, Otbasy, Freedom and others), ARDFM, the National Bank, police and prosecutors, eGov, Kazpost, and Kazakh and Russian news outlets. Every item keeps its URL, publisher and date in `data/processed/real_all.jsonl`; collection logs are in `data/real_test/*_sources.md`. Short quotations are used for research evaluation. The 575 test-A texts were used once to score version 1 and then moved into version 2's training; the 225 dev texts were never trained on.
- **Real bank SMS formats:** 75 legit notification texts from the public GitHub collection zenmoney/sms-formats (no licence stated): https://github.com/zenmoney/sms-formats. 32 sit in dev and were never trained on. The other 43 were in test A, and when test A moved into version 2's training they went with it. We had intended to keep this collection evaluation-only and noticed the slip after version 2 was frozen; we did not retrain, because that would have meant scoring test B twice. The texts are short machine-generated bank notification formats; the training mix is not published.
- **Everyday chat:** held-out lines from Telegram Corpus KAZ_RU, kurumikz (CC BY-NC-SA 4.0): https://huggingface.co/datasets/kurumikz/telegram-corpus-russian-kazakh

## Training data
Hugging Face corpora (label decisions per dataset in `data/processed/hf_extra_report.md`):
- rasheq/scam-shield-sms (CC BY 4.0), VusalShahbazovAz/smishing-AZ-SC (CC BY 4.0), Ridham115/indian-scam-sms-synthetic-audited (CC BY 4.0)
- anmolshrivastav/scam_ham_india_14_languages (MIT)
- DmitryKRX/anti_spam_ru (Apache-2.0; social-engineering spam kept as scam, advertising spam dropped, also used for baseline B2)
- FredZhang7/all-scam-spam, flowxai/scamguardbench, Bektemir96az96/Uzbek_and_Russian_Phishing_dataset, ysangam/Indian_Cyber_Scam_PhoneCall_Hinglish_Dataset (Apache-2.0)
- BothBosu/scam-dialogue, single-agent-scam-conversations, multi-agent-scam-conversation, Scammer-Conversation, youtube-scam-conversations (Apache-2.0; caller turns only)
- shaw/scambench-training (CC BY-SA 4.0)
- dbarbedillo/SMS_Spam_Multilingual_Collection_Dataset (GPL)
- dokster/adaption-scam-dataset-ru-en-v1 (Apache-2.0)
- alt-gnome/telegram-spam (CC0)
- Abdurohman/fraudlens-ru-v1 (CC BY 4.0; anti-fraud posts used as legit hard negatives)
- kurumikz/telegram-corpus-russian-kazakh (CC BY-NC-SA 4.0; training lines disjoint from the evaluation lines)

Other training data:
- 989 real Russian-language scam texts quoted by non-Kazakhstan sources: 338 in batch 1 (T-J/journal.tinkoff.ru, Belarusian, Uzbek and Ukrainian banks; `data/train_extra/ru_rf_sources.md`) and 651 in batch 2 for version 3 (T-J, KP, AiF, Habr, Lenta, RIA, Lifehacker, Kaspersky and others; `data/train_extra/ru_rf2_sources.md`). Some batch-2 rows are Russian versions of US scam examples as published by the source.
- About 2,600 Kazakh machine translations of the corpora above, made with NLLB-200 1.3B.
- 6,050 synthetic Kazakhstan-specific messages and call phrases (Kazakh, Russian, mixed, keyboard-Kazakh) generated with Claude under the protocols in `data/synthetic/`, never shown the evaluation data; the last 1,200 (G8, protocol v3) are 60% Russian.
- About 5,100 rule-based legit service notifications and 2,200 scam "twins" (`pipeline/src/gen_notifications.py`).

## Pretrained models
- intfloat/multilingual-e5-large (MIT): version 1 (two fine-tuned copies), version 2 (four) and the final version 3 (one); version 3's weights are published at https://huggingface.co/itsaibarr/saq-bol-v3 (CC BY-NC-SA 4.0, because of the non-commercial training data) https://huggingface.co/intfloat/multilingual-e5-large
- FacebookAI/xlm-roberta-base and xlm-roberta-large (MIT), kz-transformers/kaz-roberta-conversational (Apache-2.0): compared, not used in the final model
- Horizon-Labs/phishing-scam-detector-base (Apache-2.0): baseline B5 ("existing multilingual scam model", scored as is on tests A and C) and a compared fine-tune https://huggingface.co/Horizon-Labs/phishing-scam-detector-base
- facebook/nllb-200-distilled-1.3B and -600M (CC BY-NC 4.0): Russian/English to Kazakh translation for training data
- sentence-transformers/LaBSE (Apache-2.0): translation-pair linking and leakage checks

## Libraries, compute and tools
PyTorch, Hugging Face Transformers, sentence-transformers, scikit-learn, pandas, SciPy, matplotlib, Gradio, nbformat. Training on Kaggle (free T4 GPUs) through the Kaggle CLI.

## AI assistants
- Claude Code (Anthropic, Claude Opus 5.5): research, coding, synthetic data generation, data collection agents, and three-reviewer "council" critiques of the design and results. All numbers come from the code in this repository.

## Related work
- Ordalinnn/AI-Fraud-Detector, a kk/ru/en fraud-message detector by a Kazakhstan school team (all rights reserved; not used, cited for context): https://github.com/Ordalinnn/AI-Fraud-Detector
