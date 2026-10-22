# R19-B1 G2 continuation

- Agent/task: ASTRA; continue the user-authorized R19-B1 bounded G2 smoke workflow.
- Start UTC: 2026-10-22 07:23:56 UTC (logged continuation start; earlier implementation/preload work is recorded in session history and the preceding R19 G1 record).
- Evidence-record seal UTC: 2026-10-22 07:48:03 UTC; GitHub push/ref verification follows as a separate provenance transaction.
- Status: G2_FAIL before branch-arm execution; exact-SHA review PASS; one bounded G2 smoke ran once and stopped at the mandatory replay gate.
- Scientific repository: `MikazukiMisaki/Alfworld-Self-Improvement-Project`.
- Scientific branch: `codex/r19-recovery-duration-v1`.
- Scientific starting SHA for this continuation: `991ca1d7048f03b89ec444cb287fcb2fb1179605`.
- Scientific current SHA: `f4fb81842e949930433def5817723bab74159f14`.
- Scientific starting SHA requested by the user: `dddf684f488873537196588beeec324cb1893dd7`; history was advanced normally, without reset.
- Provenance repository starting SHA: `2ec300bb7b064824683ae196d179effa52937d6a` on `main`.

## Scope and boundaries

Authorized work: finish exact-SHA independent review; only if it explicitly passes, execute the pre-registered bounded G2 smoke for R8-F16 and R8-S04; offline verification; preserve and upload provenance; verify remote SHAs. The approved prospective baseline is R19-B1, using model snapshot revision `b968826d9c46dd6066d109eabc6255188de91218` and the existing SFT-P0 adapter. Historical R18 model identity remains `MODEL_IDENTITY_UNRESOLVED` / `NOT_ESTABLISHED`; this task makes no claim of equivalence.

Not authorized: G3 or any fresh TRAIN task (including the 127-task schedule), training, DPO/ORPO, selector training, held-out evaluation, model replacement, quota/exclusion/budget changes, added cases, unplanned retries, or automatic experiment expansion. Stop after G2 report and provenance.

## Evidence ledger

OBSERVED at continuation start — scientific worktree was clean at `991ca1d7048f03b89ec444cb287fcb2fb1179605`; `git ls-remote` reported the same SHA for `refs/heads/codex/r19-recovery-duration-v1`. The commit is a normal successor; no reset or destructive history operation was used.

OBSERVED — `tests/test_r19_recovery_duration.py` completed with 46 passed and process exit 0 on the exact current commit.

OBSERVED — frozen protocol SHA-256 is `3d7d1865c807d12276a8109b06c55da4e9182df0ca05a0b5463f8128dd03e122`; baseline manifest SHA-256 is `d503f35ae913b137dfff091263bf29c38aa0ade2eea648dc45d7e6cf80da0973`; amendment SHA-256 is `f8a138045cde125f2c5e08a7d077f75e3838cc7f6d0c67703faffe1166099e49`; local ALFWorld config SHA-256 is `e90f93eb4604a473b6eb4a259a19ef1ca3c296bba1771ba70a1c9b0edbc99700`; frozen R8 prefix manifest SHA-256 is `cfb3be3e0e87eec74216068d27530063307ead1698c39481e0b734ebe629f44f`.

OBSERVED — effective runtime expectations canonical SHA-256 is `dbfb7aa1a1d48d1148ad25be93002e7424d8b22e85422125ed502ac0f4db967e`; frozen preload-runtime SHA-256 is `64ebf4667da70dc4acd0a49b645bb6b6d4c3e1fe5d3e8e6351a8bf66f148ab9a`. R7 source schedule SHA-256 remains `24ff5e65d9ef38024d168031fb271770d28ec7e8f014c57b90cba90abbbc186e`; retained R8 OSR summary SHA-256 is `f605bc6c9f87f21c55adddac04887ab72c1e742b40be7d8699af9273949944a6`.

OBSERVED — read-only preflight found the ALFWorld data root and frozen adapter present; the scientific worktree has no pre-existing R19-B1 G2 output directory. The supervisor and runner create unique output directories and refuse to overwrite existing ones.

