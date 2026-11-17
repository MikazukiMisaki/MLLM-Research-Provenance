"""Synthetic boundaries around exact original episode/generation/parser/IPC code.

No real task, model, tokenizer, environment or GPU is opened or instantiated.
"""
import contextlib
import dataclasses
import hashlib
import json
import os
from pathlib import Path
import sys
import types

SOURCE_ROOT=Path('/home/lizening/.codex/worktrees/parallel-goal-runtime-9dd/src')
OLD=Path('/home/lizening/research-notes/agent-logs/20261116__CODEX__two-object-paired-eval__candidate/gate-live')
EPISODE=Path('/home/lizening/research-notes/agent-logs/20261118__CODEX__fixed_product_per_arm__private/runtime/fixed_product_dev/episode.py')
BINDINGS={
 str(EPISODE):'06922aed662e84c1366624600c361f64ca7fba1ee93daccf83ff8de7a174a21b',
 str(OLD/'source_worker.py'):'36f4d2a4d82e5798a5d3fd786fa80505fe3c345ff7333aa8bdfaf52581a34111',
 str(OLD/'effect_ipc.py'):'046c0c48291efdae06457d87343d084357ae5a1774c3d670e3e232b15fd16dd8',
 str(SOURCE_ROOT/'models/protocol_stability.py'):'d363677d90e247b15cccf68bdfdcaf3712d684567b8c167de266da2850ebb87d',
 str(SOURCE_ROOT/'models/__init__.py'):'816de73a81c638c747ed78dd1ee75434ed98e0dc7949f689ee8b00a216e6e960',
 str(SOURCE_ROOT/'models/action_parser.py'):'0a1c668d590980d1d8cdd4104a2b3c9aa851037fc238a2c73c45b57ab4432fbe',
 str(SOURCE_ROOT/'models/policy.py'):'afbb9544e2ea0c2aa73d3f7dcfbf7e366f1daf6eb95fd4e89fefe0c913dda469',
 str(SOURCE_ROOT/'models/qwen.py'):'ee3a5a599a8dece7b206b2aa675004723fa343bcbd8844063d00a7af154140eb',
 str(SOURCE_ROOT/'env/__init__.py'):'6a4a3de8e04902930dff5a78aaaa27b546d335d4d15d717908561fa7b6e6a831',
 str(SOURCE_ROOT/'env/base.py'):'a3ae633aa79c8f80a70629fd398b880ea9c1807e7c219717b98e518b12496abb',
 str(SOURCE_ROOT/'self_improvement/__init__.py'):'84ba2265d10e0d1bec7c1ea8da5ef4d7e6ee2d1272a04ad63bb1b2f00ca8b272',
 str(SOURCE_ROOT/'self_improvement/si_p3/__init__.py'):'16d722a95f36a7d6a36dcce9757b940b4310960eab7f990e32bf61dc2cbb87be',
 str(SOURCE_ROOT/'self_improvement/si_p3/contract.py'):'2d7b05d5c230cb45c2ad90c7507c11a5c76ce52f7335548c46a48d78e8842239',
 str(SOURCE_ROOT/'recovery/__init__.py'):'7acbbbda9e57a74450898d3764135724006fb747f5e2419b32079ba994805352',
 str(SOURCE_ROOT/'recovery/corpus.py'):'14d8ee0f4059f43e76cd94f6511f4ad1e40b4c97377e9bce987d48b59e66a6a1',
 str(SOURCE_ROOT/'recovery/fixed.py'):'2f8e1c6366e873aed0f804d021072bd7d7efc32fa109483a7e47dfbcefdd177f',
 str(SOURCE_ROOT/'recovery/pilot.py'):'f60af87ec1a5e762afaefd26c048a103de7bc538cedff3afc4281a3a613bbd72',
 str(SOURCE_ROOT/'recovery/two_stage.py'):'7fbdfa36268083a167ff1ce04f8dcb33b20024ee115ed65424e1c257b9329629',
 str(SOURCE_ROOT/'sft/__init__.py'):'7e4d035251916371c0129102558ab9f242ae7afe75ed5f69dcdeb4b1fafe4877',
 str(SOURCE_ROOT/'sft/protocol.py'):'cb9a8ee23d1208064348810ef3580773ba14403bfaac6a4e7f4a43c5540178a8'}
raw={}
for path,expected in BINDINGS.items():
    data=Path(path).read_bytes()
    if hashlib.sha256(data).hexdigest()!=expected:raise SystemExit('source hash mismatch')
    raw[path]=data

def load_bound(name,path):
    module=types.ModuleType(name);module.__file__=str(path)
    exec(compile(raw[str(path)],str(path),'exec'),module.__dict__)
    return module
ipc=load_bound('effect_ipc_bound',OLD/'effect_ipc.py')
source=load_bound('source_worker_bound',OLD/'source_worker.py')
episode=load_bound('episode_bound',EPISODE)
sys.path.insert(0,str(SOURCE_ROOT))
from models.protocol_stability import parse_p2_selection
import models.protocol_stability as parser_module
from self_improvement.si_p3.contract import PublicState, projection
import self_improvement.si_p3.contract as contract_module
if Path(contract_module.__file__).resolve() != (SOURCE_ROOT/'self_improvement/si_p3/contract.py').resolve():
    raise SystemExit('unexpected production contract origin')
if Path(parser_module.__file__).resolve() != (SOURCE_ROOT/'models/protocol_stability.py').resolve():
    raise SystemExit('unexpected parser origin')
