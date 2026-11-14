# 30 — AI + Finance track research (Kazakhstan-first, Finance x Language)

Researched 2026-11-14 (all URLs accessed that day). Team member: Astana, fluent Kazakh / Russian / English, passion = Finance + Languages.
Prototype disclaimer that must go in any write-up: "This project is a prototype and is not financial advice."

**Source-quality note.** Kazakhstan agency pages (nationalbank.kz, gov.kz, kazpravda) often return binary/403 to automated fetches, so most KZ numbers below are reputable KZ outlets quoting a named agency or official (bizmedia.kz, bes.media, 24.kz, inbusiness.kz, Times of Central Asia, tengrinews). Each row names the original agency. KZ fraud statistics **conflict across agencies** (police vs Prosecutor General vs National Bank count different things) — quote them with the agency name, never as one "true" number.

---

## 0. Bottom line

**Build a Kazakh / Russian / code-switched "scam-call and scam-message early-warning" model that flags a social-engineering script *before the ask* (SMS code, "safe account", "take a loan for the investigation"), evaluated on a hand-built real Kazakhstan test set, with per-language fairness and a time-based split by scheme date.** Reasons are in section 6. The strongest backup with near-zero data risk is the Bank Account Fraud (BAF) onboarding-fraud + age-fairness project (candidate C2).

---

## 1. Where AI works in consumer finance protection (2025-2026), where it fails, gaps

