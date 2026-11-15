# RU-3 sources log (held-out real test set B)

Collected 2026-11-15 (main agent + 2 helper agents). Only Kazakhstan pages NOT in `used_urls.txt` were used; no non-KZ sources, no data/processed or runs.
Every `text` was script-checked as an exact substring of the page fetched on 2026-11-15 (after normalising quotes, dashes, whitespace, HTML entities); scrub placeholders [NAME]/[PHONE]/[CARD]/[IIN] treated as gaps.
Deduplicated against all `data/real_test/*.jsonl` (exact, containment, or >=0.85 char-sequence similarity after lowercasing/stripping punctuation) and within this file (>=0.90).
Third-person scheme descriptions and anti-fraud advice were not collected. `notes: typical_example` = phrase from a published list of typical scammer wording rather than a specific received message. Many items are short call phrases (3-6 words), not whole messages.

## Caveats
- **Short of target** (100+ scam / 40+ legit) because of the 55-minute limit: most fresh 2025-2026 KZ pages repeat phrases already in earlier slices (about 33 candidates were dropped as duplicates of existing rows, incl. the MVD top-10 phrase list).
- Legit rows are mostly MChS/akimat mass-alert push/SMS texts quoted in news; no new bank OTP/transaction samples were found on non-used pages.
- Finratings.kz `published_date` comes from page JSON-LD/meta (the visible date on the page is the fetch date).

Totals: 44 items. label={'scam': 40, 'legit': 4}; kind={'call_quote': 28, 'messenger': 5, 'web': 5, 'sms': 4, 'push': 2}; year={'2023': 2, '2025': 21, '2026': 21}.

