# Independent review: pair-owned real-interface candidate

Decision: **HOLD; not ready for scientific execution or production acceptance.** This review is limited to the frozen candidate and fictional CPU evidence, not the actual task pool or model/environment execution. The candidate's own HOLD is material and remains in force.

## Exact inputs and verification

Candidate directory: `/home/lizening/research-notes/agent-logs/20261118__CODEX__pair-owned-real-interface__private/`. Its `FILE_HASHES.sha256` SHA256 is `3311d3cfb671fe661db9df8a73b0be9eac452688d5635d892b9364596ad79f8a`; all 35 entries independently passed `sha256sum -c`. Complete output: `file-hashes-verification.log` alongside this file. The inventory checks file bytes, not scientific validity or integrity of external files omitted from the inventory.

Key file SHA256:

- README.md: `5865d90242d0835242b5ecd5b4c530ee58fa2a701de9490f6e2a1bd992526445`
- candidate-manifest.json: `a9662d89af5ebb9b47deda411d1d35a159dfa89dc4c12819130b7e80aaaf87f6`
- global_owner.py: `89286aea9dc3651f00db4ebc59f49fae42dbdf3760b537cd7ffc8ebef18c6a56`
- fake_worker.py: `dae168aac8e0d78cea40b1934d0a944ffdfa6f620c48de0a104f356a38099e36`
- test_candidate.py: `2a612f74b9e89ed0ecbe5bfcf3f14f6d0cabe3b2d00905383ad70259a7d83ae1`
- fixed_product_dev/worker.py: `867ba0b620b02d10269bd4c2c838f7dd8a9c9deec5ae8e74af565135bd50aa77`
- fixed_product_dev/arm_budget.py: `583bb81e202ad25d16863aba120d349f91c82bc5d8ee13925d9b89391bc55fae`
- fixed_product_dev/arm_stage.py: `d68653a6e8c80f148e414a9089c3d291c6c94580db938fc8a131013c933a050d`
- existing external effect_ipc.py: `046c0c48291efdae06457d87343d084357ae5a1774c3d670e3e232b15fd16dd8`
- existing external eprime_ports.py: `a1c5d80d58d0b4219ed813f7d61e30fe0e1a02ddca273f93b6734799e491e20e`

## Finding: incomplete prepared-context and generation-options binding

`global_owner.py:40–47` validates only selected keys in the child-claimed `kwargs` and no required `public` or `rendered_prompt`. Existing `fake_worker.py:39–43` itself sends this reduced prepared structure and the positive test accepts it. An independently written fictional journal using the existing production Journal was also accepted with `num_return_sequences=2`, no `public`, and no `rendered_prompt`. Reproduction `reproduce_incomplete_prepared.py` SHA256 `45472ee0e8983d20c116e946e475da3a96ff159b84902b1df8ae8fd86c33c994`; output `reproduce-output.log` SHA256 `226702a39c018e817af047e882f3c4868667db91c79ae716788f632581fb2dc5`. It does not run a generation; it establishes acceptance of this claim, not actual overspend or dishonest worker behavior.

The pre-ACK output reservation is 16 tokens per call. If an actual invocation used multiple returned sequences, a per-sequence `max_new_tokens` alone would not establish this total bound. A later receipt shape rejection cannot undo an already incurred effect. The candidate already discloses that trusted production worker identity is not bound and its actual worker is deliberately disabled; this reproduction identifies a specific validation gap that must be closed before any future release.

Smallest next change: bind the reviewed production worker and fixed producer options and strictly validate the complete expected generation kwargs, including a single return sequence, prior to ACK; bind and verify the public-state/prompt claim and its relationship to that fixed worker and the reserved step. Preserve the frozen producer semantics rather than silently changing its generation options. Add fictional CPU tests that reject missing context, extra/inconsistent kwargs, and multiple sequences before reservation/ACK. Child records remain claims, not independent physical proof; code/identity binding and real runtime/cleanup checks remain separate requirements.

## Reservation, matching, interruption, and HOLD

`fixed_product_dev/arm_budget.py:49–56,71` invokes the global reservation before building the ACK. `global_owner.py:135–147` reserves and synchronously writes the parent ledger entry before returning, with conservative 4096 input and 16 output tokens per generation; the record implementation fsyncs file and containing directory. These are **reserved maxima**, not independently measured physical tokens. Assertions depend on the trusted parent and successful I/O.

The parent compares generation prepared sequence/digest with the later child ledger and checks returned sequence equals input plus reported output, with claimed shape and output length (`global_owner.py:48–57,151–169`). The child journal chain and line hash support integrity/association within the claimed log; they do not authenticate the real worker or physical effect. A received `unknown` immediately fails stop (`arm_budget.py:57–60`) and the active reservation is not refunded. Incomplete EOF fails stop (`arm_budget.py:84–88`); the positive suite includes ACK-then-interrupt and verifies no refund. The received unknown receipt is not itself validated and recorded as a successful parent return; preserve the child log for later reconciliation. I did not independently demonstrate exhaustive crash or I/O failure behavior.

The schedule and parent counters exist in one owner object, but actual four-pair/eight-arm operation is not established: `worker.py:43–45` explicitly raises `RESEARCH_HOLD`, and `GlobalOwner.close_arm_after_cleanup` and `complete` unconditionally stop. The HOLD blocks the intended worker entry and batch completion, not arbitrary direct invocation of helper functions. Actual worker launch/identity, four-pair lifecycle, cleanup, native outcomes, physical token accounting, and complete runtime/resource controls are not integrated/proven here.

## Independent fictional CPU tests

Ran once in the pinned Python environment with bytecode writing disabled: `python -m unittest -v test_candidate`. Six tests passed; original output `test-output.log` SHA256 `1266d178e13850e209bef4832d96bce492f0f1ab296dbae2f159701e53046577`. Tests exercise actual StageBudgetChannel and source-bound IPC plus fictional files, callback, process and fake episode. They check missing/duplicate prepared, reset mismatch, changed input, interrupted generation with reserved cost, and worker HOLD. They do **not** run real producer `_generation`, real worker main as a successful worker, a real tokenizer/model/environment, native success, all four pairs, GPU, or actual cleanup. The additional independent malformed prepared claim above is not covered by those six tests.

No real task, model, GPU, environment, preflight, or science run was invoked, and no candidate code or old evidence was modified. This review grants no launch or scientific-execution clearance.
