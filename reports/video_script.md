# 2-minute demo video (screen recording + your voice)

Record the screen with QuickTime (File > New Screen Recording) while `python app.py` runs, and talk over it. Upload to YouTube as Unlisted.

| Time | On screen | Say (English) |
|---|---|---|
| 0:00-0:15 | README title and the recall chart | "Gulnara apa, 67, Astana. A caller says: Kaspi security, read me the code to cancel a loan in your name. Kazakhstan had a record 27,892 internet-fraud cases in 2025. Scam filters work in English and Russian, not Kazakh." |
| 0:15-0:35 | Message tab, first Kazakh example, click Тексеру | "She pastes the message. Red: likely scam. The highlighted phrase drove the score, the red flags are from the official list, and the advice is in Kazakh: hang up and call the number on your card." |
| 0:35-0:45 | The OTP example | "A normal bank code SMS that says 'never share this code' stays quiet." |
| 0:45-1:00 | Call tab, click the button | "Call mode re-scores after every line. The warning fires at line N, before the caller asks for the code." (read N off the screen) |
| 1:00-1:15 | Paste: Вам сообщили о попытке оформления кредита? Срочно созвонитесь с банком! | "Our first version flagged real bank warnings like this one: 14.5% of real service SMS were false alarms, against a 5% target. We retrained on real SMS; fresh SMS are still too few to measure the new rate." |
| 1:15-1:45 | Test C chart | "We copied 1,301 real scam and legit texts from 720 public pages. Version 1 caught 81% of real scams, against 44% for TF-IDF and 27% for the official keyword rule. Each time, the old test set went into training and we collected a new one. Version 2 was weak in Russian, so version 3 got more Russian data. On 151 scams set aside before training, version 3 catches 90%: 91% in Russian, 88% in Kazakh, against 80% for version 2 on the same texts." |
| 1:45-2:00 | Where it fails | "It still misses call openers with no scam signal, it flags some real courier messages, and Kazakh is not yet at 90%. Next: calibrate on volunteers' bank and delivery SMS, and real keyboard-Kazakh data. Prototype, not financial advice." |

# 5-minute finals plan
- 0:00-0:40 Gulnara, the moment of the call, the regulator's 7 questions (since 1 Oct 2026).
- 0:40-2:40 Live app: Kazakh scam, the same text in keyboard Kazakh, the OTP SMS staying safe, call mode, the real bank-SMS false alarm. Run locally with models preloaded; keep the video and Colab as backup.
- 2:40-3:50 How the test sets were built (1,301 texts, 720 pages, verbatim, URL + date), leakage drops, why the bank-SMS rule exists, the falsified predictions, the baseline chart, and the v2-to-v3 step on a fresh test set (80% to 90%, Russian 83% to 91%, p = 0.0003).
- 3:50-4:30 Fairness: Kazakh vs Russian on the same test set (88% vs 91%); keyboard Kazakh -4 points for v3 on test C; Russian outside Kazakhstan 88% from publishers never used in training.
- 4:30-5:00 Impact and next steps (speech-to-text, volunteer SMS calibration, a phone-sized model).

# Q&A prep (short answers)
- Precision? On test A, 205 of 219 flagged texts were scams (94%), at the test set's artificial mix of scams and legit texts.
- Why is the threshold 0.998? Scores are very confident; the threshold is whatever flags at most 1% of everyday chat and 5% of real service SMS on dev.
- Did you pick on test? No. Model choice and threshold on dev; each test set scored once after freezing (RUNS.md). Version 3 is the single model our pre-written rule picked over a 4-model ensemble.
- Isn't Claude-written training data circular? The test set is real public text, and the model catches 69% of scam types it never saw in training.
- Why no LLM baseline? Time; a zero-shot LLM is the obvious next comparison.
- Phone? Version 3 is one 560M-parameter model (1.1 GB); next step is a smaller distilled model.