| Source URL | Publisher | Page date | Items (ids) | What was taken |
|---|---|---|---|---|
| https://24.kz/ru/news/social/763540-kazakhstantsev-preduprezhdayut-o-novykh-skhemakh-moshennichestva | 24KZ | 2026-04-15 | ru3_001 | 1 scam/call_quote |
| https://finance.kz/articles/kak-ne-popastsya-moshennikam-v-whatsapp-v-kazahstane | Finance.kz | 2026-05-06 | ru3_002 | 1 scam/messenger |
| https://finance.kz/articles/kak-voruyut-dengi-cherez-whatsapp | Finance.kz | 2026-07-21 | ru3_003 | 1 scam/messenger |
| https://finratings.kz/news/10367-vam-posylka-kazakhstantsam-napomnili-o-novogodnikh-lovushkakh-moshennikov/ | Finratings.kz | 2025-12-30 | ru3_004 | 1 scam/sms |
| https://finratings.kz/news/11644-kazakhstantsev-preduprezhdaiut-o-novoi-skheme-moshennikov-k-14-fevralia/ | Finratings.kz | 2026-02-11 | ru3_005, ru3_006 | 2 scam/call_quote |
| https://finratings.kz/news/11867-novyi-trend-moshennikov-dengi-ischezaiut-posle-skanirovaniia-qr-koda/ | Finratings.kz | 2026-02-18 | ru3_007 | 1 scam/web |
| https://finratings.kz/news/14307-vzlomali-whatsapp-i-prosiat-dengi-chto-delat-v-pervye-24-chasa/ | Finratings.kz | 2026-05-24 | ru3_008 | 1 scam/messenger |
| https://finratings.kz/news/16113-moshenniki-pridumali-novuiu-skhemu-s-etsp-v-kazakhstane/ | Finratings.kz | 2026-08-14 | ru3_009 | 1 scam/call_quote |
| https://finratings.kz/news/16179-moshenniki-zastavliaiut-kazakhstantsev-samim-podtverzhdat-krazhu-deneg/ | Finratings.kz | 2026-08-18 | ru3_010, ru3_011, ru3_012, ru3_013, ru3_014, ru3_015 | 6 scam/call_quote |
| https://finratings.kz/news/8985-falshivye-e-mail-zastavliaiut-liudei-perevodit-dengi-moshennikam/ | Finratings.kz | 2025-11-17 | ru3_016 | 1 scam/web |
| https://finratings.kz/news/9573-kak-moshenniki-vybiraiut-zhertv-6-priznakov-chto-vy-legkaia-dobycha/ | Finratings.kz | 2025-12-04 | ru3_017, ru3_018, ru3_019 | 3 scam/call_quote |
| https://finratings.kz/news/9579-moshenniki-atakuiut-pod-vidom-pererascheta-pensii-kak-zashchititsia-kazakhstantsam/ | Finratings.kz | 2025-12-04 | ru3_020, ru3_021, ru3_022, ru3_023, ru3_024, ru3_025, ru3_026 | 7 scam/call_quote |
| https://finratings.kz/news/9656-moshenniki-smenili-taktiku-v-rk-teper-zhertva-sama-vykhodit-na-kontakt/ | Finratings.kz | 2025-12-06 | ru3_027, ru3_028 | 1 scam/sms; 1 scam/call_quote |
| https://finratings.kz/news/9666-moshennicheskaia-skhema-smotriu-na-foto-mozhet-priiti-i-v-kazakhstan/ | Finratings.kz | 2025-12-06 | ru3_029 | 1 scam/messenger |
| https://finratings.kz/news/9774-kliknul-na-iarkii-zagolovok-otdal-dostup-moshennikam-novaia-skhema/ | Finratings.kz (citing ARDFM) | 2025-12-10 | ru3_030, ru3_031, ru3_032 | 3 scam/web |
| https://kazpravda.kz/n/kiberpolitsiya-predupredila-o-novoy-sheme-s-prodleniem-sim-karty/ | Казахстанская правда | 2026-07-04 | ru3_033 | 1 scam/call_quote |
| https://polisia.kz/ru/politsejskij-spas-zhitelya-petropavlovska-ot-moshennikov-predotvrativ-poteryu-3-mln-tenge/ | Polisia.kz (ДП СКО) | 2026-10-13 | ru3_034, ru3_035, ru3_036 | 3 scam/call_quote |
| https://tengrinews.kz/article/oni-ploxo-vygovarivaiut-kazaxskie-slova-kakie-sxemy-obmana-2246/ | Tengrinews.kz | 2023-12-06 | ru3_037 | 1 scam/call_quote |
| https://tengrinews.kz/kazakhstan_news/vash-zakaz-na-sklade-kazahstantsev-predupredili-opasnyih-603185/ | Tengrinews.kz | 2026-07-03 | ru3_038 | 1 scam/call_quote |
| https://ulysmedia.kz/news/71007-v-kazakhstane-moshenniki-nashli-novyi-sposob-obmana-grazhdan/ | Ulys Media | 2026-04-02 | ru3_039 | 1 scam/call_quote |
| https://www.zakon.kz/obshestvo/6538235-kiberdetektivy-protiv-shantazha-i-ugroz-kak-kostanayskikh-shkolnikov-uchat-tsifrovoy-bezopasnosti.html | Zakon.kz | 2026-11-11 | ru3_040 | 1 scam/messenger |
| https://bes.media/news/natsionalnoe-opoveshenie-v-astane-v-mchs-soobshili-chto-ne-yavlyayutsya-initsiatorom-9cf32b/ | BES.media | 2025-03-06 | ru3_041 | 1 legit/push |
| https://finratings.kz/news/8223-vnimanie-zemletriasenie-zhiteliam-almaty-prishlo-massovoe-uvedomlenie/ | Finratings.kz | 2025-10-23 | ru3_042 | 1 legit/push |
| https://www.caravan.kz/?p=955055 | Caravan.kz | 2023-09-05 | ru3_043 | 1 legit/sms |
| https://www.nur.kz/technologies/software/2324462-kazahstancev-predupredili-o-novyh-uvedomleniyah-ot-1414/ | NUR.KZ | 2025-12-24 | ru3_044 | 1 legit/sms |
