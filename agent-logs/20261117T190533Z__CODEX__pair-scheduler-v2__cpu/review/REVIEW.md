# Independent review: pair-owned synthetic scheduler v2

Decision: HOLD. The v1 multiple-output prepared-claim flaw is fixed at this synthetic validator boundary, but an independently reproduced spawn/identity-failure cleanup gap remains. This does not authorize production or scientific execution.

## Frozen candidate and tests

`/home/lizening/research-notes/agent-logs/20261118__CODEX__pair-owned-scheduler-v2__private/` inventory SHA256 `36ba6a6b596f6b11c0d17f0cedfca6e419fed880836f01c745194a2d24107321`: 105/105 entries verified; full independent output `inventory-check.log` in this review directory. Key SHA256:

- `global_owner.py`: `edc8763a7ac64c6f873849f048fb819fabdd24c35c23628fd28868fe12f024b0`
- `scheduler_synthetic.py`: `c7f03a41909444725b434c0e29a2296d8e426f092ad7c73ab459403898d1a453`
- `process_guard.py`: `8e1ce0319ab0fe222d751ea332297da983c9ca3fe741ea58cbe858a2b25af1e4`
- `fake_worker.py`: `fd6b530bd102f72c41a63de1b845a256830d36fea9ad29bcc542f0f02d36ad8f`
- `test_scheduler.py`: `6e14520ef137e452722c5fe632193cd680f37852bf28f1cc18871809a02c0f9f`
- `fixed_product_dev/worker.py`: `867ba0b620b02d10269bd4c2c838f7dd8a9c9deec5ae8e74af565135bd50aa77`
- `fixed_product_dev/arm_budget.py`: `583bb81e202ad25d16863aba120d349f91c82bc5d8ee13925d9b89391bc55fae`

Independently ran the three CPU fictional tests once; all passed. `tests.log` is retained here. All tests and reproduced children were fictional; no real task, tokenizer, model, CUDA, ALFWorld, or scientific batch executed.

## New observed cleanup defect

`scheduler_synthetic.py:32–40` calls `Popen` then `capture_owned(proc)`. If identity capture throws after the child exists, `ident` is still `None`; the exception branch at `:57–67` attempts cleanup only when both `proc` and `ident` are non-None. Thus fail-stop is recorded but a live direct child may survive. Actual procfs read failure/identity uncertainty can exercise that path; the defect is not a claim that the synthetic candidate ran a real worker. It is distinct from intentionally declining to signal an unverified PID.

I injected capture failure into an isolated synthetic run whose replacement process was a reviewer-owned `sleep`-like Python child. After the scheduler raised, the Popen child was observed alive; the review harness then explicitly terminated and reaped that exact child. Reproduction `reproduce_capture_failure.py` SHA256 `417d4bcfefdc21221520e8330ce69763a906494eb2e5a19caf927c46efc15a89`; output `reproduce_capture_failure.log` SHA256 `9b9f8f0c32057858d16bbe7127da59b393f329d78358a0b71424db1745cc44ae`.

Before adapting for real workers, introduce a reliable own-child spawn/identity-capture failure strategy, with independent ownership and race safety, explicit durable cleanup/unknown evidence, and fault-injection coverage. Do not signal arbitrary PIDs or process groups merely to hide uncertainty. The existing current-procfs observation cannot prove absence of escaped or host-hidden descendants or GPU use.

## Findings on requested invariants

- `global_owner.py:42–47` canonical-compares the full six expected kwargs, including `num_return_sequences=1`, matching the fixed `source_worker.KWARGS`; changed/missing/extra values are refused. The fictional test independently rerun explicitly rejects `num_return_sequences=2`, omitted public, and wrong public-prompt hash. This closes the earlier exact validator reproducer, not the larger physical actor/producer trust boundary. Child-reported rendered prompt and IDs are not independently retokenized or established to be the values actually used.
- One global owner enforces four pair materializations, eight per-arm reset/model-load maxima, 400 generation and step maxima, and per-arm maxima of 50 each; each generation reserves 4096 input and 16 output units, no refunds. The reserve record is fsynced before StageBudgetChannel can send ACK. These are conservative reservations, not measured consumption or a full wall-time/GPU/physical resource budget.
- Each new pair clears/rebinds the first reset state (`global_owner.py:113–118,223–225`); a second reset must match the first within the same case before model-load admission (`:146–148,182–199`). Claims are child-supplied; fake states differ across cases. The test demonstrates four fictional pairs, alternated order, eight isolated fake workers, 4/8/8/8/8/8 setup/construct/init/reset/load/generation and zero steps, 32768/128 reserved input/output. This is not scientific evidence.
- `arm_budget.py:49–60,71` orders reserve before ACK and stops on an `unknown` receipt; unfinished EOF stops and previously reserved amounts remain charged. The independent suite tests timeout after three fictional generations and no subsequent pair or refund. Not all crash, persistence or I/O fault cases were tested.
- Normal fake direct-child completion is checked by `process_guard.py` with a process identity and a current-procfs group scan; timeout only signals the verified own direct child. Its scope excludes escaped/host-hidden processes and GPU ownership. The capture-failure defect above remains.
- The candidate `worker.py` remains explicitly hard-held; `scheduler_synthetic.py` invokes only `fake_worker.py`. Real `_generation`, production worker, tokenizer, actual task manifest and environment, native outcome, physical budgets and full cleanup are not integrated/proved. The synthetic complete marker does not grant experimental clearance.

No developer candidate files or previous evidence were modified.
