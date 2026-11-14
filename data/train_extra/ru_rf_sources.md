# ru_rf_collected.jsonl: sources

Collected 2026-11-14 for TRAINING only. All sources are outside Kazakhstan (RU, BY, UA, UZ); no .kz domain or Kazakhstan-focused item was used, and items mentioning Kaspi/Kazakhstan/tenge/eGov were filtered out.

## Method

- Pages fetched with curl (T-J needed its `?mc_attempt=1` bot-check fallback; Russian-CA sites fetched with `-k`). HTML converted to text with BeautifulSoup.
- Candidates = text inside «…»/“…” quotes (and `— ` dialogue lines in T-J reader stories) with 5+ words; every kept item was hand-picked as a scammer SMS/messenger message or scammer call turn and hand-labelled with a scheme.
- Verbatim check: each text (before scrubbing) is an exact substring of the whitespace-normalised page text; after scrubbing, a regex with placeholders as wildcards re-matched 344/344 rows. Narrator tails glued to some dialogue lines were cut at a sentence boundary (prefix stays verbatim).
- Scrubbing: phones -> [PHONE], card numbers -> [CARD], persona/real first names -> [NAME] (11 rows touched). Deduplicated on lowercased alphanumerics.
- Legit rows are genuine bank OTP SMS texts quoted in articles (e.g. "Списание ... Никому не говорите код ..."). Very few such examples exist in these sources, so legit is small.

## Counts

- total 344: scam 338, legit 6
- by scheme: scam/bank_security 56, scam/investment 42, scam/fake_law_enforcement 33, scam/job 32, scam/relatives 16, scam/social_payout 15, scam/gosuslugi 14, scam/mobile_operator 13, scam/safe_account 12, scam/loan_in_your_name 11, scam/sms_code 10, scam/phishing_link 10, scam/fake_friend 10, scam/prize 9, scam/other 9, scam/rental 8, scam/marketplace 7, scam/delivery 7, legit/otp_code 6, scam/fake_acquaintance 4, scam/tax_refund 3, scam/tech_support 3, scam/telegram_gift 3, scam/debt_relief 2, scam/mistaken_transfer 2, scam/insurance 2, scam/loan_offer 2, scam/recovery_scam 2, scam/fake_boss 1
- by publisher: Т—Ж / T-Bank Journal (journal.tinkoff.ru) 307, Myfin.by 9, Финуслуги (Мосбиржа) 7, SecurityLab.ru 5, Журнал Совкомбанка 4, Хабр 4, Лайфхакер 3, Anhor.uz 2, iGuides 1, EMA (Ukraine) 1, Anti-Malware.ru 1

## Gaps

- cbr.ru, fincult.info, sberbank.ru (Kibrary), gosuslugi.ru did not return usable HTML via plain fetch (TLS/geo/JS); Kaspersky blog guessed slugs 404. Not retried in a browser because of the 40-minute limit.
- T-J (journal.tinkoff.ru, now t-j.ru) dominates (~89%); its reader stories quote messages and calls verbatim. Some quotes are short single call turns (5-8 words).

## Source URLs (rows per URL)

