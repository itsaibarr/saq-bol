# 40 — AI + Languages research (Kazakh-first, with a Languages × Finance angle)

Research date: 2026-11-14. Updated mid-task after the user's note: they live in **Astana**, are fluent in Kazakh, Russian and English (so they can do the real-speaker check), and care most about **Languages and Finance**.

How sources are marked:
- **[F]** I opened the page (or ran the API or file) myself.
- **[S]** The figure comes only from a search-result summary. Open the source before quoting it to judges.
- **[OWN]** I computed it myself in this session (method given).

---

## 0. Bottom line

1. **Recommended project: C1 "Сақ бол", a screener for scam SMS, messenger messages and calls in Kazakh, Russian and code-switched Kazakh-Russian, built for an Astana pensioner. Submit it under the Finance track.**
   - Its central idea is a **language-fairness audit**: does a fraud filter protect Kazakh-speakers and people who type "keyboard Kazakh" as well as it protects Russian-speakers?
   - Its language component is the Kazakh-letter normaliser from C3. Voice (C2) is an optional extra.
   - It covers everything Finance judges check: precision and recall, a fair rule baseline, a time-based split by when each scam scheme appeared, fairness across groups, and explanations.
   - It also gives the Languages-style evidence (results per language, side-by-side outputs, a real speaker).
2. **Lowest-risk fallback: C3 "Қ, not К" (Languages track).** It restores Kazakh-specific letters in text typed on Russian keyboards and measures the knock-on effect on translation, LLM answers and scam detection. Data is plentiful, nobody has built it yet (I found no tool on HF), and it is very feasible.
3. **Most technical Languages-track option: C2.** Speech recognition for code-switched "shala-qazaq" speech, with error rates reported separately for Kazakh words and Russian words.

---

## 1. Where language AI works and fails for low-resource languages (2025–2026), with numbers

### 1.1 Speech recognition (ASR)

| Fact | Number | Source |
|---|---|---|
| Whisper on FLEURS Kazakh (WER %) | tiny 165.2 · base 109.2 · small 70.3 · medium 48.8 · large 43.8 · large-v2 **37.7** | Radford et al., *Whisper* paper, Table 13 (arXiv 2212.04356, 2022) [F] https://ar5iv.labs.arxiv.org/html/2212.04356 |
| Whisper Kazakh→English speech translation (BLEU) | large-v2 **5.4** | same paper, Table 14 [F] |
| Same paper, same baseline, three languages | OpenAI Whisper baseline WER: **Kazakh 21.55%** vs English 5.15% vs Russian 5.89%; ISSAI fine-tune `issai/whisper-turbo` reaches 8.84% on Kazakh | ISSAI et al., "Multilingual ASR Interface for Typing…", Astana IT Univ. journal, DOI 10.37943/24AHNP6638 (2025) [S] https://journal.astanait.edu.kz/index.php/ojs/article/view/897 |
| Model card benchmark on FLEURS kk (WER/CER) | Whisper-small 70.45/21.23 · medium 48.69 · large-v3 31.10 · large-v3-turbo 19.75 · XLSR Kazakh 21.75 · **Kazakh fine-tuned turbo 11.80/4.98** | `shyngys879/kazakh-whisper-large-v3-turbo` card (self-reported, Apache-2.0, ~1,500 h training) [F] https://huggingface.co/shyngys879/kazakh-whisper-large-v3-turbo |
| Real broadcast and parliament speech (KSC2) is much harder | Whisper large-v3-turbo zero-shot **81.2% WER** on KSC2, 39.3% after song-data fine-tuning | Yeshpanov, "Using Songs to Improve Kazakh ASR", LREC 2026 (arXiv 2603.00961, Mar 2026) [F] https://arxiv.org/abs/2603.00961 |
| **Code-switched Kazakh-Russian speech**: first public benchmark (31 clips, 3.7 min, CC BY YouTube) | WER: fine-tuned Kazakh Whisper 11.9% · Yandex SpeechKit 17.1% · Gemini 2.5 Flash 29.5% · **Whisper large-v3 42.5%** · **Google Cloud STT 64.9%**. The repo adds that Russian insertions push WER up for every system except Yandex; the fine-tuned model goes from 8.4% to 18.2% on clips with insertions. | `Tim2190/kazakh-codeswitch-asr` (created 2026-07-27, CC BY 4.0) [F] https://huggingface.co/datasets/Tim2190/kazakh-codeswitch-asr · https://github.com/Tim2190/Kaz-ASR-codeswitch-benchmark |
| How common code-switching is in real Kazakh speech | **About 10% of words** in Kazakh call-centre speech are Russian code-switches. A Kazakh-only model's WER on the Russian words is **59.53%**, and bilingual training improves that by 14.69 points. | Ubskii, Matveev, Minker, CEUR-WS Vol-2590 (2019/2020) [F] https://ceur-ws.org/Vol-2590/short13.pdf |
| Meta Omnilingual ASR (Nov 2025), 7B LLM-ASR, per-language CER on Meta's own eval sets | kaz_Cyrl **2.6** (407 h) · kaa_Cyrl (Karakalpak) 2.6 (18.6 h) · uig_Cyrl 2.2 (24.8 h) · uig_Arab 1.4 · kir 2.6 · rus 1.5. No Dungan row. | `per_language_results_table_7B_llm_asr.csv` [F] https://github.com/facebookresearch/omnilingual-asr |
| Omnilingual ASR headline | CER below 10 for 78% of 1,600+ languages, but only **36%** of languages with less than 10 h of training data reach that | Meta blog, 2025-11-10 [S] https://ai.meta.com/blog/omnilingual-asr-advancing-automatic-speech-recognition/ ; the-decoder [S] |
| MMS vs Whisper, average over 54 FLEURS languages | MMS 33.3 WER (no LM) / 20.7 (with LM) vs Whisper large-v2 44.3 | Pratap et al. 2023, arXiv 2305.13516 [S] |

