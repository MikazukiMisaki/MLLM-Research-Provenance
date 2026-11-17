# Prepared claim contract: isolated CPU candidate

Status **HOLD**: this is a software validation candidate, not a launchable or scientifically reviewed experiment. Copied source from `20261118__CODEX__pair-owned-real-interface__private` into this separate directory; no existing source/evidence was edited. Worker main's `RESEARCH_HOLD` is unchanged. Actual worker/source/process identity, physical effects, authenticity of prompt and environment, scheduler, process cleanup, device admission, runtime EOS and token cost all remain unproved.

`global_owner.patch` is the narrowly scoped candidate delta: require all seven actual `prepared` fields; validate public field types, action map and prompt digest; rendered prompt, token IDs and mask; exact all six source KWARGS with exact Python types (`num_return_sequences=1` included); config/EOS shape and values; and bind public, prompt, rendered prompt, input IDs, mask, kwargs, config and EOS SHA-256s to the same fsynced generation reservation. Hashes bind child claims only, not the true prompt, true model, or actual external calls. No inference/verification of semantically correct prompt rendering is claimed. Comparison of kwargs is order independent.

`fake_worker.py` checks and executes the actual frozen source_worker.py bytes SHA256 `36f4d2a4d82e5798a5d3fd786fa80505fe3c345ff7333aa8bdfaf52581a34111`, invokes its genuine `_generation`, real existing EffectOwner/Controller/Journal and StageBudgetChannel, and emits the original genuine prepared structure before going through the candidate global owner. Producer, tensor, tokenizer, model, CUDA synchronization, task, environment and outputs are fictional: no torch import, CUDA device, real model or ALFWorld is used. Test-only wrapper mutates prepared rows for negative cases; it is not proposed as production source.

Positive independent fake subprocess: 1 genuine `_generation` prepared claim accepted and reserved with the expected prompt/input hashes; fictional result returned; previous stage caps and hard HOLD remain. Negative cases exercise `num_return_sequences=2`, type substitutions including bool/int equality traps, other KWARGS changes, missing/extra fields, bad prompt hash, action mapping, eos, mask and missing rendered prompt. Global IPC negatives demonstrate malformed public/kwargs are rejected before generation reservation; separate claim unit mutations also fail. Missing/duplicate prepared and interrupted-after-ACK reservation remain covered.

Reproduction from this directory (pinned Python; `-I` means the test directory must be explicitly added):

```
/home/lizening/miniconda3/envs/alfworld-self-improve/bin/python -I -B -c 'import sys,unittest;sys.path.insert(0,".");unittest.main(module="test_candidate",verbosity=2)'
```

Observed `test_final.log`: **7 tests passed, exit 0**. The first attempted invocation incorrectly used `-I -m unittest` without adding the test path, so it failed before tests were imported; `test_initial.log` preserves that failure. `test_second.log` records the intermediate passing suite. No full pipeline or real task was run.

| File | SHA256 |
|---|---|
| `global_owner.py` | `3c44c65b00efe1800d9a091c5928a7b1df9979fcdfbf147b1fc2ab3ed9399ebd` |
| `global_owner.patch` | `bb52a1ea3945c4378a0e925002aaed638c5ffc7d91dac2fc016a7a420cb8fb19` |
| `fake_worker.py` | `2bb3735ec37773b0c3f4001fa7c22bb2f5bae7ff864987c4ba403a58d7bcaabc` |
| `test_candidate.py` | `36b8a0e929cca6fc0bd68dcde86f16e0f954acccbef566c57c5ddb759499a278` |
| `test_final.log` | `05910f4e90a4085b06833f9b8a05bc17e0a17b3d1a7860a559937bdb5a20502c` |
| unchanged `fixed_product_dev/worker.py` | `867ba0b620b02d10269bd4c2c838f7dd8a9c9deec5ae8e74af565135bd50aa77` |
