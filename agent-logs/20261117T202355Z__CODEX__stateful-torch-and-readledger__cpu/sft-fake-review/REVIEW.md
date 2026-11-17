# Independent review: stateful fictional SFT candidate

**PASS for the scoped fictional Python core and separate CPU reference tests; real trainer integration and scientific execution remain HOLD.** The PyTorch test does not execute the candidate's Python training core; it validates a separately implemented small CPU mathematical pattern.

## Exact evidence

Candidate `/home/lizening/research-notes/agent-logs/20261118__CODEX__si-stateful-fake-sft__private/`: all 15 inventory files and all three referenced source hashes independently matched. `FILE_HASHES.sha256` SHA256 `09a7598cb625dee079646821149b882b36d8f3d63841c24457ec7d3b89e448c5`; `fake_stateful_sft.py` `836684a16de9e3c4ff0344c05f7394e1903cf4155980a269063db22d25eb5e36`; fixed fictional `fixture.json` `768fc562e2d32681d13fe8738c4a4804e7b3c0a191d26fd0a634b375102cb3d5`; `test_fake_stateful_sft.py` `5d1e662a4747e926441951a2948f42bdd22a5246ef077014727f2b3c559e1877`; `test_torch_cpu_state.py` `236c9b1ca8ae59e9fc2cddc9ba814c8527aebe19b7c75431471a3c99434647d0`.

Independent pinned-Python tests: 3/3 fake-core tests, `fake-tests.log` SHA256 `27ae8f8a2c9c8035407ac1452f05cce67642e592862e969e99e7ff2242c72b5e`; and 1/1 separate PyTorch CPU test, `torch-tests.log` SHA256 `f3e7a8a7a82a4bdceb1d33b6b22797d59aaae87aa4d4876fd0029a8f2cb6f8b9`. The latter ran with `CUDA_VISIBLE_DEVICES=''`, asserts CPU tensor/optimizer state, and the reviewer wrapper reports `CUDA_INITIALIZED False`. Only fictional rows and self-initialized tiny CPU parameters were used.

## Core and its limits

`fake_stateful_sft.py:33–64` constructs one fake model and one fake Adam, traverses 16 fixed rows in fixed order over four epochs, groups four rows per update, and records 64 fictional microbatches / 16 updates. The tests check optimizer moment/step continuity, mask/label arrays, order and final-only checkpoint, and independently calculate the first batch's loss and first-moment gradient. Code uses `labels[j+1]` and divides the summed gradient by total active completion targets across four rows, corresponding to the causal shift and token-total loss form of the existing native one-step function. This fake's position-independent logits and Python floats cannot establish numerical, parameter, optimizer implementation or performance equivalence to a transformer, Qwen/LoRA, or GPU.

The separate `test_torch_cpu_state.py` creates its own `torch.nn.Linear` and its own loop/AdamW, and calls only the candidate's fictional row validator, **not** `run_fake_fixture`. For that separately implemented loop, all 16 accumulated-vs-aggregate shifted cross-entropy gradient comparisons pass, the same CPU model and AdamW object persist, and optimizer steps progress to 16. It is meaningful reference-pattern evidence, not execution of a production or PyTorch-backed candidate core or an end-to-end adapter test.

`run_fake_fixture` only accepts the fixed fictional fixture hash; `run_training` unconditionally raises RESEARCH_HOLD. No model/optimizer state, pretrained adapter, trainer artifact, original source trajectory, physical cost or native outcome has been proven. Actual authenticated data resolver, exact trainer token/mask transformation and P0 identity, real model/optimizer/checkpoint lifecycle, full budget and independent integration review are still needed. This narrowly scoped review grants no actual training or experiment clearance.
