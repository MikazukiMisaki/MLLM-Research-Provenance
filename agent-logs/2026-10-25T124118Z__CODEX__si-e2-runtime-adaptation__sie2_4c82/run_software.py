from pathlib import Path
import datetime,json,os,subprocess,sys,time
OWN=Path(__file__).resolve().parent
assert OWN.name == "2026-10-25T124118Z__CODEX__si-e2-runtime-adaptation__sie2_4c82"
label=sys.argv[1];argv=sys.argv[2:]
assert label and "/" not in label
out=OWN/"receipts"/label
assert not out.with_suffix(".json").exists()
env=dict(os.environ,PYTHONPATH="src:tests",PYTHONDONTWRITEBYTECODE="1",CUDA_VISIBLE_DEVICES="",HF_HUB_OFFLINE="1",TRANSFORMERS_OFFLINE="1",TOKENIZERS_PARALLELISM="false")
start=time.monotonic();utc=datetime.datetime.now(datetime.timezone.utc).isoformat()
with open(str(out)+".stdout","xb") as a,open(str(out)+".stderr","xb") as b:
 r=subprocess.run(argv,cwd="/home/lizening/wt-si-p3-runtime-adaptation",env=env,stdout=a,stderr=b)
receipt={"argv":argv,"cwd":"/home/lizening/wt-si-p3-runtime-adaptation","started_utc":utc,"elapsed_seconds":time.monotonic()-start,"returncode":r.returncode,"scope":"software only; no real model/environment calls"}
Path(str(out)+".json").write_text(json.dumps(receipt,indent=2)+"\n")
print(json.dumps(receipt));sys.exit(r.returncode)
