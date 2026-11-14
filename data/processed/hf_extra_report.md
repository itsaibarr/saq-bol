# hf_extra: public Hugging Face training data

Built by `pipeline/src/build_hf_extra.py` on 2026-11-14. Output `data/processed/hf_extra.jsonl`: **46697 rows** (scam 13412 / legit 33285).

Pipeline: textnorm.normalize -> 3-80 words -> dedup (exact; normalized-lowercase; template skeleton with digits and salutation names masked; skeletons seen with both labels dropped) -> cap 15k rows/dataset (ru first, then en, then others; each label up to half) -> cap 20k rows/language (water-filling across datasets; rasheq weight 4) -> leakage check vs real_all.jsonl (exact normalized text or char-5gram Jaccard >= 0.5).

- Dedup removed 141743 rows; 12 rows dropped as label conflicts.
- Leakage check dropped 0 rows (filter verified with a positive control: all real items and lightly edited copies are caught).
- `language`: lang_tag() for Cyrillic text (ru / mixed / kk); ISO code from the source otherwise (hi-Latn etc. = romanised code-mixed text). `kind`: sms | message | email | call_turn.
- Licences: CC BY-SA (scambench) and GPL (dbarbedillo) rows carry share-alike/copyleft terms; filter by `license` if that matters.

## Totals by language

| language | scam | legit |
|---|---|---|
| ru | 773 | 14969 |
| en | 8484 | 11516 |
| az | 363 | 2913 |
| hi-Latn | 1216 | 874 |
| bn | 281 | 473 |
| hi | 398 | 449 |
| pa | 231 | 364 |
| mr | 237 | 359 |
| ks | 227 | 356 |
| gu | 250 | 349 |
| ro | 85 | 85 |
| bn-Latn | 69 | 66 |
| te-Latn | 62 | 63 |
| mr-Latn | 65 | 62 |
| ta-Latn | 64 | 61 |
| es | 100 | 31 |
| pt | 65 | 28 |
| vi | 38 | 27 |
| ko | 72 | 27 |
| ar | 53 | 25 |
| fr | 34 | 22 |
| de | 34 | 22 |
| te | 20 | 20 |
| tr | 36 | 20 |
| ml | 20 | 20 |
| as | 20 | 20 |
| kn | 20 | 20 |
| or | 25 | 19 |
| ta | 25 | 13 |
| th | 34 | 7 |
| uz | 4 | 4 |
| mixed | 0 | 1 |
| ja | 2 | 0 |
| zh | 5 | 0 |

## Datasets used

### DmitryKRX/anti_spam_ru

- **What:** Russian anti-spam corpus (66k): real Russian tech-chat (ODS-style) + machine-translated Enron/SpamAssassin/UCI SMS + LLM-written spam posts.
- **Licence:** apache-2.0
- **Kept:** 15000 rows - scam 577 / legit 14423; by language (scam/legit): ru 577/14422, mixed 0/1; kinds: {'message': 15000}
- **Label mapping:** ham -> 0. spam -> 1 ONLY if it matches a social-engineering cue (prize/win, account blocked, password/card data, fake investment / get-rich-quick, fines, parcels) and no advertising cue (pharma, adult, loans, discounts, products, 'chance to win' competitions, hashtags); all other spam (advertising) dropped. 'Get rich quick' posts thinned to 1/4 (near-paraphrases). Latin-only rows dropped.
- **Quality notes:** Scam side is mostly UK premium-rate prize SMS (machine-translated, '£', 'фунтов') and LLM get-rich-quick posts: style differs from KZ scams. Legit side is real Russian chat + MT e-mails/SMS; topically off-domain (ML/data-science chat). 95% legit.

Samples:

