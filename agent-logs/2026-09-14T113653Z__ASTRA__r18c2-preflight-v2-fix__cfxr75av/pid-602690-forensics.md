# PID 602690: evidence and limits

OBSERVED: The prior task `2026-09-14T100950Z__GEMINI__r18c2-durable-resume__JKzeagYA` has only RECORD.md, commands.log, preflight.log and boot-id.txt. At 10:09:56 UTC its preflight reported `STOP: existing runner/wrapper processes ['602690']`; the launch script exited 65 before dispatch. No launcher/runner PID or runner log was created. The same PID occurs in those three provenance documents only. `/proc/602690` is absent at this audit.

OBSERVED: No retained cmdline, executable, cwd, PPID, PGID, SID, start ticks, parent command or start/end lifetime for PID 602690 was found. The prior boot-id.txt identifies the launch host boot but does not establish that PID's identity.

INFERRED: The old detector selected at least one argv entry whose basename matched either the scientific filename or durable-wrapper.sh. That follows from its actual code and recorded error, but the particular matching argument is not retained. Its scan time falls within the recorded launch/preflight interval, 10:09:50–10:09:56 UTC; exact process lifetime is not proven.

NOT PROVEN: PID 602690's exact identity or whether it was a Python runner, Bash wrapper, editor, Git/diagnostic command, or other transient process. The failed launch itself did not dispatch a formal runner or wrapper. The empty runtime and idle GPU reports do not retrospectively prove every other process's identity. Classification: unidentified historic argv match, consistent with a false positive; exact attribution unknown.

Direct answers:

- Real formal runner? NOT PROVEN; none dispatched by this failed attempt.
- Durable wrapper? NOT PROVEN; none dispatched by this failed attempt.
- Merely an argv-string match? OBSERVED detector semantics; whether the process was unrelated is NOT PROVEN.
- Exact identity provable? NO with retained evidence.
- Why can V1 flag unrelated processes? It applies Path(arg).name to every argv item, including data/search/file arguments. It does not inspect /proc/exe, script operand position, process cwd, runtime, resume mode or process birth identity.

Confidence: high in the detector defect and fail-before-dispatch sequence; low/unknown in any specific identity assigned to PID 602690. V2 fixes the demonstrated class of defects without inventing missing history.
