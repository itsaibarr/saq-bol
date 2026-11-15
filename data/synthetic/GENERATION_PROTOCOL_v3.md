# Synthetic protocol v3, Russian focus (fixed 2026-11-15 15:05 UTC+5, before generation)

Why: version 2 is weakest in Russian. Russian scams are outnumbered about 10 to 1 by Russian legit rows in the v2 training mix, and some Russian scam families are almost absent (pension and social-payment "recalculation" offers). Families below were chosen from v2's misses on test set B, which is spent (it becomes training data for v3). Version 3 is scored on a new test set C that no generator sees.

Generator: Claude Opus 5.5 subagent, no web access. Off-limits: data/real_test/, data/processed/, data/train_extra/, runs/, reports/, council/, README.md, SPEC.md, RUNS.md, CREDITS.md. Read only this file and data/synthetic/GENERATION_PROTOCOL_v2.md.

Held-out schemes, still NOT generated: meter_replacement_biometrics (ЖКХ/ТКШ meter replacement, "pass biometrics"), egov_eds_reissue (ЭЦП/ЭЦҚ renewal, eGov signature). Also not generated: requests to vote in an online contest (kept as an unseen family on dev).

Output: data/synthetic/gen_G8.jsonl, 1,200 rows, same schema as v2 with "group": "G8".
- Labels: 600 scam, 600 legit.
- Language: ru 60%, mixed 20%, kk 10%, kbd 10%. Russian must be the Russian people speak in Kazakhstan (Kaspi, Halyk, ЕНПФ, ГФСС, ЦОН, eGov, Казпочта, Kcell, тенге, акимат), with real register variety: formal call-centre, casual chat, elderly speech, typos, no punctuation.
- Channel: call_turn 60%, sms 20%, messenger 20%. Length 3-25 words; about half "short" (3-10 words).

Scam families (about 60 rows each, all languages):
1. pension_social_recalc: ЕНПФ or ГФСС "доплата", "перерасчёт пенсии за прошлые годы", "возврат пенсионных взносов", "индексация", "компенсация вкладов", "единовременная выплата", "положена сумма, уже рассчитана"; the ask can come later in the call.
2. delivery_order_pretext: courier, Казпочта, flowers or a gift "from a man", "your order is at the warehouse", confirm the address, a code for delivery, an order you did not make.
3. relative_or_friend_messenger: new number, "can't talk, write here", accident or police trouble, hacked friend asking to borrow, an "old acquaintance" sending a photo or link.
4. isolation_instructions: during a call the scammer tells the victim to distrust anyone who tries to stop them (bank staff, cashier, relatives, police at the branch), to lie about the purpose of a transfer or loan, to keep the call open.
5. fake_security_or_police_stages: Russian call-centre scripts from "служба безопасности", "финмониторинг", АФМ, КНБ, полиция, across call stages (opener, trust, fear, ask, pressure, follow-up).
6. clickbait_and_prize_links: health or "you won't believe" lures, prizes, lotteries, surveys with payouts.
7. investment_and_side_income: guaranteed income, state-company shares, crypto, "second salary", paid tasks.
8. seller_buyer_marketplace: OLX/Krisha/Kolesa buyer or seller, discount for prepayment, QR-code payment, "safe deal" link.
9. operator_and_services: SIM-card or contract "renewal", number blocking, ЦОН callback, utility debt, internet provider.
10. loan_and_card: loan "in your name", "safe account", card blocked, SMS code request.

Legit counterparts (same surface features, same rates): real ЕНПФ/ГФСС notices about contributions, statements and payments that ask for nothing; real couriers and Казпочта arranging delivery; relatives and friends talking about money normally (including a new number, "can't talk"); bank staff and cashiers who ask about the purpose of a transfer (they are the real anti-fraud check); real investment-app and broker notices; real marketplace buyers and sellers; real operator and ЦОН notices; real bank call-centre reminders and OTP SMS that say "never share this code".

Anti-shortcut rules from v2 apply: shared surface features across labels (amounts, years, bank and agency names, [NAME], [PHONE], politeness, urgency words), no links or [LINK] at all, no shared templates, varied wording and register. A scam row is something a scammer says and a legitimate sender would not; an opener with no scam signal at all (a plain "your order is at the warehouse") should be written as legit unless the row itself carries a scam cue.
