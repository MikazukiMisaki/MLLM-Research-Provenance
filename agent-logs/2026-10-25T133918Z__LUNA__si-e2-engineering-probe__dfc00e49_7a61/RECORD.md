# SI-E2 concrete engineering-probe proposal record

**Status:** `CONCRETE_PROPOSAL_PREPARED / ROOT_REVIEW_PENDING`  
**Release status:** `NOT_GRANTED`  
**Science authorization:** `NOT_GRANTED`  
**Writable scope:** this new Luna-owned task directory only. No model, CUDA context, ALFWorld, training, supervisor, preflight, or science invocation occurred. No shared provenance file was staged, committed, or pushed.

## Task and candidate binding

- Current task instruction `LUNA_CONCRETE_PROPOSAL_TASK.md` SHA256: `c130a1e39785be5e1b2451ca93a8e5d7e6f80c078dc17d81f67bcd893f513752`.
- Proposal source is the clean local candidate `dfc00e49d1ef4d48453d2331507429f8a0c7bbc5` at `/home/lizening/wt-si-p3-runtime-adaptation`, branch `codex/si-p3-runtime-adaptation`. The final read-only status receipt records this exact HEAD and empty porcelain status. Developer clean tests/push, root full regression, and independent exact-SHA review were still pending when this proposal was prepared; this is not an implementation PASS.
- Read the committed runtime engineering contract and exact proposal/authorization schemas. Their paths and SHA256s, plus relevant runtime-gate/backend/environment/supervisor source-file hashes, are in `PROPOSAL_HASHES.json`. No project validator or test suite was run.
- The synthetic prompt digest was derived from the candidate's fixed `engineering_prompts()` using the pinned interpreter in `-I` mode. The capture emitted only its digest/key/byte-length summary and asserted torch, ALFWorld, and TextWorld were not imported. Receipt return code was 0; digest is `a5495b4fa0af3a1c34e8b11203bd707ce409f355cb193df0d46be39d9fed4437`.

## Immutable proposal package

- `SI_E2_PROPOSAL.json` conforms to the required `SI_E2_PROPOSAL_V1` wire shape. It binds the original source trajectory JSONL and raw event ledger, active R19 YAML, exact saved game and `traj_data.json`, original TRAIN data root, Alfred domain/grammar, cached base snapshot, actual P0 final adapter, pinned interpreter, eight package/module path hashes and public module versions, and the fixed synthetic prompt digest.
- Package/module versions and expected path/hash bindings come from root `independent_pinned_package_bindings.json` (SHA256 `2f1e7aaa8ea10a527182d37d1535770377674c79313b3b66788df5483c3c84af`). Luna independently rehashed the interpreter and all eight bound module files in the captured proposal-input subprocess; all matched. Empty `__version__` values for ALFWorld and the nested environment/TextWorld modules are preserved exactly; no distribution version was substituted.
- The proposal's trajectory path SHA is the whole original `source_trajectories.jsonl` file hash; the canonical source-episode identity hash is separately recorded in `FIRST_SOURCE_REPLAY_BINDINGS.json`. No prompt, action command, task body, token array, model weights, adapter bytes, or cache contents are copied into this proposal directory.
- Raw proposal SHA256: recorded in `PROPOSAL_HASHES.json`; canonical compact-JSON SHA256 is separately recorded. Authorization binds the proposal's exact raw bytes.
- `ENGINEERING_ARGV_PROPOSAL.json` contains the pinned absolute Python `-I` command and exact script/authorization/proposal paths. The authorization raw SHA remains `PENDING_ROOT_AUTHORIZATION_RAW_SHA256`; the argv is deliberately non-runnable. No authorization document was authored.
- `ENGINEERING_ENV_PROPOSAL.json` sets `inherit_environment=false`, gives the exact minimal allowlisted set/unset values, removes Python path overrides, LD_PRELOAD, CUDA device-order overrides and credential variables, and retains offline/HOME/PATH/CUDA-library/ALFWORLD settings. `PATH` is reduced to `/usr/bin:/bin` (the actual resolved nvidia-smi path is `/usr/bin/nvidia-smi`). No token values were read. The environment's ALFWORLD_DATA remains the original TRAIN root; the reviewed no-scan task-path restriction must apply before constructor entry.
- Future output leaf is this new directory's `engineering_run`; root authorization path is `...__SOL__si-e2-runtime-resource-review__sie2_4c82/engineering_authorization.json`. Final state receipt proves both absent, candidate SHA/clean status, and records return codes. Do not create output or record path before a separate release.

## First-source replay binding

