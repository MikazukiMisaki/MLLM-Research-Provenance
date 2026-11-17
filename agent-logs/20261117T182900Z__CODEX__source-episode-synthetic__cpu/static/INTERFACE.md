# Production episode with synthetic edges: static integration guidance

Static code review only. No actual task content, model, tokenizer, environment
or GPU was accessed, and no experimental job was started. The following paths
are existing code, not a newly approved experiment.

## Source hashes

| Source | SHA256 |
|---|---|
| `fixed_product_dev/episode.py` | `06922aed662e84c1366624600c361f64ca7fba1ee93daccf83ff8de7a174a21b` |
| `fixed_product_dev/worker.py` | `1f2dadcf27530438e20ed96ab04f0fb7e6a7492662650008a7fefc098140e4fb` |
| `gate-live/source_worker.py` | `36f4d2a4d82e5798a5d3fd786fa80505fe3c345ff7333aa8bdfaf52581a34111` |
| `gate-live/effect_ipc.py` | `046c0c48291efdae06457d87343d084357ae5a1774c3d670e3e232b15fd16dd8` |
| `src/models/protocol_stability.py` | `d363677d90e247b15cccf68bdfdcaf3712d684567b8c167de266da2850ebb87d` |
| `src/models/action_parser.py` | `0a1c668d590980d1d8cdd4104a2b3c9aa851037fc238a2c73c45b57ab4432fbe` |
| `src/self_improvement/si_p3/contract.py` | `2d7b05d5c230cb45c2ad90c7507c11a5c76ce52f7335548c46a48d78e8842239` |

`fixed_product_dev` is
`/home/lizening/research-notes/agent-logs/20261118__CODEX__fixed_product_per_arm__private/runtime/fixed_product_dev`;
`gate-live` is
`/home/lizening/research-notes/agent-logs/20261116__CODEX__two-object-paired-eval__candidate/gate-live`;
the `src` root is `/home/lizening/.codex/worktrees/parallel-goal-runtime-9dd`.

## Real functions and boundaries

Call the original `run_episode(*, arm, controller, env_factory, load_producer,
source_worker, projection, parser, parse_value, state_factory, expected_game,
expected_eos, expected_pad, previous_initial=None)` and the real
`source_worker._generation(producer, public, controller, expected_eos,
expected_pad)`. The real worker adapts the real parser as
`parse_p2_selection(raw, actions, reflection_required=False)` and converts its
`P2Selection` dataclass with `dataclasses.asdict` (`worker.py:142–158`). A fake
parser does not test this interface. Using the real projection and action map
adds confidence that ordered current actions and the parser agree.

Use explicitly fictional state, environment transition, model generation,
tokenizer/tensors, resource and clock boundaries; never attribute their
fabricated results to ALFWorld or a real model. If the real Controller,
EffectOwner and Journal are part of the integration, bind their real IPC
protocol and an appropriately scoped fake parent; otherwise state clearly
that controller/IPC coverage is mocked. Do not infer production device or
physical-cost evidence from either case.

## Parser and mapping

`action_id_mapping` enumerates ordered actions **from zero**: first `A000`,
second `A001`. `parse_p2_selection` strips lines, takes the final nonempty
line, requires a bare `A` plus exactly three digits, then maps that ID to the
current valid tuple. Earlier nonempty lines are treated as reflection text;
do not silently substitute a different one-line parser. A selected ID must map
to the exact current action and selected index. In the real episode, malformed
or out-of-range selection and missing primary EOS are policy failures; unknown
selection statuses, mapping inconsistency and other technical exceptions
stop. The empty-action-map parser case needs a direct parser unit test because
the episode rejects empty/duplicate mappings before invoking the parser.

## Generation boundary

The fake producer must implement `prepare`, tokenizer IDs/call, `eos_ids`,
`model.generation_config.to_dict`, model `eval`, `parameters`, `generate`,
`torch.no_grad` and `torch.cuda.synchronize` as harmless fake objects,
`resource` hooks, `verify_state`, `decode`, and cleanup. Returned fake tensors
must support shape `[1,n]`, indexing, `tolist`, and `.to`; input IDs/mask
must match the prepared values. The production `_generation` bounds input at
4096 and output at 16, checks batch/prefix/scores, fixed effective EOS list,
tokenizer primary EOS and pad, and writes generation receipt before later EOS
classification. Keep primary EOS distinct from PAD and make a valid positive
fixture end in primary EOS. The separate issue where an allowed secondary
model stop ID equals PAD remains subject to its existing adjudication; do not
quietly change or relabel this behavior in a synthetic test.

## Reset, step and outcome

A realistic fake reset returns `(state, expected_game,
{'candidate_native_reset': {'won_batch':[False], 'won_batch_type':'list'}})`
or the `'tuple'` origin label, with a state exposing `to_dict`, `ended`,
`observation` and ordered `valid_actions` tuple. `previous_initial` is checked
before model load. For a fake transition, supply nonempty observation, finite
reward, real boolean `done` and `truncated`, tuple/None valid actions, and
metadata with `alfworld_info.won=[bool]`,
`candidate_native_done_batch=[bool]`, `candidate_native_won_batch=[bool]`;
the latter two must agree with the normalized fields checked by the real
`source_worker._transition_wire`. A positive fixture can emit `A000`, return a
fake `done=True, won=True` transition, and assert the exact command supplied
to the fake environment plus the real terminal result and journal sequence.
Test malformed ID, out-of-range ID, inconsistent native/normalized booleans,
truncation and reset mismatch separately. Keep a policy-format failure with
zero steps distinct from a technical UNKNOWN; do not fabricate a native result.

Passing these tests would demonstrate only the specific source interfaces
under fictional boundaries. It would not establish genuine task semantics,
native success, reproducible GPU identity, physical costs or scientific
evidence and would not authorize an actual run.