- `1` [ru, message] 🚨 ВАУ, ВЫ НЕ ПОВЕРИТЕ, ЧТО ТОЛЬКО ЧТО ПРОИЗОШЛО!!! 🤑🤑🤑 🎁🎁🎁 БЕСПЛАТНЫЕ ПОДАРОЧНЫЕ КАРТЫ ДЛЯ ВСЕХ!!! 🎁🎁🎁 👉 Привет, ребята, это ваша любимая социальная сеть! Вам надоело видеть одно и то же в своей ленте каждый день? Хотите
- `1` [ru, message] Выиграйте БЕСПЛАТНЫЕ iPhone и iPad, нажав на эту ссылку! Ограниченное по времени предложение!
- `1` [ru, message] Позвоните нашему представителю службы поддержки клиентов по БЕСПЛАТНОМУ ТЕЛЕФОНУ 0808 145 4742 с 9 00 до 23 00 так как вы ВЫИГРАЛИ гарантированный приз в размере 1000 фунтов стерлингов наличными или 5000 фунтов стерлинго
- `0` [ru, message] Я ищу набор данных, связанный с обнаружением объектов, чтобы обнаружить объект после того, как дом/офис пережил пожар. Есть ли у кого-нибудь наводка на этот тип данных, доступны ли они или нет, или какие-либо наводки отн
- `0` [ru, message] На самой новой не пошло

### rasheq/scam-shield-sms

- **What:** English SMS: IMC-2025 public smishing reports (real), Mishra & Soni SMS ham (UCI-like), synthetic safe service messages from 21 countries (OTP, bank alerts, deliveries).
- **Licence:** cc-by-4.0
- **Kept:** 8777 rows - scam 4389 / legit 4388; by language (scam/legit): en 4389/4388; kinds: {'sms': 8777}
- **Label mapping:** scam -> 1, safe -> 0 (source already drops advertising spam). Masks mapped: <URL> -> <url>, <PHONE_NUMBER> -> [PHONE], <EMAIL_ADDRESS> -> <url>, <NUMBER> -> random 6-digit number. Rows with masking glitches ('<URL>ease') and IMC 'scam' rows that are genuine OTP notices ('do not share this code') dropped.
- **Quality notes:** Some IMC reports are benign messages people reported (label noise). Given 4x weight in the English language cap (real data).

Samples:

- `1` [en, sms] Verizon Free Msg: bill processed. Thanks, ! Here's a little gift for you: <url>
- `1` [en, sms] Dear SBI user Your SBI YONO And Sbi Account will be blocked within please update your PAN CARD NUMBER by clicking the link Thank you SBI
- `1` [en, sms] Get entertained with drama series like , Blue Bloods, , and more on CH19. Dial *423*3# to Pay and enjoy. STOP*456*9*5#
- `0` [en, sms] […] anyway, many good evenings to u! s
- `0` [en, sms] Hey happy birthday...

### anmolshrivastav/scam_ham_india_14_languages

- **What:** 14k template SMS (7k scam / 7k ham) in 14 Indian languages.
- **Licence:** mit
- **Kept:** 5255 rows - scam 2132 / legit 3123; by language (scam/legit): bn 281/473, hi-Latn 290/459, pa 231/364, mr 237/359, ks 227/356, gu 250/349, hi 254/340, en 232/311, as 20/20, kn 20/20, ml 20/20, te 20/20, or 25/19, ta 25/13; kinds: {'sms': 5255}
- **Label mapping:** scam -> 1, ham -> 0.
- **Quality notes:** Heavily templated (names/numbers swapped): template dedup keeps ~5k. Non-English rows are translations of the same templates.

Samples:

