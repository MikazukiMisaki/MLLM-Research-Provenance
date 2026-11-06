# Independent read-only review of tiny PEFT CPU integration result

Status: `SYNTHETIC_CPU_INTERFACE_CHECK_PASS`; `SCIENTIFIC_EFFECT_NOT_EVALUATED`. This review read the original launcher receipt, stdout/stderr, operation and guard journals, the launcher claim and relevant source bytes. It did not re-execute the check or modify original evidence.

The authentic launcher receipt reports direct subprocess return code 0, no timeout and `own_process_group_not_observed`. Its recorded child-before and child-after SHA256 both match the independently rehashed reviewed child, and its launcher hash matches the independently rehashed reviewed launcher. Its stdout and stderr SHA256s match the bytes independently rehashed. The recorded elapsed interval is 4.2312 seconds, with direct-child usage record approximately 3.724 user plus 0.404 system CPU seconds and max RSS 581,140 KiB. These are launcher observations, not a whole-process-tree, device allocation or full resource audit.

The operation journal records started and returned pairs for two tiny model constructions, one synthetic LoRA attachment and adapter save, one synthetic PEFT load and one policy call. Inside that policy call the guard journal contains exactly one `claimed`, `started`, `returned` sequence: three input token IDs `[1,5,6]`, four output IDs `[22,48,33,50]`, `max_new_tokens=4`. The claim and event order agree with the reviewed trusted call path. This establishes one recorded tiny synthetic generation through that guarded path, not globally enforced absence of every possible untraced call.

The stdout/operation result records a 4,480-parameter in-code random model, a fake tokenizer and no research-model, research-adapter or environment calls; the reviewed source is consistent with that scope. CUDA initialized was reported false at the end and the launcher bound empty `CUDA_VISIBLE_DEVICES`; this does not prove no native CUDA API or external access occurred, because no full native-access trace was collected. The real research model, its tokenizer, its adapter and ALFWorld were not validated by this check.

The fake decoder rendered the random IDs as `T22 T48 T33 T50`. The referenced production `parse_p2_selection` requires the final nonempty line to match a bare action ID of the form `A` followed by exactly three digits; the reported `action_format_violation` is consistent with that output. The test did not execute an environment action. This format violation is expected to be possible for an untrained random tiny network with a fake decoder and says nothing about the real P0 model's format compliance or success rate; the test's PASS concerns the specified PEFT/cache/guard pipeline, not successful action selection.

The original stderr contains a PEFT warning that a config file was not found and vocabulary modification would be assumed absent. The synthetic save/load events returned; this warning remains part of the evidence and does not verify vocabulary compatibility of a real model or adapter. The launcher reports `untraced_native_access=true` and `global_retry_control=false`; no claim of complete native access monitoring, secure sandboxing, global one-shot enforcement, escaped-descendant cleanup or crash-proof durability is made. Not all transitive Python code and libraries were hash-bound. A local source and operation log includes machine-specific paths; preserve original bytes locally and use reviewed/redacted material for any remote publication.

Independent SHA256:

- `launcher_receipt.json`: `0b96efb9658375d42679ed248d53ae1dd8b355fbe1f1cca69f5b3f5b234ff66e`
- `stdout.log`: `6f4b2e4469dbd2e0c53ba19c3ce4b6041632f17ab388666ad694e6fa68003f83`
- `stderr.log`: `a6dad3b1365eca2600baf18172b24415c4acb3da63d7e851bf7d1733fe6d0ef1`
- `execution/operations.jsonl`: `9c27f0d6484a87246ed12c43397366f6005c5c39d2a7ad44b8a910e6690665e0`
- `execution/guard/generation_events.jsonl`: `edaed3236c26cee05e0b4d67a4baf71f62e33446d2c82793c9493a8740d10f4c`
- `launcher.py`: `030d1bad688e337abee509972790438cfa2bc950497e0947b6be6e12688ed396`
- `tiny_peft_test.py`: `99112a654a789af8e57fda802e8261f14c2821432e85628f66103397bd42082c`

The current hashes of the four individually bound production/guard files matched the expected hashes in the reviewed child source. The initial and final observation of launcher bytes are recorded, but not an independent kernel-level measurement of every byte executed in between.
