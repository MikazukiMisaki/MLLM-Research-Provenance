# C-low resource envelope, revision 2

**DRAFT / NOT READY; supersedes only the budget proposal in the first draft.**
This revision responds to independent review of draft SHA256
`c450605ff4e16e1ae6560facf3d23e38f000bbf201a0b09add2b5504ccb9981c`
(`INDEPENDENT_REVIEW.md` in `si-resource-envelope-independent-review`).
No actual gate, preflight, model, environment, training or protected task was
run or read for this revision. Proposed ceilings are not measured physical
cost, approval or proof that the existing supervisor can enforce them.

## Source-level accounting and observations

The reviewed historical `9bbaa12c2d8177a60ec5a74ed2f970ef29a57bce`
continuation gate calls `tree_sha256` on base and adapter in preflight, live
and worker modes. Historical `train_from_p0` separately hashes base and
adapter before and after training, and uses the local Transformers model
loader. Thus **conditional on an identical successful path and unchanged
artifacts**, a separate positive preflight plus one live attempt performs five
full base-tree hashes: one during preflight, live gate, worker gate, trainer
before and trainer after. An interrupted path may perform fewer or leave an
unobserved partial pass. The new candidate's exact production connection and
outer supervision have not yet been reviewed; the recipe is not proof it will
use the same calls or that hidden retries cannot occur.

Read-only metadata of the five locally cached Qwen3-8B shard entries gives
3,996,250,744 + 3,993,160,032 + 3,959,604,768 + 3,187,841,392 +
1,244,659,840 = **16,381,516,776 bytes = 15.256476 GiB** per complete
five-shard pass. These are file-size observations, not a new content hash or
proof that the candidate will load those exact leaves. A base tree also has
other files. Four live-stage hashes alone consume at least
**65,526,067,104 bytes = 61.025906 GiB** in shard read requests. Five across
preflight and live are **81,907,583,880 bytes = 76.282382 GiB**. In addition,
reserve one full shard equivalent for model loading when sizing the live stage:
four hashes plus that loading allowance are **76.282382 GiB**. That allowance
is not a measurement or a claim that actual mmap/page-in behavior equals one
full pass. Adapter, tokenizer, dataset, protocol, imported packages, writes,
re-reads, logs and native work are additional.

Historical C training output metadata records **349,723,988 bytes
(0.325706 GiB)** across five files, including one **349,243,752-byte** adapter
weight file and training events/result. Its complete run directory had 12
regular files and about 350.4 MB logical bytes. B was similar. These are
historical final-file sizes, not a bound on temporary checkpoints, duplicate
copies, filesystem overhead or future outputs. No model-weight contents were
read to obtain these sizes.

The historical source/result records C caps of **700,000 input tokens and
6,240 supervised tokens**; observed C was 695,872/6,240, leaving 4,128 and 0
respectively. The real C-low specification changed LR 0.0001 to 0.00005 and
the corresponding fixed 78-step schedule, not these caps. This revision
preserves the inner caps exactly; a looser outside ceiling must never override
them. Actual tokenization or source drift can make C-low fail those limits.

A read-only check at preparation time found the `/home` filesystem has
**35,826,626,560 bytes = 33.366146 GiB** available. Final destination,
quota and competing writers are not verified. This is a transient point-in-time
observation, not a reservation or authorization to delete/move old evidence.

## Proposed one-shot stage envelope and explicit pass allocation

All quantities below are upper reservations for **this** attempt only, never
transferred across stages. `GiB` means 1,073,741,824 bytes. A read ceiling
refers to accounted logical byte requests or explicitly charged whole-file
mmap/load reservations, not guaranteed physical device I/O. The exact source,
datasets' lengths, output destination and operator coverage must be frozen and
independently verified before the ceiling can be called enforceable. One
missing/unaccounted operation means stop/UNKNOWN; do not widen a cap in place.

| Stage | Wall ceiling | Proposed logical reads | Explicit allocations / conditions |
|---|---:|---:|---|
| 1. Independent custody | 900 s | 20 GiB | One independently scoped full base hash: ≥15.256476 GiB shard reads plus other base files, P0/source/data/review records and safety remainder. No extra base traversal unless separately budgeted. At most 0.25 GiB new metadata/artifacts. |
| 2. Exact model-free positive preflight | 600 s | 20 GiB | Owns the mandatory preflight gate's one base hash: ≥15.256476 GiB shards, plus base extras, P0, B/C dataset bytes, packages and source/protocol review. No model/tokenizer/CUDA/environment. Actual gate path and included I/O must be confirmed before invocation; 20 GiB/600 s are proposals, not proven fit. At most 0.25 GiB new artifacts. |
| 3. One supervised C-low live attempt | 1,800 s; ≤0.5 allocated-device-clock h | 96 GiB | Outer supervisor covers CLI live gate **before** worker, worker gate, trainer pre/post hash, loader, training, failure/exit and cleanup. Four shard hashes ≥61.025906 GiB plus one full-shard-equivalent loading reservation 15.256476 GiB = 76.282382 GiB, leaving 19.717618 GiB for actual base extras, repeated adapter/data/protocol/package reads and loader overhead. This slack is an explicit sizing assumption, not evidence of sufficiency. Stop if complete path inventory/instrument coverage cannot support it. ≤4 GiB incremental output under enforceable quota. |
| 4. Independent artifact custody | 900 s | 20 GiB | One fresh post-run base hash ≥15.256476 GiB plus two historical-size C adapter scans ≈0.651 GiB, plus metadata/audit and slack. The fresh pass gives a new point observation, not a continuous immutability guarantee. Actual artifact size, audit recipe and other reads must fit independently. ≤1 GiB new audit artifacts. |
| 5. Optional four-case development evaluation | each of three arms ≤1,800 s and ≤0.5 allocated-device-clock h | 48 GiB **per arm**, ≤144 GiB total | Sizing placeholder: one five-shard hash + one load reservation per arm ≥30.512953 GiB, leaving 17.487047 GiB/arm for other work. This is **not** an approved real evaluator recipe: if pre/post hashes, multiple loads or native coverage require more, this stage remains blocked and must be redesigned/re-reviewed before any arm. ≤1 GiB artifacts per arm. |

