#!/usr/bin/env bash
set -eu
umask 077
base_dir=$(cd -- "$(dirname -- "$0")" && pwd)
export LAUNCH_TEST_SENTINEL=$'space and $literal; line\nsecond'
job_dir="$base_dir/synthetic-$1"
mkdir "$job_dir"
printf '%s\n' "$$" > "$job_dir/dispatch-shell.pid"
nohup setsid --fork /usr/bin/bash --noprofile --norc "$base_dir/durable-wrapper.sh" "$job_dir" "$base_dir" "$base_dir/synthetic-shared.lock" /home/lizening/miniconda3/envs/alfworld-self-improve/bin/python "$base_dir/synthetic_payload.py" "$job_dir" "$2" > "$job_dir/dispatch.log" 2>&1 < /dev/null &
printf '%s\n' "$!" > "$job_dir/dispatch.pid"
printf 'DISPATCH_RETURNED %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
