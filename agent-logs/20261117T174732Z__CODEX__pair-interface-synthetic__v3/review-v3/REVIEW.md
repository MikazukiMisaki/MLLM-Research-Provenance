# Pair-interface v3 independent CPU re-review

The candidate is synthetic and has not been authorized or verified for
production. Exact source hashes: `candidate.py`
`73d7cecfb0700963214d4b86649597442e7f5d4e9da3b521d25063d4ba864488`,
`fake_arm.py` `1b18ccc38ea7c4c77232e410e2be5ad70d2cb4049a563f5809281e008c224f13`,
and `test_candidate.py` `ddfeb3d165a3acc775d32fa2a0c9e7580a486927067cb32a0fea6ba104103e1a`.

The pinned interpreter independently ran all 15 existing fake-interface tests:
15 passed. Raw `suite-output.log` SHA256
`3134a54d54d73d56f112af1952960245f8bb56315ac3e19d13afa1fdad2b9607`.

Independent `replay.py` SHA256
`d263125e82d3e4284fd7a2c78acbaf61acd9273c956a1af63a8a15b26375ad03`
and its raw `replay-output.log` SHA256
`6216539771e79b6bace6e011487c23d26ad7c32d8693465e6b8f1d57d5202844`
show the following:

- Starting the fictional fourth case first or reversing the first case's arm
  order each failed with zero setup calls, zero materialization reservations,
  and an owner latched failed.
- The correct first case/order used exactly one fake setup and advanced to
  the second case's reversed order.
- A mismatched second initial state in the fourth pair stopped with seven
  closed arms, seven model-load reservations and batch completion refused.

At `candidate.py:231`, the schedule test precedes directory creation and
materialization reservation. The schedule is fictional code constants, not
an authenticated scientific roster or real product binding. Production
materialization, actor, IPC, native success, resource/time/token controls and
cleanup remain unconnected. The tests used only fictional subprocesses and
temporary inputs; no real task, model, GPU or ALFWorld was invoked.