| url | publisher | country | scam | legit |
|---|---|---|---|---|
| https://t-j.ru/spec-fraud-protection/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 21 | 0 |
| https://t-j.ru/vishing/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 10 | 0 |
| https://t-j.ru/guide/top-vk-frauds/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 8 | 0 |
| https://t-j.ru/smishing/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 7 | 0 |
| https://t-j.ru/moshenniki-arenda/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 7 | 0 |
| https://finuslugi.ru/navigator/kak-ehto-rabotaet/stat_7-skhem-moshennichestva-kak-ne-poteryat-dengi-i-chto-delat-esli-uzhe-popalis-na-udochku-moshennika | Финуслуги (Мосбиржа) | RU | 7 | 0 |
| https://t-j.ru/scammers-go-away/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 6 | 0 |
| https://t-j.ru/scammers-force-transfer-money/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 6 | 0 |
| https://t-j.ru/razvod-babushek/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 6 | 0 |
| https://t-j.ru/job-marketplaces-fraud/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 6 | 0 |
| https://t-j.ru/short/govoryat-moshenniki/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 6 | 0 |
| https://t-j.ru/hustle/bistro-obnovi/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 5 | 0 |
| https://t-j.ru/hustle/telegram-sports-fraud/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 5 | 0 |
| https://t-j.ru/brands-fraud/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 5 | 0 |
| https://t-j.ru/fake-ozon-delivery/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 3 | 2 |
| https://www.securitylab.ru/analytics/533211.php | SecurityLab.ru | RU | 5 | 0 |
| https://myfin.by/article/zhizn/ostorozno-telefonnye-mosenniki-kakie-frazy-case-vsego-ispolzuut-aferisty-40168 | Myfin.by | BY | 5 | 0 |
| https://t-j.ru/law-practice-vzlom-gosuslug/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 5 | 0 |
| https://journal.sovcombank.ru/news/frazy-telefonnyx-mosennikov | Журнал Совкомбанка | RU | 4 | 0 |
| https://t-j.ru/fraud-stories-fake-investment-training/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 4 | 0 |
| https://habr.com/ru/articles/933784/ | Хабр | RU | 4 | 0 |
| https://t-j.ru/telegram-gifts-scam/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 4 | 0 |
| https://t-j.ru/hustle/fraud-bus-blablacar/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 2 |
| https://t-j.ru/sms-code-fraud/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 3 | 0 |
| https://t-j.ru/phishing/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 3 | 0 |
| https://t-j.ru/calls-from-scammers/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 3 | 0 |
| https://t-j.ru/fraud-stories-bezopasnyi-schet-i-obratnyi-zvonok/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 2 | 1 |
| https://lifehacker.ru/8-fraz-telefonnyx-moshennikov/ | Лайфхакер | RU | 3 | 0 |
| https://t-j.ru/scammers-pretended-familiar/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 3 | 0 |
| https://t-j.ru/fun-answers-scammers/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 3 | 0 |
| https://t-j.ru/hustle/finansoviy-nomer/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 3 | 0 |
| https://t-j.ru/hustle/haha-obmanuli/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 3 | 0 |
| https://t-j.ru/fraud-stories-another-fsb-call/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 3 | 0 |
| https://t-j.ru/hustle/povis-limiti/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 3 | 0 |
| https://t-j.ru/fraud-phone/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 3 | 0 |
| https://t-j.ru/messages-director-fraud/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 3 | 0 |
| https://t-j.ru/rosfinmonitoring-fraudcall/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 3 | 0 |
| https://t-j.ru/short/criptoscams/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 3 | 0 |
| https://t-j.ru/skazochniy-fraud/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 3 | 0 |
| https://t-j.ru/why-people-fall-for-scams/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 3 | 0 |
| https://t-j.ru/sms-bombing/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 3 | 0 |
| https://myfin.by/stati/view/13764-belorusskie-banki-preduprezhdayut-o-moshennichestve-v-viber | Myfin.by | BY | 2 | 0 |
| https://t-j.ru/apps-recommendations-form/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 2 | 0 |
| https://myfin.by/stati/view/realnye-istorii-kibermosennicestva-kak-zapodozrit-obman | Myfin.by | BY | 2 | 0 |
| https://t-j.ru/hustle/allo-nachalnik/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 2 | 0 |
| https://t-j.ru/hustle/fake-police-calls/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 2 | 0 |
| https://t-j.ru/hustle/nakonezto-dozvonilas/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 2 | 0 |
| https://t-j.ru/stories-police-scammers/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 2 | 0 |
| https://t-j.ru/adress-dlya-moshennika/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 2 | 0 |
| https://t-j.ru/hustle/tax-compensation/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 2 | 0 |
| https://t-j.ru/fraud-stories-osago/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 2 | 0 |
| https://t-j.ru/fraud-stories-fsb-and-cb/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 2 | 0 |
| https://t-j.ru/fraud-stories-udalennaya-rabota/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 2 | 0 |
| https://t-j.ru/stories-lifehacks-scammers/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 2 | 0 |
| https://t-j.ru/they-are-scammers-not-us/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 2 | 0 |
| https://t-j.ru/hustle/prodli-oms/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 2 | 0 |
| https://t-j.ru/imitation-relatives-fraud/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 2 | 0 |
| https://t-j.ru/fraud-stories-moshenniki-iz-chata-dlia-znakomstv/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 2 | 0 |
| https://t-j.ru/how-scammers-tried-to-deceive-me-with-the-typewriter-vacancy/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 2 | 0 |
| https://t-j.ru/fraud-stories-dogovornye-matchi-2/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 2 | 0 |
| https://t-j.ru/hustle/dopros-povestka-whatsapp/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 2 | 0 |
| https://t-j.ru/hustle/friendly-phishing/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 2 | 0 |
| https://t-j.ru/fraud-stories-quick-money-chatgpt/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 2 | 0 |
| https://t-j.ru/bonus-fraud/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 2 | 0 |
| https://t-j.ru/computer-wizard-fraud/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 2 | 0 |
| https://t-j.ru/fraud-accountant/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 2 | 0 |
| https://t-j.ru/kak-ia-iskala-rabotu-v-italii-i-narvalas-na-moshennikov/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 2 | 0 |
| https://t-j.ru/police-calls-fraud/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 2 | 0 |
| https://t-j.ru/scams/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 1 |
| https://t-j.ru/wiki/fraud/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 2 | 0 |
| https://t-j.ru/kasko-drop/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 2 | 0 |
| https://t-j.ru/scammers-fine/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/scammer-police-captain/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/fraud-stories-plemiannitsu-podrostka-pytalis-razvesti-moshenniki/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/fraud-stories-pod-vidom-dostavki/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/fraud-stories-fake-model/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/hustle/youtube-costot/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/hustle/razvod-otmena-naloga/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/fraud-stories-trading-in-job-search-telegram/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/fraud-stories-arbitrazh-trafika-v-telegram/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://www.iguides.ru/main/security/s_vami_govorit_telefonnyy_moshennik/ | iGuides | RU | 1 | 0 |
| https://t-j.ru/fraud-stories-obman-pri-poiske-raboty/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/fraud-stories-kriptomoshenniki/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/hustle/go-scam-yourself/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/fraud-stories-sait-znakomstv/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/fraud-stories-trader-from-dating-site/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/salvation-from-scammers/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/scammers-are-calling/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/news/zvonok-iz-fns/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/hustle/ostav-nomerok/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/inspektor-nalogovoi-zvonit/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/call-scammers-stories/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/kak-ya-spas-dengi-mamy/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://ema.com.ua/citizens/cyber-safety-school/vishing-scam-of-scam | EMA (Ukraine) | UA | 1 | 0 |
| https://t-j.ru/fraud-stories-moloko-dlia-rebenka/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/scammers-jobs/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/social-media-page-hack-fail/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/fraud-stories-money-to-manage-an-acquaintance-from-personal-growth-course/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/fraud-stories-chuzhoy-akkaunt-max-na-moem-nomere/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/fraud-stories-girls-signals-in-telegram-chat-room/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/hustle/bank-is-calling-again/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/hustle/golosovoe-druga/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/hustle/google-presentation-fraud/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/hustle/natalia-solovyova/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/hustle/nazhmite-pokazhite/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/5-razgovorov-s-roditeliami-kotorye-zashchitiat-ot-moshennikov/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/fraud-stories-call-on-zoom/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/fraud-stories-non-employee-of-russian-post/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/fraud-stories-fake-copywriter-vacancy/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/hustle/fake-bloggers/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/fraud-stories-trading-cfd-in-fake-terminal-using-signals/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/hustle/priem-centrobank/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/fraud-stories-45k-na-dogovornykh-matchakh/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/fraud-stories-aferisti/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/fraud-stories-false-job/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/fraud-stories-ot-imeni-pochty-rossii/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/otlichit-zvonok-moshennika-ot-zvonka-banka-stanovitsia-vse-slozhnee-opinion/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/hustle/pismo-iz-mfz/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/answer-scammers-phone/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/fraud-stories-betting/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://www.anti-malware.ru/news/2025-06-10-121598/46310 | Anti-Malware.ru | RU | 1 | 0 |
| https://t-j.ru/beggars-fraud/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/best-time-for-fraud/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/company-promising-to-withdraw-money-from-fake-terminal/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/cryptocurrency-scam-fail/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/delivery-fraud/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/fraud-at-work/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/fraud-older-people/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/fraudsters-offer-decent-wages-hate/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/job-fraud-onlain-sobesedovanie/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/job-fraud-tester/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/kak-obmanyvaiut-rieltory-v-italii/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/kak-zarabotat-v-internete-i-ne-narvatsia-na-moshennikov/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/kosheliok-vash-a-dengi-ukhodiat-moshennikam/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/law-practice-kak-ne-stat-zhertvoi-moshennikov/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/list/mail-fraud/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/money-scam-street/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/moshenniki-i-gosuslugi/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/moshenniki-ugnali-instagram/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/news/lovite-moshennikov-vse/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/obman-poproshaek/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/pochtarf-fraud/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/posredniki-moshenniki/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/scam-call-hangup/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/short/fake-zhkh/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/rent-fraud/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/list/kitty-knows-scam/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/moshenniki-znaiut-o-nas-vsio-hate/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/fortune-tellers-fraud/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/hamster-kombat-scam-or-not/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://anhor.uz/news/v-uzbekistane-predupredili/ | Anhor.uz | UZ | 1 | 0 |
| https://anhor.uz/ru/news/qwizzserial | Anhor.uz | UZ | 1 | 0 |
| https://t-j.ru/10-hacks-to-save-money/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/kto-vymogatel/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/plohotron-avalon/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/plohotron-mercurynft/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
| https://t-j.ru/plohotron-tonstake/ | Т—Ж / T-Bank Journal (journal.tinkoff.ru) | RU | 1 | 0 |
