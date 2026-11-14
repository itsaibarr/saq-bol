#!/bin/bash
cd "$(dirname "$0")/.."
export PYTORCH_ENABLE_MPS_FALLBACK=1
.venv/bin/python -u pipeline/src/train_encoder.py --mix data/processed/mix_v5a --model kz-transformers/kaz-roberta-conversational --name enc_kazroberta_v5a --epochs 3 --lr 5e-5 --bs 32 --max-len 96 --scam-weight 4 > logs/enc_kazroberta_v5a.log 2>&1
echo DONE >> logs/enc_kazroberta_v5a.log