- `1` [bn, sms] Netflix সাবস্ক্রিপশনের মেয়াদ শেষ হচ্ছে, রিনিউয়াল ১৯৯ টাকায়। পে করুন <url> নাহলে অ্যাকাউন্ট সাসপেন্ড। - Netflix ইন্ডিয়া
- `1` [hi-Latn, sms] Flipkart se baat kar rahe hain sir, aapka refund 16,000 pending hai. OTP aa raha hai na? Wo bata dijiye, main refund release kar deta hun.
- `1` [kn, sms] ಆಧಾರ್ ಲಿಂಕ್ ಆಗಿಲ್ಲದ ಕಾರಣ ಬ್ಯಾಂಕ್ ಸೇವೆ ನಿಲ್ಲುತ್ತದೆ. OTP ಮತ್ತು ಆಧಾರ್ ವಿವರ ಕಳುಹಿಸಿ. ಉಲ್ಲೇಖ 6.
- `0` [mr, sms] प्रिय विक्रम, तुमचे लायब्ररीचे पुस्तक 20 सप्टेंबर रोजी परत करायचे आहे. विलंब शुल्क टाळण्यासाठी कृपया वेळेत परत करा.
- `0` [hi-Latn, sms] Udaipur ki tickets book ho gayi 12 ko, packing start kar de

### VusalShahbazovAz/smishing-AZ-SC

- **What:** 4.5k Azerbaijani SMS (ham / spam / smishing); partly translated UCI SMS.
- **Licence:** cc-by-4.0
- **Kept:** 3276 rows - scam 363 / legit 2913; by language (scam/legit): az 363/2913; kinds: {'sms': 3276}
- **Label mapping:** smishing -> 1 only if it has a scam cue (prize, urgent, account, card, password, delivery, tax/fine, bank, link) and is not a translated premium-rate ad (ringtones, minutes, video phones, coupons). spam (advertising) dropped. ham -> 0.
- **Quality notes:** Turkic language (Latin script); mix of real local SMS and translations.

Samples:

- `1` [az, sms] Açıq ŞanslıTəsadüfi Çəkilişə qatıldınız və Tata Safari qazandınız! Əlaqə: 99XXXXXXXXX - 2294871295 Ətraflı məlumat: <url>
- `1` [az, sms] Bu gün üç ayrı vaxtda müəyyən edilmiş 1 millik radiusdan çıxdığınız üçün sizə cərimə bildirişi göndərilib. Bildiriş seçki siyahısında göstərilən ünvanınıza göndərilib. Daha ətraflı məlumat və apellyasiyalar üçün gov.az/c
- `1` [az, sms] Siz qalibsiniz! Siz xüsusi olaraq 1000 AZN nağd pul və ya 4 otel və uçuş daxil olmaqla tətillər almaq üçün seçilmişsiniz. Mükafatı tələb etmək üçün canlı operatorla danışmaq üçün 08XXXXXXX nömrəsinə zəng edin.
- `0` [az, sms] Asan satıla biləcək bir şey göndərmək istəyirəm. pul qazanmaq asan deyil.
- `0` [az, sms] Maaiyyə problemini mən həll edəcəm :) kömək edəcəm.

### FredZhang7/all-scam-spam

- **What:** 42k English spam/ham: UCI SMS, Enron + SpamAssassin e-mails, ~1k hand-collected multilingual chat.
- **Licence:** apache-2.0
- **Kept:** 2222 rows - scam 161 / legit 2061; by language (scam/legit): en 152/2042, ru 9/19; kinds: {'email': 1914, 'sms': 280, 'message': 28}
- **Label mapping:** ham -> 0. spam -> 1 only if SMS with a social-engineering cue (prize/claim/account/refund...) without advertising cues, or an e-mail with an unmistakable phishing/419 cue; everything else (pharma, watches, software, loans, stocks) dropped. Non-English Latin rows dropped (no language code).
- **Quality notes:** Legit side is mostly Enron/mailing-list e-mail: off-domain.

Samples:

- `1` [en, sms] URGENT! Your Mobile No was awarded a £2,000 Bonus Caller Prize on 1/08/03! This is our 2nd attempt to contact YOU! Call 0871-4719-523 BOX95QU BT National Rate
- `1` [en, sms] Dear Dave this is your final notice to collect your 4* Tenerife Holiday or #5000 CASH award! Call 09061743806 from landline. TCs SAE Box326 CW25WX 150ppm
- `1` [en, sms] T-Mobile customer you may now claim your FREE CAMERA PHONE upgrade & a pay & go sim card for your loyalty. Call on 0845 021 3680.Offer ends 28thFeb.T&C's apply
- `0` [en, email] gtc vs . master louise , the consensus which emerged from the meeting this morning is that the power guys would like to have a full blown master agreement on enrononline instead of a simpler gtc . obviously , i can put e
- `0` [en, email] congratulations your majesty , congratulations on your well deserved promotion to managing director . i am very happy for you and a little sad as well because this was so long overdue . the list every year was not comple

