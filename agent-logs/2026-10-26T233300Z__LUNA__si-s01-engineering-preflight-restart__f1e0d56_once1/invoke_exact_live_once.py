import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time


EVIDENCE = Path("/home/lizening/research-notes/agent-logs/2026-10-26T233300Z__LUNA__si-s01-engineering-preflight-restart__f1e0d56_once1")
RELEASE_DIR = Path("/home/lizening/research-notes/agent-logs/2026-10-26T233148Z__SOL__si-s01-controlled-engineering-restart__f1e0d56_c66ea6e2")
CLEARANCE_PATH = RELEASE_DIR / "ENGINEERING_LIVE_CLEARANCE.json"
COMMANDS_PATH = RELEASE_DIR / "EXACT_COMMANDS.json"
EXPECTED_CLEARANCE = "fe22aaffbbc869deca440f618a031afa6c1fbaffe25e3dd93a0e3efa8d2d889e"
EXPECTED_COMMANDS = "7755960626e6345a2f4da712284fe9239d590dad792eadfae418e137293f3a99"
EXPECTED_AUTH = "8829121a1a6f78ccaaab1010980d9b41a3f7fbbff36120facfa36f1d876851ad"
EXPECTED_PROPOSAL = "a9b1c43ebdafbb2d7e33a2377c34428a5788d91afc140d5bbcf1957d08881c2a"
EXPECTED_RUN = "af705f48405544e9a86eb1da437335a1"
EXPECTED_SOURCE = "f1e0d56a1be2a65876bbec5b8950fb76cda3eace"


def sha(data):
    return hashlib.sha256(data).hexdigest()


def canonical_hash(value):
    return sha(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode())


def write_exclusive(path, payload):
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, "wb") as f:
        f.write(payload)
        f.flush()
        os.fsync(f.fileno())


