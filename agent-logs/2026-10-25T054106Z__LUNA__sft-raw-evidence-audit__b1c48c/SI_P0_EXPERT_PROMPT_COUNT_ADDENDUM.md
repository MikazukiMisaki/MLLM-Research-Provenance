# SI-P0 expert-prompt count addendum

Status: read-only reconciliation. This is an additive note; the original SI-P0 report, JSON, inventory, and hash manifest remain unchanged.

## Reconciled count stages

The original audit recorded the producer summary values `duplicate_prompt_hash_occurrences=148` and `duplicate_exact_rows_removed=21`. The coordination supplement supplied Sol's independent stdlib audit, which reports 20,967 final rows, 127 retained repeated-prompt occurrences, 110 repeated-prompt groups, and 110 groups with multiple action targets.

I independently streamed the existing final JSONL without project imports or data regeneration. It has SHA-256 `c547e8f0c5988b29288f2a097169c7859741b7d4f53f222af31f5e2889d516cf` both before and after the recount, matching the saved summary. The recount confirms 20,967 rows; 127 repeated-prompt occurrences across 110 groups; all 110 groups have multiple `(target_action_id, target_command)` pairs; zero such groups cross the saved train/validation split; and zero field/hash/action-map errors. No exact prompt/completion/command triplet duplicates remain in the final file.

The stage distinction is in `src/sft/dataset.py`: `deduplicate_exact_rows` increments `prompt_counts` before checking `exact_hash` and skipping an exact duplicate (current lines 274–286). Thus the summary's 148 is a pre-exact-dedup occurrence count carried forward in the duplicate-count metadata, while the saved output's direct count is post-dedup. The recorded removal count is 21, and `148 - 21 = 127`, exactly matching both independent direct counts of the final file. The earlier report's figures therefore reconcile under the producer's counting convention; they are not evidence of a dataset inconsistency.

The 110 multi-target prompt groups are authentic label multiplicity in the saved rendered-prompt representation. They are not, by themselves, a field-hash or action-map integrity failure, nor do they prove that the targets are interchangeable or that the prompt contains all behaviorally relevant state. Preserve this as a dataset characteristic for any later scientific interpretation.

## Provenance limitation retained

This count reconciliation does not resolve the historical split/exclusion binding issue. The preserved `sft_training_protocol.json` declares split/exclusion hashes `e6695359…` and `8e0d04d3…`, whereas the currently preserved manifest files hash to `5347163365e77f46517756156c22e803a7e5a6a54009f7151eab92fb51e6ff56` and `fdbe3b1c2d8162fa7c95ff25b57ace1eaf01c1224d42f9f1f447bf7a859541c5`. The older manifest bytes were not located. This is a saved-record binding conflict; it does not establish which manifest bytes the historical process actually loaded. No old record was edited and no runtime evidence was reconstructed.

## Scope and evidence

- Sol's supplied result: `independent_expert_dataset_check.json`, SHA-256 `8c2b381d7ae6e0b30c66911683531a71a450271a0dddd5f39629c8ab25a1650b`; its receipt reports return code 0. The result, script, receipt, and log were read-only inputs.
- Luna's independent recount: `prompt_occurrence_recount.json` and `recount_prompt_occurrences_addendum.py` in this directory. The recount process returned 0.
- No dataset reconstruction, model/tokenizer/environment, project analyzer/validator, pytest, training, policy replay, scientific-source edit, original-record edit, shared-index update, commit, or push occurred.

