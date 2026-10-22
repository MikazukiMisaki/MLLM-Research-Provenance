# R19 Luna execution readiness

**Status:** `NOT_READY_FOR_EXECUTION` — read-only preparation complete; waiting for a corrected implementation, exact-SHA review PASS, reconciled failure-unit adjudication, and explicit new execution authorization.

**Prepared:** 2026-10-22 23:05 UTC by Codex/Luna, Experiment Operator & Provenance Owner.

## Executive result

The failed G3 run is conclusively stopped, with one completed model generation and one completed reset, no action step, and no incomplete external operation. Its source unit did not complete. The current source-repair candidate is not approved: the independent exact-SHA review of `da7d348ffd3677d619dd31357e1e1e3cca28c9ec` returned `IMPLEMENTATION_REVIEW=FAIL`, `G2_CARRY_FORWARD=PASS` only for the authentic prior G2 evidence and unchanged smoke semantics, and `positive_preflight_eligible=false`. No launch clearance was issued.

No New Agent replacement commit was visible in the local R19 worktrees or remote R19 refs at the time of this read-only check. No new gate was created, no preflight was run, and no model or ALFWorld operation was performed. The key real-source acceptance remains unmet: completed source episodes in the failed live run = 0.

## Git, worktree, and process state

- Scientific worktree: `/home/lizening/wt-r19-recovery-duration-v1`.
- Branch / HEAD: `codex/r19-source-contract-repair` / `da7d348ffd3677d619dd31357e1e1e3cca28c9ec`.
- `origin/codex/r19-source-contract-repair` resolved to the same SHA; the worktree was clean.
- Other registered task worktrees included detached R19 reviewer checkouts at `ef2328f`, `51ec074`, and `da7d348`; no separate New Agent R19 worktree or replacement ref was observed.
- No process matched the R19 supervisor/runner entrypoints. The recorded historical PIDs (supervisor `759377`, child `759380`) were absent from the process table. The only G3 output directory found was the failed run below; the two other R19 runtime directories were the known G2 runs.
- No claim is made about unrelated system processes. The check covered R19 launch/runner processes and available R19 ledgers/output directories.

## Failed live run and physical cost

