# Sanitized budget ledger template — SI minimal exploration

**Status: DESIGN ONLY.** This is a fillable ledger, not an executable budget,
gate, data schedule, or permission to run. `UNKNOWN` means no evidence in the
reviewed sources; it must not be replaced with zero. The public upload allowlist
is this file and `SANITIZED_RESULT_SUMMARY.md` only.

## Frozen design envelope from Proposal V3

Source: `PROPOSAL_V3.md`, SHA-256
`358daf235945a0644f338fc318d922fb6af2dc8af0ba527eb312ece2b17f71c9`.

| Phase | Planned arms | Proposed monitored stop threshold | Status / caveat |
|---|---|---:|---|
| Training | C1 uniform and C4 targeted-weight, one product per arm | 1.5 device-hours per arm; 3.0 total | Proposal only; not a forecast or hard physical cutoff. Training recipe, dataset, step count, memory, and actual device attribution are not established. |
| Evaluation | P0, C1, C4 on the same prospectively fixed development panel | 1.0 device-hour per arm; 3.0 total | Proposal only. `N`, eligible assets, task/parent grouping, runtime token caps, and task-disjointness are unknown. |
| Combined train + evaluation | Sequential on one GPU | 6.0 device-hours | Candidate monitored threshold only; not an authorized reservation. Loading, failed work, cleanup tails, and unresolved liabilities must count. |
| Optional one-episode P0 engineering check | One separate P0 episode only if needed | 0.5 device-hour | Separate from the 6-hour envelope; not mandatory and not an effect estimate. |
| New self-experience/source acquisition | Separate phase and pool | **UNKNOWN / not included** | Before any acquisition, budget every source episode, generation, token, reset, step, selection/filter/failure, and cleanup separately. |

The proposal uses `H=50` and `N` as the actual episodes per arm. Conditional
maximums are:

| Quantity | Per arm | Three evaluation arms |
|---|---:|---:|
| Episodes | `N` | `3N` |
| Generations, at most one per action | `50N` | `150N` |
| Environment operations, including one reset per episode | `51N` | `153N` |
| Input tokens, only if actual runtime cap is 8,192/generation | `409,600N` | `1,228,800N` |
| Output tokens, only if actual runtime cap is 16/generation | `800N` | `2,400N` |

`N=16` is an arithmetic illustration only: 48 episodes, 2,400 generations,
2,448 environment operations, 19,660,800 input tokens, and 38,400 output tokens
under the conditional 8,192/16-token caps. It is not evidence that 16 eligible
episodes exist. The proposal explicitly disallows assuming historical example
counts or family counts apply to a future dataset.

## Fillable run/phase ledger

Create one row per `(run_id, phase, arm)` and append event-level rows for every
physical operation. Keep acquisition, training, evaluation, and cleanup costs
separate; maintain a cumulative total across all phases.

| Field | Value to freeze or measure |
|---|---|
| `proposal_version_sha256` / `run_id` / `arm` / `phase` | `UNKNOWN` until bound; arm in P0/C1/C4, phase in acquisition/train/eval/cleanup |
| `source_commit_sha` / exact-review SHA / execution-clearance SHA | `UNKNOWN` for any future run; prior one-shot clearance is consumed |
| `base_model_sha` / adapter or checkpoint SHA / tokenizer SHA / runtime SHA | `UNKNOWN` for future exact run; bind immutable identities before release |
| `input_asset_opaque_id` / version / content SHA / producer stage | `UNKNOWN`; do not infer assets from historical aggregate counts |
| `loader_scope` / rows or episodes in scope / exclusions evidence | `UNKNOWN`; specify the exact loader-visible scope and completeness basis |
| `T_episodes` / `G_parent_groups` / `N_per_arm` / pairing schedule SHA | `UNKNOWN`; freeze episode and parent units separately |
| `H` / seed policy / termination policy / loss normalization | Proposal: `H=50`; other executable values must be frozen |
| `training_epochs` / microbatch / accumulation / sequence length / optimizer steps | `UNKNOWN`; do not import historical 1,248 microbatches or 78 updates as defaults |
| `rows_seen` / padded input slots / nonpad input tokens / supervised tokens | `UNKNOWN`; record separately for each training arm and epoch |
| `generations_started` / completed / failed / input tokens / output tokens | `UNKNOWN` until run; count partial and failed work; state EOS accounting convention |
| `reset_count` / `step_count` / `replay_count` / physical operation IDs | `UNKNOWN` until run; every real operation counts, including failed attempts and replay |
| `GPU_UUID` / `PID↔GPU mapping evidence` / allocation start and release monotonic times | `UNKNOWN` until trustworthy attribution is established |
| `device_count` / actual device-seconds / device-hours / conservative upper bound | `UNKNOWN` until measured; never substitute wall time for GPU allocation |
| `allocator_peak_allocated` / `allocator_peak_reserved` / NVML samples and timestamps | `UNKNOWN` for new runs; keep memory metrics separate from device-hours |
| `CPU/RAM/storage/network ceilings` / observed peaks | `UNKNOWN`; set explicit values before an executable release |
| `reserved_threshold` / actual use / overrun or unresolved tail | `UNKNOWN` until frozen/measured; retain liabilities rather than rounding down |
| `runner_exit` / supervisor_exit / cleanup confirmation / artifact hashes | `UNKNOWN` for future runs; missing receipts or cleanup are fail-stop conditions |

