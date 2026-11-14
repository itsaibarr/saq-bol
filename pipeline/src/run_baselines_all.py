"""Kaggle job: fetch the public datasets the baselines need, then score B5 (off-the-shelf) and B0-B3 on the mix's eval table
under the A4 operating point. usage: python run_baselines_all.py data/processed/mix"""
import subprocess, sys
mix = sys.argv[1] if len(sys.argv) > 1 else "data/processed/mix"
for cmd in [["pipeline/src/fetch_raw.py"], ["pipeline/src/baseline_offshelf.py", mix], ["pipeline/src/baselines.py", mix]]:
    print("+", cmd, flush=True)
    subprocess.run([sys.executable, "-u"] + cmd, check=True)
