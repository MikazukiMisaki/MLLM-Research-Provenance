# Pair-owned materialization: isolated production-interface candidate

Status: **interface candidate only; NO production acceptance or launch authorization**. No real materialization, model, GPU, ALFWorld or old batch was invoked. Tests use invented files and child processes exclusively. A four-materialization cap here is a candidate budget for a future proposal, not unused balance from the prior budget; historical six materializations remain charged.

## Candidate implementation

- `candidate.pair` accepts the existing production materializer signature `setup(output, inputs, journal, family='two')` and verifier signature `verify(game, config, dataset, inputs, journal, phase)` as injected callables. It calls setup once per pair and passes identical absolute returned paths to two separate injected child processes. This is **signature-level compatibility only**: neither real production function has been imported, connected or run here.
- The same owner retains a durable exclusive no-resume claim and fsyncs chained global reservations before each setup or child effect. It enforces 4 setup, 8 construction/init/reset/load, 400 generation and 400 step global caps and 1/1/1/1/50/50 local per-arm caps. An unfinished reservation continues to consume budget; an existing claim cannot be restarted. Record ambiguity stops this instance.
- The parent sends a budget reply to each child's JSON-lines requests and stores return receipts; children do not grant themselves budget. Verification and materialized-file/path fingerprints run before and after each arm; second public initial state must equal the first before the second child can request a model load. If an arm exits or fails with a reserved operation, no second attempt is made. The first arm's observed result is recorded even if later checks fail; it is not automatically accepted as a valid scientific result.
- `fake_arm.py` supplies test-only made-up operations and fake observations, and is not a scientific actor or environment. All setup fixtures are invented and do not use real task assets.

## What is explicitly not implemented or proven

1. **No production integration** with real `materialize`, `verify_materialized`, actual actor, production `EffectOwner`/`Controller`, ALFWorld or supervisor. The adapter, exact method binding, real owned-process launch and production event-journal integration must be designed, implemented and independently reviewed; matching a Python signature alone does not establish compatibility.
2. Token-level ceilings, pair/batch wall-clock budget, model identity/hash enforcement, output roster accounting, actual ALFWorld native success, EOS/PAD correction, worker receipt authentication and production process-resource admission are not implemented. The socket read timeout is a test safeguard, not the research wall budget. No observations here support scientific efficacy.
3. Files are checked for path containment, symlinks, file shape and pre/between/post hashes. These checks are not kernel-enforced isolation and cannot prove absence of transient changes or TOCTOU races. The candidate does not prove the real environment can operate on read-only inputs.
4. On a failure it requests termination of its directly owned synthetic child; reliable process-group/subreaper cleanup, asynchronous interrupt handling and crash recovery are not implemented. Unresolved state must stop, remain accounted and be reconciled offline; never resume or retry under the same allowance. A producer could violate the test protocol or emit misleading synthetic receipts. Per-arm budgets are parent-controlled, but this is not evidence of production enforcement.
5. A hash-chain check alone cannot authenticate logs against a malicious same-UID writer; no persistent-ledger transaction or cross-host lock is asserted. Immutable retained evidence and an independently verified resource/execution gate remain needed before any future study.

## Validation

`python -m unittest -v test_candidate`: 6 passed, actual exit code 0, as recorded in `test-output.log` and `test-receipt.json`. Tests check four setups/eight fictional children with identical pair paths, mismatch before second-arm model-load request, retained incomplete generation reservation, post-arm input drift, per-arm duplicate limits, and truncated ledger. They use no real model/environment/asset and cannot support a readiness claim.

Exact hashes are listed in `FILE_HASHES.sha256`; its own checksum is delivered in the handoff. The earlier `budget_prototype_base.py` is retained as an unused reference copy and is not imported by this candidate.
