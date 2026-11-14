#!/bin/bash
# Detached chain on the M5: XLM-R base, then the Horizon-Labs scam checkpoint (keeps its fraud head), both on mix_v3.
cd "$(dirname "$0")/.."
export PYTORCH_ENABLE_MPS_FALLBACK=1
.venv/bin/python -u pipeline/src/train_encoder.py --mix data/processed/mix_v3 --model FacebookAI/xlm-roberta-base --name enc_xlmr_v3 --epochs 4 --lr 3e-5 --bs 32 --max-len 96 > logs/enc_xlmr_v3.log 2>&1
echo CHAIN_STEP1_DONE >> logs/enc_xlmr_v3.log
.venv/bin/python -u pipeline/src/train_encoder.py --mix data/processed/mix_v3 --model Horizon-Labs/phishing-scam-detector-base --name enc_horizon_v3 --num-labels 3 --pos-idx 2 --epochs 3 --lr 2e-5 --bs 32 --max-len 128 > logs/enc_horizon_v3.log 2>&1
echo CHAIN_DONE >> logs/enc_horizon_v3.log
