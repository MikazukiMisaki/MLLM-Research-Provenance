import datetime,hashlib,json,os,pathlib,subprocess,time
E=pathlib.Path(__file__).resolve().parent
method=pathlib.Path('/home/lizening/research-notes/agent-logs/2026-10-29T221000Z__SOL__si-u1-independent-statistics__c2356/independent_stats.py')
a=pathlib.Path('/home/lizening/research-notes/agent-logs/2026-10-29T113523Z__ASTRA__three-arm-prospective-design__a55d1af9/FINAL_PILOT82_PAIRED_ANALYSIS_C2356.json')
m=pathlib.Path('/home/lizening/research-notes/agent-logs/2026-10-29T144100Z__SOL__si-u1-stage2-plan__2060cc8/stage2/manifest.json')
s=pathlib.Path('/home/lizening/research-notes/agent-logs/2026-10-29T113523Z__ASTRA__three-arm-prospective-design__a55d1af9/PILOT82_PROPOSED_SCHEDULE_PRIVATE.json')
r=pathlib.Path('/home/lizening/research-notes/agent-logs/2026-10-29T224100Z__LUNA__si-u1-approved-extraction__062a/PROCESS_RECEIPT.json')
def sha(p):return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
for p,h in [(method,'e7ec762a7ae6d2643d5393634c5318a63d83bbf22d1330508b0511bcef4cab06'),(a,'4a3ea016d4c06022980482ac9dbc58155a68bbe20fbc723a68ce49c7c345ea9b'),(m,'7d1b61a9054f99a40fe895c7bb292a81e7a578bbd5fc6bf0777157676213e338'),(s,'c352a0d708b910bb3703c63009aed3a800b5ba4d40f95021f3bd30db0e4823cd'),(r,'b3121522e37551451b30bc5611dc744b0dc85f39604dbdf8c6ba65220961c7ee')]:assert p.is_file() and not p.is_symlink() and sha(p)==h,str(p)
receipt=json.loads(r.read_bytes());assert receipt['authentic_returncode']==0 and receipt['closed_success'] is True and receipt['analysis_sha256']==sha(a) and receipt['original_evidence_unchanged'] is True
out=E/'INDEPENDENT_COMPARISON.json';assert not out.exists()
cmd=['/home/lizening/miniconda3/envs/alfworld-self-improve/bin/python3.10',str(method),'--analysis',str(a),'--analysis-sha256',sha(a),'--manifest',str(m),'--schedule',str(s),'--output',str(out)]
env={'HOME':'/home/lizening','PATH':'/usr/bin:/bin','LC_ALL':'C.UTF-8','PYTHONDONTWRITEBYTECODE':'1'};start=datetime.datetime.now(datetime.timezone.utc).isoformat();t=time.monotonic()
with (E/'stdout').open('xb') as stdout,(E/'stderr').open('xb') as stderr:
 proc=subprocess.Popen(cmd,cwd=E,env=env,stdout=stdout,stderr=stderr);rc=proc.wait()
res={'argv':cmd,'env':env,'cwd':str(E),'pid':proc.pid,'returncode':rc,'start_utc':start,'end_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'elapsed_seconds':time.monotonic()-t,'input_before_after_unchanged':all(sha(p)==h for p,h in [(method,'e7ec762a7ae6d2643d5393634c5318a63d83bbf22d1330508b0511bcef4cab06'),(a,'4a3ea016d4c06022980482ac9dbc58155a68bbe20fbc723a68ce49c7c345ea9b'),(m,'7d1b61a9054f99a40fe895c7bb292a81e7a578bbd5fc6bf0777157676213e338'),(s,'c352a0d708b910bb3703c63009aed3a800b5ba4d40f95021f3bd30db0e4823cd')]),'output_sha256':sha(out) if out.exists() else None,'no_model_environment_or_evaluation_calls':True}
with (E/'PROCESS_RECEIPT.json').open('x') as f:json.dump(res,f,sort_keys=True,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
print(json.dumps({'returncode':rc,'output_sha256':res['output_sha256']}))
if rc:raise SystemExit(rc)