The candidate is the first record by original JSONL order (schedule index 0), not an outcome-selected episode: task `pick_and_place_simple-Pencil-None-GarbageCan-316/trial_T20190907_165839_449092`, TRAIN, seed `30000`, six saved commands. Source line SHA256 is `465bff755ba34c18acca299470cd7c3a40455cb395df3e6fe43eee9919a7c73`; canonical source trajectory SHA256 is `fba2a4278c4f1d9640c1c39f527fe3d5e7022ab50af4d353bc017bb31bbead89`; whole source JSONL SHA256 is `c6f37a7da28e326c70818524c79c17bbd85a286754c111f17db07cbe151a4f1c`; raw event journal SHA256 is `05e1d443ff304eaa25d08b92a4e19d204a6c93a4f46bbe50aefef3271f211762`.

Proposal: two fresh one-game instances, each reset once with seed `30000`, the same explicit TextWorld pool seed `30000`, then replay the same six saved commands. Total 2 resets / 12 physical action steps. Compare task, goal, observation, ordered valid-action maps, reward/done/truncated, and every transition. Do not execute generated commands. Future replay terminal-map behavior remains unobserved; preserve null/missing exactly and fail strict comparison rather than fabricating. The original global YAML and TRAIN data root remain hash-bound; the environment factory must narrow effective discovery to this exact task directory before constructor scanning.

## Exact proposed limits and monitor

One engineering-only diagnostic on the bound A40 UUID; at most 1,800 seconds, 0.5 allocated-device-hour, four generations, 88 generated tokens, 8,192 input tokens/call and 32,768 total input tokens. Calls/caps: source 16, Stage 1 40, Stage 2 16, suffix 16. Fixed synthetic public prompt/state only; no generated action is executed in ALFWorld. No training, optimizer, adapter save, acquisition, evaluation, G2/G3/G4, retry, or policy outcome search. Replay cap is tightened to the exact 2 fresh instances / 2 resets / 12 steps.

`FUTURE_READ_ONLY_MONITOR_PLAN.md` defines read-only one-second device/process sampling, owned PID/start-tick checks, sampled-memory-peak caveat, monotonic deadline/device-hour accounting, fail-stop on foreign compute or uncertain ownership, and stopping only this task's own process. The known small graphics process can remain a disclosed shared baseline, but its owner/PID mapping is unresolved and there is no GPU exclusivity claim. The future worker must prove its own CUDA-context/NVML PID before full 8B allocation or stop cheaply.

## Authentic preparation receipts and counts

Captured subprocess receipts preserve exact argv/cwd/environment, UTC/monotonic times, return codes, stdout/stderr byte counts and hashes:

- `prompt_digest_receipt.json`: 0; prompt text not emitted; no torch/ALFWorld/TextWorld imported.
- `proposal_input_hashes_receipt.json`: 0; 16 bound input/runtime files hashed by the pinned interpreter; no task JSONL row was parsed by that hash subprocess.
- `safe_environment_receipt.json`: 0; only the named non-secret environment keys captured.
- `final_proposal_state_receipt.json`: git HEAD/status commands returned 0; output and root authorization path both absent.
- `proposal_finalization_receipt.json`: actual final raw/canonical proposal hash capture subprocess returned 0 at `2026-10-25T13:47:09.418645+00:00`–`2026-10-25T13:47:09.463838+00:00`; raw stdout/stderr are preserved under `raw/`.
- `final_consistency_attempt01_receipt.json`: an initial narrow stdlib assertion used a nonexistent top-level key and exited 1; the captured exception is preserved and did not call project code or change inputs. `final_consistency_attempt02_receipt.json` corrected the lookup to the actual receipt schema and exited 0. This was a bookkeeping-check correction, not a proposal/runtime validation failure.
- The final narrow consistency check confirmed proposal hash/size linkage, candidate identity, absent output/authorization paths, and successful proposal finalization. `FILE_HASHES.sha256` is the final local inventory (manifest self-excluded).
- Original SI-E2 read-only receipts remain preserved in the prior completed readiness directory and are referenced, not edited.

Actual counts for this proposal task: model loads 0, CUDA contexts 0, generations 0, training 0, environment constructors 0, resets 0, steps 0, supervisor/preflight invocations 0. Historical science remains 5,142 generations / 7,949 environment operations including resets; earlier 177/342 is already included. No actual device-hour was consumed or claimed.

## Pending fields / handoff

Root must complete exact-SHA code review/regression acceptance, issue a separate immutable authorization with raw SHA and UTC window, approve exact proposal/environment/argv/GPU UUID/output identity, and separately release any engineering invocation. The authorization raw SHA, executable argv value, authorization id/window, and execution result remain pending. No science execution is permitted by this record. All files here are local-only; no shared INDEX or provenance Git operation was performed.

**Task start UTC:** `2026-10-25T13:42:24.189257Z` (first captured preparation receipt).  
**Task finish UTC:** `2026-10-25T13:48:48Z` (after final stdlib consistency receipt; hash inventory regenerated and verified immediately afterward).  
**Final status:** `CONCRETE_PROPOSAL_PREPARED / ROOT_REVIEW_PENDING`; stop here pending root review.  
**Publication boundary:** see `PUBLICATION_ALLOWLIST.md` and `LOCAL_ONLY_FILES.md`; no provenance Git changes were made.
