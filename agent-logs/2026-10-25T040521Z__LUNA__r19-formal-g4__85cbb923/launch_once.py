#!/home/lizening/miniconda3/bin/python3
"""Single-attempt exact-argv launcher for the explicitly cleared offline G4."""

import datetime as dt
import hashlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path


TASK = Path(__file__).resolve().parent
CLEARANCE_DIR = Path(
    "/home/lizening/research-notes/agent-logs/"
    "2026-10-25T035854Z__SOL__r19-g4-exact-proposal-clearance__85cbb923_fd79db"
)
PROPOSAL_REVIEW = CLEARANCE_DIR / "proposal_and_drift_review.json"
CLEARANCE = CLEARANCE_DIR / "offline_G4_execution_clearance.json"
ARGV_PATH = CLEARANCE_DIR / "proposed_analyzer_argv.json"
ENV_PATH = CLEARANCE_DIR / "proposed_environment.json"
PREHASH_PATH = TASK / "pre_execution_input_hashes.json"
LATCH_PATH = TASK / "analyzer_attempt_latch.json"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_sha(obj) -> str:
    return sha256(
        json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    )


def write_durable(path: Path, obj) -> None:
    data = (json.dumps(obj, indent=2, ensure_ascii=False) + "\n").encode()
    with path.open("xb") as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat()


clearance = json.loads(CLEARANCE.read_text())
argv = json.loads(ARGV_PATH.read_text())
plan = json.loads(ENV_PATH.read_text())
review = json.loads(PROPOSAL_REVIEW.read_text())
marker = json.loads((TASK / "consumption_marker.json").read_text())

if marker.get("clearance_id") != clearance.get("clearance_id"):
    raise SystemExit("STOP: consumption marker does not match clearance")
if marker.get("consumption_status") != "CONSUMED_BEFORE_FIRST_CHILD_START":
    raise SystemExit("STOP: clearance is not durably marked consumed")
if marker.get("analysis_identity") != "r19-g4-offline-2026-10-25T040521Z-ebad1a0c":
    raise SystemExit("STOP: unexpected analysis identity")
if clearance.get("maximum_analyzer_invocations") != 1 or clearance.get("automatic_retry") is not False:
    raise SystemExit("STOP: clearance invocation bounds differ")
if not argv or argv[0] != "/home/lizening/miniconda3/envs/alfworld-self-improve/bin/python":
    raise SystemExit("STOP: approved pinned interpreter mismatch")
if "--allow-synthetic" in argv:
    raise SystemExit("STOP: synthetic override is forbidden")
if argv != json.loads(
    Path("/home/lizening/research-notes/agent-logs/2026-10-23T043602Z__LUNA__r19-g4-readiness__85cbb923/proposed_analyzer_argv.json").read_text()
):
    raise SystemExit("STOP: argv differs from independently reviewed proposal")
approved_env = plan.get("set")
if plan.get("inherit_unspecified_environment") is not False or not isinstance(approved_env, dict):
    raise SystemExit("STOP: environment inheritance is not disabled")
if set(approved_env) != set(clearance["effective_environment"]):
    raise SystemExit("STOP: environment allowlist keys differ")
if approved_env != clearance["effective_environment"]:
    raise SystemExit("STOP: environment values differ from clearance")
if sha256(ARGV_PATH.read_bytes()) != clearance["argv_raw_sha256"]:
    raise SystemExit("STOP: approved argv raw hash mismatch")
if canonical_sha(argv) != clearance["argv_canonical_sha256"]:
    raise SystemExit("STOP: approved argv canonical hash mismatch")
if sha256(ENV_PATH.read_bytes()) != clearance["environment_raw_sha256"]:
    raise SystemExit("STOP: approved environment raw hash mismatch")
if canonical_sha(plan) != clearance["environment_canonical_sha256"]:
    raise SystemExit("STOP: approved environment canonical hash mismatch")

output_path = Path(clearance["planned_output_path"])
if output_path.exists() or output_path.is_symlink():
    raise SystemExit("STOP: authorized output path collision")
