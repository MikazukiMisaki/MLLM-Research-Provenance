"""Post-exit only: inspect accounting and archive B evidence, never rerun training."""
import collections,gzip,hashlib,json,math,tarfile
from pathlib import Path
here=Path(__file__).resolve().parent;out=Path('/home/lizening/research-notes/agent-logs/2026-10-29T125500Z__SOL__si-pilot82-bc-authorization-drafts__9bbaa/run_parent/B_run_064d0c7f39f14414acf24f399188f85f');pre=Path('/home/lizening/research-notes/agent-logs/2026-10-29T134700Z__LUNA__si-pilot82-b-preflight__9bbaa');auth=Path('/home/lizening/wt-si-self-imitation-train/configs/local/si_pilot82_b_authorization_064d0c7f39f14414acf24f399188f85f.json');clear=Path('/home/lizening/research-notes/agent-logs/2026-10-29T134800Z__CODEX__si-pilot82-b-release__9bbaa/B_TRAINING_CLEARANCE_ONE_SHOT.json')
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for x in iter(lambda:f.read(1048576),b''):h.update(x)
 return h.hexdigest()
def tree(p):
 rows=[]
 for x in sorted(p.rglob('*')):
  if x.is_symlink() and not x.is_file():raise ValueError('bad symlink')
  if x.is_file():rows.append([x.relative_to(p).as_posix(),x.stat().st_size,sha(x)])
  elif not x.is_dir():raise ValueError('unexpected tree entry')
 return {'sha256':hashlib.sha256(json.dumps(rows,ensure_ascii=False,separators=(',',':')).encode()).hexdigest(),'file_count':len(rows),'total_bytes':sum(x[1] for x in rows),'files':rows}
assert (here/'LAUNCHER_EXIT.json').exists() and (out/'supervisor_exit.json').exists(), 'must wait for actual exit'
A=json.loads(auth.read_text());S=json.loads((out/'supervisor_exit.json').read_text());L=json.loads((here/'LAUNCHER_EXIT.json').read_text());resultpath=out/'training/training_result.json';J=out/'training/training_events.jsonl';resourcepath=out/'resource.jsonl';result=json.loads(resultpath.read_text()) if resultpath.is_file() else {};events=[json.loads(s) for s in J.read_text().splitlines()] if J.is_file() else [];resources=[json.loads(s) for s in resourcepath.read_text().splitlines()] if resourcepath.is_file() else [];manifest=json.loads(Path(A['manifest']['path']).read_text());protocol=json.loads(Path(A['protocol']['path']).read_text())
checks={}
checks['supervisor_exit0_and_cleanup']=S.get('authentic_returncode')==L.get('authentic_returncode')==0 and S.get('status')=='EXIT_RECORDED' and S.get('cleanup_established') is True and S.get('within_time_cap') is True
checks['real_result_hash']=resultpath.is_file() and S.get('training_result_sha256')==sha(resultpath)
checks['no_automatic_retry']=S.get('retry_authorized') is False and L.get('retry_authorized') is False
checks['source_and_arm']=result.get('arm')=='B' and S.get('binding',{}).get('source_sha')==A['source_sha'] and result.get('manifest_sha256')==A['manifest']['sha256']
checks['all_78_optimizer_steps']=result.get('counts',{}).get('optimizer_steps')==78 and [e.get('optimizer_step') for e in events if e.get('kind')=='optimizer_step_completed']==list(range(78))
starts=[e for e in events if e.get('kind')=='microbatch_started'];dones=[e for e in events if e.get('kind')=='microbatch_completed'];ids=[item for e in starts for item in e.get('sample_ids',[])];checks['frozen_1248_sample_order']=ids==manifest['ordered_sample_ids'] and len(dones)==len(starts)==1248
counts=result.get('counts',{});checks['exact_exposure_counts']=counts.get('input_tokens')==661620 and counts.get('supervised_tokens')==6240 and counts.get('microbatches_started')==counts.get('microbatches_completed')==1248 and sum(e.get('input_tokens',0) for e in starts)==661620 and sum(e.get('supervised_tokens',0) for e in starts)==6240
checks['finite_losses']=len(dones)==1248 and all(type(e.get('loss')) in (int,float) and math.isfinite(e['loss']) for e in dones)
rates=[e.get('learning_rate') for e in events if e.get('kind')=='optimizer_step_started'];planned=protocol['learning_rate_definition']['values_by_one_based_step'];checks['frozen_learning_rates']=len(rates)==len(planned)==78 and all(type(a) in (int,float) and math.isclose(a,b,rel_tol=1e-14,abs_tol=1e-16) for a,b in zip(rates,planned))
checks['resource_pass_no_oom']=bool(resources) and all(x.get('status')=='PASS' and x.get('allocator_ooms')==0 for x in resources);checks['resource_no_retry_observed']=bool(resources) and all(x.get('allocator_retries')==0 for x in resources)
adapter=out/'training/final_adapter';adapter_tree=tree(adapter) if adapter.is_dir() else None;checks['adapter_hash_matches']=adapter_tree is not None and adapter_tree['sha256']==result.get('final_adapter_sha256');base=tree(Path(A['base']['path']));p0=tree(Path(A['adapter']['path']));checks['frozen_base_p0_unchanged']=base['sha256']==A['base']['sha256'] and p0['sha256']==A['adapter']['sha256'];checks['declared_completed']=result.get('status')=='COMPLETED'
files=[(p,'run/'+p.relative_to(out).as_posix()) for p in sorted(out.rglob('*')) if p.is_file() and not p.is_relative_to(adapter)];files.append((out.with_name(out.name+'.claim.json'),'run_claim.json'))
for n in ['launch_b_once.py','ONE_SHOT_B_DISPATCH.json','LAUNCHER_START.json','LAUNCHER_EXIT.json','launcher.stdout','launcher.stderr','gpu_samples.jsonl']:files.append((here/n,'launcher/'+n))
for n in ['RECORD.md','STATIC_CHECKS.json','DISPATCH_ONCE.json','PREFLIGHT_PROCESS_RECEIPT.json','child.stdout','child.stderr','FILE_HASHES.sha256']:files.append((pre/n,'preflight/'+n))
files += [(Path(A['preflight_path']),'preflight_receipt.json'),(auth,'authorization.json'),(clear,'clearance.json')]
before={n:{'sha256':sha(p),'bytes':p.stat().st_size} for p,n in files}
with (here/'B_RAW_EVIDENCE_PRIVATE.tar.gz').open('xb') as dest:
 with gzip.GzipFile(fileobj=dest,mode='wb',filename='',mtime=0) as gz:
  with tarfile.open(fileobj=gz,mode='w') as tar:
   for p,n in files:
    info=tar.gettarinfo(str(p),arcname=n);info.uid=info.gid=0;info.uname=info.gname='';info.mtime=0
    with p.open('rb') as f:tar.addfile(info,f)
