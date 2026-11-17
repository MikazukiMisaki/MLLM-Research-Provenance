# Combined synthetic pair: independent CPU review

This candidate is a one-pair synthetic test, not a scientific execution
system. Its original-port `eprime_ports.py` SHA256 is
`a1c5d80d58d0b4219ed813f7d61e30fe0e1a02ddca273f93b6734799e491e20e`
and original-client `effect_ipc.py` SHA256 is
`046c0c48291efdae06457d87343d084357ae5a1774c3d670e3e232b15fd16dd8`.
The former is executed with fabricated `CASES` and fake temporary inputs;
the latter is used with fake effect callbacks in separate child processes.

Candidate hashes: `bridge.py`
`9f9693bcf468fca526fd21f2481788c653bcbc297757494b631a9d64945c5573`;
`pair_synthetic.py`
`a983497d5ef7ab6e7d0fc1948131db91c398abdbe7fdeb06c8c795889cf143e4`;
`fake_arm.py`
`915bd30465441ea2699e5bf2e89789b108ab76f92e2d7c6e0127172b9bc3b01b`;
`test_pair.py`
`376cf812de3ecf0b4a44093eaab42fea492f289417e611b52a4e32d278c27334`.

The parent checks the full claimed reset-return line hash and worker chain,
extracts `payload.evidence.state`, checks its fake schema and compares states
before admitting the second model-load reservation. The 4 author tests were
independently executed once: 4 passed, exit 0. Raw `test-output.log` SHA256
`58d2d586062d79b0466b2ca358b3e0cc455d8abee2dcd187791576ce4ce71206`.
In the mismatch case B is started and reset, but no B model load is admitted;
on A interrupt or post-A file tampering B is not started, and the test checks
the aborted parent record and preservation of the outstanding reservation.

## Concrete reset-shape incompatibility

`bridge.py:146–151` requires `candidate_native_reset` equal exactly
`{'won_batch':[False]}`. The original `environment_step.py:30–42`, SHA256
`1c2df60c671ab408dfd5738192edd0371db848191a904c77e695dc250ff7b00e`,
constructs both `won_batch` **and** `won_batch_type`. The cited old episode
forwards that dictionary. Thus, if directly connected, even a valid reset
claim of the actual shape would be rejected before A model load.

The independent `reproduce_real_shape.py` changes only a **temporary copy**
of the fictional child to emit both fields. It uses fake inputs, fake state
and no-op operations. It reproducibly exits through `fake reset claim invalid`,
retains an aborted parent ledger, admits zero model loads and never starts B.
Script SHA256
`465aa7faed4a24b35e1860326fa4d2985bd7264ba527f80c698b5651dc461e74`;
`reproduce-output.log` SHA256
`1fef99538628b88ccc50b6734463df557dcebd49adb89877a89842bd21590e0a`.
The four author tests plus this reproduction use five materializations of
fictional files in this independent review; real scientific setups are zero.

All reset and outcome data here are child claims. A production worker,
verified native success, genuine scientific manifest and roster, model and
GPU binding, complete cumulative budget, signal/process-group cleanup and
independent physical-cost proof remain absent. No experiment is authorized
by this result.
