# Pre-ACK token-budget binding: static assessment

Static source review only; no real task, model, tokenizer, GPU, environment,
preflight or scientific execution was accessed or invoked. No code was changed.

## Exact source bindings

| Source | SHA256 |
|---|---|
| `gate-live/source_worker.py` | `36f4d2a4d82e5798a5d3fd786fa80505fe3c345ff7333aa8bdfaf52581a34111` |
| `gate-live/effect_ipc.py` | `046c0c48291efdae06457d87343d084357ae5a1774c3d670e3e232b15fd16dd8` |
| `fixed_product_dev/arm_budget.py` | `73711d9ccc5c0a07f3fa1f57fc82cbbe8c4a00b59b93f582c2c320686f40c073` |
| `fixed_product_dev/supervise.py` | `0cc7cd3e5b640c4ddc1652f97236891e09b25b7e09857c99fcdc4c5c0965e307` |

`gate-live` is `/home/lizening/research-notes/agent-logs/20261116__CODEX__two-object-paired-eval__candidate/gate-live`;
`fixed_product_dev` is `/home/lizening/research-notes/agent-logs/20261118__CODEX__fixed_product_per_arm__private/runtime/fixed_product_dev`.

## What exists

`source_worker.py:139–164` prepares the prompt, checks a nonempty integer ID
list of at most 4096, matching all-one attention mask and matching re-encoded
tensors, then child-journals `prepared` with `input_ids`, mask, public prompt,
rendered prompt, model generation config and fixed kwargs. The kwargs at
lines 12–13 include `max_new_tokens=16`. `effect_ipc.Journal.emit` fsyncs its
JSONL line before returning (`effect_ipc.py:18–33`). Generation is invoked
only through `controller.effect('generation', ...)` at source line 180.

However, `EffectOwner.start` emits a reservation request containing only
`kind`, `seq` and `operation`; `prepared` has no explicit parent ticket,
one-time preparation ID, arm or step (`effect_ipc.py:64–69`). Its later
`generation_started` line has `owner_seq` but is written only **after** the
reservation ACK. The cited `StageBudgetChannel` counts operation reservations
and validates seq, cap and receipt-hash syntax; it does not parse `prepared`
or track tokens (`arm_budget.py:27–61`). The cited supervisor does not add
that logic before ACK (`supervise.py:245–271`). Consequently the existing
parent cannot presently claim an input-plus-output token cap is enforced
before generation.

## Prospective minimum, not an implemented guarantee

Before accepting a generation reservation and sending ACK, the parent needs a
durable, unique binding among the pair/arm, active `owner_seq`, and exactly one
not-yet-consumed prepared record. It should reject missing, duplicate, stale,
partial, malformed or inconsistent records, verify their line/chain and the
actual fixed producer contract, check input IDs/mask and per-call limits, and
fsync a parent reservation for the validated claimed input count plus the
maximum 16 output tokens. It must check the cumulative, per-unit and overall
remaining caps before ACK. The same prepared record cannot be reused for a
second request. A strictly single-flight state machine with a verified
one-time journal cursor can support such association; a recorded explicit
preparation ID/sequence bound to the request would be clearer and needs an
exactly specified bridge and tests. Neither is implemented in the old parent.

Returned `generation_returned` evidence contains the claimed sequence and
output IDs (`source_worker.py:172–179`); it can support a separately checked
actual-token tally and output cap. If an operation is interrupted, a receipt
is missing, journal/ACK fails, or provenance is uncertain, preserve the
reservation and stop for reconciliation. A reserved maximum is not proof a
physical operation occurred, and an ACK failure is not by itself proof it
did not. If unused maximum-output capacity is to be released, the policy and
the trusted evidence required to do so must be specified before execution.

Tests should include missing/stale/repeated `prepared`, wrong owner seq or
arm, changed IDs/mask/config, over-limit input and cumulative budget, partial
journal, lost/partial ACK, interruption, and separate-arm cumulative debits.
The bridge must also retain all actual prior physical cost and unknown work.

## Limits and races

Token count and returned tokens above are **child claims**. A verified line
hash and producer source do not independently prove what was physically sent
to a model, guard against same-UID tampering or make the ACK/effect transition
atomic. Exact runtime identity and independent monitoring have to be handled
separately. `source_worker.py:158–160` tokenizes and moves tensors to the model
device before the `prepared` line and before generation reservation. Thus a
pre-ACK token allowance bounds only the later model-generation contract; it
does not prove zero tokenizer/CPU/GPU setup, allocations or other physical
resource consumption. No existing experimental outcome is reclassified by
this proposal.
