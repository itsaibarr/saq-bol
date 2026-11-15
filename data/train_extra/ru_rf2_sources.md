# ru_rf2_collected.jsonl: sources

Second batch, collected 2026-11-15 for TRAINING only (not test). Real Russian-language scam texts quoted word for word by the publishers below, plus a few genuine bank/service SMS quoted as legit. Same schema as `ru_rf_collected.jsonl` plus `id` (`rurf2_001`...).

## Publisher rules applied

- Only these publishers were used: t-j.ru, habr.com, lifehacker.ru, kaspersky.ru, tbank.ru (incl. secrets.tbank.ru), vtb.ru, sberbank.ru, myfin.by, journal.sovcombank.ru, finuslugi.ru, securitylab.ru, iguides.ru, lenta.ru, ria.ru, kp.ru, aif.ru, mk.ru (regional subdomains of kp.ru/aif.ru/mk.ru included). A script rejected any URL outside the allow-list or on the forbid-list (all .kz, banki.ru, sravni.ru, rbc.ru, kommersant.ru, vedomosti.ru, fontanka.ru, mvd.ru, belta.by, onliner.by, sb.by, kun.uz, gazeta.uz, daryo.uz, 24.kg, kaktus.media, akipress.org, newsmaker.md, point.md, sputnik).
- Items whose text mentions Kazakhstan, Kaspi, tenge or eGov were dropped (regex check on every text).

## Method

