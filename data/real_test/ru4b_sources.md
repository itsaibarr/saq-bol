# RU-4b sources log (held-out real test set C, slice: KZ official / bank / operator / public Telegram)

Collected 2026-11-15 15:00-16:10 (UTC+5) by one agent, following `COLLECTION_PROTOCOL_C.md`. Only Kazakhstan official, bank, operator sites and public `t.me/s/` previews of KZ official channels were used; no news media, no non-KZ sites.

## Method

- Pages fetched with `requests` (curl fallback for live.fingramota.kz, whose TLS chain fails in requests) into the session scratchpad; text extracted with BeautifulSoup (`.venv/bin/python -I`). Every `text` is an exact substring of the fetched page text after normalising quotes, dashes, whitespace and HTML entities; [NAME]/[PHONE]/[CARD]/[IIN] treated as gaps.
- Discovery: polisia.kz WordPress REST API (ru, 2025-2026 posts matching мошенник/звонк/сообщени/представил); gov.kz news listings of 18 regional police departments (pages 1-34) filtered by fraud keywords; live.fingramota.kz/ru news listing; Bank RBK 'Вниманию клиентов' notice series; t.me/s/ previews of @POLICE_of_KZ, @dp_abai, @dp_zhetysu, @kaspikz, @enpfkz, @egov_kz, @kazhydromet, @finregkz, @afm_rk; a few bank/operator fraud pages found by web search.
- Skipped every URL in `used_urls.txt` and every `source_url` already in `data/real_test/*.jsonl` (ru3 sources are not yet in used_urls.txt). Deduplicated against all `data/real_test/*.jsonl` (exact, containment, >=0.85 SequenceMatcher after lowercasing/stripping punctuation) and within file (>=0.90). Caps: <=12 per publisher, <=6 per page.
- Telegram items: `source_url` is the post permalink `https://t.me/<channel>/<id>`; verification page was the public preview `https://t.me/s/<channel>/<id>` fetched the same day.

## Caveats

- **Scam target missed: 35 of 50+.** The web-search budget ran out mid-session, and most fresh official pages repeat phrases already in earlier slices (about 20 candidates dropped as duplicates, e.g. the voting-link lure, 'Скинь 80 тысяч', WhatsApp 'START' messages, SIM-renewal call). Another 11 verified fingramota phrases were dropped only by the 12-per-publisher cap.
- **Legit items are not SMS samples.** No official KZ page in reach showed verbatim bank OTP/transaction or eGov/ЕНПФ SMS wording (egov.kz is now a client-side app with no server HTML; Kaspi/Halyk help pages describe sender names only). The 40 legit rows are (a) 10 Bank RBK client notices (web, 2016-2022, tech works, branch hours, tariff and deferral notices), (b) 30 official Telegram broadcast posts from Kaspi.kz, ЕНПФ, eGov (2020-2022) and Казгидромет storm/fire-danger alerts. They measure false alarms on official bank/government messages but are a different register from SMS; Kaspi posts are partly promotional.
- Publisher interpretation: gov.kz police departments (separate entity sections) and each Telegram channel are counted as separate publishers; polisia.kz, live.fingramota.kz and bankrbk.kz each hit the 12 cap. Polisia.kz and gov.kz police pages often carry the same press release; within-file dedupe removed the overlaps.
- live.fingramota.kz/ru posts are Russian versions of a site whose Kazakh posts were used by earlier slices; the Russian URLs were not in used_urls.txt, and the Russian texts passed the cross-file dedupe, but a few may be translations of articles whose kk versions fed earlier sets.
- Most scam rows are `typical_example` phrases (short call lines) from police or regulator lists, not a specific received message. Two rows (beeline.kz fraud page, Bank RBK security page) have no visible page date; `published_date` is the fetch date with `date_confidence: low`.

Totals: 75 items. label={'scam': 35, 'legit': 40}; language={'ru': 74, 'kk': 1}; kind={'call_quote': 23, 'messenger': 37, 'web': 15}; year={'2016': 1, '2020': 4, '2021': 5, '2022': 9, '2025': 4, '2026': 52}; publishers=14.