### BothBosu/scam-dialogue

- **What:** 1.6k synthetic English phone dialogues (caller/receiver), 8 types (ssn, refund, support, reward, delivery, insurance, telemarketing, wrong number).
- **Licence:** apache-2.0
- **Kept:** 2195 rows - scam 1098 / legit 1097; by language (scam/legit): en 1098/1097; kinds: {'call_turn': 2195}
- **Label mapping:** Split into turns; only caller turns kept. Scam dialogue -> caller(scammer) turns = 1; legit dialogue -> caller turns = 0; receiver turns dropped.
- **Quality notes:** Turn labels inherit the dialogue label: some scammer turns are generic ('Let me check that for you'). Legit side includes telemarketing sales calls (kept as legit: harmless).

Samples:

- `1` [en, call_turn] Our website might be experiencing some technical difficulties. But trust me, you won't want to miss out on this opportunity.
- `1` [en, call_turn] Let me check on that. Okay, it says here that you're owed $500 from a purchase you made at Walmart last year.
- `1` [en, call_turn] Just your Windows login credentials and credit card information to process the payment for the service.
- `0` [en, call_turn] No, not exactly. We're just calling to let people know about the offer and see if they're interested.
- `0` [en, call_turn] We're offering a special promotion on our eco-friendly cleaning products and I was wondering if you'd be interested in learning more about it.

### BothBosu/multi-agent-scam-conversation

- **What:** 1.6k synthetic English dialogues between two LLM agents (victim personality varied).
- **Licence:** apache-2.0
- **Kept:** 2195 rows - scam 1097 / legit 1098; by language (scam/legit): en 1097/1098; kinds: {'call_turn': 2195}
- **Label mapping:** Suspect turns only: scam -> 1, legit -> 0.
- **Quality notes:** Longer, more natural turns than the other BothBosu sets.

Samples:

- `1` [en, call_turn] Thank you, Mr. Johnson. I've updated your address in our system. Just one more thing to finalize the refund. I need you to create a temporary password to access your refund account. Can you please choose a password and s
- `1` [en, call_turn] Thank you, Emily. I've got that information recorded. Just one more step to finalize the refund. We need to process a small verification fee of $29.95 to ensure the refund is legitimate and to prevent any fraud. I can wa
- `1` [en, call_turn] Hello, is this Emily Wilson? My name is Officer James from the Social Security Administration. We've been trying to reach you regarding a serious issue with your social security number. It's been suspended due to suspici
- `0` [en, call_turn] You're welcome, Emily. I've verified the details and everything looks good. Your package will be delivered to 123 Main Street, Apartment 4B between 10am and 2pm today. Thank you for your time, and we'll see you soon. Hav
- `0` [en, call_turn] I completely understand your skepticism. I would do the same in your shoes. Why don't I give you our company's customer service number, and you can call them directly to verify my identity and the purpose of my call? Tha

### BothBosu/single-agent-scam-conversations

- **What:** 1.6k synthetic English dialogues (Suspect/Innocent), same 8 types.
- **Licence:** apache-2.0
- **Kept:** 2194 rows - scam 569 / legit 1625; by language (scam/legit): en 569/1625; kinds: {'call_turn': 2194}
- **Label mapping:** Suspect turns only: scam -> 1, legit -> 0.
- **Quality notes:** 92% of its scam turns duplicate BothBosu/scam-dialogue (removed by dedup), hence fewer scam rows. In a few legit dialogues the 'Suspect' is the customer.

