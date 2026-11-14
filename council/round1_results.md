# Council round 1 (2026-11-14 ~16:15 UTC+5). Three Claude Opus delegates, high effort, read-only.

| Delegate | Lens | Score |
|---|---|---|
| Claude Opus | ML evaluation rigor | 5.5/10 |
| Claude Opus | Hackathon judge (official rubric) | 6.5/10 (projected Round 1 ~68/100, ceiling ~85) |
| Claude Opus | Kazakhstan domain + Kazakh language | 5/10 |

## Agreed findings (acted on)
1. Length shortcut: real scams are mostly short call phrases, real legit are long warnings; a length-only score gets PR-AUC 0.92-0.94. -> unit column, headline on full messages, length baseline in every table.
2. Translation-pair leak across dev/test (kk translations of ru items split apart). -> link pairs via the RU URL recorded in notes + text order, re-split, stratify by language.
3. Training shortcuts: [LINK] / defanged "[.]" / ".example" URLs only on scam rows; markdown in translated warnings; reassurance lines only in legit synthetic bank calls; noisy NLLB dokster translations. -> URL/markdown normalization, drop dokster-NLLB, drop reassurance legit rows.
4. Metrics: headline = recall at <=1% FPR on everyday chat (threshold from chat-dev only); PR-AUC vs chat at realistic prevalence; warnings FPR reported as a stress test; group bootstrap by source page + Wilson; paired model comparisons; hide n<10 slices.
5. Pre-registration: P1 and P2 are falsified by the baselines, report them as such; P3/P4 restated (amendment A2, after baselines were seen).
6. Demo: left-truncation for calls, kk/ru advice toggle, no false comfort on "safe", police/KNB and investment advice lines, Kazakh/Russian UI, sample call with harmless opening turns.

## Disagreement
- Temperature scaling: rigor lens says cut (does not change any metric), judge lens says keep. Decision: keep the code (already written), call the output a "risk score", do not claim calibrated probabilities.
- 2026 date slice: keep as a secondary slice, no headline.

## Cut (consensus)
Encoder sweep beyond one alternative (fine-tune the B5 checkpoint), dialogue early-warning metric, LLM baseline, model soup, conformal abstention, Tilmash, hosted Space, live ASR, real "mixed" claims (synthetic only), single language_gap number.