What this means:
- Clean, read Kazakh is close to solved once a model is fine-tuned (FLEURS WER about 9–12%).
- Kazakh as it is actually spoken is not: broadcast speech (81% WER zero-shot), Russian insertions (Whisper 42.5%, Google 64.9%), dialects (I found no labelled corpus) and elderly speakers (no corpus).
- A low CER can hide a high WER, because Kazakh is agglutinative (one wrong suffix makes the whole word wrong).

### 1.2 Machine translation (MT)

| Fact | Number | Source |
|---|---|---|
| FLORES, chrF (BLEU) | RU→KK: NLLB base 0.49 (0.08) · Tilmash 0.54 (0.13) · Google 0.54 (0.13). EN→KK: NLLB 0.49 · Tilmash 0.60 · Google 0.60. KK→EN: Google 0.65 (0.36). | KazParC paper, LREC-COLING 2024, Table 6 [F] https://arxiv.org/html/2403.19399v3 |
| **Colloquial code-switched Kazakh→Russian (KRCS, 618 social-media sentences)** | chrF++: NLLB-600M 36.67 · NLLB-3.3B 39.68 (42.27 fine-tuned) · Yandex 47.13 · Google 47.84. Human rating out of 5: Google 3.49, NLLB 3.09, Yandex 2.80; reference translations 4.75. | Borisov, Kozhirbayev, Malykh, arXiv 2503.20007 (Mar 2025) [F] https://arxiv.org/html/2503.20007v1 |

What this means: even the best commercial MT is mediocre on informal, mixed text, and that is the register people actually write in.

### 1.3 LLMs

| Fact | Number | Source |
|---|---|---|
| Same 4B model, same MMLU-Pro questions (machine-translated) | **Kazakh 40.62 · Russian 47.42 · English 58.09** (Qolda No-Think). The 34B variant scores kk 73.67 / ru 76.34 / en 79.00. | `issai/Qolda` model card (2025-11 / 2026-08) [F] https://huggingface.co/issai/Qolda |
| KazMMLU (23k questions; 10,969 Kazakh, 12,031 Russian), zero-shot overall | GPT-4o 76.6 · DeepSeek V3 76.9 with an English prompt but **45.5 with a Kazakh prompt** · Llama-3.1-8B 39.7 · Qwen-2.5-7B 42.5 · Sherkala-8B 45.6. Models generally do slightly better in Russian than in Kazakh. | KazMMLU paper (MBZUAI), arXiv 2502.12829 v2 (Jul 2025) [F] https://arxiv.org/html/2502.12829v2 ; data https://huggingface.co/datasets/MBZUAI/KazMMLU (CC BY-NC 4.0, not gated) [F] |
| Kazakh LLMs available now | ISSAI KAZ-LLM 8B/70B (Llama-3.1, Dec 2024, CC BY-NC, gated) [F card] · Sherkala-8B-Chat (Llama-3.1, 45.3B-token continued pretraining, COLM 2025) [S] · **issai/Qwen3.5-4B/9B/35B-A3B-Kazakh** (Aug 2026, Apache-2.0, +16K Kazakh tokens) [F] · issai/Qolda 4B VLM (Apache-2.0) [F] | https://huggingface.co/issai |

### 1.4 Global picture

- Stanford HAI, "Mind the (Language) Gap" (white paper, 2025-04-22): most major LLMs underperform on low-resource languages, mainly because data is scarce and poor in quality. [S] https://hai.stanford.edu/policy/mind-the-language-gap-mapping-the-challenges-of-llm-development-in-low-resource-language-contexts
- Data-access change: since October 2025, Common Voice is distributed only through the Mozilla Data Collective (an account and new terms are required, and older versions are withdrawn). Teams following the brief's "Common Voice on HF" instruction may get stuck. [S] https://huggingface.co/datasets/mozilla-foundation/common_voice_17_0 · https://discourse.mozilla.org/t/common-voice-dataset-segments-now-available-on-mdc/149060

---

## 2. Problem size: statistics and news

### 2.1 The Kazakh language

