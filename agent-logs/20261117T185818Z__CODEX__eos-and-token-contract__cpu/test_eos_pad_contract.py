"""CPU contract tests calling the original episode and generation functions.

All effects, tokenization, model and environment objects are fictional.
"""
import contextlib
import importlib.util
import types
import unittest
from pathlib import Path

ROOT = Path('/home/lizening/research-notes/agent-logs/20261118__CODEX__fixed_product_per_arm__private/runtime/fixed_product_dev')
SOURCE = Path('/home/lizening/research-notes/agent-logs/20261116__CODEX__two-object-paired-eval__candidate/gate-live/source_worker.py')

def import_path(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

episode = import_path('review_episode', ROOT / 'episode.py')
source = import_path('review_source', SOURCE)
EOS = 151645
PAD = 151643
EXPECTED = [EOS, PAD]

class Tensor:
    def __init__(self, values): self.values = values; self.shape = (1, len(values))
    def to(self, device): return self
    def __getitem__(self, index): return self
    def tolist(self): return self.values

class Tokenizer:
    def __init__(self, eos=EOS, pad=PAD): self.eos_token_id=eos; self.pad_token_id=pad
    def __call__(self, **kwargs):
        return {'input_ids':Tensor([8,9]), 'attention_mask':Tensor([1,1])}

class Model:
    device = 'fictional'
    def __init__(self, output):
        self.output=output
        self.generation_config=types.SimpleNamespace(to_dict=lambda:{'eos_token_id':EXPECTED,
            'pad_token_id':PAD, 'forced_eos_token_id':None})
    def eval(self): pass
    def parameters(self): return []
    def generate(self, **kwargs):
        return types.SimpleNamespace(sequences=Tensor([8,9]+self.output), scores=[0]*len(self.output))

class Resource:
    def before_generation(self, *args, **kwargs): pass
    def after_generation(self, *args, **kwargs): pass
    def close(self): pass

class Producer:
    def __init__(self, output, eos=EOS, pad=PAD):
        self.model=Model(output);self.tokenizer=Tokenizer(eos,pad);self.eos_ids=[eos]
        self.resource=Resource();self.arm='A'
        self.torch=types.SimpleNamespace(cuda=types.SimpleNamespace(synchronize=lambda:None),
                                        no_grad=contextlib.nullcontext)
    def prepare(self, prompt):
        return {'prompt':prompt,'rendered_prompt':'fake','input_ids':[8,9], 'attention_mask':[1,1]}
    def decode(self, ids): return 'not an action'
    def verify_state(self): return {'fictional':True}
    def close(self): pass

class Journal:
    def __init__(self): self.rows=[]
    def emit(self, kind, payload): self.rows.append((kind,payload))

class Controller:
    def __init__(self): self.journal=Journal();self.ops=[]
    def effect(self, kind, fn, convert):
        self.ops.append(kind); value=fn(); self.journal.emit(kind+'_returned',convert(value)); return value

class State:
    ended=False
    valid_actions=('fake action',)
    observation='fake observation'
    def to_dict(self): return {'observation':self.observation}

class Env:
    def initialize(self): pass
    def reset(self): return State(), 'fake-game', {'candidate_native_reset':{'won_batch':[False]}}
    def close(self): pass

def run_episode(producer, controller):
    return episode.run_episode(arm='P0',controller=controller,env_factory=Env,
        load_producer=lambda arm:producer,source_worker=source,
        projection=lambda state,history:{'public_prompt':'fake','action_map':{'A001':'fake action'}},
        parser=lambda raw,valid:{'selection_status':'action_format_violation'},
        parse_value=lambda value:value,state_factory=None,expected_game='fake-game',
        expected_eos=EXPECTED,expected_pad=PAD)

class EOSContract(unittest.TestCase):
    def test_distinct_primary_eos_and_pad_reaches_parser(self):
        controller=Controller(); result=run_episode(Producer([777,EOS]),controller)
        self.assertEqual((result['termination'],result['failure_reason']),('POLICY_FAILURE','UNSELECTED'))
        self.assertEqual(controller.ops.count('generation'),1)
        self.assertTrue(any(kind=='dev_parser_returned' for kind,_ in controller.journal.rows))

    def test_equal_primary_eos_and_pad_rejected_before_generation(self):
        controller=Controller()
        with self.assertRaisesRegex(ValueError,'tokenizer EOS/pad configuration incompatible'):
            run_episode(Producer([777,PAD],eos=PAD,pad=PAD),controller)
        self.assertNotIn('generation',controller.ops)

    def test_output_model_secondary_eos_equal_to_pad_is_policy_failure(self):
        controller=Controller(); result=run_episode(Producer([777,PAD]),controller)
        self.assertEqual((result['termination'],result['failure_reason']),('POLICY_FAILURE','OUTPUT_PADDING'))
        self.assertEqual(controller.ops.count('generation'),1)
        self.assertTrue(any(kind=='generation_returned' for kind,_ in controller.journal.rows))
        self.assertNotIn('step',controller.ops)

    def test_pad_before_final_primary_eos_is_earlier_eos_failure(self):
        controller=Controller(); result=run_episode(Producer([777,PAD,EOS]),controller)
        self.assertEqual((result['termination'],result['failure_reason']),('POLICY_FAILURE','EARLIER_EOS'))
        self.assertEqual(controller.ops.count('generation'),1)
        self.assertNotIn('step',controller.ops)

if __name__=='__main__': unittest.main()
