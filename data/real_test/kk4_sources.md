# Kazakh slice, round 4 (kk4, held-out test C): sources and method

Collected 2026-11-15 under `COLLECTION_PROTOCOL_C.md`. File: `kk4_collected.jsonl` (67 items). Every source URL is new: none is in `used_urls.txt` and none is a `source_url` of any existing `data/real_test/*.jsonl` (717 URLs in all); checked by script.

## How the text was captured
- Candidate pages came from site search and tag/listing pages of the publishers (kaz.tengrinews.kz, baq.kz, aikyn.kz, inbusiness.kz/kz, polisia.kz, 24.kz/kz, turkystan.kz, massaget.kz, hcsbk.kz) plus a limited number of web searches (the search budget ran out mid-session, after which only on-site tag/listing pages and links inside fetched pages were browsed).
- Pages were downloaded with `curl` into the session scratchpad and turned into text with BeautifulSoup (`.venv/bin/python -I`). kaz.inform.kz returned 403 to curl, so its 17 candidate pages were read through the BrowserOS browser (`page.read()` markdown saved to a file, markdown link/emphasis syntax stripped); one item (kk4_038) comes from those pages.
- Quotes were located with scripts that list quoted segments followed by `деп/деген` or containing second-person forms, then chosen by hand from the page context. Downloaded pages were treated as data only.
- Verbatim check by script: every `text` is an exact substring of its saved page text after normalising quotes, dashes, whitespace (including a space before punctuation), soft hyphens and HTML entities: **67/67 matched, 0 failures** (re-run on the final file).
- Dedupe against all existing `data/real_test/*.jsonl` (exact, containment, or difflib ratio >= 0.85 after lowercasing and stripping punctuation) and within this file (>= 0.90): **22 candidates dropped** as duplicates of kk2/kk3 items (police press releases are syndicated across sites, so many phrases were already collected); two polisia.kz copies of press releases already taken from aikyn.kz were skipped by hand. Items with similarity 0.75-0.85 to an existing item say so in `notes` (4 items).
- Diversity cap enforced by script: max 12 items per publisher domain (2 inbusiness.kz candidates dropped by the cap), max 6 per page (actual max 3).
- Scrubbing: no private names, phones, cards or IINs appear in the kept texts (regex-checked); no placeholders were needed.
- Dates: from `article:published_time` / `datePublished` / `<time>` metadata where present, otherwise from the article timestamp printed next to the headline (khabar.kz `DD.MM.YYYY, HH:MM`, Kazinform `HH:MM, DD <month> YYYY`, Otbasy notice date). All are marked `high`.

