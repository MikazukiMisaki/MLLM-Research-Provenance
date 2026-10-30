# Historical resource evidence for the thesis

Status: `PARTIAL_SELECTED_LEAVES_RAW_RECOUNTED; FULL_PROJECT_COST_UNKNOWN`. This is a read-only evidence table, not a future budget or an execution plan. The numeric subtotal includes only the seven named original physical-event ledgers below; it excludes training, engineering, previous experiments and all unknown/overlapping work. It is not the cost of the entire thesis or project. A recorded operation or interval is not evidence of exclusive GPU ownership.

## Selected physical-event ledger recount

| Recorded leaf | Completed generations | Reset-inclusive environment operations | Evidence character |
|---|---:|---:|---|
| R19 G2 failed replay predecessor | 0 | 19 | 18 non-reset + 1 reset |
| R19 G2 successful smoke | 176 | 322 | 312 non-reset + 10 resets |
| R19 G3 failed predecessor | 1 | 1 | 1 reset, no non-reset completion; source unit remains incomplete |
| R19 G3 completed successor | 4,965 | 7,607 | 7,273 non-reset + 334 resets |
| SI-S01 source collection (96 episodes) | 1,959 | 2,055 | 1,959 steps + 96 resets |
| SI-M1 five-case probe | 10 | 64 | 55 replay + 4 teacher steps + 5 resets |
| SI-U1 paired three-arm evaluation | 5,001 | 5,247 | 5,001 steps + 246 resets |
| **Seven selected original ledgers** | **12,112** | **15,315** | Partial subtotal only; neither full project nor future spend |

`RAW_LEDGER_RECOUNT.json` and `recount_raw_ledgers.py` in this directory bind every named journal path and raw SHA-256, with input bytes rehashed before and after. For the three SI journals, the independent script additionally pairs each saved `unit_completed` to its saved `unit_started` event ID, unit and identity, counts only completed operations and finds no unmatched started units. It independently sums generation input/output token fields. For R19, it recounts event types and operation names and checks aggregate start/completion counts; it does **not** independently revalidate every operation's unique identity or the full hash chain. The earlier R19 identity/physical reconciliation and production validation remain separate evidence. No such metadata count can prove that no unrecorded external work happened.

The R19 campaign aggregate is 5,142 generations and 7,949 reset-inclusive operations, already represented by the four R19 rows. It includes historical 177/342 and must not be added again. The earlier G3 import-failure receipt is reported to have produced no scientific operations; it is not an extra counted leaf in this raw-journal subtotal. The 169 `environment_step_completed` wrapper records in the successful G3 are already represented by their physical operation events and must not be charged a second time.

In the three directly recounted SI journals, source96, M1 and SI-U1 evaluation additionally record **347 environment constructions and 347 closes** (96+5+246 each). These 694 lifecycle calls are separate from the 15,315 reset-plus-nonreset subtotal and are not a count of all project constructions or closes. The earlier V2 partial ledger explicitly counted only source96 and SI-U1 evaluation lifecycle calls: 342+342; this note adds the five M1 constructs and five closes as supported by its raw completed-unit events, without altering the prior record or the 15,315 subtotal.

## Training and elapsed allocation evidence

| Historical work | Observed work | Time and interpretation |
|---|---|---|
| P0 expert SFT | 2,354 optimizer steps; reported 23,860,000 input tokens | Training result reports 27,406.2827 wall seconds (~7.61 h); source does not by itself establish an exclusive device-allocation interval or per-task optimizer exposure. |
| SI-U1 B continuation | 1,248 microbatches, 78 optimizer steps, 6,240 supervised tokens; 661,620 reported input tokens | Supervisor allocation interval 883.2236 device seconds; shared device, not proof of exclusivity. |
| SI-U1 C continuation | Same step/dose counts; 695,872 reported input tokens | Supervisor allocation interval 916.8314 device seconds; shared device, not proof of exclusivity. |
| SI-U1 three-arm evaluation | 246 episodes, counted in physical table above | Supervisor allocation interval 4,263.2806 device seconds. B+C+evaluation intervals total 6,063.3356 seconds; do not also add this aggregate to its three leaves. |
| SI-U1 four separate engineering attempts | Includes failed and completed attempts; separate from scientific results | Allocation intervals total 455.8561 seconds. Nested worker, launcher and supervisor clocks describe overlapping intervals and must not be summed. |

P0 `training_result.json` raw SHA `e6a47124200cacba4d1f3eaf97fdf79657d7df04f072a4d5446c2bec677c399e`. B independent acceptance `/home/lizening/research-notes/agent-logs/2026-10-29T141700Z__SOL__si-pilot82-c-start-provenance__9bbaa/B_INDEPENDENT_ACCEPTANCE.json` SHA `32a7b319ea2ed5f865659949ed5a320af5c4fbd435eb737511bad8926252c32d`; C acceptance `/home/lizening/research-notes/agent-logs/2026-10-29T113523Z__ASTRA__three-arm-prospective-design__a55d1af9/C_REAL_INDEPENDENT_ACCEPTANCE_9BBAA.json` SHA `6603562a9853ff302f7b71995fe2657825ca9480b0cc1530ba2dca63a715a7ce`. Evaluation and engineering allocation sources and their exact raw hashes are bound in the prior partial ledger below; their intervals were not independently rederived from clocks in this task. Input-token accounting for training is not interchangeable with completed generation counts.

The separately reviewed evaluation-engineering pair contains one physical reset that returned but failed the logical lossless-recording unit, plus a later separately launched completed check. Together they represent two physical resets, one step and one generation. The failed reset and its reservation describe the same physical call, not two. These engineering calls are **not** in the 12,112/15,315 subtotal.

## Logical policy costs are a different quantity

R19's K2 and CONTINUE logical full-branch means are 9,854.25 and 7,470.22 tokens per eligible prefix respectively, approximately 31.9% higher for K2. These are reconstructed per-policy logical costs, not physical research expenditures, device hours, or observed deployment latency. Shared stages are logically charged to each policy, while recorded physical calls are counted once; derived aliases do not create extra physical calls. See `/home/lizening/research-notes/agent-logs/2026-10-30T015900Z__SOL__r19-thesis-methods__8be2/RECOUNT.json`, SHA `eeafe9edcb38940a14955c74bcd12f840eb596bd1e5cd8e178b0ec7577cfd88b`, and the frozen R19 cost protocol cited in the methods appendix.

## Completeness and provenance limits

Earlier project work, P0 setup, source acquisition, engineering, interrupted/failed/open operations, external resource costs, lifecycle calls and elapsed intervals are incompletely inventoried. The earlier reported pre-source96 engineering aggregate of one generation and seven operations has no independently bound unique leaf identity; it remains explicitly non-additive until its overlap is resolved. No omitted metric is silently treated as zero. Previous V2 accounting record and its failed-reset correction are `/home/lizening/research-notes/agent-logs/2026-10-30T010000Z__CODEX__si-project-ledger-correction-independent/RECORD.md` SHA `960ccb06ea670996b18f18bfb60785a2ccae0e71920cc02d2c6914a1a099e34d` and `PARTIAL_ACTUAL_LEDGER_V2.json` SHA `3c9060003bbf4b96e49afa596cabedbd53a5a6448edc611227d2ac2395937470`. This document strengthens several previously summary-only rows to direct raw-event counts; it does not establish exhaustive historical accounting.

No model, CUDA, ALFWorld, training, scientific analyzer or new experiment ran; no old evidence or scientific code was changed. Raw event journals contain private task/model data and are referenced by path/hash, not copied into this report. The new evidence remains pending independent review and coordinator publication.