| Source URL | Publisher | Page date | Items (ids) | What was taken |
|---|---|---|---|---|
| https://polisia.kz/ru/politsiya-preduprezhdaet-o-rasprostranennoj-sheme-internet-moshennichestva/ | Polisia.kz | 2025-08-14 | ru4b_001, ru4b_002 | 2 scam/call_quote |
| https://polisia.kz/ru/internet-moshennichestvo-na-5-mln-tenge-rassleduyut-politsejskie-v-sko/ | Polisia.kz | 2025-12-18 | ru4b_003 | 1 scam/call_quote |
| https://polisia.kz/ru/novyj-podhod-k-profilaktike-internet-moshennichestva-realizuyut-v-sko/ | Polisia.kz | 2026-05-15 | ru4b_004, ru4b_005, ru4b_006, ru4b_007 | 4 scam/call_quote |
| https://polisia.kz/ru/politsejskie-preduprezhdayut-grazhdan-ob-opasnyh-shemah-internet-moshennichestva-v-oblasti-ulytau/ | Polisia.kz | 2026-08-20 | ru4b_008, ru4b_035 | 2 scam/call_quote |
| https://polisia.kz/ru/politsiya-preduprezhdaet-o-novyh-shemah-internet-moshennichestva/ | Polisia.kz | 2026-07-03 | ru4b_009, ru4b_010 | 2 scam/call_quote |
| https://live.fingramota.kz/ru/news/post/ya-sama-perevela-dengi-kak-moshenniki-zastavlyayut-lyudej-otdavat-milliony | Fingramota.kz (live.fingramota.kz) | 2026-05-18 | ru4b_011, ru4b_012, ru4b_013 | 3 scam/call_quote |
| https://live.fingramota.kz/ru/news/post/zvonok-ot-imeni-egov-kak-moshenniki-ispolzuyut-gosudarstvennye-servisy-v-svoih-shemah | Fingramota.kz (live.fingramota.kz) | 2026-09-30 | ru4b_014, ru4b_015 | 2 scam/call_quote |
| https://live.fingramota.kz/ru/news/post/dengi-v-odin-klik-kak-moshenniki-obmanyvayut-v-messendzherah | Fingramota.kz (live.fingramota.kz) | 2026-11-11 | ru4b_016 | 1 scam/messenger |
| https://live.fingramota.kz/ru/news/post/cena-legkih-deneg-kak-obychnaya-podrabotka-mozhet-prevratit-cheloveka-v-droppera | Fingramota.kz (live.fingramota.kz) | 2026-08-11 | ru4b_017, ru4b_018 | 1 scam/web; 1 scam/messenger |
| https://live.fingramota.kz/ru/news/post/dve-shemy-internet-moshennikov-kotorye-mogut-ostavit-vas-s-dolgami | Fingramota.kz (live.fingramota.kz) | 2026-07-26 | ru4b_019, ru4b_020 | 1 scam/web; 1 scam/messenger |
| https://live.fingramota.kz/ru/news/post/investirujte-i-zarabatyvajte-kak-dipfejki-zamanivayut-na-falshivye-platformy | Fingramota.kz (live.fingramota.kz) | 2026-09-21 | ru4b_021 | 1 scam/messenger |
| https://live.fingramota.kz/ru/news/post/my-vernem-vashi-dengi-kak-moshenniki-zamanivayut-zhertv-v-novuyu-lovushku | Fingramota.kz (live.fingramota.kz) | 2026-08-17 | ru4b_022 | 1 scam/messenger |
| https://www.gov.kz/memleket/entities/mvd-shymkent/press/news/details/1308388?lang=ru | ДП г. Шымкент (gov.kz) | 2026-10-09 | ru4b_023, ru4b_024 | 1 scam/call_quote; 1 scam/web |
| https://www.gov.kz/memleket/entities/mvd-karaganda/press/news/details/1255973?lang=ru | ДП Карагандинской области (gov.kz) | 2026-07-09 | ru4b_025 | 1 scam/call_quote |
| https://bankrbk.kz/ru/security/novosti/kak-zashchititsya-ot-moshennikov | Bank RBK (bankrbk.kz) | 2026-11-15 | ru4b_026 | 1 scam/messenger |
| https://t.me/kaspikz/676 | Kaspi.kz (Telegram @kaspikz) | 2025-07-27 | ru4b_027 | 1 scam/web |
| https://beeline.kz/ru/fraud | Beeline Казахстан (beeline.kz) | 2026-11-15 | ru4b_028 | 1 scam/call_quote |
| https://www.gov.kz/memleket/entities/mvd-abay/press/news/details/1254050?lang=ru | ДП области Абай (gov.kz) | 2026-07-07 | ru4b_029, ru4b_030 | 2 scam/call_quote |
| https://www.gov.kz/memleket/entities/mvd-aktobe/press/news/details/1265156?lang=ru | ДП Актюбинской области (gov.kz) | 2026-07-29 | ru4b_031 | 1 scam/call_quote |
| https://www.gov.kz/memleket/entities/mvd-atyrau/press/news/details/1263946?lang=ru | ДП Атырауской области (gov.kz) | 2026-07-27 | ru4b_032, ru4b_033 | 1 scam/web; 1 scam/messenger |
| https://www.gov.kz/memleket/entities/mvd-kyzylorda/press/news/details/1273327?lang=ru | ДП Кызылординской области (gov.kz) | 2026-08-13 | ru4b_034 | 1 scam/call_quote |
| https://bankrbk.kz/ru/media/novosti/vnimaniyu-klientov-6 | Bank RBK (bankrbk.kz) | 2020-01-22 | ru4b_036 | 1 legit/web |
| https://bankrbk.kz/ru/media/novosti/vnimaniyu-klientov-1 | Bank RBK (bankrbk.kz) | 2016-07-19 | ru4b_037 | 1 legit/web |
| https://bankrbk.kz/ru/media/novosti/vnimaniyu-klientov-17 | Bank RBK (bankrbk.kz) | 2022-01-13 | ru4b_038 | 1 legit/web |
| https://bankrbk.kz/ru/media/novosti/vnimaniyu-klientov-20 | Bank RBK (bankrbk.kz) | 2022-01-24 | ru4b_039 | 1 legit/web |
| https://bankrbk.kz/ru/media/novosti/vnimaniyu-klientov-21 | Bank RBK (bankrbk.kz) | 2022-02-14 | ru4b_040 | 1 legit/web |
| https://bankrbk.kz/ru/media/novosti/vnimaniyu-klientov-28 | Bank RBK (bankrbk.kz) | 2022-06-14 | ru4b_041 | 1 legit/web |
| https://bankrbk.kz/ru/media/novosti/vnimaniyu-klientov-40 | Bank RBK (bankrbk.kz) | 2022-10-14 | ru4b_042 | 1 legit/web |
| https://bankrbk.kz/ru/media/novosti/vnimaniyu-klientov-38 | Bank RBK (bankrbk.kz) | 2022-10-11 | ru4b_043 | 1 legit/web |
| https://bankrbk.kz/ru/media/novosti/vnimaniyu-klientov-44 | Bank RBK (bankrbk.kz) | 2022-12-01 | ru4b_044 | 1 legit/web |
| https://bankrbk.kz/ru/media/novosti/vnimaniyu-klientov-24 | Bank RBK (bankrbk.kz) | 2022-04-27 | ru4b_045 | 1 legit/web |
| https://t.me/kaspikz/980 | Kaspi.kz (Telegram @kaspikz) | 2026-11-13 | ru4b_046 | 1 legit/messenger |
| https://t.me/kaspikz/967 | Kaspi.kz (Telegram @kaspikz) | 2026-10-21 | ru4b_047 | 1 legit/messenger |
| https://t.me/kaspikz/875 | Kaspi.kz (Telegram @kaspikz) | 2026-05-20 | ru4b_048 | 1 legit/messenger |
| https://t.me/kaspikz/874 | Kaspi.kz (Telegram @kaspikz) | 2026-05-14 | ru4b_049 | 1 legit/messenger |
| https://t.me/kaspikz/864 | Kaspi.kz (Telegram @kaspikz) | 2026-04-30 | ru4b_050 | 1 legit/messenger |
| https://t.me/kaspikz/919 | Kaspi.kz (Telegram @kaspikz) | 2026-07-16 | ru4b_051 | 1 legit/messenger |
| https://t.me/kaspikz/933 | Kaspi.kz (Telegram @kaspikz) | 2026-08-14 | ru4b_052 | 1 legit/messenger |
| https://t.me/kaspikz/876 | Kaspi.kz (Telegram @kaspikz) | 2026-05-23 | ru4b_053 | 1 legit/messenger |
| https://t.me/kaspikz/938 | Kaspi.kz (Telegram @kaspikz) | 2026-08-26 | ru4b_054 | 1 legit/messenger |
| https://t.me/kaspikz/923 | Kaspi.kz (Telegram @kaspikz) | 2026-07-23 | ru4b_055 | 1 legit/messenger |
| https://t.me/kaspikz/922 | Kaspi.kz (Telegram @kaspikz) | 2026-07-21 | ru4b_056 | 1 legit/messenger |
| https://t.me/enpfkz/3882 | ЕНПФ (Telegram @enpfkz) | 2026-10-06 | ru4b_057 | 1 legit/messenger |
| https://t.me/enpfkz/3653 | ЕНПФ (Telegram @enpfkz) | 2026-01-12 | ru4b_058 | 1 legit/messenger |
| https://t.me/enpfkz/3661 | ЕНПФ (Telegram @enpfkz) | 2026-01-16 | ru4b_059 | 1 legit/messenger |
| https://t.me/enpfkz/3818 | ЕНПФ (Telegram @enpfkz) | 2026-06-05 | ru4b_060 | 1 legit/messenger |
| https://t.me/enpfkz/3805 | ЕНПФ (Telegram @enpfkz) | 2026-05-21 | ru4b_061 | 1 legit/messenger |
| https://t.me/egov_kz/35 | eGov Казахстан (Telegram @egov_kz) | 2022-04-22 | ru4b_062 | 1 legit/messenger |
| https://t.me/egov_kz/31 | eGov Казахстан (Telegram @egov_kz) | 2021-09-29 | ru4b_063 | 1 legit/messenger |
| https://t.me/egov_kz/32 | eGov Казахстан (Telegram @egov_kz) | 2021-09-29 | ru4b_064 | 1 legit/messenger |
| https://t.me/egov_kz/18 | eGov Казахстан (Telegram @egov_kz) | 2020-04-06 | ru4b_065 | 1 legit/messenger |
| https://t.me/egov_kz/33 | eGov Казахстан (Telegram @egov_kz) | 2021-10-20 | ru4b_066 | 1 legit/messenger |
| https://t.me/egov_kz/21 | eGov Казахстан (Telegram @egov_kz) | 2020-07-18 | ru4b_067 | 1 legit/messenger |
| https://t.me/egov_kz/23 | eGov Казахстан (Telegram @egov_kz) | 2020-12-14 | ru4b_068 | 1 legit/messenger |
| https://t.me/egov_kz/24 | eGov Казахстан (Telegram @egov_kz) | 2021-02-17 | ru4b_069 | 1 legit/messenger |
| https://t.me/egov_kz/27 | eGov Казахстан (Telegram @egov_kz) | 2021-07-22 | ru4b_070 | 1 legit/messenger |
| https://t.me/kazhydromet/3034 | Казгидромет (Telegram @kazhydromet) | 2026-11-13 | ru4b_071 | 1 legit/messenger |
| https://t.me/kazhydromet/3030 | Казгидромет (Telegram @kazhydromet) | 2026-11-13 | ru4b_072 | 1 legit/messenger |
| https://t.me/kazhydromet/3024 | Казгидромет (Telegram @kazhydromet) | 2026-11-12 | ru4b_073 | 1 legit/messenger |
| https://t.me/kazhydromet/2993 | Казгидромет (Telegram @kazhydromet) | 2026-11-10 | ru4b_074 | 1 legit/messenger |
| https://t.me/kazhydromet/2953 | Казгидромет (Telegram @kazhydromet) | 2026-11-09 | ru4b_075 | 1 legit/messenger |