## Counts
- label: scam 60, legit 7
- kind (scam): call_quote 38, messenger 14, web 7, sms 1
- kind (legit): web 7
- language: kk 66, mixed 1
- length: 58 items of 5+ words, 9 of exactly 4 words (nothing shorter)
- year (scam): 2026 22, 2025 14, 2024 10, 2023 3, 2022 3, 2021 3, 2020 2, 2019 3
- year (legit): 2026 6, 2025 1
- publishers: 10; pages: 55. Per publisher: Inbusiness.kz (kz) 12, Tengrinews (kaz.tengrinews.kz) 11, Polisia.kz (MVD media centre) 10, Baq.kz 7, Aikyn.kz 7, 24KZ (24.kz/kz) 6, Otbasy Bank (hcsbk.kz) client notice 6, Khabar (khabar.kz/kk) 4, Massaget.kz 3, Kazinform (kaz.inform.kz) 1
- scam schemes: 39 distinct; top: safe_account 6, fake_bank_security 4, pension_withdrawal_intermediary 4, fake_law_enforcement 3, fake_cyberpolice 3, whatsapp_takeover_link 2, fake_financial_monitoring 2, business_phishing_email 2, fake_charity 2, investment_fraud 2
- `typical_example` (phrase lists in warnings rather than a single victim's message): 16

## Caveats
- Legit is thin and one-register: 7 items, 6 of them Otbasy Bank website notices (hcsbk.kz "Құрметті клиенттер!" pages, body only, the greeting heading and date are not part of the text) plus 1 eGov service-page notice quoted by inbusiness.kz. No new verbatim Kazakh OTP, transaction or 1414 SMS text was found. Three Otbasy notices share a "holiday payment crediting" template (pairwise similarity < 0.90, so kept).
- Only 1 item is `mixed` (Otbasy notice with Russian `АО` bank names). Kazakh-Russian mixed scam texts did not turn up on these pages; Latin brand names (iPhone, GPA, LIV Hospital, WhatsApp) were not counted as mixing.
- Many scam items are short scammer lines embedded in news text (9 items are exactly 4 words) or content-level quotes introduced by `деген мазмұнда/сарында/сипатта` (flagged in notes where relevant). 16 are `typical_example` phrases from police/regulator warnings.
- `call_quote` is also used for things fraudsters said in person or where the channel is not stated (kk4_041, kk4_044, kk4_047, kk4_052, kk4_056); see notes. Emails are tagged `web` (kk4_012, kk4_013, kk4_054, kk4_059).
- kk4_048: the original WhatsApp message starts with "Банктегі лимитім бітіп қалып тұр еді." but the page splits that sentence from the rest with metadata, so only the contiguous second part is kept.
- kk4_017/018 (khabar.kz, 2019) are the oldest; publisher spread is uneven (inbusiness.kz and kaz.tengrinews.kz near the cap). turkystan.kz (68 pages) and the POLICE_of_KZ Telegram preview gave no new verbatim quotes.
- The web-search budget was exhausted during the session; the rest of discovery used only on-site tag/listing pages and links found in fetched pages.

## Sources used
| # | Source URL | Publisher | Date (confidence) | scam | legit | ids | what was taken |
|---|---|---|---|---|---|---|---|
| 1 | https://kaz.tengrinews.kz/kazakhstan_news/rekvizitterd-jber-alayaktar-kazakstandyiktarga-arptesternn-382521/ | Tengrinews (kaz.tengrinews.kz) | 2026-10-09 (high) | 1 | 0 | kk4_001 | boss_colleague_impersonation |
| 2 | https://kaz.tengrinews.kz/tengri-health/kazakstandyiktar-dargerge-bargannan-keyn-kudkt-konyiraular-372687/ | Tengrinews (kaz.tengrinews.kz) | 2026-04-02 (high) | 1 | 0 | kk4_002 | fake_doctor_sms_code |
| 3 | https://kaz.tengrinews.kz/article/juzdegen-million-tengenn-whatsapp-alayaktyigyi-ma-tauar-2321/ | Tengrinews (kaz.tengrinews.kz) | 2026-11-13 (high) | 1 | 0 | kk4_003 | fake_car_import |
| 4 | https://kaz.tengrinews.kz/kazakhstan_news/eshbr-messendjer-tolyik-kaupsz-emes-politsiya-383075/ | Tengrinews (kaz.tengrinews.kz) | 2026-10-20 (high) | 1 | 0 | kk4_004 | whatsapp_takeover_link |
| 5 | https://baq.kz/alayaqtar-shotty-qalay-bugattaydy-331111/ | Baq.kz | 2024-05-10 (high) | 1 | 0 | kk4_005 | fake_bailiff |
| 6 | https://baq.kz/elordada-internet-alayaqtyqpen-kures-qalay-zhurip-zhatyr-200002108/ | Baq.kz | 2024-11-23 (high) | 1 | 0 | kk4_006 | safe_account |
| 7 | https://baq.kz/internet-alayaqtyqtyn-zhana-adisteri-odan-qalay-qorganamyz-200001343/ | Baq.kz | 2024-11-13 (high) | 1 | 0 | kk4_007 | fake_buyer_delivery_link |
| 8 | https://baq.kz/telefon-arqyly-qalay-tonalasyz-alayaqtyn-aylasynan-saqtanu-zholdary-200018740/ | Baq.kz | 2025-08-05 (high) | 2 | 0 | kk4_008–kk4_009 (2) | fake_law_enforcement; remote_access_app |
| 9 | https://baq.kz/alayaqtyqtyn-zhana-shemasy-qma-azamattardy-saq-boluga-shaqyrdy-200021447/ | Baq.kz | 2025-09-17 (high) | 1 | 0 | kk4_010 | fake_financial_monitoring |
| 10 | https://baq.kz/internet-alayaqtyq-nege-kobeyip-ketti-200008540/ | Baq.kz | 2025-02-27 (high) | 1 | 0 | kk4_011 | fake_law_enforcement |
| 11 | https://kaz.tengrinews.kz/money/internet-alayaktyik-bizneske-tonetn-tsifrlyik-kaup-katerler-363355/ | Tengrinews (kaz.tengrinews.kz) | 2024-10-31 (high) | 3 | 0 | kk4_012–kk4_028 (3) | business_phishing_email; fake_law_enforcement |
| 12 | https://kaz.tengrinews.kz/article/komektesnzder-uakyit-tyigyiz-kayyiryimdyilyik-jasaymyin-dep-2299/ | Tengrinews (kaz.tengrinews.kz) | 2026-11-06 (high) | 1 | 0 | kk4_014 | fake_charity |
| 13 | https://massaget.kz/news/szge-gul-jberd-alayaktar-WhatsApp-akkauntyin-buzudyin-jana-117666/ | Massaget.kz | 2024-10-07 (high) | 2 | 0 | kk4_015–kk4_016 (2) | whatsapp_takeover_link; whatsapp_takeover_sms_code |
| 14 | https://khabar.kz/kk/news/114948-bank-atyn-burkengen-alayaktar-kazakstandyktardy-aldap-zhur | Khabar (khabar.kz/kk) | 2019-08-28 (high) | 2 | 0 | kk4_017–kk4_018 (2) | fake_bank_security |
| 15 | https://massaget.kz/news/kma-atyinan-habarlasatyin-alayaktar-payda-bolgan-shugyil-131020/ | Massaget.kz | 2025-10-17 (high) | 1 | 0 | kk4_019 | fake_financial_monitoring |
| 16 | https://inbusiness.kz/kz/news/sms-kod-ta-kazhet-emes-alayaktar-zhana-taktikaga-koshti | Inbusiness.kz (kz) | 2025-06-18 (high) | 1 | 1 | kk4_020–kk4_021 (2) | egov_fine_notice; fake_prewarning_sms |
| 17 | https://polisia.kz/alayaqtar-cyberpol-tobynyng-zhedel-uakiline-qongyrau-shaldy/ | Polisia.kz (MVD media centre) | 2024-08-22 (high) | 2 | 0 | kk4_022–kk4_023 (2) | investment_fraud |
| 18 | https://polisia.kz/belgisiz-qongyraulargha-senbengiz-politsiya-turghyndardy-qyraghylyqqa-shaqyrady/ | Polisia.kz (MVD media centre) | 2025-04-25 (high) | 1 | 0 | kk4_024 | fake_anti_fraud_officer |
| 19 | https://polisia.kz/qyzylordalyq-politsejler-turghyngha-qongyrau-shalyp-aqshasyn-zhymqyrghan-alayaqty-qolgha-tusirdi/ | Polisia.kz (MVD media centre) | 2023-12-25 (high) | 3 | 0 | kk4_025–kk4_027 (3) | fake_national_bank; safe_account |
| 20 | https://inbusiness.kz/kz/news/bzhzk-karazhatyn-maksatsyz-zhumsau-faktileri-bojynsha-atyrauda-200-mlrd-tengelik-shema-ashkerelendi | Inbusiness.kz (kz) | 2025-09-16 (high) | 1 | 0 | kk4_029 | pension_withdrawal_intermediary |
| 21 | https://inbusiness.kz/kz/news/3-pater-zher-telimi-5-kolik-elordalyk-erli-zajypty-ulynyn-emine-zhinagan-akshany-zheke-maksatta-pajdalangan | Inbusiness.kz (kz) | 2025-07-29 (high) | 1 | 0 | kk4_030 | fake_charity |
| 22 | https://aikyn.kz/143255/petropavl-turgyny-zhalgan-bank-kyzmet | Aikyn.kz | 2021-06-04 (high) | 1 | 0 | kk4_031 | fake_bank_security |
| 23 | https://khabar.kz/kk/news/okiga/169957-akhtobede-bank-khyzmetkeri-alaiakhtykhtyn-aldyn-aldy | Khabar (khabar.kz/kk) | 2025-02-25 (high) | 1 | 0 | kk4_032 | fake_bank_security |
| 24 | https://khabar.kz/kk/news/okiga/190128-alaiakhtar-endi-neke-merzimin-uzartuga-koshti | Khabar (khabar.kz/kk) | 2026-09-02 (high) | 1 | 0 | kk4_033 | fake_marriage_renewal_link |
| 25 | https://24.kz/kz/zha-aly-tar/kogam/755741-karagandylyk-kasipker-alaaktardan-aman-kaldy | 24KZ (24.kz/kz) | 2026-02-25 (high) | 3 | 0 | kk4_034–kk4_036 (3) | fake_cyberpolice |
| 26 | https://24.kz/kz/zha-aly-tar/kogam/795795-petropavl-policeji-zejnetkerdin-2-7-mln-tengesin-alaaktardan-saktap-kaldy | 24KZ (24.kz/kz) | 2026-10-01 (high) | 1 | 0 | kk4_037 | safe_account |
| 27 | https://kaz.inform.kz/news/alayaktar-halikti-sotka-katisu-turali-zhalgan-habarlama-arkili-alday-bastadi-politsiya-ad612b/ | Kazinform (kaz.inform.kz) | 2026-04-05 (high) | 1 | 0 | kk4_038 | fake_court_summons |
| 28 | https://inbusiness.kz/kz/last/internet-alayak-pavlodarlyktyn-shotyndagy-40-mln-tengeni-koldy-kyldy | Inbusiness.kz (kz) | 2022-04-21 (high) | 1 | 0 | kk4_039 | safe_account |
| 29 | https://inbusiness.kz/kz/last/damu-kory-halykty-abaj-boluga-shakyrdy | Inbusiness.kz (kz) | 2019-12-25 (high) | 1 | 0 | kk4_040 | fake_damu_investment |
| 30 | https://inbusiness.kz/kz/last/shymkentte-500-ge-zhuyk-adamdy-aldagan-alayak-ajelder-ustaldy | Inbusiness.kz (kz) | 2022-01-27 (high) | 1 | 0 | kk4_041 | loan_split_scheme |
| 31 | https://inbusiness.kz/kz/last/turkistan-oblysynda-bes-adamnyn-atynan-nesie-rasimdegen-alayak-ustaldy | Inbusiness.kz (kz) | 2022-05-17 (high) | 1 | 0 | kk4_042 | fake_telecom_employee |
| 32 | https://inbusiness.kz/kz/last/580-myn-tenge-uttynyz-alayaktyktyn-zhana-turi-pajda-boldy | Inbusiness.kz (kz) | 2021-05-26 (high) | 1 | 0 | kk4_043 | fake_grant_prize |
| 33 | https://inbusiness.kz/kz/news/bes-zhyl-bojy-turgyndardyn-karzhysyn-kaltasyna-baskan-alayak-sottaldy | Inbusiness.kz (kz) | 2020-11-13 (high) | 2 | 0 | kk4_044–kk4_047 (2) | fake_loan_help; fake_property_deal |
| 34 | https://aikyn.kz/294351/kuyeuin-nin--whatsapp-tag-y-hatyn-ok-ug-a-komektesemin--k-azak-standa-alayak-tyk-tyn--zhan-a-turi-payda-boldy | Aikyn.kz | 2025-11-14 (high) | 1 | 0 | kk4_045 | whatsapp_spy_service |
| 35 | https://inbusiness.kz/kz/last/bank-alayaktardan-korgaj-almajdy | Inbusiness.kz (kz) | 2021-12-02 (high) | 1 | 0 | kk4_046 | safe_account |
| 36 | https://aikyn.kz/295327/internet-ark-yly-zhasalg-an-alayak-tyk | Aikyn.kz | 2025-12-04 (high) | 1 | 0 | kk4_048 | hacked_account_loan_request |
| 37 | https://aikyn.kz/293186/salyk--deklaraciyasynyn--merzimi-otip-ketken--alayak-tar-zhan-a-ayla-oylap-tapty | Aikyn.kz | 2025-10-25 (high) | 1 | 0 | kk4_049 | fake_tax_declaration |
| 38 | https://aikyn.kz/296946/600-myn--ten-gege-deyin-tabys-tabasyn--bk-o-da-otirik-onlayn-kurs-satk-andar-ak-shasyn-k-aytardy | Aikyn.kz | 2026-01-05 (high) | 1 | 0 | kk4_050 | fake_online_course |
| 39 | https://aikyn.kz/303568/belgisiz-tu-lg-alardyn--telefon-ark-yly-bergen-nu-sk-aularyn-oryndaman-yz | Aikyn.kz | 2026-05-12 (high) | 1 | 0 | kk4_051 | fake_esalyq_app |
| 40 | https://polisia.kz/gpa-korsetkishin-koterip-beremin-astanada-alayaqtyq-zhasaghan-kudikti-ustaldy/ | Polisia.kz (MVD media centre) | 2026-06-19 (high) | 1 | 0 | kk4_052 | fake_university_fixer |
| 41 | https://kaz.tengrinews.kz/kazakhstan_news/almatyi-oblyisyinda-zeynetker-alayaktar-kesrnen-paternen-373558/ | Tengrinews (kaz.tengrinews.kz) | 2026-04-24 (high) | 1 | 0 | kk4_053 | real_estate_courier_scheme |
| 42 | https://kaz.tengrinews.kz/kazakhstan_news/sz-iphone-satyip-aldyinyiz-kazakstandyiktarga-jana-shema-374376/ | Tengrinews (kaz.tengrinews.kz) | 2026-05-13 (high) | 1 | 0 | kk4_054 | fake_purchase_email |
| 43 | https://kaz.tengrinews.kz/article/azenizge-bred-pitt-xabarlasuy-mumkin-qazaqstandyqtar-zana-zi-1762/ | Tengrinews (kaz.tengrinews.kz) | 2026-04-08 (high) | 1 | 0 | kk4_055 | pressure_urgency |
| 44 | https://24.kz/kz/zha-aly-tar/kogam/792474-arzan-baspana-alyp-beremin-oskemendik-zigit-25-adamdy-san-soktyrdy | 24KZ (24.kz/kz) | 2026-09-17 (high) | 1 | 0 | kk4_056 | fake_housing_help |
| 45 | https://24.kz/kz/zha-aly-tar/o-i-a/768683-zejnetakynyzdy-sygaryp-beremin-astanalyk-turgyn-alaakka-aldanyp-kalgan | 24KZ (24.kz/kz) | 2026-05-15 (high) | 1 | 0 | kk4_057 | pension_withdrawal_intermediary |
| 46 | https://polisia.kz/astanada-iri-kolemde-alayaqtyq-zhasaghan-azamat-ustaldy/ | Polisia.kz (MVD media centre) | 2026-05-04 (high) | 1 | 0 | kk4_058 | fake_national_bank |
| 47 | https://aikyn.kz/294677/internet-alayak-tardan-k-alay-sak-tanu-kerek | Aikyn.kz | 2025-11-21 (high) | 1 | 0 | kk4_059 | fake_tax_email |
| 48 | https://polisia.kz/aqtobede-20-dan-astam-adam-alayaqtyng-qurbany-boldy/ | Polisia.kz (MVD media centre) | 2026-04-01 (high) | 1 | 0 | kk4_060 | pension_withdrawal_intermediary |
| 49 | https://polisia.kz/elordada-zejnetaqy-qarazhatyn-sheship-berudi-syltau-etken-alayaqtyqqa-kudikti-ustaldy/ | Polisia.kz (MVD media centre) | 2026-05-15 (high) | 1 | 0 | kk4_061 | pension_withdrawal_intermediary |
| 50 | https://hcsbk.kz/news/press_relize/uvazhaemye-klienty-zachislenie-platezhey-26-oktyabrya/ | Otbasy Bank (hcsbk.kz) client notice | 2026-10-22 (high) | 0 | 1 | kk4_062 | bank_service_notice |
| 51 | https://hcsbk.kz/news/press_relize/uvazhaemye-klienty-20260302/ | Otbasy Bank (hcsbk.kz) client notice | 2026-02-27 (high) | 0 | 1 | kk4_063 | bank_service_notice |
| 52 | https://hcsbk.kz/news/press_relize/uvazhaemye-klienty-sz-582-2026/ | Otbasy Bank (hcsbk.kz) client notice | 2026-01-08 (high) | 0 | 1 | kk4_064 | bank_service_notice |
| 53 | https://hcsbk.kz/news/press_relize/uvazhaemye-klienty-tehraboty-01-2026/ | Otbasy Bank (hcsbk.kz) client notice | 2026-01-05 (high) | 0 | 1 | kk4_065 | bank_service_notice |
| 54 | https://hcsbk.kz/news/press_relize/uvazhaemye-klienty-may-2026/ | Otbasy Bank (hcsbk.kz) client notice | 2026-04-29 (high) | 0 | 1 | kk4_066 | bank_service_notice |
| 55 | https://hcsbk.kz/news/press_relize/uvazhaemye-klienty-2026-03-22/ | Otbasy Bank (hcsbk.kz) client notice | 2026-03-17 (high) | 0 | 1 | kk4_067 | bank_service_notice |
