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
