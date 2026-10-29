"""SI-U1 offline result extractor. Never calls a model, CUDA, or environment.

The only live path executes the reviewed evaluator's own complete offline auditor.
Approval and specification are byte-bound before any output is opened. This tool
is a candidate for independent review, not an execution or analysis release.
"""
from __future__ import annotations
import argparse, hashlib, importlib.util, json, math, os, re, subprocess, sys
from pathlib import Path

SOURCE='8532275932dabddc498c23a2b6d9a045647542f0'
SCHEDULE='c352a0d708b910bb3703c63009aed3a800b5ba4d40f95021f3bd30db0e4823cd'
STATS='dc65a06fda495517bc76357022a90a0622d1b17c11ee101e19d958aebb5e3251'
TRAINING='f72e1de1b27659f0c0cb187c276c7c60483af089d4a756fbe3c3d7819dcc5698'
BASE='0239d34c87594c9d86c2fe5e81e515fa871809fa18b9ed67856fd0dc8e19c00b'
P0='6b13612c33d96ae9bbda041c08d33e0e1888406c4782670e90c8ebd27467b5a5'

class Rejected(ValueError): pass

def need(ok,message):
    if not ok: raise Rejected(message)

def sha(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for b in iter(lambda:f.read(1048576),b''):h.update(b)
    return h.hexdigest()

def strict(raw):
    def pairs(items):
        d={}
        for k,v in items:
            if k in d:raise Rejected('duplicate JSON key')
            d[k]=v
        return d
    def constant(_):raise Rejected('non-finite JSON number')
    return json.loads(raw,object_pairs_hook=pairs,parse_constant=constant)

def binding(x):
    need(type(x) is dict and set(x)=={'path','sha256'} and type(x['path']) is str and type(x['sha256']) is str and re.fullmatch('[0-9a-f]{64}',x['sha256']) is not None,'file binding')
    p=Path(x['path']);need(p.is_absolute() and p.is_file() and not p.is_symlink() and sha(p)==x['sha256'],'bound byte mismatch')
    return p

def tokenizer_binding(x, base, production_file_binding):
    """Validate snapshot-child tokenizer bytes using the frozen runtime contract."""
    need(type(x) is dict and set(x)=={'path','sha256'} and type(x['path']) is str and type(x['sha256']) is str and re.fullmatch('[0-9a-f]{64}',x['sha256']) is not None,'tokenizer file binding')
    p=Path(x['path']);need(base.is_absolute() and p.is_absolute() and p.parent==base,'tokenizer snapshot path')
    return production_file_binding(x)

def exact_keys(obj,keys,label):
    need(type(obj) is dict and set(obj)==set(keys),label+' unknown or missing fields')

def check_approval(spec_path,spec_sha,approval_path,approval_sha):
    s=strict(binding({'path':str(spec_path),'sha256':spec_sha}).read_bytes())
    a=strict(binding({'path':str(approval_path),'sha256':approval_sha}).read_bytes())
    exact_keys(s,['schema','source_sha','evaluator_root','run_output','analysis_output','manifest','runtime_spec','plan','protocol','schedule','analysis','authorization','clearance','stats'],'spec')
    exact_keys(a,['schema','decision','spec_sha256','extractor_sha256','source_sha','stats_sha256','reviewer'],'approval')
    need(s['schema']=='SI_U1_EXTRACTION_SPEC_V1' and s['source_sha']==SOURCE and a['schema']=='SI_U1_EXTRACTION_APPROVAL_V1' and a['decision']=='APPROVED_FOR_POSTRUN_AUDIT_AND_EXTRACTION' and a['spec_sha256']==spec_sha and a['extractor_sha256']==sha(Path(__file__).resolve()) and a['source_sha']==SOURCE and a['stats_sha256']==STATS and type(a['reviewer']) is str and bool(a['reviewer']),'independent pre-outcome approval')
    need(s['schedule']['sha256']==SCHEDULE and s['stats']['sha256']==STATS,'fixed schedule/statistics')
    return s

def verify_source(root):
    root=Path(root);need(root.is_absolute() and root.is_dir() and not root.is_symlink(),'source directory')
    get=lambda *a:subprocess.check_output(['git',*a],cwd=root,text=True).strip()
    need(get('rev-parse','--show-toplevel')==str(root) and get('rev-parse','HEAD')==SOURCE and not get('status','--porcelain','--untracked-files=normal'),'source identity or dirty worktree')
    return root

def source_import(root):
    root=verify_source(root)
    sys.path.insert(0,str(root/'src'))
    import self_improvement.si_transfer_eval.audit as auditmod
    import self_improvement.si_transfer_eval.protocol as protocolmod
    import self_improvement.si_transfer_eval.isolation as isolationmod
    import self_improvement.si_transfer_eval.live_audit as livemod
    import self_improvement.si_transfer_eval.runtime_identity as identitymod
    import self_improvement.si_transfer_eval.runtime_binding as runtimemod
    for m in (auditmod,protocolmod,isolationmod,livemod,identitymod,runtimemod):need(Path(m.__file__).resolve().is_relative_to(root/'src'),'production module origin')
    return auditmod,protocolmod,isolationmod,livemod,identitymod,runtimemod

def check_schedule_rows(manifest,schedule,report):
    tasks=manifest['tasks'];rows=report.get('episodes')
    need(type(tasks) is list and len(tasks)==82 and type(rows) is list and len(rows)==246,'full paired data required')
    need(len({t['task_id'] for t in tasks})==82 and len({t['task_id'].split('/')[0] for t in tasks})==82,'duplicate task/parent')
    need(report.get('schema')=='SI_TRANSFER_EVAL_REPORT_V1' and report.get('evidence_class')=='live' and report.get('status')=='COMPLETE' and report.get('pending_na')==[] and report.get('stop') is None,'live complete report')
    exact_keys(report,['schema','evidence_class','manifest_sha256','status','episodes','pending_na','stop','reserved_or_spent','completed','arm_reserved_or_spent','arm_completed'],'report')
    need(type(schedule) is dict and len(schedule.get('rows',[]))==82,'schedule')
    result={t['task_id']:{'task_id':t['task_id'],'family':t['family']} for t in tasks}
    for i,(task,sched) in enumerate(zip(tasks,schedule['rows'])):
        need(sched['schedule_index']==i and sched['environment_seed']==2000000+i and sched['parent']==task['task_id'].split('/')[0] and (task['task_id'],task['family'],task['seed'])==(sched['task_id'],sched['family'],sched['environment_seed']),'manifest schedule/parent mismatch')
    for row,(arm,t) in zip(rows,[(arm,t) for arm in ('A','B','C') for t in tasks]):
        exact_keys(row,['arm','task_id','family','seed','outcome','termination','steps','end_state'],'episode')
        need((row['arm'],row['task_id'],row['family'],row['seed'])==(arm,t['task_id'],t['family'],t['seed']) and type(row['outcome']) is int and row['outcome'] in (0,1) and row['termination'] in ('terminal','selection_failure','horizon') and type(row['steps']) is int and 0<=row['steps']<=50 and type(row['end_state']) is dict,'episode identity, order or unknown outcome')
        result[t['task_id']][arm]=bool(row['outcome'])
    return [result[t['task_id']] for t in tasks]

def scan_journal(p):
    first=last=None
    with p.open('rb') as f:
        for line in f:
            need(line.endswith(b'\n'),'truncated journal')
            row=strict(line)
            if first is None:first=row
            last=row
    need(type(first) is dict and type(last) is dict and first.get('kind')=='run_opened' and last.get('kind')=='run_closed','journal boundaries')
    return first,last

def check_physical_cost(launch, receipt, journal_path, manifest, protocol):
    """Reconstruct single-device physical time using frozen caps and durable arm events."""
    need(manifest['limits']['elapsed_seconds']==protocol['limits']['elapsed_seconds']==43200 and manifest['arm_limits']['elapsed_seconds']==protocol['arm_limits']['elapsed_seconds']==14400,'frozen time caps')
    need(type(launch.get('allocated_devices')) is int and launch['allocated_devices']==1 and type(receipt.get('allocated_devices')) is int and receipt['allocated_devices']==1,'device count')
    need(type(launch.get('max_allocation_seconds')) is int and launch['max_allocation_seconds']==43200 and type(launch.get('deadline_seconds')) is int and launch['deadline_seconds']==43200 and type(launch.get('per_arm_allocation_seconds')) is int and launch['per_arm_allocation_seconds']==14400,'supervisor allocation caps')
    def finite(v):return type(v) in (int,float) and math.isfinite(v)
    start=launch.get('allocation_started_monotonic');elapsed=receipt.get('elapsed_seconds');hours=receipt.get('allocated_device_hours')
    need(all(finite(v) and v>=0 for v in (start,elapsed,hours)) and elapsed<=43200 and math.isclose(hours,elapsed/3600,rel_tol=1e-12,abs_tol=1e-12),'supervisor physical device time')
    need(receipt.get('scope')=='three_arm_transfer_evaluation' and receipt.get('spawn_or_supervisor_error') is None and receipt.get('reaping_error') is None and receipt.get('arm_deadline_triggered') is None and receipt.get('members_after_cleanup')==[] and receipt.get('subreaper_restored') is True and receipt.get('restore_error') is None and receipt.get('artifact_snapshot_error') is None and receipt.get('final_arm_cleanup_within_cap') is True,'supervisor cleanup and error state')
    events=[]
    with Path(journal_path).open('rb') as f:
        for line in f:
            need(line.endswith(b'\n'),'truncated journal')
            row=strict(line)
            if row.get('kind') in ('arm_started','arm_finished'):events.append(row)
    need(len(events)==6,'three complete arm timings')
    previous=start; result={}
    for i,arm in enumerate(('A','B','C')):
        opened,closed=events[2*i:2*i+2];op=opened['payload'];cl=closed['payload']
        need(opened['kind']=='arm_started' and closed['kind']=='arm_finished' and op.get('arm')==cl.get('arm')==arm,'arm timing order')
        st=op.get('started_monotonic');end=cl.get('ended_monotonic');ot=opened.get('monotonic');ct=closed.get('monotonic')
        need(all(finite(v) for v in (st,end,ot,ct)) and previous<=st<=ot<=end<=ct<=start+elapsed and end-previous<=14400,'actual arm physical time')
        result[arm]={'allocation_start_monotonic':previous,'arm_started_monotonic':st,'arm_finished_monotonic':end,'accounted_seconds':end-previous}
        previous=end
    need(start+elapsed-result['C']['allocation_start_monotonic']<=14400,'final arm cleanup time')
    return {'allocated_devices':1,'elapsed_seconds':elapsed,'allocated_device_hours':hours,'arm_timing':result,'final_arm_including_cleanup_seconds':start+elapsed-result['C']['allocation_start_monotonic']}

def execute(spec,approval_sha):
    need(sys.flags.isolated==1 and not any(k in os.environ for k in ('PYTHONPATH','PYTHONHOME','LD_PRELOAD')) and os.environ.get('HF_HUB_OFFLINE')=='1' and os.environ.get('TRANSFORMERS_OFFLINE')=='1','isolated offline execution required')
    auditmod,protocolmod,isolationmod,livemod,identitymod,runtimemod=source_import(spec['evaluator_root'])
    paths={key:binding(spec[key]) for key in ('manifest','runtime_spec','plan','protocol','schedule','analysis','authorization','clearance','stats')}
    manifest=strict(paths['manifest'].read_bytes());runtime=strict(paths['runtime_spec'].read_bytes());protocol=strict(paths['protocol'].read_bytes());schedule=strict(paths['schedule'].read_bytes());auth=strict(paths['authorization'].read_bytes());clear=strict(paths['clearance'].read_bytes())
    need(auth.get('schema')=='SI_TRANSFER_EVAL_AUTHORIZATION_V1' and auth.get('purpose')=='PREFLIGHT_ONLY' and auth.get('source_sha')==SOURCE and all(auth.get(k)==spec[k] for k in ('manifest','runtime_spec','plan','protocol','schedule','analysis')),'authorization artifact mismatch')
    need(clear.get('schema')=='SI_U1_EVAL_CLEARANCE_V1' and clear.get('decision')=='RELEASE_ONE_THREE_ARM_EVALUATION' and clear.get('source_sha')==SOURCE and clear.get('authorization_sha256')==spec['authorization']['sha256'] and clear.get('maximum_launches')==1 and clear.get('retry_authorized') is False and all(clear.get(k+'_sha256')==spec[k]['sha256'] for k in ('manifest','runtime_spec','plan','protocol')) and clear.get('review_sha256')==auth['review']['sha256'],'clearance bindings')
    sw_review=strict(binding(auth['review']).read_bytes())
    need(sw_review=={'schema':'SI_TRANSFER_EVAL_REVIEW_V1','decision':'PASS_SOFTWARE_ONLY','source_sha':SOURCE,'manifest_sha256':spec['manifest']['sha256'],'runtime_spec_sha256':spec['runtime_spec']['sha256'],'protocol_sha256':spec['protocol']['sha256'],'plan_sha256':spec['plan']['sha256']},'exact software review')
    preflight=binding({'path':auth['receipt_path'],'sha256':clear['preflight_receipt_sha256']});pr=strict(preflight.read_bytes());pf=binding(clear['preflight_execution']);pe=strict(pf.read_bytes())
    need(pr.get('schema')=='SI_TRANSFER_EVAL_PREFLIGHT_V1' and pr.get('status')=='PREFLIGHT_ONLY_PASS_NOT_LAUNCH_AUTHORITY' and pr.get('authorization_sha256')==spec['authorization']['sha256'] and pr.get('source_sha')==SOURCE and all(pr.get(k+'_sha256')==spec[k]['sha256'] for k in ('manifest','runtime_spec','plan','protocol','schedule','analysis')),'actual preflight receipt')
    expected=[spec['authorization']['sha256'] if x=='@AUTHORIZATION_SHA256@' else x for x in auth['preflight_argv']]
    need(pe.get('schema')=='SI_U1_PREFLIGHT_EXECUTION_V1' and pe.get('authentic_returncode')==0 and pe.get('authorization_sha256')==spec['authorization']['sha256'] and pe.get('preflight_receipt_sha256')==clear['preflight_receipt_sha256'] and pe.get('argv')==expected and pe.get('source_sha')==SOURCE and pe.get('cwd')==spec['evaluator_root'] and type(pe.get('child_pid')) is int and pe['child_pid']>0 and type(pe.get('child_start_tick')) is int and pe['child_start_tick']>0 and pe.get('timed_out') is False and pe.get('supervisor_error') is None and sha(pf.parent/'stdout')==pe.get('stdout_sha256') and sha(pf.parent/'stderr')==pe.get('stderr_sha256'),'actual preflight subprocess')
    output=Path(spec['run_output']);analysis_output=Path(spec['analysis_output']);need(output.is_absolute() and str(output)==auth['output_path'] and output.is_dir() and not output.is_symlink() and analysis_output.is_absolute() and not analysis_output.exists() and not analysis_output.is_symlink() and not analysis_output.is_relative_to(output) and analysis_output.parent.is_dir(),'run/output paths')
    context=livemod.authenticate_run(output);launch=strict((output/'launch_context.json').read_bytes())
    template=[auth['interpreter'],'-I',str(Path(spec['evaluator_root'])/'scripts/run_si_transfer_eval.py'),'--live','--authorization',spec['authorization']['path'],'--authorization-sha256','@AUTHORIZATION_SHA256@','--clearance',spec['clearance']['path'],'--clearance-sha256','@CLEARANCE_SHA256@']
    expected_live=[spec['authorization']['sha256'] if x=='@AUTHORIZATION_SHA256@' else spec['clearance']['sha256'] if x=='@CLEARANCE_SHA256@' else x for x in template]
    need(clear.get('live_argv')==template and launch.get('supervisor_argv')==expected_live,'actual live command')
    b=context['binding'];need(b['source_sha']==SOURCE and b['authorization_sha256']==spec['authorization']['sha256'] and b['clearance_sha256']==spec['clearance']['sha256'] and b['manifest_sha256']==spec['manifest']['sha256'] and b['runtime_spec_sha256']==spec['runtime_spec']['sha256'] and b['protocol_sha256']==spec['protocol']['sha256'] and b['run_id']==clear['run_id'],'actual supervisor context mismatch')
    need(runtime.get('training_protocol_sha256')==TRAINING and runtime.get('base_sha256')==BASE and runtime.get('adapters',{}).get('A',{}).get('sha256')==P0,'P0/base/training provenance')
    train=strict(binding(runtime['training_protocol']).read_bytes());need(runtime['training_protocol']['sha256']==TRAINING,'frozen training bytes')
    identitymod.verify_static(train['runtime_identity'],train['runtime_identity']['interpreter']['path'],train['epoch_shuffle_rule'])
    isolation=runtime['isolation_proof']['sha256'];protocolmod.validate_frozen_protocol(protocol,paths['plan'].read_bytes(),paths['manifest'].read_bytes(),paths['schedule'].read_bytes(),isolation_review_sha256=isolation,analysis_sha256=spec['analysis']['sha256']);isolationmod.validate_isolation_spec(runtime,manifest_sha256=spec['manifest']['sha256'],schedule_sha256=SCHEDULE)
    need(protocol.get('manifest_sha256')==spec['manifest']['sha256'] and runtime.get('manifest_sha256')==spec['manifest']['sha256'],'manifest exact canonical bytes')
    need(runtimemod.verify_static_runtime(runtime,manifest)['status']=='STATIC_BYTES_VERIFIED_NOT_A_LAUNCH_CLEARANCE','static training and input lineage')
    base=Path(runtime['base_path']);token_files=[f for f in runtime['base_files'] if Path(f['path']).name in ('tokenizer.json','tokenizer_config.json','vocab.json','merges.txt','special_tokens_map.json','added_tokens.json')];need(any(Path(f['path']).name=='tokenizer.json' for f in token_files),'tokenizer bytes absent')
    for f in token_files:tokenizer_binding(f,base,runtimemod.file_binding)
    from transformers import AutoTokenizer
    tokenizer=AutoTokenizer.from_pretrained(str(base),local_files_only=True,trust_remote_code=False)
    eos=(tokenizer.eos_token_id,) if type(tokenizer.eos_token_id) is int else tuple(tokenizer.eos_token_id or ());need(bool(eos) and all(type(x) is int for x in eos),'tokenizer EOS')
    events=output/'evaluation'/'events.jsonl';report_path=output/'evaluation'/'report.json';need(events.is_file() and report_path.is_file() and not events.is_symlink() and not report_path.is_symlink(),'missing evidence')
    before={str(p):sha(p) for p in (events,report_path,output/'supervisor_exit.json',output/'launch_context.json',output/'worker_start.json')}
    first,last=scan_journal(events);report=strict(report_path.read_bytes());need(last['payload']==report and first['payload']['manifest']==manifest and report['manifest_sha256']==spec['manifest']['sha256'],'report/journal/manifest mismatch')
    supervisor_receipt=strict((output/'supervisor_exit.json').read_bytes())
    physical_cost=check_physical_cost(launch,supervisor_receipt,events,manifest,protocol)
    result=auditmod.audit(events,decode=lambda arm,ids:tokenizer.decode(ids,skip_special_tokens=True).strip(),eos_ids=eos,live_output=output)
    need(result.get('status')=='AUDIT_PASS_LIVE' and result.get('report_status')=='COMPLETE' and result.get('episode_count')==246 and result.get('pending_na_count')==0,'production auditor did not fully pass')
    pairs=check_schedule_rows(manifest,schedule,report)
    loader=importlib.util.spec_from_file_location('frozen_paired_stats',paths['stats']);module=importlib.util.module_from_spec(loader);loader.loader.exec_module(module)
    stats=module.analyze(pairs,expected_tasks={t['task_id']:t['family'] for t in manifest['tasks']})
    for f in token_files:tokenizer_binding(f,base,runtimemod.file_binding)
    for key in ('manifest','runtime_spec','plan','protocol','schedule','analysis','authorization','clearance','stats'):binding(spec[key])
    binding(auth['review']);binding(clear['preflight_execution']);binding({'path':auth['receipt_path'],'sha256':clear['preflight_receipt_sha256']})
    need(sha(pf.parent/'stdout')==pe['stdout_sha256'] and sha(pf.parent/'stderr')==pe['stderr_sha256'],'preflight log drift')
    need(runtimemod.verify_static_runtime(runtime,manifest)['status']=='STATIC_BYTES_VERIFIED_NOT_A_LAUNCH_CLEARANCE','runtime inputs changed during audit')
    identitymod.verify_static(train['runtime_identity'],train['runtime_identity']['interpreter']['path'],train['epoch_shuffle_rule'])
    need(before=={str(p):sha(p) for p in (events,report_path,output/'supervisor_exit.json',output/'launch_context.json',output/'worker_start.json')} and livemod.authenticate_run(output)==context,'evidence drift during audit')
    verify_source(spec['evaluator_root'])
    return {'schema':'SI_U1_PAIRED_ANALYSIS_V1','source_sha':SOURCE,'analysis_approval_sha256':approval_sha,'manifest_sha256':spec['manifest']['sha256'],'run_id':b['run_id'],'evidence_hashes':before,'production_audit':result,'physical_cost':physical_cost,'paired_records':pairs,'overall_successes':{arm:sum(int(row[arm]) for row in pairs) for arm in ('A','B','C')},'statistics':stats,'interpretation':'Finite fixed schedule descriptive; registry completeness and unseen layouts unproven; N82 underpowered for 5pp; population inference requires assumptions.'}

def main():
    p=argparse.ArgumentParser();p.add_argument('--spec',required=True);p.add_argument('--spec-sha256',required=True);p.add_argument('--approval',required=True);p.add_argument('--approval-sha256',required=True);a=p.parse_args()
    s=check_approval(a.spec,a.spec_sha256,a.approval,a.approval_sha256);result=execute(s,a.approval_sha256)
    need(check_approval(a.spec,a.spec_sha256,a.approval,a.approval_sha256)==s,'approval or spec changed during audit')
    out=Path(s['analysis_output']);flags=os.O_WRONLY|os.O_CREAT|os.O_EXCL
    with os.fdopen(os.open(out,flags,0o600),'w') as f:json.dump(result,f,sort_keys=True,separators=(',',':'),allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
    print('OFFLINE_ANALYSIS_COMPLETE',sha(out))
if __name__=='__main__':main()
