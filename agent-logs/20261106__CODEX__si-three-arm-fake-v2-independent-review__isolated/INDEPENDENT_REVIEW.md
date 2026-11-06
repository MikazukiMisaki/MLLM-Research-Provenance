# Independent exact-byte review — three-arm fake acceptance v2

Disposition: PASS for the three requested fixes and retained behavior within this synthetic, single-process scope, with one low-severity test-entrypoint finding below. This does not authorize real execution or establish causal treatment efficacy, durable provenance, model/environment compatibility, hardware readiness, independent tasks, or complete cost accounting.

## Independent reproduction

- Actual received fake input shape `(1, 4097)` was rejected before the relevant `GEN_START` and before the fake model callback in each of P0, B-stage-1, B-stage-2, C-stage-1, C-stage-2. Every fake backend accepted actual shape `(1, 4096)` in a complete synthetic path. A separate class-level FakeInput-shape patch reproduced the first-generation stop. Tokenizer/template/transfer work before the model guard was not zeroed; this does not test real tokenizer IDs or tensor/backend behavior.
- Twelve separately constructed Study objects raced the same explicit registry/group: one completed, 11 were refused without events. After an injected failure at the first fake raw-return event, the group remained consumed, a fresh Study was refused and did not generate. This is in-memory same-registry behavior only; it is not cross-process, crash-persistent, same-user-adversarial or independently controlled custody.
- Returned nested maps/tuples resisted assignment and remained unchanged after mutation of internal fake ledger/source/result objects. This proves detachment for tested JSON-compatible fake results, not append-only records or a security boundary.
- Actual imported local module origins and the 16 pinned source byte hashes matched in this run; candidate tests include fake changed-origin, changed-bytes and unlisted-module negative checks. The pin is not the entire interpreter, native dependency or future-import closure and cannot eliminate TOCTOU.
- Existing tests exercised actual local SFTP0QwenPolicy.act / P2 parser and actual TwoStageRecoveryV2Operator.act / inherited generation wrapper and V2 parsers using fake edges, while forbidding real Qwen load. They cover source replay, A/B/C paths, P0 cap 16, recovery caps 40/16, invalid-first still calling stage 2, frozen two control placeholders, validity marker, map mismatch and fake fault stops. Fake outputs and per-arm replay do not demonstrate real cache separation or scientific task independence.

Re-ran the documented module-discovery command `PYTHONDONTWRITEBYTECODE=1 python -B -m unittest -v test_three_arm_fake`: 24 tests passed. Six additional independent fake-only adversarial tests passed. Candidate SHA256SUMS verified before and after; all 16 selected production source pins matched. The candidate itself was not edited. No real model/tokenizer/ALFWorld/GPU/protected task was invoked or read.

## Low-severity test-entrypoint finding

`test_three_arm_fake.py:100` calls unittest.main before `AcceptanceGaps` is defined at line 102. Directly executing `python -B test_three_arm_fake.py` therefore reports success after only 13 tests, silently omitting the 11 added acceptance tests. Independently reproduced in `direct_script_test.log`; this does not invalidate the documented module-discovery 24-test run, which includes both classes. Any downstream report must specify the command and 24-test count; move unittest.main below all test classes in a future candidate to remove the trap, followed by exact-byte re-review.

All effects are fake. Actual cost, error handling, external watchdog, physical generation/step ledger, and trustworthy custody remain separate tasks; no complete outcome/benefit claim follows from this review.
