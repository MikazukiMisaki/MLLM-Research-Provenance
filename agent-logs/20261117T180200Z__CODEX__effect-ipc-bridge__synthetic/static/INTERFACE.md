# Effect IPC and parent budget channel: static contract

This is static source review only. No production source, task, model,
environment, GPU or scientific execution was run or changed. It is not an
execution authorization.

Exact sources:

| Source | SHA256 |
|---|---|
| `gate-live/effect_ipc.py` | `046c0c48291efdae06457d87343d084357ae5a1774c3d670e3e232b15fd16dd8` |
| `gate-live/stage_budget.py` | `d3c6b9c5485670b6fe6b2af3354dd7125c85dc94bf47ed3a44d21f4df2f263cd` |
| `gate-live/owner.py` | `a8090a17c95c96026c2c6f703baaafe2c874714ad63507de6f1f83a5` |
| `fixed_product_per_arm__private/runtime/fixed_product_dev/arm_budget.py` | `73711d9ccc5c0a07f3fa1f57fc82cbbe8c4a00b59b93f582c2c320686f40c073` |
| `fixed_product_per_arm__private/runtime/fixed_product_dev/supervise.py` | `0cc7cd3e5b640c4ddc1652f97236891e09b25b7e09857c99fcdc4c5c0965e307` |

The gate-live root is `/home/lizening/research-notes/agent-logs/20261116__CODEX__two-object-paired-eval__candidate/gate-live`;
the fixed-product root is `/home/lizening/research-notes/agent-logs/20261118__CODEX__fixed_product_per_arm__private`.

## Client messages and sequencing

`effect_ipc.py:45–83` requires an AF_UNIX stream descriptor >=3, a per-operation
allowlist/caps, and a five-second socket timeout. It starts at seq=0 with no
active operation. Every request is canonical JSON followed by newline, at most
4096 bytes including newline. The reply must be exactly
`{"kind":"ack","seq":S,"allowed":true}`, with integer (not boolean) seq and
boolean allowed. Duplicate JSON keys, nonfinite values, EOF before newline,
invalid shape and mismatched seq fail. Each exchange blocks for that ACK; the
client does not intentionally pipeline messages.

An operation uses this sequence, all with the same `S`:

1. `{"kind":"reserve","seq":S,"operation":OP}`. Only after its ACK
   does the client mark OP active, increase its local count, and fsync an
   `OP_started` child journal line. The controller then invokes the effect.
2. On return it writes and fsyncs `OP_returned` and sends
   `{"kind":"returned","seq":S,"operation":OP,"receipt_sha256":H}`.
   `H` is SHA256 of the complete returned journal line including newline,
   **not** the nested journal row's internal chain digest. On the ACK, it
   clears active and increments client seq.
3. On exception the controller attempts `unknown` with the same fields and a
   hash of its fsynced `OP_unknown` line. On ACK the client increments seq,
   clears active and prevents future reserves. This reporting attempt can
   itself fail; it must not be silently treated as a known no-op.
4. Once no operation is active, it sends
   `{"kind":"finished","seq":NEXT,"status":"COMPLETED"|"STOPPED"}`.
   An unknown status prevents client-side `COMPLETED`; it does not authenticate
   the actual native result or impose parent-side resource policies.

`Journal.emit` (`effect_ipc.py:18–33`) uses a separate hash chain and fsyncs
each line. If writing, sending or receiving fails at a boundary, the parent
must conservatively preserve any reserved effect and reconcile available
evidence. A completed effect can have its child receipt written even if the
ACK is lost. Conversely, a durable reservation or ACK alone does not prove
that physical work started. In particular a receipt hash is a child claim,
not independent evidence that the contents or operation are authentic.

## Existing parent behavior

`stage_budget.py:30–73` and `arm_budget.py:27–70` parse one newline-framed
request at a time, buffer fragments, enforce max 4096 bytes, and reject extra
frames before the prior ACK has been written. Both require exact key sets,
strict integer seq, and one outstanding operation. On reserve the parent
increments its `next_seq` and count, creates an outstanding `(seq,operation)`,
and emits `operation_reserved` before preparing an ACK. The corresponding
return/unknown must carry that same seq and operation and a lowercase 64-hex
receipt hash. It emits a child-claim event then clears outstanding. Unknown
prohibits another reservation. The parent checks only the hash's shape here,
not that it equals a particular child line; verification must be separate.

On `finished`, the seq must equal parent's next sequence, no effect may be
outstanding, and completed requires mandatory reservation counts, no unknown,
and minimum generation count. `stage_budget`'s EVAL profile is a two-arm
profile (one materialization, two of each construct/init/reset/load, 100
generation/step and at least two generations). `arm_budget` is one-arm
(one materialization and one construct/init/reset/load, 50 generation/step
and at least one generation). Neither can be reused unchanged for pair-owned
setup plus two separate workers: both mandate child materialization, and they
do not alone establish a shared global four-pair ledger.

The channel sets a two-second ACK deadline and supports partial nonblocking
ACK writes; it does **not** autonomously schedule writes, enforce the clock or
reap processes. The concrete supervisor calls `receive`, checks stop/deadline,
and calls `write_ack`; it also separately checks the stored ACK deadline
(`supervise.py:221–286`). Durability of an emitted parent reservation depends
on the injected journal: the existing `owner.Journal` fsyncs each emitted line
(`owner.py:52–65`), whereas the budget channel itself accepts a generic
`journal.emit` and cannot guarantee durability independently.

The parent's `eof()` rejects leftover frame data, pending ACK, outstanding
effect, or absent finished marker; a successfully finished `STOPPED`/unknown
session is not a completed scientific episode. The cited supervisor requires
child exit zero, `finished=COMPLETED` and no unknown, plus its separate cleanup
checks (`supervise.py:287–308`). Any process interruption, pending reservation,
partial ACK, journal I/O error or missing child receipt needs fail-stop
accounting; do not infer nonexecution, synthesize a receipt, or retry silently.

## Bridge obligations and limits

The separate v3/v4 prototype uses `type`/token/initial/done messages and is
not wire-compatible with this `kind`/seq/ACK client. A bridge must establish
ordering and durable counting on exactly one side, pass ACK only after the
appropriate accepted reservation, reconcile claims, handle partial frames,
EOF and lost ACKs, and avoid double counting. Explicit first/second initial
state handoff must happen after reset and before second model-load admission;
it is not a message provided by `EffectOwner`. It must also implement and
independently verify the intended scientific roster, actual native outcomes,
model identities, process ownership, device limits, wall/token/global limits,
source provenance, and cleanup. Static protocol compatibility does not prove
any of those facts or equivalence of hidden task state.
