"""Independent read-only recount; does not import developer ledger/auditor."""
from pathlib import Path
from collections import Counter
from datetime import datetime, timezone
import argparse
import hashlib
import json

OWN=Path(__file__).resolve().parent
assert OWN.name=='2026-10-25T124118Z__SOL__si-e2-runtime-resource-review__sie2_4c82'

def canonical(v):
    return json.dumps(v,ensure_ascii=True,sort_keys=True,separators=(',',':'),allow_nan=False)
def digest(v):
    return hashlib.sha256(canonical(v).encode()).hexdigest()

def recount(run):
    events=[json.loads(s) for s in (run/'engineering_events.jsonl').read_text().splitlines()]
    starts={};done={};failed={};previous=None
    for i,row in enumerate(events):
        assert row['sequence']==i and row['previous']==previous
        assert digest({k:v for k,v in row.items() if k!='event_id'})==row['event_id']
        previous=row['event_id']
        p=row['payload'];kind=row['kind']
        if kind=='external_started':
            assert p['unit'] not in starts
            starts[p['unit']]=p
        elif kind in ('external_completed','external_failed'):
            u=p['unit'];assert u in starts and u not in done and u not in failed
            (done if kind=='external_completed' else failed)[u]=p
    count=Counter();unknown=Counter();gen=[];reserved=Counter()
    phases=[('source',16,'P0'),('stage_one',40,'BASE'),('stage_two',16,'BASE'),('suffix',16,'P0')]
    for u,p in starts.items():
        reserved.update(p['reservation'])
        if u not in done:
            unknown.update(p['reservation']);continue
        count[p['kind']]+=1
        if p['kind']!='generation':continue
        data=done[u]['data'];r=data['raw'];prep=p['prepared']
        assert prep==data['tensor_proof']['prepared']==data['tensor_proof']['sent']
        assert r['input_tokens']==len(prep['input_ids'])==len(prep['attention_mask'])
        assert r['generated_tokens']==len(r['token_ids'])
        assert r['token_ids_sha256']==hashlib.sha256(json.dumps(r['token_ids'],separators=(',',':')).encode()).hexdigest()
        phase,cap,mode=phases[len(gen)]
        assert p['phase']==phase and r['max_new_tokens']==cap and r['adapter_mode']==mode
        assert r['do_sample'] is False and r['thinking'] is False
        assert 0<len(r['token_ids'])<=cap
        assert r['rendered_prompt']==prep['rendered_prompt'] and r['prompt']==prep['prompt']
        assert r['rendered_prompt_sha256']==hashlib.sha256(prep['rendered_prompt'].encode()).hexdigest()
        states=data['adapter_states']
        assert states['before']==states['after']
        for point in ('before','during','after'):
            expected=point!='during' or mode=='P0'
            state=states[point]
            assert state['model']['enabled'] is expected and state['model']['trainable_params']==0
            assert state['model']['active_adapters']==['default'] and state['model']['merged_adapters']==[]
            assert state['layers']
            assert all(x['enabled'] is expected and x['active_adapters']==['default'] and x['merged_adapters']==[] for x in state['layers'])
        gen.append({'phase':phase,'mode':mode,'input_tokens':r['input_tokens'],'generated_tokens':r['generated_tokens'],
                    'latency_seconds':r['latency_seconds'],'raw_output':r['raw_output']})
    report=json.loads((run/'engineering_report.json').read_bytes()) if (run/'engineering_report.json').exists() else None
    receipt=json.loads((run/'supervisor_exit.json').read_bytes())
    result={'schema':'SI_E2_ROOT_INDEPENDENT_PHYSICAL_RECOUNT_V1','observed_utc':datetime.now(timezone.utc).isoformat(),
            'run_directory':str(run),'journal_chain':'PASS','source_sha':receipt['source_sha'],
            'authentic_child_returncode':receipt['authentic_returncode'],'deadline_triggered':receipt['deadline_triggered'],
            'spawn_or_supervisor_error':receipt['spawn_or_supervisor_error'],
            'within_time_cap':receipt['within_time_cap'],'child_report_present':receipt['child_report_present'],
            'remaining_members':receipt['members_after_cleanup'],'allocated_device_hours':receipt['allocated_device_hours'],
            'completed_external_kinds':dict(count),'open_units':sorted(set(starts)-set(done)),
            'failed_units':sorted(failed),'incomplete_conservative_reservations':dict(unknown),
            'generation_details':gen,'engineering_actual_generations':len(gen),
            'engineering_actual_input_tokens':sum(r['input_tokens'] for r in gen),
            'engineering_actual_generated_tokens':sum(r['generated_tokens'] for r in gen),
            'engineering_completed_resets':count['reset'],'engineering_completed_action_steps':count['step'],
            'engineering_completed_reset_inclusive_ops':count['reset']+count['step'],
            'report_status':report['status'] if report else 'ABSENT',
            'historical_science_cumulative_unchanged':{'generations':5142,'reset_inclusive_operations':7949},
            'known_R19_plus_this_engineering_completed_physical_total':{'generations':5142+len(gen),
                    'reset_inclusive_operations':7949+count['reset']+count['step']},
            'accounting_note':'Engineering is not a scientific sample, but is real expenditure. Completed totals exclude unknown open reservations; do not relabel them zero.',
            'science_acquisition_training_evaluation':'NOT_RUN_NOT_GRANTED',
            'inputs':{p.name:{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
                      for p in run.iterdir() if p.is_file()}}
    return result

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('run',type=Path);a=parser.parse_args()
    result=recount(a.run.resolve())
    dest=OWN/'independent_runtime_recount.json'
    assert not dest.exists()
    dest.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
