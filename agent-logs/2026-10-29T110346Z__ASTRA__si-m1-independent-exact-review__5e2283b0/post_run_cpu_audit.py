from pathlib import Path
from datetime import datetime,timezone
import sys,os,json,hashlib,subprocess,collections,time
ROOT=Path('/home/lizening/wt-si-five-case-probe');DEST=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'src'))
assert os.environ.get('CUDA_VISIBLE_DEVICES')=='' and os.environ.get('HF_HUB_OFFLINE')=='1'
from self_improvement.si_m1.history import read_source
from self_improvement.si_m1.contract import LIVE,LIMITS,text_hash
from self_improvement.si_m1.gate import Permit
from self_improvement.si_m1.audit import audit
from self_improvement.si_m1.evidence import read_events
from self_improvement.si_p3.runtime_backend import LocalInference
from models.action_parser import action_id_mapping
from recovery.two_stage_v2 import parse_bare_stage_two_output
BASE=Path('/tmp/si_m1_uid-2000_run-394f9f90869dd8505844caa7ea1a7e9f_35jwli1v');OUT=BASE/'output';CONTROL=BASE/'control'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(p):return json.loads(Path(p).read_bytes())
files=[p for d in (OUT,CONTROL) for p in d.iterdir() if p.is_file()];before={str(p):sha(p) for p in files}
ap=ROOT/'configs/local/si_m1_authorization_e37046d42289de2898d82bddd04b5f14.json';pp=ROOT/'configs/local/si_m1_single_step_proposal_draft.json';a=read(ap);p=read(pp);cases=read_source(p['source_files'],evidence_class=LIVE);permit=Permit(a,p,cases,ROOT,sha(ap),sha(pp));binding=permit.binding()
from transformers import AutoTokenizer
class Encoder:
    prepare=LocalInference.prepare
    def __init__(self,path):
        self.tokenizer=AutoTokenizer.from_pretrained(path,local_files_only=True,trust_remote_code=False)
        eos=self.tokenizer.eos_token_id;self.eos_ids=(eos,) if type(eos)is int else tuple(eos)
    def decode(self,ids):return self.tokenizer.decode(ids,skip_special_tokens=True).strip()
encoder=Encoder(p['model']['base_snapshot']);rebuilt=audit(OUT/'probe_events.jsonl',permit,encoder);stored=read(OUT/'probe_report.json');assert rebuilt==stored
# Independently compare every original public prompt rendering/token projection.
source_token_checks=0
for c in cases:
 for old in c.actor_prepared:
  assert encoder.prepare(old['prompt']).to_dict()==old;source_token_checks+=1