### Event-level accounting row

Use an append-only record with these columns (one row per actual physical
operation or resource interval):

```text
run_id,phase,arm,operation_id,operation_type,start_monotonic_ns,
return_monotonic_ns,completed,failed,underlying_physical_event_id,
input_tokens_nonpad,output_tokens,train_tokens_padded,train_tokens_nonpad,
train_tokens_supervised,optimizer_updates,GPU_UUID,PID_identity_evidence,
allocation_start_ns,allocation_end_ns,device_count,device_seconds,
allocator_peak_allocated_bytes,allocator_peak_reserved_bytes,
NVML_timestamp,memory_used_bytes,exit_code,cleanup_state,unresolved_cost
```

Keep a separate reservation/stop table per phase. Count each physical reset,
step, replay, and generation once. If a software wrapper references an already
recorded physical event, link the IDs and do not double-count it; never erase
the physical operation. Logical token totals, padded training slots, model
calls, environment operations, memory, and device-time are distinct metrics.

## Reconciliation and stop procedure

1. Before release, freeze the asset/schedule/runtime hashes, complete scope,
   caps, reservation, episode-vs-parent unit, token-count conventions, resource
   measurement windows, and unresolved-tail policy.
2. Record monotonic start/return/completion events for every model and
   environment call. Record per-arm train tokens and optimizer updates; do not
   derive them from wall time.
3. Independently monitor the authorized process and the physical device. Compute
   device-seconds only from intervals with defensible PID-to-UUID attribution;
   for sequential single-GPU work, sum those intervals. If attribution or
   release time is unknown, report actual usage as `UNKNOWN` and separately
   retain the conservative launch-to-confirmed-cleanup envelope.
4. Keep allocator peaks and timestamped NVML samples separate. A point snapshot
   is not a sustained capacity estimate. Training peak memory cannot be inferred
   from an inference-only engineering smoke.
5. Reconcile event ledger, supervisor receipts, token counters, physical
   environment IDs, and resource intervals. Any unexplained difference,
   missing receipt, integrity/access anomaly, cap breach, or uncertain cleanup
   stops the run. Count failed/partial work and the observed cleanup tail; do
   not retry automatically or represent an unknown tail as zero.
6. Report phase actuals, cumulative actuals, reservations, remaining proposal
   thresholds, and unresolved liabilities separately. Acquisition is outside
   the six-hour train/evaluation proposal until separately bounded.

## Known actuals versus unknowns

The only measured new run in the reviewed summary was a one-task engineering
smoke: 1 generation, 267 input tokens, 5 output tokens, 1 reset, and 1 step.
Its outer elapsed time was 104.1789 seconds; the inner receipt reports
0.028890565521756395 device-hours, while actual physical allocation remains
`UNKNOWN_FROM_OUTER`. This single inference path is not used to forecast training
or a full evaluation.

Unknown for a future experiment: eligible `N`; asset identity, versions, loader
scope and split; `T/G` grouping; actual input lengths and context; acquisition
cost; training epochs, batches, supervised tokens and optimizer steps; training
memory; evaluation latency distribution; device ownership; CPU/RAM/storage
ceilings; and total future budget. These fields stay blank/`UNKNOWN` until
independently bound.
