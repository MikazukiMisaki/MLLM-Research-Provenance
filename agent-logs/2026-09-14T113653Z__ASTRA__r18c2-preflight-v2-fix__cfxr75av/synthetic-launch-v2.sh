#!/usr/bin/env bash
set -eu
umask 077
base=$(cd "$(dirname "$0")" && pwd)
job="$base/synthetic-jobs/$1"
mkdir -p "$base/synthetic-jobs"
mkdir "$job"
export SYNTHETIC_SENTINEL='retained value $ ;'
export SYNTHETIC_EXIT="$2"
export SYNTHETIC_JOB="$job"
printf '%s\n' "$$" > "$job/dispatch-shell.pid"
# Synthetic payload only: no scientific script, data, model or runtime is invoked.
nohup setsid --fork /usr/bin/bash --noprofile --norc "$base/durable-wrapper-v2.sh" "$job" "$base" "$base/synthetic-launch.lock" /home/lizening/miniconda3/envs/alfworld-self-improve/bin/python "$base/synthetic-payload-v2.py" --output "$base/synthetic-runtime" --resume > "$job/dispatch.log" 2>&1 < /dev/null &
printf '%s\n' "$!" > "$job/dispatch.pid"
printf 'SYNTHETIC_DISPATCH_RETURNED %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
