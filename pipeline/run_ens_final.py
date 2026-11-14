import subprocess, sys, glob
M = "data/processed/mix_v6c"
E2 = ["kg_e5L_v6c_s1", "kg_e5L_v6c_s2", "kg_e5L_v6c_s3"]; E3 = ["kg_e5L_v6c_e3_s4", "kg_e5L_v6c_e3_s5", "kg_e5L_v6c_e3_s6"]
E = {"e5ep3x3": E3, "e5all6": E2 + E3, "e5all6_hz": E2 + E3 + ["kg_horizon_v6c"]}
for meth in ["pct", "logit_z"]:
    for n, ms in E.items():
        subprocess.run([sys.executable, "pipeline/src/ensemble.py", f"--method={meth}", f"runs/ens_v6c_{n}_{meth}", M] + [f"runs/{m}" for m in ms], check=True, capture_output=True)
cands = sorted(glob.glob("runs/kg_*v6c*")) + sorted(glob.glob("runs/ens_v6c_*"))
subprocess.run([sys.executable, "pipeline/src/rank_candidates.py", M] + cands)
