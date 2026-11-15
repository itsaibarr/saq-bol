# RUCIS sources log (held-out real test set C, non-Kazakhstan Russian stratum)

Collected 2026-11-15 15:00-15:35 UTC+5 by one agent (43 pages used), following `COLLECTION_PROTOCOL_C.md`. This is the "CIS Russian" stratum: Russian-language scam texts from publishers outside Kazakhstan (RU/BY/UZ/KG/MD). It tests whether the model generalizes in Russian beyond KZ.

## Method
- Publishers came only from the allowed list (banki.ru, sravni.ru, rbc.ru, kommersant.ru, vedomosti.ru, fontanka.ru, belta.by, onliner.by, sb.by, sputnik.by, uz.sputniknews.ru, kun.uz, gazeta.uz, podrobno.uz, kaktus.media, akipress.org, point.md). The script rejected every forbidden training domain and all `.kz` hosts. No URL in `used_urls.txt` was used.
- Pages were fetched with `requests` into a scratch folder, text was extracted with BeautifulSoup (`.venv/bin/python -I`), and each `text` was kept only if it is an exact substring of the page text after normalising quotes, dashes, ellipsis, whitespace and HTML entities. Scrub placeholders [NAME]/[PHONE]/[CARD] count as gaps of up to 80 characters.
- Dedup: compared with every other `data/real_test/*.jsonl` (exact match, containment, or >=0.85 SequenceMatcher ratio after lowercasing and stripping punctuation), and within this file (>=0.90). Caps: at most 12 items per publisher and 6 per page.
- Scrubbing: private people's names and scammer aliases -> [NAME], phone numbers -> [PHONE], account digits -> [CARD]. Bank hotline numbers that appear in genuine bank SMS were kept.
- `notes: typical_example` = a phrase from a published list of typical scammer wording (MVD, Bank of Russia, police or bank warnings), not a specific received message. Section headers that only quote a scheme name were excluded (7 candidates dropped), as were third-person retellings.
- `country` = country of the publisher/audience. Two pages reprint material from elsewhere: Fontanka 2024-11-11 reprints an E1.RU (Yekaterinburg) call transcript, and Sravni 2021-10-05 quotes a leaked call-centre script first published by Strana.ua.

## Caveats
- **The shared WebSearch budget ran out mid-session.** After that, sources were found only by following related-article and tag links on pages already fetched from allowed publishers. Coverage of MD (newsmaker.md returned HTTP 403 to scripted fetches; point.md briefs are mostly paraphrase) and of UZ/KG is therefore thin.
- **Legit side is small (6):** a VTB SBP-subscription alert quoted by a victim, the Gosuslugi login-code template, bank cash-desk and post-office code wording (Sravni), a Belarus MChS test SMS and a Kyrgyz MChS SMS heading.
- Many scam items are short call fragments or list phrases. Victim and journalist transcripts make up the longer items: Fontanka 2021/2022/2024, Sputnik BY 2020, Kaktus 2025, banki.ru reviews.
- banki.ru reviews from 2013 are old SMS formats ("Заявка на списание ... Инф:"). Kun.uz 2020 (rucis_075) is a deceptive premium-SMS "winner" mailing that the regulator ruled misleading advertising; its scam label is debatable.
- 10 candidates were dropped as duplicates of rows already in ru/ru2/ru2_A3frozen/ru3/ru4b. ru4b was being written at the same time, so dedup was re-run at the end.
- Point.md 2023-11-13 and Kaktus 2025-02-19 dates come from page metadata/HTML timestamps (Point.md marked low confidence).

Totals: 93 items. label={'scam': 87, 'legit': 6}; country={'RU': 49, 'BY': 21, 'KG': 12, 'UZ': 10, 'MD': 1}; kind={'call_quote': 48, 'messenger': 23, 'sms': 17, 'web': 5}; year={'2013': 4, '2020': 7, '2021': 11, '2022': 5, '2023': 9, '2024': 12, '2025': 30, '2026': 15}; publishers=17: {'Фонтанка.ру': 12, 'РБК': 8, 'Сравни.ру': 12, 'Onliner': 6, 'СБ. Беларусь сегодня': 5, 'БелТА': 5, 'Sputnik Узбекистан': 3, 'Kaktus.media': 10, 'Коммерсантъ': 4, 'Ведомости': 3, 'Банки.ру': 10, 'Point.md': 1, 'Gazeta.uz': 2, 'AKIpress': 2, 'Kun.uz': 4, 'Podrobno.uz': 1, 'Sputnik Беларусь': 5}.