def main():
    if sha(CLEARANCE_PATH.read_bytes()) != EXPECTED_CLEARANCE or sha(COMMANDS_PATH.read_bytes()) != EXPECTED_COMMANDS:
        raise SystemExit("STOP: clearance/commands digest mismatch; no child started")
    clearance = json.loads(CLEARANCE_PATH.read_text())
    commands = json.loads(COMMANDS_PATH.read_text())
    argv = commands["live_argv"]
    env = commands["environment"]
    if (clearance["run_id"] != EXPECTED_RUN or clearance["source_sha"] != EXPECTED_SOURCE
            or clearance["authorization"]["sha256"] != EXPECTED_AUTH
            or clearance["proposal"]["sha256"] != EXPECTED_PROPOSAL
            or commands["authorization_sha256"] != EXPECTED_AUTH
            or commands["proposal_sha256"] != EXPECTED_PROPOSAL
            or commands["source_sha"] != EXPECTED_SOURCE
            or canonical_hash(argv) != clearance["allowed_live_argv_sha256"]
            or canonical_hash(env) != clearance["environment_sha256"]
            or argv != clearance["allowed_live_argv"]
            or commands["inherit_environment"] is not False
            or commands["retry"] is not False
            or argv[-1] != "--live"):
        raise SystemExit("STOP: command/context binding mismatch; no child started")
    now = datetime.datetime.now(datetime.timezone.utc)
    expires = datetime.datetime.fromisoformat(clearance["expires_utc"].replace("Z", "+00:00"))
    if now >= expires:
        raise SystemExit("STOP: clearance expired; no child started")
    cwd = Path(commands["cwd"])
    output = Path(clearance["output_path"])
    claim = Path(str(output) + ".launch_claim.json")
    if output.exists() or claim.exists():
        raise SystemExit("STOP: output/claim collision; no child started")
    git_head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=cwd, check=True, stdout=subprocess.PIPE, text=True).stdout.strip()
    git_status = subprocess.run(["git", "status", "--porcelain=v1"], cwd=cwd, check=True, stdout=subprocess.PIPE, text=True).stdout
    if git_head != EXPECTED_SOURCE or git_status:
        raise SystemExit("STOP: checkout drift; no child started")
    guard = Path(clearance["old_authority_revocation_guard"]["path"])
    if sha(guard.read_bytes()) != clearance["old_authority_revocation_guard"]["sha256"]:
        raise SystemExit("STOP: old revocation guard mismatch; no child started")
    consumed = EVIDENCE / "LIVE_CLEARANCE_CONSUMED.json"
    if not consumed.is_file():
        raise SystemExit("STOP: durable consumption marker absent; no child started")
    attempt = EVIDENCE / "LIVE_CHILD_START_ATTEMPT.json"
    stdout_path = EVIDENCE / "live.stdout.bin"
    stderr_path = EVIDENCE / "live.stderr.bin"
    receipt_path = EVIDENCE / "live_subprocess_receipt.json"
    if any(p.exists() for p in (attempt, stdout_path, stderr_path, receipt_path)):
        raise SystemExit("STOP: local invocation evidence already exists; no child started")
    start_utc = datetime.datetime.now(datetime.timezone.utc).isoformat()
    start_ns = time.monotonic_ns()
    attempt_payload = json.dumps({
        "schema": "SI_S01_LIVE_CHILD_START_ATTEMPT_V1",
        "clearance_sha256": EXPECTED_CLEARANCE,
        "run_id": EXPECTED_RUN,
        "argv_sha256": canonical_hash(argv),
        "environment_sha256": canonical_hash(env),
        "cwd": str(cwd),
        "attempt_started_utc": start_utc,
        "retry": False,
    }, sort_keys=True, indent=2).encode() + b"\n"
    write_exclusive(attempt, attempt_payload)
    child = None
    try:
        with stdout_path.open("xb") as out, stderr_path.open("xb") as err:
            child = subprocess.Popen(argv, cwd=str(cwd), env=env, stdin=subprocess.DEVNULL,
                                     stdout=out, stderr=err, shell=False, close_fds=True)
            started = {
                "event": "LIVE_CHILD_STARTED",
                "pid": child.pid,
                "run_id": EXPECTED_RUN,
                "start_utc": start_utc,
                "argv_sha256": canonical_hash(argv),
                "environment_sha256": canonical_hash(env),
                "cwd": str(cwd),
            }
            print(json.dumps(started, sort_keys=True), flush=True)
            returncode = child.wait()
            end_ns = time.monotonic_ns()
            end_utc = datetime.datetime.now(datetime.timezone.utc).isoformat()
            out.flush()
            err.flush()
            os.fsync(out.fileno())
            os.fsync(err.fileno())
        stdout_bytes = stdout_path.read_bytes()
        stderr_bytes = stderr_path.read_bytes()
        receipt = {
            "schema": "SI_S01_AUTHENTIC_LIVE_SUBPROCESS_RECEIPT_V1",
            "run_id": EXPECTED_RUN,
            "pid": child.pid,
            "returncode": returncode,
            "start_utc": start_utc,
            "end_utc": end_utc,
            "elapsed_monotonic_ns": end_ns - start_ns,
            "argv": argv,
            "argv_sha256": canonical_hash(argv),
            "cwd": str(cwd),
            "environment": env,
            "environment_sha256": canonical_hash(env),
            "inherit_environment": False,
            "shell": False,
            "stdin": "DEVNULL",
            "stdout_path": str(stdout_path),
            "stdout_bytes": len(stdout_bytes),
            "stdout_sha256": sha(stdout_bytes),
            "stderr_path": str(stderr_path),
            "stderr_bytes": len(stderr_bytes),
            "stderr_sha256": sha(stderr_bytes),
        }
        write_exclusive(receipt_path, json.dumps(receipt, sort_keys=True, indent=2).encode() + b"\n")
        print(json.dumps({"event": "LIVE_CHILD_FINISHED", "pid": child.pid,
                          "returncode": returncode, "end_utc": end_utc,
                          "elapsed_monotonic_ns": end_ns - start_ns}, sort_keys=True), flush=True)
        return returncode
    except BaseException as exc:
        error = {
            "schema": "SI_S01_LIVE_LAUNCHER_EXCEPTION_V1",
            "run_id": EXPECTED_RUN,
            "child_pid": child.pid if child is not None else None,
            "child_started": child is not None,
            "exception_type": type(exc).__name__,
            "exception": repr(exc),
            "observed_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        }
        try:
            write_exclusive(EVIDENCE / "live_launcher_exception.json",
                            json.dumps(error, sort_keys=True, indent=2).encode() + b"\n")
        except FileExistsError:
            pass
        print(json.dumps({"event": "LIVE_LAUNCHER_EXCEPTION", **error}, sort_keys=True), flush=True)
        raise


if __name__ == "__main__":
    sys.exit(main())
