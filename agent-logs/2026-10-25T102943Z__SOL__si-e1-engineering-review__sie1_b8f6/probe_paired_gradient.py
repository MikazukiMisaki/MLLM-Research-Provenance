"""CPU token fixtures plus real controller/optimizer; not P0 or scientific training."""
from pathlib import Path
import math
import sys
import json
import copy
import tempfile
from types import SimpleNamespace
import torch
import torch.nn.functional as F
from self_improvement.si_p3.data import Example, CompletionCollator, fixed_schedule, audit_exposure
from self_improvement.si_p3.contract import FAMILIES, BACKGROUND_QUOTAS, ADOPTION_QUOTAS, ContractError
from self_improvement.si_p3.continuation import Final18Controller
from self_improvement.si_p3.evidence import Budget

assert str(Path.cwd()).startswith('/tmp/si-e1-independent-review-')
torch.set_num_threads(1)
order = fixed_schedule()
first_update = order[0][:16]
short = set(first_update[:8])
families = [f for f in FAMILIES for _ in range(BACKGROUND_QUOTAS[f])]
families += [f for f in FAMILIES for _ in range(ADOPTION_QUOTAS[f])]
pairs = []
for i, family in enumerate(families):
    n = 2 if i in short or (i not in first_update and i % 2 == 0) else 6
    target = (2,) * (n - 1) + (1,)  # final true EOS=PAD; positional masking
    ids = (2 if n == 2 else 3, 3, 3) + target
    def example(arm):
        role = 'background' if i < 120 else 'new'
        task = family + '-SYNTHETIC-' + role + '-' + (str(i) if i < 120 else arm + str(i)) + '/trial-SYNTHETIC'
        return Example(task, family, 'explicit synthetic token fixture', 'synthetic', 'A000', 'synthetic command',
                       'synthetic-' + str(i), role, ids, (-100,) * 3 + target, 3)
    b = example('B')
    pairs.append((b, b if i < 120 else example('C')))
collator = CompletionCollator(1)
exposure = audit_exposure(pairs, collator)
assert len(exposure['microbatch_loss_tokens']) == 144 and len(exposure['update_loss_tokens']) == 18
assert exposure['update_loss_tokens'][0] == [64, 64]
swapped = copy.copy(pairs)
s = next(i for i in range(120, 144) if pairs[i][0].loss_tokens == 2)
l = next(i for i in range(120, 144) if pairs[i][0].loss_tokens == 6)
swapped[s] = (pairs[l][0], pairs[s][1])
swapped[l] = (pairs[s][0], pairs[l][1])
assert sum(b.loss_tokens for b, c in swapped) == sum(b.loss_tokens for b, c in pairs)
try:
    audit_exposure(swapped, collator)
except ContractError:
    pass
else:
    raise AssertionError('equal global totals hid a slotwise length swap')

class ToyLogits(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.lora_logits = torch.nn.Parameter(torch.zeros(4))
        self.config = SimpleNamespace(vocab_size=4, model_type='si_e1_cpu_toy', _name_or_path='synthetic', use_cache=False)
    def forward(self, input_ids, attention_mask):
        logits = self.lora_logits[None, None, :].expand(*input_ids.shape, 4).clone()
        mask = input_ids[:, 0] == 2
        logits[mask, :, 0] -= 1e9
        logits[mask, :, 3] -= 1e9
        return SimpleNamespace(logits=logits)

model = ToyLogits()
reference = ToyLogits()
all_examples = [pairs[i][0] for i in first_update]
batch = collator(all_examples)
labels = batch['labels'][:, 1:].contiguous()
logits = reference(**{k: batch[k] for k in ('input_ids', 'attention_mask')}).logits[:, :-1, :].contiguous()
reference_loss = F.cross_entropy(logits.reshape(-1, 4), labels.reshape(-1), ignore_index=-100, reduction='sum') / 64
expected_loss = (16 * math.log(2) + 48 * math.log(4)) / 64
assert math.isclose(reference_loss.item(), expected_loss, rel_tol=1e-6)
reference_loss.backward()
torch.nn.utils.clip_grad_norm_(reference.parameters(), 1.0)
expected_gradient = reference.lora_logits.grad.detach().clone()
directory = Path(tempfile.mkdtemp(prefix='si-e1-gradient-software-')) / 'output'
controller = Final18Controller(model, pairs, collator, directory, arm='B', evidence_class='cpu_toy_software')
captured = []
original_step = controller.optimizer.step
def observe_step(*args, **kwargs):
    captured.append(model.lora_logits.grad.detach().clone())
    return original_step(*args, **kwargs)  # do execute the genuine AdamW update
controller.optimizer.step = observe_step
rows = [controller.consume(micro) for micro in controller.microbatches[:8]]
assert all(r['update_loss_token_denominator'] == 64 for r in rows)
assert controller.updates == 1 and len(captured) == 1
assert torch.allclose(captured[0], expected_gradient, atol=1e-7, rtol=1e-6)
observed_loss = sum(r['loss_sum'] for r in rows) / 64
assert math.isclose(observed_loss, expected_loss, rel_tol=1e-6)
try:
    controller.finish()
except ContractError:
    pass
else:
    raise AssertionError('partial update accepted as final18')

budget = Budget()
budget.reserve('complete', input_tokens=8192, output_cap=16)
budget.complete('complete', actual_output=16)
budget.reserve('unknown', input_tokens=8192, output_cap=16)
budget.stop()
cost = budget.snapshot()
assert cost['completed']['generations'] == 1 and cost['completed']['input_tokens'] == 8192
assert cost['reserved_or_spent']['generations'] == 2 and cost['open_units'] == ['unknown']
assert cost['reserved_or_spent']['input_tokens'] == 16384 and cost['reserved_or_spent']['generated_tokens'] == 32
for tokens, allowed in ((2, True), (3, False)):
    b = Budget(); b.used['input_tokens'] = 15999998  # explicit prior-spend fixture, no actual call
    try:
        b.reserve('boundary', input_tokens=tokens, output_cap=16)
    except ContractError:
        assert not allowed
    else:
        assert allowed
print(json.dumps({'status': 'PASS_INDEPENDENT_HETEROGENEOUS_TOKEN_GRADIENT_AND_RESERVATION_PROBES',
                  'paired_microbatches': 144, 'updates_in_exposure_schedule': 18,
                  'first_update_examples': 16, 'short_long_rows': [8, 8], 'short_long_target_tokens': [2, 6],
                  'first_update_loss_denominator': 64, 'expected_loss': expected_loss, 'observed_loss': observed_loss,
                  'gradient_matches_single_concatenated_reference': True, 'global_total_preserving_slot_swap_rejected': True,
                  'unknown_output_retains_16_token_reservation_not_actual_zero': cost,
                  'input_16M_exact_boundary_and_overflow': True,
                  'activity': {'tiny_CPU_model_objects': 2, 'actual_toy_optimizer_updates': 1,
                               'actual_8B_P0_models': 0, 'ALFWorld_calls': 0, 'scientific_training': 0},
                  'limit': 'Explicit token/logit fixtures, not actual tokenizer or admissible training data; genuine PEFT roundtrip checked separately in full suite.'}, indent=2))
