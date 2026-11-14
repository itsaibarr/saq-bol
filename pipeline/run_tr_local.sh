#!/bin/bash
cd "$(dirname "$0")/.."
export PYTORCH_ENABLE_MPS_FALLBACK=1
.venv/bin/python -u pipeline/src/translate_batch.py --inp data/processed/hf_extra_to_translate.jsonl --out data/processed/kk_tr_local_out.jsonl --bs 24 > logs/translate_local.log 2>&1
echo TR_DONE >> logs/translate_local.log
