# Council round 6 (2026-11-15 ~19:30 UTC+5). Three Claude Opus delegates, read-only. Check of the round-5 fixes.

| Delegate | Lens | R4 | R5 | R6 |
|---|---|---|---|---|
| Claude Opus | ML evaluation rigor | 7.5 | 8.0 | 8.5 (satisfied after edits) |
| Claude Opus | Hackathon judge | 8.0 | 8.5 | 8.5, projected Round 1 ~87/100 (satisfied after the 406 fix) |
| Claude Opus | Kazakhstan domain + language | 7.5 | 7.5 | 8.0 (satisfied) |

All round-5 fixes verified against the reports and test-C data. Fixed after round 6:
- v2 Russian on test C is 86/103 = 83.5% (83.49), written as 83% (was 84%) in README, SPEC and the video script; Kazakh vs Russian gain +15 vs +8.
- Demo check: "406 test-C texts" -> 306 test-C texts and 100 chat lines.
- Non-Kazakhstan near-copy caveat now says it affects only that stratum (66/75), not the 151-text headline.
- Keyboard Kazakh: 87.5% is the 88% above; folding used the same letter map as 8,471 training rows, so a best case.
- Kazakhstan courier-code SMS ("Сообщите код курьеру после получения товара") noted as not flagged.
Not changed (scope): the title's "the mix people actually type" (test C has no mixed Kazakh-Russian scams; tests A/B did).
