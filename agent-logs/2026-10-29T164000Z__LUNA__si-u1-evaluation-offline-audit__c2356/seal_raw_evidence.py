"""Archive actual completed run unchanged. Private: contains task text/outcomes."""
import gzip,hashlib,json,re,tarfile
from pathlib import Path
here=Path(__file__).resolve().parent;run=Path('/home/lizening/research-notes/agent-logs/2026-10-29T145200Z__LUNA__si-u1-production-preflight-proposal__853/run_parent/evaluation_c2356bbda2b44159a333e7c9d24fc2d4');launcher=Path('/home/lizening/research-notes/agent-logs/2026-10-29T150000Z__LUNA__si-u1-three-arm-evaluation__853');astra=Path('/home/lizening/research-notes/agent-logs/2026-10-29T113523Z__ASTRA__three-arm-prospective-design__a55d1af9');release=Path('/home/lizening/research-notes/agent-logs/2026-10-29T150100Z__CODEX__si-u1-eval-live-release__853')
assert (run/'supervisor_exit.json').is_file() and (launcher/'OUTER_EXIT_V4.json').is_file()
sources=[(p,'run/'+p.relative_to(run).as_posix()) for p in sorted(run.rglob('*')) if p.is_file()]
sources.append((run.with_name(run.name+'.launch_claim.json'),'run_claim.json'))
for n in ['DETACHED_LAUNCH_CLAIM.json','DETACHED_WRAPPER_START.json','LIVE_DISPATCH_ONCE_V4.json','SUPERVISOR_START_V4.json','OUTER_EXIT_V4.json','detached_wrapper.stdout','detached_wrapper.stderr','supervisor_v4.stdout','supervisor_v4.stderr','online_monitor_samples.jsonl','launch_three_arm_v4.py','detached_dispatch_v4.py','process_control_v4.py','monitor_readonly_v4.py']:
 p=launcher/n
 if p.exists():sources.append((p,'launcher/'+n))
sources += [(astra/'EXTRACTION_SPEC_C2356_CANDIDATE_V1.json','approval/extraction_spec.json'),(release/'EXTRACTION_APPROVAL_C2356.json','approval/extraction_approval.json'),(release/'LIVE_CLEARANCE_ONE_SHOT.json','approval/clearance.json')]
assert all(not p.name.endswith(('.safetensors','.bin','.pt','.pth','.ckpt','.gguf')) for p,_ in sources)
patterns={'private_key_header':re.compile(rb'-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----'),'github_token':re.compile(rb'\b(?:gh[pousr]_[A-Za-z0-9_]{20,}|github_pat_[A-Za-z0-9_]{20,})\b'),'hf_token':re.compile(rb'\bhf_[A-Za-z0-9]{25,}\b'),'aws_access_key':re.compile(rb'\bAKIA[0-9A-Z]{16}\b')}
def info(p):
 h=hashlib.sha256();counts=collections.Counter();tail=b''
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):
   h.update(b);scanned=tail+b
   for k,v in patterns.items():counts[k]+=len(v.findall(scanned))
   tail=scanned[-256:]
 return {'sha256':h.hexdigest(),'bytes':p.stat().st_size,'credential_matches':dict(counts)}
import collections
before={n:info(p) for p,n in sources};assert not any(sum(x['credential_matches'].values()) for x in before.values())
archive=here/'FULL_RAW_EVIDENCE_PRIVATE.tar.gz'
with archive.open('xb') as dest:
 with gzip.GzipFile(fileobj=dest,mode='wb',filename='',mtime=0) as gz:
  with tarfile.open(fileobj=gz,mode='w') as tar:
   for p,n in sources:
    t=tar.gettarinfo(str(p),arcname=n);t.uid=t.gid=0;t.uname=t.gname='';t.mtime=0
    with p.open('rb') as f:tar.addfile(t,f)
assert before=={n:info(p) for p,n in sources}
with tarfile.open(archive,'r:gz') as tar:
 members=list(tar);assert len(members)==len(sources)
 for m in members:
  h=hashlib.sha256();count=0
  with tar.extractfile(m) as f:
   for b in iter(lambda:f.read(1048576),b''):h.update(b);count+=len(b)
  assert count==before[m.name]['bytes'] and h.hexdigest()==before[m.name]['sha256']
data={'schema':'SI_U1_FULL_RAW_EVIDENCE_PRIVATE_V1','status':'SEALED_WAITING_INDEPENDENT_AUDIT','original_run_files_all_included':True,'archive_sha256':info(archive)['sha256'],'archive_bytes':archive.stat().st_size,'members':before,'source_files_unchanged_and_archive_members_rehashed':True,'contains_private_task_text_and_outcomes':True,'no_model_weights_or_input_dataset_files':True,'credential_scan_no_targeted_matches':True,'scientific_results_not_extracted':True}
path=here/'RAW_EVIDENCE_INVENTORY_PRIVATE.json'
with path.open('x') as f:json.dump(data,f,indent=2,sort_keys=True);f.write('\n')
print(json.dumps({'archive_sha256':data['archive_sha256'],'archive_bytes':data['archive_bytes'],'member_count':len(sources),'inventory_sha256':info(path)['sha256']}))
