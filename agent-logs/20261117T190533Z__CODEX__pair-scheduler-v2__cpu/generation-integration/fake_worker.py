"""Test-only independent process exercising real StageBudgetChannel wire client.

Fake episode deliberately does not call a tokenizer, model, or ALFWorld.
"""
import hashlib
import json
import os
from pathlib import Path
import sys
import types

HERE=Path(__file__).parent
sys.path.insert(0,str(HERE))
from fixed_product_dev.arm_stage import run_arm
import production_adapter
SOURCE=Path('/home/lizening/research-notes/agent-logs/20261116__CODEX__two-object-paired-eval__candidate/gate-live/effect_ipc.py')
raw=SOURCE.read_bytes()
if hashlib.sha256(raw).hexdigest()!='046c0c48291efdae06457d87343d084357ae5a1774c3d670e3e232b15fd16dd8':raise SystemExit('effect source drift')
ipc=types.ModuleType('effect_ipc_bound');exec(compile(raw,str(SOURCE),'exec'),ipc.__dict__)
SOURCE_WORKER=SOURCE.with_name('source_worker.py')
source_raw=SOURCE_WORKER.read_bytes()
if hashlib.sha256(source_raw).hexdigest()!='36f4d2a4d82e5798a5d3fd786fa80505fe3c345ff7333aa8bdfaf52581a34111':raise SystemExit('source worker drift')
source_worker=types.ModuleType('source_worker_bound');exec(compile(source_raw,str(SOURCE_WORKER),'exec'),source_worker.__dict__)
config=json.loads(Path(sys.argv[1]).read_text());fd=int(sys.argv[2]);mode=sys.argv[3]
cases={'synthetic':{'family':'two','inputs':config['inputs']}}
_,verify,_=production_adapter.load_synthetic_bound(Path(config['port_source']),Path(config['fixture_root']),cases)
class State:
    goal='fictional';family='pick_two_obj_and_place'
    def to_dict(self):return {'task_id':'synthetic','family':self.family,'goal':self.goal,'observation':'fixture',
                              'valid_actions':['fictional action'],'done':False,'reward':0,'truncated':False}
class Env:
    def __init__(self,game,config_path,data_root,seed,*,family,case_id):self.game=str(game)
    def initialize(self):return {'synthetic':True}
    def reset(self):return (State(),self.game,{'candidate_native_reset':{'won_batch':[False],'won_batch_type':'list'}})
    def close(self):pass

class Row:
    def __init__(self, values):self.values=values
    def tolist(self):return self.values
class Tensor:
    def __init__(self, values):self.values=values;self.shape=(1,len(values))
    def to(self, device):return self
    def __getitem__(self, index):return Row(self.values)
class Tokenizer:
    eos_token_id=151645;pad_token_id=151643
    def __call__(self, **kw):return {'input_ids':Tensor([4,5]),'attention_mask':Tensor([1,1])}
class Config:
    def to_dict(self):return {'eos_token_id':[151645,151643],'pad_token_id':151643,'forced_eos_token_id':None}
class Model:
    device='SYNTHETIC';generation_config=Config()
    def eval(self):pass
    def parameters(self):return []
    def generate(self, **kwargs):
        if mode=='interrupt':os._exit(7)
        return types.SimpleNamespace(sequences=Tensor([4,5,99,151645]),scores=[None,None])
class Torch:
    cuda=types.SimpleNamespace(synchronize=lambda:None)
    @staticmethod
    def no_grad():
        class Context:
            def __enter__(self):pass
            def __exit__(self,*args):pass
        return Context()
class Resource:
    def before_generation(self,*a,**kw):pass
    def after_generation(self,*a,**kw):pass
class Producer:
    tokenizer=Tokenizer();model=Model();torch=Torch();resource=Resource();eos_ids=[151645];arm='P0'
    def prepare(self,prompt):return {'prompt':prompt,'rendered_prompt':'synthetic rendered prompt','input_ids':[4,5],'attention_mask':[1,1]}
    def decode(self, ids):return 'A000'
    def verify_state(self):return 'synthetic state'

def fake_episode(*,arm,previous_initial,controller,env_factory,**unused):
    env=controller.effect('env_construct',env_factory,lambda _:{'arm':arm})
    controller.effect('env_init',env.initialize,lambda _:{'arm':arm})
    reset=controller.effect('reset',env.reset,lambda v:{'arm':arm,'state':v[0].to_dict(),'gamefile':v[1],
                'candidate_native_reset':v[2]['candidate_native_reset']})
    controller.effect('model_load',lambda:'FAKE MODEL LABEL',lambda _:{'arm':arm})
    prompt='synthetic public prompt'
    public={'goal':'fictional','observation':'synthetic', 'public_prompt':prompt,
            'public_prompt_sha256':hashlib.sha256(prompt.encode()).hexdigest(), 'recent_history':[],
            'valid_actions':['fictional action'], 'action_map':{'A000':'fictional action'}}
    original=controller.journal
    class JournalWrapper:
        def emit(self,kind,payload):
            if kind=='prepared':
                if mode=='missing_prepared':return None
                if mode=='bad_public':payload['public']['public_prompt_sha256']='0'*64
                if mode=='bad_kwargs':payload['kwargs']['num_return_sequences']=2
                result=original.emit(kind,payload)
                if mode=='duplicate_prepared':original.emit(kind,payload)
                return result
            return original.emit(kind,payload)
    controller.journal=JournalWrapper()
    try:source_worker._generation(Producer(),public,controller,[151645,151643],151643)
    finally:controller.journal=original
    env.close()
    return {'arm':arm,'initial_public':reset[0].to_dict(),'won':False,'steps':0,'termination':'FAKE_ONLY'}

run_arm(output=config['output'],budget_fd=fd,case=config['case'],arm=config['arm'],
        previous_initial=None,inputs=config['inputs'],seed=42,journal_class=ipc.Journal,
        owner_class=ipc.EffectOwner,controller_class=ipc.Controller,pair_binding=config['binding'],
        verify_materialized=verify,environment_class=Env,step_wrapper=lambda x:x,episode=fake_episode,
        projection=None,source_worker=None,load_producer=None,parser=None,parse_value=None,
        state_factory=None,expected_eos=[151645,151643],expected_pad=151643)