OBSERVED — the actual local model/tokenizer snapshot files match the frozen `b968826d9c46dd6066d109eabc6255188de91218` manifest, and the existing SFT-P0 adapter matches directory SHA-256 `6e403d85b150a74dfcc176f1f180ce4baf6fdacd922d2f96b3ceef0a21100f11` across its 11 recorded files. A local identity load (no generation and no ALFWorld calls) confirmed both resolved revisions equal the pinned snapshot; BF16, SDPA, Qwen3 config, Qwen2 fast tokenizer length 151669, recovery adapters empty, actor active adapter `default`, separate model objects, and no shared KV cache. The pre-load runtime/environment matched the frozen manifest. Historical R18 equivalence remains NOT ESTABLISHED.

OBSERVED — the exact already-consumed smoke task files match the B1 manifest: R8-F16 game `a7e89adcef5bbe43de73fe96813b414672251786670a05ea317857fa7ffc1822`, trajectory `71a136f7ffc4433d8610a63f9ff1d8519b8bf8f292d132d449b9d2d876d2b6c6`; R8-S04 game `d406ad3303ac7460ad3b92bbca37679d6f79f848a20db445f4eccd8f21376a29`, trajectory `1c2142d78915a708d7f6aafac34d70844fc9d362e970005200aff9ec0784aa9d`.

OBSERVED — frozen prelaunch G2 bounds are 6 production arms, at most 228 model generations and 374 environment operations for the exact two cases; original hard limits remain 8 arms, 408 generations, and 400 environment operations. The approved mode is smoke only; G3 is false.

OBSERVED — no active R19 runner, supervisor, ALFWorld, or R19 test process remained after the focused test completed.

OBSERVED — exact-SHA independent review of `991ca1d7048f03b89ec444cb287fcb2fb1179605` returned BLOCKED. Reviewer found K3 arm references were not bound to their execution prefix/K, the two K3 reference sets were not required to be disjoint, and offline verification did not rebuild stored K3 signatures from raw events. Full review text is in `review-991ca1d.log`. Earlier review of superseded SHA `bd55e67…` was interrupted and explicitly does not count.

OBSERVED — before this continuation, B1 model/tokenizer/runtime/environment identity had been frozen and a no-generation local model-load isolation check had passed. That check loaded local model weights only; it did not generate text or create/reset/step ALFWorld. Detailed hashes and outputs will be included in this task record or linked evidence before finalization.

OBSERVED — exact review of `b7abaf30b0ddd0242391461f421e36f5466acc16` returned BLOCKED on the event-shape mismatch: production stores `recovery_action_index` in `payload.action`, not event identity. Full verdict is preserved in `review-b7abaf30.log`; this SHA is superseded and has no PASS.

OBSERVED — follow-up commit `f4fb81842e949930433def5817723bab74159f14` corrects the validator to read the production payload location and corrects the synthetic fixture to omit the field from identity. It was pushed normally; local and remote refs match and the worktree is clean. This successor also includes the earlier prefix/K binding, arm-payload equality, K3 evidence disjointness, and raw-trace rebuild/offline verification fixes. Independent exact-SHA review by Chandrasekhar returned PASS with no severity-ranked findings; the byte-preserved report is `review-f4fb818.log`, SHA-256 `8fe98c492e1a6c29e5d071a839155b5693a81b2f5a313842d8facca327160c28`.

OBSERVED — post-commit focused suite at exact SHA `f4fb81842e949930433def5817723bab74159f14`: `tests/test_r19_recovery_duration.py` completed with 46 passed in 0.89s, process exit 0. Post-change `py_compile` and `git diff --check` passed (exit 0).

PRE-LAUNCH OBSERVATION — before the authorized smoke, this continuation had run no model generation and no ALFWorld reset/step; no fresh or held-out task had been consumed.

OBSERVED — exact-SHA independent review of `f4fb81842e949930433def5817723bab74159f14` returned PASS with no severity-ranked findings. The gate manifest binds the exact implementation, baseline, amendment, runtime, and reviewer report.

OBSERVED — the single authorized G2 smoke ran under durable supervisor run ID `089429e4a2554bc386580d87014b4951` from `2026-10-22T07:40:52.478596Z` to `2026-10-22T07:41:43.001255Z`. It failed before any branch arm because replay of R8-F16 differed from its frozen public prefix. The runner's authentic subprocess exit code was 2; the supervisor did not interrupt it. No retry or substitute task was used.

