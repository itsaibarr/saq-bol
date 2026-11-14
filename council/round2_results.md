# Council round 2 (2026-11-14 ~20:50 UTC+5). Three Claude Opus delegates, high effort, read-only.

| Delegate | Lens | Round 1 | Round 2 |
|---|---|---|---|
| Claude Opus | ML evaluation rigor | 5.5/10 | 5.5/10 |
| Claude Opus | Hackathon judge | 6.5/10 | 6.5/10 (evaluation ~8/10, deliverables ~2/10) |
| Claude Opus | Kazakhstan domain + language | 5/10 | 5.5/10 |

## Agreed and acted on
- A4 (notification-aware threshold) is the honest operating point; keep it as the headline. Self-contained subset only as a secondary row; never lead with it or with the looser "suspicious" point.
- The A4 threshold rests on ~1 dev notification item, and the notification templates were written after inspecting dev errors: v6 dev numbers are optimistic. Only test counts. -> disclosed; epoch selection switched to a threshold-free criterion (AP of dev scams vs chat + real notifications).
- Format shortcuts ("bank format = legit", <url>/[PHONE]/KZT imbalance) -> official bank/gov domains get their own token (<url_official>, with lookalike protection), hotline numbers and official links added to legit notifications, stacked bilingual notifications replace the unrealistic mixed template, 2,500 "scam twins" in the same formats with a scam ask.
- Russian scam data thin/skewed -> Telegram job spam capped at 400, GBP prize SMS dropped, NLLB Kazakh rows halved; Russian-language scam texts from non-Kazakhstan sources collected for training only.
- Second blind annotator on 80 items: agreement 0.86 (kappa 0.76, 3-class), binary kappa 0.73. Tags frozen.
- Freeze the model at Sun 10:00 UTC+5; score real-test once; then deliverables only. Submit by Mon 06:00.

## Rejected
- A5 (separate thresholds for call mode vs message mode): would be a fifth operating-point change after seeing results; not adopted.
- Fresh calibration set from the team's own bank SMS: asked the user; used only if provided before the freeze.