assert before=={n:{'sha256':sha(p),'bytes':p.stat().st_size} for p,n in files}
with tarfile.open(here/'B_RAW_EVIDENCE_PRIVATE.tar.gz','r:gz') as tar:
 for m in tar:
  b=tar.extractfile(m).read();assert len(b)==before[m.name]['bytes'] and hashlib.sha256(b).hexdigest()==before[m.name]['sha256']
summary={'schema':'SI_U1_LUNA_B_RUN_AUDIT_V1','status':'OBSERVED_COMPLETED_AWAIT_INDEPENDENT_REVIEW' if all(checks.values()) else 'STOP_OR_INCONCLUSIVE','checks':checks,'source_sha':A['source_sha'],'run_id':A['run_id'],'arm':'B','supervisor_exit':S,'launcher_exit':L,'counts':counts,'resource_rows':len(resources),'resource_peak_allocated_bytes':max((r.get('allocated_peak_bytes',0) for r in resources),default=0),'resource_peak_reserved_bytes':max((r.get('reserved_peak_bytes',0) for r in resources),default=0),'base_tree':base,'p0_tree':p0,'b_final_adapter_tree':adapter_tree,'adapter_weights_excluded_from_archive':True,'adapter_remains_at_original_run_output':True,'raw_event_ledger_contains_private_metadata':True,'raw_archive_sha256':sha(here/'B_RAW_EVIDENCE_PRIVATE.tar.gz'),'archive_members':before,'archive_members_byte_verified':True,'c_preflight_or_training_started_by_this_task':False,'retry_authorized':False}
with (here/'B_RUN_AUDIT.json').open('x') as f:json.dump(summary,f,indent=2,sort_keys=True);f.write('\n')
print(json.dumps({'status':summary['status'],'checks':checks,'audit_sha256':sha(here/'B_RUN_AUDIT.json'),'archive_sha256':summary['raw_archive_sha256'],'archive_members':len(files),'adapter_sha256':adapter_tree['sha256'] if adapter_tree else None,'elapsed_seconds':S.get('elapsed_seconds')}))