### Works (with evidence)
| What | Evidence | Source |
|---|---|---|
| Bank/consortium-side blocking of *unauthorised* fraud (card, account takeover) | UK unauthorised fraud losses fell 5% to £703.4m in 2025, attributed to investment in detection and prevention | UK Finance Annual Fraud Report 2026, https://www.ukfinance.org.uk/news-and-insight/press-release/fraud-report-2026-press-release (Jun 2026) |
| Shared antifraud data hub in KZ | National Antifraud Center (operated by NBK's National Payment Corporation): 127 bn tenge of fraudulent operations prevented since 2024, as of 1 Sep 2026; 270+ connected orgs (banks, MFOs, telcos, police) | digitalbusiness.kz 2026-09-14, https://digitalbusiness.kz/2026-09-14/moshenniki-pitalis-ukrast-127-mlrd-tenge-kto-v-kazahstane-ostanovil-ih/ |
| Friction at the loan moment works against "loans taken under scammer dictation" | Fraudulent loans in KZ: 8.7k loans / 20.3 bn tenge (2024) → 5.1k / 4.6 bn (2025) → 1.3k / 2.1 bn (2026 YTD), after Stop-credit self-ban, biometrics, cooling-off periods (ARDFM figures) | 24.kz 2026-10-20, https://24.kz/ru/news/economyc/800545-bolee-7-mln-kazakhstantsev-podklyuchili-stop-kredit-ot-chego-on-zashchishchaet |
| Reimbursement + bank interventions reduce APP losses (short-term) | PSR: 88% (£173m) of reimbursable APP losses returned, 7 Oct 2024–30 Sep 2025; Frontier Economics evaluation: APP losses −21% (−£73m) in year one | https://www.psr.org.uk/information-for-consumers/app-scams-reimbursement-dashboard (upd. 2026-01-30); https://www.frontier-economics.com/media/2ctd3jq2/app-fraud-evaluation-final-summary-report-26-06-26.pdf |
| Tabular GBDT models on realistic fraud data | BAF benchmark: LightGBM evaluated at 5% FPR, temporal split (months 0-5 train, 6-7 test) is the accepted protocol | Jesus et al., NeurIPS 2022 D&B, https://arxiv.org/abs/2211.13358 |
| LLMs can read scam *conversations* in real time | "Promising results" for LLM phone-scam detection as calls happen | Shen et al. 2024, https://arxiv.org/abs/2409.11643 |

### Fails (with evidence)
| Failure | Evidence | Source |
|---|---|---|
| **Authorised (social-engineering) fraud keeps growing even where card fraud falls** — the victim makes the payment, so transaction models see a "normal" customer | UK APP fraud +19% to £576.4m, 248,070 cases in 2025, while unauthorised fell 5% | UK Finance 2026 (above) |
| Same pattern in US | FTC: record $15.9 bn reported losses 2025, investment scams $7.9 bn, imposters ~1M reports / $3.5 bn. FBI IC3: $20.877 bn (+26%), 1,008,597 complaints, investment $8.65 bn, 60+ age group $7.75 bn (+59%) | FTC testimony 2026-03-25 via https://www.pymnts.com/fraud-prevention/2026/consumer-fraud-losses-quintupled-since-2020-ftc-says/ and https://www.spokesman.com/stories/2026/apr/03/americans-lost-a-record-159-billion-to-scams-in-20 ; IC3 via https://therecord.media/cyber-fraud-surges-to-17-billion-fbi-ic3 and https://www.theblock.co/post/397134/ |
| Interventions decay as scammers adapt | Australia: losses −25.9% in 2024 to A$2.03 bn, then +7.8% to ~A$2.18 bn in 2025 | NASC Targeting Scams report 2025, https://www.nasc.gov.au/system/files/targeting-scams-report-2025.pdf |
| LLM scam detectors break under adversarial rewording | Adversarial scam messages cause high misclassification | Chang et al., arXiv 2412.00621 (Dec 2024), https://arxiv.org/abs/2412.00621 |
| LLMs fail in multi-round inducement and across languages | Fraud-R1: 8,564 cases, 15 LLMs; worst in role-play and fake-job scenarios; large Chinese vs English gap → "need for better multilingual fraud detection" (ACL Findings 2025) | https://arxiv.org/abs/2502.12904 |
| Phone-scam LLM detection: low recall, hallucination, biased datasets | Shen et al. 2024 | https://arxiv.org/abs/2409.11643 |
| Kazakh and Russian are weak spots for LLMs | KazMMLU (23k questions; 10,969 KK + 12,031 RU): "even the best-performing models struggle" in Kazakh and Russian | https://arxiv.org/abs/2502.12829 (2025) |
| Voice-deepfake detectors don't generalize | "Performance degradation of up to one thousand percent" on in-the-wild audio | Müller et al., Interspeech 2022, https://arxiv.org/abs/2203.16263 |
| Gambling-harm AI cannot be compared | No standardized benchmarks for AI player-risk detection | Ghaharian et al., J. Gambling Studies 2026, https://arxiv.org/abs/2511.21658 |

### Gaps (= where a 30-hour project can be original)
1. **Conversation-level, user-side, pre-payment detection** in the language the victim actually speaks. Bank models act at the transaction; the deciding signal in authorised fraud is in the *call/chat script*, minutes earlier.
2. **Kazakh and Kazakh-Russian code-switched scam text: no public labelled dataset exists.** Checked 2026-11-14: Hugging Face API (`language:kk` + scam/fraud/spam) → 0 datasets; Kaggle CLI search "kazakh" → no scam data; GitHub search → only a 2025 email-spam toy repo. KZ papers (SDU 2023, ENU 2025) built private sets: https://repository.sdu.edu.kz/handle/123456789/1556 , https://vestnik.agakaz.kz/?p=9811 . The KRCS paper says no public code-switched RU-KK parallel data existed before it: https://arxiv.org/abs/2503.20007 .
3. **Early warning** ("how many turns before the scammer asks for the code?") is not a standard metric in any public scam dataset found.
4. **Fairness by language group** (Kazakh-first vs Russian-first users) is unmeasured, although KazMMLU shows models are weaker in Kazakh.

---

## 2. Problem size

### Kazakhstan (the core)
| Fact | Number | Agency / source | URL, date |
|---|---|---|---|
| Internet-fraud cases 2025 | 27,892 registered (record); 2026 to date 14,414 (−13% y/y) | Committee on Legal Statistics (Prosecutor General) via bizmedia | https://bizmedia.kz/2026-10-12-izobrazheniya-i-golosa-sotrudnikov-bankov-i-rodnyh-poddelyvayut-moshenniki-v-kazahstane/ (2026-10-12) |
| Share of all crime | 23.3% of registered criminal offences in 2025; 55x growth since 2018 (517 cases) — bank.kz reports 28.9k cases | bank.kz / 24.kz quoting legal statistics | https://bank.kz/news/finansy-news/internet-moshennichestvo-kazakhstan-statistika/ ; https://24.kz/ru/news/economyc/787066-pochti-kazhdoe-chetvertoe-prestuplenie-v-kazakhstane-svyazano-s-internet-moshennichestvom-nazvany-tsifry |
| Damage 2025 (prosecutors) | 12.2 bn tenge; ~5 bn returned; Q1 2026 4.8 bn, 2.4 bn returned | Ye. Akhmetov, deputy chair, Committee on Legal Statistics, AntiFraud Forum | https://bes.media/news/zhertvam-internet-moshennichestva-vernuli-5-mlrd-tenge-za-2025-god-29b6f5/ (2026-04-08) |
| Damage 2025 (police) | >29 bn tenge citizen losses | MVD cyber-police unit, via inbusiness/finprom | https://inbusiness.kz/ru/last/milliardy-poter-pochemu-kazahstancy-vse-chashe-zayavlyayut-ob-internet-moshennikah (2025-12-31) |
| 2024 "voluntary" transfers to fraudsters | ~45 bn tenge | Vice-Minister of Internal Affairs S. Sarsenov, Digital Almaty 2025 | https://finratings.kz/news/407-kazakhstantsy-dobrovolno-otdali-moshennikam-45-mlrd-tenge-v-2024-godu-mvd/ |
| Scheme mix (NBK antifraud-center data since Jul 2024) | **phone scams 22%, fake investment platforms 19%, "drop" cards 19%** | National Bank via Times of Central Asia | https://timesca.com/kazakhstan-to-hold-banks-and-mobile-operators-liable-for-online-fraud-losses/ (2025-06-24) |
| SIM cards on fake identities | ~100,000 cases detected in 2025 (to June) | President Tokayev, same article | same |
| Money mules ("droppers") | Criminal Code Art. 232-1 in force 16 Sep 2025; >112 bn tenge passed through dropper accounts (AFM) | bizmedia; kazpravda (AFM) | https://bizmedia.kz/2025-09-16-v-kazahstane-vvedena-ugolovnaya-otvetstvennost-za-dropperstvo/ ; https://www.kazpravda.kz/n/cherez-scheta-dropperov-v-kazahstane-proshlo-bolee-112-mlrd-tege (403 on fetch, figure from search snippet — verify) |
| Loans taken under scammer control | 8.7k / 20.3 bn tenge (2024); 5.1k / 4.6 bn (2025); 1.3k / 2.1 bn (2026 YTD) | ARDFM via 24.kz | https://24.kz/ru/news/economyc/800545-bolee-7-mln-kazakhstantsev-podklyuchili-stop-kredit-ot-chego-on-zashchishchaet (2026-10-20) |
| Stop-credit self-ban (eGov) | >7 million users (Oct 2026); 5.1M on 16 Mar 2026 | 24.kz; digitalbusiness | same; https://digitalbusiness.kz/2026-03-31/5-mln-kazahstantsev-zapretili-sebe-brat-krediti-vot-kak-eto-rabotaet/ |
| **New decision moment (1 Oct 2026)**: ARDFM 7-question anti-fraud questionnaire before any unsecured online loan. Q2: "не поступал ли звонок от человека, представившегося сотрудником банка, полиции или службы безопасности"; Q5: "не собирается ли заёмщик переводить средства на «безопасный счёт»"; Q6: understands amount/term/rate/schedule; Q7: pressure/urgency. Plus cooling-off (≥8 h / ≥24 h for high-risk) | ARDFM resolutions of 15 May 2026 | https://finratings.kz/news/16827-kakie-voprosy-budut-zadavat-kazakhstantsam-pered-vydachei-onlain-kreditov/ (2026-09-29) |
| NBK antifraud rules (amended 10 Jun 2026 No. 58) | Center keeps databases of "compromised phone numbers", "potential victims", and **"multiple credit applications" = applications to ≥2 lenders within 1 hour** (a coded scam signal) | National Bank, official rules text | https://nationalbank.kz/file/download/129443 (docx) |
| Scam scripts (official, verbatim fragments, RU) | 6 schemes: fake "bank security"; WhatsApp "bank employee" with logo; fake eGov aid ("вводите ИИН и коды подтверждения… оформляете кредит по инструкции"); fake KNB/MVD "joint operation" ("не говорить никому", "оформить кредит… в помощь следствию"); fake meter replacement ("пройти биометрию"); voice-cloned relative ("продиктовать код из SMS") | Bank CenterCredit official page | https://www.bcc.kz/about/press-center/main-schemes-used-by-scammers/ (2026-09-24) |
| Deepfakes now used in KZ | Faked voices/images of bank staff, police, relatives; fake video calls; Halyk warned of deepfake of its CEO | bizmedia; finratings | https://bizmedia.kz/2026-10-12-izobrazheniya-i-golosa-sotrudnikov-bankov-i-rodnyh-poddelyvayut-moshenniki-v-kazahstane/ ; https://finratings.kz/news/13584-halyk-bank-srochno-predupredil-o-dipfeikakh-s-umut-shaiakhmetovoi/ |
| Astana-specific: AIFC impersonation | AFSA 2026 alerts: forged AFSA licences, clones of licensed firms (Jade Capital, Kantai, Venera Capital, Freedom Finance Global), Telegram "t.me/investlink_kz" promising 10-15% per month | AFSA | https://afsa.aifc.kz/alert-fraudulent-impersonation-of-kantai-securities-limited-and-unauthorised-investment-solicitations/ ; IOSCO I-SCAN https://www.iosco.org/i-scan/?id=56847 |
| Over-indebtedness | Retail loans 90+ overdue: 6% (May 2026), peak 8.2% (Apr 2025). Payday loans: 18.9% 90+ overdue (1 Jun 2025); 1.2M PDL users in 2024, 2/3 holding other microloans, 383k used PDLs >6 months, avg age 33.2 | National Bank via inbusiness | https://inbusiness.kz/ru/last/19-pochti-kazhdyj-pyatyj-zajm-do-zarplaty-v-kazahstane-prosrochen (2026-07-31) |
| Personal bankruptcy | >51,000 declared bankrupt in 2025, 188 bn tenge written off; ~300k eligible from 2026 | Vice-Minister of Finance Ye. Birzhanov | https://bes.media/amp/okolo-300-tisyach-kazahstantsev-smogut-podat-na-bankrotstvo-s-2026-goda-minfin-04a16f/ (2025-12-05) |
| Rate caps (GESV) | 46% unsecured bank loans and MFO microcredits; 35% secured; 25% mortgage; MFO ≤45 days and ≤45 MRP: <0.3%/day, max 179% (from 16 May 2026) | ARDFM + NBK joint resolution | https://bizmedia.kz/2026-05-06-predelnye-gesv-po-zajmam-i-mikrokreditam-opredelili-arrfr-i-naczbank/ ; https://nationalbank.kz/ru/news/informacionnye-soobshcheniya/19873 |
| Gambling | ~350k people involved (~2% of population, incl. minors); min. age 21; eGov self-ban up to 10 yrs; banks blocked ~$21M illegal-casino payments in 6 months (2026) | Government statements via industry press (lower confidence) | https://egov.kz/cms/en/news/zapred_azartn_igry ; https://casinobeats.com/2026/07/07/kazakhstan-govt-says-banks-have-blocked-21m-worth-of-illegal-casino-transactions/ |
| Pension early withdrawals | >1 trn tenge withdrawn in 2025 (~824 bn housing, ~392 bn treatment); dental-treatment withdrawals suspended from 15 Sep 2025 | ENPF figures via search results (verify before quoting) | https://bes.media/news/kazahstantsy-potratili-435-mlrd-tenge-iz-enpf-na-zhile-i-lechenie-s-nachala-2026-goda/ |

### Global (for the "why this matters" slide)
- FTC 2025: $15.9 bn (record), investment $7.9 bn, 60+ ≈ $3 bn (links above; FTC older-adults report https://www.ftc.gov/node/338049).
- FBI IC3 2025: $20.9 bn, crypto-related $11.4 bn, 60+ $7.75 bn (links above).
- UK Finance 2026: £1.28 bn total (+4%), APP £576.4 m (+19%), 66% of APP cases start online (link above).
- UNODC (Jul 2026): scam losses US$88.3–114.1 bn across East/SE Asia + AU/NZ in 2025; trafficked scam-compound workers from ≥80 countries: https://decrypt.co/374140/southeast-asian-scam-networks-cost-victims-up-to-114b-in-a-year-un (verify against UNODC PDF).

---

## 3. The generic answers other teams will build (avoid)
1. SMS Spam Collection + TF-IDF + Naive Bayes, maybe "+20 scam texts in my language" — the brief itself suggests this, so it is the most crowded idea.
2. ULB credit-card fraud (2013, PCA features) + SMOTE + XGBoost.
3. German Credit fairness with the under-25 split.
4. FinBERT headlines → DJIA.
5. PaySim mobile-money fraud (known balance-column leakage → fake 99% scores).
6. Lending Club / Home Credit 2018 default model + SHAP.
7. "AI budgeting assistant for teens" / "explain bank fees" GPT wrapper (both are the brief's own examples) — usually no real evaluation.
8. Phishing-URL classifier on UCI phishing features.
9. English scam-call classifier on BothBosu synthetic dialogues (the top HF hit for "scam conversation").
10. Stock/crypto price LSTM.
Differentiators that ChatGPT-style answers won't produce: Kazakh/code-switched data, KZ-specific scheme taxonomy from official sources, the ARDFM 7-question moment, early-warning metric, per-language fairness, date-based split by scheme emergence, real hand-collected KZ test set.

---

## 4. Candidate projects

### C1. Qazaq/Russian scam-script early warning (calls + messages) — RECOMMENDED
- **User + moment.** Gulnara apa, 67, Kazakh-first pensioner in Astana. On a WhatsApp call from "Kaspi security" / "KNB investigator", seconds before she reads out an SMS code, takes an online loan "to protect her money", or moves funds to a "safe account". Secondary user: the grandchild who installs it. The ARDFM 7-question checklist (1 Oct 2026) is the official version of this moment, and Q2/Q5/Q7 are exactly what the model detects.
- **Input → output.** Running transcript (typed, pasted, or Whisper/KSC2 ASR of a staged call) or a forwarded message → per-turn risk score, the matched scheme (6 BCC schemes + NBK descriptions), the highlighted trigger phrase, and one sentence of advice in the user's language ("Банк ешқашан SMS-кодты сұрамайды — 1477-ге немесе банкке өзіңіз қоңырау шалыңыз").
- **Evidence.** Phone scams 22% of schemes (NBK); scammer-dictated loans 20.3 bn tenge in 2024 (ARDFM); 27.9k internet-fraud cases 2025; deepfaked bank staff/relatives (2026); LLMs weak in Kazakh (KazMMLU) and in multi-turn inducement (Fraud-R1).
- **Datasets (all checked 2026-11-14):**
  | Dataset | Size | License | Access |
  |---|---|---|---|
  | BothBosu/single-agent-scam-conversations (EN, Llama-3-70B synthetic, typed scam scenarios) | 1,280 train / 320 test | Apache-2.0 | `load_dataset("BothBosu/single-agent-scam-conversations")` https://huggingface.co/datasets/BothBosu/single-agent-scam-conversations |
  | BothBosu/multi-agent-scam-conversation | 1,280 / 320 | Apache-2.0 | HF |
  | dokster/adaption-scam-dataset-ru-en-v1 (synthetic triage: risk level, 14 scam types incl. family_impersonation, marketplace_scam) | 2,324 (1,124 RU) | Apache-2.0 | HF https://huggingface.co/datasets/dokster/adaption-scam-dataset-ru-en-v1 |
  | Abdurohman/fraudlens-ru-v1 — RU posts from 8 public anti-fraud Telegram channels, **dated 2021-12 → 2026-05** (4,086 in 2025, 1,878 in 2026), auto-labelled fraud_type/method/target. They are *posts about scams*, not raw scam messages → use for scheme lexicon + date split; 91 mention KZ terms | 6,327 | CC BY 4.0 | HF jsonl https://huggingface.co/datasets/Abdurohman/fraudlens-ru-v1 |
  | DmitryKRX/anti_spam_ru (benign + spam RU) | 66,119 (21.5k spam) | Apache-2.0 | HF |
  | alt-gnome/telegram-spam (RU) | 21,411 | CC0 | HF |
  | Kaggle rivalcults/youtube-scam-phone-call-transcripts (real EN scam calls) | ~150 KB | check card | `kaggle datasets download rivalcults/youtube-scam-phone-call-transcripts` |
  | issai/tilmash (KK↔RU↔EN MT), facebook/nllb-200 (kaz_Cyrl) for translation | — | check cards | HF |
  | ISSAI KSC2 Kazakh speech (1.2k h, includes KK-RU code-switching) for ASR / benign speech | 600k+ utterances | CC BY 4.0 | https://issai.nu.edu.kz/ksc2/ |
  | KRCS code-switched KK-RU social-media sentences (benign code-switch style) | 618 | per paper | https://arxiv.org/abs/2503.20007 |
  | **Real KZ test set (build it, ~100-200 items):** verbatim fragments from BCC (6 schemes, 2026-09-24), NBK/fingramota tips, Kaspi Guide videos (guide.kaspi.kz, transcribe), ARDFM questionnaire, KGD/eGov fake-tax-notice warnings, AFSA alerts, news reproductions of real scam SMS (e.g. https://finratings.kz/news/13107-kazakhstantsev-atakuiut-moshenniki-cherez-sms-ot-halyk-bank/ , https://finratings.kz/news/13256-ot-imeni-halyk-bank-i-beeline-kazakhstantsam-slali-falshivye-sms/amp). Hard negatives: real *legit* bank SMS/notification templates (OTP "никому не сообщайте код", legit collection reminders) with all personal data removed. Two annotators, report agreement. | small | public pages; cite each | manual |
- **Baseline.** (a) Keyword/regex rule from official warnings in RU+KK ("код из SMS", "безопасный счёт", "служба безопасности", "қауіпсіздік қызметі", "AnyDesk", "на вас оформляется кредит", "не говорите родственникам"); (b) TF-IDF + logistic regression.
- **ML.** Fine-tune `intfloat/multilingual-e5-base` or `xlm-roberta-base` on turn-prefixes (classify after each turn → early warning); compare zero-shot LLM (Sherkala-8B-Chat / issai KazLLM-8B (CC BY-NC) / Qwen2.5-7B) on the real test set. Training data: EN dialogues translated to RU and KK (Tilmash vs NLLB, report both), plus LLM-generated KZ-scheme dialogues including code-switched variants (disclose as synthetic).
- **Metrics (judge-aligned).** Conversation recall at 1% FPR and PR-AUC; **median turns of warning before the "ask"**; **per-language breakdown (kk / ru / code-switched / en)** = fairness across groups; **time split**: train on schemes documented up to 2025, test on 2026 schemes (meter-replacement + biometrics, fake KNB "joint operation", "blocked account", NFC "tap your card", deepfake relative). Show 5 failures (legit collection calls, legit OTP SMS).
- **Originality.** High: no public Kazakh scam dataset exists; first KZ scheme taxonomy grounded in official sources; early-warning metric; language fairness. Fits both of the user's passions while staying in the Finance track.
- **Feasibility (30 h).** 4-6 h data + real test set, 3 h translation, 4 h synthetic KZ scripts, 6 h models/baselines, 4 h evaluation + failures, 5 h demo (Gradio: paste/stream transcript, risk bar per turn, Kazakh/Russian explanation), 3 h write-up. ASR on audio = optional stretch.
- **Risks.** Synthetic-heavy training inflates scores → headline only real-test-set numbers. Translation artefacts in Kazakh → native-speaker check (the team member). LLM-generated scripts must be disclosed. Real-test-set size is small → report confidence intervals. Do not use real victim recordings or personal data.

### C2. Onboarding-fraud ("dropper / fake-identity account") model with age fairness — BAF
- **User + moment.** Onboarding analyst at an Astana digital bank deciding auto-approve vs manual review for a new account; the person harmed by false positives is a 55+ applicant blocked from banking.
- **Evidence.** ~100k SIM cards on fake identities (2025), dropper accounts >112 bn tenge (AFM), Art. 232-1 (2025).
- **Data.** Kaggle `sgpjesus/bank-account-fraud-dataset-neurips-2022`: 6 CSVs (~213-252 MB each), 1M applications each, 30 features, 8 months (Feb-Sep), fraud 0.85-1.5%/month, protected attributes customer_age / income / employment_status; license **CC BY-NC-SA 4.0**; 29.6k downloads. Paper: https://arxiv.org/abs/2211.13358.
- **Baseline.** Rule (velocity + email-name similarity + foreign request) and logistic regression.
- **ML.** LightGBM; threshold at 5% FPR; predictive equality (FPR ratio, age >50 vs ≤50); train *without* age and find proxies; Variants IV/V show temporal bias shift.
- **Originality** medium (a known benchmark, but not among the brief's cases). **Feasibility** very high. **Risks:** synthetic data; no language angle; non-commercial license.

### C3. "Easy money" dropper-recruitment ad detector for teenagers (RU/KK)
- **User + moment.** 17-year-old in Astana seeing a Telegram/Instagram ad: "подработка: принимать переводы на свою карту, 30 000 ₸ в день" — before replying.
- **Evidence.** Art. 232-1 criminal liability (Sep 2025); several thousand citizens on dropper lists (https://timesca.com/thousands-of-kazakhstanis-added-to-financial-watchlists-over-suspected-fraud/); Tokayev on people renting out accounts for reward.
- **Data.** Positives: FraudLens `recruitment_scam` (485, RU), EMSCAD fake jobs (Kaggle `shivamb/real-or-fake-fake-jobposting-prediction`, 17,880 EN postings / 866 fraudulent), synthetic RU/KK dropper ads. Negatives: real KZ vacancies — **hh.ru API now returns 403 without an app token (tested 2026-11-14)**, so collect manually from enbek.kz / hh.kz pages.
- **Baseline** keyword list; **ML** multilingual encoder; per-language fairness. **Originality** high, good story (teens protecting teens). **Risk:** few real positives → evaluation thin.

### C4. Money-mule (dropper) ring detection on transaction graphs
- **User + moment.** AML analyst at a payment organisation deciding which accounts to freeze/report to the AFM today.
- **Data.** IBM AMLworld (Kaggle `ealtman2019/ibm-transactions-for-anti-money-laundering-aml`, CDLA-Sharing-1.0; HI/LI Small-Medium-Large; HI-Medium_Trans 3.0 GB, HI-Large 17 GB — use HI-Small), paper https://arxiv.org/abs/2306.16424. Alternative: Kaggle `dmitrygaydabura/synthetic-sepa-transfer-fraud` (APP, Verification-of-Payee, mules; 118 MB; Oct 2026; unknown provenance).
- **Baseline** fan-in/fan-out/pass-through rules; **ML** GBDT on graph features or GNN; native time split. **Fairness** weak (no demographics). **Originality** medium. **Feasibility** medium (data size).

### C5. Kazakh plain-language microcredit contract explainer + legal-cap checker
- **User + moment.** 19-year-old student in Astana about to sign an MFO "договор присоединения" on the phone; ARDFM Q6 asks if she understands amount, term, rate, schedule.
- **Evidence.** PDL 18.9% 90+ overdue; 383k PDL users >6 months in 2024; 51k bankruptcies in 2025; GESV caps 46% / 0.3%/day / 179%.
- **Data.** Public MFO offer contracts (PDF, KK + RU; e.g. KMF rules PDF https://kmf.kz/storage/app/media/Financial/12-19-pravila-predostavleniia-mikrokreditov-no-1-ot-26082024-1.pdf), ARDFM MFO register; hand-label 30-50 contracts; inject illegal terms for a synthetic violation test.
- **Baseline** regex extraction; **ML** LLM extraction + Kazakh simplification; metric = field exact-match, violation precision/recall, comprehension quiz with 5-10 real readers; kk vs ru accuracy gap. **Weakness:** no time split; "explain fees" is a brief example (others may do it in English); labelling cost.

### C6. Fake investment platform / AIFC-impersonation checker (Astana-specific)
- **User + moment.** Astana office worker reading a Telegram channel claiming an "AIFC licence" and 10-15% monthly returns, before the first deposit.
- **Evidence.** Fake investment platforms 19% of KZ schemes; AFSA 2026 clone-firm alerts; FTC investment $7.9 bn, IC3 $8.65 bn.
- **Data.** AFSA alerts + AFSA public register; IOSCO I-SCAN warnings; ScamWorld (HF `oscarwu/ScamWorld`, 363 scam + 53 legit rebuilt websites, 26 languages incl. ru, CC BY-NC 4.0, Nov 2026; paper arXiv 2611.04879 per card); FraudLens `investment_scam` (119).
- **Key insight:** a register-lookup baseline fails on clone firms (they use real licensed names). **Risk:** real labelled RU/KK investment-ad text must be scraped → data thin for 30 h.

### C7. Voice-clone "relative in trouble" detector for Kazakh/Russian voice notes
- **User + moment.** Parent receives a WhatsApp voice note "мама, срочно переведи…" in the child's voice.
- **Data.** Real speech: KSC2 (CC BY 4.0), Mozilla Common Voice kk/ru; fakes generated with open TTS (e.g. ISSAI KazakhTTS2, MMS-TTS-kaz, XTTS-v2 for ru); evaluate on a held-out TTS system.
- **Evidence** BCC scheme #6 (2026), deepfakes in KZ (Oct 2026). **Risk:** Müller et al. show detectors overfit to known generators → expect large drop; finance link is indirect; edges into Languages track.

### C8. (Global backup) P2P/APP-scam complaint triage with "Older American" fairness — CFPB
- **User + moment.** A scam victim deciding whether and how to escalate a Zelle/wire scam complaint; or a consumer advocate prioritising cases.
- **Data.** CFPB Consumer Complaint Database (public, US-government, CSV + API, dated, product/issue labels, optional narratives, "Older American"/"Servicemember" tags) https://www.consumerfinance.gov/data-research/consumer-complaints/ — verify size on download.
- **Baseline** majority/company base-rate; **ML** text classifier predicting "closed with monetary relief"; date split; fairness by tag. **Weak on local angle and language.**

### Considered and rejected
- **Youth gambling harm (KZ):** strong evidence (350k gamblers, age-21 law), but no public player-level data (bwin/Transparency Project data is ~2005; RGC/GREO data are surveys); arXiv 2511.21658 confirms no benchmarks.
- **Pension early withdrawal advisor:** it is a calculator; AI would not do the main job.
- **Loan-default/overindebtedness model (Home Credit 2018/2024):** generic; 2024 "credit risk model stability" data is competition-licensed; metric was known to be gameable.

---

## 5. Scores (1-5) and ranking

| # | Candidate | Impact evidence | Originality | Data now | Feasibility 30h | Demo | Judge fit | **Total /30** |
|---|---|---|---|---|---|---|---|---|
| C1 | KK/RU scam-script early warning | 5 | 5 | 3 | 4 | 5 | 5 | **27** |
| C2 | BAF onboarding fraud + age fairness | 4 | 3 | 5 | 5 | 4 | 5 | **26** |
| C3 | Dropper-recruitment ad detector | 4 | 5 | 2 | 4 | 4 | 4 | **23** |
| C8 | CFPB APP-scam triage + Older-American fairness | 4 | 3 | 5 | 4 | 3 | 4 | **23** |
| C4 | Mule-ring graph detection | 4 | 3 | 4 | 3 | 4 | 4 | **22** |
| C7 | KK/RU voice-clone detector | 3 | 5 | 3 | 3 | 5 | 3 | **22** |
| C5 | Kazakh contract explainer + cap checker | 4 | 3 | 3 | 3 | 4 | 3 | **20** |
| C6 | AIFC-impersonation investment checker | 4 | 5 | 2 | 2 | 4 | 3 | **20** |

C1 judge fit = 5: it has the right metric (recall at fixed low FPR plus warning lead time, not accuracy), two fair baselines (rule, TF-IDF), trust (shows the trigger phrase and the official rule), fairness across language groups without any personal attribute, and a time split by scheme date.

---

## 6. Strongest recommendation: C1, with one design choice that makes it win

**Why C1.**
1. It goes at the part of fraud that is growing and that bank models miss: authorised, social-engineering fraud (UK APP +19%, FTC/IC3 records, KZ phone scams 22% + scammer-dictated loans).
2. It matches a brand-new, official KZ decision moment (ARDFM 7 questions, 1 Oct 2026), so judges can see the real-world hook.
3. It needs the team's rare asset, native Kazakh + Russian, which other teams' ChatGPT answers cannot supply. No public Kazakh scam dataset exists, so the contribution is real.
4. Every finance-judge criterion maps to a concrete number (section 5).
5. The demo is strong: a staged call transcript where the risk bar turns red at turn 3, before the scammer asks for the code at turn 6, with the explanation in Kazakh.

**The design choice:** headline only results on the **real, hand-collected KZ test set**, and report per-language and early-warning results. Use synthetic/translated data only for training. Pre-register the rule baseline from official bank warnings so "beats a simple rule" is honest. A likely, reportable finding is that the keyword rule has high precision but fires late (only at the "ask"), while the model warns earlier at the cost of some false positives on legit collection calls.

**Fallback if the real test set ends up too small by Saturday night:** pivot to C2 (BAF); it can be built in under 15 hours and fits the judge rubric directly.

**Ethics line for write-up:** no real victim data; synthetic data disclosed; prototype, not financial advice; points users to 1477 (NBK contact centre) / 102 / their bank's official number.
