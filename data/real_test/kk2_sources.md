# Kazakh slice, round 2 (kk2): sources and method

Collected 2026-11-14. File: `kk2_collected.jsonl` (283 items). Every source page below is NEW (not in `kk_sources.md`, `ru_sources.md` or `ru2_sources.md`).

## How the text was captured
- Each page was downloaded with `curl` (Telegram posts via public `t.me/s/<channel>` pages; nitec.kz via its public news API; the two PDFs via PyMuPDF) and turned into plain text locally. Text was copied from that local text, never from an AI summary.
- A script checked that every item (before PII scrubbing) appears word for word in its saved page text after whitespace/quote/dash normalisation: **283/283 matched, 0 failures**. Saved page texts are in the session scratchpad (not in this folder).
- One allowed edit: in the Fingramota OYLA PDF, line-break hyphens were joined (`карта-/ның` → `картаның`). Source typos are kept (e.g. legit item starting `025 жылдың` = 2025).
- Deduplicated (case/punctuation-insensitive) against all existing `data/real_test/*.jsonl` texts and within this file: 3 cross-source exact duplicates dropped. Items with difflib similarity ≥0.85 to an existing item say so in `notes` (5 items). Within the file, 5 pairs are close rewordings from different sources and were kept on purpose (kk2_016/068/221 "несие рәсімделді"; kk2_046/067; kk2_096/170 QR delivery; kk2_189/198 delivery SMS code).
- Scrubbing: names → [NAME], phones → [PHONE] (1 legit item). No cards or IINs appeared.

## Counts
- label: scam 232, legit 51
- unit: message 188, fragment 80, call_phrase 15
- kind: call_quote 100, messenger 93, web 76, sms 14
- language: kk 282, ru 1
- kbd: False 283
- year (scam): 2026 170, 2025 48, 2024 2, 2023 3, 2021 5, 2020 4
- year (legit): 2026 26, 2025 19, 2023 1, 2022 1, 2020 1, 2019 1, 2018 1, 2017 1
- scam schemes: 87 distinct; top: money_mule_recruitment 22, fake_bank_security 19, investment_platform 12, relative_in_trouble 8, fake_delivery_code 6, investment_ad 6, fake_rental 5, fake_utility_meter 5, romance 5, fake_prize_giveaway 5, free_diagnostics_upsell 5, safe_account 4, account_takeover_loan 4, real_estate_sale_coercion 4, fake_broker_investment 4

