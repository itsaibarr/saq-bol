# 2-minute demo video (screen recording + your voice)

Record the screen with QuickTime (File > New Screen Recording) while `python app.py runs/ens_v6c_e5s2s3_logit_z` runs, and talk over it. Upload to YouTube as Unlisted.

| Time | On screen | Say (English) |
|---|---|---|
| 0:00-0:15 | README title and the recall chart | "Gulnara apa, 67, Astana. A caller says: Kaspi security, read me the code to cancel a loan in your name. Kazakhstan had a record 27,892 internet-fraud cases in 2025. Scam filters work in English and Russian, not Kazakh." |
| 0:15-0:35 | Message tab, first Kazakh example, click Тексеру | "She pastes the message. Red: likely scam. The highlighted phrase drove the score, the red flags are from the official list, and the advice is in Kazakh: hang up and call the number on your card." |
| 0:35-0:45 | The OTP example | "A normal bank code SMS that says 'never share this code' stays quiet." |
| 0:45-1:00 | Call tab, click the button | "Call mode re-scores after every line. The warning fires at line N, before the caller asks for the code." (read N off the screen) |
| 1:00-1:15 | Paste: Вам сообщили о попытке оформления кредита? Срочно созвонитесь с банком! | "This is a real bank warning and we flag it. That is our main weakness: 14.5% of real service SMS were false alarms on test, against a 5% target." |
| 1:15-1:45 | Recall chart | "We tested on 800 real texts copied from 389 Kazakh public pages, never trained on. Two fine-tuned multilingual-e5 models catch 81% of real scams, against 44% for TF-IDF, 30% for an existing scam model and 27% for the official keyword rule." |
| 1:45-2:00 | Keyboard-Kazakh chart | "Kazakh typed on a Russian keyboard still costs us 10 points. Next: real keyboard-Kazakh data and calibrating on volunteers' bank SMS. Prototype, not financial advice." |

# 5-minute finals plan
- 0:00-0:40 Gulnara, the moment of the call, the regulator's 7 questions (since 1 Oct 2026).
- 0:40-2:40 Live app: Kazakh scam, the same text in keyboard Kazakh, the OTP SMS staying safe, call mode, the real bank-SMS false alarm. Run locally with models preloaded; keep the video and Colab as backup.
- 2:40-3:50 How the test set was built (389 pages, verbatim, URL + date), 155 leakage drops, why the bank-SMS rule exists, the falsified predictions, the baseline chart.
- 3:50-4:30 Fairness: keyboard Kazakh -10 points; identical official texts caught only in Russian 10 times vs only in Kazakh once; English junk text causes most chat false alarms.
- 4:30-5:00 Impact and next steps (speech-to-text, volunteer SMS calibration, a phone-sized model).

# Q&A prep (short answers)
- Precision? 205 of 219 flagged test texts were scams (94%), at the test set's artificial mix of scams and legit texts.
- Why is the threshold 0.99994? Scores are very confident; the threshold is whatever flags at most 1% of everyday chat and 5% of real service SMS on dev.
- Did you pick on test? No. Every choice on dev; test scored once after freezing (RUNS.md). The two seeds were the best two on dev, which we disclose.
- Isn't Claude-written training data circular? The test set is real public text, and the model catches 69% of scam types it never saw in training.
- Why no LLM baseline? Time; a zero-shot LLM is the obvious next comparison.
- Phone? Two large models are too big; next step is distilling into one small model.
