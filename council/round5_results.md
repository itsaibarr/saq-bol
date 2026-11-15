# Council round 5 (2026-11-15 ~19:00 UTC+5). Three Claude Opus delegates, read-only. Version 3 (Russian focus) iteration.

| Delegate | Lens | R1 | R2 | R3 | R4 | R5 |
|---|---|---|---|---|---|---|
| Claude Opus | ML evaluation rigor | 5.5 | 5.5 | 7.5 | 7.5 | 8.0 |
| Claude Opus | Hackathon judge | 6.5 | 6.5 | 8.0 | 8.0 | 8.5 (projected Round 1 ~86/100) |
| Claude Opus | Kazakhstan domain + language | 5 | 5.5 | 7 | 7.5 | 7.5 |

All three: the v3 iteration is valid. Checked: test C items unchanged since the lock (only the tag column added); mix v8 built after the lock; no v8 training row reaches Jaccard 0.5 with a test-C item; training Russian quotes share no publisher with test C; the A5 pick follows the written rule; v2 kept its frozen threshold; only the frozen v3 and v2 were scored on test C.

Fixed after round 5 (wording and disclosure only, nothing re-scored):
- "151 scams from 163 pages" -> 102 pages (163 counted legit pages too); non-Kazakhstan scams 35 pages, 16 publishers. README, SPEC and figure note.
- Bold lead now gives Russian and Kazakh with intervals and says the 90% overall clears by one text; "Russian reached it" -> point estimate only, neither interval excludes < 90%.
- "Test A (800 texts)" -> 575 texts, 254 scams. "Every choice was made on dev" -> selection and thresholds on dev, v3 data designed from test-B misses.
- Delivery-line false alarm: both versions flag "На ваше имя пришла посылка"; v3 adds "курьер не смог доставить заказ". 7 of v3's 16 extra catches are "no"-tagged lines. No legit call lines in test C.
- Keyboard Kazakh: 87.5% -> 83.3%, script-folded, v2 lost 6 on the same texts. Moldova added. Chat pool reuse stated. Recognizable Kazakh 90%. Kazakh gain (+15) larger than Russian (+7), likely from test B joining training.
- Disclosed in SPEC: rucis_065 nearly contained in a longer training quote (without it 66/75 = 88.0%); kk4_020 label noise (without it 135/150, Kazakh 41/47); clips not protect-checked (2 G8 clips vs a legit item); lock-note page count corrected after scoring; no git commit between A7 and scoring.
Open: team details (README "Team: TBD"), Hugging Face write token, demo video.
