# Independent review: pair-owned scheduler v3

**HOLD; synthetic candidate only.** The SHA-bound real `_generation` is exercised with fictional boundaries in each of eight fake arms, but the production worker and episode and physical runtime are not integrated. The old v2 capture-failure issue is now explicitly observed and classified; it is not fully cleaned up when identity is unavailable.

## Exact bytes and independently run checks

Candidate `/home/lizening/research-notes/agent-logs/20261118__CODEX__pair-owned-scheduler-v3__private/`: inventory `FILE_HASHES.sha256` SHA256 `c43f0084645a827c884b4c3cc980de628572f15383665e487935d4e35ed524d5`; independently checked all **205/205** listed entries, recorded in `inventory.log`. All entries in `source-bindings.json` also matched independently; see `source-bindings.log`.

Key SHA256: `REPORT.md` `9db3ea1a7efdc01942dc72add4ab7ab3ae2def80de2d4247cf2d629eb130a2e2`; `global_owner.py` `8d741f0e4c748d8ef24d16515a0c334392a3d37275e115a7db5bc1a0d0f9d9c6`; `scheduler_synthetic.py` `e3f2439b59195f7f5dd2d0caba24bbfe723b68bbdb38dc7fe99a750d0123a8fb`; `fake_worker.py` `ba90afe5b86416f5d05fdd72145481e2b1743b160bbb827b7b41cfc0f414a56b`; `test_scheduler.py` `5455d3bfe845e1f681f6ced0c9a70cf05738218654d6157cf72d3da45ccc0cc7`; `process_guard.py` `8e1ce0319ab0fe222d751ea332297da983c9ca3fe741ea58cbe858a2b25af1e4`; `fixed_product_dev/worker.py` `867ba0b620b02d10269bd4c2c838f7dd8a9c9deec5ae8e74af565135bd50aa77`; original `source_worker.py` `36f4d2a4d82e5798a5d3fd786fa80505fe3c345ff7333aa8bdfaf52581a34111`.

Independent CPU-only test run: 6 tests passed, exit 0; raw `tests.log` SHA256 `7ae7e74fae02d4794a55729f7f24ef55ed2fadf926be94a9ecd23a13973c15f2`. It used only fictional inputs and subprocesses.

## Real function versus fake edges

`fake_worker.py:20–23,74–98` verifies and imports the exact original source bytes then directly calls its `_generation` function; each of the eight fictional arms takes that path. Its tokenizer, producer/model, CUDA-like methods, reset, environment, episode and outcomes are deliberately fake. Tests establish the candidate data flow, not that a real worker physically uses the claimed prompts or tokens, or the native task outcome. The positive fixture has four pairs/eight fake workers, one generation per arm and no actions; it does not exercise 50-step real episodes.

`global_owner.py:37–75` requires exact field sets, types and all six frozen kwargs (including `num_return_sequences=1`), with prompt/action-map claims and hashes. The bad-kwargs test changes the emitted fictional prepared claim to two sequences and confirms denial before generation reserve; normal arms use the original producer routine. The trusted worker, actual tokenizer-to-prompt relationship, loaded runtime generation config and worker identity are not independently proven by the child journal. Real config including forced EOS remains unobserved.

## Budgets and persistence

`global_owner.py:101–116,155–176` appends and fsyncs the parent event and directory before returning from reservation, which `arm_budget.py:49–56,71` does before scheduling ACK. It has global fictional operation limits and charges 4096 input/16 output reserved per generation, no refund, while enforcing per-arm limits. These values are reservations under the trusted-child assumption, not independently measured physical model tokens. UNKNOWN and unfinished EOF cause fail-stop, retaining the reservation. Actual GPU, time, model identity and end-to-end scientific budget need independent implementation and review.

The existing positive fiction tests four materializations, eight model-load and generation claims and four pairs; initial reset claims agree within each pair and vary across pairs. It does not prove hidden state equality or native success. The fake scheduler uses original IPC plus synthetic materialization and one durable global ledger.

## Capture failure: observed UNKNOWN, not cleanup

`scheduler_synthetic.py:61–72` now closes its local socket endpoints, performs a bounded three-second wait on the Popen direct child, records an explicit reaped or `UNKNOWN_DIRECT_CHILD_STILL_UNREAPED` classification where writable, sends no unverified signal, and stops. A reaped direct child also leaves descendants/host GPU unknown. On ledger write failure, even durable classification is unproven.

Beyond the author's forced wait-proxy case, I injected a failed capture with an actual reviewer-owned fictional process sleeping 20 seconds. The parent's real three-second `wait` timed out; it durably recorded UNKNOWN, sent no signal, aborted, and the direct child was **still alive** when the scheduler returned. Review harness then terminated and reaped that exact child. Script `reproduce_unknown_live.py` SHA256 `22a704f83f5d779dcd47cca54acc84c7292ff5718c647bcbacf03bda8ff9930f`; output `reproduce_unknown_live.log` SHA256 `3bc4d14e70091223e1724cd012a37e58fc2b21c06f97885de3e20b85a4348320`.

This corrects the v2 silent/nonrecorded cleanup path, but does **not** make an uncooperative child disappear or prove cleanup. Before any real use, supply a race-safe, verifiable ownership/cleanup strategy and demonstrate its failure cases without signaling arbitrary processes. Current procfs cannot prove absence of host-hidden or escaped descendants or GPU activity.

`fixed_product_dev/worker.py` remains hard-held; no real runner, production episode/native predicate, exact product/task identity, complete real resource controls, or robust cleanup is established. No developer code or old evidence was altered; no model, real task, GPU, environment, preflight or science execution occurred during review. No launch clearance is granted.
