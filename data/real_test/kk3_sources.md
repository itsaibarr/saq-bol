# Kazakh slice, round 3 (kk3, held-out test B): sources and method

Collected 2026-11-15. File: `kk3_collected.jsonl` (174 items). Every source URL is new: none is in `used_urls.txt` (426 URLs from earlier rounds); checked by script.

## How the text was captured
- Pages were downloaded with `curl` (egemen.kz, aikyn.kz, ult.kz, qamshy.kz, khabar.kz, massaget.kz, zhasalash.kz, 24.kz, gov.kz, hcsbk.kz, kapital.kz, nationalbank.kz, kgd.gov.kz and others) or, where curl got 403 (kazinform), read through the BrowserOS browser. Each page was turned into plain text locally and items were copied from that text, never from an AI summary.
- A script checked that every item (before PII scrubbing) appears word for word in its saved page text after whitespace/quote/dash/soft-hyphen normalisation: **174/174 matched, 0 failures**. Saved page texts are in the session scratchpad (`pages/k3a_*`, `k3b_*`, `k3c_*`), not in this folder.
- egemen.kz pages contain soft hyphens (U+00AD); they were removed from `text`. Source spelling is otherwise kept (e.g. `ресімделді`).
- Filters: items under 4 words dropped (4); legit notice intro lines ending in ":" dropped (7, not whole messages); one "деген сарында" deepfake example dropped (illustrative, not a real message).
- Deduplicated (case/punctuation-insensitive) against all existing `data/real_test/*.jsonl` texts and within this file: 3 exact duplicates and 1 near-duplicate (difflib >= 0.90) dropped at merge, plus 5 exact duplicates and 3 template near-copies dropped during collection. Items with similarity 0.80-0.90 to an existing item say so in `notes`.
- Scrubbing: names -> [NAME]. No phones, cards or IINs appeared (regex-checked).
- Items the article introduces with "деген мазмұнда/сарында" (content-level quote, possibly condensed) are flagged in `notes`.

## Counts
- label: scam 137, legit 37
- kind (scam): call_quote 85, messenger 35, web 11, sms 6
- kind (legit): web 35, call_quote 2
- language: kk 168, mixed 6
- length: 146 items of 5+ words, 28 of exactly 4 words
- year (scam): 2026 50, 2025 51, 2024 6, 2023 1, 2022 6, 2021 17, 2020 6
- year (legit): 2026 13, 2025 15, 2024 3, 2023 1, 2022 3, 2021 2
- scam schemes: 58 distinct; top: fake_bank_security 20, safe_account 10, relative_in_trouble 6, sms_code_theft 6, money_mule_recruitment 5, investment_platform 4, fake_favours_promise 4, child_device_takeover 4, investment_fraud 3, fake_drivers_license 3, pressure_urgency 3, fake_military_summons 3