- Run ID: `3d1ccea7e97f4727abf8e216ac6ec498`.
- Failed implementation SHA: `bf31f3da430ffc35bd17fc380e1752adce6d1467` (the current `da7d348` is a later repair candidate, not the run's code).
- Output: `artifacts/runtime/r19_b1_g3_pilot_after_a0de515d7e104101bf8157175ea3d995_20261022T190221Z`.
- Supervisor receipt: actual child exit `1`, source `subprocess.returncode`, status `failed`, `interrupted_by_supervisor=false`; completed at `2026-10-22T19:11:25.157792Z`. The runner log records `AttributeError: 'dict' object has no attribute 'selection_status'` in `_collect_one_source`.
- Execution ledger has exactly four chained events: reset started/completed and generation started/completed. The generation consumed 267 input and 5 generated tokens (272 total). There is no environment-step event and no `source_episode_completed` event.
- Independently audited delta: **1 generation, 1 reset, 0 action steps, 0 incomplete operations, 0 completed source episodes**. Cumulative G2 + failed G3 remains **177 generations / 342 environment operations including resets** (G2: 176 / 341; failed G3 increment: 1 / 1).
- Raw hashes: `execution_events.jsonl` `fde95fcd72f1c4ac6409fab7f2112654e145f6184fefec690cae58ad345f1cd7`; `execution_manifest.json` `f5d3efa6c17abea3d944d7dea01099210d846eb8ed107057ec24502bbb51d2df`; `unit_registry.json` `870923242ae585c66cbcffa554528ab3d92cf98fc4d87dee2c4d408f5f6ba800`; empty `branches.jsonl` `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.
- Supervisor hashes: `runner.log` `ee7c6010edf0e46bcba2969cdddf236e7c6d23830d2bd92e88593d7a21a7bbcd`; `runner_exit.json` `a802079398fd415765b8f6b8685fec998325625da733011ff7a9ce11459a9386`; `supervisor_status.json` `e2a70bf670376b648e52357376fa88f3a7a3cac92b41a5c628bd4ad251353913`; `launch_context.json` `6b8933ed06db1b2e74f1b921ca13e6f73842b18e7a0c8217381a809ed4ea180e`.
- Independent failure audit: `/home/lizening/research-notes/agent-logs/2026-10-22T191409Z__ASTRA__r19-g3-failure-audit__3d1ccea7/failure_audit.json`, SHA256 `8eb1248c1d863674119813ba1f90ba3ca6834bb1906cb2aa67acc6a4e087fe34`.
- The original registry still says `in_progress` and the execution manifest still says `RUNNING`. These are preserved failure artifacts, not evidence of an active process; the supervisor receipt and absent PIDs establish the run ended.

## Evidence-based unit adjudication proposal

The evidence supports the narrow disposition `KNOWN_FAILED_SOURCE_CONTRACT_AFTER_GENERATION_BEFORE_ACTION`, with unit completion status `INCOMPLETE_PRESERVED_IN_ORIGINAL_REGISTRY` and physical outcome `DETERMINATE_KNOWN_FAILURE`. Do not call this a completed source episode; do not mark it successful; do not edit the original registry, manifest, or raw ledger.

An append-only resolution event is already present at `configs/experiments/r19_b1_g3_source_unit_resolution_events_v1.jsonl` (SHA256 `58783ba60b076ee190dccb0875aac65891d7e1c811e00fbe6303ca65896369d9`). The exact-SHA reviewer records `known_failed_disposition=PASS_KNOWN_FAILED_NO_ACTION_NO_UNCERTAINTY`. However, that existing event still contains `review_status=PENDING_EXACT_SHA_REVIEW`. This read-only task did not rewrite it. Sol/New Agent should reconcile the stale review marker through a new append-only review/adjudication receipt or an explicitly reviewed versioned amendment, while preserving the original bytes and unit identity.

The scheduled index-zero identity remains `pick_and_place_simple-Pencil-None-GarbageCan-316/trial_T20190907_165839_449092`, nominal seed 30000. Any later restart must retain index 0 and charge the repeated reset/generation; it must not substitute or skip the task.

## Frozen R19-B1 and runtime inventory

Observed frozen hashes in the current worktree:

| Item | SHA256 / identity |
|---|---|
| R19-B1 baseline manifest | `d503f35ae913b137dfff091263bf29c38aa0ade2eea648dc45d7e6cf80da0973` |
| Baseline model | Qwen/Qwen3-8B, snapshot revision `b968826d9c46dd6066d109eabc6255188de91218` |
| SFT adapter directory (frozen receipt hash) | `6e403d85b150a74dfcc176f1f180ce4baf6fdacd922d2f96b3ceef0a21100f11` |
| Machine protocol | `3d7d1865c807d12276a8109b06c55da4e9182df0ca05a0b5463f8128dd03e122` |
| Source schedule | `0be460359fe43193e73f8cb55a8fb19fdba02ea70e3d0809ec5978fad21c8948` |
| Exclusion manifest | `70447bba1b2a944d52ab9b4041b2d6ff3d865f4f0abd55d655214c8060ff5367` |
| Original G3 authorization | `89b887518c85d22d3176af0b50fb1861b58fb1c3b13a4ecc2b76485a66529b31` |

Historical R18 model equivalence remains `NOT_ESTABLISHED`; this inspection neither changes nor reopens that conclusion.

Read-only schedule check found **127 unique canonical TRAIN identities**, contiguous schedule indexes 0–126, with index 0 matching the failed unit. Frozen G3 scope remains 120 initial attempts; at most 60 eligible states (failure 30, success control 15, random control 15; no quota transfer); K=1..5; total horizon 50.

G2 remains PASS at execution SHA `92aae1d9b230cc212c6ec4effc99aa468941e69d`, run ID `33b5563d86d6491a821db224dd38ec3c`. Do not rerun it. The current review permits carry-forward only of those authentic G2 records and unchanged smoke semantics; it does not approve the G3 candidate.

The original phase ceilings are source 9,000 generations / 9,000 environment operations; initial attempts 240 / 5,520; common-path extension 240 / 2,940; logical branches 17,100 / 18,000; replay-gate generation ceiling 0 and environment ceiling 5,400. After the observed failed source call/reset, the source headroom is 8,999 / 8,999. Other phase limits and global ceilings remain as frozen: 26,988 generations and 41,260 environment operations cumulatively including G2; projected maximum 26,756 / 41,201. No quota or budget transfer is permitted.

Runtime facts are separated from runtime re-execution:

- The pinned interpreter exists at `/home/lizening/miniconda3/envs/alfworld-self-improve/bin/python`; current package metadata matched the last recorded runtime manifest (Python 3.10.20; Torch 2.6.0+cu124; Transformers 4.56.2; PEFT 0.17.1; ALFWorld 0.4.2; TextWorld 1.7.0; remaining package versions are in that manifest).
- The local ALFWorld config exists and hashes to `e90f93eb4604a473b6eb4a259a19ef1ca3c296bba1771ba70a1c9b0edbc99700`; the configured adapter directory and data root exist. No model weights were reloaded or rehashed and no environment was constructed.
- Raw on-disk hashes from the last live run: `runtime_manifest.json` `306a9e7c2d1b968e2a56e258fcd07aaf7467739460802a2b94c5e20411264916`; `runtime_manifest_preload.json` `6395e65abf266ba5f6a0834023b1da5c3799550b124a75db4d819cf613ee3312`; `environment_manifest.json` `81ea3b3aea86a850c70d88846f1ce12dfb276cca34aacb9f598ea13e733bf902`. Separately, the execution manifest's run-context identity fields were runtime `f4c6b5eac9b1558b82e0e626ea4412437ff924f839a62f8fe3962a141effe7f7`, preload `64ebf4667da70dc4acd0a49b645bb6b6d4c3e1fe5d3e8e6351a8bf66f148ab9a`, and environment `2a1e4d35db31cdd0d8adcdf15df60b577a79b3b7e51c74c2546ed97463c178d0`. It recorded the pinned revision, BF16/SDPA, separate actor/recovery model objects and SFT adapter isolation on an A40. These are historical receipts, not a claim of a fresh model load.
- A previous real `PREFLIGHT_ONLY_PASS` exited 0 but was bound to code SHA `bf31f3da430ffc35bd17fc380e1752adce6d1467` and gate SHA `63d6634f14fe9f768b3cc8c4120d7b85ba09bd54ca2b8e1f2c103a705137e1ee`. Existing ignored gates bind still older SHAs (`bf31f3` and `ef2328f`). None is valid for a replacement implementation; do not reuse them.

## Independent review state

Review artifact: `/home/lizening/research-notes/agent-logs/2026-10-22T225858Z__ASTRA__r19-source-contract-exact-review__da7d348/independent_review.json`, SHA256 `8fcd731bcbfd01b2e89228e79f70834e15c57a5f3502e1a68f559355ab2e3c40`.

It inspected exact SHA `da7d348…` and reproduced three blockers:

1. **Blocking — restart comparator is not one-time.** After the synthetic index-zero source episode completes, schedule index 1 repeats the comparator and collides with the existing comparison sidecar after a reset and generation; the 127-source run cannot progress.
2. **Major — clean-process G4 import failure.** A fresh standalone analyzer process cannot resolve `scripts.run_r19_experiment` from outside the repository, despite in-process tests passing.
3. **Major — trajectory digest inconsistency.** The trajectory hash is calculated before adding `metadata.source_restart_comparison_sha256`; the persisted row declares `17a8aea3…dee74` while production recomputation yields `6458ff77…b45532`.

The review reports a synthetic single-episode source-to-validator path PASS, but it is not a real source episode. Its final gate is FAIL, `positive_preflight_eligible=false`, `launch_clearance_issued=false`. No real first source episode completed; no usable K1–K5 result or G4 efficacy result exists.

During this preparation, a separate Sol audit evidence directory appeared at `/home/lizening/research-notes/agent-logs/2026-10-22T230825Z__SOL__r19-independent-audit-task-handoff__599954/`. Its unfinalized `probes.log` independently reports a synthetic first-source integration pass, the same second-source comparator collision (one synthetic reset/generation, zero actions), the same clean-process G4 import failure, and a trajectory digest mismatch on its own fixture. This directory had no final `RECORD.md` or PASS at inspection and was not modified or staged; it is supplemental in-progress evidence, not a review or authorization.

## Preflight and new gate preparation — not executed

No new gate was created. Once the above blockers are repaired and an exact-SHA review PASS, unit adjudication is reconciled, and a new explicit execution authorization is provided, the next gate should be a new ignored file under `configs/local/` bound to:

- replacement implementation SHA and exact review artifact/hash;
- original G2 execution SHA/run and authentic evidence hashes (without claiming a new G2 smoke);
- failed run ID, authentic event/registry/manifest/supervisor/failure-audit hashes, append-only unit disposition, and cumulative 177/342 start;
- unchanged baseline/model/adapter, protocol, schedule, exclusions, runtime expectations, and all frozen quotas/caps;
- one successor identity, fresh output path, source-index-zero compare-before-first-action rule, source headroom 8,999/8,999, and no retry/second campaign.

Then, and only after the formal authorization/review handoff, run the same pinned interpreter and production supervisor/CLI in explicit `preflight_only` mode with PYTHONPATH, PYTHONHOME, and VIRTUAL_ENV absent. Require authentic exit 0 and `PREFLIGHT_ONLY_PASS`, exact module origins and source/gate/runtime/review hashes, output absent, and zero model/environment/scientific-unit side effects. The historical bf31 preflight cannot satisfy this gate. After a successful fresh preflight, wait for the separate formal launch handoff; do not treat a queued command as a started run. Any comparator mismatch or real successor failure stops without retry.

Command shape prepared only (not executable until all placeholders are replaced by the reviewed authorization; not run):

```text
/home/lizening/miniconda3/envs/alfworld-self-improve/bin/python \
  /home/lizening/wt-r19-recovery-duration-v1/scripts/launch_r19_supervised.py \
  --record-dir /home/lizening/research-notes/agent-logs/[fresh-preflight-record]/supervisor \
  --evidence-class preflight_only \
  --supersedes-run-id [authorization-bound-predecessor] \
  -- \
  /home/lizening/miniconda3/envs/alfworld-self-improve/bin/python \
  /home/lizening/wt-r19-recovery-duration-v1/scripts/run_r19_recovery_duration.py pilot \
  --protocol /home/lizening/wt-r19-recovery-duration-v1/configs/experiments/r19_recovery_duration_v1.json \
  --manifest /home/lizening/wt-r19-recovery-duration-v1/configs/local/[new-reviewed-gate].json \
  --output /home/lizening/wt-r19-recovery-duration-v1/artifacts/runtime/[fresh-absent-successor-output] \
  --adapter /home/lizening/Alfworld-Self-Improvement-Project/artifacts/runtime/model-artifacts/sft-policy-bootstrap/full/final_adapter \
  --data-root /home/lizening/alfworld_data \
  --config /home/lizening/wt-r19-recovery-duration-v1/configs/local/r19_b1_g2_alfworld.yaml \
  --preflight-only \
  --preflight-receipt /home/lizening/research-notes/agent-logs/[fresh-preflight-record]/pilot_preflight_receipt.json
```

## Provenance and disclosure

The provenance repository is `/home/lizening/research-notes`; at inspection time local `main` and `origin/main` both equaled `d54ebb7eec421f6e5c70565f895adfdbe6498ee2`. The original G3 failure bundle, failure audit, and exact-SHA review are already tracked there. The old raw evidence remains unchanged. This readiness report contains hashes, bounded metadata, and local evidence references only; it does not copy model weights, adapters, datasets, caches, credentials, or raw observation/generation payloads.

For this report, maintain the existing provenance protocol: unique task directory; `RECORD.md`, command summary and file hash inventory; index row; secret scan; stage only this task's safe files; push `MLLM-Research-Provenance/main` without force; verify local and remote SHAs. Preserve unrelated untracked provenance directories.

## Final state for handoff

`R19_LUNA_EXECUTION_READINESS=NOT_READY_FOR_EXECUTION`.

Luna performed read-only inspection and provenance preparation only. **No scientific code/configuration was changed; no tests, model loads/generations, ALFWorld constructions/resets/steps, G2 rerun, G3 preflight, G3 launch, or G4 analysis were performed in this readiness task.** Await New Agent's corrected implementation, Sol's exact-SHA review PASS, reconciled failure-unit disposition, and explicit new execution authorization/formal handoff.
