# R19 Phase1 preparation proposal — draft only

**Status: PREPARATION_PROPOSAL_ONLY / NOT_APPROVED / NOT_EXECUTABLE.** This is not a production gate and authorizes no checkout switch, supervisor, preflight, model, ALFWorld, live G3, G2, or G4 operation. Exact argv and paths below are proposed for Sol's separate Phase1 release; revalidate every path, byte identity, and absence immediately before any later release.

## 1. Current evidence and checkout state

- Reviewed implementation: `2da980f631badc25086d12db60d128ff507d3ae6`, branch `codex/r19-source-contract-review-fixes`; dedicated worktree `/home/lizening/wt-r19-source-contract-review-fixes` is tracked-clean and matches remote `origin/codex/r19-source-contract-review-fixes`.
- Original designated execution worktree: `/home/lizening/wt-r19-recovery-duration-v1`, restored at `da7d348ffd3677d619dd31357e1e1e3cca28c9ec`, branch `codex/r19-source-contract-repair`, matching remote. Its only untracked file is `R19_IMPLEMENTATION_ONBOARDING.md`; tracked files are unchanged. Do not add an ignore rule.
- Independent review: `/home/lizening/research-notes/agent-logs/2026-10-22T234140Z__SOL__r19-exact-sha-independent-review__2da980f_198732/independent_review.json`, SHA256 `85a694f24da347dcb0e6f09f4fe0d33afefb46abf1d5b0063361870c3fe7820b`; implementation and G2 carry-forward PASS. It is a prerequisite only, not a Phase1 release, preflight result, launch clearance, or new user live authorization.
- Immutable adjudication: `/home/lizening/research-notes/agent-logs/2026-10-22T234140Z__SOL__r19-exact-sha-independent-review__2da980f_198732/known_failed_adjudication.json`, SHA256 `3abea8efc2bd9d88677d71031aef0a21e905e6dd7b3ed75d06f1486d4c6718e0`; binds the preserved failed source unit. Keep its source episode incomplete and preserve all predecessor raw bytes/statuses.
- Original onboarding report SHA256 is `27be0ca4c3e5abffa4fa492aaf47bf087328f41718fcc5f774c43fdf5b1c4e7e`. A byte-identical mode/timestamp-preserving copy is at `preserved/R19_IMPLEMENTATION_ONBOARDING.md` with the same SHA256. Original remains untouched in the execution worktree.
- No R19 runner/model/ALFWorld process was observed during the read-only process check. No output or supervisor record was created.

## 2. Safe exact-SHA staging and restoration plan

Do not stage by silently switching the shared execution worktree. If Sol later releases Phase1:

1. Reconfirm no process is using the execution root; recheck both local/remote refs, tracked diff, ignored local files, onboarding source SHA, archive SHA, and all frozen input hashes. Stop on any drift.
2. Verify `preserved/R19_IMPLEMENTATION_ONBOARDING.md` still hashes to `27be0ca4c3e5abffa4fa492aaf47bf087328f41718fcc5f774c43fdf5b1c4e7e`. Move the original untracked report out of the execution checkout to a distinct, non-overwriting staging archive name (retain the verified copy above); do not delete it, ignore it, or edit it. Verify the moved bytes against the recorded SHA before checkout staging.
3. Only after those checks and the concrete Sol release, stage the original designated execution worktree at exact commit `2da980f631badc25086d12db60d128ff507d3ae6` using a detached checkout. Do not modify any other agent's worktree. Preserve ignored local gates as historical artifacts; never reuse either existing gate. Do not reset or clean.
4. Verify exact HEAD, expected branch/detached state, no tracked/untracked source changes, exact remote source SHA, gate inputs, runtime/source identities, and output absence. Only then create the new local gate under the ignored `configs/local/` path named below; no gate is created by this proposal.
5. If staging/preflight is not released, fails, or is stopped, first confirm supervisor and child are gone and preserve all receipts. Restore the execution worktree to branch `codex/r19-source-contract-repair` at `da7d348ffd3677d619dd31357e1e1e3cca28c9ec` without reset/clean; restore the original onboarding file from the verified archive with mode 0644, then byte-compare/hash both copies. Keep archive and any new failure evidence. If a preflight succeeds, leave the exact-SHA source untouched pending independent launch-clearance review and a separate fresh user science authorization; do not infer or start live execution.

This staging sequence is proposed only. No checkout movement has occurred.

## 3. Future gate content and bindings (no runnable gate written)

Proposed ignored path, only after a separate Sol Phase1 release:

