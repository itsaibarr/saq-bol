# RU-4 sources log (held-out real test set C, slice: Russian scam texts quoted on Kazakhstan news media)

Collected 2026-11-15, about 15:00-15:40 UTC+5 (main agent plus 2 helper agents with fixed publisher splits), following `COLLECTION_PROTOCOL_C.md`.

## Method
- Pages found with web search (Russian queries per scheme) and by following related-article links on already fetched news pages. Only the allowed KZ news domains were used; no police/government/bank sites, no Telegram, no non-.kz sites. Every URL was checked against `used_urls.txt` before fetching.
- Each page was fetched with `requests` into a scratch folder and converted to text with BeautifulSoup (`.venv/bin/python -I`). Every `text` was script-checked as an exact substring of the page text after normalising quotes, dashes, whitespace and HTML entities; scrub placeholders ([NAME] etc.) are treated as gaps.
- Deduplicated by script against every `data/real_test/*.jsonl` present at write time (including the concurrently written `ru4b_collected.jsonl` and `rucis_collected.jsonl`): exact, containment, or >=0.85 char-sequence similarity after lowercasing and stripping punctuation; within this file >=0.90. Caps enforced by script: <=12 items per publisher, <=6 per page.
- Only direct speech/text attributed to the scammer (or a genuine service text) was taken; third-person scheme descriptions, advice and headlines were skipped. `notes: typical_example` = a phrase from a published list of typical scammer wording, not one specific received message.
- `country` is `KZ` for every row (all pages are Kazakhstan media about Kazakhstan cases).

