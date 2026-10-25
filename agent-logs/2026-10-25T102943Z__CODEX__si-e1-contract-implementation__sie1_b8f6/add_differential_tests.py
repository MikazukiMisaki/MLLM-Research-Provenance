from pathlib import Path
OWN=Path(__file__).resolve().parent
assert OWN==Path('/home/lizening/research-notes/agent-logs/2026-10-25T102943Z__CODEX__si-e1-contract-implementation__sie1_b8f6')
ROOT=Path('/home/lizening/wt-si-p3-engineering-contracts')
f=ROOT/'tests/test_si_p3_collector.py';s=f.read_text()
old='    reg = UnitRegistry(journal)\n    identity = {"slot":"s","task_id":"t","phase":"source","index":0,"operation":"reset"}\n    unit, started = reg.start(identity,{})\n    reg.finish(identity,unit,started,{})'
new='    slot=synthetic_plan()[0]\n    journal.append("slot_planned", {"slot":asdict(slot),"slot_key":slot.key})\n    reg = UnitRegistry(journal)\n    identity = {"slot":slot.key,"task_id":slot.task_id,"phase":"source","index":0,"operation":"reset"}\n    unit, started = reg.start(identity,{})\n    data={"session":digest([slot.key,"source"]),"seed":slot.seed,"state":PublicState(slot.task_id,slot.family,"goal","obs",("wait",)).to_dict()}\n    reg.finish(identity,unit,started,data)'
assert old in s;s=s.replace(old,new)
s+=r'''


@pytest.mark.parametrize('case',['wrong_start','wrong_kind','wrong_task','wrong_run','wrong_seed','shape','without_start'])
def test_registry_rejects_bad_completion_online_before_journal_append(tmp_path,case):
    slot=synthetic_plan()[0]
    def create(name):
        journal=Journal(tmp_path/name,plan_sha256='a'*64,evidence_class='synthetic')
        journal.append('slot_planned',{'slot':asdict(slot),'slot_key':slot.key})
        return journal,UnitRegistry(journal)
    journal,registry=create('one.jsonl')
    identity={'slot':slot.key,'task_id':slot.task_id,'phase':'source','index':0,'operation':'reset'}
    unit,started=registry.start(identity,{})
    data={'session':digest([slot.key,'source']),'seed':slot.seed,'state':PublicState(slot.task_id,slot.family,'goal','obs',('wait',)).to_dict()}
    if case=='wrong_start':started='wrong'
    if case=='wrong_kind':identity=identity|{'operation':'generation'}
    if case=='wrong_task':identity=identity|{'task_id':'other'}
    if case=='wrong_seed':data['seed']+=1
    if case=='shape':data={'parsed':{}}
    if case=='without_start':unit='missing'
    if case=='wrong_run':
        other,other_registry=create('other.jsonl')
        unit,started=other_registry.start(identity,{})
        other.close()
    count=len(journal.events)
    with pytest.raises(ContractError):registry.finish(identity,unit,started,data)
    assert len(journal.events)==count and registry.states[next(iter(registry.states))]=='started'
    journal.close()


@pytest.mark.parametrize('phase',['source','suffix'])
def test_new_P0_decision_equals_actual_frozen_actor_generation_for_cap_incomplete(monkeypatch,phase):
    from types import SimpleNamespace
    from scripts import run_r19_experiment as frozen
    from recovery.r19_duration import RecoveryCursor
    from self_improvement.si_p3.collector import parse_generation
    from self_improvement.si_p3.contract import request
    slot=synthetic_plan()[0]
    state=PublicState(slot.task_id,slot.family,'Synthetic goal','Synthetic observation',('wait','change'))
    tok=SyntheticTokenizer()
    def incomplete(raw,boundary):
        ids=raw['token_ids'][:-1]+[tok.token(' ')]*(16-len(raw['token_ids'])+1)
        raw.update(token_ids=ids,generated_tokens=16,token_ids_sha256=hashlib.sha256(json.dumps(ids,separators=(',',':')).encode()).hexdigest(),output_complete=False,token_cap_reached=True)
        return raw
    raw_boundary=RawBoundary(tok,mutate=incomplete)
    port=ProducerAdapter(tok,raw_boundary,evidence_class='synthetic')
    prepared=port.prepare(projection(state,[])['public_prompt'])
    value=port.generate(prepared,16,'P0')
    observed=parse_generation(phase,value,state)
    # Substitute only the raw model boundary; execute the real frozen actor method.
    monkeypatch.setattr(frozen,'_generate_exact',lambda backend,prompt,cap:raw_boundary(prompt,cap,'P0'))
    runtime=SimpleNamespace(actor_backend=object(),_reserve_model_call=lambda identity:None,
                            sink=lambda *args:{'event_id':'frozen-software-event'})
    cursor=RecoveryCursor(task=request(state,[]).task,task_id=slot.task_id,canonical_trial_id=slot.task_id,
                          nominal_seed=slot.seed,observation=state.observation,valid_actions=state.valid_actions,
                          history=(),actions_consumed=0)
    _,expected,_=frozen.LiveR19Runtime.actor_generation(runtime,cursor,component='task_actor' if phase=='source' else 'suffix',identity={'operation':'source_generation' if phase=='source' else 'task_actor_generation'})
    assert value.raw['output_complete'] is False and value.raw['token_cap_reached'] is True
    assert observed=={'status':expected['status'],'action_id':expected['action_id'],'command':expected['action']}
    assert observed['status']=='selected' and observed['command']=='wait'


@pytest.mark.parametrize('output,complete,expected',[('A001',True,'selected'),('Action-ID: A001',True,'malformed_id'),('A001',False,'truncated_stage_two'),('A999',True,'out_of_range_id')])
def test_teacher_v2_prompt_and_parser_differential(output,complete,expected):
    from recovery.two_stage_v2 import stage_two_prompt as frozen_prompt,parse_bare_stage_two_output
    from self_improvement.si_p3 import collector,audit
    from self_improvement.si_p3.contract import Generation,request
    slot=synthetic_plan()[0]
    state=PublicState(slot.task_id,slot.family,'goal','observation',('wait','change'))
    raw={'prompt':'synthetic prompt','raw_output':output,'generated_tokens':16 if not complete else 2,
         'input_tokens':10,'latency_seconds':0,'output_complete':complete,'token_cap_reached':not complete,'max_new_tokens':16}
    generation=Generation(raw)
    kwargs={'diagnosis':'Repeated waiting','subgoal':'Change activity','stage_one_valid':True}
    wanted=frozen_prompt(request(state,[]),**kwargs)
    assert collector.stage_two_prompt(request(state,[]),**kwargs)==wanted
    assert audit.stage_two_prompt(request(state,[]),**kwargs)==wanted
    frozen=parse_bare_stage_two_output(generation.record(),state.valid_actions)
    parsed=collector.parse_generation('stage_two',generation,state)
    assert parsed=={'status':frozen.status,'action_id':frozen.action_id,'command':frozen.action}
    assert parsed['status']==expected


def test_source_and_suffix_execute_valid_bare_ID_even_if_cap_incomplete(tmp_path):
    def mutate(raw,boundary):
        if raw['adapter_mode']=='P0':
            ids=raw['token_ids'][:-1]+[boundary.tokenizer.token(' ')]*(16-len(raw['token_ids'])+1)
            raw.update(token_ids=ids,generated_tokens=16,token_ids_sha256=hashlib.sha256(json.dumps(ids,separators=(',',':')).encode()).hexdigest(),output_complete=False,token_cap_reached=True)
        return raw
    run,events,tok,raw,envs=collect_synthetic(tmp_path/'P0-cap',mutate=mutate)
    assert run['status']=='COMPLETE'
    checked=audit_run(run,events,tok)
    assert checked['components']['source:step']>0 and checked['components']['suffix:step']==96
    for phase in ('source','suffix'):
        values=[e['payload']['data'] for e in events if e['kind']=='unit_completed' and e['payload']['identity']['operation']=='generation' and e['payload']['identity']['phase']==phase]
        assert values and all(v['raw']['output_complete'] is False and v['parsed']['status']=='selected' for v in values)
    from self_improvement.si_p3.data import build_pool
    assert len(build_pool(run,events,tok).candidates)==96  # teacher targets remain complete; no actor policy redesign


@pytest.mark.parametrize('mode',['labeled','incomplete'])
def test_actual_collector_uses_v2_teacher_bare_and_strict_completion(tmp_path,mode):
    first=synthetic_plan()[0]
    def mutate(raw,boundary):
        targeted=raw['prompt'].startswith('Select the one currently available action') and f'synthetic task {first.task_id.rsplit("/",1)[-1]}.' in raw['prompt'] and first.family in raw['prompt']
        if targeted:
            text='Action-ID: A001' if mode=='labeled' else 'A001'
            ids=boundary.tokenizer(text)['input_ids']
            if mode=='incomplete':ids+=[boundary.tokenizer.token(' ')]*(16-len(ids))
            else:ids+=[1]
            raw.update(raw_output=text,token_ids=ids,generated_tokens=len(ids),token_ids_sha256=hashlib.sha256(json.dumps(ids,separators=(',',':')).encode()).hexdigest(),token_cap_reached=len(ids)==16,output_complete=mode!='incomplete')
        return raw
    run,events,tok,*_=collect_synthetic(tmp_path/mode,mutate=mutate)
    audit_run(run,events,tok)
    row=run['slots'][0]
    assert row['disposition']=='INVALID_TEACHER' and row['YT'] is None
    assert row['branch']['teacher_step'] is None and row['branch']['suffix'] is None
'''
f.write_text(s)
# Bind step before-state to its already completed generation/source step online.
f=ROOT/'src/self_improvement/si_p3/evidence.py';s=f.read_text();s=s.replace('require(data["generation_event"] is None and proof["data"]["action_id"] == data["action_id"] and','require(data["generation_event"] is None and proof["data"]["before"] == data["before"] and proof["data"]["action_id"] == data["action_id"] and');s=s.replace('require(data["source_step"] is None and proof["data"]["parsed"]["status"] == "selected" and','require(data["source_step"] is None and proof["data"]["state"] == data["before"] and proof["data"]["parsed"]["status"] == "selected" and');f.write_text(s)
print('Added actual frozen actor method differential, frozen v2 prompt/parser differential, full source/suffix and teacher negative integration tests.')