Samples:

- `1` [en, call_turn] We'll credit it back to your card. But like I said earlier, I need to verify some information with you first.
- `1` [en, call_turn] I'd be happy to explain, but first, can you please confirm your social security number so I can access your account?
- `1` [en, call_turn] Oh, um, we got it from a third-party marketing firm that we work with. They provided us with a list of eligible customers.
- `0` [en, call_turn] No need to apologize, Emily. I'm just glad we were able to clear things up. Would you like to confirm the appointment for tomorrow at 2 PM?
- `0` [en, call_turn] We met in college, we're old friends. Do you think I might have the wrong number?

### Ridham115/indian-scam-sms-synthetic-audited

- **What:** 1.6k LLM-written Indian scam SMS and genuine look-alikes (en, hi, Hinglish, Roman-script bn/mr/ta/te), label-audited.
- **Licence:** cc-by-4.0
- **Kept:** 1580 rows - scam 797 / legit 783; by language (scam/legit): hi-Latn 324/315, en 126/136, hi 87/80, bn-Latn 69/66, te-Latn 62/63, mr-Latn 65/62, ta-Latn 64/61; kinds: {'sms': 1580}
- **Label mapping:** scam -> 1, safe -> 0 (audited labels used).
- **Quality notes:** Good hard negatives (real bank/courier/bill SMS). Generated with Gemini / gpt-oss: provider terms may apply.

Samples:

- `1` [ta-Latn, sms] Badhaiya irukku unga numberuku 50 lakhs jackpot vizhundhurukku. Tax fees katti amounta anuppu, link bit.ly/kbcprize982 click pannu.
- `1` [hi-Latn, sms] Alert: Rs 29,999 deducted successfully from your ICICI Bank account via UPI ref 48291048. To cancel this transaction and get a full refund, verify your debit card PIN and OTP on this secure page: <url>
- `1` [hi-Latn, sms] Urgent requirement of cash? Get instant loan up to Rs 10 Lakhs in your account today. No salary slip needed, 0% interest for first 3 months. Download app: <url>
- `0` [hi-Latn, sms] Axis Bank Update: EMI of Rs 12350 successfully debited from your a/c XX5839 on 10 Oct. Txn ID: AXIS8472910. Thank you.
- `0` [en, sms] Your HDFC Bank debit of INR 4,720.00 from A/C XXXX3421 is successful. Ref ID: TXN9K3L8M. Do not share this OTP 839274 with anyone.

### BothBosu/Scammer-Conversation