| Stat | Source |
|---|---|
| 2021 census: about 80% of residents aged 5+ (over 13 million) speak Kazakh, and almost half of them use it daily. Among citizens of Slavic origin, only **22–25% understand spoken Kazakh** and 2.9% read and write it professionally. Uyghurs 71.7% and Uzbeks 72% have good spoken command. | Astana Times, 2023-04-16 (draft state language-policy concept) [F] https://astanatimes.com/2023/04/kazakhstan-prepares-new-document-to-boost-development-and-prevalence-of-kazakh-language/ |
| Policy targets for 2029: 84% Kazakh-speaking; 94% of state record-keeping in Kazakh | same [F] |
| **71% of schoolchildren** were enrolled in Kazakh-medium classes this year; 70% of 6,000+ books published last year were in Kazakh (Tokayev, Qazaq tili Kurultai) | Zakon.kz, **2026-11-10** [F] https://www.zakon.kz/obshestvo/6538137-bolee-70-pervoklassnikov-v-etom-godu-poshli-v-klassy-s-kazakhskim-yazykom-obucheniya--prezident.html |
| UNT 2025 (main session, over 210k test-takers): **about 76.5% took it in Kazakh**, 23.5% in Russian | Ministry of Science and Higher Education via Kazinform and gov.kz [S] https://www.gov.kz/memleket/entities/sci/press/news/details/1026598?lang=ru |
| Astana city schools: 58% → 62% → 65% of pupils in Kazakh classes (2022–2024). **1,500–2,000 Astana adults a year** take free Kazakh courses, about 40% of them from other ethnic groups. | Bizmedia, 2024-09-16 [F] https://bizmedia.kz/2024-09-16-vse-bolshe-zhitelej-astany-izuchayut-kazahskij-yazyk/ |
| Tokayev said KazLLM "is not yet in expected demand" and that people prefer ChatGPT. The ministry reports **KazLLM 600k+ users**, ChatGPT used by **about 13%** of residents, and KazLLM + ALEM LLM running in 40+ services including eGov AI. | Bizmedia, 2026-02-10 [F] https://bizmedia.kz/2026-02-10-tokaev-kritikuet-kazllm-pochemu-kazahstanczy-vybirayut-chatgpt/ |
| eOtinish (citizen appeals): AI has processed **2.8 million complaints** (summary, tags, draft reply) since 2025. The ministry says **no accuracy or error statistics exist**, and staff rated only about 0.25% of cases. | BES.media, 2026-10-16 [F] https://bes.media/news/ii-obrabotal-2-8-mln-zhalob-kazahstantsev-cherez-eotinish-no-nikto-ne-znaet-skolko-raz-on-oshibsya/ |
| eGov GPT: 50 state services available by correspondence (Aug 2026) | Bizmedia, 2026-08-26 [S] https://bizmedia.kz/2026-08-26-kazahstanczy-mogut-poluchit-gosuslugi-cherez-egov-gpt-bez-poseshheniya-czona/ |
| Script: the Latin transition is phased over 2023–2031, and Kazakh is **still mainly written in Cyrillic** | Astana Times, 2021-02 and 2026-04 [S] https://astanatimes.com/2021/02/kazakhstan-presents-new-latin-alphabet-plans-gradual-transition-through-2031/ |
| **[OWN]** In a public Telegram kk/ru corpus (1.49M lines), **26.2%** of occurrences of 13 common Kazakh words are typed with Russian look-alike letters (n=1,300). Per word: ғой→гой 49%, қайда→кайда 40%, жақсы→жаксы 39%, жоқ→жок 25%. | Method: exact-token counts of the correct form vs Russian-letter variants; words that are also Russian words were excluded; script at scratchpad `count_sub.py`. Corpus: https://huggingface.co/datasets/kurumikz/telegram-corpus-russian-kazakh (CC BY-NC-SA 4.0). This is a rough estimate from one corpus, mostly Russian chats. |
| KazSAnDRA (180,064 Kazakh reviews) lists five written forms of Kazakh, including **Cyrillic text with Russian letters in place of Kazakh ones** (e.g. "кп" for "көп"). The authors leave spelling and code-switching unhandled and suspect they weaken their models. | Yeshpanov & Varol, LREC-COLING 2024 [F] https://arxiv.org/html/2403.19335v2 |
| User comments on Kazakhstani news sites: 63% Kazakh, 34.4% Russian, the rest mixed; homoglyphs and mixed scripts were common enough to need a normalisation step | Myrzakhmetov et al., IEEE AICT 2018 [S] https://nur.nu.edu.kz/handle/123456789/3749 |

### 2.2 Money and fraud (the Languages × Finance angle)

