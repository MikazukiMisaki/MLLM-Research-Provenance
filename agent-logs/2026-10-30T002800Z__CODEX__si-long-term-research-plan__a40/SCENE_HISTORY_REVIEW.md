# Static parent-name scene-number proxy and history audit

**Status:** evidence for independent scrutiny; no release, no selected future task. This metadata audit compared the already inventoried conservative 350-parent archive/local union against *separately named* historic input or execution categories. It uses filename/parent identity, not future task contents, action outcomes or candidate selection. Game and trajectory bytes are streamed for the previous hash-based exclusion; candidate bodies are not parsed or emitted. No model, CUDA, environment or experiment was run.

## Source of the scene-number proxy

For all 1,410 task identities in the original saved SFT source pools (including candidate, training, validation and online-evaluation pool entries, with no assertion they were all executed), the final decimal field of the parent name equals the stored trajectory `scene.scene_num` and the numeric part of `scene.floor_plan`: 1,410/1,410/1,410. This cross-check parses the archived **historical** trajectory scene metadata, not the prospective candidate trajectories. Every parent used in the aggregate must match regex `[^/]+-(\\d+)`; any unexpected format aborts the audit. The finding supports use as a name-based proxy, not a proven property of every candidate or cross-version map geometry.

## Direct bindings of execution categories

- The G1 source is `configs/evaluation/sft_heldout_valid_unseen_schedule.json`, tied to `/home/lizening/Alfworld-Self-Improvement-Project/artifacts/runtime/validation/sft-valid-unseen-g1-20260829T031028Z/{run_manifest.json,trajectories.jsonl}`. Direct independent local check in `historical_binding_audit.py`: the manifest authenticates both file hashes, lists 60 accepted episodes, and all 60 trajectory records match schedule index, task ID, split and game hash; they contain 41 distinct parent identifiers. Matching index and identity does not by itself validate environment behavior.
- B and C materialization manifest hashes match each completed training result; both authentic supervisor returncodes are 0, result bytes match the supervisor receipt, each records 1,248 completed microbatches, and each manifest records 78 parent exposures. The hash-bound selected datasets and detailed 312-example, four-epoch verification are separately recorded in `/home/lizening/research-notes/agent-logs/2026-10-29T230000Z__SOL__si-u1-training-coverage-audit__independent/RECORD.md`. A manifest and aggregate microbatch counter are not independently a trace of each example actually processed; refer to the stronger independent training-coverage record for its exact checks.
- Balanced expert source means the documented 1,200-task expert dataset used as the P0 input and is not a direct trace of each model update. Its exact source hash is bound in `SCENE_HISTORY_AGGREGATE.json`; those data are a source-exposure proxy, not a claim of individual recalled content.
- SI-U1 evaluation identities come from the fixed 82-row schedule. The formal report `SI_U1_SCIENTIFIC_REVIEW_AND_THESIS_NEXT_STEPS.md` records actual 246 completed 3-arm trajectories, and the accepted original analysis independently checked the evaluation. This audit did not re-read the complete SI-U1 raw evaluation journal or independently reconstruct each of its 82 records.
- Original SFT candidate lists and old partition proposal are **separate** protection categories and may include never-executed entries; they are not assigned to executed categories.

Named manifest, archive, dataset and receipt input hashes, scene-aggregation code, binding-check code and machine-readable aggregates are retained in this directory and checked before/after. The 1,410 historical trajectory files were hashed as read and independently rehashed afterwards; a hash of their sorted relative-path/hash inventory is in the aggregate JSON, without publishing identities. Dynamically discovered protected-file hash inputs do not have a separate snapshot inventory or after-check; this limits reproducibility and should be remedied by an independent recount. No identifier lists or scene numbers are emitted.

## Aggregate comparisons

On the preserved earlier conservative filter (old proposal protected, 950 old-only archive trial paths and six local parent names, deduplicated to 350 potential parent identities):

| Comparison set | Potential parents whose parent-name numeric suffix matches any name in set |
| --- | ---: |
| Balanced expert input | 322/350 |
| B/C training materializations | 210/350 |
| SI-U1 82-task evaluation schedule | 151/350 |
| Executed SFT G1 60-task schedule | 24/350 |
| Union of the above four | 346/350 |
| Broad protected recorded/possible-use set | 350/350 |

These categories overlap and the values do not add. The broad set contains candidate lists; it is not evidence of 350 executed or trained tasks. Four parents do not match the first union; this does not establish newness, past nonexposure, independent sampling or eligibility.

Of 24 potential parent identities in the **valid_unseen** split, 24/24 have a numeric suffix matching one of the four suffixes represented by the consumed 60-task SFT G1 schedule. An earlier audit established zero G1 parent-identity overlap, so the two results are consistent: different parent names can share this scene-number proxy. This is not a claim the 24 old-version games were executed, that their actual geometry equals G1, that they were training examples, or that inference history is complete. At most it rules out asserting scene-number disjointness under this proxy and the cited history.

## Next necessary checks

Independently reproduce using distinct implementation and compare category and split aggregates; inspect project history for additional dated actual use and unresolved old-source versions. Explicitly define a prospective claim before using scene grouping: same numeric identifier versus same realized object configuration versus held-out distribution are different concepts. If source or scenario semantics remain unknown, write that limitation in the thesis and do not relabel the inventory unseen or held-out. Compatibility would require a separate, reviewed procedure and budget; this static review does not authorize environment-only probing or evaluation.
