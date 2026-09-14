# Durable R18-C2 launcher recommendation — DESIGN ONLY

**OBSERVED:** tmux, screen, systemd-run, systemctl, and pstree are unavailable in this container. There is no usable systemd user manager to test. nohup, setsid, flock, Bash and Python exist. No installation, service change, or linger change was made.

**OBSERVED:** Two ~35-second synthetic jobs using the proposed wrapper survived the launch shell's completion and were observed alive from separate command invocations. Both had no controlling TTY, stdin `/dev/null`, one Python payload child, preserved environment sentinel (including spaces, shell metacharacters and newline), seven timestamp/PID/PPID/PGID/SID records, and seven stderr records. Natural statuses **7** and **0** were automatically persisted. All launcher and Python PIDs disappeared after completion. A concurrent attempt using the shared external lock was rejected with launcher.error=75 before a Python child was created. See launcher-test.log and launcher-test-results.json.

**INFERRED recommendation:** Use **nohup + setsid --fork + a dedicated external Bash wrapper**, started by a single file-based command. This is the simplest available mechanism demonstrated to work here. It separates monitoring from launching and avoids the IDE's multi-line command parsing and tee/status-capture failure.

**NOT PROVEN:** Survival of an actual IDE shutdown, SSH disconnection, container teardown, host reboot, explicit descendant/cgroup kill, or SIGKILL of the wrapper. These were not tested. New session and ignored SIGHUP remove ordinary terminal coupling; they do not defeat administrative process cleanup. If the wrapper is killed before it records its child's status, runner.exitcode must remain absent/UNKNOWN, never manually fabricated. A wrapper-only termination can leave the Python child alive; inspect its identity and the formal lock before any later decision.

## A. Launch — later authorization only

No formal command in this document was executed. A new explicit authorization must name frozen SHA `aa9fa3c34520941e7e3be00294b111e8254fd65b`. Setting an environment variable is merely an operational guard and is **not** itself user authorization.

Before the future launch, inspect current `ps -eo pid,ppid,pgid,sid,tty,stat,args` and `nvidia-smi` from the authoritative worktree. Stop for any active R18-C2 runner, competing scientific job, unexplained live launcher/runner identity, changed manifest/accepted set, or ambiguous previous attempt. Review older task records explicitly: the known Gemini runner.exitcode=1 is synthetic and the present forensic audit resolves that record as unknown Python status with no live runner. No “IDE disconnected” message is sufficient grounds for a launch.

The supplied read-only `future-preflight.py` checks exact local/remote SHA, branch, cleanliness, environment, existing adapter/config/data paths, unchanged runtime file hashes/counters, absence of formal reports, owner assignment, active runner/wrapper command lines, recorded PID/start-time identities, and nonblocking formal lock availability. It imports only the standard library and never imports the runner. Its hash gate intentionally stops if runtime state differs from this audit; a changed accepted set needs a new review, not automatic adaptation. It compares only the explicitly authorized runtime/control files, not held-out data.

After separate authorization, execute ONE file-based command (the full launch script follows below):

```bash
R18C2_AUTHORIZED_SHA=aa9fa3c34520941e7e3be00294b111e8254fd65b /usr/bin/bash /home/lizening/research-notes/agent-logs/2026-09-14T054711Z__ASTRA__r18c2-operational-forensics__nvrcqcpb/future-launch.sh.txt
```

This file is deliberately named `.txt` and was only syntax-checked. Do not paste its multi-line body into the IDE's command executor. The printed TASK_RECORD_DIR identifies a fresh, private external attempt. Preserve that exact directory for all monitoring and final recording.