| Stat | Source |
|---|---|
| Jan–Jul 2026: **13.1k internet-fraud cases**, 19.5% of all registered crime and 57% of all fraud. **Astana has the most cases: 2.3k.** Largest category: **fake SMS and calls "from banks", 2.9k**; then phishing 2.7k, service ads 2.6k, online purchases 1.9k, online loans 1.3k, pyramids 770. | Finratings (citing Finprom), **2026-08-22** [F] https://finratings.kz/news/16274-nazvan-gorod-kazakhstana-s-naibolshim-chislom-internet-moshennichestv/ |
| **84.5 million fraudulent calls blocked** in 2025; 13 call centres shut down (Interior Minister) | Times of Central Asia, 2026-01-12 [F] https://timesca.com/kazakhstan-blocks-nearly-85-million-fraudulent-phone-calls-in-2025/ |
| H1 2025: online fraud up 25% (9,936 → 12,390 cases) while total fraud fell 0.7% | Astana Times, 2025-07-21 [F] https://astanatimes.com/2025/07/online-fraud-surges-despite-overall-decline-in-cases/ |
| 2025: 26.3k internet-fraud cases (+86.1%); H1 2025 losses over 25bn tenge | npck.kz anti-fraud forum [S] https://npck.kz/?p=36791 |
| Typical 2026 schemes: calls "from Kaspi/Halyk/Freedom" about a loan being taken in your name, then a request for the SMS code or a transfer to a "safe account"; fake KNB and National Bank staff; fake Kazpost; AI voice cloning of relatives. An **Astana pensioner lost about 18 million tenge** after a "Kazakhtelecom → KNB" call. | Zakon.kz (Sep 2026) [S] https://www.zakon.kz/proisshestviia/6533160-zvonok-ot-kazakhtelekoma-i-knb-astanchanka-stala-zhertvoy-i-kurerom-moshennikov-otdav-im-18-mln.html ; Finance.kz [S] |
| Official red-flag lists are published **in Kazakh** (gov.kz ARDFM page, 2025-07-03): read-out SMS code, CVV, WhatsApp call "from Kazpost", links from unknown senders | [F] https://www.gov.kz/memleket/entities/ardfm/press/news/details/1029204?lang=kk |
| No public Kazakh or Russian scam-message corpus exists. The only Kazakh spam work uses small, self-collected sets (one with 200 samples), and its authors say annotated Kazakh spam data is lacking. | SDU Bulletin [S] https://repository.sdu.edu.kz/handle/123456789/1556 ; HF API search for kazakh/russian scam or spam returned 0 datasets [F] |
| Household debt: 27.5 trillion tenge owed by **8.95M borrowers** on **39.4M loans** (4.4 per borrower) as of 2026-01-01 | Bizmedia, 2026-06-11 [F] https://bizmedia.kz/2026-06-11-275-trln-tenge-dolzhny-kreditoram-zayomshhiki-v-kazahstane/ |
| Loans more than 90 days overdue: 1.177 trillion tenge (2026-04-01), up from 386bn in 2021. Over **51k people declared bankrupt** in 2025. Debt passed to collectors reached 1.1 trillion tenge (+37.2% y/y, Mar 2026). | Tengrinews and BES.media via search [S] |
| General financial-literacy index **41.5%** (2025); 69.2% have no personal savings (NBK, Apr 2024) | [S] finratings.kz/news/10182… ; daryo.uz 2024-05-14 |

---

## 3. Generic projects other teams will likely build (avoid these)

1. Tatoeba language identification with TF-IDF and logistic regression, plus "a language I speak". Kazakh vs Kyrgyz will be the usual twist.
2. NLLB-600M on FLORES with chrF for English→French vs one low-resource language, plus a "worst 5 translations" table.
3. Whisper-small WER across Common Voice accents or two FLEURS languages. Common Voice is now behind the Mozilla Data Collective login, so expect friction.
4. Thin wrappers around ChatGPT or Gemini: a "Kazakh tutor chatbot", a "plain-language form rewriter", "street-sign OCR + translate", a "Latin↔Cyrillic Kazakh converter". The converter is rule-based, so AI is not central to it.
5. Whisper fine-tuned on FLEURS or Common Voice Kazakh. At least 8 such models are already on HF (for example shyngys879 and BuzzASR), so it is not original.
6. ASL fingerspelling with MediaPipe, relabelled as "sign language".
7. Finance-track overlap: the English SMS Spam Collection (2011) filter, with "scams in my language" bolted on. The brief itself suggests this, so expect many versions; only the depth of the execution will stand out.

What will stand out instead:
- **real, messy Kazakh** (code-switching, keyboard Kazakh, voice);
- **evaluation split by language and register**, framed as a fairness question;
- an **Astana or Kazakhstan user with dated, local evidence**;
- the team as the native-speaker check.

---

## 4. Candidate projects

Each candidate gives: user and moment · evidence · data and models · baseline · ML approach · originality · 30-hour feasibility · risks · track.

### C1. "Сақ бол": scam-message and scam-call screener for Kazakh, Russian and code-switched text, with a language-fairness audit. **Track: Finance** (also usable under Languages)

- **User and moment.** A 68-year-old in Astana who speaks Kazakh at home gets a WhatsApp voice call or SMS "from Kaspi / Halyk / Kazpost / KNB": *"Сіздің атыңызға кредит рәсімделіп жатыр, SMS-кодты айтыңызшы"*. She forwards it (or holds the phone to the laptop). The tool returns: **scam / not scam**, the red flags it found in Kazakh ("банк ешқашан SMS-кодты сұрамайды"), and what to do next.
- **Evidence.**
  - Astana is the #1 city for internet fraud (2.3k cases, Jan–Jul 2026), and bank-impersonation SMS and calls are the #1 category (2.9k).
  - 84.5M fraud calls were blocked in 2025.
  - The 2026 schemes are new (Kazakhtelecom → KNB, Kazpost, AI voice cloning), so a time-based split is meaningful.
  - No public Kazakh or Russian scam corpus exists (§2.2).