## Sources used
| # | Source URL | Publisher | Date (confidence) | scam | legit | ids |
|---|---|---|---|---|---|---|
| 1 | https://t.me/POLICE_of_KZ/15524 | MVD RK official Telegram channel (POLISIA.KZ, t.me/POLICE_of_KZ) | 2025-09-08 (high) | 10 | 0 | kk2_001–kk2_010 (10) |
| 2 | https://t.me/dp_abai/19339 | Abai Region Police Department Telegram channel (t.me/dp_abai) | 2026-08-12 (high) | 1 | 0 | kk2_011 |
| 3 | https://t.me/POLICE_of_KZ/17761 | MVD RK official Telegram channel (POLISIA.KZ, t.me/POLICE_of_KZ) | 2026-08-12 (high) | 1 | 0 | kk2_012 |
| 4 | https://t.me/POLICE_of_KZ/15697 | MVD RK official Telegram channel (POLISIA.KZ, t.me/POLICE_of_KZ) | 2025-10-01 (high) | 1 | 0 | kk2_013 |
| 5 | https://t.me/POLICE_of_KZ/15814 | MVD RK official Telegram channel (POLISIA.KZ, t.me/POLICE_of_KZ) | 2025-10-24 (high) | 2 | 0 | kk2_014–kk2_015 (2) |
| 6 | https://t.me/GenPr/9913 | Prosecutor General's Office Telegram channel (t.me/GenPr) | 2025-10-31 (high) | 2 | 0 | kk2_016–kk2_017 (2) |
| 7 | https://t.me/dp_zhetysu/1071 | Zhetysu Region Police Department Telegram channel (t.me/dp_zhetysu) | 2026-01-14 (high) | 1 | 0 | kk2_018 |
| 8 | https://t.me/dp_abai/14306 | Abai Region Police Department Telegram channel (t.me/dp_abai) | 2026-01-13 (high) | 4 | 0 | kk2_019–kk2_022 (4) |
| 9 | https://t.me/POLICE_of_KZ/16744 | MVD RK official Telegram channel (POLISIA.KZ, t.me/POLICE_of_KZ) | 2026-03-27 (high) | 2 | 0 | kk2_023–kk2_024 (2) |
| 10 | https://t.me/dp_abai/19032 | Abai Region Police Department Telegram channel (t.me/dp_abai) | 2026-07-27 (high) | 3 | 0 | kk2_025–kk2_027 (3) |
| 11 | https://t.me/dp_abai/19067 | Abai Region Police Department Telegram channel (t.me/dp_abai) | 2026-07-28 (high) | 1 | 0 | kk2_028 |
| 12 | https://t.me/dp_abai/19139 | Abai Region Police Department Telegram channel (t.me/dp_abai) | 2026-08-03 (high) | 3 | 0 | kk2_029–kk2_031 (3) |
| 13 | https://t.me/POLICE_of_KZ/17782 | MVD RK official Telegram channel (POLISIA.KZ, t.me/POLICE_of_KZ) | 2026-08-15 (high) | 1 | 0 | kk2_032 |
| 14 | https://t.me/dp_abai/19414 | Abai Region Police Department Telegram channel (t.me/dp_abai) | 2026-08-15 (high) | 3 | 0 | kk2_033–kk2_035 (3) |
| 15 | https://t.me/dp_abai/16542 | Abai Region Police Department Telegram channel (t.me/dp_abai) | 2026-04-08 (high) | 5 | 0 | kk2_036–kk2_040 (5) |
| 16 | https://t.me/POLICE_of_KZ/17934 | MVD RK official Telegram channel (POLISIA.KZ, t.me/POLICE_of_KZ) | 2026-09-04 (high) | 1 | 0 | kk2_041 |
| 17 | https://t.me/dp_abai/19863 | Abai Region Police Department Telegram channel (t.me/dp_abai) | 2026-09-04 (high) | 1 | 0 | kk2_042 |
| 18 | https://t.me/dp_abai/17422 | Abai Region Police Department Telegram channel (t.me/dp_abai) | 2026-05-15 (high) | 4 | 0 | kk2_043–kk2_046 (4) |
| 19 | https://t.me/dp_abai/18058 | Abai Region Police Department Telegram channel (t.me/dp_abai) | 2026-06-11 (high) | 5 | 0 | kk2_047–kk2_051 (5) |
| 20 | https://t.me/dp_abai/18289 | Abai Region Police Department Telegram channel (t.me/dp_abai) | 2026-06-19 (high) | 3 | 0 | kk2_052–kk2_054 (3) |
| 21 | https://t.me/dp_abai/15492 | Abai Region Police Department Telegram channel (t.me/dp_abai) | 2026-02-24 (high) | 2 | 0 | kk2_055–kk2_056 (2) |
| 22 | https://t.me/dp_abai/16468 | Abai Region Police Department Telegram channel (t.me/dp_abai) | 2026-04-06 (high) | 1 | 0 | kk2_057 |
| 23 | https://t.me/dp_abai/19468 | Abai Region Police Department Telegram channel (t.me/dp_abai) | 2026-08-18 (high) | 6 | 0 | kk2_058–kk2_063 (6) |
| 24 | https://t.me/dp_abai/17850 | Abai Region Police Department Telegram channel (t.me/dp_abai) | 2026-06-03 (high) | 1 | 0 | kk2_064 |
| 25 | https://t.me/dp_abai/14707 | Abai Region Police Department Telegram channel (t.me/dp_abai) | 2026-01-30 (high) | 3 | 0 | kk2_065–kk2_067 (3) |
| 26 | https://t.me/dp_abai/14399 | Abai Region Police Department Telegram channel (t.me/dp_abai) | 2026-01-16 (high) | 2 | 0 | kk2_068–kk2_069 (2) |
| 27 | https://t.me/dp_abai/15772 | Abai Region Police Department Telegram channel (t.me/dp_abai) | 2026-03-05 (high) | 1 | 0 | kk2_070 |
| 28 | https://t.me/dp_abai/13898 | Abai Region Police Department Telegram channel (t.me/dp_abai) | 2025-12-26 (high) | 1 | 0 | kk2_071 |
| 29 | https://t.me/POLICE_of_KZ/13302 | MVD RK official Telegram channel (POLISIA.KZ, t.me/POLICE_of_KZ) | 2024-11-12 (high) | 1 | 0 | kk2_072 |
| 30 | https://t.me/nationalbankkz/5364 | National Bank of Kazakhstan Telegram channel (t.me/nationalbankkz) | 2025-12-08 (high) | 1 | 0 | kk2_073 |
| 31 | https://t.me/nationalbankkz/4335 | National Bank of Kazakhstan Telegram channel (t.me/nationalbankkz) | 2024-01-26 (high) | 1 | 0 | kk2_074 |
| 32 | https://t.me/POLICE_of_KZ/17466 | MVD RK official Telegram channel (POLISIA.KZ, t.me/POLICE_of_KZ) | 2026-06-29 (high) | 2 | 0 | kk2_075–kk2_076 (2) |
| 33 | https://t.me/dp_abai/20244 | Abai Region Police Department Telegram channel (t.me/dp_abai) | 2026-09-22 (high) | 1 | 0 | kk2_077 |
| 34 | https://t.me/dp_abai/15600 | Abai Region Police Department Telegram channel (t.me/dp_abai) | 2026-02-27 (high) | 1 | 0 | kk2_078 |
| 35 | https://t.me/dp_abai/11827 | Abai Region Police Department Telegram channel (t.me/dp_abai) | 2025-09-30 (high) | 1 | 0 | kk2_079 |
| 36 | https://tengrinews.kz/internet/whatsapp-tan-jazyip-karyiz-suraydyi-aleumettk-jeldeg-5-413226/ | Tengrinews.kz (kaz) | 2020-09-07 (high) | 4 | 0 | kk2_080–kk2_083 (4) |
| 37 | https://24.kz/kz/zha-aly-tar/kogam/719925-karagandy-oblysynda-alaakka-sengen-zejnetker-ujsiz-kala-zazdady | 24.kz (Хабар 24) | 2025-07-15 (high) | 3 | 0 | kk2_084–kk2_086 (3) |
| 38 | https://24.kz/kz/zha-aly-tar/kogam/758266-bulletendi-tirkejmiz-alaaktar-azamattardy-aldap-zatyr | 24.kz (citing Central Communications Service anti-fake centre) | 2026-03-12 (high) | 2 | 0 | kk2_087–kk2_088 (2) |
| 39 | https://24.kz/kz/telepoject/stop-alaak/768353-alaaktar-kommunaldyk-kyzmet-okili-bolyp-habarlasudy-sygardy | 24.kz ('Стоп алаяқ' programme) | 2026-05-14 (high) | 1 | 0 | kk2_089 |
| 40 | https://24.kz/kz/telepoject/stop-alaak/769761-zurtka-zejnetaky-korynan-aksa-alyp-bermek-bolgan-alaak-ustaldy | 24.kz ('Стоп алаяқ' programme) | 2026-05-21 (high) | 1 | 0 | kk2_090 |
| 41 | https://kz.kursiv.media/kk/2026-06-26/ulttyq-bank-tegin-foto-tuesirip-beremin-deushilerden-saq-boluga-shaqyrdy/ | Kursiv Media Қазақстан (citing National Bank) | 2026-06-26 (high) | 3 | 0 | kk2_091–kk2_093 (3) |
| 42 | https://inbusiness.kz/kz/news/alayaktardyn-zhujesi-syr-bere-bastady | Inbusiness.kz | 2021-06-18 (high) | 2 | 0 | kk2_094–kk2_095 (2) |
| 43 | https://baq.kz/alayaqtar-qr-kod-arqyly-aqsha-zhymqyrudyn-zhana-adisin-oylap-tapty-320015181/ | Baq.kz | 2026-02-19 (high) | 1 | 0 | kk2_096 |
| 44 | https://baq.kz/buryngy-zhumys-ornynan-shalyngan-qonyrau-petropavl-turgyny-2-million-tengesinen-ayyryldy-320015785/ | Baq.kz | 2026-02-24 (high) | 1 | 0 | kk2_097 |
| 45 | https://baq.kz/8-nauryzda-gul-de-qauipti-bola-alady-320016136/ | Baq.kz | 2026-02-26 (high) | 2 | 0 | kk2_098–kk2_099 (2) |
| 46 | https://baq.kz/qaragandyda-tuystarynan-salemdeme-algan-zeynetkerler-aqshalarynan-ayyryldy-320018256/ | Baq.kz | 2026-03-13 (high) | 1 | 0 | kk2_100 |
| 47 | https://baq.kz/zeynetaqynyzdy-shygaryp-beremin-zhambylda-alayaq-ayelden-48-mln-tenge-algan-320022142/ | Baq.kz | 2026-04-11 (high) | 2 | 0 | kk2_101–kk2_102 (2) |
| 48 | https://baq.kz/alayaqtar-zhasandy-intellekt-arqyly-aldauga-koshti-qalay-saqtanu-kerek-320022472/ | Baq.kz | 2026-04-14 (high) | 1 | 0 | kk2_103 |
| 49 | https://baq.kz/alayaqtar-qarttardy-qalay-aldaydy-en-kop-taralgan-shemalar-320026839/ | Baq.kz | 2026-05-15 (high) | 1 | 0 | kk2_104 |
| 50 | https://baq.kz/medtaksi-rasimdep-beremin-qaragandyda-aleumettik-qyzmetker-zeynetkerlerdi-taqyrga-otyrgyzgan-320027844/ | Baq.kz | 2026-05-22 (high) | 1 | 0 | kk2_105 |
| 51 | https://baq.kz/telefondagy-qauip-alayaqtar-zhazgy-demalysta-mektep-oqushylaryn-qalay-andidy-320028183/ | Baq.kz | 2026-05-25 (high) | 3 | 0 | kk2_106–kk2_108 (3) |
| 52 | https://baq.kz/enbek-otiliniz-tabyldy-bzhzq-atyn-zhamylgan-alayaqtar-qazaqstandyqtardy-aldap-zhatyr-320029059/ | Baq.kz | 2026-06-01 (high) | 1 | 0 | kk2_109 |
| 53 | https://baq.kz/aqshanyzdy-eselep-qaytaramyn-154-adamdy-aldagan-alayaqqa-ukim-shyqty-320029195/ | Baq.kz | 2026-06-02 (high) | 1 | 0 | kk2_110 |
| 54 | https://baq.kz/nesiendi-zhauyp-beremin-aqtobelik-ayel-tanysyna-senip-aqshasynan-ayyryldy-320029587/ | Baq.kz | 2026-06-04 (high) | 1 | 0 | kk2_111 |
| 55 | https://baq.kz/shugyl-aqsha-kerek-shymkentte-internet-alayaqtar-toby-ustaldy-320031956/ | Baq.kz | 2026-06-22 (high) | 1 | 0 | kk2_112 |
| 56 | https://baq.kz/tuysynyzbyn-dep-10-zeynetkerdi-san-soqtyrgan-alayaq-sottaldy-320032143/ | Baq.kz | 2026-06-23 (high) | 1 | 0 | kk2_113 |
| 57 | https://baq.kz/shugyl-ort-dabylyn-auystyrynyz-qaragandyda-kasipkerlerdi-aldagan-alayaq-ustaldy-320034307/ | Baq.kz | 2026-07-09 (high) | 3 | 0 | kk2_114–kk2_116 (3) |
| 58 | https://baq.kz/sizge-13-million-tenge-grant-maquldandy-zharnamaga-sengender-milliondarynan-ayyryldy-320036061/ | Baq.kz | 2026-07-22 (high) | 1 | 0 | kk2_117 |
| 59 | https://baq.kz/ipoteka-rasimdep-beremin-elordalyq-ayel-tanystary-men-korshilerinin-500-mln-tengesin-zhymqyrgan-320036185/ | Baq.kz | 2026-07-23 (high) | 1 | 0 | kk2_118 |
| 60 | https://baq.kz/paterinizdi-shugyl-satynyz-aqtobelik-ayel-baspanasynan-ayyrylyp-qala-zhazdady-320037021/ | Baq.kz | 2026-07-29 (high) | 1 | 0 | kk2_119 |
| 61 | https://baq.kz/kiprden-pater-alyp-beremin-100-mln-tengege-ayeldi-aldangan-qazaqstandyq-gruziyadan-elge-zhetkizildi-320038217/ | Baq.kz | 2026-08-06 (high) | 1 | 0 | kk2_120 |
| 62 | https://baq.kz/nesie-ushin-bonus-alynyz-alayaqtar-zhana-shema-oylap-tapty-320038982/ | Baq.kz | 2026-08-11 (high) | 1 | 0 | kk2_121 |
| 63 | https://baq.kz/mama-men-senin-balanmyn-dep-sendirgen-taldyqorganda-ayel-35-mln-tengesin-alayaqqa-audargan-320048270/ | Baq.kz | 2026-10-08 (high) | 1 | 0 | kk2_122 |
| 64 | https://baq.kz/tuystarynyzga-syylyq-keldi-ayel-5-mln-tengesinen-ayyryla-zhazdady-320048497/ | Baq.kz | 2026-10-09 (high) | 1 | 0 | kk2_123 |
| 65 | https://baq.kz/aqshanyzdy-qorganyz-degen-qonyrau-zeynetker-3-mln-tengesinen-ayyrylyp-qala-zhazdady-320050106/ | Baq.kz | 2026-10-19 (high) | 1 | 0 | kk2_124 |
| 66 | https://baq.kz/whatsapp-tagy-qauipti-habarlama-dauys-bershi-degen-otinishtin-artynda-ne-zhatyr-320050210/ | Baq.kz | 2026-10-20 (high) | 1 | 0 | kk2_125 |
| 67 | https://baq.kz/aqshanyzdy-eki-eselep-beremin-astanada-zhalgan-investitsiya-usyngan-ayel-ustaldy-320052776/ | Baq.kz | 2026-11-05 (high) | 1 | 0 | kk2_126 |
| 68 | https://baq.kz/chatgpt-ge-neni-zhuktemeu-kerek-tsifrlyq-ortada-alayaqtan-qalay-qorganamyz-320053301/ | Baq.kz | 2026-11-10 (high) | 3 | 0 | kk2_127–kk2_129 (3) |
| 69 | https://baq.kz/ubt-ny-sizdin-ornynyzga-tapsyramyz-talapkerlerge-manyzdy-eskertu-zhasaldy-320039636/ | Baq.kz | 2026-08-15 (high) | 1 | 0 | kk2_130 |
| 70 | https://baq.kz/qaryzy-bar-adamdy-tauyp-beremin-aqtobede-kasipker-4-million-tengeden-ayyrylgan-320033455/ | Baq.kz | 2026-07-02 (high) | 1 | 0 | kk2_131 |
| 71 | https://baq.kz/pavlodarda-ofitser-zhalgan-uade-arqyly-aqsha-algany-ushin-sottaldy-320014682/ | Baq.kz | 2026-02-16 (high) | 1 | 0 | kk2_132 |
| 72 | https://baq.kz/50-payyz-paydaga-senip-nesie-algan-tarazdyq-ayel-2-mln-ga-zhuyq-qarzhysynan-ayyryldy-320053930/ | Baq.kz | 2026-11-13 (high) | 1 | 0 | kk2_133 |
| 73 | https://baq.kz/oskemende-halyqaralyq-izdeude-zhurgen-alayaq-ustaldy-320023345/ | Baq.kz | 2026-04-20 (high) | 1 | 0 | kk2_134 |
| 74 | https://baq.kz/remont-zhasap-beremin-instagram-arqyly-21-mln-tenge-zhymqyrgan-astanalyq-sottaldy-320052345/ | Baq.kz | 2026-11-03 (high) | 1 | 0 | kk2_135 |
| 75 | https://baq.kz/zhambyl-oblysynda-emtihansyz-kualik-alyp-bermek-bolgan-alayaq-sottaldy-320026605/ | Baq.kz | 2026-05-14 (high) | 1 | 0 | kk2_136 |
| 76 | https://live.fingramota.kz/kk/news/post/abajlayz-kredit-alayaty-shemalardy-alaj-anytaua-bolady | Fingramota.kz (ARDFM financial literacy portal) | 2026-08-24 (high) | 4 | 0 | kk2_137, kk2_138, kk2_223, kk2_224 |
| 77 | https://live.fingramota.kz/kk/news/post/abajlayz-zhalan-brokerler-azamattardy-dropperlikke-tartuda | Fingramota.kz (ARDFM financial literacy portal) | 2026-04-06 (high) | 2 | 0 | kk2_139–kk2_140 (2) |
| 78 | https://live.fingramota.kz/kk/news/post/adamny-cifrly-izi-zhelige-rbir-kirgen-sajyn-ne-alady | Fingramota.kz (ARDFM financial literacy portal) | 2026-09-14 (high) | 5 | 0 | kk2_141…kk2_222 (5) |
| 79 | https://live.fingramota.kz/kk/news/post/aldamshy-lem-dipfejkter-aldau-ralyna-alaj-ajnalady | Fingramota.kz (ARDFM financial literacy portal) | 2025-10-28 (high) | 1 | 0 | kk2_143 |
| 80 | https://live.fingramota.kz/kk/news/post/aldanbaua-tyrysyyz-marketologtar-men-alayatar-sizdi-emociyalaryyzda-alaj-ojnajdy | Fingramota.kz (ARDFM financial literacy portal) | 2026-03-19 (high) | 7 | 0 | kk2_144–kk2_150 (7) |
| 81 | https://live.fingramota.kz/kk/news/post/art-adamdara-arzhyly-alayatardan-alaj-satanu-kerek | Fingramota.kz (ARDFM financial literacy portal) | 2025-08-04 (high) | 1 | 0 | kk2_151 |
| 82 | https://live.fingramota.kz/kk/news/post/art-azamattar-tuekel-ajmaynda-zhelilik-biznes-trinde-zhasyrynan-alayatyty-alaj-tanyp-biluge-bolady | Fingramota.kz (ARDFM financial literacy portal) | 2026-06-15 (high) | 1 | 0 | kk2_152 |
| 83 | https://live.fingramota.kz/kk/news/post/aryza-batyruy-mmkin-internet-alayatyty-eki-tsili | Fingramota.kz (ARDFM financial literacy portal) | 2026-07-26 (high) | 6 | 0 | kk2_153–kk2_158 (6) |
| 84 | https://live.fingramota.kz/kk/news/post/ashayzdy-ajtaramyz-alayatar-rbandaryn-zhaa-tzaa-alaj-tartady | Fingramota.kz (ARDFM financial literacy portal) | 2026-08-17 (high) | 1 | 0 | kk2_159 |
| 85 | https://live.fingramota.kz/kk/news/post/ata-ana-baylauy-zhaa-alayaty-shema | Fingramota.kz (ARDFM financial literacy portal) | 2025-11-26 (high) | 3 | 0 | kk2_160–kk2_162 (3) |
| 86 | https://live.fingramota.kz/kk/news/post/azastandytardy-onlajn-ojyndarday-alayatardan-sa-bolua-shayrdy | Fingramota.kz (ARDFM financial literacy portal) | 2025-07-14 (high) | 5 | 0 | kk2_163–kk2_167 (5) |
| 87 | https://live.fingramota.kz/kk/news/post/banktik-shota-auip-tnip-tr-alaj-alayaty-shemany-atysushysy-bolmaua-bolady | Fingramota.kz (ARDFM financial literacy portal) | 2026-10-19 (high) | 1 | 0 | kk2_168 |
| 88 | https://live.fingramota.kz/kk/news/post/bir-basumen-asha-alayatar-messendzherlerde-alaj-aldajdy | Fingramota.kz (ARDFM financial literacy portal) | 2026-11-11 (high) | 1 | 0 | kk2_169 |
| 89 | https://live.fingramota.kz/kk/news/post/bir-skan-imyl-ashayza-minus-alayatar-yzmet-krsetu-salasynda-zhalan-qr-kodtardy-alaj-pajdalanady | Fingramota.kz (ARDFM financial literacy portal) | 2026-02-18 (high) | 1 | 0 | kk2_170 |
| 90 | https://live.fingramota.kz/kk/news/post/densaulyty-tegin-diagnostikalaudan-bastap-pter-zhndeuge-dejin-alayatyty-zhaa-trleri | Fingramota.kz (ARDFM financial literacy portal) | 2025-06-23 (high) | 2 | 0 | kk2_171–kk2_172 (2) |
| 91 | https://live.fingramota.kz/kk/news/post/dropperlik-alayaty-shemaa-alaj-seriktes-bolyp-almau-kerek | Fingramota.kz (ARDFM financial literacy portal) | 2025-07-09 (high) | 5 | 0 | kk2_173–kk2_177 (5) |
| 92 | https://live.fingramota.kz/kk/news/post/dropperlik-ylmys | Fingramota.kz (ARDFM financial literacy portal) | 2025-09-15 (high) | 2 | 0 | kk2_178–kk2_179 (2) |
| 93 | https://live.fingramota.kz/kk/news/post/egov-ty-atynan-oyrau-shalu-alayatar-zderini-shemalarynda-memlekettik-yzmetterdi-alaj-pajdalanady | Fingramota.kz (ARDFM financial literacy portal) | 2026-09-30 (high) | 2 | 0 | kk2_180–kk2_181 (2) |
| 94 | https://live.fingramota.kz/kk/news/post/fejkter-zhne-hajp-shemalar-nelikten-internetten-krgenni-brine-senuge-bolmajdy | Fingramota.kz (ARDFM financial literacy portal) | 2025-08-18 (high) | 1 | 0 | kk2_182 |
| 95 | https://live.fingramota.kz/kk/news/post/investiciyalar-salasynday-alayaty-shemalar-aldanyp-almaudy-amaldary | Fingramota.kz (ARDFM financial literacy portal) | 2025-06-16 (high) | 2 | 0 | kk2_183–kk2_184 (2) |
| 96 | https://live.fingramota.kz/kk/news/post/investiciyalayz-zhne-tabys-tabyyz-dipfejkter-zhalan-platformalara-alaj-tartady | Fingramota.kz (ARDFM financial literacy portal) | 2026-09-21 (high) | 1 | 0 | kk2_185 |
| 97 | https://live.fingramota.kz/kk/news/post/kepildendirilgen-tabys-zhne-zhyldam-asha-arzhy-piramidalary-alaj-zhmys-istejdi-zhne-adamdar-nege-milliondaryn-zhoaltuyn-zhalastyruda | Fingramota.kz (ARDFM financial literacy portal) | 2026-07-07 (high) | 3 | 0 | kk2_186–kk2_188 (3) |
| 98 | https://live.fingramota.kz/kk/news/post/kmndi-zhetkizu-alayatar-satyp-alushylar-men-satushylardy-alaj-aldajdy | Fingramota.kz (ARDFM financial literacy portal) | 2026-08-31 (high) | 3 | 0 | kk2_189–kk2_191 (3) |
| 99 | https://live.fingramota.kz/kk/news/post/leumettik-zhelilerdegi-alayaty-ziizdi-alaj-orau-kerek | Fingramota.kz (ARDFM financial literacy portal) | 2025-10-13 (high) | 1 | 0 | kk2_192 |
| 100 | https://live.fingramota.kz/kk/news/post/men-zim-asha-audardym-alayatar-alajsha-adamdardy-milliondaan-asha-beruge-mzhbrlejdi | Fingramota.kz (ARDFM financial literacy portal) | 2026-05-18 (high) | 3 | 0 | kk2_193–kk2_195 (3) |
| 101 | https://live.fingramota.kz/kk/news/post/nazar-audaryyz-alayatar-habarlamamen-shabuyldajdy-belgisiz-esim-sranystary-nemen-auipti | Fingramota.kz (ARDFM financial literacy portal) | 2026-08-09 (high) | 1 | 0 | kk2_196 |
| 102 | https://live.fingramota.kz/kk/news/post/saly-organdary-men-halya-yzmet-krsetu-ortalyynan-keletin-bayt-hattary-alayatardy-ajlasy | Fingramota.kz (ARDFM financial literacy portal) | 2025-07-21 (high) | 1 | 0 | kk2_197 |
| 103 | https://live.fingramota.kz/kk/news/post/satu-mausymy-nemese-alayaty-mausymy-alayatar-ashany-rlau-shin-zheildikter-men-zhetkizilimderdi-alaj-pajdalanady | Fingramota.kz (ARDFM financial literacy portal) | 2026-03-11 (high) | 2 | 0 | kk2_198–kk2_199 (2) |
| 104 | https://live.fingramota.kz/kk/news/post/sizdi-akkauntyyza-auip-tnip-tr-alayatar-pajdalanushylardy-kil-kjin-alaj-pajdalanady | Fingramota.kz (ARDFM financial literacy portal) | 2026-05-14 (high) | 4 | 0 | kk2_200–kk2_203 (4) |
| 105 | https://live.fingramota.kz/kk/news/post/whatsapp-y-zhaa-ater-zhne-odan-alajsha-oranu-azhet-nrda-azastandytardy-eskertedi | Fingramota.kz (ARDFM financial literacy portal) | 2026-01-14 (high) | 5 | 0 | kk2_204–kk2_208 (5) |
| 106 | https://live.fingramota.kz/kk/news/post/zejnetay-zhne-osymsha-zhmys-osymsha-tabysty-alajsha-izdeuge-zhne-arzhy-piramidasyna-tap-bolmaua-bolady | Fingramota.kz (ARDFM financial literacy portal) | 2026-06-29 (high) | 1 | 0 | kk2_209 |
| 107 | https://live.fingramota.kz/kk/news/post/zhalan-nauandardy-alajsha-tanua-zhne-derekteriizdi-oraua-bolady | Fingramota.kz (ARDFM financial literacy portal) | 2025-11-17 (high) | 2 | 0 | kk2_210–kk2_211 (2) |
| 108 | https://live.fingramota.kz/kk/news/post/zheil-ashany-ny-kdimgi-osymsha-zhmys-adamdy-dropperge-alaj-ajnaldyra-alady | Fingramota.kz (ARDFM financial literacy portal) | 2026-08-11 (high) | 7 | 0 | kk2_212–kk2_218 (7) |
| 109 | https://live.fingramota.kz/kk/news/post/smartfon-aj-kezde-osal-bolady-derekterdi-rlaudy-alty-scenariji | Fingramota.kz (ARDFM financial literacy portal) | 2026-10-27 (high) | 1 | 0 | kk2_219 |
| 110 | https://phpmyadmin.fingramota.kz/storage/app/media/kids-apps/oyla/online%20scammers/Fingramota_OYLA_KAZ.pdf | Fingramota.kz, OYLA children's magazine No.76 (PDF) | 2021-12-01 (medium) | 3 | 0 | kk2_225–kk2_227 (3) |
| 111 | https://informburo.kz/kaz/newskaz/almatyda-alaiaqtarga-aldangan-75-zastagy-qariia-men-nemeresi-uiin-qaitaruga-komek-surady | Informburo.kz | 2026-06-12 (high) | 1 | 0 | kk2_228 |
| 112 | https://informburo.kz/kaz/newskaz/paiyzsyz-nesie-qarzy-agenttigi-telegram-alayaqtarynan-abai-boluga-saqyrdy | Informburo.kz (citing Fingramota / ARDFM) | 2023-02-27 (high) | 3 | 0 | kk2_229–kk2_231 (3) |
| 113 | https://kz.kursiv.media/kk/2025-01-06/slbt-whatsapp/ | Kursiv Media Қазақстан | 2025-01-06 (high) | 1 | 0 | kk2_232 |
| 114 | https://nitec.kz/news/294 | JSC National Information Technologies (nitec.kz) | 2020-11-06 (high) | 0 | 1 | kk2_233 |
| 115 | https://nitec.kz/news/204 | JSC National Information Technologies (nitec.kz) | 2023-05-18 (high) | 0 | 1 | kk2_234 |
| 116 | https://nitec.kz/news/229 | JSC National Information Technologies (nitec.kz) | 2022-10-21 (high) | 0 | 1 | kk2_235 |
| 117 | https://nitec.kz/news/520 | JSC National Information Technologies (nitec.kz) | 2018-08-08 (high) | 0 | 1 | kk2_236 |
| 118 | https://nitec.kz/news/513 | JSC National Information Technologies (nitec.kz) | 2019-01-11 (high) | 0 | 1 | kk2_237 |
| 119 | https://nitec.kz/news/472 | JSC National Information Technologies (nitec.kz) | 2017-02-14 (high) | 0 | 1 | kk2_238 |
| 120 | https://hcsbk.kz/news/press_relize/-rmetti-klientter040626/ | Otbasy Bank (hcsbk.kz) | 2026-06-04 (high) | 0 | 1 | kk2_239 |
| 121 | https://hcsbk.kz/news/press_relize/-rmetti-klientter19032026/ | Otbasy Bank (hcsbk.kz) | 2026-03-19 (high) | 0 | 1 | kk2_240 |
| 122 | https://hcsbk.kz/news/press_relize/-rmetti-klientter190320262/ | Otbasy Bank (hcsbk.kz) | 2026-03-19 (high) | 0 | 1 | kk2_241 |
| 123 | https://hcsbk.kz/news/press_relize/-rmetti-klientter300901/ | Otbasy Bank (hcsbk.kz) | 2026-09-30 (high) | 0 | 1 | kk2_242 |
| 124 | https://hcsbk.kz/news/press_relize/uana-khabarlaymyz-tekhnikaly-zh-mystar-s-tti-aya-taldy/ | Otbasy Bank (hcsbk.kz) | 2026-06-17 (high) | 0 | 1 | kk2_243 |
| 125 | https://hcsbk.kz/news/press_relize/uvazhaemye-klienty-01-05-2026/ | Otbasy Bank (hcsbk.kz) | 2026-04-28 (high) | 0 | 1 | kk2_244 |
| 126 | https://hcsbk.kz/news/press_relize/uvazhaemye-klienty-04-07-2026/ | Otbasy Bank (hcsbk.kz) | 2026-06-30 (high) | 0 | 1 | kk2_245 |
| 127 | https://hcsbk.kz/news/press_relize/uvazhaemye-klienty-06-05-2026/ | Otbasy Bank (hcsbk.kz) | 2026-05-05 (high) | 0 | 1 | kk2_246 |
| 128 | https://hcsbk.kz/news/press_relize/uvazhaemye-klienty-11-07-2026/ | Otbasy Bank (hcsbk.kz) | 2026-07-10 (high) | 0 | 1 | kk2_247 |
| 129 | https://hcsbk.kz/news/press_relize/uvazhaemye-klienty-2026-02-26/ | Otbasy Bank (hcsbk.kz) | 2026-02-26 (high) | 0 | 1 | kk2_248 |
| 130 | https://hcsbk.kz/news/press_relize/uvazhaemye-klienty-2026-03-04/ | Otbasy Bank (hcsbk.kz) | 2026-03-03 (high) | 0 | 1 | kk2_249 |
| 131 | https://hcsbk.kz/news/press_relize/uvazhaemye-klienty-2026-03-19/ | Otbasy Bank (hcsbk.kz) | 2026-03-18 (high) | 0 | 1 | kk2_250 |
| 132 | https://hcsbk.kz/news/press_relize/uvazhaemye-klienty-8-avgusta-2026-goda-s-00-00-do-06-00/ | Otbasy Bank (hcsbk.kz) | 2026-08-03 (high) | 0 | 1 | kk2_251 |
| 133 | https://hcsbk.kz/news/press_relize/uvazhaemye-klienty-otbasy-bankakz/ | Otbasy Bank (hcsbk.kz) | 2026-07-01 (high) | 0 | 1 | kk2_252 |
| 134 | https://hcsbk.kz/news/press_relize/uvazhaemye-klienty-quanysh-ai-04-2026/ | Otbasy Bank (hcsbk.kz) | 2026-04-15 (high) | 0 | 1 | kk2_253 |
| 135 | https://hcsbk.kz/news/press_relize/uvazhaemye-klienty-rabota-messendzhera-whatsapp-vosstanovlena/ | Otbasy Bank (hcsbk.kz) | 2026-10-02 (high) | 0 | 1 | kk2_254 |
| 136 | https://hcsbk.kz/news/press_relize/uvazhaemye-klienty-s-02-00-do-06-00-20-iyunya/ | Otbasy Bank (hcsbk.kz) | 2026-06-19 (high) | 0 | 1 | kk2_255 |
| 137 | https://hcsbk.kz/news/press_relize/uvazhaemye-klienty-s-diplomom-v-selo/ | Otbasy Bank (hcsbk.kz) | 2026-04-08 (high) | 0 | 1 | kk2_256 |
| 138 | https://hcsbk.kz/news/press_relize/uvazhaemye-klienty-servisy-gons-vosstanovleny/ | Otbasy Bank (hcsbk.kz) | 2026-10-22 (high) | 0 | 1 | kk2_257 |
| 139 | https://hcsbk.kz/news/press_relize/uvazhaemye-klienty-tekhnicheskie-raboty-08-10-2026/ | Otbasy Bank (hcsbk.kz) | 2026-10-08 (high) | 0 | 1 | kk2_258 |
| 140 | https://hcsbk.kz/news/press_relize/uvazhaemye-klienty-tekhnicheskie-raboty-14-noyabrya/ | Otbasy Bank (hcsbk.kz) | 2026-11-10 (high) | 0 | 1 | kk2_259 |
| 141 | https://hcsbk.kz/news/press_relize/uvazhaemye-klienty-tekhnicheskie-raboty-zaversheny/ | Otbasy Bank (hcsbk.kz) | 2026-10-09 (high) | 0 | 1 | kk2_260 |
| 142 | https://hcsbk.kz/news/press_relize/uvazhaemye-ocheredniki-tekhnicheskie-raboty-23-25-oktyabrya/ | Otbasy Bank (hcsbk.kz) | 2026-10-23 (high) | 0 | 1 | kk2_261 |
| 143 | https://hcsbk.kz/news/press_relize/uvazhaemye-polzovateli-21022026/ | Otbasy Bank (hcsbk.kz) | 2026-02-20 (high) | 0 | 1 | kk2_262 |
| 144 | https://hcsbk.kz/news/press_relize/vnimanie-g-aktobe-ul-zhankozha-batyra-9/ | Otbasy Bank (hcsbk.kz) | 2026-06-04 (high) | 0 | 1 | kk2_263 |
| 145 | https://hcsbk.kz/news/press_relize/-rmetti-klientter08121/ | Otbasy Bank (hcsbk.kz) | 2025-12-08 (high) | 0 | 1 | kk2_264 |
| 146 | https://hcsbk.kz/news/press_relize/-rmetti-klientter1505251/ | Otbasy Bank (hcsbk.kz) | 2025-05-14 (high) | 0 | 1 | kk2_265 |
| 147 | https://hcsbk.kz/news/press_relize/-rmetti-klientter181125/ | Otbasy Bank (hcsbk.kz) | 2025-11-18 (high) | 0 | 1 | kk2_266 |
| 148 | https://hcsbk.kz/news/press_relize/-rmetti-klientter-171025/ | Otbasy Bank (hcsbk.kz) | 2025-10-17 (high) | 0 | 1 | kk2_267 |
| 149 | https://hcsbk.kz/news/press_relize/kurmetti-klientter-01052025/ | Otbasy Bank (hcsbk.kz) | 2025-04-30 (high) | 0 | 1 | kk2_268 |
| 150 | https://hcsbk.kz/news/press_relize/kurmetti-klientter-04062025/ | Otbasy Bank (hcsbk.kz) | 2025-06-03 (high) | 0 | 1 | kk2_269 |
| 151 | https://hcsbk.kz/news/press_relize/kurmetti-klientter-1000000/ | Otbasy Bank (hcsbk.kz) | 2025-06-02 (high) | 0 | 1 | kk2_270 |
| 152 | https://hcsbk.kz/news/press_relize/kurmetti-klientter-2025-03-31/ | Otbasy Bank (hcsbk.kz) | 2025-03-31 (high) | 0 | 1 | kk2_271 |
| 153 | https://hcsbk.kz/news/press_relize/kurmetti-klientter-2025-06-25/ | Otbasy Bank (hcsbk.kz) | 2025-06-25 (high) | 0 | 1 | kk2_272 |
| 154 | https://hcsbk.kz/news/press_relize/kurmetti-klientter-8-9-nauryzda/ | Otbasy Bank (hcsbk.kz) | 2025-03-07 (high) | 0 | 1 | kk2_273 |
| 155 | https://hcsbk.kz/news/press_relize/kurmetti-klientter-call-centervko-kz-06-2025/ | Otbasy Bank (hcsbk.kz) | 2025-06-20 (high) | 0 | 1 | kk2_274 |
| 156 | https://hcsbk.kz/news/press_relize/kurmetti-klientter-depozity-scheta-i-spetsialnye-scheta/ | Otbasy Bank (hcsbk.kz) | 2025-10-08 (high) | 0 | 1 | kk2_275 |
| 157 | https://hcsbk.kz/news/press_relize/kurmetti-klientter-mob-kosymshasy/ | Otbasy Bank (hcsbk.kz) | 2025-09-19 (high) | 0 | 1 | kk2_276 |
| 158 | https://hcsbk.kz/news/press_relize/kurmetti-klientter-nfd-i-epv/ | Otbasy Bank (hcsbk.kz) | 2025-09-12 (high) | 0 | 1 | kk2_277 |
| 159 | https://hcsbk.kz/news/press_relize/kurmetti-salymshylar-enpfotbasy/ | Otbasy Bank (hcsbk.kz) | 2025-04-11 (high) | 0 | 1 | kk2_278 |
| 160 | https://hcsbk.kz/news/press_relize/memlekettik-servisti-ua-ytsha-olzhetimsizdigi-turaly-khabarlama/ | Otbasy Bank (hcsbk.kz) | 2026-02-03 (high) | 0 | 1 | kk2_279 |
| 161 | https://hcsbk.kz/news/press_relize/kurmetti-klientter-otbasybank-2025-05/ | Otbasy Bank (hcsbk.kz) | 2025-05-06 (high) | 0 | 1 | kk2_280 |
| 162 | https://hcsbk.kz/news/press_relize/kurmetti-klientter-pavl-2025-09/ | Otbasy Bank (hcsbk.kz) | 2025-09-18 (high) | 0 | 1 | kk2_281 |
| 163 | https://hcsbk.kz/news/press_relize/kurmetti-klientter-10072025-00/ | Otbasy Bank (hcsbk.kz) | 2025-07-09 (high) | 0 | 1 | kk2_282 |
| 164 | https://hcsbk.kz/news/press_relize/kurmetti-klientter-aldyn-ala/ | Otbasy Bank (hcsbk.kz) | 2025-03-19 (high) | 0 | 1 | kk2_283 |

