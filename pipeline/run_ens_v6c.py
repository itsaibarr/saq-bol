import subprocess, sys
M = "data/processed/mix_v6c"
E = {"e5x3": ["kg_e5L_v6c_s1", "kg_e5L_v6c_s2", "kg_e5L_v6c_s3"],
     "e5x3_hz": ["kg_e5L_v6c_s1", "kg_e5L_v6c_s2", "kg_e5L_v6c_s3", "kg_horizon_v6c"],
     "e5s2s3": ["kg_e5L_v6c_s2", "kg_e5L_v6c_s3"]}
names = []
for meth in ["pct", "logit_z"]:
    for n, ms in E.items():
        out = f"runs/ens_v6c_{n}_{meth}"; names.append(out)
        subprocess.run([sys.executable, "pipeline/src/ensemble.py", f"--method={meth}", out, M] + [f"runs/{m}" for m in ms], check=True, capture_output=True)
subprocess.run([sys.executable, "pipeline/src/select_dev.py", M, "runs/kg_e5L_v6c_s1", "runs/kg_e5L_v6c_s2", "runs/kg_e5L_v6c_s3", "runs/kg_horizon_v6c"] + names)