if 'torch' in sys.modules or 'transformers' in sys.modules:raise SystemExit('unexpected real runtime import')
for name,module in tuple(sys.modules.items()):
    if not (name=='models' or name.startswith(('models.','env.','recovery.','sft.','self_improvement.')) or name in ('env','recovery','sft','self_improvement')):continue
    path=getattr(module,'__file__',None)
    if path is None:continue
    actual=str(Path(path).resolve())
    if actual not in BINDINGS or hashlib.sha256(Path(actual).read_bytes()).hexdigest()!=BINDINGS[actual]:
        raise SystemExit('unbound production import: '+name)

fd=int(sys.argv[1]);log=sys.argv[2];arm=sys.argv[3];paths=json.loads(sys.argv[4]);mode=sys.argv[5]
previous=json.loads(sys.argv[6])
journal=ipc.Journal(log,1024*1024)
owner=ipc.EffectOwner(fd,journal,{'env_construct':1,'env_init':1,'reset':1,'model_load':1,'generation':2,'step':2})
controller=ipc.Controller(owner)
journal.emit('synthetic_input_paths',{'paths':paths})
journal.emit('synthetic_source_bindings',{'hashes':BINDINGS,'projection_module':projection.__module__,
  'public_state_module':PublicState.__module__,'parser_module':parse_p2_selection.__module__,
  'scope':'original functions, fake model/environment edges'})


class FakeEnvironment:
    def __init__(self):self.steps=0
    def initialize(self):return {'synthetic':True}
    def reset(self):
        state=PublicState('synthetic','synthetic','fictional goal',
          'different fake observation' if ((mode=='mismatch' and arm=='B') or (mode=='mismatch_A' and arm=='A')) else 'same fake observation',('fictional action',))
        native={'won_batch':[False],'won_batch_type':'tuple' if mode=='tuple' else 'list'}
        if arm=='B':
            if mode=='bad_true':native['won_batch']=[True]
            if mode=='bad_integer':native['won_batch']=[0]
            if mode=='bad_type':native['won_batch_type']='array'
            if mode=='bad_missing':native.pop('won_batch_type')
            if mode=='bad_extra':native['other']=False
            if mode=='bad_length':native['won_batch']=[False,False]
        return state,paths[0],{'candidate_native_reset':native}
    def step(self,action):
        if action!='fictional action':raise ValueError('unexpected fictional action')
        self.steps+=1
        done=self.steps==2
        return types.SimpleNamespace(observation='fictional completed' if done else 'first fictional observation',
          reward=1 if done else 0,done=done,truncated=False,valid_actions=('fictional action',),
          metadata={'alfworld_info':{'won':[done]},'candidate_native_done_batch':[done],
                    'candidate_native_won_batch':[done]})
    def close(self):pass

class FakeRow:
    def __init__(self,data):self.data=data
    def tolist(self):return list(self.data)
class FakeTensor:
    def __init__(self,data):self.data=data;self.shape=(1,len(data))
    def to(self,device):return self
    def __getitem__(self,key):
        if key!=0:raise IndexError()
        return FakeRow(self.data)
class FakeTokenizer:
    eos_token_id=151645;pad_token_id=151643
    def __call__(self,**kwargs):return {'input_ids':FakeTensor([4,5]),'attention_mask':FakeTensor([1,1])}
class FakeModel:
    device='fictional-cpu'
    generation_config=types.SimpleNamespace(to_dict=lambda:{'forced_eos_token_id':None,
        'eos_token_id':[151645,151643],'pad_token_id':151643})
    def eval(self):pass
    def parameters(self):return ()
    def generate(self,**kwargs):
        return types.SimpleNamespace(sequences=FakeTensor([4,5,99,151645]),scores=[None,None])
class FakeResource:
    def before_generation(self,*a,**kw):pass
    def after_generation(self,*a,**kw):pass
    def close(self):pass
class FakeProducer:
    def __init__(self):
        self.tokenizer=FakeTokenizer();self.model=FakeModel();self.eos_ids=[151645];self.arm=arm
        self.resource=FakeResource();self.torch=types.SimpleNamespace(cuda=types.SimpleNamespace(synchronize=lambda:None),no_grad=contextlib.nullcontext)
    def prepare(self,prompt):return {'prompt':prompt,'input_ids':[4,5],'attention_mask':[1,1],'rendered_prompt':'synthetic rendered prompt'}
    def decode(self,ids):return 'bad output' if mode=='bad_format' else 'A000'
    def verify_state(self):return 'fictional-state'
    def close(self):pass

def load_producer(_):
    if (mode=='interrupt' and arm=='A') or mode=='interrupt_any':os._exit(7)
    return FakeProducer()
def parse(raw,actions):return parse_p2_selection(raw,actions,reflection_required=False)
def state_factory(old,after):
    return PublicState(old.task_id,old.family,old.goal,after['observation'],tuple(after['valid_actions']),
                       after['done'],after['reward'],after['truncated'])
try:
    result=episode.run_episode(arm=arm,controller=controller,env_factory=FakeEnvironment,
       load_producer=load_producer,projection=projection,source_worker=source,parser=parse,
       parse_value=dataclasses.asdict,state_factory=state_factory,expected_game=paths[0],
       expected_eos=[151645,151643],expected_pad=151643,previous_initial=previous)
    journal.emit('synthetic_observed_episode_returned',{'result':result,'scope':'child claim; not scientific'})
    owner.finish('COMPLETED')
finally:
    owner.close();journal.close()
