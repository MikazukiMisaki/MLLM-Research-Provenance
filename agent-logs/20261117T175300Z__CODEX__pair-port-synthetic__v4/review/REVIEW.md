# Independent v4 synthetic port review

This review exercises only fictional temporary files and child processes. It
does not access actual task inputs, model, tokenizer, CUDA or ALFWorld, and is
not a scientific execution authorization.

Source SHA256 values independently checked:

- Existing `eprime_ports.py`: `a1c5d80d58d0b4219ed813f7d61e30fe0e1a02ddca273f93b6734799e491e20e`.
- v4 `production_adapter.py`: `39b9eb9085d76b6e21c7b539944f2e74ca660128f625be5afaf00a193cf8976d`.
- v4 `test_production_adapter.py`: `b73d30b330cf043ae185dea3f27b4baf17c9009180a00a181ef0de947739d6c9`.
- v4 `candidate.py`: `73d7cecfb0700963214d4b86649597442e7f5d4e9da3b521d25063d4ba864488`.
- v4 `production_source_binding.json`: `3b10dc9ead2402d9b41637866f2aa3ac62f2d06e555330bb4893878bce195830`.

The adapter reads and hashes original port source bytes before compiling them,
while substituting a deliberately fictional `forward_specs.CASES`. The real
case registry and real tasks are not tested. This is evidence of source-level
port compatibility for the synthetic inputs, not real run readiness.

The four-pair/eight-arm test asserts four original materializer calls, sixteen
pre/post verifier calls and identical per-pair paths. A separate tamper test
calls the original materializer once more and rejects changed synthetic bytes.
Hence **five synthetic materializations in this independent test invocation**;
scientific materializations are zero. Other tests reject a wrong source digest
and a fixture outside its temporary root. The tests cannot establish semantic
correctness or actual environment feasibility.

Independent pinned-interpreter run of `python -m unittest -v test_candidate
test_production_adapter` returned exit code 0, 19 tests passed. The raw output
is `test-output.log`, SHA256
`59caa4444b9d7be41971d6273e8dc379de24f48510b0a43b342f309545d6804f`.

The synthetic owner wire format still differs from the production EffectOwner
protocol; there is no production IPC bridge, actor integration, native won
validation or scientific budget/resource supervisor. Process cleanup, hidden
state equivalence and secure runtime isolation are not established. This review
does not accept or authorize real execution.
