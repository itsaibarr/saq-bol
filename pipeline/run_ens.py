import subprocess, sys
M = "data/processed/mix_v5b"
ENS = {"ens_e5_hz": ["kg_e5L_v5b", "kg_horizon_v5b_s2"],
       "ens_e5_hz_b5": ["kg_e5L_v5b", "kg_horizon_v5b_s2", "B5_offshelf_scam_model"],
       "ens_e5_hz_b3": ["kg_e5L_v5b", "kg_horizon_v5b_s2", "B3_tfidf_our_mix"],
       "ens_all4": ["kg_e5L_v5b", "kg_horizon_v5b_s2", "B5_offshelf_scam_model", "B3_tfidf_our_mix"]}
for n, ms in ENS.items():
    subprocess.run([sys.executable, "pipeline/src/ensemble.py", f"runs/{n}", M] + [f"runs/{m}" for m in ms], check=True, capture_output=True)
subprocess.run([sys.executable, "pipeline/src/select_dev.py", M] + [f"runs/{n}" for n in ENS])
