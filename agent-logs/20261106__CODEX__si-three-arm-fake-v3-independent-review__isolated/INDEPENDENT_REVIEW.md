# Independent exact-byte review: three-arm fake v3

Disposition: PASS for the synthetic test-entrypoint correction only. No real execution or scientific claim is authorized by this review.

Compared v3 to independently reviewed v2: `three_arm_fake.py`, `core_v2.py`, and `PINNED_SOURCE_SHA256.txt` are byte-identical. The complete `test_three_arm_fake.py` diff removes `unittest.main` from before `AcceptanceGaps` and places it after all test classes, with no other test changes. The v3 source diff was independently checked. Candidate SHA256SUMS passed before and after testing and all 16 selected production-source pins matched locally; this does not authenticate the full runtime.

Independent runs, all fake/temp only, actual exit status 0 (saved separately):

- Documented module discovery: 24 tests passed (`module.log`).
- Direct test-file entrypoint: 24 tests passed (`direct.log`), correcting v2's silent 13-test execution.
- Six independent v2 adversarial checks, with only the import path changed to v3: 6 passed (`adversarial.log`). These test 4096/4097 actual fake input, first-call class-level oversize injection, a 12-object shared-registry race, same-group refusal after a fake raw-return failure, and detached nested snapshots.

The fake fixture calls selected pinned production P0/recovery/parser code using synthetic fake model, tokenizer and environment interfaces; it is not the production backend or a real task. A local in-memory registry is not durable or cross-process. No actual model/tokenizer weights, GPU, ALFWorld environment, protected data, research inference, or training was invoked in this review. Scientific validity, full runtime/custody, physical cost accounting, task independence and real execution remain separate requirements.