OBSERVED — the copied raw event ledger independently revalidated with the production event-ledger validator: 38 events; 19 starts and 19 completions; zero incomplete environment operations; 0 model generations/tokens, 18 physical environment steps, and 1 reset. Only already-consumed development task R8-F16 was observed. R8-S04 was not reached. The unit registry retains one `in_progress` prefix-replay/initial-recovery unit as incomplete/indeterminate; it was not altered or regenerated.

OBSERVED — the full offline G2 verifier exited 2 because the required `smoke_checks.json` does not exist after the replay failure; no `offline_verification.json` PASS artifact was produced. The separate raw event-ledger validation exited 0. Historical R18 model equivalence remains NOT ESTABLISHED.

## Commands and worktrees

Scientific worktree: isolated task worktree on `codex/r19-recovery-duration-v1`.

Provenance worktree: separate `MLLM-Research-Provenance` checkout on `main`.

Exact focused test command: `conda run -n alfworld-self-improve env PYTHONPATH=src python -m pytest -q tests/test_r19_recovery_duration.py` (exit 0; 46 passed).

Read-only checks included current/remote branch SHA comparison, frozen manifest/protocol/config hashes, local data/adapter availability, output-collision check, and process check. Full command details and subsequent gate/smoke/verifier commands will be recorded in `commands.log`.

## Changes, reviews, and execution

The only scientific edits are the targeted changes in `scripts/run_r19_experiment.py` and `tests/test_r19_recovery_duration.py` to close the exact-review findings. Commits: `b7abaf30b0ddd0242391461f421e36f5466acc16` and `f4fb81842e949930433def5817723bab74159f14`; only the latter is the exact-SHA PASS target. Frozen protocol, baseline, amendment, model, quotas, exclusions, and configuration are unchanged. The gate manifest is tied to the exact review PASS and frozen bundle.

Exact review evidence is preserved byte-for-byte as `review-f4fb818.log`. The one bounded G2 attempt used only the frozen two-case plan and original caps; the replay failure occurred before branch execution. No scientific code/configuration changes were made after review or after observing the result. The incomplete unit is preserved and will not be retried or regenerated in this task.

## Final status

R19-B1 / G2 status is **G2_FAIL before branch-arm execution**. Exact review PASS applies to implementation SHA `f4fb81842e949930433def5817723bab74159f14`, not to G2 scientific acceptance. R8-F16 frozen-prefix replay is a hard gate and failed; R8-S04, K1 reference/production, K3 repeats, handoff/extension coverage, and horizon checks were consequently not reached. Historical OSR output comparison was not reached and remains diagnostic only.

- Authorization: user explicitly approved R19-B1 freeze, exact-SHA review, and bounded G2 on R8-F16/R8-S04 only; G3 remained unauthorized.
- Baseline: R19-B1; base/tokenizer snapshot `b968826d9c46dd6066d109eabc6255188de91218`; existing adapter directory SHA-256 `6e403d85b150a74dfcc176f1f180ce4baf6fdacd922d2f96b3ceef0a21100f11`; local artifacts were verified before launch. Historical equivalence: NOT ESTABLISHED.
- Runtime/environment: frozen identity and prelaunch checks passed; both policy model objects were separate, recovery adapter inactive, actor `default` adapter active, and KV cache not shared. Smoke stopped during environment replay.
- Counts: 0 of 6 production arms; K1 reference 0, production K1 0, K3 repeats 0; physical model generations 0; environment steps 18 plus 1 reset (19 charged operations); logical per-policy cost not applicable.
- Task boundary: fresh tasks 0; held-out 0; model training 0; paid/external model calls 0; G3 not authorized/not run; unplanned retries 0; completed-unit reruns 0; one indeterminate unit retained.
- Authentic status: runner subprocess exit code 2; supervisor status failed, `interrupted_by_supervisor=false`; full offline verifier exit 2 for missing `smoke_checks.json`; separate raw-ledger validator exit 0.
- Uploaded provenance files and SHA-256 values are inventoried in `FILE_HASHES.sha256`; original receipts with machine-specific command paths remain local, while `supervisor_receipt_summary.json` is sanitized. Sizes, hashes, and reasons for excluded local supervisor files are listed in `EXCLUDED_FILES.md`.

NEXT: STOP.