launch=read(OUT/'launch_context.json');worker=read(OUT/'worker_start.json');sup=read(OUT/'supervisor_exit.json');external=read(CONTROL/'live_invocation_exit.json');start=read(CONTROL/'live_invocation_start.json');claim=read(CONTROL/'live_dispatch_claim.json');clear=read(DEST/'ONE_LIVE_CLEARANCE_394f9f90869dd8505844caa7ea1a7e9f.json')
assert launch['probe_binding']==binding and launch['clearance_sha256']==sha(DEST/'ONE_LIVE_CLEARANCE_394f9f90869dd8505844caa7ea1a7e9f.json') and launch['supervisor_pid']==start['pid']==external['pid']
assert launch['supervisor_start_tick']==start['start_tick']==external['start_tick'] and launch['supervisor_uid']==worker['uid']==a['execution_uid']
assert sup['launch_context_sha256']==sha(OUT/'launch_context.json') and sup['worker_start_sha256']==sha(OUT/'worker_start.json') and worker['launch_context_sha256']==sha(OUT/'launch_context.json')
live=[sha(DEST/'ONE_LIVE_CLEARANCE_394f9f90869dd8505844caa7ea1a7e9f.json') if x=='@CLEARANCE_SHA256@' else x for x in clear['argv']]
assert launch['supervisor_argv']==live and worker['argv']==['--worker' if x=='--live' else x for x in live]+['--launch-context-sha256',sha(OUT/'launch_context.json')]
assert worker['pid']==worker['pgid']==worker['sid'] and worker['authorization_sha256']==claim['authorization_sha256']==external['authorization_sha256']==binding['authorization_sha256']
assert claim['no_retry'] is True and claim['clearance_sha256']==external['clearance_sha256']==launch['clearance_sha256'] and external['returncode']==sup['authentic_returncode']==0
assert sup['execution_status']=='EXIT_RECORDED' and sup['cleanup_established'] and sup['cleanup_within_budget'] and sup['within_time_cap'] and sup['subreaper_restored'] and not sup['members_after_cleanup'] and not sup['deadline_triggered'] and sup['spawn_or_supervisor_error'] is None
assert sup['allocated_devices']==1 and 0<=sup['allocated_device_hours']==sup['elapsed_seconds']/3600<=LIMITS['device_hours']
assert external['stdout_sha256']==sha(CONTROL/'live.stdout') and external['stderr_sha256']==sha(CONTROL/'live.stderr')
assert not Path('/proc/'+str(worker['pid'])).exists() and not Path('/proc/'+str(start['pid'])).exists()
events=read_events(OUT/'probe_events.jsonl');completed=[e for e in events if e['kind']=='unit_completed'];counts=collections.Counter(e['payload']['identity']['kind'] for e in completed)
gens=[e for e in completed if e['payload']['identity']['kind'] in ('stage_one','stage_two')];actual={'generations':len(gens),'environment_operations':sum(counts[k] for k in ('reset','replay','teacher_step')),'generated_tokens':sum(e['payload']['data']['raw']['generated_tokens'] for e in gens),'input_tokens':sum(e['payload']['data']['raw']['input_tokens'] for e in gens)};assert actual==stored['physical']['completed']=={'generations':10,'environment_operations':64,'generated_tokens':184,'input_tokens':5846}
rows=[]
for c in cases:
 closed=next(e['payload'] for e in events if e['kind']=='case_closed' and e['payload']['case_id']==c.case_id)
 parts={e['payload']['identity']['kind']:e['payload']['data'] for e in gens if e['payload']['identity']['case_id']==c.case_id};step=[e['payload']['data'] for e in completed if e['payload']['identity']['kind']=='teacher_step' and e['payload']['identity']['case_id']==c.case_id]
 row={'case_id':c.case_id,'cutoff':c.cutoff,'stage_one_raw':parts['stage_one']['raw']['raw_output'],'stage_two_raw':parts['stage_two']['raw']['raw_output'],'decision':closed['decision'],'actual_teacher_steps':len(step),'Z_immediate':closed['Z_immediate'],'terminal_observed':closed['terminal_observed']}
 if step:
  assert step[0]['command']!='look' and text_hash(step[0]['command'])==c.diagnostic_command_sha256 and step[0]['after']['done'] and step[0]['after']['reward']>0
  row['command']=step[0]['command'];row['matches_frozen_diagnostic_command']=True
 rows.append(row)
