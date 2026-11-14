"""Upload the two frozen ensemble members to the Hugging Face Hub with a model card."""
import json, sys
from huggingface_hub import HfApi
api = HfApi()
r = json.load(open("runs/ens_v6c_e5s2s3_logit_z/final_report.json")); t = r["test"]["headline"]
for seed in ["s2", "s3"]:
    repo = f"itsaibarr/saq-bol-e5-{seed}"
    card = f"""---
license: cc-by-nc-sa-4.0
language: [kk, ru]
base_model: intfloat/multilingual-e5-large
pipeline_tag: text-classification
tags: [scam-detection, fraud, kazakh, russian, code-switching]
---
# Сақ бол scam classifier, ensemble member {seed}

One of two `intfloat/multilingual-e5-large` fine-tunes that together form the Сақ бол scam early-warning model for Kazakhstan (Kazakh, Russian, mixed, keyboard-Kazakh). Use both members, averaged on z-scored logits, as in https://github.com/itsaibarr/saq-bol (`app.py`). Inputs must be prefixed with `query: `. Label 1 = scam.

Ensemble results on a real, hand-collected Kazakhstan test set scored once after freezing: recall {t['recall']['rate']:.1%} on 254 scam messages and call phrases, {t['chat_fpr']['rate']:.1%} false alarms on everyday chat, {t['notification_fpr']['rate']:.1%} on real service SMS. Full report and limitations in the repository README.

Prototype for the Veritas AI International High School Hackathon 2026. Not financial advice. Licence is non-commercial because part of the training data (Telegram Corpus KAZ_RU) is CC BY-NC-SA 4.0.
"""
    api.create_repo(repo, repo_type="model", private=False, exist_ok=True)
    open(f"runs/kg_e5L_v6c_{seed}/best/README.md", "w").write(card)
    api.upload_folder(folder_path=f"runs/kg_e5L_v6c_{seed}/best", repo_id=repo, repo_type="model", commit_message="Frozen ensemble member")
    print("uploaded", repo)
