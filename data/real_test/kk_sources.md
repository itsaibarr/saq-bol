# Kazakh / code-switched real test set: sources and method

Collected 2026-11-14 by one agent (Kazakh slice). File: `kk_collected.jsonl` (132 items). A separate agent covers Russian-language sources.

## How the text was captured
- Every page was downloaded as raw HTML with `curl` and turned into plain text locally. Item text was copied from that text, not from an AI summary. WebFetch was not used for item text because it only returns summaries.
- A script (`bin/verify.py` in the session scratchpad; it needs the saved HTML, which is not in this folder) checked that every item's `text` appears word for word in its source page text, after whitespace normalisation: **132/132 matched, 0 failures**. One allowed difference: kk_037 had a first name scrubbed (`Сашаға` became `[NAME]ға`).
- No translation, no completion of fragments. Spelling slips in the source are kept as published (e.g. kk_008 "SMS кодын таңдаңыз", which reads like a translation of RU "назовите").

## Counts
- label: scam 91 (83 verbatim + 8 `kind=paraphrase`), legit 41.
- kind: call_quote 77, web 37, paraphrase 8, sms 6, messenger 4.
- language: kk 131, mixed 1 (kk_061, Russian word "посылка" inside a Kazakh sentence). kbd=true: 0.
- parallel_group set on 36 items (ARDFM 13, BCC 16, Otbasy 7); the Russian URL for each is in `notes`.