## Caveats
- Legit is weak on SMS. Almost all legit items are website service notices from Otbasy Bank (hcsbk.kz "Құрметті клиенттер!" pages), plus 2 tax-portal system messages and 2 real bank-employee call questions. No new verbatim Kazakh OTP, transaction or 1414 SMS text was found: earlier rounds took what is public (egov.kz/cms/kk/news/* and guide.kaspi.kz/client/kz/app/security/* are in the used list; the other Kaspi /kz SMS guide pages list sender names, not message texts). So legit here is one publisher and one register.
- 15 scam items from 2021 come from one Massaget page (2021-03-04); its bank-call dialogues are described as real cases with names changed.
- Many call_quote items are short scammer lines (4-6 words) embedded in news reports, not whole turns.
- 4 recruiter lines (khabar.kz, 2026-10-10) were said face to face and are tagged call_quote; see notes.

## Sources used
| # | Source URL | Publisher | Date (confidence) | scam | legit | ids |
|---|---|---|---|---|---|---|
| 1 | https://ult.kz/kz/post/alaiaqtar-paterin-satqyzbaq-bolgan-aqtobede-aiel-8-mln-tengesinen-aiyrylyp-qala-zazdady | Ult.kz (Ұлт порталы) | 2026-07-29 (high) | 1 | 0 | kk3_001 |
| 2 | https://ult.kz/kz/post/balam-zol-apatyna-tusti-alaiaqtar-endi-tuystyn-dauysyn-zi-arqyly-ainytpai-salyp-zur | Ult.kz (Ұлт порталы) | 2026-08-19 (high) | 1 | 0 | kk3_002 |
| 3 | https://ult.kz/kz/post/instagram-arqyly-154-adamdy-aldagan-qyzylordalyq-sottaldy | Ult.kz (Ұлт порталы) | 2026-06-02 (high) | 1 | 0 | kk3_003 |
| 4 | https://ult.kz/kz/post/kartandy-bersen-aqsa-toleimin-oralda-dropperler-zelisin-qurgan-kudikti-ustaldy | Ult.kz (Ұлт порталы) | 2026-08-27 (high) | 1 | 0 | kk3_004 |
| 5 | https://aikyn.kz/292688/balam-ushin-b-rine-bardym--alayak-tyn--arbauyna-tusken-ana-k-omak-ty-k-aryzdan-k-alay-k-u-tyldy | Aikyn.kz | 2025-10-16 (high) | 1 | 0 | kk3_005 |
| 6 | https://aikyn.kz/295759/ak-shan-dy-kobeytip--p-ter--peremin--dep-aldag-an-alayak---yel-u-staldy | Aikyn.kz | 2025-12-12 (high) | 2 | 0 | kk3_006–kk3_007 (2) |
| 7 | https://aikyn.kz/311211/beytanys-nomirden--s-lem--dep-zhazsa--zhauap-bermen-iz--alayak-tardyn--zhan-a-t-silge-koshti | Aikyn.kz | 2026-10-02 (high) | 3 | 0 | kk3_008–kk3_010 (3) |
| 8 | https://egemen.kz/news/article400178-sizge-aqshany-qatelesip-audaryppyn-alayaqtardynh-dganha-tasilinen-qorghanudynh-d | Egemen Qazaqstan (egemen.kz) | 2025-11-27 (high) | 1 | 0 | kk3_011 |
| 9 | https://egemen.kz/news/article400511-alayaqtar-ustaldy | Egemen Qazaqstan (egemen.kz) | 2025-12-02 (high) | 4 | 0 | kk3_012–kk3_015 (4) |
| 10 | https://egemen.kz/news/article402091-balalar-quqyqtaryn-qorghau-komiteti-dganha-alayaqtyq-turaly-eskertti | Egemen Qazaqstan (egemen.kz) | 2025-12-20 (high) | 1 | 0 | kk3_016 |
| 11 | https://egemen.kz/news/article405186-alayaqtar-adette-qanday-soz-tirkesterin-qoldanady | Egemen Qazaqstan (egemen.kz) | 2026-01-27 (high) | 2 | 0 | kk3_017–kk3_018 (2) |
| 12 | https://egemen.kz/news/article406975-ulttyq-bank-eskertedi-tolem-kartasyn-bughattau-arqyly-dgasalatyn-alayaqtyq-kobey | Egemen Qazaqstan (egemen.kz) | 2026-02-17 (high) | 1 | 0 | kk3_019 |
| 13 | https://egemen.kz/news/article409908-baspanagha-qatysty-dganha-alayaqtyq-skhema-iim-qazaqstandyqtargha-eskertu-dgasad | Egemen Qazaqstan (egemen.kz) | 2026-03-28 (high) | 1 | 0 | kk3_020 |
| 14 | https://egemen.kz/news/article410597-politsiya-investitsiyalyq-alayaqtyqtynh-qauipti-skhemalary-turaly-eskertti | Egemen Qazaqstan (egemen.kz) | 2026-04-08 (high) | 1 | 0 | kk3_021 |
| 15 | https://egemen.kz/news/article417893-aqtobe-turghyny-zhurgizushi-kualigin-satyp-alamyn-dep-alayaqqa-aldanyp-qaldy | Egemen Qazaqstan (egemen.kz) | 2026-07-24 (high) | 1 | 0 | kk3_022 |
| 16 | https://egemen.kz/news/egov-atynan-zhasalatyn-alayaqtyq | Egemen Qazaqstan (egemen.kz) | 2026-10-14 (high) | 1 | 0 | kk3_023 |
| 17 | https://egemen.kz/news/sashaga-dauys-bershi-alayaqtar-turgyndardy-aldaudyn-zhana-tasilin-oylap-tapty | Egemen Qazaqstan (egemen.kz) | 2026-10-20 (high) | 2 | 0 | kk3_024–kk3_025 (2) |
| 18 | https://egemen.kz/news/sizdin-atynyzga-senimhat-rasimdeldi-ulttyq-bank-alayaqtyqtyn-zhana-shemasy-turaly-eskertti | Egemen Qazaqstan (egemen.kz) | 2026-10-15 (high) | 1 | 0 | kk3_026 |
| 19 | https://aikyn.kz/280369/aldang-an--ag-artushy--arbag-an-alayak--kop | Aikyn.kz | 2025-02-15 (high) | 2 | 0 | kk3_027–kk3_028 (2) |
| 20 | https://aikyn.kz/286035/zeynetker-4-million-ten-geden-astam-k-arazhatyn-alayak-targ-a-bergen | Aikyn.kz | 2025-06-12 (high) | 1 | 0 | kk3_029 |
| 21 | https://aikyn.kz/288459/alayak-tar-ak-shany-ielenu-ushin-k-anday--dister-k-oldanuy-mumkin | Aikyn.kz | 2025-07-29 (high) | 2 | 0 | kk3_030–kk3_031 (2) |
| 22 | https://aikyn.kz/292646/zhurgizushi-ku-ligin-alug-a-zh-rdem-beremin--alayak--ozin-policiya-k-yzmetkeri-retinde-tanystyrg-an | Aikyn.kz | 2025-10-15 (high) | 1 | 0 | kk3_032 |
| 23 | https://aikyn.kz/293124/alayak-tyk-tyn--zhan-a-turi-payda-boldy | Aikyn.kz | 2025-10-24 (high) | 1 | 0 | kk3_033 |
| 24 | https://aikyn.kz/295183/shetelge-ok-ug-a-tusiremin--sertifikat-beremin--astanada-alayak--azamattardyn--152-million-ten-gesin-iemdengen | Aikyn.kz | 2025-12-01 (high) | 1 | 0 | kk3_034 |
| 25 | https://aikyn.kz/295832/zhan-a-zhyl-aldyndag-y-demalys--alayak-tar-zhii-sayahattaytyn-adamdy-k-alay-aldaytyny-belgili-boldy | Aikyn.kz | 2025-12-13 (high) | 1 | 0 | kk3_035 |
| 26 | https://aikyn.kz/301329/salg-an-ak-shan-dy-eselep-k-aytaramyn--121-adamdy-san-sok-tyrg-an-k-yzylordalyk--alayak--sottaldy | Aikyn.kz | 2026-03-28 (high) | 1 | 0 | kk3_036 |
| 27 | https://aikyn.kz/310856/zhi-d-uirindegi-zhan-a-alayak-tyk | Aikyn.kz | 2026-09-26 (high) | 1 | 0 | kk3_037 |
| 28 | https://aikyn.kz/312805/alayak-tardyn--aylasy-ask-ynyp-barady | Aikyn.kz | 2026-10-31 (high) | 1 | 0 | kk3_038 |
| 29 | https://egemen.kz/news/alayaqtardyn-arbauyna-qalay-iligemiz | Egemen Qazaqstan (egemen.kz) | 2026-09-26 (high) | 1 | 0 | kk3_039 |
| 30 | https://egemen.kz/news/article381774-internet-alayaqtan-qalay-saqtanamyz | Egemen Qazaqstan (egemen.kz) | 2025-02-14 (high) | 1 | 0 | kk3_040 |
| 31 | https://egemen.kz/news/article383767-kiberalayaqtan-saqtanu-dgoly-qanday | Egemen Qazaqstan (egemen.kz) | 2025-03-18 (high) | 2 | 0 | kk3_041–kk3_042 (2) |
| 32 | https://egemen.kz/news/article386085-qyzylordada-alayaq-ayel-ustaldy | Egemen Qazaqstan (egemen.kz) | 2025-04-23 (high) | 1 | 0 | kk3_043 |
| 33 | https://egemen.kz/news/article387881-qazaqstandyqtargha-alayaqtyqtynh-dganha-turi-turaly-eskertu-dgasaldy | Egemen Qazaqstan (egemen.kz) | 2025-05-22 (high) | 3 | 0 | kk3_044–kk3_046 (3) |
| 34 | https://egemen.kz/news/article390177-alayaqtar-ayylyn-dgiyar-emes | Egemen Qazaqstan (egemen.kz) | 2025-06-25 (high) | 1 | 0 | kk3_047 |
| 35 | https://egemen.kz/news/article392450-internettegi-alayaqtyq-orship-barady | Egemen Qazaqstan (egemen.kz) | 2025-08-01 (high) | 1 | 0 | kk3_048 |
| 36 | https://egemen.kz/news/article399642-zhenhildetilgen-nesie-alyp-beremin-astanada-alayaqqa-ukim-shyqty | Egemen Qazaqstan (egemen.kz) | 2025-11-20 (high) | 1 | 0 | kk3_049 |
| 37 | https://egemen.kz/news/article402567-alayaqtar-bala-arqyly-aldaugha-koshti | Egemen Qazaqstan (egemen.kz) | 2025-12-26 (high) | 6 | 0 | kk3_050–kk3_055 (6) |
| 38 | https://egemen.kz/news/article404418-uysiz-kuysiz-qaldy-pavlodarlyq-zeynetker-alayaqtardynh-arbauymen-baspanasyn-saty | Egemen Qazaqstan (egemen.kz) | 2026-01-19 (high) | 1 | 0 | kk3_056 |
| 39 | https://egemen.kz/news/article406584-petropavlda-alayaqtynh-arbauyna-tusken-ayel-18-mln-tenhgesinen-ayyryldy | Egemen Qazaqstan (egemen.kz) | 2026-02-12 (high) | 1 | 0 | kk3_057 |
| 40 | https://egemen.kz/news/article406853-internet-alayaqtargha-aldanghandar-oqighasy-zhii-kezdesetin-qatelikter-men-kenhe | Egemen Qazaqstan (egemen.kz) | 2026-02-17 (high) | 2 | 0 | kk3_058–kk3_059 (2) |
| 41 | https://egemen.kz/news/article362411-alayaqtar-su-tasqyny-dgaghdayyn-azamattardy-aldau-ushin-paydalana-bastady | Egemen Qazaqstan (egemen.kz) | 2024-04-16 (high) | 3 | 0 | kk3_060–kk3_062 (3) |
| 42 | https://egemen.kz/news/article345681-qostanay-turghyndaryn-20-mln-tenhgege-san-soqtyrghan-alayaq-ustaldy | Egemen Qazaqstan (egemen.kz) | 2023-07-13 (high) | 1 | 0 | kk3_063 |
| 43 | https://egemen.kz/news/article236522-qyzylorda-departament-bastyghy-turghyndardy-alayaqtardan-saq-bolugha-shaqyrdy | Egemen Qazaqstan (egemen.kz) | 2020-05-25 (high) | 1 | 0 | kk3_064 |
| 44 | https://egemen.kz/news/article239212-qostanay-oblysynda-zeynetkerlerdi-aldap-aqsha-tauyp-kelgen-alayaqtar-ustaldy | Egemen Qazaqstan (egemen.kz) | 2020-06-15 (high) | 1 | 0 | kk3_065 |
| 45 | https://egemen.kz/news/article240245-alayaq-turmeden-shygharyp-beremin-dep-turghyndy-aldaghan | Egemen Qazaqstan (egemen.kz) | 2020-06-24 (high) | 1 | 0 | kk3_066 |
| 46 | https://egemen.kz/news/article251184-qyzylordalyq-politseyler-taghy-bir-alayaqty-ustady | Egemen Qazaqstan (egemen.kz) | 2020-10-06 (high) | 1 | 0 | kk3_067 |
| 47 | https://egemen.kz/news/article262079-qyzylordada-eki-alayaq-ayel-sottaldy | Egemen Qazaqstan (egemen.kz) | 2021-01-21 (high) | 1 | 0 | kk3_068 |
| 48 | https://egemen.kz/news/article272144-tarazda-dgurgizushi-kualigin-satqan-alayaq-ustaldy | Egemen Qazaqstan (egemen.kz) | 2021-04-20 (high) | 1 | 0 | kk3_069 |
| 49 | https://egemen.kz/news/article285726-birdgadan-aqshany-kobeytip-beremin-shymkentte-alayaq-ustaldy | Egemen Qazaqstan (egemen.kz) | 2021-08-19 (high) | 1 | 0 | kk3_070 |
| 50 | https://egemen.kz/news/article289937-zher-alyp-beremin-degen-alayaq-ustaldy | Egemen Qazaqstan (egemen.kz) | 2021-09-21 (high) | 1 | 0 | kk3_071 |
| 51 | https://egemen.kz/news/article320892-turkistanda-tanysyn-dgumysqa-ornalastyrmaq-bolghan-alayaq-ustaldy | Egemen Qazaqstan (egemen.kz) | 2022-08-17 (high) | 1 | 0 | kk3_072 |
| 52 | https://egemen.kz/news/article415743-qauipsiz-shotqa-aqsha-audarynhyz-aqtobe-turghynynynh-qomaqty-qardgysyn-alayaqtar | Egemen Qazaqstan (egemen.kz) | 2026-06-25 (high) | 1 | 0 | kk3_073 |
| 53 | https://ult.kz/kz/post/20-million-tenge-nesie-satylgan-pater-almatyda-zeynetker-alayaktardyn-kurbany-boldy | Ult.kz (Ұлт порталы) | 2026-03-28 (high) | 2 | 0 | kk3_074–kk3_075 (2) |
| 54 | https://ult.kz/kz/post/aldanyp-kalmanyzdar-tursynbek-kabatov-elge-manyzdy-akparatty-khabarlady | Ult.kz (Ұлт порталы) | 2025-11-05 (high) | 4 | 0 | kk3_076–kk3_079 (4) |
| 55 | https://ult.kz/kz/post/kuyeuinnin-whatsapp-tagy-khattaryn-ashyp-beremin-kostanaylyk-ayel-alayaktarga-aldanyp-kaldy | Ult.kz (Ұлт порталы) | 2025-11-18 (high) | 1 | 0 | kk3_080 |
| 56 | https://ult.kz/kz/post/nesie-tarikhyn-zhaksartyp-beremiz-bko-da-internet-alayaktykpen-aynalyskan-top-ustaldy | Ult.kz (Ұлт порталы) | 2024-11-13 (high) | 1 | 0 | kk3_081 |
| 57 | https://ult.kz/kz/post/oskemende-turgyndardy-ortak-biznes-ashamyz-dep-aldagan-alayak-ustaldy | Ult.kz (Ұлт порталы) | 2025-10-08 (high) | 1 | 0 | kk3_082 |
| 58 | https://aikyn.kz/282911/k-yzylorda-tu-rg-yny-3-million-ten-gege-aldanyp-k-aldy | Aikyn.kz | 2025-04-11 (high) | 1 | 0 | kk3_083 |
| 59 | https://aikyn.kz/289244/tu-rg-yndardy-zhasospirimderdin--whatsapp-akkaunttary-ark-yly-aldag-an | Aikyn.kz | 2025-08-13 (high) | 1 | 0 | kk3_084 |
| 60 | https://aikyn.kz/289423/studentter-p-ter-zhaldag-anda-aldanyp-k-almaudyn--zholdary | Aikyn.kz | 2025-08-16 (high) | 1 | 0 | kk3_085 |
| 61 | https://aikyn.kz/294539/beytanys-adamg-a-24-million-ten-ge-audarg-an--tobylda-policiya-tort-dropperdi-anyk-tady | Aikyn.kz | 2025-11-18 (high) | 5 | 0 | kk3_086–kk3_090 (5) |
| 62 | https://aikyn.kz/301310/dropper-k-u-rban-ba--k-ylmysker-me | Aikyn.kz | 2026-03-28 (high) | 1 | 0 | kk3_091 |
| 63 | https://egemen.kz/news/article389791-qardgy-piramidasynynh-dgoly-kesildi | Egemen Qazaqstan (egemen.kz) | 2025-06-19 (high) | 1 | 0 | kk3_092 |
| 64 | https://egemen.kz/news/article390264-kiberqylmyspen-kures-tolastamaydy | Egemen Qazaqstan (egemen.kz) | 2025-06-26 (high) | 1 | 0 | kk3_093 |
| 65 | https://egemen.kz/news/article407670-1414-ten-sms-kelse-saq-bolynhyz-azamattardy-aldaudynh-dganha-skhemasy-belgili-bo | Egemen Qazaqstan (egemen.kz) | 2026-02-25 (high) | 1 | 0 | kk3_094 |
| 66 | https://kaz.inform.kz/news/zhana-shema-alayaktar-emhana-atin-zhamilip-kod-suray-bastagan-8feda007/ | Kazinform (kaz.inform.kz) | 2026-05-24 (high) | 5 | 0 | kk3_095–kk3_099 (5) |
| 67 | https://kaz.inform.kz/news/internet-alayaktari-zheke-derekternzge-kalay-kol-zhetkzed-f53762/ | Kazinform (kaz.inform.kz) | 2025-04-02 (high) | 1 | 0 | kk3_100 |
| 68 | https://khabar.kz/kk/news/okiga/166515-zhambyl-oblysynda-internet-alayaktyk-orship-tur | Khabar (khabar.kz/kk) | 2024-11-12 (high) | 2 | 0 | kk3_101–kk3_102 (2) |
| 69 | https://qazaqstan.tv/news/234034 | Qazaqstan National TV (qazaqstan.tv) | 2026-11-03 (high) | 1 | 0 | kk3_103 |
| 70 | https://qazaqstan.tv/news/130652 | Qazaqstan National TV (qazaqstan.tv) | 2020-09-07 (high) | 1 | 0 | kk3_104 |
| 71 | https://zhasalash.kz/news/alayaqtar-aldynda-quqyq-qorgau-oryndary-nege-alsiz-20706/ | Jas Alash (zhasalash.kz) | 2022-06-07 (high) | 5 | 0 | kk3_105–kk3_109 (5) |
| 72 | https://massaget.kz/zhadnama/bank-kyizmetkern-alayaktan-kalay-ajyiratuga-boladyi-64613/ | Massaget.kz | 2021-03-04 (high) | 11 | 1 | kk3_110–kk3_126 (12) |
| 73 | https://khabar.kz/kk/news/kogam/181762-kharagandylykh-erlizaiypty-uiinen-aiyrylyp-khala-zhazdady | Khabar (khabar.kz/kk) | 2026-01-20 (high) | 2 | 0 | kk3_121–kk3_122 (2) |
| 74 | https://khabar.kz/kk/news/kogam/132138-elimizde-alayaktyk-okigalary-zhiilep-ketti | Khabar (khabar.kz/kk) | 2021-03-09 (high) | 2 | 1 | kk3_123–kk3_125 (3) |
| 75 | https://kaz.inform.kz/news/ozin-bank-kyzmetkerimin-degen-alayak-oral-turgynynyn-1-4-mln-tengesin-iemdenip-ketken_a3640788/ | Kazinform (kaz.inform.kz) | 2020-04-21 (high) | 1 | 0 | kk3_127 |
| 76 | https://kaz.inform.kz/news/10-min-tenge-ushn-aktobede-studentterd-dropperlkke-kalay-tartadi-6554cf67/ | Kazinform (kaz.inform.kz) | 2026-10-10 (high) | 6 | 0 | kk3_128–kk3_133 (6) |
| 77 | https://kaz.inform.kz/news/kizilorda-universitet-grantka-tusremz-degen-habarlamalardi-zhokka-shigardi-1506ac77/ | Kazinform (kaz.inform.kz) | 2026-08-19 (high) | 1 | 0 | kk3_134 |
| 78 | https://www.gov.kz/memleket/entities/mvd-pavlodar/press/news/details/1316486?lang=kk | Pavlodar Region Police Department via gov.kz (mvd-pavlodar) | 2026-10-23 (high) | 1 | 0 | kk3_135 |
| 79 | https://www.gov.kz/memleket/entities/mvd-aktobe/press/news/details/1287148?lang=kk | Aktobe Region Police Department via gov.kz (mvd-aktobe) | 2026-09-07 (high) | 1 | 0 | kk3_136 |
| 80 | https://www.gov.kz/memleket/entities/prokuratura-kyzylorda/press/news/details/1232302?lang=kk | Kyzylorda Region Prosecutor's Office via gov.kz (prokuratura-kyzylorda) | 2026-06-02 (high) | 1 | 0 | kk3_137 |
| 81 | https://nationalbank.kz/kz/news/informacionnye-soobshcheniya/18679 | National Bank of Kazakhstan (nationalbank.kz/kz) | 2026-02-17 (high) | 1 | 0 | kk3_138 |
| 82 | https://kapital.kz/kk/gosudarstvo/148650/bzhzkh-atyn-zhamylghan-alayakhtar-khor-khazakhstandykhtargha-eskertu-zhasady.html | Kapital.kz (kk), citing ENPF | 2026-05-29 (high) | 1 | 0 | kk3_139 |
| 83 | https://www.gov.kz/memleket/entities/kgd/press/article/details/233841?lang=kk | State Revenue Committee (kgd) via gov.kz, ESF IS FAQ | 2025-11-28 (low) | 0 | 1 | kk3_140 |
| 84 | https://hcsbk.kz/news/press_relize/-rmetti-klientter14012/ | Otbasy Bank (hcsbk.kz) client notice | 2022-01-14 (medium) | 0 | 1 | kk3_141 |
| 85 | https://hcsbk.kz/news/press_relize/-rmetti-klientter2602224/ | Otbasy Bank (hcsbk.kz) client notice | 2024-02-26 (medium) | 0 | 1 | kk3_142 |
| 86 | https://hcsbk.kz/news/press_relize/-rmetti-klientter0131/ | Otbasy Bank (hcsbk.kz) client notice | 2022-03-01 (high) | 0 | 1 | kk3_143 |
| 87 | https://hcsbk.kz/news/press_relize/-rmetti-klientter--2024-04-16/ | Otbasy Bank (hcsbk.kz) client notice | 2024-04-16 (high) | 0 | 1 | kk3_144 |
| 88 | https://hcsbk.kz/news/press_relize/-rmetti-klientter0604-2/ | Otbasy Bank (hcsbk.kz) client notice | 2023-04-06 (medium) | 0 | 1 | kk3_145 |
| 89 | https://hcsbk.kz/news/press_relize/-rmetti-klientter0991/ | Otbasy Bank (hcsbk.kz) client notice | 2022-09-09 (medium) | 0 | 1 | kk3_146 |
| 90 | https://hcsbk.kz/news/press_relize/-rmetti-klientter-16-11-2024/ | Otbasy Bank (hcsbk.kz) client notice | 2024-11-16 (high) | 0 | 1 | kk3_147 |
| 91 | https://hcsbk.kz/news/press_relize/uvazhaemye-klienty-s-10-marta-2026-goda-na-portale-baspana-market/ | Otbasy Bank (hcsbk.kz) client notice | 2026-03-16 (high) | 0 | 1 | kk3_148 |
| 92 | https://hcsbk.kz/news/press_relize/uvazhaemye-klienty-s-21-po-24-marta-2026/ | Otbasy Bank (hcsbk.kz) client notice | 2026-03-20 (high) | 0 | 1 | kk3_149 |
| 93 | https://hcsbk.kz/news/press_relize/uvazhaemye-klienty-s-22-00-23-noyabrya-do-03-00-24/ | Otbasy Bank (hcsbk.kz) client notice | 2025-11-21 (high) | 0 | 1 | kk3_150 |
| 94 | https://hcsbk.kz/news/press_relize/uvazhaemye-klienty-spravka-o-nalichii-ssudnoy-zadolzhennosti/ | Otbasy Bank (hcsbk.kz) client notice | 2026-04-16 (high) | 0 | 1 | kk3_151 |
| 95 | https://hcsbk.kz/news/press_relize/uvazhaemye-klienty-01-012026/ | Otbasy Bank (hcsbk.kz) client notice | 2025-12-10 (high) | 0 | 1 | kk3_152 |
| 96 | https://hcsbk.kz/news/press_relize/uvazhaemye-klienty-07-02-2026/ | Otbasy Bank (hcsbk.kz) client notice | 2026-02-06 (high) | 0 | 1 | kk3_153 |
| 97 | https://hcsbk.kz/news/press_relize/uvazhaemye-klienty-12-2025/ | Otbasy Bank (hcsbk.kz) client notice | 2025-12-18 (high) | 0 | 1 | kk3_154 |
| 98 | https://hcsbk.kz/news/press_relize/uvazhaemye-klienty-1234-2026/ | Otbasy Bank (hcsbk.kz) client notice | 2025-12-30 (high) | 0 | 1 | kk3_155 |
| 99 | https://hcsbk.kz/news/press_relize/uvazhaemye-klienty-14-noyabrya-2025-/ | Otbasy Bank (hcsbk.kz) client notice | 2025-11-14 (high) | 0 | 1 | kk3_156 |
| 100 | https://hcsbk.kz/news/press_relize/uvazhaemye-klienty-16-02-2026/ | Otbasy Bank (hcsbk.kz) client notice | 2026-02-13 (high) | 0 | 1 | kk3_157 |
| 101 | https://hcsbk.kz/news/press_relize/uvazhaemye-klienty-19-00-chasov-12-yanvarya-2026/ | Otbasy Bank (hcsbk.kz) client notice | 2026-01-12 (high) | 0 | 1 | kk3_158 |
| 102 | https://hcsbk.kz/news/press_relize/uvazhaemye-klienty-2-4-01-2026/ | Otbasy Bank (hcsbk.kz) client notice | 2025-12-30 (high) | 0 | 1 | kk3_159 |
| 103 | https://hcsbk.kz/news/press_relize/uvazhaemye-klienty-2-4-2026/ | Otbasy Bank (hcsbk.kz) client notice | 2025-12-31 (high) | 0 | 1 | kk3_160 |
| 104 | https://hcsbk.kz/news/press_relize/uvazhaemye-klienty-20251216-100/ | Otbasy Bank (hcsbk.kz) client notice | 2025-12-15 (high) | 0 | 1 | kk3_161 |
| 105 | https://hcsbk.kz/news/press_relize/uvazhaemye-klienty-2026-01-16/ | Otbasy Bank (hcsbk.kz) client notice | 2026-01-16 (high) | 0 | 1 | kk3_162 |
| 106 | https://hcsbk.kz/news/press_relize/uvazhaemye-klienty-2026-07-06/ | Otbasy Bank (hcsbk.kz) client notice | 2026-07-01 (high) | 0 | 1 | kk3_163 |
| 107 | https://hcsbk.kz/news/press_relize/uvazhaemye-klienty-29-2025/ | Otbasy Bank (hcsbk.kz) client notice | 2025-12-29 (high) | 0 | 1 | kk3_164 |
| 108 | https://hcsbk.kz/news/press_relize/uvazhaemye-klienty-7-9-maya/ | Otbasy Bank (hcsbk.kz) client notice | 2026-05-06 (high) | 0 | 1 | kk3_165 |
| 109 | https://hcsbk.kz/news/press_relize/uvazhaemye-klienty-8-i-9-aprelya-s-02-00-do-06-00/ | Otbasy Bank (hcsbk.kz) client notice | 2026-04-07 (high) | 0 | 1 | kk3_166 |
| 110 | https://hcsbk.kz/news/press_relize/uvazhaemye-klienty-astana-ul-koshkarbaeva-26/ | Otbasy Bank (hcsbk.kz) client notice | 2026-01-21 (high) | 0 | 1 | kk3_167 |
| 111 | https://hcsbk.kz/news/press_relize/uvazhaemye-klienty-atyrau-ul-abaya-15-a-1/ | Otbasy Bank (hcsbk.kz) client notice | 2025-11-14 (high) | 0 | 1 | kk3_168 |
| 112 | https://hcsbk.kz/news/press_relize/uvazhaemye-klienty-dekabr-2025/ | Otbasy Bank (hcsbk.kz) client notice | 2025-12-19 (high) | 0 | 1 | kk3_169 |
| 113 | https://hcsbk.kz/news/press_relize/uvazhaemye-klienty-enpf-otbasy-kz-vremenno-nablyudayutsya-tekhnicheskie-nepoladki/ | Otbasy Bank (hcsbk.kz) client notice | 2025-11-20 (high) | 0 | 1 | kk3_170 |
| 114 | https://hcsbk.kz/news/press_relize/uvazhaemye-klienty-kabinet-mio-s-diplomom-v-selo/ | Otbasy Bank (hcsbk.kz) client notice | 2025-11-14 (high) | 0 | 1 | kk3_171 |
| 115 | https://hcsbk.kz/news/press_relize/uvazhaemye-klienty-napominaet-zayemshchikam-o-vozmozhnosti-obrashcheniya/ | Otbasy Bank (hcsbk.kz) client notice | 2026-01-12 (high) | 0 | 1 | kk3_172 |
| 116 | https://hcsbk.kz/news/press_relize/uvazhaemye-klienty-otbasy-bank-stal-uchastnikom/ | Otbasy Bank (hcsbk.kz) client notice | 2026-07-20 (high) | 0 | 1 | kk3_173 |
| 117 | https://hcsbk.kz/news/press_relize/uvazhaemye-klienty-platforma-enpf-otbasy-kz-rabotaet-v-shtatnom-rezhime/ | Otbasy Bank (hcsbk.kz) client notice | 2025-11-20 (high) | 0 | 1 | kk3_174 |