Stage deadlines sum to **9,600 s = 2 h 40 min**; one train and three
sequential evaluations allocate at most **2.0 device-clock hours** by wall
interval. That is not measured GPU compute, exclusive ownership, or a bound on
unobserved tail. Logical read ceilings total **300 GiB**; this is a proposed
accounting ceiling, not measured disk I/O or a complete historical project
ledger. These sums include the proposed stage 1 and 4 rehashes: they do not
pretend those passes remove the separate gate hashes in stages 2 and 3.

Stage 3 permits at most 1,248 started microbatches and 78 optimizer steps,
with the existing inner ≤700,000 input and ≤6,240 supervised tokens; 0
model generations and 0 environment operations. The 1,800 s includes live
gate hashes (outside the historical worker-only timing) and may be too short;
no based-on-history runtime fit is claimed. One attempt only; retain incomplete
or failed units and all costs, do not retry/resume.

For the optional four-case, three-arm plan only, each arm has ≤4 resets,
≤200 generations and ≤200 steps at horizon 50, ≤819,200 input and ≤3,200
output tokens. Across arms the maxima are 12 resets, 600 generations, 600
steps, 2,457,600 input and 9,600 output tokens; each call still requires
reservation before invocation. Four exposed development cases are descriptive:
paired differences change in 25 percentage-point increments and even 4/4
concordant discordances give two-sided exact McNemar p=0.125; this is neither
adequate precision nor unseen/held-out generalization.

## Revised storage and shared-GPU admission

The independently enforced incremental-output reservations are 0.25 GiB each
for stages 1/2, 4 GiB stage 3, 1 GiB stage 4 and 1 GiB for each evaluation
arm: **8.5 GiB** total. The 4 GiB training proposal is roughly 12.3 times the
historical 0.325706 GiB final C training tree, not a guarantee against other
writers, temporary allocations, repeated checkpoints or future model format.
Immediately before stage 3 require ≥**12 GiB** unallocated availability on the
reviewed output filesystem: 4 + 1 + 3 GiB remaining output caps plus 4 GiB
reserved filesystem headroom; stage 1/2 output has already been accounted by
then. Recheck free space at each stage and include uncommitted/partially written
outputs; other users can consume the same space concurrently. If a reviewed
per-stage quota, trace or reservation cannot prevent exceeding the output cap
while leaving room for failure evidence, treat enforcement as UNKNOWN and do
not admit that stage. The current ≈33.37 GiB observation exceeds the proposed
12 GiB floor, but the final target and actual quota are not yet known. No
historical evidence may be deleted to obtain capacity.

The proposed shared A40 admission remains: bind exact UUID and bus ID; obtain
at least 12 valid read-only samples over one minute with each showing ≥30 GiB
free and ≤20% utilization. Current host/PID namespace mappings and independent
exclusive ownership remain UNKNOWN even if the GPU process list is empty.
Sample device-wide free/used/temperature/power/utilization at most 5 s apart;
collect worker allocator counters when possible. Stop on telemetry loss,
worker reserved >28 GiB, OOM/allocator instability, or <2 GiB whole-device
free for three consecutive samples. A sampler cannot enforce a strict memory
cap or rule out an inter-sample spike; it must not kill other users' jobs or
claim their utilization as this worker's. A valid external owner must cover the
whole live CLI (including its gate), descendants, deadline, cleanup and final
persistence. Abrupt stop may produce unbounded-to-us physical tail; account it
as UNKNOWN incident work rather than free completion.

## Measurable admission, unresolved blockers and provenance

The read-only command examples in the first draft for exact Git identity,
GPU UUID/memory/utilization and `df -B1` remain diagnostic only. Before each
stage, use a reviewed verifier to record byte-length and number of planned
base/P0/dataset/source passes, compare all hashes to independently anchored
pins, and make its entire output volume and monitoring plan explicit. Do not
print dataset rows, task identities, witness contents, private paths, keys or
other users' process command lines. The budget is conditional on a real
meter/reservation layer covering application/native reads and mmap-backed
model loading, plus enforceable storage quotas and a process-tree supervisor.
No such complete implementation or actual final output-volume reservation has
been established. Any unavailable coverage is a pre-launch blocker, not an
implicit 96 GiB physical-I/O guarantee.

A genuine source/pair review, data permissions, immutable input custody,
exact production-gate compatibility, authentic future C-low product, safe
witness isolation, independently reviewed common evaluation runtime and a
prospectively fixed development panel all remain outstanding. Required actual
preflight effects, source-tree count and additional bytes must be verified on
the exact selected path. Stage 5 is only an envelope for feasibility planning;
it is not an instruction or scientific authorization. Preserve original failed
runs and budget records. Until these conditions are independently resolved,
status stays **NOT READY**.
