# R19 Luna execution readiness — Sol Phase0 addendum

**Status: `PHASE0_READ_ONLY_COMPLETE / NOT_READY_FOR_EXECUTION`.** This is an evidence addendum to the previously finalized [readiness report](../2026-10-22T230530Z__CODEX__r19-luna-readiness__d7c2ad/R19_LUNA_EXECUTION_READINESS.md), SHA256 `ed042904cfbd746a1aa29c98b66230018d803c85b14f869004ebd8834490e940`; it reuses that report for still-valid inspections and adds the independent Sol audit and current point-in-time checks. It is not a preflight receipt, approval, launch gate, or execution authorization.

## Handoff and current scientific repository state

- Sol handoff `LUNA_TASK.md`: SHA256 `d0f740910dde5f5d7809b35ff73126f681af66fd4413cdc81d92adb4d3a31db1`; sibling `INDEPENDENT_AUDIT.md`: `6fafc7d0776c988c6618d2a5420660b587e48d79ef56078db05e514568bb9a5a`.
- Scientific repository/worktree: `/home/lizening/wt-r19-recovery-duration-v1`; current branch `codex/r19-source-contract-repair`; HEAD and `origin/codex/r19-source-contract-repair` are both `da7d348ffd3677d619dd31357e1e1e3cca28c9ec`.
- The frozen `codex/r19-recovery-duration-v1` remote remains at `bf31f3da430ffc35bd17fc380e1752adce6d1467`; the repair remote remains at `da7d348ffd3677d619dd31357e1e1e3cca28c9ec`. A new local developer worktree appeared during this Phase0 observation at `/home/lizening/wt-r19-source-contract-review-fixes`, branch `codex/r19-source-contract-review-fixes`, still based at HEAD `da7d348ffd3677d619dd31357e1e1e3cca28c9ec`. Its status shows modified `scripts/analyze_r19_recovery_duration.py`, `scripts/run_r19_experiment.py`, `tests/test_r19_source_contract.py`, and untracked `tests/test_r19_source_pipeline.py`; no remote branch ref or replacement commit SHA is available yet. These likely represent active implementation work, but their contents were not inspected, staged, or touched. The reviewer worktrees at `ef2328f`, `51ec074`, and `da7d348` remain detached and untouched.
- The main scientific worktree has one untracked file, `R19_IMPLEMENTATION_ONBOARDING.md`, not present in the earlier readiness observation. It was neither read, modified, nor staged. Do not infer that it is a reviewed implementation or candidate commit.
- `da7d348` remains `IMPLEMENTATION_REVIEW=FAIL` with one blocking and two major findings. Its review artifact is `/home/lizening/research-notes/agent-logs/2026-10-22T225858Z__ASTRA__r19-source-contract-exact-review__da7d348/independent_review.json`, SHA256 `8fcd731bcbfd01b2e89228e79f70834e15c57a5f3502e1a68f559355ab2e3c40`. The narrow `G2_CARRY_FORWARD=PASS` applies only to authentic earlier G2 records and unchanged smoke semantics; it is not implementation approval, preflight eligibility, or launch clearance.

The unresolved findings are: **R19-SRC-01 (BLOCKING)** the restart comparator is not restricted to the first scheduled source and collides with its existing receipt at index 1 after a synthetic reset/generation and before any action; **R19-SRC-02 (MAJOR)** a clean standalone process cannot import the comparator's runner dependency from outside the checkout; **R19-SRC-03 (MAJOR)** the persisted trajectory digest differs from canonical recomputation because comparison metadata is appended after hashing. Exact replacement review must resolve all three with production-path tests; test count or a one-episode synthetic pass alone is insufficient.

## Failed source unit and physical cost

Sol's independently produced `evidence/state_and_cost_audit.json` has SHA256 `b666f5d2d69171a0305c6657f952d70f5ab304295c13b171fc77690a9cb05dab`. It reran the production raw-ledger validator against the pinned failed predecessor, successful G2, and failed G3 journals. Totals are **177 completed physical generations; 330 completed non-reset environment operations; 12 resets; 342 environment operations including resets; 0 incomplete external operations**. The failed G3 increment is exactly one generation (267 input + 5 generated tokens), one reset, zero action steps, zero completed source episodes, zero recovery attempts/eligible prefixes/branches, and zero incomplete external operations.

