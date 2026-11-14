import subprocess, sys
M = "data/processed/mix_v6b"
E = {"e5x2": ["kg_e5L_v6b_s1", "kg_e5L_v6b_s2"], "e5x2_hz": ["kg_e5L_v6b_s1", "kg_e5L_v6b_s2", "kg_horizon_v6b"],
     "e5x2_hz_kz": ["kg_e5L_v6b_s1", "kg_e5L_v6b_s2", "kg_horizon_v6b", "kg_kazrob_v6b"]}
names = []
for meth in ["pct", "logit_z"]:
    for n, ms in E.items():
        out = f"runs/ens_v6b_{n}_{meth}"; names.append(out)
        subprocess.run([sys.executable, "pipeline/src/ensemble.py", f"--method={meth}", out, M] + [f"runs/{m}" for m in ms], check=True, capture_output=True)
subprocess.run([sys.executable, "pipeline/src/select_dev.py", M, "runs/kg_e5L_v6b_s1", "runs/kg_e5L_v6b_s2", "runs/kg_horizon_v6b"] + names)
