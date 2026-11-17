# Effect IPC bridge v2: independent CPU review

The candidate is a synthetic protocol fragment, not a production execution
gate or authorization. This review invoked only the author's fictional
subprocesses and no-op callbacks: no real tasks, models, tokenizer, GPU or
environment.

Independently checked source SHA256:

- Original `effect_ipc.py`: `046c0c48291efdae06457d87343d084357ae5a1774c3d670e3e232b15fd16dd8`.
- v2 `bridge.py`: `eeca56dfea03068c15b9512f07fbe90fd48a95d4799fb585aacf2b2c5d1b4dfa`.
- v2 `fake_client.py`: `8ef38efb36e4262de1932e8538398b759833a4dbfa50aee321dcabe4b67c37a1`.
- v2 `test_bridge.py`: `8a7679199bf159f7c6ded163e8b13287feaeb75a386182956c5d3b453cc7625c`.

The fake subprocess verifies, compiles and instantiates the original Journal,
EffectOwner and Controller; its operations are no-op fixtures. The pinned
interpreter independently ran the author's suite once: **12 passed, exit 0**.
Raw `test-output.log` SHA256
`b97c83cd6a438c4126d643af0d107041c813f14af781842a0670e6aa7cd615fc`.

The tested cases cover parent-enforced per-arm caps independent of child caps;
refusal to alter an existing ledger with no claim; fail-stop and retained
reservation after injected `SystemExit`; acknowledgement after forced
one-byte sends; valid non-effect journal lines between started and returned;
and rejection of missing, duplicated or mismatched effect lifecycle events.
The tests also cover disconnect after ACK, unknown effect, aggregate cap,
arm order and malformed protocol. These are fixture observations and do not
establish fault handling for all kernel errors or process races.

An important correction: original v1 `bridge.py:112` already used
`sock.sendall`. There is no demonstrated v1 single-write short-ACK defect.
The v2 explicit loop is a newly testable implementation choice.

Production actor/worker/manifest and first-reset comparison, real native
outcomes, four-pair scientific budget, live GPU/resource supervision, robust
signals/descendant cleanup and authentic physical-cost proof remain unconnected.
Child-generated hash-chain receipts support claims, not independent evidence
that the physical effect occurred. No real-run permission follows.