- **Data (to build in the first ~6 h).**
  - **Real scams for the test set**: verbatim messages quoted in news and official warnings (zakon.kz, finratings.kz, gov.kz ARDFM, NBK, police; gov.kz pages exist in kk and ru) and screenshots from the team's own family phones (with permission). Target 150–300 real items, each with a date and scheme label.
  - **Real legitimate messages**: own bank, eGov and Kazpost SMS and notifications (own data). Target 150–300.
  - **Training only**: LLM-generated variants in kk, ru and code-switched form, written from the dated scheme descriptions, plus synthetic noise (keyboard Kazakh, Latin translit). Never put synthetic items in the test set.
  - **Voice (stretch)**: 30–60 role-played calls recorded by the team in kk, ru and mixed, transcribed by ASR.
- **Models and tools.**
  - Classifiers: TF-IDF char 1–5-gram + logistic regression; a multilingual sentence encoder (e.g. LaBSE or multilingual-e5-small) + logistic regression; a zero-shot LLM (`issai/Qwen3.5-4B-Kazakh`, Apache-2.0 [F]; Gemini free tier).
  - ASR: `shyngys879/kazakh-whisper-large-v3-turbo` (Apache-2.0) vs `openai/whisper-large-v3-turbo` (MIT).
  - Normaliser: C3's model.
- **Baselines.**
  - (a) "Everything legitimate" (recall 0).
  - (b) **ARDFM red-flag keyword rules** in kk and ru ("SMS-код", "CVV", "қауіпсіз шот", "безопасный счёт", "AnyDesk", links…). This is the fair "simple rule" the Finance brief asks for.
- **ML plan.**
  1. Train on schemes dated up to 2025-12-31; test on 2026 schemes. This is the time-based split.
  2. Report precision and recall **separately for kk / ru / mixed / keyboard-Kazakh / Latin-translit**. That is the fairness-across-groups result.
  3. Show the recall gap, then close it with the normaliser and synthetic augmentation; report the ablation.
  4. Explanations come from the LR top features or the matched rule, mapped to a Kazakh explanation template.
  5. Compute: all CPU or a T4, under 2 GPU-hours. ASR inference on a Kaggle T4 takes minutes.
- **Originality: 4/5.** The brief suggests a scam filter, but a version that is fair across language groups, handles code-switched text and voice, is time-split by scheme, and comes with Astana evidence is far from the English SMS Spam Collection.
- **Feasibility.** Medium. Text MVP by about hour 12; voice by about hour 22.
- **Risks.**
  - Collecting the real test set is manual and slow. Cap it at 6 h, then pivot to C3.
  - Small n means wide confidence intervals; report bootstrap CIs.
  - The fairness gap may turn out small. That is still an honest result, so report it.
  - Never use real victims' recordings. Use only role-plays and public text.
  - Include the line "prototype, not financial advice".

### C2. "Shala-qazaq" ASR for code-switched Kazakh-Russian voice messages and voice bots. **Track: Languages**

- **User and moment.** An Astana resident leaves a voice message or talks to a voice assistant (bank or eGov bot) the way people actually speak: *"Мен кеше Kaspi-ге перевод жасадым, но деньги әлі түскен жоқ"*. The bot mis-hears the Russian words.
- **Evidence.**
  - About 10% of words in call-centre Kazakh are Russian, and a Kazakh-only model gets 59.5% WER on those words (Ubskii).
  - Whisper large-v3 gets 42.5% WER and Google STT 64.9% on code-switched clips (Tim2190).
  - Whisper gets 81.2% zero-shot WER on KSC2 broadcast speech.
- **Data.**
  - Test: `Tim2190/kazakh-codeswitch-asr` (31 clips, CC BY 4.0, open) [F], **plus 150–300 utterances recorded by the team** (finance and public-service phrases, two or three speakers, with consent), plus a FLEURS kk_kz control (parquet available, CC BY 4.0, not gated) [F] https://huggingface.co/datasets/google/fleurs.
  - Training: `diaslmb/KSC2` (parquet re-pack of KSC2, 406,138 utterances, 56 GB in 99 shards of ~570 MB, so a few shards can be streamed; card gives no license, original KSC2 is CC BY 4.0) [F] https://huggingface.co/datasets/diaslmb/KSC2. The official `issai/Kazakh_Speech_Corpus_2` is about 1.2k hours, not gated, and ships as 10 split `tar.gz` parts of ~80 GB [F], which is impractical in 30 h.
  - Russian side: FLEURS ru_ru.
- **Models.** Whisper large-v3-turbo (MIT), the Kazakh fine-tune above, Omnilingual ASR (check its license), `nur-dev/Qwen3-ASR-0.6B-kk-ru-en` (gated, license tag conflicts) [F].
- **Baseline.** Whisper with language=kk vs language=ru vs auto-detect.
- **ML plan.**
  1. Word-level language tags (lexicon plus char-LID) on the references, then **WER on Kazakh words vs on Russian words**. This is the per-language breakdown judges ask for.
  2. Fixes, cheapest first: (a) an initial prompt with bilingual vocabulary; (b) decode as kk and as ru, then pick per segment by language-ID or confidence; (c) LoRA fine-tune turbo or small on KSC2 shards whose transcripts contain Russian words, plus some Russian FLEURS. About 3–5 h on a Kaggle T4×2.
