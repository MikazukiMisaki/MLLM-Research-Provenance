# Bounded first-source event binding record

Status: `READ_ONLY_BOUNDING_COMPLETE`; historical internal TextWorld pool seed/game RNG counter remain unobserved. No source PASS, runtime clearance, or execution authorization is inferred.

Completed: 2026-10-26T12:19:24Z. Start timestamp was not captured by the dispatch receipt and is not inferred here.

The capture examined only the first line of the already completed R19 trajectory, its explicitly referenced reset, six transition receipts, source-episode completion receipt, and first generation receipt (needed to bind the first prompt receipt). It streamed the event journal prefix and stopped when all nine referenced IDs were found: 27 lines / 149,225 bytes scanned. It did not invoke a full-journal helper, read another source episode, or copy prompt/action/command/observation/state/token values into the report.

## Raw evidence

- Trajectory: `/home/lizening/wt-r19-recovery-duration-v1/artifacts/runtime/r19_b1_g3_successor_after_3d1ccea7_20261023T002200Z/source_trajectories.jsonl`; first record offset 0, 35,486 bytes including newline, SHA-256 `465bff755ba34c18acca299470cd7c3a40455cb395df3e6fe43eee99119a7c73`.
- Source identity: run `260422ac02bd42a8b2929d7ef240526b`; task `pick_and_place_simple-Pencil-None-GarbageCan-316/trial_T20190907_165839_449092`; split `train`; family `pick_and_place_simple`; schedule index 0; recorded nominal seed 30000; six transitions.
- Event-journal header: offset 0, 2,832 bytes, sequence 1, kind `environment_operation_started`, event ID `321e9c9675f6e1e42aa1315df21bd7573cbd75800413b1a52acbbf718ee09c90`, line SHA-256 `a1bad56c9468ea8d76b983cc37741d0b56d05bf4d1a898c8befbece45305aa84`; run ID/evidence class match the trajectory's containing run (`live`).
- The per-event original raw line path, byte offset, byte length, sequence, event ID, SHA-256, kind, run identity, safe source identity scalars, and reference cross-bind booleans are recorded in `FIRST_SOURCE_EVENT_BINDINGS_V2.json`.

## Cross-bind result

All nine referenced IDs were found exactly. The reset is sequence 2 (`environment_operation_completed`) and directly binds the task ID, train split, schedule index 0, and seed 30000. The six transition IDs match the six per-step `r19_transition_event_id` references in order; each event has the same run ID, train split, and schedule index 0. The first generation ID is sequence 4 (`generation_completed`) and equals the first step's `r19_generation_event_id`. The `source_episode_completed` event is sequence 27 and directly binds the same task ID, split, family, schedule index, and seed. Its embedded trajectory agrees with the final first-row identity and other fields, with exactly two structural differences: `metadata.r19_source_event_refs` and `metadata.source_trajectory_sha256`; report hashes are retained and no body values are emitted.

The first generation receipt is included only as a reference/hash-bound event, not as a prompt or output transcription. This permits locating the original first-generation evidence without expanding the report with content.

## Limits and truthful incompleteness

The historical reset receipt still does not record the internal TextWorld pool seed or game RNG counter. The nominal seed must not be substituted for either. The full event journal was not hashed or validated; the scan proves only the requested bounded referenced records and their captured line hashes. The initial extraction attempt exited 1 because it assumed event sequence 0; the actual header is sequence 1. Its authentic failure is preserved in `FIRST_SOURCE_EVENT_BINDING_COMMAND_RECEIPTS.json`; the corrected bounded capture exited 0.

The first produced JSON `FIRST_SOURCE_EVENT_BINDINGS.json` (SHA-256 `6b6c1fa6f548fb9b338a6002095523e912d6e24140918d56086de816dae88b8b`) is retained as a superseded local-only intermediate: it lacked the structural-difference explanation and repeated the embedded-row comparison on every event. The final `FIRST_SOURCE_EVENT_BINDINGS_V2.json` supersedes it; neither changes raw evidence. The initial failed scan and this intermediate are both recorded in the command receipts.

The original report/addendum, all previous evidence, historical source files, shared INDEX/inventory, and provenance repository were left unchanged. No model/tokenizer/CUDA/environment/SSH, project validator/test, preflight, supervisor, or science call occurred. No launch release exists.