if LATCH_PATH.exists() or PREHASH_PATH.exists():
    raise SystemExit("STOP: prior attempt/latch evidence exists; no retry")

expected = review["input_sha256"]
observed = {}
for raw_path, expected_hash in expected.items():
    path = Path(raw_path)
    if not path.is_file():
        raise SystemExit(f"STOP: bound input is missing: {raw_path}")
    actual_hash = sha256(path.read_bytes())
    observed[raw_path] = actual_hash
    if actual_hash != expected_hash:
        raise SystemExit(f"STOP: bound input drift: {raw_path}")
write_durable(
    PREHASH_PATH,
    {
        "schema_version": "r19_formal_g4_pre_execution_hashes_v1",
        "recorded_at_utc": utc_now(),
        "clearance_id": clearance["clearance_id"],
        "count": len(observed),
        "all_match_exact_proposal_review": True,
        "sha256": observed,
    },
)

# Exclusive durable latch: a second helper invocation can never start another child.
write_durable(
    LATCH_PATH,
    {
        "schema_version": "r19_formal_g4_analyzer_attempt_latch_v1",
        "clearance_id": clearance["clearance_id"],
        "analysis_identity": marker["analysis_identity"],
        "attempt_latched_at_utc": utc_now(),
        "analyzer_invocation_allowance_consumed": True,
        "retry_permitted": False,
    },
)

stdout_path = TASK / "analyzer.stdout.raw"
stderr_path = TASK / "analyzer.stderr.raw"
started_at = utc_now()
started_monotonic = time.monotonic()
try:
    with stdout_path.open("xb") as stdout_stream, stderr_path.open("xb") as stderr_stream:
        process = subprocess.Popen(
            argv,
            cwd=plan["cwd"],
            env=approved_env,
            stdin=subprocess.DEVNULL,
            stdout=stdout_stream,
            stderr=stderr_stream,
            shell=False,
        )
        start_receipt = {
            "schema_version": "r19_formal_g4_child_start_v1",
            "analysis_identity": marker["analysis_identity"],
            "clearance_id": clearance["clearance_id"],
            "pid": process.pid,
            "started_at_utc": started_at,
            "argv": argv,
            "argv_canonical_sha256": canonical_sha(argv),
            "cwd": plan["cwd"],
            "environment": approved_env,
            "environment_canonical_sha256": canonical_sha(plan),
            "stdout_path": str(stdout_path),
            "stderr_path": str(stderr_path),
            "shell": False,
        }
        write_durable(TASK / "child_start.json", start_receipt)
        print(f"ANALYZER_CHILD_STARTED pid={process.pid} started_at_utc={started_at}", flush=True)
        try:
            returncode = process.wait()
        except BaseException as error:
            write_durable(
                TASK / "wait_exception.json",
                {
                    "exception_type": type(error).__name__,
                    "exception": repr(error),
                    "observed_at_utc": utc_now(),
                    "pid": process.pid,
                    "retry_permitted": False,
                },
            )
            raise
        finished_at = utc_now()
        exit_receipt = {
            "schema_version": "r19_formal_g4_child_exit_v1",
            "analysis_identity": marker["analysis_identity"],
            "clearance_id": clearance["clearance_id"],
            "pid": process.pid,
            "started_at_utc": started_at,
            "finished_at_utc": finished_at,
            "duration_seconds": time.monotonic() - started_monotonic,
            "returncode": returncode,
            "returncode_source": "subprocess.Popen.wait",
            "interrupted": False,
            "stdout_path": str(stdout_path),
            "stderr_path": str(stderr_path),
            "retry_permitted": False,
        }
        write_durable(TASK / "child_exit.json", exit_receipt)
        print(f"ANALYZER_CHILD_EXIT returncode={returncode} finished_at_utc={finished_at}", flush=True)
        sys.exit(returncode)
except Exception as error:
    exception_path = TASK / "launch_exception.json"
    if not exception_path.exists():
        write_durable(
            exception_path,
            {
                "exception_type": type(error).__name__,
                "exception": repr(error),
                "observed_at_utc": utc_now(),
                "phase": "child_start_or_capture",
                "retry_permitted": False,
            },
        )
    raise