- **Originality: 4/5.** One 31-clip benchmark appeared in July 2026. We would extend it with an Astana finance and public-service test set, a per-word-language analysis and an actual fix.
- **Feasibility.** Medium. Fine-tuning plus evaluation fits, but it is GPU-bound.
- **Risks.**
  - GPU quota and long training. Keep a "fixes without training" path, (a) and (b) above.
  - Normalisation choices (numbers, Kazakh vs Russian spelling of loanwords) can dominate WER. Follow Tim2190's two reference layers.

### C3. "Қ, not К": restoring Kazakh letters in keyboard Kazakh, and the downstream gains. **Track: Languages**

- **User and moment.** A Kazakh speaker types on a phone without a Kazakh layout: *"кайда барасын? жаксы, коп рахмет"*. Translation apps, search, spell-check and scam filters then treat it as broken Russian. The tool restores *"қайда барасың? жақсы, көп рахмет"* before the text reaches them. The same applies to transcripts of informal speech.
- **Evidence.**
  - [OWN] 26% of occurrences of common Kazakh words in a Telegram corpus use Russian letters (49% for ғой).
  - KazSAnDRA lists this as one of five written forms of Kazakh and says it was left unhandled.
  - The 2018 NU normalisation work exists, but it is rule-based and maps text to Russian Cyrillic.
  - HF has only one related model, a spelling-error *detector* (`daniyar51/kazroberta-kazakh-spelling-detector`) [F].
- **Data.**
  - Clean Kazakh for training with synthetic corruption: the KazParC kk side (371,902 sentences, CC BY 4.0, GitHub IS2AI/KazParC; HF `issai/tilmash` is click-gated) [F]; `kurumikz/Cleaned-Kazakh-Wikipedia` (ODC-BY) [F]; `kz-transformers/multidomain-kazakh-dataset` (Apache-2.0) [F].
  - **Real test set**: 300 messages from the Telegram corpus (CC BY-NC-SA, not gated) [F] and KazSAnDRA reviews (CC BY 4.0, HF click-gated, mirror on GitHub) [F], restored by hand by the team. That is the native-speaker check.
- **Baselines.** Identity (no change), and a unigram "most frequent correct form" dictionary.
- **ML plan.**
  - Model: char-level BiLSTM tagger, or ByT5-small seq2seq (~1–2 h on a T4), or KazRoBERTa token classification.
  - Metrics: per-letter precision and recall for ә ғ қ ң ө ұ ү һ і, plus word accuracy.
  - Downstream: chrF of Tilmash or NLLB kk→ru/en on gold vs keyboard vs restored text; LLM QA accuracy; recall of C1's scam filter.
- **Originality: 5/5.** It addresses a real gap that standard benchmarks don't measure.
- **Feasibility: 5/5.** All data loads in minutes.
- **Risks.**
  - The impact story needs the downstream numbers to land.
  - Ambiguous restorations (кол → қол or көл) need context, so this makes a good failure example.

### C4. "Same question, worse money answer": Kazakh vs Russian gap of LLM finance and law answers. **Track: Languages** (alt. Finance)

- **User and moment.** An 11th-grader in a Kazakh-medium school (71% of pupils), or a Kazakh-speaking borrower, asks an AI assistant about a loan, a deposit guarantee or bankruptcy rules in Kazakh. They get a worse answer than they would in Russian.
- **Evidence.**
  - Qolda 4B on MMLU-Pro: kk 40.6 vs ru 47.4 vs en 58.1.
  - DeepSeek V3 falls to 45.5 with a Kazakh prompt (KazMMLU).
  - 76.5% of UNT takers sit it in Kazakh.
  - KazLLM has 600k users and ChatGPT reaches about 13% of residents.
- **Data.**
  - `issai/MMLU-Pro_Kazakh_Russian`: **12,032 questions paired by question_id**, same answer key [OWN check]; business 789, economics 844, law 1,101 (machine-translated, MIT) [F].
  - `MBZUAI/KazMMLU` (CC BY-NC) [F].
  - `kz-transformers/kazakh-unified-national-testing-mc` (UNT, Apache-2.0) [F].
  - A **team-written set of 50–80 Kazakhstan-specific money questions** in kk and ru (GESV/APR, KDIF deposit guarantee, out-of-court bankruptcy threshold of 1,600 MRP, collector rules), with answers taken from official pages.
- **Baseline.** The same model answering in Russian, and a translate-test route.
- **ML plan.**
  - Paired accuracy per language with a McNemar test; compare base Qwen3.5-4B, `issai/Qwen3.5-4B-Kazakh`, KazLLM-8B (CC BY-NC, gated) and Gemini.
  - Fixes: translate-test with Tilmash, or retrieval over official Kazakh FAQ pages.
  - Compute: 4-bit 4–8B models on a T4, a few thousand questions, about 2–4 h.
- **Originality: 3/5.** The language-gap evaluation itself is known (KazMMLU, Qolda). The Kazakhstan-specific money-question set and the fix are new.
- **Feasibility: 5/5.**
- **Risks.**
  - It can read as "just an evaluation"; it needs the fix plus a clear user.
  - Machine-translated benchmarks carry translation noise, so the team should spot-check 50 items.

