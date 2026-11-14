# Сақ бол: catching phone and message scams in Kazakh, Russian and the mix people actually type

**Track:** Finance
**Team:** TBD

This project is a prototype and is not financial advice.

## The problem

Gulnara apa is 67 and lives in Astana. Her first language is Kazakh. Her phone rings: "Kaspi security service, someone is taking a loan in your name, read me the code we just sent so we can cancel it." In 2025 Kazakhstan registered 27,892 internet-fraud cases, a record (Committee on Legal Statistics, via bizmedia.kz, 2026-10-12). Phone scams are 22% of the schemes the National Bank's antifraud center sees. Since 1 October 2026 every lender must ask seven anti-fraud questions before an online loan, and two of them are exactly this call: "did someone claiming to be bank or police security contact you?" and "are you moving money to a safe account?"

Scam filters are built for English and, at best, Russian. We found no public labelled scam dataset in Kazakh (Hugging Face, Kaggle and GitHub, checked 2026-11-14). People in Kazakhstan also write in a Kazakh-Russian mix, and often type Kazakh on a Russian keyboard (қ becomes к, ү becomes у). A filter that only works in Russian protects the people who need it least.

## What we built

You paste a message, or a call transcript one line per turn. The model returns a risk band (scam / suspicious / no clear signs), highlights the phrase that drove the score, lists the red flags it matched, and gives one concrete action in Kazakh or Russian ("Тұтқаны қойыңыз. Банкке картаның артындағы нөмірге өзіңіз хабарласыңыз."). In call mode it re-scores after every turn, so you can see when the warning would fire.

## What we added

Our own idea. Three things we think are new:
1. A real Kazakhstan test set: every item copied word for word from a public page of a bank, regulator, police department or news outlet, with its URL and date, and checked by script against the saved page. It is used only for testing.
2. A language fairness check without any personal data. Language is the group. We compare the same official warning text in Kazakh and in Russian (translation pairs found with LaBSE), and the same Kazakh scam typed with and without Kazakh letters.
3. Honest bookkeeping: predictions were written down before training (SPEC.md), two of them turned out false, and we say so.

## How it works

**Test data, never trained on.** 800 real texts copied word for word from 300+ public pages: banks (Kaspi, Halyk, BCC, Otbasy), the regulator ARDFM, the National Bank, police and prosecutors, eGov, and Kazakh and Russian news. 578 are scams and 222 are legit (real bank SMS and push texts, and official anti-fraud advice). Each item keeps its URL and publication date. We split them once into a selection set (dev) and a test set, grouped so that the Kazakh and Russian versions of the same official text, found with the LaBSE sentence model, always land on the same side. The headline counts only full messages and call phrases of 5+ words: 254 scams in test (146 Kazakh, 108 Russian).

**Training data, about 81,000 rows.** No labelled Kazakh scam data exists, so we built it:
- open scam and legit corpora from Hugging Face (Russian, English and 15 other languages), with advertising spam removed;
- 6,000 of those translated into Kazakh with NLLB-200 1.3B;
- 4,850 synthetic Kazakhstan-specific messages and call phrases in Kazakh, Russian, mixed and keyboard-Kazakh, written by Claude under a fixed protocol, never shown the test set, with two scam types deliberately left out so we could test unseen schemes;
- 35,000 real everyday Kazakh and Russian chat lines and 5,000 rule-based bank, eGov and delivery notifications as negatives;
- keyboard-Kazakh copies of Kazakh rows (қ to к, ү to у and so on).

Every training row was compared with every real test item, and 171 near-copies were dropped.

**Model.** We fine-tuned `intfloat/multilingual-e5-large` (560M parameters, XLM-RoBERTa architecture) as a scam/legit classifier on Kaggle T4 GPUs, with fp16, AdamW, warmup plus cosine decay, and a class weight of 4 for scams. The final model averages several fine-tuned copies trained with different random seeds (their scores are z-scored against everyday chat, then averaged). We also tried XLM-R large, a Kazakh-only RoBERTa, and continued training of an existing multilingual scam detector. e5-large held up best on real Kazakhstan text. We picked the epoch and the ensemble with a rule we wrote down before the last training round: the highest threshold-free precision-recall score on dev, preferring fewer models when scores are close.

**Fair threshold for every model.** Each model, baselines included, gets the threshold that flags at most 1 in 100 everyday chat messages **and** at most 1 in 20 real bank notifications, both measured on dev. Then we count how many real scams it catches. We added the bank-notification condition after we caught our own model flagging real OTP SMS as scams, which the chat-only rule had hidden.

## Results

TBD after freeze. Headline: recall on real Kazakhstan scam messages and call phrases at no more than 1 false alarm per 100 everyday messages, per language, against the keyword rule, a generic spam filter, and an existing multilingual scam model.

## Where it fails

TBD after freeze.

## What we'd do next

TBD.

## Sources

See CREDITS.md.
