# Original source episode with fictional boundaries: independent review

The candidate is a synthetic contract test, not a scientific experiment or
permission to execute one. I independently checked all twelve source entries in
`production-source-hashes.json`; all matched their current bytes. The source
manifest SHA256 is
`afafd0ad2b55adca9f99d5cdbeb00ba2b409bb2dec86818bcf3bc12900af932d`.

Key exact source/origin bindings:

| Source | SHA256 |
|---|---|
| `fixed_product_dev/episode.py` | `06922aed662e84c1366624600c361f64ca7fba1ee93daccf83ff8de7a174a21b` |
| `gate-live/source_worker.py` | `36f4d2a4d82e5798a5d3fd786fa80505fe3c345ff7333aa8bdfaf52581a34111` |
| `gate-live/effect_ipc.py` | `046c0c48291efdae06457d87343d084357ae5a1774c3d670e3e232b15fd16dd8` |
| `gate-live/eprime_ports.py` | `a1c5d80d58d0b4219ed813f7d61e30fe0e1a02ddca273f93b6734799e491e20e` |
| `src/models/protocol_stability.py` | `d363677d90e247b15cccf68bdfdcaf3712d684567b8c167de266da2850ebb87d` |
| `src/models/action_parser.py` | `0a1c668d590980d1d8cdd4104a2b3c9aa851037fc238a2c73c45b57ab4432fbe` |

`fixed_product_dev` is
`/home/lizening/research-notes/agent-logs/20261118__CODEX__fixed_product_per_arm__private/runtime/fixed_product_dev`;
`gate-live` is
`/home/lizening/research-notes/agent-logs/20261116__CODEX__two-object-paired-eval__candidate/gate-live`;
`src` is `/home/lizening/.codex/worktrees/parallel-goal-runtime-9dd/src`.

Candidate `fake_arm.py` SHA256
`416683be34fc7521f2805c6a49f6371137a608bf07a2b4acf0e96da37aed4acf`;
`test_pair.py` SHA256
`2ccd4b478d9b17a125e5c4993bf96089fbdabcbcd1b0401bad5ba1878e701caf`.
The fake child checks and executes original source bytes for episode,
generation/transition and IPC; it imports the actual P2 parser and checks its
resolved module origin. The exercised parser, episode, generation and
transition functions are not substituted. Task file bytes, registry, model,
tokenizer, tensors, CUDA methods, environment, state, resources and projection
are synthetic; a real Qwen model and ALFWorld are not instantiated.

Independent pinned-interpreter `python -m unittest -v test_pair` ran once:
**8 tests passed, exit 0**. Raw `test-output.log` SHA256
`a2c75cb78c84645885b782396f2980c9dd83765b9ed1326e2920e3641537f21d`.
Positive assertions show selected `A000`; the fictional environment accepts
only its matching command, then supplies a fake terminal success after one
step. Bad format reaches the real parser and produces a fake zero-step policy
failure. The tests exercise retained reservation, malformed reset and
post-arm fake-file tampering.

For the B mismatch negative, B has already supplied a reset receipt; the
synthetic parent rejects that claim before ACK/model-load reservation. Thus
the original episode's own **later B local comparison is not reached** in
that negative case. In the positive path B receives the first claimed state
and proceeds through the original comparison. Claims in child records do not
prove native state, independent physical effects or hidden-state equality.

Real production worker and StageBudgetChannel, real projection, genuine task
roster and manifest, native outcome, model identity, GPU and full scientific
budgets/resource cleanup remain unconnected and unverified. A fake terminal
success is not an ALFWorld success or a research result. No real task, model,
environment or GPU was accessed in this review.
