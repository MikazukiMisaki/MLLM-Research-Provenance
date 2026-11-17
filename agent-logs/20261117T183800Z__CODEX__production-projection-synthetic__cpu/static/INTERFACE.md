# PublicState and projection: static integration contract

This document is a static code reading, not a runtime or scientific result.
No actual task content, model, tokenizer, environment or GPU was accessed or
run. A future CPU integration may call the original functions on wholly
fictional data, but must not claim native physical evidence from those data.

## Source bindings

All paths below are relative to
`/home/lizening/.codex/worktrees/parallel-goal-runtime-9dd/src`.

| Source | SHA256 |
|---|---|
| `self_improvement/si_p3/contract.py` | `2d7b05d5c230cb45c2ad90c7507c11a5c76ce52f7335548c46a48d78e8842239` |
| `sft/protocol.py` | `cb9a8ee23d1208064348810ef3580773ba14403bfaac6a4e7f4a43c5540178a8` |
| `models/action_parser.py` | `0a1c668d590980d1d8cdd4104a2b3c9aa851037fc238a2c73c45b57ab4432fbe` |
| `models/policy.py` | `afbb9544e2ea0c2aa73d3f7dcfbf7e366f1daf6eb95fd4e89fefe0c913dda469` |
| `env/base.py` | `a3ae633aa79c8f80a70629fd398b880ea9c1807e7c219717b98e518b12496abb` |
| `recovery/two_stage.py` | `7fbdfa36268083a167ff1ce04f8dcb33b20024ee115ed65424e1c257b9329629` |
| `recovery/corpus.py` | `14d8ee0f4059f43e76cd94f6511f4ad1e40b4c97377e9bce987d48b59e66a6a1` |

The last two are direct imports of the contract module, not assertions that
projection executes a recovery or that these alone cover every transitive
dependency. These hashes are static source bindings, not loaded-module origin
proof.

## State contract

`PublicState(task_id, family, goal, observation, valid_actions, done=False,
reward=0.0, truncated=False)` is a frozen dataclass (`contract.py:123–155`).
The first four fields must have exact type `str` and be nonempty. Actions must
be an exact tuple of unique nonempty exact strings, with at most 1000 entries;
an empty tuple can be constructed but is not usable for `projection`. `done`
and `truncated` must be exact booleans; reward must be an exact finite int or
float. `ended` is their logical OR. `to_dict()` emits the same fields with
`valid_actions` as a list; `from_dict()` requires exactly the declared field
set and a list, then revalidates the tuple. `PublicState` itself requires a
nonempty family but does not require it to be in the separate `FAMILIES` list.

## Projection and history

`projection(state, history)` (`contract.py:158–173`) rejects ended states and
empty actions, builds a real `ActionRequest` using a `Task` with the state
identity/goal, literal split `train` and family, then calls `sft_p0_prompt`,
`action_id_mapping` and `validate_public_prompt`. A literal split in this
wrapper does not demonstrate historical exposure, data provenance or task
independence.

Actions are mapped from the original tuple order as `A000`, `A001`, …; no
sorting or one-based offset. Returned keys are `goal`, `observation`,
`recent_history`, `valid_actions`, `public_prompt`, `public_prompt_sha256`
and `action_map`. The SHA256 is of UTF-8 prompt bytes. `recent_history` is
the final four input `(observation, action)` pairs converted to lists; the
request receives a tuple of the supplied history. The function assumes the
history supports sequence operations and the expected pair structure; it does
not explicitly perform a separate comprehensive history-type validation.

`sft_p0_prompt` freezes `history_window=4` (`sft/protocol.py:56–88`). For each
retained pair it renders its action and a result: the next history item's
observation, or the current observation for the final pair. Empty history
renders `(none)`. The full indexed action block preserves current order.
`validate_public_prompt` checks nonempty content, forbidden marker strings,
and the exact indexed block (`sft/protocol.py:109–118`). These checks do not
prove that history is genuine, public-state observations came from an actual
environment, or hidden-state equivalence holds.

For a CPU-only fixture, use clearly fictional goal/observation, two unique
commands, five fictional `(observation, action)` history pairs and actual
`PublicState`/`projection`. Assert last-four behavior, `A000/A001` order,
the rendered next-observation result logic and UTF-8 hash; exercise invalid
duplicate actions, ended and empty-action states separately. This would test
the software contract only. No change to prompt or frozen baseline is implied.