### C5. Loan and microcredit contract explainer for Kazakh-speaking borrowers. **Track: Finance**

- **User and moment.** A borrower about to sign a microloan reads the Kazakh contract. The tool pulls out GESV/APR, total overpayment, penalties, early-repayment terms and collateral, then explains them in plain Kazakh.
- **Evidence.** 8.95M borrowers with 4.4 loans each; 1.177 trillion tenge more than 90 days overdue; 51k bankruptcies in 2025; collector debt up 37%.
- **Data.** Public standard contract templates from bank and MFO websites in kk and ru (to collect; aim for 20–40 documents). Gold fields annotated by the team.
- **Baseline.** Regex extraction.
- **ML.** LLM extraction (Qwen3.5-Kazakh or Gemini) with schema validation; field-level accuracy per language.
- **Originality.** 4/5.
- **Feasibility.** Medium: PDF collection and annotation eat the time.
- **Risks.** A very small evaluation set; legal accuracy; must state "not financial advice".

### C6. Kazakh pronunciation coach for adult learners (Astana language courses). **Track: Languages**

- **User and moment.** A Russian-speaking civil servant in an Astana free course (1,500–2,000 adults a year) practises minimal pairs such as қол/кол and өл/ол and gets feedback on each sound.
- **Evidence.** Only 22–25% of Slavic-origin citizens understand spoken Kazakh; the 2029 target is 84% Kazakh-speaking.
- **Data and models.** CTC character posteriors from a Kazakh wav2vec2-XLSR or Omnilingual CTC model, with GOP-style scoring. **I found no public L2-Kazakh learner speech corpus**, so the test set is the team's own recordings, read correctly and with deliberate Russian-style substitutions.
- **Baseline.** Raw ASR string match.
- **Originality.** 4/5.
- **Feasibility.** Medium.
- **Risks.** Evaluation rests on synthetic or self-made errors, which makes the impact evidence weaker.

### C7. Router for citizen appeals in kk, ru and mixed text (eOtinish-style). **Track: Languages**

- **Evidence.** 2.8M complaints were processed by AI with no accuracy statistics.
- **Data.** No public eOtinish data, only synthetic data, so the evidence is weak. Not recommended.

### C8. Kazakh-Russian Sign Language recognition. **Track: Languages**

- **Data.**
  - K-RSL (10 signers, 28,250 sentences, 600 signs; CoNLL 2020): download page unverified [S] https://aclanthology.org/2020.conll-1.51.
  - FluentSigners-50 (50 signers, 43,250 videos, 173 sentences; PLOS ONE 2022; continuous-recognition baseline TSPNet 16.0) [S] https://krslproject.github.io/FluentSigners-50.
- **Why not.** The team doesn't sign, so there is no real-speaker check; the data is large and continuous recognition is hard. Not recommended.

### Considered and rejected

- **Cyrillic Uyghur bridge.** NLLB covers only uig_Arab, while Omnilingual has uig_Cyrl ASR. The team can't check Uyghur output.
- **Karakalpak.** Mostly spoken in Uzbekistan.
- **Dungan.** No Omnilingual row, and I found no data.
- **Arabic-script Kazakh** (Kazakhs in China). MediaWiki already converts it by rule, so ML adds little.
- **Kazakh dialect ASR.** No dialect-labelled corpus; KSC has region diversity but no labels [S].

---

## 5. Scores (1–5) and ranking

| # | Project | Track | Impact evidence | Originality | Data now | Feasibility | Demo | Judge fit | **Sum /30** |
|---|---|---|---|---|---|---|---|---|---|
| C3 | Kazakh-letter restoration + downstream | Languages | 3 | 5 | 5 | 5 | 4 | 4 | **26** |
| C4 | kk vs ru LLM money/law answer gap + fix | Languages | 4 | 3 | 5 | 5 | 4 | 4 | **25** |
| C1 | Сақ бол scam screener, language-fair (kk/ru/mixed, voice stretch) | **Finance** | 5 | 4 | 2 | 3 | 5 | 5 | **24** |
| C1+C3 | C1 using C3 as its language component | Finance | 5 | 5 | 3 | 3 | 5 | 5 | **26** |
| C2 | Code-switched ASR with per-word-language WER | Languages | 3 | 4 | 4 | 3 | 4 | 5 | **23** |
| C5 | Loan-contract explainer kk/ru | Finance | 4 | 4 | 2 | 3 | 4 | 4 | **21** |
| C6 | Pronunciation coach | Languages | 3 | 4 | 2 | 3 | 5 | 3 | **20** |
| C7 | eOtinish-style appeal router | Languages | 3 | 3 | 1 | 3 | 3 | 3 | 16 |
| C8 | Kazakh-Russian Sign Language | Languages | 3 | 3 | 2 | 2 | 4 | 2 | 16 |

Ranking by weighted judgement: **C1+C3 > C3 > C2 > C4 > C1 alone > C5 > C6 > C7, C8**.

The weighting reflects the finals: demo 30%, impact 20%, technical depth 30%. Read the plain sum with that in mind. C3 wins on safety; C1+C3 wins on story and impact.

