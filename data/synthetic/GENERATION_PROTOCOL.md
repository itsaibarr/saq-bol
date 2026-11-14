# Synthetic data protocol (fixed 2026-11-14 16:05 UTC+5, before any model was trained)

Generator: Claude Opus 5.5 subagents, no web access, never shown any real collected item.
Held-out schemes (NOT generated, used to test unseen-scheme generalization): meter_replacement_biometrics, egov_eds_reissue.
Placeholders used in every source: [NAME] [PHONE] [CARD] [IIN] [LINK] (or a plausible fake domain).
Every generated row has synthetic=true and is excluded from headline numbers.

Row schema (JSONL): {"text", "label": "scam"|"legit", "language": "kk"|"ru"|"mixed"|"kbd", "scheme", "channel": "sms"|"messenger"|"call_turn", "pair_hint": short note of what makes it scam/legit, "synthetic": true, "generator": "claude-opus-5.5", "group": "G1".."G4"}

Language targets per agent: kk 35%, ru 25%, mixed 25%, kbd 15%. kbd = Kazakh typed with Russian look-alike letters (кайда, калай, жок, гой, ушин, бугин, рахмет, кеше, сагат) the way people type on a Russian keyboard.
Label balance: about 50/50. Channels: sms 40%, messenger 40%, call_turn 20%.
