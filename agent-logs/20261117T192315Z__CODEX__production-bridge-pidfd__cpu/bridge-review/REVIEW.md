# Independent review: fictional parent / worker-CLI bridge

**HOLD; budget sufficiency NOT_VERIFIED.** The fixture demonstrates a CLI-shaped connection to a fake child and does not execute the production worker main. No new real scientific execution path was established in this focused review; the public Python fixture API itself is not a security sandbox.

## Exact candidate and tests

Candidate `/home/lizening/research-notes/agent-logs/20261118__CODEX__pair-owned-production-bridge__private/`; `FILE_HASHES.sha256` SHA256 `e75260b82ca733b958cfcfe44172e3ac5150f3b351a4456ab4079b412a0c3667`. Independently verified all 179 entries, raw `inventory.log` SHA256 `80dc4303bdc1812d06eb5383b2b66ba2c70cb1e2a3f495031593d1120880af33`. Key hashes: `bridge.py` `388953870b46a4c12b106d6063a5819c6e4dbf4dcdbca813135712cb4bf4379b`; `fake_cli_worker.py` `2870bd5bcaa881a71f5f3213081aae7b5c74602a3bc399c131434ca8c4dd8558`; `test_bridge.py` `0ec1b57d8d164e37baaa192026a8d65cbdffe97256e8276c77e111a4e0557677`; `fixed_product_dev/worker.py` `867ba0b620b02d10269bd4c2c838f7dd8a9c9deec5ae8e74af565135bd50aa77`; `static_adapter.py` `66a1de9889e4446084630ffd0c55387e3d459ab4290f7f7cf63482f466e09753`.

Independently reran two tests with pinned Python and fictional inputs only, exit 0; raw `tests.log` SHA256 `102db5961f9135a3c284591699d425a98cb8d4872259eb9863324e2ec3570c7c`. Positive test used 4 pairs and 8 fake subprocesses; negative test reset mismatch stopped before the second model-load reservation, retaining the first fictional arm's generation/step reservation. No real task/model/GPU/environment/preflight was invoked.

## Actual data path and HOLD

`bridge.py:21–23,62–70` builds a fictional config and starts its fixed `fake_cli_worker.py` with worker-style `--config`, `--config-sha256`, `--budget-fd` and passed socket. The fake child calls the held worker's actual `read_bound` for config/manifest (`fake_cli_worker.py:74–84`) and then the candidate StageBudgetChannel plus original SHA-bound episode, generation, parser, projection and IPC with a fake tokenizer/model/world (`:87–145`). Its config includes `synthetic_test_context`. The held worker's **main**, and therefore its own complete config validation, source/product load and runtime path, are not exercised by this test.

`bridge.launch_production` unconditionally raises (`bridge.py:115–116`) and `fixed_product_dev/worker.py:43–45` independently raises at the start of `main`. The reviewed explicit subprocess command names only the fake child. This is an application-level HOLD, not a sandbox: `run_synthetic_bridge` accepts arbitrary caller-supplied Python `materialize` and `verify` callbacks, which could themselves have arbitrary side effects. It must not be presented as proving that an untrusted same-UID caller cannot perform real operations by other means.

## Costs and remaining work

The parent writes `synthetic_scope` with actual historical budget UNKNOWN and budget sufficiency NOT_VERIFIED (`bridge.py:25`); its product paths, balances, effects and terminal outcomes are fabricated (`:29–37`, fake child). Eight reserved generations and steps are test ledger events, not physical cost. Parent reservations use the existing fsync-before-ACK candidate global owner. The static adapter's previously independently reproduced all-zero proposed-additions acceptance remains unchanged; therefore arithmetic consistency does not prove adequate real budget. Neither fabricated allowances nor runtime record may be added to or replace prior physical cost.

The v3/v4 direct-child cleanup UNKNOWN limitation persists; pidfd-owner v2 is not integrated. A capture failure may leave a live child, and an UNKNOWN or direct-child reap does not prove descendants, host process state or GPU cleanup. There is no authenticated real product/source/manifest/ledger binding, real parent-worker integration, full physical token/time/device budget, genuine native-success verification, nor exact launch authorization here. This review grants no experiment clearance and did not edit developer code or earlier evidence.