`/home/lizening/wt-r19-recovery-duration-v1/configs/local/r19_b1_g3_gate_2da980f_phase1.json`

Status now: **not created; gate SHA256: NOT APPLICABLE / PENDING**. Do not copy, convert, or execute this Markdown proposal as a gate. The future gate must be freshly constructed for the staged exact SHA; neither prior local gate nor consumed clearance is reusable.

Bind at minimum:

| Binding | Required value |
|---|---|
| source SHA | `2da980f631badc25086d12db60d128ff507d3ae6` |
| independent review path / SHA | `/home/lizening/research-notes/agent-logs/2026-10-22T234140Z__SOL__r19-exact-sha-independent-review__2da980f_198732/independent_review.json` / `85a694f24da347dcb0e6f09f4fe0d33afefb46abf1d5b0063361870c3fe7820b` |
| adjudication path / SHA | sibling `known_failed_adjudication.json` / `3abea8efc2bd9d88677d71031aef0a21e905e6dd7b3ed75d06f1486d4c6718e0` |
| protocol / B1 manifest / B1 amendment | `3d7d1865c807d12276a8109b06c55da4e9182df0ca05a0b5463f8128dd03e122` / `d503f35ae913b137dfff091263bf29c38aa0ade2eea648dc45d7e6cf80da0973` / `f8a138045cde125f2c5e08a7d077f75e3838cc7f6d0c67703faffe1166099e49` |
| original G3 / entrypoint authorizations | `89b887518c85d22d3176af0b50fb1861b58fb1c3b13a4ecc2b76485a66529b31` / `026eb1f0b05bcc27a6c901c10d787110cbac0e329551051973dda93e907bdc71` |
| source-contract amendment / restart authorization / resolution event | `1b94a0ed37284d37a21d07985a5ba18de25ea4e11f9ffa553ca624c9739aee1e` / `164179291d16066d7fc6d650a943011099e8be940f48b62d86970ba7f5c17048` / `58783ba60b076ee190dccb0875aac65891d7e1c811e00fbe6303ca65896369d9` |
| runtime expectations / preload manifest | `dbfb7aa1a1d48d1148ad25be93002e7424d8b22e85422125ed502ac0f4db967e` / `64ebf4667da70dc4acd0a49b645bb6b6d4c3e1fe5d3e8e6351a8bf66f148ab9a` |
| source schedule / exclusion manifest | `0be460359fe43193e73f8cb55a8fb19fdba02ea70e3d0809ec5978fad21c8948` / `70447bba1b2a944d52ab9b4041b2d6ff3d865f4f0abd55d655214c8060ff5367` |
| historical environment manifest | corrected raw SHA `81ea3b3aea86a850c70d88846f1ce12dfb276cca34aacb9f598ea13e733bf902`; never use the mistyped `...70c888...` value. This is distinct from run-context identity hashes. |
| G2 carry-forward | execution SHA `92aae1d9b230cc212c6ec4effc99aa468941e69d`, run `33b5563d86d6491a821db224dd38ec3c`, review says PASS, no rerun; preserve manifest `7d8758bcc1fa5e40bb0f1b8f3e13707062104f6a2038673dd3cff93171de4c39`, event ledger `1456c43f7d3f0a849fe4bb8015164815fd70f4e2813d343449c1a34c2eaebe0c`, branch ledger `c91f9ff8ab5869bfcdcddd850e038b84c84ad317a7098928a4a09129652e96d3`, offline verification `80b704131ec4e9738aca25d30512e2d4b84d675ac7537eec27a1083e16cc0b29`, smoke checks `bf1fed5ff1731fc59280d5d3c55acb540c657eef1f34255bd3816619641f91bb` |
| failed predecessor | run `3d1ccea7e97f4727abf8e216ac6ec498`; genuine exit 1; event SHA `fde95fcd72f1c4ac6409fab7f2112654e145f6184fefec690cae58ad345f1cd7`; manifest SHA `f5d3efa6c17abea3d944d7dea01099210d846eb8ed107057ec24502bbb51d2df`; registry SHA `870923242ae585c66cbcffa554528ab3d92cf98fc4d87dee2c4d408f5f6ba800`; branch ledger empty SHA `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| historical cost start | 177 completed model generations; 342 environment operations = 330 non-reset + 12 reset; no incomplete external operation; source episode remains incomplete |
| model / actor | Qwen/Qwen3-8B local snapshot revision `b968826d9c46dd6066d109eabc6255188de91218`; SFT-P0 adapter directory SHA `6e403d85b150a74dfcc176f1f180ce4baf6fdacd922d2f96b3ceef0a21100f11`; exact filesystem bytes must be reverified before release; historical R18 identity remains unresolved |
| frozen campaign / caps | 127 TRAIN identities, index 0 first; 120 initial attempts; at most 60 eligible with 30/15/15, no quota transfer; K=1..5; horizon 50; source remainder 8,999 generations/8,999 environment operations; preserve all other phase/global caps; no retries |
| review status | independent review `PASS`; new production preflight has not run; no launch clearance; no fresh user live authorization; all execution-release fields remain absent |

## 4. Proposed fresh zero-science preflight binding

Only if Sol later releases the concrete Phase1 preflight, propose:

- CWD: `/home/lizening/wt-r19-recovery-duration-v1` at exact reviewed SHA.
- Supervisor interpreter and child interpreter: `/home/lizening/miniconda3/envs/alfworld-self-improve/bin/python`.
- Supervisor record directory: `/home/lizening/research-notes/agent-logs/2026-10-22T235413Z__CODEX__r19-phase1-preparation__2da980f/preflight_supervisor` (currently absent).
- Preflight receipt: same record directory, `pilot_preflight_receipt.json` (currently absent).
- New gate path: `configs/local/r19_b1_g3_gate_2da980f_phase1.json` (currently absent and not created by this proposal).
- Output sentinel: `/home/lizening/wt-r19-recovery-duration-v1/artifacts/runtime/r19_b1_g3_preflight_2da980f_20261022T235413Z` (currently absent; must remain absent after preflight).
- Existing inputs: protocol `/home/lizening/wt-r19-recovery-duration-v1/configs/experiments/r19_recovery_duration_v1.json`; source schedule/exclusions under `configs/experiments/r19_preflight_v3/`; ALFWorld data root `/home/lizening/alfworld_data`; ALFWorld config `/home/lizening/wt-r19-recovery-duration-v1/configs/local/r19_b1_g2_alfworld.yaml`; adapter `/home/lizening/Alfworld-Self-Improvement-Project/artifacts/runtime/model-artifacts/sft-policy-bootstrap/full/final_adapter`; offline Qwen snapshot `/home/lizening/.cache/huggingface/hub/models--Qwen--Qwen3-8B/snapshots/b968826d9c46dd6066d109eabc6255188de91218`.
- Existence-only checks in this preparation confirmed the interpreter, adapter directory, snapshot directory, TRAIN data directory, and config file exist. No weights were loaded and no model/data payload was opened. The exact file-byte/runtime identity check remains a release-time gate; do not interpret existence as hash verification.

### Proposed supervisor argv

```text
/home/lizening/miniconda3/envs/alfworld-self-improve/bin/python
/home/lizening/wt-r19-recovery-duration-v1/scripts/launch_r19_supervised.py
--record-dir
/home/lizening/research-notes/agent-logs/2026-10-22T235413Z__CODEX__r19-phase1-preparation__2da980f/preflight_supervisor
--evidence-class
preflight_only
--supersedes-run-id
3d1ccea7e97f4727abf8e216ac6ec498
--
/home/lizening/miniconda3/envs/alfworld-self-improve/bin/python
/home/lizening/wt-r19-recovery-duration-v1/scripts/run_r19_recovery_duration.py
pilot
--protocol
/home/lizening/wt-r19-recovery-duration-v1/configs/experiments/r19_recovery_duration_v1.json
--manifest
/home/lizening/wt-r19-recovery-duration-v1/configs/local/r19_b1_g3_gate_2da980f_phase1.json
--output
/home/lizening/wt-r19-recovery-duration-v1/artifacts/runtime/r19_b1_g3_preflight_2da980f_20261022T235413Z
--adapter
/home/lizening/Alfworld-Self-Improvement-Project/artifacts/runtime/model-artifacts/sft-policy-bootstrap/full/final_adapter
--data-root
/home/lizening/alfworld_data
--config
/home/lizening/wt-r19-recovery-duration-v1/configs/local/r19_b1_g2_alfworld.yaml
--preflight-only
--preflight-receipt
/home/lizening/research-notes/agent-logs/2026-10-22T235413Z__CODEX__r19-phase1-preparation__2da980f/preflight_supervisor/pilot_preflight_receipt.json
```

The shell-level environment must explicitly remove `PYTHONPATH`, `PYTHONHOME`, and `VIRTUAL_ENV`; the supervisor itself injects `R19_RUN_ID`, `R19_EVIDENCE_CLASS=preflight_only`, `R19_EXIT_RECEIPT_PATH`, and `R19_SUPERVISOR_CONTEXT_PATH`. `--supersedes-run-id` must remain the failed run above. A successful authentic child exit 0 and `PREFLIGHT_ONLY_PASS` are required, with correct source/gate/review/runtime/input hashes, module origins from the exact checkout, absent output, and zero model loads/generations, ALFWorld constructions/resets/steps, and scientific units.

### Environment allowlist to pin and revalidate

Use only the supervisor's recorded allowlist; never inherit these three Python override variables:

| Variable | Proposed value / rule |
|---|---|
| `PYTHONPATH`, `PYTHONHOME`, `VIRTUAL_ENV` | unset; explicitly remove before launching supervisor |
| `CONDA_PREFIX` | `/home/lizening/miniconda3` (as captured in the prior authentic supervisor context; revalidate) |
| `PATH` | pin to the reviewed effective value below; do not let an interactive shell silently rewrite it |
| `ALFWORLD_DATA` | `/home/lizening/alfworld_data` |
| `ALFWORLD_CONFIG_PATH` | `/home/lizening/wt-r19-recovery-duration-v1/configs/local/r19_b1_g2_alfworld.yaml` |
| `HF_HUB_CACHE` | `/home/lizening/.cache/huggingface/hub` |
| `HF_HUB_OFFLINE`, `TRANSFORMERS_OFFLINE` | `1` |
| `HF_HOME`, `CUDA_VISIBLE_DEVICES`, `CUDA_HOME` | unset, as in the captured prior authentic supervisor context, unless Sol's concrete release specifies and independently pins a reviewed value |
| supervisor-injected keys | `R19_RUN_ID` fresh supervisor UUID; `R19_EVIDENCE_CLASS=preflight_only`; receipt/context paths inside the new record directory |

Captured prior-authentic-context `PATH` (must be revalidated before any release):

```text
/home/lizening/.local/bin:/home/lizening/.local/bin:/home/lizening/.local/bin:/usr/local/cuda/bin:/home/lizening/.codex/packages/standalone/releases/0.163.0-x86_64-unknown-linux-musl/codex-path:/home/lizening/.codex/tmp/arg0-linux/codex-arg0VXC9gg:/home/lizening/.local/bin:/home/lizening/.local/bin:/home/lizening/.local/bin:/home/lizening/.local/bin:/home/lizening/miniconda3/bin:/home/lizening/miniconda3/condabin:/home/lizening/.local/bin:/usr/local/cuda/bin:/home/lizening/.local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin
```

The pinned Python executable is absolute in both argv positions. No interactive-shell `PYTHONPATH` or package installation may participate.

## 5. Hashes and pending release dependencies

- This preparation proposal SHA256 is reported out-of-band with the Sol handoff (a file cannot contain its own stable digest).
- Byte-preserved onboarding report SHA256: `27be0ca4c3e5abffa4fa492aaf47bf087328f41718fcc5f774c43fdf5b1c4e7e`.
- Canonical planned child argv SHA256: `eea6b0032ca714ec011b3d48f9c6a1a1bec3879560910ae77ce3da1c924aaa68`; canonical planned supervisor argv SHA256: `7c1519ccb6f34683ee1ac09d4757d8a00bc225576b6a4f8370736790a2b9235b`; sorted static environment-allowlist proposal SHA256: `6f9462a0234a24fb6967946b165bd99db54641c926de88cd0bac33580b702516`. Hashes use the production canonical JSON encoding (`ensure_ascii=True`, sorted keys, compact separators). They are proposal hashes, not an execution receipt. Gate SHA256 remains **NOT CREATED / NOT APPLICABLE**.
- No launch-context SHA256 can exist until the supervisor actually creates its new run UUID and authentic context; no such run has started.
- Required before Sol can release Phase1: confirm candidate/source and reviewer bytes unchanged; adjudication accepted; approve this exact record/output/argv/environment/gate-path proposal; independently verify current inputs and absent paths; populate and review a new gate digest. This proposal itself supplies none of those approvals.
- After any future preflight: return authentic `runner_exit.json`, `launch_context.json`, status, log and receipt hashes to Sol; wait for a distinct independent launch-clearance review. A separate fresh explicit user science authorization is required before any live G3. Old consumed clearance and old gate are unusable.

## 6. Provenance coordination

This record is isolated under Luna's task directory. It does not edit `INDEX.md`, inventory, any other agent's directory, any scientific worktree, or any old record. Coordinate the shared publication window with Sol before INDEX/inventory updates or commit/push. No publication or remote write is performed by this proposal.
