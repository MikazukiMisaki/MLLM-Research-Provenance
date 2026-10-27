#!/usr/bin/env python3
"""Verify the reviewed release and invoke its one exact source preflight once."""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time


TASK = Path("/home/lizening/research-notes/agent-logs/2026-10-27T001612Z__SOL__si-s01-A96-source-authority__f1e0d56_f96b86f3")
OWN = Path("/home/lizening/research-notes/agent-logs/2026-10-27T001713Z__LUNA__si-s01-source-preflight__f96b86f3")
EXPECTED = {
    "SOURCE_PREFLIGHT_ONLY_RELEASE.json": "56fce9fccf33e33f624f97e156bebcf1ad7c32a7ac6eba6c26a13f4507543e4a",
    "ROOT_SOURCE_AUTHORIZATION_V2.json": "cf25576d5bf019a925cb1cd1d878046921162f136de173dad870ce8365e40a05",
    "SOURCE_EXACT_COMMANDS.json": "149953aab65001c79f5838c03c1c401867459ccf5976854c58e854cf2133e19a",
    "SOURCE_PRODUCTION_PROPOSAL.json": "227eef584d8d8bd991e4e783eebb1203f249f9e64835282ba5b4e69328e02580",
    "SOURCE_CONCRETE_RELEASE_REVIEW.json": "93acff00d94a5dbf632c4460ab88aceb70dc51fe1a25a820aed60830f3588b82",
}


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def utcnow() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat().replace("+00:00", "Z")


def durable_json(path: Path, value: object, *, exclusive: bool = True) -> None:
    flags = os.O_WRONLY | os.O_CREAT | (os.O_EXCL if exclusive else os.O_TRUNC)
    fd = os.open(path, flags, 0o600)
    with os.fdopen(fd, "wb") as stream:
        stream.write((json.dumps(value, sort_keys=True, indent=2, ensure_ascii=False) + "\n").encode())
        stream.flush()
        os.fsync(stream.fileno())
    dfd = os.open(path.parent, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0))
    try:
        os.fsync(dfd)
    finally:
        os.close(dfd)


def git(root: Path, *args: str) -> str:
    result = subprocess.run(["git", "-C", str(root), *args], check=True, capture_output=True, text=True)
    return result.stdout.strip()


