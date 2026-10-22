# R19 successor gate — DRAFT ONLY

> **NOT_APPROVED / NOT_EXECUTABLE.** This Markdown note is deliberately not a JSON manifest and is not accepted by the production CLI. Do not copy it to `configs/local/`, convert it into a runnable gate, or invoke any runner from it. Phase0 did not create a gate or authorize preflight/live execution.

## Required future binding fields

All placeholders below must be replaced only after the stated future handoffs. A mismatch, missing hash, stale evidence, or changed frozen input blocks the gate.

| Field | Draft binding / required value |
|---|---|
| gate status | `NOT_APPROVED / NOT_EXECUTABLE` |
| replacement scientific SHA | `<NEW_AGENT_EXACT_40_HEX_SHA_PENDING>`; verify local branch and remote ref match, clean tracked tree, reviewed checkout origin |
| Sol exact-SHA review | `<SOL_IMPLEMENTATION_REVIEW_PASS_ARTIFACT_PATH_AND_SHA256_PENDING>`; must review the full base-to-exact delta and production/source/G4 path |
| adjudication | `<IMMUTABLE_SOL_REVIEWED_ADJUDICATION_RECEIPT_PATH_AND_SHA256_PENDING>`; bind prior failed run/unit evidence and separately preserve `source_episode=INCOMPLETE` |
| phase release | `<SEPARATE_SOL_PHASE1_PREFLIGHT_RELEASE_PATH_OR_MESSAGE_ID_PENDING>` |
| fresh user scientific authorization | `<NEW_EXPLICIT_USER_AUTHORIZATION_PATH_AND_SHA256_PENDING>`; scope one successor only, exact replacement SHA, fresh output and all frozen limits |
| independent launch clearance | `<NEW_POST_PREFLIGHT_CLEARANCE_PATH_AND_SHA256_PENDING>`; must not reuse consumed clearance `594bfa...` or its argv hash |
| historical model identity | `NOT_ESTABLISHED` (immutable historical R18 conclusion) |
| prior G3 authorization | original SHA `89b887518c85d22d3176af0b50fb1861b58fb1c3b13a4ecc2b76485a66529b31`; prior entrypoint-repair authorization SHA `026eb1f0b05bcc27a6c901c10d787110cbac0e329551051973dda93e907bdc71`; prior source-contract restart authorization SHA `de634ba310e47d3d49838b8a73d9c6d87f7db87deed042311e3718061a7eb428`. Preserve all; none substitutes for the fresh explicit authorization required later. |
| source-contract repair amendment | SHA `62ff158f5739859266664b1db2e323dca6ea0ad3b8e84134ecbe5fd06c847372`; preserve and require a new exact-SHA review that resolves all findings |
| baseline | R19-B1 manifest SHA `d503f35ae913b137dfff091263bf29c38aa0ade2eea648dc45d7e6cf80da0973` |
| B1 snapshot | `Qwen/Qwen3-8B`, revision `b968826d9c46dd6066d109eabc6255188de91218`; local file manifest must match |
| SFT-P0 adapter | directory SHA `6e403d85b150a74dfcc176f1f180ce4baf6fdacd922d2f96b3ceef0a21100f11`; keep actor/controller identities isolated |
| runtime expectation identity | frozen expectations SHA `dbfb7aa1a1d48d1148ad25be93002e7424d8b22e85422125ed502ac0f4db967e`; runtime package/device/precision and local input identity must be checked in the new reviewed preflight |
| historical G2 runtime receipts | raw file hashes: runtime manifest `306a9e7c2d1b968e2a56e258fcd07aaf7467739460802a2b94c5e20411264916`, preload manifest `6395e65abf266ba5f6a0834023b1da5c3799550b124a75db4d819cf613ee3312`, environment manifest `81ea3b3aea86a850c70c88846f1ce12dfb276cca34aacb9f598ea13e733bf902`; run-context identity hashes are a distinct hash domain |
| baseline amendment | `R19_B1_G2_AMENDMENT.md`, SHA `f8a138045cde125f2c5e08a7d077f75e3838cc7f6d0c67703faffe1166099e49` |
| machine protocol | `configs/experiments/r19_recovery_duration_v1.json`, SHA `3d7d1865c807d12276a8109b06c55da4e9182df0ca05a0b5463f8128dd03e122` |
| source schedule / exclusions | schedule SHA `0be460359fe43193e73f8cb55a8fb19fdba02ea70e3d0809ec5978fad21c8948`; exclusions SHA `70447bba1b2a944d52ab9b4041b2d6ff3d865f4f0abd55d655214c8060ff5367` |
| prior G2 implementation | `92aae1d9b230cc212c6ec4effc99aa468941e69d`, run `33b5563d86d6491a821db224dd38ec3c`; no G2 rerun or smoke relabeling |
| authentic G2 evidence — manifest | `7d8758bcc1fa5e40bb0f1b8f3e13707062104f6a2038673dd3cff93171de4c39` |
| authentic G2 evidence — event ledger | `1456c43f7d3f0a849fe4bb8015164815fd70f4e2813d343449c1a34c2eaebe0c` |
| authentic G2 evidence — branch ledger | `c91f9ff8ab5869bfcdcddd850e038b84c84ad317a7098928a4a09129652e96d3` |
| authentic G2 evidence — offline verification | `80b704131ec4e9738aca25d30512e2d4b84d675ac7537eec27a1083e16cc0b29` |
| authentic G2 evidence — smoke checks | `bf1fed5ff1731fc59280d5d3c55acb540c657eef1f34255bd3816619641f91bb` |
| failed G3 predecessor | run `3d1ccea7e97f4727abf8e216ac6ec498`; authentic exit 1; prior evidence remains immutable; new run must link to this predecessor |
| consumed historical one-use clearance | SHA256 `594bfa7978ee5cc4962c22eb2804f8f4cdbb1f202501330dd1faf993ccdca06b`; canonical argv SHA256 `972ee7903bce0bed38189a8878426558821c81dec689e048a3860a3114c727f5`; never reusable |
| obsolete prior gate / preflight | old `bf31f3` gate SHA256 `63d6634f14fe9f768b3cc8c4120d7b85ba09bd54ca2b8e1f2c103a705137e1ee`; positive preflight was for `bf31f3da...`, not a replacement; neither is reusable |
| cumulative campaign start | 177 generations / 342 environment operations including resets, independently reconciled; no incomplete external operation |
| new preflight record/output | `<FRESH_UNIQUE_PREFLIGHT_RECORD_DIR_AND_ABSENT_OUTPUT_PATH_PENDING>` |
| new live record/output | `<FRESH_UNIQUE_LIVE_RECORD_DIR_AND_ABSENT_OUTPUT_PATH_PENDING>`; must be distinct from predecessor and preflight dirs |
| run identity/retry | supervisor-generated new identity; one successor maximum; `automatic_retry=false`; mismatch/failure stops |
| restart comparison | repeat schedule index 0 only once under the reviewed implementation; frozen restart snapshot SHA `d85d870bfddbad4eb62116d3d5de54a4b7fd4f250634af1c1ed89958e4c400b8`; compare exact reset state, valid-action ordering/map, prompt/rendering, generated bytes/token IDs, parsed selection and mapped command before any action; mismatch stops without retry |
| frozen campaign scope | all 127 TRAIN identities in original order; max 120 initial attempts; max 60 eligible states, quotas 30/15/15, no transfer; K=1..5; horizon 50; quotas/exclusions/prompt/model unchanged |
| physical caps | bind [the cumulative physical ledger](R19_BUDGET_LEDGER_DRAFT.md); current start 177/342; source remainder 8,999 generations/8,999 environment operations; all other original phase/global caps unchanged; count new reset/replay physically |