## Problems and caveats (read before reporting results)
1. **Evidence strength varies.** Most scam items are *typical example* phrasings written by an agency or outlet (MVD/police Telegram posts, Fingramota.kz articles, BCC-style lists), not recordings of real messages. Reproduced real wording is a minority: e.g. victims' quotes in Informburo (kk2 Almaty 75-year-old case), 24.kz/Baq.kz court and police reports, the deepfake "Анашым…" case. Check `notes`.
2. **Many short items.** 80 items are `fragment` (≤4 words), mostly Baq.kz headline quotes and police Telegram lists. 152 scam items are ≥5 words.
3. **Legit set is weak.** Only 3 legit items are real SMS/push texts (nitec.kz: 1414 document-expiry SMS, eGov push greeting, 1414 "no residence registration" SMS). The other 48 are official web/app notices; 45 come from one publisher (Otbasy Bank client notices). No verbatim Kazakh bank OTP or transaction SMS was found on any reachable page.
4. **No keyboard-Kazakh (kbd=true) and no Kazakh+Russian code-switched scam texts were found.** One item is Russian (a scammer outburst quoted inside a Kazakh Inbusiness article, 2021). X/Twitter search needs login (not available); Instagram/Threads not reachable.
5. **Fingramota dates** are the post date shown on the page. OYLA PDF is dated to the issue month (2021-12, medium).
6. Kind is inferred from the article context (sms vs messenger vs call); several Fingramota/BCC items do not state the channel precisely.

