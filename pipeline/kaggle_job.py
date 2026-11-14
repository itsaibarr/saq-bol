"""Package code + a data mix as a private Kaggle dataset, and run up to two jobs per kernel (one per T4).

usage:
  python pipeline/kaggle_job.py upload <mix_dir> [extra files...]        # create/version dataset itsaibarr/saqbol-data
  python pipeline/kaggle_job.py run <slug> '<job1 args>' ['<job2 args>']  # push kernel itsaibarr/<slug>
  python pipeline/kaggle_job.py fetch <slug> [--weights]                 # pull outputs into runs/
Job args are passed to a script under pipeline/src (first token = script name, e.g. "train_encoder.py --model ...").
"""
import json, os, shutil, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KGL = os.path.join(ROOT, "pipeline", "bin", "kgl")
OWNER, DS = "itsaibarr", "saqbol-data"
STAGE = os.path.join(ROOT, "pipeline", "kernels")


def sh(cmd):
    print("+", cmd); r = subprocess.run(cmd, shell=True, capture_output=True, text=True); print(r.stdout[-1500:], r.stderr[-1500:]); return r


def upload(mix, extra):
    d = os.path.join(STAGE, "_dataset"); shutil.rmtree(d, ignore_errors=True)
    os.makedirs(f"{d}/pipeline_src"); os.makedirs(f"{d}/mix")
    for f in os.listdir(f"{ROOT}/pipeline/src"):
        if f.endswith(".py"):
            shutil.copy(f"{ROOT}/pipeline/src/{f}", f"{d}/pipeline_src/{f}")
    for f in ["train.jsonl", "val.jsonl", "eval.jsonl", "stats.json"]:
        shutil.copy(f"{ROOT}/{mix}/{f}", f"{d}/mix/{f}")
    for f in extra:
        shutil.copy(f"{ROOT}/{f}", f"{d}/{os.path.basename(f)}")
    json.dump({"title": DS, "id": f"{OWNER}/{DS}", "licenses": [{"name": "other"}]}, open(f"{d}/dataset-metadata.json", "w"))
    exists = sh(f"{KGL} datasets status {OWNER}/{DS}").returncode == 0
    sh(f"{KGL} datasets version -p {d} -m 'update {mix}' -r zip" if exists else f"{KGL} datasets create -p {d} -r zip")


RUNNER = r'''
import glob, os, shutil, subprocess, sys, json, time
src = glob.glob("/kaggle/input/**/pipeline_src", recursive=True)[0]
base = os.path.dirname(src)
W = "/kaggle/working/proj"; os.makedirs(f"{W}/pipeline/src", exist_ok=True); os.makedirs(f"{W}/data/processed", exist_ok=True)
for f in os.listdir(src): shutil.copy(f"{src}/{f}", f"{W}/pipeline/src/{f}")
shutil.copytree(f"{base}/mix", f"{W}/data/processed/mix", dirs_exist_ok=True)
for f in os.listdir(base):
    if f.endswith(".jsonl"): shutil.copy(f"{base}/{f}", f"{W}/data/processed/{f}")
os.chdir(W)
print(subprocess.run("nvidia-smi -L", shell=True, capture_output=True, text=True).stdout, flush=True)
JOBS = __JOBS__
procs = []
for gpu, args in enumerate(JOBS):
    env = dict(os.environ, CUDA_VISIBLE_DEVICES=str(gpu), TOKENIZERS_PARALLELISM="false")
    log = open(f"/kaggle/working/job{gpu}.log", "w")
    procs.append(subprocess.Popen(f"python -u pipeline/src/{args}", shell=True, env=env, stdout=log, stderr=subprocess.STDOUT))
while any(p.poll() is None for p in procs):
    time.sleep(60)
    for gpu in range(len(JOBS)):
        print(f"--- job{gpu} tail:", open(f"/kaggle/working/job{gpu}.log").read()[-400:].replace("\n", " | "), flush=True)
print("exit codes", [p.returncode for p in procs])
if os.path.exists(f"{W}/runs"): shutil.copytree(f"{W}/runs", "/kaggle/working/runs", dirs_exist_ok=True)
for f in glob.glob(f"{W}/data/processed/*_out.jsonl"): shutil.copy(f, "/kaggle/working/")
'''


def run(slug, jobs):
    d = os.path.join(STAGE, slug); shutil.rmtree(d, ignore_errors=True); os.makedirs(d)
    jobs = [j.replace("data/processed/mix_v4", "data/processed/mix").replace("--mix data/processed/mix ", "--mix data/processed/mix ") for j in jobs]
    open(f"{d}/run.py", "w").write(RUNNER.replace("__JOBS__", json.dumps(jobs)))
    json.dump({"id": f"{OWNER}/{slug}", "title": slug, "code_file": "run.py", "language": "python", "kernel_type": "script",
               "is_private": True, "enable_gpu": True, "enable_internet": True, "dataset_sources": [f"{OWNER}/{DS}"],
               "competition_sources": [], "kernel_sources": [], "model_sources": []}, open(f"{d}/kernel-metadata.json", "w"))
    sh(f"{KGL} kernels push -p {d} --accelerator NvidiaTeslaT4 -t 7200")


def fetch(slug, weights):
    out = os.path.join(ROOT, "pipeline", "kernels", slug, "out"); os.makedirs(out, exist_ok=True)
    pat = "" if weights else " --file-pattern '.*\\.(json|jsonl|log|txt|csv)$'"
    sh(f"{KGL} kernels output {OWNER}/{slug} -p {out} -o -q{pat}")
    if os.path.exists(f"{out}/runs"):
        for r in os.listdir(f"{out}/runs"):
            shutil.copytree(f"{out}/runs/{r}", f"{ROOT}/runs/{r}", dirs_exist_ok=True); print("fetched run", r)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "upload":
        upload(sys.argv[2], sys.argv[3:])
    elif cmd == "run":
        run(sys.argv[2], sys.argv[3:])
    elif cmd == "fetch":
        fetch(sys.argv[2], "--weights" in sys.argv)