def main() -> int:
    if os.geteuid() != 2000:
        raise RuntimeError(f"unexpected uid: {os.geteuid()}")
    if not OWN.is_dir() or OWN.stat().st_uid != 2000 or (OWN.stat().st_mode & 0o777) != 0o700:
        raise RuntimeError("own evidence directory missing or not private mode 0700")

    file_hashes = {}
    for name, expected in EXPECTED.items():
        data = (TASK / name).read_bytes()
        actual = sha(data)
        file_hashes[name] = actual
        if actual != expected:
            raise RuntimeError(f"release binding mismatch: {name}")

    release = json.loads((TASK / "SOURCE_PREFLIGHT_ONLY_RELEASE.json").read_text())
    authorization = json.loads((TASK / "ROOT_SOURCE_AUTHORIZATION_V2.json").read_text())
    commands = json.loads((TASK / "SOURCE_EXACT_COMMANDS.json").read_text())
    proposal = json.loads((TASK / "SOURCE_PRODUCTION_PROPOSAL.json").read_text())

    argv = commands["preflight_argv"]
    env = commands["environment"]
    cwd = Path(commands["cwd"])
    auth_argv_template = authorization["preflight_argv"]
    auth_sha = file_hashes["ROOT_SOURCE_AUTHORIZATION_V2.json"]
    if (argv != release["allowed_argv"] or len(auth_argv_template) != len(argv)
            or auth_argv_template.count("@AUTHORIZATION_SHA256@") != 1):
        raise RuntimeError("argv differs across release and exact commands, or authorization template is malformed")
    auth_argv_expanded = [auth_sha if item == "@AUTHORIZATION_SHA256@" else item for item in auth_argv_template]
    if auth_argv_expanded != argv:
        raise RuntimeError("authorization argv template does not expand to the reviewed exact command")
    if sha(canonical(argv)) != commands["preflight_argv_sha256"]:
        raise RuntimeError("canonical argv digest mismatch")
    env_sha = sha(canonical(env))
    if env_sha != commands["environment_sha256"] or env_sha != release["environment_sha256"]:
        raise RuntimeError("canonical environment digest mismatch")
    if env != authorization["environment"] or len(env) != 13:
        raise RuntimeError("environment is not the reviewed exact 13-key mapping")
    if any(k in env for k in ("PYTHONPATH", "PYTHONHOME", "VIRTUAL_ENV")):
        raise RuntimeError("forbidden Python environment override present")
    if "--preflight-only" not in argv or "--live" in argv or "--worker" in argv:
        raise RuntimeError("argv is not the released zero-science preflight mode")
    if commands["inherit_environment"] is not False:
        raise RuntimeError("release requires an explicit isolated environment")
    if release["status"] != "RELEASED_ONE_SOURCE_ZERO_SCIENCE_PREFLIGHT_ONLY":
        raise RuntimeError("preflight release status is not active")
    if authorization["status"] != "PREFLIGHT_ONLY" or authorization["maximum_launches"] != 1:
        raise RuntimeError("authorization status/cap mismatch")
    if authorization["source_sha"] != release["source_sha"] or commands["source_sha"] != release["source_sha"]:
        raise RuntimeError("source SHA bindings disagree")
    if authorization["output_path"] != commands["output_path"] or authorization["preflight_receipt_path"] != release["preflight_receipt_path"]:
        raise RuntimeError("output or receipt path bindings disagree")
    if authorization["proposal_sha256"] != sha((TASK / "SOURCE_PRODUCTION_PROPOSAL.json").read_bytes()):
        raise RuntimeError("authorization proposal binding mismatch")
    if sha((TASK / "SOURCE_PRODUCTION_PROPOSAL.json").read_bytes()) != authorization["proposal_sha256"]:
        raise RuntimeError("proposal SHA differs from authorization")
    if proposal.get("schema") is None:
        raise RuntimeError("proposal schema is absent")
    now = dt.datetime.now(dt.timezone.utc)
    start = dt.datetime.fromisoformat(authorization["not_before_utc"].replace("Z", "+00:00"))
    expiry = dt.datetime.fromisoformat(authorization["expires_utc"].replace("Z", "+00:00"))
    if not (start <= now < expiry):
        raise RuntimeError("authorization is outside its validity interval")

    head = git(cwd, "rev-parse", "HEAD")
    branch = git(cwd, "branch", "--show-current")
    status = git(cwd, "status", "--porcelain=v1")
    if head != release["source_sha"] or status:
        raise RuntimeError(f"source checkout drift: head={head}, dirty={bool(status)}")
    remote_ref = "refs/heads/" + branch
    remote = subprocess.run(["git", "-C", str(cwd), "ls-remote", "origin", remote_ref], check=True, capture_output=True, text=True).stdout.strip()
    remote_sha = remote.split("\t", 1)[0] if remote else ""
    if remote_sha != head:
        raise RuntimeError(f"remote SHA mismatch: {remote_sha}")

    output = Path(commands["output_path"])
    receipt = Path(release["preflight_receipt_path"])
    if output.exists() or receipt.exists():
        raise RuntimeError("released output or receipt path already exists")
    if argv[0] != "/home/lizening/miniconda3/envs/alfworld-self-improve/bin/python":
        raise RuntimeError("pinned interpreter mismatch")
    if not Path(argv[0]).is_file() or not Path(argv[2]).is_file():
        raise RuntimeError("pinned interpreter or production entrypoint missing")
    if release["source_run_id"] != authorization["run_id"]:
        raise RuntimeError("run identity mismatch")

    script = argv[2]
    active = []
    for proc in Path("/proc").iterdir():
        if not proc.name.isdigit():
            continue
        try:
            args = [part.decode(errors="replace") for part in (proc / "cmdline").read_bytes().split(b"\0") if part]
        except OSError:
            continue
        if script in args:
            active.append(proc.name)
    if active:
        raise RuntimeError(f"same source preflight entrypoint already active: {active}")

    # Byte-copy only the immutable release inputs into Luna's own evidence directory.
    for name in EXPECTED:
        target = OWN / name
        with target.open("xb") as stream:
            stream.write((TASK / name).read_bytes())
            stream.flush()
            os.fsync(stream.fileno())

    precheck = {
        "checked_utc": utcnow(),
        "release_inputs_sha256": file_hashes,
        "authorization_argv_template_expanded_by_bound_sha256": auth_argv_expanded == argv,
        "argv_sha256_canonical": sha(canonical(argv)),
        "environment_sha256_canonical": env_sha,
        "source_head": head,
        "source_branch": branch,
        "origin_branch_sha": remote_sha,
        "worktree_clean": True,
        "run_id": release["source_run_id"],
        "output_absent": True,
        "receipt_absent": True,
        "same_entrypoint_process_absent": True,
        "evidence_class": "source_preflight_only",
        "model_environment_science_calls_before_child": 0,
    }
    durable_json(OWN / "PRELAUNCH_CHECKS.json", precheck)

    # This durable, exclusive record consumes the single preflight allowance before child start.
    intent = {
        "consumed_utc": utcnow(),
        "release_status": release["status"],
        "run_id": release["source_run_id"],
        "authorization_id": authorization["authorization_id"],
        "argv": argv,
        "argv_sha256_canonical": sha(canonical(argv)),
        "cwd": str(cwd),
        "environment": env,
        "environment_sha256_canonical": env_sha,
        "inherit_environment": False,
        "automatic_retry": False,
        "state": "CONSUMED_BEFORE_CHILD_START",
    }
    durable_json(OWN / "PREFLIGHT_INVOCATION_CONSUMED.json", intent)

    stdout_path = OWN / "preflight.stdout.bin"
    stderr_path = OWN / "preflight.stderr.bin"
    started = utcnow()
    mono_started = time.monotonic()
    with stdout_path.open("xb") as stdout, stderr_path.open("xb") as stderr:
        child = subprocess.Popen(argv, cwd=str(cwd), env=dict(env), stdin=subprocess.DEVNULL,
                                 stdout=stdout, stderr=stderr, shell=False, close_fds=True)
        child_record = {
            "started_utc": started,
            "pid": child.pid,
            "argv": argv,
            "argv_sha256_canonical": sha(canonical(argv)),
            "cwd": str(cwd),
            "environment_sha256_canonical": env_sha,
            "environment_key_count": len(env),
            "inherit_environment": False,
        }
        durable_json(OWN / "CHILD_START.json", child_record)
        returncode = child.wait()
        stdout.flush(); os.fsync(stdout.fileno())
        stderr.flush(); os.fsync(stderr.fileno())
    elapsed = time.monotonic() - mono_started
    ended = utcnow()

    receipt_hash = None
    receipt_bytes = None
    receipt_status = None
    if receipt.is_file():
        rb = receipt.read_bytes()
        receipt_hash = sha(rb)
        receipt_bytes = len(rb)
        try:
            rj = json.loads(rb)
            receipt_status = rj.get("status")
        except Exception:
            receipt_status = "UNPARSEABLE_JSON"
    result = {
        "started_utc": started,
        "ended_utc": ended,
        "child_pid": child.pid,
        "returncode": returncode,
        "elapsed_seconds_monotonic": elapsed,
        "argv": argv,
        "argv_sha256_canonical": sha(canonical(argv)),
        "cwd": str(cwd),
        "environment_sha256_canonical": env_sha,
        "inherit_environment": False,
        "stdout_bytes": stdout_path.stat().st_size,
        "stdout_sha256": sha(stdout_path.read_bytes()),
        "stderr_bytes": stderr_path.stat().st_size,
        "stderr_sha256": sha(stderr_path.read_bytes()),
        "production_receipt_path": str(receipt),
        "production_receipt_exists": receipt.is_file(),
        "production_receipt_bytes": receipt_bytes,
        "production_receipt_sha256": receipt_hash,
        "production_receipt_status": receipt_status,
        "output_path_exists_after": output.exists(),
        "retry": False,
    }
    durable_json(OWN / "SOURCE_PREFLIGHT_SUBPROCESS_RECEIPT.json", result)
    print(json.dumps({"source_run_id": release["source_run_id"], "child_pid": result["child_pid"], "returncode": returncode,
                      "receipt_status": receipt_status, "own_record": str(OWN / "SOURCE_PREFLIGHT_SUBPROCESS_RECEIPT.json")}, sort_keys=True))
    return 0 if returncode == 0 else returncode


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        # A failing pre-launch check is recorded locally and never triggers an alternate command.
        try:
            abort_path = OWN / "PRELAUNCH_ABORT.json"
            suffix = 2
            while abort_path.exists():
                abort_path = OWN / f"PRELAUNCH_ABORT_{suffix:02d}.json"
                suffix += 1
            durable_json(abort_path, {
                "recorded_utc": utcnow(),
                "exception_type": type(exc).__name__,
                "message": str(exc),
                "child_invocation_started": (OWN / "PREFLIGHT_INVOCATION_CONSUMED.json").exists(),
            })
        except Exception:
            pass
        print(f"PRELAUNCH_ABORT: {type(exc).__name__}: {exc}", file=sys.stderr)
        raise
