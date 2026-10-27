import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess
import time


EVIDENCE = Path("/home/lizening/research-notes/agent-logs/2026-10-27T000600Z__LUNA__si-s01-amended-preflight__f1e0d56_once1")
RELEASE_DIR = Path("/home/lizening/research-notes/agent-logs/2026-10-27T000517Z__SOL__si-s01-framework-default-amendment__f1e0d56_bf6d2eb7")
RELEASE_PATH = RELEASE_DIR / "PREFLIGHT_ONLY_RELEASE.json"
COMMANDS_PATH = RELEASE_DIR / "EXACT_COMMANDS.json"
EXPECTED_RELEASE = "ffd0fc4bf652801e144761ee2c3c25b1def1c60f3072d16a4ec8d2b1616e2e91"
EXPECTED_COMMANDS = "ee45f22068a3e5f24506561bcde1a9c135b9099ea0d08253081ff741814c08ea"
EXPECTED_AUTH = "588b3f3f49f2f500b78bfab01bb09f31a1f2e129f55037a841aa4bcab8f5450a"
EXPECTED_PROPOSAL = "a9b1c43ebdafbb2d7e33a2377c34428a5788d91afc140d5bbcf1957d08881c2a"
EXPECTED_REVIEW = "6ac8d943ff59d3a3054a6fad6ce618a7fdde230afe1bf8a127da0022b5731f4d"
EXPECTED_SOURCE = "f1e0d56a1be2a65876bbec5b8950fb76cda3eace"


def sha(data):
    return hashlib.sha256(data).hexdigest()


def canonical_hash(value):
    return sha(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode())


def write_exclusive(path, data):
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, "wb") as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())


def main():
    if sha(RELEASE_PATH.read_bytes()) != EXPECTED_RELEASE or sha(COMMANDS_PATH.read_bytes()) != EXPECTED_COMMANDS:
        raise SystemExit("STOP: release/commands SHA mismatch; child not started")
    release = json.loads(RELEASE_PATH.read_text())
    commands = json.loads(COMMANDS_PATH.read_text())
    auth_path = Path(release["authorization"]["path"])
    proposal_path = Path(release["proposal"]["path"])
    review_path = Path(release["review"]["path"])
    auth = json.loads(auth_path.read_text())
    argv = commands["preflight_argv"]
    env = commands["environment"]
    if (sha(auth_path.read_bytes()) != EXPECTED_AUTH
            or sha(proposal_path.read_bytes()) != EXPECTED_PROPOSAL
            or sha(review_path.read_bytes()) != EXPECTED_REVIEW
            or auth["source_sha"] != EXPECTED_SOURCE
            or commands["source_sha"] != EXPECTED_SOURCE
            or commands["authorization_sha256"] != EXPECTED_AUTH
            or commands["proposal_sha256"] != EXPECTED_PROPOSAL
            or auth["environment"] != env
            or canonical_hash(argv) != release["allowed_argv_sha256"]
            or canonical_hash(argv) != commands["preflight_argv_sha256"]
            or canonical_hash(env) != release["environment_sha256"]
            or commands["inherit_environment"] is not False
            or commands["retry"] is not False
            or argv[-1] != "--preflight-only"
            or commands["live_argv"][-1] != "--live"
            or env.get("CUDA_MODULE_LOADING") != "LAZY"):
        raise SystemExit("STOP: release binding mismatch; child not started")
    now = datetime.datetime.now(datetime.timezone.utc)
    not_before = datetime.datetime.fromisoformat(auth["not_before_utc"].replace("Z", "+00:00"))
    expires = datetime.datetime.fromisoformat(auth["expires_utc"].replace("Z", "+00:00"))
    if not (not_before <= now < expires):
        raise SystemExit("STOP: authorization time window invalid; child not started")
    cwd = Path(commands["cwd"])
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=cwd, check=True,
                          stdout=subprocess.PIPE, text=True).stdout.strip()
    status = subprocess.run(["git", "status", "--porcelain=v1"], cwd=cwd, check=True,
                            stdout=subprocess.PIPE, text=True).stdout
    if head != EXPECTED_SOURCE or status:
        raise SystemExit("STOP: source checkout drift; child not started")
    output = Path(commands["output_path"])
    if output.exists() or Path(str(output) + ".launch_claim.json").exists():
        raise SystemExit("STOP: output/claim collision; child not started")
    claims = release["old_claims_must_remain"]
    for item in claims:
        p = Path(item["path"])
        if not p.is_file() or sha(p.read_bytes()) != item["sha256"]:
            raise SystemExit("STOP: historical claim drift; child not started")
    consumed = EVIDENCE / "PREFLIGHT_RELEASE_CONSUMED.json"
    if not consumed.is_file():
        raise SystemExit("STOP: preflight consumption marker absent; child not started")
    attempt = EVIDENCE / "PREFLIGHT_START_ATTEMPT.json"
    stdout_path = EVIDENCE / "preflight.stdout.bin"
    stderr_path = EVIDENCE / "preflight.stderr.bin"
    receipt_path = EVIDENCE / "preflight_subprocess_receipt.json"
    if any(p.exists() for p in (attempt, stdout_path, stderr_path, receipt_path)):
        raise SystemExit("STOP: evidence collision; child not started")
    start_utc = datetime.datetime.now(datetime.timezone.utc).isoformat()
    start_ns = time.monotonic_ns()
    write_exclusive(attempt, json.dumps({
        "schema": "SI_S01_AMENDED_PREFLIGHT_START_ATTEMPT_V1",
        "release_sha256": EXPECTED_RELEASE,
        "run_id": auth["run_id"],
        "argv_sha256": canonical_hash(argv),
        "environment_sha256": canonical_hash(env),
        "start_utc": start_utc,
        "cwd": str(cwd),
        "retry": False,
    }, sort_keys=True, indent=2).encode() + b"\n")
    with stdout_path.open("xb") as out, stderr_path.open("xb") as err:
        child = subprocess.Popen(argv, cwd=str(cwd), env=env, stdin=subprocess.DEVNULL,
                                 stdout=out, stderr=err, shell=False, close_fds=True)
        print(json.dumps({"event": "PREFLIGHT_CHILD_STARTED", "pid": child.pid,
                          "run_id": auth["run_id"], "start_utc": start_utc,
                          "argv_sha256": canonical_hash(argv),
                          "environment_sha256": canonical_hash(env)}, sort_keys=True), flush=True)
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
        "schema": "SI_S01_AMENDED_PREFLIGHT_SUBPROCESS_RECEIPT_V1",
        "release_sha256": EXPECTED_RELEASE,
        "run_id": auth["run_id"],
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
    print(json.dumps({"event": "PREFLIGHT_CHILD_FINISHED", "pid": child.pid,
                      "returncode": returncode, "end_utc": end_utc,
                      "elapsed_monotonic_ns": end_ns - start_ns}, sort_keys=True), flush=True)
    return returncode


if __name__ == "__main__":
    raise SystemExit(main())
