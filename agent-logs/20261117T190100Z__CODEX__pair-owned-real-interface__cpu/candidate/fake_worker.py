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

def fake_episode(*,arm,previous_initial,controller,env_factory,**unused):
    env=controller.effect('env_construct',env_factory,lambda _:{'arm':arm})
    controller.effect('env_init',env.initialize,lambda _:{'arm':arm})
    reset=controller.effect('reset',env.reset,lambda v:{'arm':arm,'state':v[0].to_dict(),'gamefile':v[1],
                'candidate_native_reset':v[2]['candidate_native_reset']})
    controller.effect('model_load',lambda:'FAKE MODEL LABEL',lambda _:{'arm':arm})
    if mode!='missing_prepared':
        prepared={'input_ids':[4,5],'attention_mask':[1,1],
                  'kwargs':{'max_new_tokens':16,'do_sample':False},
                  'generation_config':{'eos_token_id':[151645,151643],'pad_token_id':151643,'forced_eos_token_id':None}}
        controller.journal.emit('prepared',prepared)
        if mode=='duplicate_prepared':controller.journal.emit('prepared',prepared)
    def fake_generation():
        if mode=='interrupt':os._exit(7)
        return None
    controller.effect('generation',fake_generation,lambda _:{'shape':[1,4],'sequence':[4,5,99,151645],
                                        'output_ids':[99,151645],'decoder_stop_reason':'NOT_OBSERVED'})
    env.close()
    return {'arm':arm,'initial_public':reset[0].to_dict(),'won':False,'steps':0,'termination':'FAKE_ONLY'}

run_arm(output=config['output'],budget_fd=fd,case=config['case'],arm=config['arm'],
        previous_initial=None,inputs=config['inputs'],seed=42,journal_class=ipc.Journal,
        owner_class=ipc.EffectOwner,controller_class=ipc.Controller,pair_binding=config['binding'],
        verify_materialized=verify,environment_class=Env,step_wrapper=lambda x:x,episode=fake_episode,
        projection=None,source_worker=None,load_producer=None,parser=None,parse_value=None,
        state_factory=None,expected_eos=[151645,151643],expected_pad=151643)
