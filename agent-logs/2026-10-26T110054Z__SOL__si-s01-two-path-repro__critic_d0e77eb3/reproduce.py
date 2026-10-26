from pathlib import Path
import collections, hashlib, json, sys

ISOLATED=Path(sys.argv[1]).resolve()
OWN=Path(sys.argv[2]).resolve()
CASE=sys.argv[3]
assert CASE in ('initialize_failure_cleanup','step50_nonterminal_empty_map')
blocked=[]
class NoRealRuntime:
    def find_spec(self, fullname, path=None, target=None):
        if fullname.split('.',1)[0] in {'torch','transformers','peft','alfworld','textworld','tokenizers','sentencepiece','numpy'}:
            blocked.append(fullname)
            raise RuntimeError('forbidden real runtime import in software reproduction: '+fullname)
sys.meta_path.insert(0,NoRealRuntime())
sys.path[:0]=[str(ISOLATED/'src'),str(ISOLATED/'tests')]
from self_improvement.si_s01.collector import Producer,Collector
from self_improvement.si_s01.audit import audit,write_report
from self_improvement.si_s01.contract import P0_SHA256
from si_s01_support import Tokenizer,FakeEnv,plan

p=plan();tok=Tokenizer();raw_calls=[];envs=[]
class BoundaryEnvironment(FakeEnv):
    def __init__(self,slot,options):
        super().__init__(slot,options);self.initialize_calls=0;self.close_calls=0;self.acquired=False
    def initialize(self):
        self.initialize_calls+=1;self.acquired=True
        if CASE=='initialize_failure_cleanup' and self.slot==p.slots[0]:
            raise OSError('synthetic initialization I/O failure after acquiring closable fixture object')
        return super().initialize()
    def close(self):
        self.close_calls+=1
        return super().close()

def factory(slot):
    options={'done_at':100,'empty_at':50} if CASE=='step50_nonterminal_empty_map' and slot==p.slots[0] else {'done_at':1}
    env=BoundaryEnvironment(slot,options);envs.append(env);return env

def raw(prepared,slot,index):
    text='A000';tokens=[ord(x) for x in text]+[1]
    record={'prompt':prepared.prepared.prompt,'rendered_prompt':prepared.prepared.rendered_prompt,
      'rendered_prompt_sha256':hashlib.sha256(prepared.prepared.rendered_prompt.encode()).hexdigest(),
      'raw_output':text,'token_ids':tokens,'token_ids_sha256':hashlib.sha256(json.dumps(tokens,separators=(',',':')).encode()).hexdigest(),
      'input_tokens':len(prepared.prepared.input_ids),'generated_tokens':len(tokens),'latency_seconds':0.0,
      'output_complete':True,'token_cap_reached':False,'max_new_tokens':16,'do_sample':False,'thinking':False,
      'adapter_mode':'P0','adapter_sha256':P0_SHA256}
    raw_calls.append((slot.key,index))
    return {'raw':record,'runtime':{'synthetic_software_fixture':True}}

producer=Producer(tok,raw,evidence_class='synthetic_software_fixture')
output=OWN/CASE
collector=Collector(p,lambda ledger:producer,factory,output,run_id=('a' if CASE=='initialize_failure_cleanup' else 'b')*32)
loaded,stop=collector.run()
events=[json.loads(line) for line in (output/'source_events.jsonl').read_text().splitlines()]
first=collector.rows[0]
observed={'status':'PRELIMINARY_REPRODUCTION_ONLY','case':CASE,'collector_stop':stop,'slot_count':len(collector.rows),
    'normal_sources':sum(row['disposition']=='NORMAL_SOURCE' for row in collector.rows),'first_row_Y0':first['Y0'],
    'first_row_termination':first.get('termination'),'first_row_end_state':first.get('end_state'),
    'source_seals':sum(e['kind']=='sources_sealed' for e in events),'synthetic_raw_generations':len(raw_calls),
    'environment_fixture_calls':[{'initialize':e.initialize_calls,'resets':e.resets,'close':e.close_calls,'closed':e.closed} for e in envs],
    'terminal_units':[{'event':e['kind'],'operation':e['payload']['identity']['kind'],'failure':e['payload'].get('data',{}).get('message')} for e in events if e['kind']=='unit_failed' or (e['kind']=='unit_completed' and e['payload']['identity']['kind'] in ('env_construct','env_close'))],
    'forbidden_import_attempts':blocked,'scientific_generations':0,'scientific_environment_operations':0}
(OWN/(CASE+'.collector_observation.json')).write_text(json.dumps(observed,indent=2)+'\n')
print(json.dumps({k:v for k,v in observed.items() if k not in ('environment_fixture_calls','terminal_units')},sort_keys=True),flush=True)
# This is the archived production auditor; no monkeypatch or exception substitution.
report=audit(output/'source_events.jsonl',output/'source_trajectories.jsonl',p,loaded)
write_report(output,report)
print(json.dumps({'production_audit_returned':True,'status':report['status'],'normal_sources':report['normal_sources'],
                 'source_phase_sealed':report['source_phase_sealed'],'physical':report['physical'],'upper_bounds':report['upper_bounds'],
                 'forbidden_import_attempts':blocked},sort_keys=True),flush=True)
