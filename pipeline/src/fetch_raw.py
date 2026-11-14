"""Download public training sources into data/raw/<name>/ (parquet/jsonl as published)."""
import sys
from huggingface_hub import snapshot_download, HfApi
REPOS = {
    "dokster_scam_ru_en": "dokster/adaption-scam-dataset-ru-en-v1",
    "anti_spam_ru": "DmitryKRX/anti_spam_ru",
    "telegram_spam": "alt-gnome/telegram-spam",
    "bothbosu_single": "BothBosu/single-agent-scam-conversations",
    "bothbosu_multi": "BothBosu/multi-agent-scam-conversation",
    "fraudlens_ru": "Abdurohman/fraudlens-ru-v1",
    "tg_ru_kk": "kurumikz/telegram-corpus-russian-kazakh",
    "sms_spam_en": "ucirvine/sms_spam",
}
api = HfApi()
for name, repo in REPOS.items():
    try:
        info = api.dataset_info(repo)
        files = [s.rfilename for s in info.siblings]
        print(f"== {name} {repo} gated={info.gated} license={(info.card_data or {}).get('license') if info.card_data else None} files={files[:12]}")
        snapshot_download(repo, repo_type="dataset", local_dir=f"data/raw/{name}", allow_patterns=["*.parquet","*.jsonl","*.json","*.csv","*.txt","*.md","*.tsv"], max_workers=4)
    except Exception as e:
        print(f"!! {name} {repo}: {type(e).__name__}: {str(e)[:200]}")