| Source URL | Publisher | Page date | Items (ids) | What was taken |
|---|---|---|---|---|
| https://www.fontanka.ru/2021/04/19/69873065/ | Фонтанка.ру (RU) | 2021-04-19 | rucis_001, rucis_002, rucis_003, rucis_004, rucis_005, rucis_006 | 6 scam/call_quote |
| https://www.rbc.ru/rbcfreenews/695775a79a79472006a3f4ba | РБК (RU) | 2026-01-02 | rucis_007, rucis_008, rucis_009, rucis_010, rucis_011 | 5 scam/call_quote |
| https://www.rbc.ru/life/news/677f52779a7947dee10721bd | РБК (RU) | 2025-01-09 | rucis_012 | 1 scam/web |
| https://www.sravni.ru/q/kak-raspoznat-i-protivostojat-socialnoj-inzhenerii-65724/ | Сравни.ру (RU) | 2024-06-20 | rucis_013, rucis_014, rucis_015, rucis_016, rucis_017 | 3 scam/call_quote; 1 scam/messenger; 1 scam/sms |
| https://money.onliner.by/2025/06/24/sxemy-moshennikov | Onliner (BY) | 2025-06-24 | rucis_018, rucis_019 | 1 scam/call_quote; 1 scam/messenger |
| https://www.sb.by/articles/feykovyy-boss-i-vam-podarok-v-militsii-rasskazali-o-samykh-rasprostranennykh-moshennicheskikh-skhema.html | СБ. Беларусь сегодня (BY) | 2025-03-27 | rucis_020 | 1 scam/messenger |
| https://belta.by/society/view/vash-rodstvennik-v-bede-kakie-legendy-ispolzujut-telefonnye-moshenniki-rasskazali-v-militsii-801460-2026 | БелТА (BY) | 2026-09-17 | rucis_021, rucis_022, rucis_023, rucis_091 | 4 scam/call_quote |
| https://money.onliner.by/2023/03/17/mama-kak-budto-byla-v-gipnoze | Onliner (BY) | 2023-03-17 | rucis_024 | 1 scam/messenger |
| https://uz.sputniknews.ru/20231118/zvonok-moshennik-kraja-dengi-karta-otvet-sb-41105407.html | Sputnik Узбекистан (UZ) | 2023-11-18 | rucis_025, rucis_026 | 1 scam/messenger; 1 scam/web |
| https://kaktus.media/doc/523216_kodovoe_slovo_iabloko._ychitel_shkoly_prodala_kvartiry_i_vyslala_dengi_moshennikam.html | Kaktus.media (KG) | 2025-05-06 | rucis_027, rucis_028, rucis_029, rucis_030, rucis_031, rucis_032 | 2 scam/messenger; 4 scam/call_quote |
| https://kaktus.media/doc/533616_telefonnye_moshenniki_atakyut:_samye_popyliarnye_shemy_seychas_i_kak_zashititsia.html | Kaktus.media (KG) | 2025-10-17 | rucis_033 | 1 scam/call_quote |
| https://www.fontanka.ru/2024/11/11/74310572/ | Фонтанка.ру (RU) | 2024-11-11 | rucis_034, rucis_035 | 2 scam/call_quote |
| https://www.fontanka.ru/2022/04/28/71293361/ | Фонтанка.ру (RU) | 2022-04-28 | rucis_036, rucis_037 | 2 scam/call_quote |
| https://www.fontanka.ru/2025/11/19/76129769/ | Фонтанка.ру (RU) | 2025-11-19 | rucis_038, rucis_088 | 2 scam/messenger |
| https://www.rbc.ru/rbcfreenews/658c75d89a79471771e153ff | РБК (RU) | 2023-12-27 | rucis_039, rucis_040 | 2 scam/call_quote |
| https://www.kommersant.ru/doc/8247881 | Коммерсантъ (RU) | 2025-11-29 | rucis_041, rucis_042, rucis_043, rucis_044 | 4 scam/messenger |
| https://www.vedomosti.ru/society/news/2025/07/07/1122507-v-mvd-predupredili | Ведомости (RU) | 2025-07-07 | rucis_045, rucis_046 | 2 scam/messenger |
| https://www.vedomosti.ru/society/news/2025/08/19/1132704-mvd-moshenniki | Ведомости (RU) | 2025-08-19 | rucis_047 | 1 scam/web |
| https://www.banki.ru/services/responses/bank/response/5926053/ | Банки.ру (RU) | 2013-11-29 | rucis_048 | 1 scam/sms |
| https://www.banki.ru/services/responses/bank/response/11727710/ | Банки.ру (RU) | 2024-09-07 | rucis_049, rucis_050 | 1 scam/sms; 1 legit/sms |
| https://www.banki.ru/services/responses/bank/response/5218082/ | Банки.ру (RU) | 2013-07-23 | rucis_051 | 1 scam/sms |
| https://www.banki.ru/services/responses/bank/response/4749941/ | Банки.ру (RU) | 2013-04-03 | rucis_052, rucis_053 | 1 scam/sms; 1 scam/call_quote |
| https://www.banki.ru/services/questions-answers/question/725401/ | Банки.ру (RU) | 2025-03-19 | rucis_054 | 1 scam/sms |
| https://www.banki.ru/news/daytheme/?id=11019614 | Банки.ру (RU) | 2025-11-25 | rucis_055, rucis_089, rucis_090 | 1 scam/sms; 2 scam/call_quote |
| https://point.md/ru/novosti/obschestvo/ts-moshenniki-pytaiutsia-vymogat-den-gi-pod-vidom-sbora-za-posylki/ | Point.md (MD) | 2023-11-13 | rucis_056 | 1 scam/sms |
| https://belta.by/society/view/sistema-opoveschenija-proverjaetsja-v-belarusi-abonenty-dvuh-mobilnyh-operatorov-poluchat-sms-380360-2020/ | БелТА (BY) | 2020-02-20 | rucis_057 | 1 legit/sms |
| https://kaktus.media/doc/494397_call_centr:_mchs_sdelalo_rassylky_no_ego_sayt_ne_rabotaet_otvet_ministerstva.html | Kaktus.media (KG) | 2024-01-23 | rucis_058 | 1 legit/sms |
| https://www.gazeta.uz/ru/2025/03/13/octobank/ | Gazeta.uz (UZ) | 2025-03-13 | rucis_059, rucis_060 | 2 scam/messenger |
| https://kaktus.media/doc/518177_postradavshaia_ot_ljesotrydnikov_gknb_vrach_prosit_tashieva_vziat_delo_pod_lichnyy_kontrol.html | Kaktus.media (KG) | 2025-02-19 | rucis_061 | 1 scam/call_quote |
| https://money.onliner.by/2023/11/21/zarplata-630-v-nedelyu-nado-prosto-obygrat-kazino-novyj-razvod-v-seti | Onliner (BY) | 2023-11-21 | rucis_062 | 1 scam/messenger |
| https://www.sravni.ru/text/13-fraz-po-kotorym-mozhno-vychislit-telefonnyh-moshennikov/ | Сравни.ру (RU) | 2021-10-05 | rucis_063, rucis_064, rucis_065, rucis_066 | 4 scam/call_quote |
| https://www.sravni.ru/text/mosshennichestvo-ot-imeni-sravni-i-drugih-kompanii/ | Сравни.ру (RU) | 2025-02-26 | rucis_067, rucis_068, rucis_069 | 3 legit/sms |
| https://kg.akipress.org/news:1851308/ | AKIpress (KG) | 2023-01-19 | rucis_070, rucis_071 | 2 scam/sms |
| https://www.sb.by/articles/ne-zaprashivayut-paroli-i-ne-toropyat-v-belpochte-napomnili-kak-raspoznat-moshennika-pod-vidom-ikh-r.html | СБ. Беларусь сегодня (BY) | 2026-06-29 | rucis_072, rucis_073, rucis_074, rucis_093 | 3 scam/call_quote; 1 scam/messenger |
| https://kun.uz/ru/news/2020/05/21/abonenty-beeline-poteryali-do-1-mlrd-sumov-iz-za-nedostovernoy-rassylki | Kun.uz (UZ) | 2020-05-21 | rucis_075 | 1 scam/sms |
| https://podrobno.uz/cat/tehnp/vladeltsev-plastikovykh-kart-v-uzbekistane-atakuyut-moshenniki-/ | Podrobno.uz (UZ) | 2020-11-12 | rucis_076 | 1 scam/web |
| https://kun.uz/ru/news/2022/09/24/dengi-na-lecheniye-moyey-materi-stali-dobychey-moshennikov-istoriya-molodogo-cheloveka-iz-surxandari | Kun.uz (UZ) | 2022-09-24 | rucis_077, rucis_078, rucis_092 | 2 scam/messenger; 1 scam/web |
| https://money.onliner.by/2024/11/27/kak-razvodyat-blizkix | Onliner (BY) | 2024-11-27 | rucis_079 | 1 scam/call_quote |
| https://tech.onliner.by/2024/09/18/120-i-ya-ostavlyu-tebya-v-pokoe-moshennik-zablokiroval-iphone-beloruski-i-potreboval-vykup | Onliner (BY) | 2024-09-18 | rucis_080 | 1 scam/messenger |
| https://kaktus.media/doc/543890_lishilas_kvartiry_posle_telefonnogo_zvonka._pensionerka_obratilas_k_prezidenty.html | Kaktus.media (KG) | 2026-04-08 | rucis_081 | 1 scam/call_quote |
| https://sputnik.by/20201223/Vam-zvonyat-iz-banka-kak-internet-moshenniki-razvodyat-belorusov-1046456349.html | Sputnik Беларусь (BY) | 2020-12-23 | rucis_082, rucis_083, rucis_084, rucis_085 | 4 scam/call_quote |
| https://sputnik.by/20261114/chat-perenositsya-v-novuyu-gruppu-moshenniki-massovo-atakuyut-v-telegram-1112740650.html | Sputnik Беларусь (BY) | 2026-11-14 | rucis_086 | 1 scam/messenger |
| https://uz.sputniknews.ru/20210603/sposoby-obmana-po-telefonu--osteregaytes-moshennikov-19061800.html | Sputnik Узбекистан (UZ) | 2021-06-03 | rucis_087 | 1 scam/call_quote |