```bash
#!/usr/bin/env bash
# DESIGN ONLY. Execute only after NEW explicit user authorization for this SHA.
set -e
set -o pipefail
umask 077
frozen_sha=aa9fa3c34520941e7e3be00294b111e8254fd65b
[[ "${R18C2_AUTHORIZED_SHA:-}" == "$frozen_sha" ]] || { echo 'STOP: separate authorization required'; exit 64; }
audit_dir=/home/lizening/research-notes/agent-logs/2026-09-14T054711Z__ASTRA__r18c2-operational-forensics__nvrcqcpb
repo_dir=/home/lizening/Alfworld-Self-Improvement-Project
python_bin=/home/lizening/miniconda3/envs/alfworld-self-improve/bin/python
source /home/lizening/miniconda3/etc/profile.d/conda.sh
conda activate alfworld-self-improve
export ALFWORLD_DATA=/home/lizening/alfworld_data
export ALFWORLD_CONFIG_PATH=/home/lizening/Alfworld-Self-Improvement-Project/configs/local/alfworld_base_university.yaml
export TOKENIZERS_PARALLELISM=false
export PYTHONPATH=.
cd "$repo_dir"
TASK_RECORD_DIR=$(mktemp -d "/home/lizening/research-notes/agent-logs/$(date -u +%Y-%m-%dT%H%M%SZ)__GEMINI__r18c2-durable-resume__XXXXXXXX")
export TASK_RECORD_DIR
printf 'TASK_RECORD_DIR=%s\n' "$TASK_RECORD_DIR"
printf 'GEMINI TASK RECORD\n\nSTATUS: PREFLIGHT\nSHA: %s\n' "$frozen_sha" > "$TASK_RECORD_DIR/RECORD.md"
cat /proc/sys/kernel/random/boot_id > "$TASK_RECORD_DIR/boot-id.txt"
# Fail closed and preserve this new record on preflight error.
if ! (
  git fetch origin && "$python_bin" "$audit_dir/future-preflight.py"
) > "$TASK_RECORD_DIR/preflight.log" 2>&1; then
  printf 'STATUS: STOP; inspect preflight.log; no runner launched\n' >> "$TASK_RECORD_DIR/RECORD.md"
  exit 65
fi
nvidia-smi > "$TASK_RECORD_DIR/gpu-before.txt"
# Review current processes/GPU BEFORE using this script; no competing scientific job.
# This external lock is shared by future attempts, separate from scientific writer.lock.
launch_control=/home/lizening/research-notes/r18c2-launch-control
mkdir -p "$launch_control"
cp "$audit_dir/durable-wrapper.sh" "$TASK_RECORD_DIR/durable-wrapper.sh"
sha256sum "$TASK_RECORD_DIR/durable-wrapper.sh" > "$TASK_RECORD_DIR/wrapper.sha256"
printf 'LAUNCH_REQUEST UTC=%s SHA=%s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$frozen_sha" > "$TASK_RECORD_DIR/commands.log"
# The only formal Python child is this command. No tee, no monitoring-shell PIPESTATUS.
nohup setsid --fork /usr/bin/bash --noprofile --norc \
  "$TASK_RECORD_DIR/durable-wrapper.sh" \
  "$TASK_RECORD_DIR" "$repo_dir" "$launch_control/launcher.lock" \
  "$python_bin" scripts/run_progress_aware_card_v2_r18_c2.py \
  --output artifacts/runtime/validation/progress-aware-r18-c2-formal-aa9fa3c34520941e \
  --resume > "$TASK_RECORD_DIR/dispatch.log" 2>&1 < /dev/null &
printf '%s\n' "$!" > "$TASK_RECORD_DIR/dispatch.pid"
printf 'STATUS: DISPATCHED; completion not yet known\n' >> "$TASK_RECORD_DIR/RECORD.md"
printf 'DISPATCHED ONLY. Monitor %s; never relaunch on missing marker or IDE disconnect.\n' "$TASK_RECORD_DIR"
```

The tested wrapper copied by that script is:

```bash
#!/usr/bin/env bash
# Infrastructure only: command is supplied as arguments, never evaluated as text.
set -u
set -o pipefail
umask 077
job_dir=$1
work_dir=$2
launch_lock=$3
shift 3
[[ -d "$job_dir" && -d "$work_dir" && $# -gt 0 ]] || exit 64
# A task directory is single use, even after a failed launch.
mkdir "$job_dir/launch.claim" || exit 73
set -C
exec > "$job_dir/runner.log" 2>&1 < /dev/null || exit 74
exec 9>> "$launch_lock" || exit 74
if ! flock -n 9; then
  printf 'DUPLICATE_LAUNCH_REJECTED\n'
  printf '75\n' > "$job_dir/launcher.error"
  exit 75
fi
cd "$work_dir" || exit 72
atomic() {
  printf '%s\n' "$2" > "$job_dir/$1.tmp" && mv "$job_dir/$1.tmp" "$job_dir/$1"
}
identity() {
  local raw rest
  IFS= read -r raw < "/proc/$2/stat" || return 1
  rest=${raw##*) }
  local -a fields
  read -r -a fields <<< "$rest"
  printf '%s %s\n' "$2" "${fields[19]}" > "$job_dir/$1.identity"
}
atomic launcher.pid "$$" || exit 74
identity launcher "$$" || exit 74
printf 'LAUNCHER_START %s PID=%s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$$"
printf 'CWD=%s\nCOMMAND=' "$PWD"
printf '%q ' "$@"
printf '\n'
for var in ALFWORLD_DATA ALFWORLD_CONFIG_PATH TOKENIZERS_PARALLELISM PYTHONPATH CONDA_PREFIX CUDA_VISIBLE_DEVICES; do
  if [[ -v $var ]]; then printf '%s=%q\n' "$var" "${!var}"; fi
done
# FD 9 remains held by wrapper and inherited child; it is NOT the runner's lock.
"$@" < /dev/null &
runner_pid=$!
atomic runner.pid "$runner_pid"
identity runner "$runner_pid" || true
# No errexit: nonzero child status must reach this wait and persistence path.
wait "$runner_pid"
runner_rc=$?
atomic runner.exitcode "$runner_rc" || exit 74
printf 'RUNNER_EXIT %s status=%s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$runner_rc"
sha256sum "$job_dir/runner.log" > "$job_dir/runner.log.sha256"
chmod 0444 "$job_dir/runner.log" "$job_dir/runner.exitcode" "$job_dir/runner.log.sha256"
exit "$runner_rc"
```