- **What:** 1k synthetic 'Person A / Person B' conversations; scam = Person A impersonates bank/insurance/tax; legit = friends' small talk.
- **Licence:** apache-2.0
- **Kept:** 1187 rows - scam 495 / legit 692; by language (scam/legit): en 495/692; kinds: {'call_turn': 1187}
- **Label mapping:** Person A turns only: scam -> 1, legit -> 0.
- **Quality notes:** Very templated ('this is X from the bank's fraud department...'); legit side is hobby small talk.

Samples:

- `1` [en, call_turn] Hello, this is Noah from the bank's fraud department. We detected unauthorized activities on your account and need to verify your account details.
- `1` [en, call_turn] Hello, this is Michael from the bank's fraud department. We detected unauthorized transactions on your account and need to verify your account details.
- `1` [en, call_turn] Good morning, I'm calling from the financial institution's fraud department. We've identified unusual activities on your account and need to verify your personal information.
- `0` [en, call_turn] I've been exploring Latin and ballroom dances, it's been quite rewarding.
- `0` [en, call_turn] I'm doing fine. I've been playing musical instruments in my free time.

### shaw/scambench-training

- **What:** Agent-safety corpus (37k multi-turn chats to an AI agent, 14 languages). Only the hand-built 'generated-culture-*' subset (1.3k, culture-specific scams per language: FSB/Sberbank calls, Avito, GIBDD fines, Gosuslugi, PIX, Enkeltrick...) is used.
- **Licence:** cc-by-sa-4.0
- **Kept:** 845 rows - scam 580 / legit 265; by language (scam/legit): es 100/31, hi 57/29, pt 65/28, ko 72/27, ru 50/27, vi 38/27, ar 53/25, de 34/22, fr 34/22, tr 36/20, th 34/7, ja 2/0, zh 5/0; kinds: {'message': 678, 'email': 54, 'sms': 95, 'call_turn': 18}
- **Label mapping:** scam conversation -> its last user turn (the scam payload) = 1. legit conversation -> its user inquiry turns (e.g. 'How do I check GIBDD fines on Gosuslugi?') = 0. Small-talk filler that also appears in scam conversations is skipped. The rest of ScamBench (prompt injection, jailbreaks, agent-addressed boilerplate, leetspeak) dropped: turn text does not carry the label.
- **Quality notes:** Templated (many repeats removed by dedup). Legit side is mostly questions ABOUT scams (hard negatives). CC BY-SA: derived data inherits ShareAlike.

Samples:

- `1` [hi, message] आपके PAN कार्ड में गड़बड़ी है। इनकम टैक्स विभाग के लिए सत्यापन ज़रूरी है: <url>
- `1` [vi, message] Em ơi, anh đây! Anh bị mất ví, cần gấp 3 triệu để đóng viện phí. Chuyển khoản giúp anh nhé: 6536 8849 70. Anh sẽ trả lại ngay khi về nhà.
- `1` [de, message] Kanzlei Schmidt & Partner: Abmahnung gem. §97 UrhG. Illegaler Download festgestellt. Unterlassungserklärung und Schadensersatz: 1.200€. Frist: 5 Werktage.
- `0` [ar, sms] كيف أبلّغ عن رسالة احتيالية وصلتني؟
- `0` [ar, sms] كيف أقدر أحصل على تقرير ائتماني؟

### ysangam/Indian_Cyber_Scam_PhoneCall_Hinglish_Dataset

- **What:** 10k Hinglish call lines (police / 'digital arrest' / KYC / lottery vs. family, office, delivery calls).
- **Licence:** apache-2.0
- **Kept:** 702 rows - scam 602 / legit 100; by language (scam/legit): hi-Latn 602/100; kinds: {'call_turn': 702}
- **Label mapping:** label 1 -> 1, 0 -> 0.
- **Quality notes:** Random opener + body templates; scam_category often mismatches the body. Collapses to ~700 rows after template dedup.

Samples:

- `1` [hi-Latn, call_turn] Cyber Crime Department se bol raha hoon. Cyber Crime Department se bol raha hoon. Aapke number se objectionable content circulate hua hai.
- `1` [hi-Latn, call_turn] Ji haan suniye Aapke Aadhaar se linked account par complaint mili hai.
- `1` [hi-Latn, call_turn] Ji haan suniye Aapke Aadhaar card ka istemal karke fake SIM issue ki gayi hai.
- `0` [hi-Latn, call_turn] Namaste ma'am Sir kal subah 10 baje meeting hai, agenda mail kar diya.
- `0` [hi-Latn, call_turn] Namaste sir Papa train mein baith gaya hoon, safely pahunch jaunga.

### dbarbedillo/SMS_Spam_Multilingual_Collection_Dataset

- **What:** UCI SMS Spam Collection machine-translated (M2M100-418M) into 20 languages; only the Russian column used.
- **Licence:** gpl
- **Kept:** 632 rows - scam 134 / legit 498; by language (scam/legit): ru 134/498; kinds: {'sms': 632}
- **Label mapping:** spam -> 1 only if the English original is a fake prize/claim/account message (else advertising, dropped). ham -> 0, but capped at 3x the scam count. Untranslated / degenerate-repetition MT rows dropped.
- **Quality notes:** Poor MT quality (broken Russian, leftover English); UK premium-rate scams. Excluded from the translation pool. GPL licence.

Samples:

- `1` [ru, sms] Поздравления Вы выиграли. Вы выиграли в нашем августе 1000 фунтов стерлингов. звоните 09066660100 NOW.
- `1` [ru, sms] Это второй раз, когда мы попытались связаться с U. Вы выиграли премию £1450, чтобы претендовать только звонить 09053750005 b4 310303.
- `1` [ru, sms] Вам гарантируется новейший телефон Nokia, 40 ГБ iPod MP3 плейер или 500 фунтов стерлингов! текст слова: COLLECT to No: 83355! IBHltd LdnW15H 150p/Mtmsgrcvd18
- `0` [ru, sms] Хорошо, я буду писать вам в нескольких
- `0` [ru, sms] Пожалуйста, напишите мне, когда вы выходите

### flowxai/scamguardbench

- **What:** Scam-detection benchmark v0.2 (EN/RO, synthetic) with a hard-legit subset (OTP, bank alerts, courier, utility...).
- **Licence:** apache-2.0
- **Kept:** 419 rows - scam 207 / legit 212; by language (scam/legit): en 122/127, ro 85/85; kinds: {'sms': 313, 'message': 66, 'email': 40}
- **Label mapping:** standard + hard: scam_likely -> 1, no_indicators -> 0. 'suspicious' subset dropped (ambiguous). Legit items of class family_money_request ('new number, send money') and marketing_promo ('you won a voucher') DROPPED: in KZ these are scam patterns.
- **Quality notes:** It is someone else's test set: do not report results on it after training.

Samples:

- `1` [en, sms] NOTICE: Unusual access detected on your account. Immediate action needed—complete identity reconfirmation in next 24 hours or restrictions apply. Visit <url> to proceed with verification. Do not delay.
- `1` [ro, sms] URGENT! Ati fost selectati pentru programul de investitii AI garantat. Dubla-ti banii in 7 zile, fara risc, profit 40% lunar SIGUR. Doar 100 lei pentru inceput. Trebuie astazi, pana la ora 18:00 sau locurile se termina! 
- `1` [ro, sms] Notificare urgenta: S-au detectat activitati neobisunuite pe profilul dvs. Aveti pana la ora 14:00 sa validati informatiile personale altfel accesul va fi restrictionat definitiv. Intrati pe <url> sau contactati departam
- `0` [ro, email] Buna, am primit o tranzactie pe cardul tau. Codul de verificare este 847293. Nu raspunde la nimeni cu acest cod. Daca nu ai facut aceasta operatiune, suna imediat la numarul din spatele cardului. Multumesc.
- `0` [en, sms] Your card ending 7492 was used for a purchase of £34.99 at SuperMart on 15 Nov at 14:23. If this wasn't you, call the number on the back of your card right away.

### BothBosu/youtube-scam-conversations

- **What:** 20 real scam-baiting call transcripts (YouTube: Scammer Payback etc.).
- **Licence:** apache-2.0
- **Kept:** 204 rows - scam 204 / legit 0; by language (scam/legit): en 204/0; kinds: {'call_turn': 204}
- **Label mapping:** Suspect (scammer) turns with >= 8 words -> 1 (all dialogues are scams). Shorter turns dropped as label noise ('Yes, open it').
- **Quality notes:** Real speech, but many turns are procedural (remote-access instructions).

Samples:

- `1` [en, call_turn] Okay, and can you please confirm what do you see on your computer right now? What do you see?
- `1` [en, call_turn] And next to the Ctrl key, which key do you see over there?
- `1` [en, call_turn] Do you have a piece of paper and pen handy with you so I can provide you my information too?

### Bektemir96az96/Uzbek_and_Russian_Phishing_dataset

- **What:** Uzbek + Russian SMS phishing (UzPhishNet), 100k rows.
- **Licence:** apache-2.0
- **Kept:** 14 rows - scam 7 / legit 7; by language (scam/legit): uz 4/4, ru 3/3; kinds: {'sms': 14}
- **Label mapping:** SOURCE LABEL IS INVERTED: 0 = phishing -> 1, 1 = legitimate -> 0.
- **Quality notes:** Only 14 templates (random URLs/numbers): collapses to 14 rows after template dedup.

Samples:

- `1` [uz, sms] Diqqat! Hisobingiz bloklandi. Tiklash uchun quyidagi havolaga o'ting: <url>
- `1` [uz, sms] Tabriklaymiz! Siz yutuq sohibi bo'ldingiz. Mukofotni olish uchun: <url>
- `1` [ru, sms] Срочно! Ваш аккаунт был взломан. Перейдите по ссылке для восстановления: <url>
- `0` [uz, sms] Xabaringiz muvaffaqiyatli yetkazildi.
- `0` [ru, sms] Здравствуйте, это напоминание о вашей встрече завтра в 10:00.

## Checked and skipped

| dataset | licence | reason |
|---|---|---|
| vichetkao/Scam_Message_9_Language | MIT | Gated (manual approval) - not accessible with the current HF token. |
| M-Arjun/SpamShield-Datasets | CC BY 4.0 | Gated (auto-approval needs accepting terms and sharing contact info in the browser) - not done on the user's behalf. Card: mostly generic/advertising 'spam' (72k 'spam' vs ~1k phishing/job_scam), 636 Russian spam rows. |
| Nachammai41/fraud-detection-underserved-20k (+ persona_conditioned v2/v3/v4) | CC BY 4.0 | Not messages: first-person victim narratives attached to synthetic transactions; is_fraud is a transaction label that contradicts the text (is_fraud=0 narratives describe being defrauded). Mostly >80 words. |
| Aleksandr505/PhishingDatasetExtended | none | No licence on the card -> skipped per rules (770 clean ru/en phishing vs legit service messages; would be useful if the author adds a licence). |
| shakeleoatmeal/phone-scam-detection-synthetic | MIT | Legit SSA calls ask for SSN/identity verification in 77% of cases: harmful hard negatives. |
| jencyyy/fraudcall | MIT | Bengali-only MT of Chinese fraud calls; labels visibly inconsistent (shopping enquiries labelled fraud, loan pitches legit); not split by speaker. |
| oscarwu/ScamWorld, ruSpamModels/russian-spam-detection, AugustLight/telegram_spam_ru, BLISS-e-V/SCAM, Scam-AI/* | CC BY-NC* | Non-commercial licences. |
| useKled/*, DominicTWHV/Discord-Scams | other | No open licence. |

## hf_extra_to_translate.jsonl

6000 rows for later MT into Kazakh, balanced {1: 3000, 0: 3000}; languages {'en': 4650, 'ru': 1350}. English/Russian rows of 4-30 words from hf_extra, excluding e-mails and the low-quality MT source (dbarbedillo). The file is frozen (already sent to MT); note it still contains some UK premium-rate prize SMS in Russian MT ('фунтов', 'Txt') from anti_spam_ru - low value for KZ, can be filtered after MT. Ranked by topic cue (banks, cards, police/courts, prizes, parcels/customs, relatives, investments/crypto, jobs, tech support, OTP/passwords, Gosuslugi/tax/fines) + kind (call_turn > sms > message), max 35% of each label from one source.
Sources: {'rasheq/scam-shield-sms': 2100, 'DmitryKRX/anti_spam_ru': 1300, 'BothBosu/scam-dialogue': 790, 'BothBosu/single-agent-scam-conversations': 627, 'BothBosu/Scammer-Conversation': 395, 'anmolshrivastav/scam_ham_india_14_languages': 300, 'Ridham115/indian-scam-sms-synthetic-audited': 153, 'FredZhang7/all-scam-spam': 107, 'BothBosu/multi-agent-scam-conversation': 79, 'flowxai/scamguardbench': 67, 'BothBosu/youtube-scam-conversations': 41, 'shaw/scambench-training': 39, 'Bektemir96az96/Uzbek_and_Russian_Phishing_dataset': 2}
