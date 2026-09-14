# R18-C2 preflight V2: process identity and launcher design

V2 is accepted for the tested operational infrastructure scope. This record does not authorize formal execution. Astra owns implementation and acceptance; Gemini is no longer an execution participant in this workflow. A later Luna worker would need separate explicit authorization.

## Defect and evidence

V1 applied `Path(arg).name` to every argv entry and treated either scientific-script or wrapper basename as an active process. Search strings, editor filenames and diagnostic arguments could therefore block launch. V2 identifies the interpreter's executed script operand before comparing its resolved path. Historical V1 files are preserved unchanged.

PID 602690 is an unidentified historical argv match. Its exact identity and matching argument were not retained. The failed attempt stopped before dispatch. The detector defect is proven by code and synthetic reproduction; attribution of PID 602690 to an unrelated process remains unproven. See [forensics](pid-602690-forensics.md).

## Runner classification

`Process` stores actual `/proc` executable, cwd, argv, PID, start ticks, boot ID, state, PPID, PGID and SID. `classify` is a pure function over that evidence and explicit path rules. Production rules have no command-line override.

An exact runner requires all of:

- `/proc/<pid>/exe` resolves to the frozen Python interpreter in `alfworld-self-improve`.
- Python is executing a script operand. Command text, stdin and unrelated module execution are ignored; ordinary interpreter switches and the option separator are parsed.
- The script resolves relative to that process's cwd to the authoritative repository's `scripts/run_progress_aware_card_v2_r18_c2.py`.
- The cwd is the authoritative repository.
- Exactly one `--output` (separate or equals form) resolves to the frozen formal runtime.
- Exactly one resume flag is present, with no unexpected script arguments.

An executed exact scientific script with a wrong environment, cwd, arguments or incomplete metadata is an ambiguous blocker. The scientific module invocation is also an ambiguous blocker. A different path with the same basename is unrelated. No scientific script is imported to make these decisions.

## Wrapper and saved identity

A wrapper requires actual Bash executing the script operand at the exact V1/V2 filename immediately inside a timestamped R18-C2 task directory. Expected cwd, job directory, work directory, external lock path and exact formal Python payload must match. A known executed wrapper with unexpected arguments remains an ambiguous blocker. Legacy task names remain recognized solely to protect historical process identities.

V2 saves atomic JSON launcher and runner identities containing PID, start ticks and boot ID. A live three-field match blocks even independently of argv classification. Mismatched start ticks mean PID reuse; mismatched boot means a previous boot. Neither case licenses killing a process. Legacy two-number records use an accompanying boot-id file where available; otherwise a matching live identity is ambiguous and blocks. Exited and zombie processes are inactive. Malformed saved identity records fail closed.

`read_process` samples start ticks before and after reading metadata to avoid combining reused PIDs. Vanished processes are normal. Permission-denied unrelated PIDs are reported; an unreadable recorded PID blocks. An exact script candidate with unreadable executable/cwd also blocks. This is a server-local operational detector, not a defense against hostile argv rewriting, arbitrary embedded Python execution, or an inaccessible process namespace. The tested server scan had no unreadable processes.

## Serialization and completion

Preflight probes existing locks using read-only opens and nonblocking exclusive flock, immediately releases them, and never creates or truncates lock files. An absent optional external lock remains absent; a missing required scientific writer lock stops preflight. Held locks stop preflight.

The wrapper acquires the separate external launcher lock before starting its payload and holds it across the child lifetime through inherited descriptor 9. The scientific writer lock is never held by the launcher. The runner's own writer lock remains final authority. Process scanning and lock probing are snapshots; external launcher serialization and the runner lock address the subsequent launch race.

Each job directory is single use. A duplicate job directory is rejected with 73; a concurrent external-lock competitor is rejected with 75. The payload's own wait status is atomically persisted, including nonzero results. The log and exit status are sealed after normal completion. Detachment uses nohup and a new session, stdin is `/dev/null`, and stdout/stderr go directly to the job log. PID records aid monitoring; they are never substitutes for the runner exit marker.

The launcher design has an explicit authorization-SHA guard and performs preflight before dispatch. The guard is a mechanical interlock, not a grant of permission. The launcher design was syntax-checked only and was not executed. Existing environment, branch, local/remote revision, clean-worktree, adapter, runtime/control hashes, exact manifest, output absence and owner gates remain enforced.

## Mechanical validation and limits

[test-results.json](test-results.json) summarizes ten passing unit-test methods: nineteen unrelated-process fixtures, seven exact runner forms, three wrapper forms, malformed/ambiguous invocation cases, saved identity and PID reuse, synthetic `/proc` snapshots, and non-destructive held-lock refusal.

Three live harmless processes (shell, Python diagnostic, grep) carried the scientific filename as data. Each was unrelated, and production read-only preflight passed while they lived. Synthetic wrapper jobs survived dispatch-shell completion, saved matching birth identities, rejected a concurrent launch and a same-directory relaunch, and naturally persisted exit statuses 7 and 0. Both completed and all owned job PIDs were absent afterward; the synthetic lock was available.

The harmless synthetic payload accepted stand-in output/resume arguments to exercise the exact structural classifier under explicit test-only path rules. These were not scientific invocations. No formal runner, replay, Qwen, ALFWorld, GPU or held-out workload was executed. Future formal execution was not tested or authorized. No claim of general host-crash durability or immunity to explicit process termination is made.

The final real-server preflight passed with zero blockers, unchanged initialized runtime and available scientific writer lock. The real external launcher lock was absent and was not created. Evidence is in the process/launcher logs and final integrity report.