**Environment:** Conda activation and explicit exports happen inside the one launch-script process. nohup/setsid and the no-profile wrapper inherit that environment; the formal Python command uses the existing absolute interpreter. There is no login shell that could reset exports. No new generation/seed/model parameters are added. PYTHONPATH, ALFWORLD_DATA, ALFWORLD_CONFIG_PATH and TOKENIZERS_PARALLELISM retain the previously required values. The wrapper logs selected operational variables, not credentials or the entire environment.

**One child / status:** A single formal Python child is launched, its PID is saved immediately, and its supervising wrapper performs `wait` and records `$?` automatically via temporary file plus rename. The launch shell's status and `dispatch.pid` describe dispatch only, never Python completion. `setsid --fork` may change PID, so the wrapper's own launcher.pid is authoritative. On child signal termination, Bash wait returns its signal-encoded status; do not pretend a shell 128+signal value is a Python exception code.

**Logs:** A new task directory plus atomic launch.claim and noclobber prevent reusing/truncating runner.log. The wrapper writes stdout+stderr directly to it, seals it read-only and writes a SHA256 after natural completion. This is single-use, operationally immutable evidence, **not** filesystem-enforced tamper-proof storage: its owner could still deliberately change permissions. Do not edit it. Live logs are necessarily writable by the running wrapper/child. If killed, logs remain incomplete and unsealed, which must be recorded.

**Locks:** `/home/lizening/research-notes/r18c2-launch-control/launcher.lock` is a separate external serialization lock created only by a future launch. It is never the scientific writer.lock. Its file descriptor is held for the wrapper's lifetime and inherited by the child, so an orphaned child still prevents cooperating duplicate wrappers. The scientific runner retains its own fcntl protection unchanged. A preflight probe of writer.lock must use an existing file without truncation, acquire nonblocking and immediately release; do not hold it while starting the real runner, which needs to acquire it itself. A probe has a time-of-check race; the runner's own lock is the final authority. Never delete either lock to bypass a refusal.

**Duplicate policy:** A duplicate using the same task directory fails atomic launch.claim before opening runner.log. A concurrent attempt with another directory fails the shared external flock before Python starts. A completed or failed directory is permanently single-use. These defenses do not authorize a new attempt; every real retry still requires explicit authorization. Missing PID or exit files after dispatch are UNKNOWN/PENDING and must trigger read-only inspection, never immediate retry. PID identity includes `/proc` start ticks; compare boot-id.txt as well to detect host reboot/PID reuse. A matching PID number alone does not establish identity.

## B. Monitor — separate invocation, never launch

Set TASK_RECORD_DIR to the exact directory printed by the authorized launch. These are read-only operations:

```bash
# Replace this value with the exact path printed by that future launch.
TASK_RECORD_DIR=/home/lizening/research-notes/agent-logs/EXACT_FUTURE_ATTEMPT
cat "$TASK_RECORD_DIR/dispatch.log"
cat "$TASK_RECORD_DIR/launcher.pid" "$TASK_RECORD_DIR/runner.pid"
cat "$TASK_RECORD_DIR/launcher.identity" "$TASK_RECORD_DIR/runner.identity"
cat "$TASK_RECORD_DIR/boot-id.txt" /proc/sys/kernel/random/boot_id
ps -p "$(cat "$TASK_RECORD_DIR/launcher.pid"),$(cat "$TASK_RECORD_DIR/runner.pid")" -o pid,ppid,pgid,sid,tty,lstart,stat,args
tail -n 50 "$TASK_RECORD_DIR/runner.log"
# Optional continuous view; stopping tail only stops this reader.
tail -F "$TASK_RECORD_DIR/runner.log"
```

Read marker separately; do not write it:

```bash
if test -f "$TASK_RECORD_DIR/runner.exitcode"; then
  cat "$TASK_RECORD_DIR/runner.exitcode"
else
  printf 'PYTHON_EXIT_STATUS_UNKNOWN_OR_STILL_RUNNING
'
fi
# Only after the wrapper has finished sealing the log:
if test -f "$TASK_RECORD_DIR/runner.log.sha256"; then
  sha256sum -c "$TASK_RECORD_DIR/runner.log.sha256"
fi
```

Read the same formal runtime's manifest, branch journal, ledger and events for durable progress; do not invoke the runner, replay helpers, or environment resets for monitoring. Counts of accepted branches and ledger consistency outrank partial log messages. If a child exits nonzero, or disappears without an automatic exit marker, stop and preserve the evidence. If status is zero, still perform the separately authorized final scientific artifact checks before claiming completion. Finalize the future task's RECORD.md for every outcome, including preflight STOP and launch failure.

**NEXT AUTHORIZED STEP: NONE. FORMAL RESUME IN THIS AUDIT: NO.**
