# Independent read-only review: saved-state tokenizer check

Status `SAVED_SELF_AUTHORED_STATE_TOKENIZATION_PASS`; `MODEL_INPUT_TENSOR_EQUIVALENCE_NOT_EVALUATED`. This review did not rerun the tokenizer, model, GPU or environment and did not alter original evidence. The input was the previously saved, partially captured state from one actual self-authored direct-engine reset; it was not a historical or held-out task sample.

The worker journal records one local tokenizer load, one chat-template render with tokenization disabled and one explicit encoding, each with started and returned events, followed by worker completion. The saved direct child return code is 0, no timeout or supervisor exception was reported, and the original process group was not observed at the post-run check. The outer shell exit file also records 0; it is not a separately supervised OS-level outer-process receipt. The original stdout digest equals both the worker-completed digest and the supervisor terminal digest; the stderr digest also matches. The output reports 189 input token IDs, six public actions and empty history.

An independent stdlib-only verifier rebuilt the frozen P0 prompt from the saved feedback, extracted normalized goal and six-action mapping and recomputed the prompt SHA256; it matches the recorded prompt. It verified the seven worker-event and four supervisor-event sequences, output-digest bindings and all 22 explicitly fixed own-input, project-source and tokenizer-file hashes against current bytes. It also checked that the recorded ID list contains 189 nonnegative integers. No task text, action commands, file paths or historical planning constants are reproduced in this report or verification JSON. These checks do not prove a complete transitive/native file-access trace or prevent undetected change-and-revert between checks.

The actual encoding used the tokenizer's ordinary list result, with `return_tensors=None`. It has **not** established equality with a future production policy's actual `return_tensors='pt'` input tensor, nor with any output from a real model. Future model-facing code must check the IDs actually consumed by that model before treating this count as a bound or binding. The recorded ID-list hash below uses compact JSON array encoding, and is not a hash of a tensor representation. Direct-engine feedback is not established equivalent to the full ALFWorld wrapper.

The worker source and journal show no intentional model weight/adapter loading, model generation or environment construct/reset/step during this check; its output reports the corresponding counters as zero. GPU visibility was empty and Python reported no torch module imported. No native or descendant activity trace was collected, so neither complete absence of all CUDA API activity nor absence of unjournaled filesystem/process effects is independently proved. The saved initial state itself came from the earlier one-reset run and its cost is not zero or repeated here.

The supervisor recorded approximately 1.629 seconds elapsed, 1.564 child CPU seconds and 209,052 KiB `RUSAGE_CHILDREN` maximum RSS. These are recorded direct-child observations, not an aggregate whole-process-tree resource guarantee or GPU accounting. Original stderr states that PyTorch, TensorFlow and Flax were unavailable to the isolated tokenizer process; this is retained as original evidence and is not a model-quality result. The original output contains machine-specific paths and self-authored action descriptions; retain its bytes locally and independently review/redact before any remote publication.

Independent verification JSON SHA256 `926c0cb4f5c7dfbd3bbfafacf639a0a13a0df8ce7e3dbcf565c2a4504880724f`; verification source SHA256 `49847f7ca1cf505189b9429d8fd834e4e84a6d8abf262632f3c67d3ed667dd49`; verification exit file SHA256 `9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa` records 0. The verification source is local because it names the exact reviewed files; the JSON and this summary contain no machine-specific paths.

Key SHA256:

- Worker source: `16173544d3cb7e48ee2bba1752d9baee3421225dd808de093a54ba114d7965fc`
- Supervisor source: `07f2dfe63c5dd06bef2090b76fd376fffbee906dec9ccef766d2d28c3dff1c27`
- Original stdout: `477bcf2d8fed543dc3d4504730517ec27eeda84874bc29ccf89078014fbc383c`
- Original stderr: `2d056a402d36c0559e8176f3048ad5de7f1c8cc6a83cd0416e91573be6e2ac50`
- Worker events: `48a3cabfda686529a19913fce172f4bec09eb725dcc619dfb24f7f33d469d002`
- Supervisor events: `efe9594dde3d8c67ba986b3276fb74820f671e107b8c6626c92023d601708a77`
- Reconstructed prompt: `c385b6adb69ca7fe41bd5fb21d7f15d810cd9e76896bb673225d2959012a2af8`
- Rendered prompt as reported by the worker: `6cfc92d3f531055b1dfe813af92511c12839b3bf95dff4d007af012fc51096ea`
- Compact JSON encoding of the 189 reported IDs: `7acecef6b70248d0c98480bd5c10443eafcff01609ca2d308ccb6dbad418a604`

The previously documented review-time accidental display of historical planning constants remains a separate provenance incident; those values and any historical task contents are not included here.