## Caveats
- Many items are short call phrases or fragments (marked `fragment` in notes); about half (48) are `typical_example` phrases from journalist/police explainers rather than a specific received message.
- Several call quotes are a victim's retelling of the caller's words (direct speech inside the victim's quote); one (Caravan, utility meters) is introduced with "мол", one (NUR, Kokshetau) is quoted inside reported speech, one Khabar item is direct speech without quote marks. Notes say so.
- Legit rows are few (fragments of genuine OTP/1414/courier-code SMS, one operator OTP, one official eGov notice); this slice found almost no verbatim bank or service SMS on fresh news pages.
- Six Tengrinews items come from one 2021 bank-sponsored article of client stories ("names changed").
- Dates: from page meta/JSON-LD; Ratel.kz dates from the visible dateline, Time.kz from the URL or dateline (date_confidence high in both cases).
- The shared web-search budget ran out at about 15:18, so later pages came only from related-article links on fetched pages.
- A few caller aliases were kept where they are the scammer's invented persona (e.g. "Дмитрий", "Михаил, из Караганды"); real private names were scrubbed.
- Two helper candidates were dropped as label-ambiguous: "К вашей карте подключены Push-уведомления" (page implies a genuine bank push triggered by fraud) and a lender's collection-threat SMS (Newtimes, sender named as a credit company, not clearly a scam).
- `used_urls.txt` was not updated by this collector; add the URLs below before the next collection.

Totals: 100 items. label={'scam': 95, 'legit': 5}; kind={'messenger': 23, 'call_quote': 57, 'sms': 6, 'web': 12, 'push': 2}; year={'2016': 1, '2020': 3, '2021': 12, '2022': 10, '2023': 2, '2024': 20, '2025': 25, '2026': 27}; publishers=20.

| Source URL | Publisher | Page date | Items (ids) | What was taken |
|---|---|---|---|---|
| https://24.kz/ru/news/economyc/789029-kurer-prosit-kod-iz-sms-kazakhstantsev-predupredili-o-skheme-moshennikov | 24KZ | 2026-08-31 | ru4_073, ru4_074, ru4_075, ru4_076 | 1 scam/call_quote; 1 scam/messenger; 1 scam/web; 1 scam/sms |
| https://24.kz/ru/news/social/694024-kursy-ot-moshennikov-ili-kak-kazakhstanets-zadolzhal-banku-9-mln-tenge | 24KZ | 2025-02-10 | ru4_079 | 1 scam/messenger |
| https://almaty.tv/ru/news/obschestvo/-857 | Almaty.tv | 2025-07-21 | ru4_008, ru4_009 | 2 scam/call_quote |
| https://bes.media/news/kto-ne-hochet-zarabotat-kak-moshenniki-ispolzuyut-korist-grazhdan-protiv-nih-50dd65/ | Bes.media | 2025-09-28 | ru4_085, ru4_086 | 2 scam/call_quote |
| https://exclusive.kz/expertiza-daily-126718/ | Exclusive.kz | 2021-12-09 | ru4_019, ru4_020 | 2 scam/call_quote |
| https://finratings.kz/news/11127-zhertvam-moshennikov-v-rk-obeshchaiut-vernut-dengi-no-grabiat-snova/ | Finratings.kz | 2026-01-27 | ru4_022 | 1 scam/messenger |
| https://finratings.kz/news/12448-kazakhstantsev-massovo-obmanyvaiut-vo-vremia-rasprodazh-vot-kak-eto-proiskhodit/ | Finratings.kz | 2026-03-11 | ru4_021 | 1 scam/sms |
| https://finratings.kz/news/5727-moshenniki-iskusno-vymanivaiut-dengi-dazhe-u-obrazovannykh-kazakhstantsev/ | Finratings.kz | 2025-07-29 | ru4_047, ru4_048 | 2 scam/call_quote |
| https://finratings.kz/news/8262-ne-verte-nalogovikam-v-trubke-novaia-moshennicheskaia-skhema-v-kazakhstane/ | Finratings.kz | 2025-10-24 | ru4_058 | 1 scam/call_quote |
| https://finratings.kz/news/8454-bloger-s-pomoshchiu-slova-tenge-obezoruzhil-telefonnogo-moshennika/ | Finratings.kz | 2025-10-30 | ru4_059 | 1 scam/call_quote |
| https://finratings.kz/news/8717-sotrudniki-banka-sami-uchastvuiut-v-skheme-kak-moshenniki-vtiraiutsia-v-doverie-zhertv/ | Finratings.kz | 2025-11-07 | ru4_046 | 1 scam/call_quote |
| https://finratings.kz/news/8825-moshenniki-atakuiut-pozhilykh-kazakhstantsev-kak-zashchititsia-ot-sotrudnika-banka/ | Finratings.kz | 2025-11-11 | ru4_050 | 1 scam/call_quote |
| https://inbusiness.kz/ru/author_news/afera-gadzhety-optom-kak-raspoznat-obman | Inbusiness.kz | 2025-01-27 | ru4_051, ru4_052, ru4_053, ru4_054 | 4 scam/web |
| https://informburo.kz/stati/kazahstancam-stali-chashe-zvonit-moshenniki-iz-polshi-vengrii-i-moldovy | Informburo.kz | 2022-08-05 | ru4_003, ru4_004 | 2 scam/call_quote |
| https://kazpravda.kz/n/moshennik-s-litsom-dzheki-chana-pytalsya-obmanut-pensionera-iz-talgara/ | Kazakhstanskaya Pravda | 2026-05-20 | ru4_067, ru4_068 | 2 scam/call_quote |
| https://kazpravda.kz/n/oni-nas-zagipnotizirovali-24-mln-tenge-vymanili-moshenniki-u-suprugov-v-kostanayskoy-oblasti/ | Kazakhstanskaya Pravda | 2022-07-28 | ru4_069, ru4_070 | 2 scam/call_quote |
| https://kazpravda.kz/n/telefon-kak-orudie-prestupleniya/ | Kazakhstanskaya Pravda | 2016-10-28 | ru4_080 | 1 scam/call_quote |
| https://khabar.kz/ru/news/obshchestvo/156710-kak-raspoznat-moshennikov-vo-vremya-telefonnogo-razgovora | Khabar | 2024-01-12 | ru4_072 | 1 scam/call_quote |
| https://khabar.kz/ru/news/obshchestvo/176765-kolichestvo-sluchaev-telefonnogo-moshennichestva-uvelichilos-v-2-raza | Khabar | 2025-09-12 | ru4_071, ru4_081 | 2 scam/call_quote |
| https://kz.kursiv.media/2022-04-19/v-arrfr-rasskazali-o-novyh-vidah-moshennichestva/ | Kursiv.media | 2022-04-19 | ru4_100 | 1 scam/call_quote |
| https://kz.kursiv.media/2023-03-10/zhnr-moshenniki/ | Kursiv.media | 2023-03-10 | ru4_084 | 1 scam/call_quote |
| https://kz.kursiv.media/2025-07-29/tri-priznaka-chto-vam-zvonit-moshennik/ | Kursiv.media | 2025-07-29 | ru4_098, ru4_099 | 2 scam/call_quote |
| https://kz.kursiv.media/2026-04-24/tsse-pensionerka-lishilas-edinstvennogo-zhilya-posle-zvonkov-lzhepoliczeiskih-v-almatinskoi-oblasti/ | Kursiv.media | 2026-04-23 | ru4_095, ru4_096 | 2 scam/call_quote |
| https://liter.kz/moshenniki-cherez-olx-obmanyvayut-kazahstanczev-na-milliony-tenge/ | Liter.kz | 2020-11-12 | ru4_010 | 1 scam/messenger |
| https://ratel.kz/raw/odin_klik_i_vy_v_lovushke_kak_izbezhat_obmana_v_whatsapp | Ratel.kz | 2024-04-09 | ru4_007 | 1 scam/messenger |
| https://ru.sputnik.kz/20240721/telefonnye-moshenniki-ustroili-rassylku-v-whatsapp-ot-imeni-akima-almaty-45804315.html | Sputnik Казахстан | 2024-07-21 | ru4_027, ru4_028 | 2 scam/call_quote |
| https://tengrinews.kz/curious/pokazyivayte-vam-zvonit-moshenniki-nauchilis-schityivat-574950/ | Tengrinews.kz | 2025-07-09 | ru4_024 | 1 scam/messenger |
| https://tengrinews.kz/healthy/karta-prosrochena-populyarnoy-sheme-moshennikov-rasskazala-568130/ | Tengrinews.kz | 2025-04-19 | ru4_023 | 1 scam/call_quote |
| https://tengrinews.kz/kazakhstan_news/rasskazali-neznakomtsu-lishnee-telefonu-eto-grozit-kak-610394/ | Tengrinews.kz | 2026-10-11 | ru4_025 | 1 scam/call_quote |
| https://tengrinews.kz/private_finance/telefonnyie-moshenniki-kazahstane-otlichit-sotrudnika-banka-430655/ | Tengrinews.kz | 2021-03-03 | ru4_011, ru4_012, ru4_013, ru4_014, ru4_015, ru4_016 | 6 scam/call_quote |
| https://tengrinews.kz/tech/whatsapp-poyavilas-hitraya-shema-moshennichestva-jertvami-458039/ | Tengrinews.kz | 2021-12-31 | ru4_002 | 1 scam/messenger |
| https://time.kz/articles/nalichnie/2026/08/21/ot-karmannyh-deneg-do-moshennikov | Time.kz | 2026-08-21 | ru4_091, ru4_092, ru4_093, ru4_094 | 4 scam/messenger |
| https://time.kz/articles/nalichnie/2026/10/28/zvonok-ot-imeni-egov | Time.kz | 2026-10-28 | ru4_082, ru4_083 | 2 scam/call_quote |
| https://time.kz/articles/risk/2022/04/01/rybaki-v-seti | Time.kz | 2022-04-01 | ru4_087, ru4_088, ru4_089 | 3 scam/messenger |
| https://time.kz/news/2024/10/16/mtsriap-ob-informatsii-o-vzlome-egov-moshenniki-polzuyutsya-ne-tehnologiej-a-doveriem-lyudej | Time.kz | 2024-10-16 | ru4_057 | 1 legit/sms |
| https://ulysmedia.kz/news/56366-ostalsia-bez-kvartiry-professor-kaken-kamzin-rasskazal-kak-stal-zhertvoi-aferistov/ | Ulysmedia.kz | 2025-08-02 | ru4_090 | 1 scam/call_quote |
| https://ulysmedia.kz/news/73785-moshenniki-s-litsom-dzheki-chana-chut-ne-vymanili-dengi-u-pensionera-v-talgare/ | Ulysmedia.kz | 2026-05-20 | ru4_097 | 1 scam/call_quote |
| https://www.caravan.kz/news/kazahstancy-rasskazali-o-novom-onlajn-moshennichestve-osobenno-opasnom-dlja-pensionerov-i-pacientov-poliklinik/ | Caravan.kz | 2026-05-20 | ru4_029, ru4_030 | 1 scam/messenger; 1 scam/call_quote |
| https://www.caravan.kz/news/my-gulyaem-na-tvoi-dengi-v-klube-ot-kibermoshennikov-v-kazakhstane-spasaet-tolko-kazakhskijj-yazyk-772119/ | Caravan.kz | 2021-09-20 | ru4_017, ru4_018 | 1 scam/messenger; 1 scam/call_quote |
| https://www.caravan.kz/society/otkuda-moshenniki-znajut-gde-vy-byli-i-kakie-dokumenty-otkryvali/ | Caravan.kz | 2025-12-04 | ru4_049 | 1 scam/call_quote |
| https://www.caravan.kz/society/u-moshennikov-teper-kazahskie-imena-i-lica-kak-k-nim-popali-dannye-kazahstancev-iz-bazy-dannyh-osms/ | Caravan.kz | 2026-04-16 | ru4_035, ru4_036 | 1 scam/call_quote; 1 legit/sms |
| https://www.inform.kz/amp/kak-moshenniki-ispol-zuyut-push-uvedomleniya-dlya-atak-na-pol-zovateley_a3963984 | Kazinform | 2022-08-07 | ru4_077, ru4_078 | 2 scam/push |
| https://www.nur.kz/incident/crime/2096909-pismo-ot-moshennikov-na-firmennom-blanke-knb-pokazali-kazahstancam/ | NUR.KZ | 2024-05-06 | ru4_031 | 1 scam/messenger |
| https://www.nur.kz/incident/crime/2135376-portal-egov-kz-obratilsya-k-kazahstancam-po-povodu-soobshcheniy-s-nomera-1414/ | NUR.KZ | 2024-07-17 | ru4_045 | 1 legit/web |
| https://www.nur.kz/incident/crime/2150526-knb-provodit-proverku-kazahstanka-perevela-15-mln-tenge-posle-sms-ot-akima/ | NUR.KZ | 2024-08-19 | ru4_026 | 1 scam/messenger |
| https://www.nur.kz/nurfin/personal/1867102-ni-na-kakie-voprosy-otvecat-ne-sobiraus-kazahstanka-dala-otpor-telefonnym-mosennikam/ | NUR.KZ | 2020-07-29 | ru4_037, ru4_038 | 2 scam/call_quote |
| https://www.nur.kz/nurfin/personal/1904150-kazahstanka-trizhdy-hodila-k-bankomatu-chtoby-perechislit-sredstva-moshennikam/ | NUR.KZ | 2021-03-25 | ru4_005 | 1 scam/call_quote |
| https://www.nur.kz/nurfin/personal/2051888-kak-kazahstantsy-teryayut-dengi-cherez-whatsapp/ | NUR.KZ | 2023-12-21 | ru4_001 | 1 scam/messenger |
| https://www.nur.kz/nurfin/personal/2115540-privez-posylku-soobshchite-kod-lzhekurery-stali-chashche-poseshchat-doma-kazahstancev/ | NUR.KZ | 2024-06-12 | ru4_043 | 1 scam/call_quote |
| https://www.nur.kz/nurfin/personal/2173989-oformili-kredit-na-2-mln-tenge-kak-moshenniki-voruyut-dengi-s-pomoshchyu-meduslug-v-kazahstane/ | NUR.KZ | 2024-10-15 | ru4_039, ru4_040 | 2 legit/sms |
| https://www.nur.kz/nurfin/personal/2272527-sboy-na-linii-kak-moshenniki-pytayutsya-obmanut-dazhe-bditelnyh-kazahstancev/ | NUR.KZ | 2025-08-07 | ru4_044 | 1 scam/call_quote |
| https://www.ratel.kz/raw/golosovye_roboty_kak_moshenniki_obmanyvajut_grazhdan | Ratel.kz | 2024-08-17 | ru4_060 | 1 scam/call_quote |
| https://www.ratel.kz/raw/kem_mogut_predstavljatsja_moshenniki_realnye_kejsy | Ratel.kz | 2024-07-14 | ru4_061, ru4_062, ru4_063, ru4_064, ru4_065 | 1 scam/call_quote; 4 scam/web |
| https://www.ratel.kz/raw/predlozhenija_ot_kotoryh_stoit_otkazatsja_kak_moshenniki_obmanyvajut_grazhdan | Ratel.kz | 2024-09-22 | ru4_055 | 1 scam/call_quote |
| https://www.ratel.kz/raw/zolotye_gory_i_legkaja_nazhiva_pochemu_nelzja_verit_obeschanijam_moshennikov | Ratel.kz | 2024-10-26 | ru4_066 | 1 scam/web |
| https://www.zakon.kz/obshestvo/6445888-pomozhem-vernut-vashi-dengi-ob-ocherednoy-ulovke-moshennikov-predupredili-kazakhstantsev.html | Zakon.kz | 2024-08-22 | ru4_041 | 1 scam/web |
| https://www.zakon.kz/obshestvo/6470052-progolosuyte-za-plemyannitsu-ili-kak-rabotayut-onlaynmoshenniki.html | Zakon.kz | 2025-03-12 | ru4_006 | 1 scam/messenger |
| https://www.zakon.kz/obshestvo/6513179-novaya-skhema-moshenniki-maskiruyutsya-pod-vrachey-i-oformlyayut-kredity-na-kazakhstantsev.html | Zakon.kz | 2026-04-02 | ru4_042 | 1 scam/call_quote |
| https://www.zakon.kz/obshestvo/6513285-politsiya-pokazala-SMS-v-WhatsApp-kotoroe-vse-kazakhstantsy-dolzhny-proignorirovat-chtoby-ne-poteryat-dengi.html | Zakon.kz | 2026-04-03 | ru4_032, ru4_033, ru4_034 | 3 scam/messenger |
| https://www.zakon.kz/obshestvo/6520429-kazakhstanka-ispugalas-ugroz-po-telefonu-nabrala-kreditov-na-5-mln-i-perevela-ikh-za-granitsu.html | Zakon.kz | 2026-06-05 | ru4_056 | 1 scam/call_quote |
