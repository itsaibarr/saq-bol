#!/bin/bash
# Detached chain: finish Kazakh warning translations -> build mix_v2 -> train XLM-R v2. Survives session restarts.
cd "$(dirname "$0")/.."
export PYTORCH_ENABLE_MPS_FALLBACK=1
.venv/bin/python -u pipeline/src/translate_warnings.py 700 > logs/translate_warnings.log 2>&1
.venv/bin/python pipeline/src/build_train.py --kbd-aug 1 --out data/processed/mix_v2 > logs/build_mix_v2.log 2>&1
.venv/bin/python -u pipeline/src/train_encoder.py --mix data/processed/mix_v2 --model FacebookAI/xlm-roberta-base --name enc_xlmr_v2 --epochs 4 --lr 3e-5 --bs 32 --max-len 96 > logs/enc_xlmr_v2.log 2>&1
echo CHAIN_DONE >> logs/enc_xlmr_v2.log