---

## 6. Strongest recommendation: C1+C3, "Сақ бол" (Finance track)

**One-line pitch.** "Fraud filters are built for Russian or English. In Astana, the city with the most internet fraud in Kazakhstan, scammers and their victims speak Kazakh, Russian and a mix of both, and type Kazakh without Kazakh letters. We measured how much worse a standard scam filter protects Kazakh-speakers, and closed the gap."

**Why this one:**
1. **The user and the evidence are local and current.**
   - Astana is #1 by cases (Jan–Jul 2026), and fake bank SMS and calls are the #1 scheme.
   - 84.5M scam calls were blocked in 2025.
   - The user's own grandparents are plausible test users and can serve as the speaker check.
2. **It covers every Finance-track judging point.** Precision and recall, a fair rule baseline (official ARDFM red flags), a **time-based split by scheme date**, **fairness across groups without direct attributes** (language and register act as the stand-in for group), explanations, and the disclaimer.
3. **It also shows the Languages-track evidence.** Per-language breakdown, side-by-side outputs, and a real-speaker check by the trilingual user.
4. **It is technically deeper than a generic spam filter.** It combines code-switched text (and optionally voice), a learned Kazakh-letter normaliser (C3) with an ablation, and a cross-lingual encoder vs TF-IDF vs zero-shot LLM.
5. **It is original next to the field.** No public kk/ru scam corpus exists. The likely competitors are English SMS-spam projects with "my language" added.

**Build order with cut lines:**

| Hours | Work | Cut line |
|---|---|---|
| 0–6 | Collect real scam and legitimate messages, dated and labelled kk/ru/mixed/keyboard/translit; write the red-flag rules | Under 100 real scams by hour 6 → switch to C3 alone (Languages) |
| 6–12 | Baselines plus TF-IDF and encoder models; per-group precision and recall | **MVP ready to submit** |
| 12–18 | C3 normaliser (ByT5-small or char tagger on KazParC kk with synthetic corruption); ablation on the keyboard-Kazakh group | — |
| 18–24 | Stretch: role-played calls → Kazakh Whisper → classifier; WER on Kazakh vs Russian words | — |
| 24–30 | Failure cases, bootstrap CIs, write-up, 2-minute demo (forward a real SMS, get a Kazakh explanation) | — |

**Fallback if data collection stalls:** C3 alone, under Languages. Its downstream evaluation can still include translating bank SMS and scam detection on the small real set.

---

## 7. Key datasets and models: access cheat-sheet

| Resource | Size | License | Access |
|---|---|---|---|
| FLEURS kk_kz / ru_ru | standard FLEURS splits | CC BY 4.0 | HF parquet, **not gated** [F] |
| Tim2190/kazakh-codeswitch-asr | 31 clips | CC BY 4.0 | HF, not gated [F] |
| diaslmb/KSC2 (parquet) | 406k utterances, 56 GB / 99 shards | not stated (source CC BY 4.0) | HF, not gated, streamable [F] |
| issai/Kazakh_Speech_Corpus_2 | ~1.2k h, ~80 GB tar parts | card says MIT; ISSAI site says CC BY 4.0 | HF, not gated [F] |
| KazParC | 371,902 sentences, kk/en/ru/tr | CC BY 4.0 | GitHub IS2AI/KazParC; HF issai/tilmash click-gated [F] |
| KazSAnDRA | 180,064 reviews | CC BY 4.0 | HF click-gated; GitHub [F] |
| kurumikz/telegram-corpus-russian-kazakh | 1.49M lines, 55 MB | CC BY-NC-SA 4.0 | HF, not gated [F] |
| issai/MMLU-Pro_Kazakh_Russian | 12,032 paired questions | MIT | HF, not gated [F] |
| MBZUAI/KazMMLU | ~23k questions | CC BY-NC 4.0 | HF, not gated [F] |
| kz-transformers/kazakh-unified-national-testing-mc | ~15k UNT questions | Apache-2.0 | HF [F] |
| shyngys879/kazakh-whisper-large-v3-turbo | 0.8B | Apache-2.0 | HF, not gated [F] |
| openai/whisper-large-v3-turbo | 0.8B | MIT | HF [F] |
| issai/Qwen3.5-4B-Kazakh | 4B | Apache-2.0 | HF, not gated [F] |
| issai/LLama-3.1-KazLLM-1.0-8B | 8B | CC BY-NC 4.0 + Llama 3.1 terms | HF, gated [F card] |
| facebook/nllb-200-distilled-600M, mms-1b-all, mms-tts-kaz | — | CC BY-NC 4.0 | HF, not gated [F] |
| ai4kazakh/ISSAI_KazakhTTS2 | parquet | CC BY 4.0 | HF [F listing] |
| Omnilingual ASR | 300M–7B | check repo license | GitHub facebookresearch/omnilingual-asr [F csv] |

Compute fit: Kaggle T4×2 or a Colab T4 covers Whisper-turbo LoRA (3–5 h), ByT5-small (1–2 h) and 4-bit 4–8B LLM evaluation. The local M5 with 16 GB is enough for TF-IDF, encoders and the Gradio demo.
