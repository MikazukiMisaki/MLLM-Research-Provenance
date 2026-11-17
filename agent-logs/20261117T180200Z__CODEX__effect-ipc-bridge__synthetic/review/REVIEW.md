# Synthetic effect IPC bridge: independent review

Static review and one independent CPU execution of the author's fictional
subprocess test suite only. No real model, tokenizer, task, CUDA, environment
or scientific run was executed. No execution permission is implied.

Source hashes:

- Existing production `effect_ipc.py`: `046c0c48291efdae06457d87343d084357ae5a1774c3d670e3e232b15fd16dd8`.
- Candidate `bridge.py`: `8f24510def275bc78938d85fa2a3edb7018d98c3ad68c890d2d47c9f81637a7a`.
- Candidate `fake_client.py`: `ca8ce7d315aaa493e1600ae0162f070aa4177ab239863b7c0aeb5b34be29adaf`.
- Candidate `test_bridge.py`: `f44e85c8577a6ba3c95e3164aeab28a3969e7ff671d90f5a1d85a9071733f63d`.
- Candidate `production-source-binding.json`: `bb4222ffa1df4465220d1b5fc3207c2c511ab01e73b8c20ae5c0bf82b41048e0`.

The fake child verifies original `effect_ipc.py` source bytes against that
digest, compiles them, then instantiates its real `Journal`, `EffectOwner` and
`Controller`; its callbacks are fictional. `bridge.py:89–95` records/fsyncs a
shared parent reservation before sending ACK and before admitting another
reservation. `bridge.py:96–102` checks returned/unknown against the active
arm/sequence/operation, child journal chain and SHA of the entire final line
including newline. `bridge.py:103–117` requires both fictional operations
returned for each arm, and fails on unknown, disconnect or malformed messages;
an acknowledged-but-unreturned reservation remains charged/open.

One independent pinned-interpreter invocation of `python -m unittest -v
test_bridge` returned 0, **6 tests passed**. Raw `test-output.log` SHA256
`fd086a8dce33792d77da95b12b3f25d19e36c04ae37601059c02ea1eb5ca942e`.
Those tests cover two sequential real protocol clients and shared count,
disconnect after ACK, unknown effect, cap, order and malformed messages.
Already-queued frame detection is not proof against timing races.

Receipt checking verifies a child-generated journal claim, not physical work
or independent actor authenticity. The candidate lacks production actor and
worker integration, real manifest, public-state handshake, native success,
actual global scientific budgets/resource guard, signal and descendant
cleanup, and persistent crash recovery. It does not prove hidden-state
identity or complete physical-cost observation. Parent fsync failures can
leave disk and memory views divergent; preserve the ledger and reconcile.