## Sources
| # | Source URL | Publisher | Date | scam | legit | paraphrase | ids |
|---|---|---|---|---|---|---|---|
| 1 | https://www.gov.kz/memleket/entities/ardfm/press/news/details/1275708?lang=kk | ARDFM (Қаржы нарығын реттеу және дамыту агенттігі) via gov.kz | 2026-08-18 | 13 | 1 | 0 | kk_001–kk_089 |
| 2 | https://www.bcc.kz/kz/about/press-center/safe-account/ | Bank CenterCredit (BCC) | 2026-08-06 | 7 | 1 | 0 | kk_014–kk_095 |
| 3 | https://hcsbk.kz/most-important/antifraud/ | Otbasy Bank (hcsbk.kz) | 2026-01-01 (low) | 7 | 1 | 0 | kk_021–kk_108 |
| 4 | https://informburo.kz/kaz/newskaz/1414-ten-kelgen-kod-zane-zalgan-nesie-almaty-oblysy-policiiasy-alaiaqtardyn-aila-sargylaryn-askereledi | Informburo.kz (citing Almaty region police) | 2026-07-28 | 9 | 1 | 0 | kk_028–kk_109 |
| 5 | https://informburo.kz/kaz/newskaz/balama-dauys-bersi-alaiaqtar-whatsapp-pen-telegram-akkaunttaryn-qalai-buzyp-zur | Informburo.kz (31 channel, citing North Kazakhstan police) | 2026-10-21 | 2 | 2 | 0 | kk_037–kk_107 |
| 6 | https://informburo.kz/kaz/qazaqstanda-alayaqtyqtyn-zana-turleri-pandemiya-kezinde-adamdardy-qalai-aldaidy | Informburo.kz | 2021-06-03 | 4 | 0 | 0 | kk_039–kk_042 |
| 7 | https://informburo.kz/kaz/omir/khalaj-akciyagha-senip-alayakhtyng-aldauyna-tuesip-khalmaugha-bolady | Informburo.kz | 2021-08-02 | 1 | 0 | 0 | kk_043–kk_043 |
| 8 | https://www.gov.kz/memleket/entities/enbek/press/news/details/1293268?lang=kk | Ministry of Labour and Social Protection (Еңбек министрлігі) via gov.kz | 2026-09-17 | 3 | 0 | 0 | kk_044–kk_046 |
| 9 | https://www.gov.kz/situations/236/1663?lang=kk | gov.kz life-situation page (fingramota memo on fraud prevention) | 2025-01-01 (low) | 1 | 0 | 0 | kk_047–kk_047 |
| 10 | https://www.gov.kz/situations/733/intro?lang=kk | gov.kz life-situation page 'Өзіңізді алаяқтардан қалай қорғауға болады' | 2025-01-01 (low) | 1 | 0 | 0 | kk_048–kk_048 |
| 11 | https://www.bcc.kz/kz/about/press-center/fraud-protection-guide/ | Bank CenterCredit (BCC) | 2025-10-08 (medium) | 3 | 0 | 0 | kk_049–kk_051 |
| 12 | https://inbusiness.kz/kz/last/iim-kazakstandyktardyn-kandaj-habarlama-alyp-zhatkanyn-tusindirdi | Inbusiness.kz (citing Polisia.kz / MVD) | 2022-08-13 | 0 | 6 | 0 | kk_052–kk_110 |
| 13 | https://live.fingramota.kz/kk/post/zhal-nsaular-telefon-alayataryny-zha-ulyy | Fingramota.kz (ARDFM financial literacy portal) | 2022-01-17 (medium) | 4 | 1 | 0 | kk_057–kk_102 |
| 14 | https://okg.kz/post?id=38843&slug=telefon-alayaqtary | OKG.KZ ('Оңтүстік Қазақстан' newspaper), quoting a citizen's Facebook post | 2025-02-03 (medium) | 7 | 0 | 0 | kk_061–kk_067 |
| 15 | https://baribar.kz/253649/telefon-alaya-tary-andaj-s-zdermen-aldajdy-iim-t-sindirdi/ | Baribar.kz (citing MVD) | 2025-09-12 | 6 | 0 | 0 | kk_068–kk_073 |
| 16 | https://qaz.ulysmedia.kz/news/13719-politsiia-kazakstanda-alaiatar-kobinese-kandai-sozdi-kop-koldanatynyn-eskertti/ | Ulysmedia.kz (citing MVD) | 2024-03-21 | 6 | 0 | 0 | kk_074–kk_079 |
| 17 | https://alatauaraiy.kz/2026/08/alayaktar-telefonnyn-ar-zhagynda/ | Alatau Araiy newspaper | 2026-08-25 | 3 | 0 | 0 | kk_080–kk_082 |
| 18 | https://informburo.kz/kaz/newskaz/ulttyq-bank-qyzmetkerimin-telefon-alayaqtarynyn-zana-sxemasy-paida-boldy | Informburo.kz (citing National Bank of Kazakhstan) | 2022-07-27 | 3 | 0 | 0 | kk_083–kk_085 |
| 19 | https://sputnik.kz/20260727/zhylu-eseptegishin-tirkeu-kerek-politsiya-alayaqtardyn-zhana-tasili-turaly-eskertti-65251334.html | Sputnik Kazakhstan (citing MVD) | 2026-07-27 | 1 | 0 | 0 | kk_086–kk_086 |
| 20 | https://elordainfo.kz/article/bank-te-policiia-da-suramaidy-kirister-komiteti-sms-kodqa-qatysty-manyzdy-eskertu-zasady | Elordainfo.kz (citing State Revenue Committee) | 2026-09-08 | 2 | 1 | 0 | kk_087–kk_100 |
| 21 | https://www.bcc.kz/kz/about/press-center/main-schemes-used-by-scammers/ | Bank CenterCredit (BCC) | 2026-09-24 | 0 | 5 | 6 | kk_090–kk_130 |
| 22 | https://nationalbank.kz/kz/news/informacionnye-soobshcheniya/20601 | National Bank of Kazakhstan | 2026-11-06 | 0 | 1 | 0 | kk_096–kk_096 |
| 23 | https://www.gov.kz/memleket/entities/enbek/press/news/details/801295?lang=kk | Ministry of Labour and Social Protection via gov.kz | 2024-06-28 | 0 | 1 | 1 | kk_097–kk_131 |
| 24 | https://www.astana-akshamy.kz/news/kommunaldyq-qyzmet-atyn-zamylgan-alaiaqtardan-saq-bolynyz | Astana Aqshamy (citing police) | 2026-07-27 | 0 | 2 | 0 | kk_098–kk_099 |
| 25 | https://informburo.kz/kaz/newskaz/sms-xabarlama-kod-ziberu-ulttyq-bank-zana-alaiaqtyq-sxemalar-paida-bolganyn-eskertti | Informburo.kz (quoting National Bank) | 2025-06-19 | 0 | 1 | 0 | kk_101–kk_101 |
| 26 | https://inbusiness.kz/kz/last/sms-kodty-ajtpanyz-onlajn-zhetkizilimdegi-alayaktyktyn-zhana-tasili | Inbusiness.kz (citing Prosecutor General's Office) | 2026-07-03 | 0 | 1 | 0 | kk_103–kk_103 |
| 27 | https://www.gov.kz/org/mvd-abay/press/news/details/1279402?lang=kk | Abai Region Police Department via gov.kz | 2026-08-25 | 0 | 1 | 0 | kk_104–kk_104 |
| 28 | https://www.gov.kz/memleket/entities/vko-ekonomika/press/news/details/1139359 | Prosecutor General's Office committee, via East Kazakhstan akimat on gov.kz | 2026-01-12 | 0 | 1 | 0 | kk_105–kk_105 |
| 29 | https://guide.kaspi.kz/client/kz/app/security/q15367 | Kaspi.kz (Kaspi Гид) | 2024-12-11 (medium) | 0 | 3 | 0 | kk_111–kk_113 |
| 30 | https://guide.kaspi.kz/client/kz/app/security/q17142 | Kaspi.kz (Kaspi Гид) | 2026-08-03 (medium) | 0 | 2 | 0 | kk_114–kk_115 |
| 31 | https://guide.kaspi.kz/client/kz/app/security/q16397 | Kaspi.kz (Kaspi Гид) | 2026-05-19 (medium) | 0 | 4 | 0 | kk_116–kk_119 |
| 32 | https://guide.kaspi.kz/client/kz/app/security/q16398 | Kaspi.kz (Kaspi Гид) | 2026-05-19 (medium) | 0 | 1 | 0 | kk_120–kk_120 |
| 33 | https://guide.kaspi.kz/client/kz/app/security/q19289 | Kaspi.kz (Kaspi Гид) | 2026-07-17 (medium) | 0 | 1 | 0 | kk_121–kk_121 |
| 34 | https://guide.kaspi.kz/client/kz/app/security/q15355 | Kaspi.kz (Kaspi Гид) | 2021-11-15 (medium) | 0 | 1 | 0 | kk_122–kk_122 |
| 35 | https://guide.kaspi.kz/client/kz/app/security/q18490 | Kaspi.kz (Kaspi Гид) | 2026-05-21 (medium) | 0 | 1 | 0 | kk_123–kk_123 |
| 36 | https://guide.kaspi.kz/client/kz/app/message/general/q12617 | Kaspi.kz (Kaspi Гид) | 2026-05-22 (medium) | 0 | 1 | 0 | kk_124–kk_124 |
| 37 | https://kapital.kz/kk/gosudarstvo/146945/astanada-halyk-bank-pen-beeline-atynan-fishing-taratkhan-top-kholgha-tuesti.html | Kapital.kz (citing Financial Monitoring Agency) | 2026-04-14 | 0 | 0 | 1 | kk_132–kk_132 |