Failed live run `3d1ccea7e97f4727abf8e216ac6ec498` truly exited 1 from `subprocess.returncode`; its supervisor status is failed and not supervisor-interrupted. The four-event journal contains reset start/completion and generation start/completion only. The authentic runner traceback identifies the collector interface error on exact execution SHA `bf31f3da430ffc35bd17fc380e1752adce6d1467`.

The original run output is preserved. Its journal, manifest, registry, empty branch ledger, supervisor receipts and audit hashes are:

| Evidence | SHA256 |
|---|---|
| `execution_events.jsonl` | `fde95fcd72f1c4ac6409fab7f2112654e145f6184fefec690cae58ad345f1cd7` |
| `execution_manifest.json` | `f5d3efa6c17abea3d944d7dea01099210d846eb8ed107057ec24502bbb51d2df` |
| `unit_registry.json` | `870923242ae585c66cbcffa554528ab3d92cf98fc4d87dee2c4d408f5f6ba800` |
| `branches.jsonl` (empty) | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| supervisor `runner.log` | `ee7c6010edf0e46bcba2969cdddf236e7c6d23830d2bd92e88593d7a21a7bbcd` |
| supervisor `runner_exit.json` | `a802079398fd415765b8f6b8685fec998325625da733011ff7a9ce11459a9386` |
| supervisor `supervisor_status.json` | `e2a70bf670376b648e52357376fa88f3a7a3cac92b41a5c628bd4ad251353913` |
| supervisor `launch_context.json` | `6b8933ed06db1b2e74f1b921ca13e6f73842b18e7a0c8217381a809ed4ea180e` |
| independent failure audit | `8eb1248c1d863674119813ba1f90ba3ca6834bb1906cb2aa67acc6a4e087fe34` |
| prior append-only unit resolution JSONL | `58783ba60b076ee190dccb0875aac65891d7e1c811e00fbe6303ca65896369d9` |

The physical reset and generation outcomes are determinate. The enclosing source episode is nevertheless incomplete: original registry status remains `in_progress`, original execution manifest status remains `RUNNING`, and no action/source-completion event exists. Those bytes are retained as failure evidence, not treated as a live process. The old resolution event's `review_status=PENDING_EXACT_SHA_REVIEW` remains unchanged; only a separate immutable Sol adjudication/review receipt may reconcile that marker. Luna made no registry calls and did not modify any original run evidence.

The scheduled index-zero identity remains `pick_and_place_simple-Pencil-None-GarbageCan-316/trial_T20190907_165839_449092`, seed 30000. It must not be skipped or substituted; any authorized successor's repeated reset and generation are newly charged physical cost.

## Frozen R19-B1 identity and runtime check

The earlier readiness report's frozen schedule/quota checks remain applicable. This addendum freshly rechecked current byte hashes and local runtime metadata without loading model weights or constructing ALFWorld:

| Frozen input | Current SHA256 / identity | Result |
|---|---|---|
| R19-B1 baseline manifest | `d503f35ae913b137dfff091263bf29c38aa0ade2eea648dc45d7e6cf80da0973` | matches frozen record |
| prior G2 amendment `R19_B1_G2_AMENDMENT.md` | `f8a138045cde125f2c5e08a7d077f75e3838cc7f6d0c67703faffe1166099e49` | matches |
| R19 machine protocol | `3d7d1865c807d12276a8109b06c55da4e9182df0ca05a0b5463f8128dd03e122` | matches |
| source schedule | `0be460359fe43193e73f8cb55a8fb19fdba02ea70e3d0809ec5978fad21c8948` | matches |
| exclusion manifest | `70447bba1b2a944d52ab9b4041b2d6ff3d865f4f0abd55d655214c8060ff5367` | matches |
| original G3 authorization | `89b887518c85d22d3176af0b50fb1861b58fb1c3b13a4ecc2b76485a66529b31` | unchanged |
| entrypoint-repair authorization | `026eb1f0b05bcc27a6c901c10d787110cbac0e329551051973dda93e907bdc71` | unchanged |
| source-contract restart authorization | `de634ba310e47d3d49838b8a73d9c6d87f7db87deed042311e3718061a7eb428` | unchanged; not sufficient for a future launch by itself |
| source-contract repair amendment | `62ff158f5739859266664b1db2e323dca6ea0ad3b8e84134ecbe5fd06c847372` | unchanged |
| local ALFWorld config | `e90f93eb4604a473b6eb4a259a19ef1ca3c296bba1771ba70a1c9b0edbc99700` | exists and matches prior receipt |

