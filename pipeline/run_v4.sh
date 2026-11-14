#!/bin/bash
# Sequential, one MPS job at a time (an OOM killed the v3 chain when other MPS work ran alongside).
cd "$(dirname "$0")/.."
export PYTORCH_ENABLE_MPS_FALLBACK=1
M=data/processed/mix_v4
.venv/bin/python -u pipeline/src/train_encoder.py --mix $M --model kz-transformers/kaz-roberta-conversational --name enc_kazroberta_v4 --epochs 4 --lr 5e-5 --bs 32 --max-len 96 > logs/enc_kazroberta_v4.log 2>&1
.venv/bin/python -u pipeline/src/train_encoder.py --mix $M --model FacebookAI/xlm-roberta-base --name enc_xlmr_v4 --epochs 3 --lr 3e-5 --bs 32 --max-len 96 > logs/enc_xlmr_v4.log 2>&1
.venv/bin/python -u pipeline/src/train_encoder.py --mix $M --model Horizon-Labs/phishing-scam-detector-base --name enc_horizon_v4 --num-labels 3 --pos-idx 2 --epochs 3 --lr 2e-5 --bs 32 --max-len 128 > logs/enc_horizon_v4.log 2>&1
echo CHAIN_V4_DONE > logs/chain_v4.done
