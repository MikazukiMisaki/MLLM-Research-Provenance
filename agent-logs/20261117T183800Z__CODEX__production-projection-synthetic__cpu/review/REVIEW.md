# Real public projection with fictional boundaries: independent review

This review runs only synthetic subprocesses and fabricated temporary task
files; no actual task, model, tokenizer, GPU or environment is invoked. It
is not a scientific result or experiment authorization.

Independently verified all 21 source entries in the candidate's
`production-source-hashes.json`, SHA256
`b2a505d1ab31d0a5fcb4b344a641ec0fc4f18817c20d0ca4892a20cd76684760`.
The relevant original sources include:

| Source | SHA256 |
|---|---|
| `fixed_product_dev/episode.py` | `06922aed662e84c1366624600c361f64ca7fba1ee93daccf83ff8de7a174a21b` |
| `gate-live/source_worker.py` | `36f4d2a4d82e5798a5d3fd786fa80505fe3c345ff7333aa8bdfaf52581a34111` |
| `gate-live/effect_ipc.py` | `046c0c48291efdae06457d87343d084357ae5a1774c3d670e3e232b15fd16dd8` |
| `src/models/protocol_stability.py` | `d363677d90e247b15cccf68bdfdcaf3712d684567b8c167de266da2850ebb87d` |
| `src/models/action_parser.py` | `0a1c668d590980d1d8cdd4104a2b3c9aa851037fc238a2c73c45b57ab4432fbe` |
| `src/self_improvement/si_p3/contract.py` | `2d7b05d5c230cb45c2ad90c7507c11a5c76ce52f7335548c46a48d78e8842239` |
| `src/sft/protocol.py` | `cb9a8ee23d1208064348810ef3580773ba14403bfaac6a4e7f4a43c5540178a8` |

`fixed_product_dev` is under
`/home/lizening/research-notes/agent-logs/20261118__CODEX__fixed_product_per_arm__private/runtime/fixed_product_dev`;
`gate-live` is
`/home/lizening/research-notes/agent-logs/20261116__CODEX__two-object-paired-eval__candidate/gate-live`;
`src` is `/home/lizening/.codex/worktrees/parallel-goal-runtime-9dd/src`.

Candidate `fake_arm.py` SHA256
`b6a3a6279c927ec23a0b9102a11e4a88c66938ed0f20ddac1076671fac5344d6`;
`test_pair.py` SHA256
`0dbc095d3d592f5bea7137dda51e5da6128dece60f78f617865fe7982fdda2b1`.
The fake child executes source-checked original episode, generation/transition
and IPC functions; it imports the real parser and PublicState/projection,
checks their origin and loaded project-module hashes, and exercises the
imported prompt renderer and action map. These functions are not mocked.
Registry and task bytes, model, tokenizer, tensors, CUDA interface, environment,
reset/step, resource hooks and resulting terminal observations are fictional.

Independent pinned-interpreter `python -m unittest -v test_pair` ran once:
**8 tests passed, exit 0**. Raw `test-output.log` SHA256
`dc4405750bf55dc4d013037aebde0df00dffa7add7a6753c51efa9aeb9134372`.
The positive test asserts action map `A000 -> fictional action`, selected real
parser output, two-step fake terminal, first empty history and second history
containing the prior observation/action with the new current observation.
Bad-format output produces a real parser format failure and zero fake steps.

In the second-arm mismatch negative, B's fake reset receipt is received and
rejected by the parent before B model-load reservation; it does not reach the
later original B episode's local `previous_initial` comparison. The child
reset and outcome remain claims, not native evidence or hidden-state proof.

The production worker/StageBudgetChannel, real task roster, authentic actor
and native success, GPU resource admission, complete four-pair/global cost and
wall/token budgets, and robust process/descendant cleanup are not integrated.
These tests establish only the specified software behavior under fake inputs.