The pinned local Qwen3-8B snapshot is revision `b968826d9c46dd6066d109eabc6255188de91218`. All five model shard hashes and all seven config/tokenizer file hashes were read directly from the local files and matched the frozen baseline manifest; the files were hashed, never deserialized or loaded into a model. Direct digests are recorded in [FROZEN_FILE_HASH_CHECKS.md](FROZEN_FILE_HASH_CHECKS.md). The SFT adapter directory was freshly hashed with the repository's `directory_sha256` algorithm (11 files) and matched `6e403d85b150a74dfcc176f1f180ce4baf6fdacd922d2f96b3ceef0a21100f11`. The pinned Python is 3.10.20; observed package versions matched the historical manifest: torch 2.6.0+cu124, transformers 4.56.2, peft 0.17.1, accelerate 1.10.1, TRL 0.23.0, ALFWorld 0.4.2, TextWorld 1.7.0, NumPy 1.26.4, tokenizers 0.22.2. The adapter/data/config paths exist. This was inventory only; no model or environment runtime was initialized.

The R19 schedule remains 127 distinct contiguous TRAIN identities, indices 0–126, including the failed identity at index 0. Frozen limits remain 120 initial attempts; at most 60 eligible states (30 failure / 15 success-control / 15 random-control; no transfer); K=1..5; total horizon 50. Historical R18 identity remains `NOT_ESTABLISHED` and is not changed.

Authentic G2 execution SHA is `92aae1d9b230cc212c6ec4effc99aa468941e69d`, run ID `33b5563d86d6491a821db224dd38ec3c`; G2 is not to be rerun. Its five carry-forward evidence hashes are listed in [the NOT_APPROVED gate draft](R19_NOT_APPROVED_GATE_DRAFT.md). They bind prior evidence only; they are not a fresh G2 or smoke receipt.

## Processes, outputs, gates, and current release

The current process check found no Python process whose command line was an R19 supervisor/runner; the GPU compute-process query returned no process. Sol's independent process inventory also records `r19_processes=[]` and no GPU compute processes. A broad pattern query once matched its own diagnostic shell because the search expression was in the command line; this was not counted as an R19 process. Three known R19 runtime directories remain: two historical G2 directories and the one failed G3 directory above; no successor output exists.

No new gate was created under `configs/local/`; no new scientific output or supervisor record was created; no preflight was run. The previous one-use clearance was consumed by run `3d1ccea7e97f4727abf8e216ac6ec498` and is unusable. The older `bf31f3` preflight/gate are not reusable. This task creates Markdown drafts in this provenance directory only, not a production-readable gate.

The shared provenance repository advanced from the previously observed `68d7c88768b23892b5119152d6580e5ee956e4d5` to Sol's published `a5f59f0a2b3c46bdb15e8f8deeb05f6a9b5a1b6d` while this task was in progress; Sol's finalized record and index row were preserved. Additional Sol-owned untracked directories appeared (`2026-10-22T231628Z__CODEX__r19-source-contract-review-fixes__implementation`, `2026-10-22T232008Z__SOL__r19-additional-contract-scope__677223`, and `2026-10-22T232351Z__SOL__r19-alias-validator-scope__535726`); their contents were not inspected or staged. The new Luna record will be published on the current main base with only its own task files and index row staged.

The draft gate, argv/environment allowlist, physical budget and adjudication proposal are separate files in this directory. Every draft is explicitly `NOT_APPROVED / NOT_EXECUTABLE`; they contain unresolved placeholders and must not be passed to the runner.

## Current boundary and dependencies

This task performed Phase0 read-only preparation/provenance only. No code, tests, model, prompt, dataset, scientific protocol, frozen configuration, registry, manifest, old resolution event, local gate, or run output was edited. No tests, model loads/generations, ALFWorld construction/reset/step, G2 rerun, preflight, G3 launch, or G4 analysis were performed. Held-out tasks and training were not used.

Next authorized sequence is: New Agent publishes the implementation; Sol reviews the exact replacement SHA and accepts an immutable failed-unit adjudication; Sol separately releases Phase1 model-free preflight; Luna performs the authentic preflight and reports receipt/argv/gate to Sol; independent launch clearance and fresh explicit user scientific authorization are then both required before any single live successor. No clearance or authorization is inferred in this report. Current state: `NOT_READY_FOR_EXECUTION`.
