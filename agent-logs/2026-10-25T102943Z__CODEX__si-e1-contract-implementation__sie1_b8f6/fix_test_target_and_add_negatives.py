from pathlib import Path
OWN=Path(__file__).resolve().parent
assert OWN==Path('/home/lizening/research-notes/agent-logs/2026-10-25T102943Z__CODEX__si-e1-contract-implementation__sie1_b8f6')
ROOT=Path('/home/lizening/wt-si-p3-engineering-contracts')
f=ROOT/'tests/test_si_p3_collector.py';s=f.read_text().replace('and first.split(\'/\')[0] in raw["prompt"]','and first.split(\'-\',1)[0] in raw["prompt"]');f.write_text(s)
f=ROOT/'tests/si_p3_support.py';s=f.read_text().replace('reached and (self.source_success or (self.changed and not self.branch_fail))','reached and (self.source_success or self.changed) and not (self.changed and self.branch_fail)');f.write_text(s)
f=ROOT/'tests/test_si_p3_collector.py';f.write_text(f.read_text()+r'''

def _coherent_semantic_tamper(run, events, mutate):
    """Rebind *all* hashes/refs so semantic guards, rather than stale hashes, decide."""
    run, events = copy.deepcopy(run), copy.deepcopy(events)
    mutate(run,events)
    replacements={}
    def rebound(x):
        if isinstance(x,str):return replacements.get(x,x)
        if isinstance(x,list):return [rebound(v) for v in x]
        if isinstance(x,dict):return {k:rebound(v) for k,v in x.items()}
        return x
    previous=None
    closed=[]
    for event in events:
        old=event['event_id']
        event['previous']=previous
        event['payload']=rebound(event['payload'])
        if event['kind']=='slot_closed':
            row=event['payload']
            row['source_reference_sha256']=digest(row['source'])
            closed.append(row)
        if event['kind']=='run_closed':
            run['slots']=closed
            event['payload']['summary_sha256']=digest({k:v for k,v in run.items() if k!='journal_last_event'})
        event['event_id']=digest({k:v for k,v in event.items() if k!='event_id'})
        replacements[old]=event['event_id'];previous=event['event_id']
    run['journal_last_event']=previous
    return run,events


@pytest.mark.parametrize('tamper,reason',[('source_action','Action-ID'),('replay_action','Action-ID'),('teacher_session','same-environment'),('future_projection','projection/future'),('teacher_label','suffix label')])
def test_semantic_integrity_survives_complete_attacker_rehash(complete,tamper,reason):
    def change(run,events):
        if tamper=='future_projection':
            target=next(e for e in events if e['kind']=='slot_closed')
            target['payload']['projection']['future_success']=1
            return
        if tamper=='teacher_label':
            target=next(e for e in events if e['kind']=='slot_closed')
            target['payload']['YT']=1-target['payload']['YT']
            return
        phase={'source_action':'source','replay_action':'replay','teacher_session':'teacher'}[tamper]
        target=next(e for e in events if e['kind']=='unit_completed' and e['payload']['identity']['operation']=='step' and e['payload']['identity']['phase']==phase)
        if tamper=='teacher_session':target['payload']['data']['session']='different-environment'
        else:target['payload']['data']['action_id']=None
    run,events=_coherent_semantic_tamper(complete[0],complete[1],change)
    validate_journal(events)
    with pytest.raises(ContractError,match=reason):audit_run(run,events,complete[2])


def test_harm_and_both_failure_stay_in_common_Q_denominator(tmp_path):
    from self_improvement.si_p3.data import build_pool
    from self_improvement.si_p3.contract import ADOPTION_QUOTAS
    plan=synthetic_plan()
    rescue=next(s for s in plan if int(s.task_id.rsplit('-',1)[-1])<ADOPTION_QUOTAS[s.family])
    neutral=next(s for s in plan if int(s.task_id.rsplit('-',1)[-1])>=ADOPTION_QUOTAS[s.family])
    targets={rescue.task_id,neutral.task_id}
    run,events,tok,*_=collect_synthetic(tmp_path/'harm',env_options=lambda s,p:{'branch_fail':s.task_id in targets})
    pool=build_pool(run,events,tok)
    assert len(pool.candidates)==96
    labels={c.example.task_id:(c.Y0,c.YT) for c in pool.candidates}
    assert labels[rescue.task_id]==(0,0) and labels[neutral.task_id]==(1,0)
''')
print('Fixed test-only invalid-output target predicate; added full-rehash semantic negatives and harms in common Q.')