## Pages checked with nothing usable
- https://www.gov.kz/memleket/entities/mvd-kostanay/press/news/details/1269839 — paraphrase only
- https://www.gov.kz/memleket/entities/mvd-akmola/press/news/details/1193531?lang=kk — paraphrase only
- https://www.gov.kz/memleket/entities/aktobe-alga-sarykobda/press/news/details/1138090?lang=kk — GhostPairing warning, no message text
- https://www.gov.kz/memleket/entities/kostanai-karasy-ilichev/press/news/details/1137816?lang=kk — GhostPairing, no message text
- https://www.gov.kz/memleket/entities/mvd-zhetysu/press/news/details/1012981?lang=kk — case description only
- https://www.gov.kz/memleket/entities/prokuratura-almaty/press/news/details/1006249?lang=kk — unrelated
- https://www.gov.kz/memleket/entities/mvd-abay/press/news/details/1197521?lang=kk — no quoted text
- https://www.gov.kz/memleket/entities/mvd-abay/press/news/details/1247322?lang=kk — fake-fine SMS described, text not quoted
- https://www.gov.kz/memleket/entities/mvd-abay/press/news/details/1196809?lang=kk — same text as t.me/dp_abai/16542 (used Telegram)
- https://www.gov.kz/memleket/entities/mvd-zko/press/news/1?lang=kk — listing page; gov.kz press releases mostly paraphrase
- https://t.me/dp_abai/11076 — near-duplicate rendering of MVD top-10 list; skipped
- https://t.me/s/GenPr (searches) — mostly case reports, few quotes
- https://t.me/s/finregkz (searches) — no verbatim scam text
- https://24.kz/kz/telepoject/stop-alaak (21 other episodes, Apr-Sep 2026) — video teasers only; paraphrase
- https://24.kz/kz/zha-aly-tar/kogam/757865-alaaktar-ajylyn-zimaj-tur — statistics only
- https://kapital.kz/kk/gosudarstvo/150064/... — paraphrase only (courier SMS-code scheme)
- https://kapital.kz/kk/info/kharzhylykh-alayakhtykh ; /internet-alayakhtykh ; /alayakhtykh — paraphrase only
- https://kz.kursiv.media/kk/2026-* (22 scam-tagged articles, Apr-Nov 2026) — court/arrest reports, no scammer wording (except 2026-06-26 photo scam, used)
- https://kaz.tengrinews.kz/kazakhstan_news/*-374128, -381101, -383202, autonews -375622 — no scammer quotes
- https://inbusiness.kz/kz/news/policiya-qr-kod-..., telefonynyzga-kyska-uakytta-... — paraphrase only
- https://bes.media/news/alayaktar-whatsapp-messendzherd-bugattap-...-3dff08/ — video only
- https://baq.kz/tag/alayaqtyq/ pages 1-20 (~290 articles, 2026) — swept; most are arrest/court reports; quotes taken from 43 items
- https://www.azattyq.org search — curl failed (no response)
- egemen.kz, qamshy.kz, aikyn.kz, massaget.kz, zhasalash.kz, ult.kz, abai.kz, adyrna.kz, turkystan.kz, khabar.kz search — site search JS-only/empty or no scam results via curl; not reached in time
- https://egov.kz/cms/kk/news/* and /cms/kk/articles/* — 302 redirect to new Next.js homepage (old CMS gone); SMS templates there unreachable
- https://kgd.gov.kz/kk/node/157554 (+163812,160462,159058,138026,160668) — JS-rendered (Enonic); every node returns the same shell
- https://gov4c.kz/kz/press-center/news/343544/ (+282347,338017,333708) — JS-only shell (85 bytes text)
- https://nitec.kz/en/node/715 — SPA; content taken via public API instead (see nitec rows)
- https://halykbank.kz/kz/knowledge_base/567 (+609,2706,606,649,3339,1477,3286,941,560) — JS-rendered placeholders; 429 rate limit
- https://guide.kaspi.kz/client/kz/app/security/* (42 question pages) — only UI labels / help text; nothing new beyond prior kk set
- https://guide.kaspi.kz/client/kz/transfers/message/sms/q12684 (+q12640,q12636,q12689,q12533) — sender-name table only, no SMS text
- https://www.gov.kz/memleket/entities/ulytau-zhezkazgan/press/news/details/1015873?lang=kk — describes 1414 proactive SMS, no text
- https://24.kz/kz/zha-aly-tar/kogam/771941-... ; 730735-... — conscription SMS described, no text
- https://informburo.kz/kaz/newskaz/qazaqstandyqtar-askerden-bosatu-... — no SMS text
- https://inbusiness.kz/kz/last/askerge-shakyru-kagazdary-endi-sms-pen-egov-arkyly-zhiberiledi — no SMS text
- https://kapital.kz/kk/gosudarstvo/148842/...sms-arkhyly-habarlanady.html — amnesty SMS announced, no text
- https://www.gov.kz/memleket/entities/aktobe-irgiz/press/news/details/1133999?lang=kk — same eLicense template (already in ru2_091)
- https://www.bcc.kz/kz/about/press-center/news/ — no client notices
- kapital.kz/kk 150064 (courier SMS code) and 152048 (phishing group) — paraphrase only
- gov.kz aqmola-bulandy-nikolskoe 1186445, qriim 1279192, vko-gask 1182481, kostanai-zhitikarin 1042612, turkestan-kurylys 1090075, mvd-zhetysu 979229, aqmola-selinograd 1001975 — paraphrase only
- gov.kz ARDFM 994335, 1001936 (paraphrase); 1259403 (404)
- informburo.kz/kaz kiberqylmysqa..., internet-alayatarynan... ; inbusiness.kz/kz whatsapp-ty-pajdalanyp... ; bes.media WhatsApp 3dff08 ; forbes.kz 269122 ; 24.kz 679398, 679536, 763683 ; kaz.tengrinews 413226 (used by news slice) — no new verbatim text
- bcc.kz/kz protect-against-scammers, bcc-journal/signs-of-fraud, personal/other/bcc-safety-info, press-center/news/mery-bezopasnosti... — advice/paraphrase only
- hcsbk.kz/kz kak-rabotayut-moshenniki... ; halykbank.kz/kz/security ; alataucitybank.kz Ösim article ; kase.kz 29_04_2022_KASE_fraud_kaz.pdf — advice/paraphrase only
- homecredit.kz/kz/security, forte.kz/kz/security, bankffin.kz/kz/security, eubank.kz/kz — 404 or JS shell
- guide.kaspi.kz/client/kz/app/video/v1131, v308, v301, v1133, v319 — video titles only
- x.com search — login wall