## Problems and caveats (read before reporting results)
1. **Almost no verbatim Kazakh SMS or messenger scam texts exist on public pages.** Kazakh-language outlets and agencies mostly paraphrase scams. What they do quote is short scammer *phrases*, usually lists of "words that should alarm you" (ARDFM, BCC, Otbasy, MVD via Baribar/Ulysmedia, Fingramota). So 76 of the 83 verbatim scam items are `call_quote`. Many are single sentences or fragments, not full messages. Only 1 scam item is `sms` (kk_048, and its channel is a guess) and 4 are `messenger`.
2. **Many quotes are written by the agency or journalist, not recorded from real calls.** Some are probably the agency's own translation of a Russian list (the BCC, ARDFM and Otbasy items all have RU twins). The real call or SMS was likely in Russian. Only okg.kz (kk_061–062) reproduces a real call reported by a citizen, and even there the citizen says the caller spoke "орысшалап" (in a Russian manner).
3. **Legit set is mostly official warning or help text (`kind=web`, 35 items), not real SMS.** Real Kazakh SMS texts appear only once: the 5 MVD/Kcell warning SMS (kk_052–056, 2022). No public page gave a verbatim Kazakh OTP SMS ("Кодты ешкімге айтпаңыз"). egov.kz/cms pages now redirect to the homepage, even in BrowserOS neo. The best hard negatives are kk_114–119 (Kaspi: an in-app block notice, the bank *does* call about suspicious operations, courier calls, loan manager contact) and kk_102 (a victim's safe reply).
4. **No keyboard-Kazakh (kbd=true) examples were found** on any public page I checked.
5. **Dates:** 11 items have date_confidence=low. These are the Otbasy page (undated, estimated 2026-01-01), the gov.kz life-situation pages (estimated 2025-01-01) and kk_085. For BCC fraud-protection-guide and Kaspi Гид, the date is the page's "Жаңартылды" (updated) date (medium). There are no items from 2023.
6. **Semantic near-duplicates are kept on purpose.** Several sources list the same idea in different wording, e.g. "…ешкімге айтпаңыз" ×4 and "…қауіпсіз шотқа аударыңыз" ×3. No two strings are identical, and a difflib check found no repeats above 0.85 similarity. Consider grouping them by `scheme` when splitting.
7. kk_085 ("Мемлекеттік бағдарламамен үй алып беремін") is the title of a related-article link on the Informburo page, so its real date is unknown.

## Pages checked with nothing usable (verbatim Kazakh)
egov.kz/cms/kk/* (redirect, empty), kolesa.kz kz eGov-SMS article (JS only), kaz.inform.kz (JS only), adcb.com/kz (JS only), nationalbank.kz kz 16819/20002 (only scheme names), ARDFM 406054/540611/1229339/1027618 (paraphrase or pyramid terms), Labour Ministry proactive-SMS pages 1045753/1045890/1082503/647592 (no SMS text), kapital.kz БЖЗҚ/eGov articles, 24.kz NB/Halyk+ articles, inbusiness WhatsApp/scheme articles, Abai police SMS-bombing (paraphrase), tengrinews/bizmedia 1414 articles (Russian only, no SMS text).
