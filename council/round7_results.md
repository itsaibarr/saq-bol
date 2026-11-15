# Council round 7 (2026-11-15 ~20:40 UTC+5). Three Claude Opus delegates, read-only. README restructured around existing approaches vs ours.

| Delegate | Lens | R5 | R6 | R7 |
|---|---|---|---|---|
| Claude Opus | ML evaluation rigor | 8.0 | 8.5 | 8.5 (satisfied after wording fixes) |
| Claude Opus | Hackathon judge | 8.5 | 8.5 | 8.5, projected Round 1 ~88/100 (~90 after fixes) |
| Claude Opus | Kazakhstan domain + language | 7.5 | 8.0 | 7.0 (wording only) |

All three: the comparison is fair (same 151 texts, same dev threshold rule, the keyword rule's own setting favours it, A8 written at 19:33 before scoring at 19:36, threshold-free AP agrees: 0.76 open model vs 0.986 ours). Every table cell and paired count matches the reports.
Fixed after round 7 (wording only):
- "Tools available today" / "tools anyone could deploy" / "tools in use today" -> "existing approaches"; only the open scam model is a ready-made tool. Keyword rule relabelled "a keyword rule we wrote from official red-flag warnings"; spam filter described as our TF-IDF model on English SMS spam and a Russian spam corpus (mostly machine-translated email); "trained without Kazakh" removed (not verifiable).
- Keyword rule's flagged Kazakhstan SMS quoted ("Никому не сообщайте свой код", "Сообщите код курьеру после получения товара"); Kazakh 12.5% -> 13% to match the table.
- Keyboard test described as simulated (Kazakh letters swapped for Russian ones); the keyword rule applies the same map, so the test cannot change it; real typing variants listed.
- Team line: "tryHard" only (names and school go in the submission form). SPEC A8 scoring window 19:36-20:14. Figures re-rendered with the new labels.