## Acceptance checklist before any later gate can be approved

1. Exact replacement SHA is independently reviewed PASS by Sol; all production import, first and second source, comparator/hash-contract, complete synthetic G3 and fresh-process G4/report-entry checks required by that review pass.
2. Sol's independent immutable adjudication receipt binds the failed unit and evidence hashes without rewriting the original resolution JSONL, RUNNING manifest, or in-progress registry.
3. Sol separately releases model-free preflight. The authentic pinned supervisor/CLI exits 0 with `PREFLIGHT_ONLY_PASS`, correct source/gate/review/runtime hashes, reviewed module origins, absent output, and zero model/environment/scientific-unit side effects.
4. Independent clearance is issued against that exact preflight/gate/context/argv. Fresh explicit user scientific authorization must match the exact replacement SHA, new output, predecessor, and unchanged experiment limits.
5. Fresh check immediately before launch confirms local/remote SHA match, no competing process/output, inputs unchanged, previous clearance consumed, and a new clearance is unconsumed. No old gate, preflight, or clearance may be reused.
6. The exact index-zero restart comparison passes before any action; it is never rerun for index 1 or later and is charged as a new reset/generation. All source, recovery, replay, logical-branch and campaign caps are enforced cumulatively.

Until these conditions are independently satisfied, every status remains `NOT_APPROVED`; this file is only a preparation aid and grants no permission.