- Pages fetched with curl (T-J with its `?mc_attempt=1` fallback) and saved as untrusted files; HTML converted to text with BeautifulSoup. URLs came from the T-J articles and community sitemaps (slug keyword filter), web search restricted to the allowed domains, and listing pages (Lenta cybercrime rubric, iGuides security, Anti-Malware news, Sovcombank journal tag).
- Candidate extractors: text inside «…»/“…”; dialogue lines starting with `— `; speaker-labelled transcript lines (`Мошенник:`, `Следователь:`, `"Сотрудник" Росфинмониторинга:` and the line after such labels); and standalone example-message paragraphs in guides (e.g. Lifehacker's "Как может выглядеть сообщение").
- Every kept row was hand-picked as a scammer turn (SMS, messenger message, email or call line) and hand-labelled with a scheme. Narrator text, advice, victim replies and paraphrases ("мошенники говорят, что...") were skipped. Where narrator text was glued to a quote, the quote was cut to a verbatim sub-span at a sentence boundary. The news-site rows (lenta/ria/kp/aif/mk) were picked by a parallel sub-agent with the same rules; I spot-checked a random 40 and scanned all rows for narrator words.
- Verbatim check by script: each text (before scrubbing) is an exact substring of the whitespace-normalised page text; after scrubbing, a second independent check (BeautifulSoup `get_text` of the whole page, placeholders as wildcards) matched 665/665 rows.
- Scrubbing: phone numbers -> [PHONE], card numbers -> [CARD], first names / name+patronymic / surnames of personas and victims -> [NAME] (50 rows contain a placeholder). Inline placeholders already present in the source such as `[ссылка]`, `[ХХХХ]` were kept as published.
- Dedupe: on lowercased alphanumerics against all 344 rows of `ru_rf_collected.jsonl` (exact and containment) and within this file (exact and containment; the shorter of two contained variants was dropped).

## Counts

- total 665: scam 651, legit 14
- by scheme: scam/fake_law_enforcement 99, scam/bank_security 84, scam/delivery 70, scam/other 41, scam/job 40, scam/mobile_operator 39, scam/relatives 35, scam/utilities 30, scam/investment 28, scam/fake_friend 26, scam/marketplace 22, scam/safe_account 21, scam/social_payout 19, scam/fake_acquaintance 16, scam/gosuslugi 16, scam/fake_boss 12, scam/sms_code 10, scam/loan_in_your_name 9, legit/otp_code 9, scam/prize 8, scam/phishing_link 6, scam/tech_support 6, scam/mistaken_transfer 5, scam/tax_refund 4, legit/bank_call 3, scam/recovery_scam 2, legit/bank_marketing 1, legit/notification 1, scam/insurance 1, scam/telegram_gift 1, scam/rental 1
- by publisher: Т—Ж / T-Bank Journal (journal.tinkoff.ru) 267, Комсомольская правда (KP.RU) 135, Аргументы и факты (aif.ru) 66, Хабр 52, Lenta.ru 27, РИА Новости 24, Лайфхакер 23, Kaspersky (kaspersky.ru) 20, Т-Банк (tbank.ru) 18, Московский комсомолец (mk.ru) 13, Myfin.by 7, ВТБ (vtb.ru) 4, СберБанк (sberbank.ru) 3, SecurityLab.ru 3, Финуслуги (Мосбиржа) 1, Журнал Совкомбанка 1, iGuides 1
- by country: RU 658, BY 7

## Caveats

- Transcript-heavy: a few long published call transcripts contribute many turns each (Habr femida_search 33, T-J fraud-stories-moshennik-v-telegram 31, T-J allo-eto-moshenniki 28, T-J frod-ruletka-kod-iz-sms 16, KP 5261489 20). Consider grouping by `source_url` when splitting train/validation.
- Some rows are example messages written up in guides rather than screenshots of a specific real message (Lifehacker Telegram guide, VTB/T-Bank/Sber "typical phrases" lists, Kaspersky resource-centre pages, which are translated from US material: USPS, dollar amounts; SecurityLab/Panda examples with `[ссылка]`).
- Pension / social-payment rows are fewer than hoped (social_payout 19). Most come from news sites; T-J has few verbatim pension quotes.
- Legit is small (14): Gosuslugi/bank OTP SMS texts, a Sber 900 notification, three example "real bank security" call lines from secrets.tbank.ru, one T-Bank marketing call. These sources rarely quote genuine bank SMS.
- Scheme `utilities` is new (fake management company / intercom codes / electricity / house chats); everything else reuses batch-1 scheme names.
- The web-search quota ran out partway through, so the alfabank.ru, sber.ru, anhor.uz and ema.com.ua pages yielded no rows (anhor.uz pages were fetched but had no usable scammer quotes).

## Source URLs (rows per URL)

| url | publisher | country | scam | legit |
|---|---|---|---|---|
| https://habr.com/ru/companies/femida_search/articles/970892/ | Хабр | RU | 33 | 0 |
| https://t-j.ru/fraud-stories-moshennik-v-telegram/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 31 | 0 |
| https://t-j.ru/allo-eto-moshenniki/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 28 | 0 |
| https://lifehacker.ru/moshenniki-v-telegramme-soobshheniya/ | Лайфхакер | RU | 21 | 0 |
| https://www.kp.ru/daily/277790/5261489/ | Комсомольская правда (KP.RU) | RU | 20 | 0 |
| https://t-j.ru/frod-ruletka-kod-iz-sms/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 16 | 0 |
| https://www.samara.kp.ru/daily/27684/5074469/ | Комсомольская правда (KP.RU) | RU | 13 | 0 |
| https://aif.ru/money/mymoney/vy_obvinyaetes_v_gosizmene_novye_ulovki_telefonnyh_moshennikov | Аргументы и факты (aif.ru) | RU | 10 | 0 |
| https://www.kp.ru/daily/26576.4/3591331/ | Комсомольская правда (KP.RU) | RU | 10 | 0 |
| https://www.kp.ru/daily/26102/2998713/ | Комсомольская правда (KP.RU) | RU | 9 | 0 |
| https://ria.ru/20190812/1557302039.html | РИА Новости | RU | 9 | 0 |
| https://www.mk.ru/social/2023/10/17/ya-vas-uslyshal-nazvany-frazy-po-kotorym-mozhno-raspoznat-telefonnykh-moshennikov.html | Московский комсомолец (mk.ru) | RU | 8 | 0 |
| https://www.ufa.kp.ru/daily/28369/4518473/ | Комсомольская правда (KP.RU) | RU | 8 | 0 |
| https://www.kaspersky.ru/blog/brushing-quishing-and-other-threats-of-unexpected-parcels/40299/ | Kaspersky (kaspersky.ru) | RU | 7 | 0 |
| https://habr.com/ru/articles/907988/ | Хабр | RU | 7 | 0 |
| https://www.ufa.kp.ru/daily/26288/3166334/ | Комсомольская правда (KP.RU) | RU | 7 | 0 |
| https://lenta.ru/articles/2025/09/24/telefonnye-moshenniki/ | Lenta.ru | RU | 7 | 0 |
| https://t-j.ru/hustle/allo-nachalnik/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 6 | 0 |
| https://habr.com/en/articles/586612/comments/ | Хабр | RU | 6 | 0 |
| https://secrets.tbank.ru/bezopasnost-biznesa/kak-otlichit-moshennikov/ | Т-Банк (tbank.ru) | RU | 3 | 3 |
| https://www.kp.ru/daily/27775/5238756/ | Комсомольская правда (KP.RU) | RU | 6 | 0 |
| https://www.kp.ru/daily/28343/4489034/ | Комсомольская правда (KP.RU) | RU | 6 | 0 |
| https://t-j.ru/scams/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 5 | 0 |
| https://t-j.ru/how-scammers-tried-to-deceive-me-with-the-typewriter-vacancy/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 5 | 0 |
| https://www.kaspersky.ru/blog/i-was-almost-scammed/39209/ | Kaspersky (kaspersky.ru) | RU | 5 | 0 |
| https://altai.aif.ru/society/dostavka_avito_moshennik_rasskazal_skolko_zarabatyvaet_na_obmane | Аргументы и факты (aif.ru) | RU | 5 | 0 |
| https://www.kp.ru/daily/27653/5004319/ | Комсомольская правда (KP.RU) | RU | 5 | 0 |
| https://aif.ru/money/mymoney/raspoznat-i-obezvredit-5-fraz-vydayushchih-obman-po-telefonu | Аргументы и факты (aif.ru) | RU | 5 | 0 |
| https://aif.ru/money/mymoney/-vy-poluchili-perevod-pyat-soobshcheniy-ot-banka-kotorye-dolzhny-nastorozhit | Аргументы и факты (aif.ru) | RU | 5 | 0 |
| https://t-j.ru/retiree-fraud/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 4 | 0 |
| https://t-j.ru/hustle/fake-police-calls/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 4 | 0 |
| https://t-j.ru/hustle/pismo-iz-mfz/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 4 | 0 |
| https://t-j.ru/short/criptoscams/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 4 | 0 |
| https://t-j.ru/video-communication-fraud/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 4 | 0 |
| https://t-j.ru/fraud-stories-skype-interview-for-remote-job/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 4 | 0 |
| https://t-j.ru/calls-from-scammers/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 4 | 0 |
| https://www.kaspersky.ru/resource-center/threats/wrong-text-number-scam | Kaspersky (kaspersky.ru) | RU | 4 | 0 |
| https://www.vtb.ru/articles/finansovaya-gramotnost/novyye-moshennicheskiye-skhemy-eto-vazhno-znat/ | ВТБ (vtb.ru) | RU | 4 | 0 |
| https://www.tbank.ru/finance/blog/phone-scam/ | Т-Банк (tbank.ru) | RU | 4 | 0 |
| https://www.kp.ru/daily/27767.5/5225584/ | Комсомольская правда (KP.RU) | RU | 4 | 0 |
| https://vl.aif.ru/society/popalsya_na_kryuchok_starye_moshennicheskie_sposoby_opustoshayut_koshelki | Аргументы и факты (aif.ru) | RU | 4 | 0 |
| https://rzn.aif.ru/incidents/details/125871 | Аргументы и факты (aif.ru) | RU | 4 | 0 |
| https://ria.ru/20251129/moshennichestvo-2058546676.html | РИА Новости | RU | 4 | 0 |
| https://lenta.ru/news/2026/11/04/perechisleny-osnovnye-frazy-moshennikov/ | Lenta.ru | RU | 4 | 0 |
| https://www.belarus.kp.ru/daily/27408/4605973/ | Комсомольская правда (KP.RU) | RU | 4 | 0 |
| https://t-j.ru/scammers-pretended-familiar/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 3 | 0 |
| https://t-j.ru/fraud-stories-vk-voting/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 3 | 0 |
| https://t-j.ru/stories-police-scammers/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 3 | 0 |
| https://t-j.ru/fraud-stories-call-on-zoom/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 3 | 0 |
| https://t-j.ru/job-marketplaces-fraud/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 3 | 0 |
| https://t-j.ru/sim-card-reregistration-fraud/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 3 | 0 |
| https://t-j.ru/fraud-stories-fsb-and-cb/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 3 | 0 |
| https://t-j.ru/police-calls-fraud/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 3 | 0 |
| https://t-j.ru/job-fraud-online-part-time-work-in-fake-trading/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 3 | 0 |
| https://t-j.ru/hustle/hustle-duet/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 3 | 0 |
| https://t-j.ru/fraud-stories-trader-from-dating-site/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 3 | 0 |
| https://www.kaspersky.ru/blog/telegram-account-hacked/38711/ | Kaspersky (kaspersky.ru) | RU | 3 | 0 |
| https://habr.com/ru/articles/1104614/ | Хабр | RU | 3 | 0 |
| https://myfin.by/article/banki/novye-skhemy-mosennicestva-i-kak-ikh-izbezat-istorii-belorusov-36894 | Myfin.by | BY | 3 | 0 |
| https://www.sberbank.ru/ru/s_m_business/pro_business/kak-moshenniki-obmanyvayut-klientov-bankov | СберБанк (sberbank.ru) | RU | 3 | 0 |
| https://www.securitylab.ru/blog/company/PandaSecurityRus/351841.php | SecurityLab.ru | RU | 3 | 0 |
| https://t-j.ru/list/eto-spam/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 3 | 0 |
| https://lenta.ru/news/2026/10/05/na-rossiyan-natselilis-zamaskirovannye-pod-sotrudnikov-poliklinik-moshenniki/ | Lenta.ru | RU | 3 | 0 |
| https://www.mk.ru/social/2025/08/07/mvd-nazvalo-tri-frazy-po-kotorym-mozhno-raspoznat-psevdobrokerov.html | Московский комсомолец (mk.ru) | RU | 3 | 0 |
| https://lenta.ru/brief/2025/09/29/telefonnye-moshenniki-glavnaya-ugroza-sovremennoy-rossii/ | Lenta.ru | RU | 3 | 0 |
| https://aif.ru/incidents/mvd-rasskazalo-frazy-moshennikov-ispolzuyushchih-gosuslugi-dlya-afyor | Аргументы и факты (aif.ru) | RU | 3 | 0 |
| https://www.alt.kp.ru/daily/27556.5/4880517/ | Комсомольская правда (KP.RU) | RU | 3 | 0 |
| https://www.kp.ru/daily/26951.4/4003077/ | Комсомольская правда (KP.RU) | RU | 3 | 0 |
| https://aif.ru/society/safety/-vam-zvonyat-iz-polikliniki-5-populyarnyh-v-2026-godu-shem-obmana-pacientov | Аргументы и факты (aif.ru) | RU | 3 | 0 |
| https://t-j.ru/psihologicheskie-tryki-moshennikov/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 2 | 0 |
| https://t-j.ru/hustle/corporate-discount/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 2 | 0 |
| https://t-j.ru/fraud-stories-secure-account/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 2 | 0 |
| https://t-j.ru/fraud-stories-kompaniya-po-zamene-domofonov-i-roskomnadzor/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 2 | 0 |
| https://t-j.ru/vishing/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 2 | 0 |
| https://t-j.ru/money-scam-street/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 2 | 0 |
| https://t-j.ru/fraud-stories-trading-in-job-search-telegram/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 2 | 0 |
| https://t-j.ru/short/school-fraud/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 2 | 0 |
| https://t-j.ru/fraud-stories-non-employee-of-russian-post/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 1 |
| https://t-j.ru/fraud-stories-kriptomoshenniki/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 2 | 0 |
| https://t-j.ru/fraud-stories-dogovor-match/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 2 | 0 |
| https://t-j.ru/fraud-stories-fake-buyer/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 1 |
| https://t-j.ru/news/cb-antifraud/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 0 | 2 |
| https://t-j.ru/fraud-former-chief/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 2 | 0 |
| https://t-j.ru/avito-delivery-fraud/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 1 |
| https://t-j.ru/fraud-stories-moloko-dlia-rebenka/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 2 | 0 |
| https://t-j.ru/job-fraud-tester/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 2 | 0 |
| https://www.tbank.ru/invest/social/profile/Provatory/79e6951a-30f3-4a7d-b8f2-5a1f25b839df/ | Т-Банк (tbank.ru) | RU | 2 | 0 |
| https://www.tbank.ru/finance/blog/fishing/ | Т-Банк (tbank.ru) | RU | 2 | 0 |
| https://www.tbank.ru/finance/blog/new-fraud/ | Т-Банк (tbank.ru) | RU | 2 | 0 |
| https://myfin.by/article/blogi/k-takoj-stepeni-realizma-nikto-ne-byl-gotov-kak-mosenniki-obmanyvaut-s-pomosu-ii-35810 | Myfin.by | BY | 2 | 0 |
| https://www.kp.ru/online/news/6751219/ | Комсомольская правда (KP.RU) | RU | 2 | 0 |
| https://ural.aif.ru/society/krugly_stol/kak_rabotayut_moshenniki_na_doverii_bezotkaznye_tehnologii_obmana | Аргументы и факты (aif.ru) | RU | 2 | 0 |
| https://www.kp.ru/daily/27649/5033252/ | Комсомольская правда (KP.RU) | RU | 2 | 0 |
| https://irk.aif.ru/incidents/-dengi-na-bochku-kak-ne-lishitsya-millionov-cherez-domovoy-chat-i-gosuslugi | Аргументы и факты (aif.ru) | RU | 2 | 0 |
| https://aif.ru/society/safety/sluzhba_bezopasnosti_banka_8_fraz_kotorye_vydayut_telefonnyh_moshennikov | Аргументы и факты (aif.ru) | RU | 2 | 0 |
| https://www.yakutia.kp.ru/online/news/5146197/ | Комсомольская правда (KP.RU) | RU | 2 | 0 |
| https://www.irk.kp.ru/daily/27743.5/5170932/ | Комсомольская правда (KP.RU) | RU | 2 | 0 |
| https://www.kp.ru/daily/27729/5118282/ | Комсомольская правда (KP.RU) | RU | 2 | 0 |
| https://www.kp.ru/daily/26831.7/3871146/ | Комсомольская правда (KP.RU) | RU | 2 | 0 |
| https://www.kp.ru/daily/277791.5/5265973/ | Комсомольская правда (KP.RU) | RU | 2 | 0 |
| https://www.kp.ru/daily/277780/5245608/ | Комсомольская правда (KP.RU) | RU | 2 | 0 |
| https://www.spb.kp.ru/daily/27756.5/5203571/ | Комсомольская правда (KP.RU) | RU | 2 | 0 |
| https://www.nsk.kp.ru/daily/27642/4994028/ | Комсомольская правда (KP.RU) | RU | 2 | 0 |
| https://www.kp.ru/putevoditel/finansovaya-gramotnost/skhemy-moshennichestva/ | Комсомольская правда (KP.RU) | RU | 2 | 0 |
| https://stav.aif.ru/society/person/lzhevoenkomy-ohotyatsya-za-dannymi-muzhchin-rasskazal-donchanin | Аргументы и факты (aif.ru) | RU | 2 | 0 |
| https://www.sevastopol.kp.ru/daily/27738/5164258/ | Комсомольская правда (KP.RU) | RU | 2 | 0 |
| https://www.kp.ru/daily/27732/5159812/ | Комсомольская правда (KP.RU) | RU | 2 | 0 |
| https://ria.ru/20260521/rassylka-2093699100.html | РИА Новости | RU | 2 | 0 |
| https://rzn.aif.ru/incidents/details/-vyplata-1-oktyabrya-kakuyu-shemu-moshenniki-primenyayut-dlya-obmana-pensionerov | Аргументы и факты (aif.ru) | RU | 2 | 0 |
| https://t-j.ru/happy-outcomes-meeting-scammers/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/hustle/haha-obmanuli/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/pochtarf-fraud/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/skazochniy-fraud/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/hustle/fake-foundations/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/list/business-scammers/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/stories-lifehacks-scammers/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/fraud-stories-borrowed-money/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/fraud-stories-bookmaker-bets/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/fraud-stories-vykupe-marketpleis/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/fraud-stories-by-mail/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/hustle/finansoviy-nomer/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/fraud-stories-paren-s-saita-znakomstv/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/moshenniki-ugnali-instagram/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/answer-scammers-phone/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/hustle/secret-customer/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/fraud-investment-dating/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/fraud-stories-another-fsb-call/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/fraud-stories-online-work/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/fraud-stories-sait-znakomstv/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/list/avito-dostavka-fake/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/hustle/telegram-sports-fraud/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/scammers-pretended-relatives/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/short/lets-talk-about-fraud/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/strangers-help-fraud/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/kak-ia-proshla-protseduru-bankrotstva-vziala-kredit-i-perevela-den-gi-moshennikam/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/stories-tech-scammers/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/fraud-stories-fake-electricity-debts/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/fraud-stories-reklama-moshennikov-vo-vremia-igry-onlain/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/fraud-online-dating/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/hustle/razvod-otmena-naloga/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/fraud-unemployed-financial-pyramid/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/npf-fraud/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/hustle/fake-invest/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/stories-call-scammers/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/fraud-stories-false-job/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/fraud-stories-priglasili-na-fotosessiiu-pytalis-oformit-kredit/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/scammers-losers/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/fraud-accountant/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/list/mail-fraud/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/hustle/golosovoe-druga/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/phishing/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/hustle/bank-is-calling-again/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 0 | 1 |
| https://t-j.ru/fun-answers-scammers/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/hustle/nakonezto-dozvonilas/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 0 | 1 |
| https://t-j.ru/list/moshennik-uhodi/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 0 | 1 |
| https://t-j.ru/fraud-stories-fake-investment-training/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/fraud-stories-job-scam/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/scammers-jobs/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/fraud-stories-sdelki-po-sovetu-analitika/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/hustle/avito-dostavka-sell-fraud/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/fraud-stories-zvonok-iz-nalogovoi-i-poddelnye-pisma-ot-gosuslug/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/hustle/tg-progress/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/they-are-scammers-not-us/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/wiki/fraud/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/fraud-stories-obman-pri-poiske-raboty/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/fraud-stories-osago/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/fraud-stories-captain-spanish-merchant-fleet/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/fraud-stories-sports-insider/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/job-fraud-poniat-razvod-zaranee/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/fraud-stories-refrigerator-repair/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/waiters-fraud/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/hustle/replica/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/hustle/tax-compensation/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/hustle/prodli-oms/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/hustle/dopros-povestka-whatsapp/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/fraud-stories-replenishing-stranger-card/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/buyer-fraud/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/internet-dating-fraud/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/scammers-force-transfer-money/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/razvod-babushek/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 0 | 1 |
| https://myfin.by/article/money/vam-ne-doscitali-devat-mesacev-staza-mosenniki-obmanyvaut-pensionerov-po-novoj-sheme-48122 | Myfin.by | BY | 1 | 0 |
| https://www.tbank.ru/finance/blog/dont-be-fraud/ | Т-Банк (tbank.ru) | RU | 1 | 0 |
| https://habr.com/ru/articles/1023260/ | Хабр | RU | 1 | 0 |
| https://habr.com/ru/articles/877156/ | Хабр | RU | 1 | 0 |
| https://finuslugi.ru/navigator/kak-ehto-rabotaet/stat_vam_zvonit_moshennik_kak_bystro_raspoznat_i_ne_stat_zhertvoj_obmana | Финуслуги (Мосбиржа) | RU | 1 | 0 |
| https://myfin.by/stati/view/uznali-pro-novye-sposoby-mosennicestva-s-bankovskimi-dannymi-kak-ne-popastsa | Myfin.by | BY | 0 | 1 |
| https://habr.com/ru/articles/1093960/ | Хабр | RU | 1 | 0 |
| https://lifehacker.ru/telefonnye-moshenniki/ | Лайфхакер | RU | 1 | 0 |
| https://journal.sovcombank.ru/sberezheniya/chto-takoe-kibermoshennichestvo-i-kak-ot-nego-zaschititsya | Журнал Совкомбанка | RU | 1 | 0 |
| https://lifehacker.ru/moshennicheskie-sxemy/ | Лайфхакер | RU | 1 | 0 |
| https://www.kaspersky.ru/resource-center/threats/what-is-smishing-and-how-to-defend-against-it | Kaspersky (kaspersky.ru) | RU | 1 | 0 |
| https://www.iguides.ru/main/other/rossiyan_nachali_durit_na_ozon_skhema_ochen_khitraya/ | iGuides | RU | 1 | 0 |
| https://www.tbank.ru/finance/blog/marketplace-fraud/ | Т-Банк (tbank.ru) | RU | 1 | 0 |
| https://t-j.ru/ukrali-telefon-fail/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/plohotron-wmrfast/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/law-story-droppery/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/fraud-easy-income/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/fraud-stories-fake-show/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/card-fraud/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 0 | 1 |
| https://t-j.ru/kto-vymogatel/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://www.irk.kp.ru/daily/27760/5189375/ | Комсомольская правда (KP.RU) | RU | 1 | 0 |
| https://www.nsk.kp.ru/online/news/3661089/ | Комсомольская правда (KP.RU) | RU | 1 | 0 |
| https://samara.aif.ru/incidents/scene/v-samare-k-8-marta-aktivizirovalis-cvetochnye-moshenniki | Аргументы и факты (aif.ru) | RU | 1 | 0 |
| https://hab.mk.ru/social/2025/11/20/kovarnyy-kod-ekspert-obyasnil-kak-raspoznat-moshennikov-pod-vidom-kurerov.html | Московский комсомолец (mk.ru) | RU | 1 | 0 |
| https://www.rostov.kp.ru/daily/27633/4983526/ | Комсомольская правда (KP.RU) | RU | 1 | 0 |
| https://crimea.ria.ru/20251018/bolshie-skidki-i-zaderzhki-zakaza-nazvany-ulovki-moshennikov-1150259415.html | РИА Новости | RU | 1 | 0 |
| https://omsk.aif.ru/society/-zaymi-na-kartu-moshenniki-vzlomali-telegram-chto-delat | Аргументы и факты (aif.ru) | RU | 1 | 0 |
| https://lenta.ru/news/2025/10/23/shema/ | Lenta.ru | RU | 1 | 0 |
| https://www.hab.kp.ru/daily/27403/4599489/ | Комсомольская правда (KP.RU) | RU | 1 | 0 |
| https://kuban.aif.ru/incidents/birzha_ili_sluzhby_bezopasnosti_kakie_shemy_ispolzuyut_moshenniki | Аргументы и факты (aif.ru) | RU | 1 | 0 |
| https://www.kp.ru/daily/27426/4626725/ | Комсомольская правда (KP.RU) | RU | 1 | 0 |
| https://ria.ru/20260923/moshenniki-2119626044.html | РИА Новости | RU | 1 | 0 |
| https://aif.ru/society/v-mvd-rasskazali-o-moshennichestve-s-vyigryshami-v-lotereyu | Аргументы и факты (aif.ru) | RU | 1 | 0 |
| https://lenta.ru/news/2026/06/23/avtolyubiteley-predupredili-o-moshennicheskoy-sheme-s-feykovoy-razdachey-benzina/ | Lenta.ru | RU | 1 | 0 |
| https://aif.ru/money/mymoney/moshenniki_na_provode_chto_delat_chtoby_aferisty_bolshe_ne_zvonili | Аргументы и факты (aif.ru) | RU | 1 | 0 |
| https://aif.ru/techno/apps/chto-za-novaya-shema-moshennikov-s-konkursami-v-telegram | Аргументы и факты (aif.ru) | RU | 1 | 0 |
| https://ria.ru/20231227/aferisty-1918574954.html | РИА Новости | RU | 1 | 0 |
| https://www.mk.ru/social/2018/06/29/moshenniki-nachali-vorovat-dengi-cherez-whatsapp-kak-ne-stat-zhertvoy.html | Московский комсомолец (mk.ru) | RU | 1 | 0 |
| https://aif.ru/society/people/istoriya_odnogo_obmana_kak_menya_razvodili_moshenniki | Аргументы и факты (aif.ru) | RU | 1 | 0 |
| https://ria.ru/20241213/moshenniki-1988950376.html | РИА Новости | RU | 1 | 0 |
| https://lenta.ru/news/2020/06/01/whatsapp/ | Lenta.ru | RU | 1 | 0 |
| https://lenta.ru/news/2022/02/03/mest/ | Lenta.ru | RU | 1 | 0 |
| https://aif.ru/society/web/chto-za-novaya-shema-razvoda-s-zarabatyvaniem-laykov-v-internete | Аргументы и факты (aif.ru) | RU | 1 | 0 |
| https://ria.ru/20240815/sber-1966331600.html | РИА Новости | RU | 1 | 0 |
| https://www.dv.kp.ru/online/news/6074722/ | Комсомольская правда (KP.RU) | RU | 1 | 0 |
| https://aif.ru/society/safety/chto-za-novoe-moshennichestvo-s-kompensaciey-za-domashniy-internet | Аргументы и факты (aif.ru) | RU | 1 | 0 |
| https://ria.ru/20240821/whatsapp-1967441702.html | РИА Новости | RU | 1 | 0 |
| https://lenta.ru/news/2025/12/05/moshenniki-stali-soobschat-rossiyanam-o-neuplachennyh-nalogah/ | Lenta.ru | RU | 1 | 0 |
| https://lenta.ru/news/2026/10/31/profayler-nazval-sposoby-raspoznat-brachnogo-aferista-v-seti/ | Lenta.ru | RU | 1 | 0 |
| https://ria.ru/20261101/moshenniki-2128457218.html | РИА Новости | RU | 1 | 0 |
| https://lenta.ru/news/2026/09/20/rossiyan-predupredili-o-moshennicheskoy-sheme-s-podrabotkami/ | Lenta.ru | RU | 1 | 0 |
| https://www.izh.kp.ru/daily/27567/4892005/ | Комсомольская правда (KP.RU) | RU | 1 | 0 |
| https://lenta.ru/articles/2024/12/16/scammers/ | Lenta.ru | RU | 1 | 0 |
| https://irk.aif.ru/incidents/investicii_v_moshennichestvo_kak_obmanyvayut_lyudey_gazprom_investicii | Аргументы и факты (aif.ru) | RU | 1 | 0 |
| https://www.kp.ru/daily/277803.5/5284240/ | Комсомольская правда (KP.RU) | RU | 1 | 0 |
| https://lenta.ru/news/2026/10/24/rossiyan-predupredili-o-nazhivayuschihsya-na-pensiyah-moshennikah/ | Lenta.ru | RU | 1 | 0 |
| https://samara.aif.ru/incidents/scene/v-samare-pod-vidom-zhkh-vymanivayut-milliony | Аргументы и факты (aif.ru) | RU | 1 | 0 |
| https://www.perm.kp.ru/daily/27064.4/4132897/ | Комсомольская правда (KP.RU) | RU | 1 | 0 |
| https://kazan.aif.ru/society/sekunda-chtoby-ne-popastsya-kak-ne-popastsya-na-fishing-sovety-eksperta | Аргументы и факты (aif.ru) | RU | 1 | 0 |
| https://ria.ru/20261001/mvd-2121369685.html | РИА Новости | RU | 1 | 0 |
| https://rzn.aif.ru/incidents/details/zhuliki-vsyo-hitree-rasskazyvaem-o-novyh-ulovkah-distancionnyh-moshennikov | Аргументы и факты (aif.ru) | RU | 1 | 0 |
| https://www.kp.ru/putevoditel/spetsproekty/prosto-zapomnite/ | Комсомольская правда (KP.RU) | RU | 1 | 0 |
| https://ria.ru/20211015/moshenniki-1754548265.html | РИА Новости | RU | 1 | 0 |
| https://aif.ru/society/safety/13-sposobov-obmana-chto-pridumali-moshenniki-v-2025-godu | Аргументы и факты (aif.ru) | RU | 1 | 0 |
| https://www.kp.ru/daily/27586/4912807/ | Комсомольская правда (KP.RU) | RU | 1 | 0 |
| https://aif.ru/society/safety/chto-za-moshennichestvo-s-zamenoy-domofonov | Аргументы и факты (aif.ru) | RU | 1 | 0 |
| https://kazan.aif.ru/incidents/details/-ty-samaya-klassnaya-podozhdi-brachnyy-aferist-obmanyval-lyubovnic-na-milliony | Аргументы и факты (aif.ru) | RU | 1 | 0 |
| https://lenta.ru/news/2026/06/26/rossiyan-predupredili-o-letnem-moshennichestve-s-nesuschestvuyuschimi-domami/ | Lenta.ru | RU | 1 | 0 |
| https://kazan.aif.ru/society/son-v-ruku-kak-aferist-kidal-druzey-i-oformlyal-mikrozaymy-na-spyashchih-podrug | Аргументы и факты (aif.ru) | RU | 1 | 0 |
