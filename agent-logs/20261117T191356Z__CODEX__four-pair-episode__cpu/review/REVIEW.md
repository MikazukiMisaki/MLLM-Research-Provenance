# Independent review: pair-owned scheduler v4

Decision: **HOLD, software-only**. The four-pair fixture calls the fixed production episode, generation, parser, public-state projection and IPC functions, with fictional models, tokenizers, world, inputs and outcomes. It is not a scientific evaluation or a release of the real worker.

## Identity and checks

Candidate: `/home/lizening/research-notes/agent-logs/20261118__CODEX__pair-owned-scheduler-v4__private/`. `FILE_HASHES.sha256` SHA256 `8d9378f7cd8d2afaa5d99e997905785f771ec89747d99ed030d860ae37136f8d`: all 96 entries passed independently (`inventory.log`). All 24 `source-bindings.json` entries matched independently (`source-bindings.log`). Pinned-Python fictional CPU test suite: two tests passed, exit 0; independent raw `tests.log` SHA256 `5cba0fee6039dc021cc7b0580d6f6b8854d00d714c22afe4a595ad204b91eea7`.

Key file SHA256:

- `REPORT.md`: `2f09dcf803cb35b11710ce65584080b800a2d66d0a83995c813ad967dad8600b`
- `fake_worker.py`: `c90fbcdb09b11360e8d9c8ce9a4a974a48e19969cf2f69d166f793e74e354db9`
- `test_episode_scheduler.py`: `92c3c69bcecf5f78d5b7b66cbc39212cd519a984217636ecc732a08eaefae729`
- `global_owner.py`: `8d741f0e4c748d8ef24d16515a0c334392a3d37275e115a7db5bc1a0d0f9d9c6`
- `scheduler_synthetic.py`: `e3f2439b59195f7f5dd2d0caba24bbfe723b68bbdb38dc7fe99a750d0123a8fb`
- `process_guard.py`: `8e1ce0319ab0fe222d751ea332297da983c9ca3fe741ea58cbe858a2b25af1e4`
- candidate `fixed_product_dev/worker.py`: `867ba0b620b02d10269bd4c2c838f7dd8a9c9deec5ae8e74af565135bd50aa77`
- original `episode.py`: `06922aed662e84c1366624600c361f64ca7fba1ee93daccf83ff8de7a174a21b`; original `source_worker.py`: `36f4d2a4d82e5798a5d3fd786fa80505fe3c345ff7333aa8bdfaf52581a34111`; original `effect_ipc.py`: `046c0c48291efdae06457d87343d084357ae5a1774c3d670e3e232b15fd16dd8`.
- original parser `models/protocol_stability.py`: `d363677d90e247b15cccf68bdfdcaf3712d684567b8c167de266da2850ebb87d`; original state/projection `self_improvement/si_p3/contract.py`: `2d7b05d5c230cb45c2ad90c7507c11a5c76ce52f7335548c46a48d78e8842239`.

## Data flow and negative path

`fake_worker.py:17–67` hashes original source and checks parser and projection import origins. At `:123–133` the synthetic wrapper directly calls SHA-bound `episode.run_episode` with the real source `_generation`, parser and projection, original IPC and candidate stage channel. Actual producer/tokenizer/model/environment and terminal transition are fakes (`:77–121`). Source binds support byte-level function identity in this software fixture; child journals and synthetic terminal success are not physical or native-success proof.

The independently rerun positive test observes four pairs and eight arms, one fake construct/init/reset/model-load/generation/step each, four materializations, and 8 × 4096/16 reserved input/output tokens. Each pair has equal fictional public reset claims and distinct cases have different claims. Each of eight logs records prepared, parser, step and outcome events. The negative test changes the second arm's reset; it aborts with two reset reservations but only one model-load, generation and step reservation from the first arm. It does not roll back the incurred first-arm reservation or start later pairs. This is CPU fake-edge evidence, not runtime cost.

`global_owner.py` and candidate `arm_budget.py` preserve fsynced parent reservation before ACK, hash-bound prepared/return child claims, global/per-arm limits, fail-stop on UNKNOWN and no refund. They are not independent physical meters or a complete real time/device budget; signed/trusted worker and product identity and actual prompt/token inputs remain future work.

## Cleanup and remaining boundary

`scheduler_synthetic.py` and `process_guard.py` are byte-for-byte identical to reviewed v3. V4 tests did not rerun the v3 capture-failure scenario. The separate independent v3 replay at `/home/lizening/research-notes/agent-logs/20261118__REVIEW__pair_scheduler_v3__SQr1ec/REVIEW.md` used an actually live reviewer-owned fictional child: after identity capture failed and bounded wait timed out the parent wrote `UNKNOWN_DIRECT_CHILD_STILL_UNREAPED`, fail-stopped without signal, and returned while the child remained alive; the review harness then reaped its own child. The same code limitation remains. UNKNOWN is not cleanup; hidden or escaped descendants and GPU ownership are not proven.

No additional concrete defect was established within this focused review. Real production entry/worker, native success, actual manifest and product identity, wall-clock/device/resource accounting, physical outcomes and host-level cleanup remain unverified. Existing candidate `worker.py` retains unconditional `RESEARCH_HOLD`. No real task, model, GPU, ALFWorld, preflight or scientific experiment was run, and old evidence and developer files were not modified.