resource=[e['payload']['data'] for e in events if e['kind']=='runtime_evidence' and e['payload']['kind']=='resource_sample'];assert len(resource)==23
from self_improvement.si_s01.shared_resource import STATS
resource_summary={'samples':len(resource),'preweight_free_bytes':next(v['global_memory']['free_bytes'] for v in resource if v['point']=='one_byte_before_weights'),'minimum_later_free_bytes':min(v['global_memory']['free_bytes'] for v in resource if v['point'] not in ('configured_before_probe','one_byte_before_weights')),'maximum_allocated_peak_bytes':max(v['allocator']['stats'][STATS[1]] for v in resource),'maximum_reserved_peak_bytes':max(v['allocator']['stats'][STATS[3]] for v in resource),'effective_limit_bytes':sorted({v['allocator']['effective_limit_bytes'] for v in resource}),'oom_counter_max':max(v['allocator']['stats'][STATS[4]] for v in resource),'allocation_retry_counter_max':max(v['allocator']['stats'][STATS[5]] for v in resource)}
assert all(sha(path)==value for path,value in before.items())
r={'schema':'SI_M1_INDEPENDENT_POST_RUN_REVIEW_V1','decision':'ACCEPT_AUTHENTIC_COMPLETE_FIVE_CASE_MECHANISM_PROBE','reviewer':'Current Astra collaboration agent /root/astra_exact_review; independent resumed review, not historical original Astra thread','reviewed_utc':datetime.now(timezone.utc).isoformat(),'source_sha':a['source_sha'],'run_id':a['run_id'],'binding':binding,'original_artifacts_sha256':before,'original_artifacts_unchanged':True,'production_audit_independently_recomputed_equal':True,'offline_tokenizer':{'loaded_once_CPU_only':True,'local_files_only':True,'trust_remote_code':False,'source_prepared_projection_checks':source_token_checks,'teacher_prompt_encode_and_output_decode_checks':10,'real_model_loaded':False,'generation_calls':0,'CUDA_calls':0,'environment_calls':0},'outcomes':{'planned_N':5,'real_teacher_action_receipts':4,'Z1':4,'Z0':0,'NA':1,'different_action_immediate_candidates':4,'rows':rows},'physical_cost':actual|{'components':dict(counts),'per_call_input_max':max(e['payload']['data']['raw']['input_tokens'] for e in gens),'generation_latency_seconds_sum':sum(e['payload']['data']['raw']['latency_seconds'] for e in gens),'unknown_cost_units':0,'failed_units':0,'open_units':0},'allocation':{'authoritative_allocated_device_hours':sup['allocated_device_hours'],'authoritative_seconds':sup['elapsed_seconds'],'wrapper_seconds_not_additive':external['elapsed_seconds'],'collector_hours_not_additive':stored['collector_allocated_device_hours_lower_bound'],'cleanup_established':True,'cleanup_within_budget':True,'real_worker_and_supervisor_absent_after_exit':True},'resource':resource_summary,'scientific_interpretation':['Four frozen selected development opportunities produced actual different-from-look diagnostic placement commands followed immediately by done=true,reward=1,truncated=false. These are observed genuine terminal successes, not unknown futures.','C093 had complete Stage1 generation but its diagnosis contains13 words, exceeding frozen12-word parser rule; Stage2 was still called under original invalid placeholders, and no teacher action executed. Z=NA, never an environmental failure or Z0. Do not repair/retry.','C094 selected and executed a successful placement, but its Stage1 subgoal says to find and take another tissuebox. Immediate success does not establish correct diagnosis or Stage1-to-action semantic agreement for all four.','Report17 reviewed source failures,5 post-hoc selected opportunities,12 previously frozen exclusions. Four of five produced environment-confirmed immediate candidates;4/5 is descriptive selected-case yield, not population success or held-out evaluation.','Hidden-state/RNG equivalence to source remains unproven; no baseline causal treatment effect, overall agent improvement, full P0 suffix recovery rate or student learning claim. No suffix ran; four immediate terminal outcomes remain known.','At most four environment-verified action candidates exist; student input fit/masking/EOS/de-duplication/conflict/transfer evidence and training authorization are not supplied.','Original96-source cost remains separately retained. This new run adds10 generations and64 reset-inclusive environment operations only; CPU post-run tokenizer validation is separate non-generative audit, not another scientific trial.','No restart, prompt change, case substitution, added suffix, training or collection is authorized by acceptance.'], 'resource_limitations':['Shared nonexclusive GPU; native allocator bound only, not total process VRAM cap.','No NVML-to-local-PID or device-wide usage attribution.','Successful completion does not prove future App/container/cgroup teardown survival.']}
fp=DEST/'POST_RUN_INDEPENDENT_AUDIT_394f9f90.json'
with fp.open('x') as f:f.write(json.dumps(r,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({'path':str(fp),'sha256':sha(fp),'decision':r['decision'],'outcomes':{k:v for k,v in r['outcomes'].items() if k!='rows'},'physical_cost':r['physical_cost'],'allocation':r['allocation'],'resource':resource_summary}))
