# Synthetic call-phrase protocol v2 (fixed 2026-11-14 17:10 UTC+5, before generation)

Why: real Kazakhstan scam evidence is mostly what a scammer SAYS on a call (short turns), while v1 data was mostly whole SMS. v2 adds short spoken turns and short messages.

Generator: Claude Opus 5.5 subagents, no web access, never shown any real collected item (data/real_test/, data/processed/real_*.jsonl are off-limits).
Held-out schemes, still NOT generated: meter_replacement_biometrics (ЖКХ/ТКШ meter replacement, "pass biometrics"), egov_eds_reissue (ЭЦП/ЭЦҚ renewal, eGov signature).

Row schema (JSONL): {"text", "label": "scam"|"legit", "language": "kk"|"ru"|"mixed"|"kbd", "scheme", "channel": "call_turn"|"sms"|"messenger", "length_class": "short"|"medium", "synthetic": true, "generator": "claude-opus-5.5", "group": "G5".."G7"}
- Length: 4-25 words. About 60% "short" (4-10 words), 40% "medium" (11-25).
- Channel mix: call_turn 70%, sms 15%, messenger 15%.
- Language mix: kk 35%, ru 30%, mixed 20%, kbd 15%. Kazakh must be natural spoken Kazakh as used in Astana/Almaty, not translated bureaucratic Kazakh.
- Labels about 50/50.

Anti-shortcut rules (from council round 1):
- Scam and legit rows must share surface features at similar rates: polite openings, bank names, numbers, amounts, "[NAME]", "[PHONE]", urgency words, the phrase "мы никогда не спрашиваем код" / "кодты ешқашан сұрамаймыз" (real scammers say it too). No links or "[LINK]" in this batch at all.
- Legit calls must be realistic: bank call-centre reminders, card-ready calls, branch confirmations, couriers arranging delivery, clinic/polyclinic reminders, akimat/ЦОН callbacks, utility (ЕРЦ, Astana Energy) notices, mobile operator offers, relatives and colleagues talking about money normally, a police officer at a real station asking a witness to come in person.
- Scam turns cover many tactics and stages of a call: opener, building trust, creating fear, the ask, pressure, secrecy, follow-up. Not every scam turn contains the ask; label the whole turn scam if it is something a scammer says in a scam call and a legitimate caller would not.
- No two rows share a template. Vary wording, word order, register, typos, filler words (ну, вот, яғни, енді, короче, слушайте, тыңдаңыз).
