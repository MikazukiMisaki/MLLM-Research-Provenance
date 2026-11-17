# Pair-owned materialization: static interface constraints

This is a static interface analysis, not an implementation, test result or
permission to run. No actual task files, materializer, model, tokenizer, GPU,
or environment were invoked. The named source files were only read for their
declared behavior; historical evidence was not changed.

## Exact source files

| File | SHA256 |
|---|---|
| `gate-live/eprime_ports.py` | `a1c5d80d58d0b4219ed813f7d61e30fe0e1a02ddca273f93b6734799e491e20e` |
| `gate-live/forward_specs.py` | `f3e07b45d233580860b8f07ead4c746901c5473a0448ee94927c917792448dd0` |
| `gate-live/effect_ipc.py` | `046c0c48291efdae06457d87343d084357ae5a1774c3d670e3e232b15fd16dd8` |
| `pair-interface-schedule-v3__private/candidate.py` | `73d7cecfb0700963214d4b86649597442e7f5d4e9da3b521d25063d4ba864488` |
| `fixed_product_per_arm__private/runtime/fixed_product_dev/arm_stage.py` | `cd59103a03065a4546c521d00848ce9056e53bfa5883ec629a72ab027cb80844` |
| `fixed_product_per_arm__private/runtime/fixed_product_dev/episode.py` | `06922aed662e84c1366624600c361f64ca7fba1ee93daccf83ff8de7a174a21b` |

The `gate-live` root above is
`/home/lizening/research-notes/agent-logs/20261116__CODEX__two-object-paired-eval__candidate/gate-live`;
the other paths are under `/home/lizening/research-notes/agent-logs/20261118__CODEX__`.

## Manifest and path contract

`materialize(output, manifest, journal, *, family)` requires exactly three
manifest keys `game`, `routing`, `config`; each value is exactly an absolute
`path` and a `sha256`. Its `_case_for_manifest` compares the whole nested
dictionary to exactly one `forward_specs.CASES[case]['inputs']`; equal content
hashes under alternative paths are not enough. The chosen family must match
that case; the two-object route uses `family='two'` and a fixed expected
routing/config structure. Its source reader checks bounded regular files,
identity stability and hashes. This is a source contract, not a test on any
actual task.

On success the returned tuple is `(game, config_path, dataset)`, with the
game at `dataset/authored-eprime-only/game.tw-pddl`, the routing sibling at
`traj_data.json`, and `config_path` pointing to a generated configuration
whose data path is the new dataset root. The v3 `snapshot` expects this same
layout. The output directory must permit a new `eprime_only` subtree. Running
once in the pair owner and passing the same tuple to both arms requires
matching canonical paths and recorded source/materialized bytes, not just
making a second copy that happens to have equal contents.

`verify_materialized(game, config_path, dataset, manifest, journal, phase)`
accepts only `phase='pre'` or `'post'`, rereads all three source artifacts,
verifies copied game/routing/config and checks dataset inventory. The v3
prototype's callback shape and four pre/post calls align at the signature
level; behavior has not been integrated or exercised with these functions.
It does not by itself guarantee an immutable file between checks or a hidden
state match between two environments.

## Controller/worker incompatibility

v3's socket protocol expects objects with `type` equal to `reserve`, `return`,
`initial`, or `done`, and returns a token or `ok`. The existing production
`EffectOwner` sends `kind=reserve/returned/unknown/finished`, sequence and
operation fields, and expects `kind=ack, seq, allowed` replies. v3 would see
no `type` on such an existing request and reject it. There is no `initial`
message in the current effect protocol. A tested bridge or consistently
redesigned protocol is required; format names alone do not establish receipt
authenticity or physical cost.

The existing `arm_stage.run_arm` starts its own `materialize` effect inside
each arm and requires an empty per-arm output directory. Passing it unchanged
after a parent setup would not create a one-setup-per-pair implementation.
A separate, reviewed integration must explicitly receive and verify the shared
tuple, remove the redundant arm materialization effect, preserve per-arm output
separation, and make the second reset's public initial match the first before
the second model-load permit. The existing episode performs its own
`previous_initial` comparison; v3's parent additionally requires an explicit
initial handshake. Those mechanisms must be reconciled, not assumed to be
automatically wired together.

## Remaining execution requirements

The fictional v3 schedule must be replaced or bound to an actual reviewed
manifest, actual case/product identities and immutable code/runtime hashes.
The prototype lacks real actor/native-success evidence and its fake receipts
are not independent physical-operation proof. Its operation counts alone do
not implement a complete model/token, setup I/O, wall-clock, GPU, accumulated
cost or process/descendant cleanup policy. It has no full resource supervisor,
secure read-only isolation or protection against TOCTOU/same-UID mutation.
Failure, reservations and already observed outcomes must remain durable with
no hidden refund or retry. Public reset equality does not establish equality
of hidden environment state. Any future exact implementation requires its own
tests, review and independently verifiable evidence before actual use.
