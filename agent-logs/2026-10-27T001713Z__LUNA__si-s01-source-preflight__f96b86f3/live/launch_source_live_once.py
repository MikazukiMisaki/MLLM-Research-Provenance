#!/usr/bin/env python3
"""One-shot launcher for the exact Root-cleared SI-S01 source execution."""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import time
import sys


TASK = Path("/home/lizening/research-notes/agent-logs/2026-10-27T001612Z__SOL__si-s01-A96-source-authority__f1e0d56_f96b86f3")
OWN = Path("/home/lizening/research-notes/agent-logs/2026-10-27T001713Z__LUNA__si-s01-source-preflight__f96b86f3/live")
ROOT_RECORD = Path("/home/lizening/research-notes/agent-logs/2026-10-27T001713Z__LUNA__si-s01-source-preflight__f96b86f3")
PINNED = {
    "SOURCE_EXECUTION_HANDOFF.json": "d2ee23838417dd37e8c4743bfc9b3c39f07c38c1a3fa7182f849fe6ea5538e26",
    "SOURCE_LAUNCH_CLEARANCE_V2.json": "3defb7052665b5ad365093880912f4be8c667d0d3c65979e15373afe014e7524",
    "SOURCE_PREFLIGHT_INDEPENDENT_VERIFICATION.json": "6a305a810c54f3cb5757222143f0564885c418287b4dad249b51ba8a09a89ad1",
    "SOURCE_PREFLIGHT_EXECUTION_V2.json": "6251263dbdb80298e3c8b896de5f316455d8a25a550c37929c5e4383813aff87",
    "ROOT_SOURCE_AUTHORIZATION_V2.json": "cf25576d5bf019a925cb1cd1d878046921162f136de173dad870ce8365e40a05",
    "SOURCE_PRODUCTION_PROPOSAL.json": "227eef584d8d8bd991e4e783eebb1203f249f9e64835282ba5b4e69328e02580",
    "SOURCE_EXACT_COMMANDS.json": "149953aab65001c79f5838c03c1c401867459ccf5976854c58e854cf2133e19a",
    "SOURCE_PREFLIGHT_ONLY_RELEASE.json": "56fce9fccf33e33f624f97e156bebcf1ad7c32a7ac6eba6c26a13f4507543e4a",
    "SOURCE_CONCRETE_RELEASE_REVIEW.json": "93acff00d94a5dbf632c4460ab88aceb70dc51fe1a25a820aed60830f3588b82",
    "CLEARANCE_RENDERING_VERIFICATION.json": "5df732a9f562900f478325168f8f17f116a234b03215caf9c11c6e0309e64c59",
    "HUMAN_TASK_AUTHORITY_BINDING.json": "b924dafe49d645d0ab80fbf7c205c77688bbe6df7f5a8f795c40f7a70aefdcbe",
}
HUMAN_AUTHORITY_EVIDENCE = (
    Path("/home/lizening/research-notes/agent-logs/2026-10-26T231851Z__ASTRA__preworker-restart-review__cdec2e72/HUMAN_AUTHORITY_EVIDENCE.json"),
    "b990191410ddb53bce4477b76a37273f325473b4b2fa97aabf06ca81e4bba0e8",
)
ENGINEERING_ACCEPTANCE = (
    Path("/home/lizening/research-notes/agent-logs/2026-10-27T000517Z__SOL__si-s01-framework-default-amendment__f1e0d56_bf6d2eb7/ACTUAL_ENGINEERING_INDEPENDENT_ACCEPTANCE.json"),
    "dfa1f3e89ff1a654a0329109d960b2775dc99841bb98a2c6dc4c7e4e6545cef9",
)
PRE_FLIGHT_RECEIPT = Path("/tmp/si_s01_source_uid-2000_run-f96b86f3391940eaa9d75040c444a8e4_oxwwsyg4/control/source_preflight_receipt.json")


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(4 * 1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


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
    return subprocess.run(["git", "-C", str(root), *args], check=True, capture_output=True, text=True).stdout.strip()


def main() -> int:
    if os.geteuid() != 2000 or not OWN.is_dir() or OWN.stat().st_uid != 2000 or (OWN.stat().st_mode & 0o777) != 0o700:
        raise RuntimeError("execution UID or private live evidence directory mismatch")
    pinned_hashes = {}
    for name, expected in PINNED.items():
        actual = sha((TASK / name).read_bytes())
        pinned_hashes[name] = actual
        if actual != expected:
            raise RuntimeError(f"pinned release hash mismatch: {name}")

    handoff = json.loads((TASK / "SOURCE_EXECUTION_HANDOFF.json").read_text())
    clearance = json.loads((TASK / "SOURCE_LAUNCH_CLEARANCE_V2.json").read_text())
    authorization = json.loads((TASK / "ROOT_SOURCE_AUTHORIZATION_V2.json").read_text())
    proposal = json.loads((TASK / "SOURCE_PRODUCTION_PROPOSAL.json").read_text())
    exact_commands = json.loads((TASK / "SOURCE_EXACT_COMMANDS.json").read_text())
    preflight_review = json.loads((TASK / "SOURCE_PREFLIGHT_INDEPENDENT_VERIFICATION.json").read_text())
    preflight_execution = json.loads((TASK / "SOURCE_PREFLIGHT_EXECUTION_V2.json").read_text())
    rendering = json.loads((TASK / "CLEARANCE_RENDERING_VERIFICATION.json").read_text())
    authority_binding = json.loads((TASK / "HUMAN_TASK_AUTHORITY_BINDING.json").read_text())

    argv = handoff["allowed_live_argv"]
    env = handoff["environment"]
    cwd = Path(handoff["cwd"])
    clearance_sha = pinned_hashes["SOURCE_LAUNCH_CLEARANCE_V2.json"]
    authorization_sha = pinned_hashes["ROOT_SOURCE_AUTHORIZATION_V2.json"]
    env_sha = sha(canonical(env))
    argv_sha = sha(canonical(argv))

    if handoff["status"] != "RELEASED_ONE_FORMAL_SOURCE_ONLY_EXECUTION":
        raise RuntimeError("source execution handoff is not released")
    if clearance["status"] != "CLEARED_ONE_SOURCE_ONLY_LAUNCH" or clearance["maximum_launches"] != 1 or handoff["maximum_source_launches"] != 1:
        raise RuntimeError("single-use live clearance status/cap mismatch")
    if len(argv) != 14 or argv_sha != handoff["allowed_live_argv_sha256"]:
        raise RuntimeError("exact live argv digest mismatch")
    clearance_template = clearance["live_argv"]
    if len(clearance_template) != len(argv) or clearance_template[:-1] != argv[:-1] or clearance_template[-1] != "@CLEARANCE_SHA256@" or argv[-1] != clearance_sha:
        raise RuntimeError("clearance self-reference does not expand to the exact handoff argv")
    if (rendering.get("number_of_slots") != 1 or rendering.get("placeholder") != "@CLEARANCE_SHA256@"
            or rendering.get("replacement") != clearance_sha or rendering.get("rendered_equals_exact_handoff") is not True
            or rendering.get("live_argv_sha256") != argv_sha):
        raise RuntimeError("pinned production clearance-rendering proof mismatch")
    if argv != exact_commands["live_base_argv"] and any(x not in argv for x in exact_commands["live_base_argv"]):
        raise RuntimeError("handoff argv does not contain the released source command")
    if argv[argv.index("--authorization-sha256") + 1] != authorization_sha:
        raise RuntimeError("authorization SHA in argv mismatch")
    if argv[argv.index("--clearance-sha256") + 1] != clearance_sha:
        raise RuntimeError("clearance SHA in argv mismatch")
    if env_sha != clearance["binding"]["environment_sha256"] or env_sha != exact_commands["environment_sha256"]:
        raise RuntimeError("exact environment hash mismatch")
    if env != exact_commands["environment"] or len(env) != 13:
        raise RuntimeError("environment differs from reviewed 13-key mapping")
    if handoff["inherit_environment"] is not False or handoff["shell"] is not False or exact_commands["inherit_environment"] is not False:
        raise RuntimeError("launcher must use exact explicit environment and shell=false")
    if "--live" not in argv or "--preflight-only" in argv or "--worker" in argv:
        raise RuntimeError("argv is not exactly source-live mode")
    if handoff["source_sha"] != clearance["binding"]["source_sha"] or handoff["run_id"] != clearance["binding"]["run_id"]:
        raise RuntimeError("source/run identity mismatch")
    if handoff["source_sha"] != "f1e0d56a1be2a65876bbec5b8950fb76cda3eace" or handoff["run_id"] != "f96b86f3391940eaa9d75040c444a8e4":
        raise RuntimeError("unexpected frozen source or source run identity")
    if (authority_binding.get("bound_source_run_id") != handoff["run_id"]
            or authority_binding.get("no_new_human_approval_claim") is not True
            or not str(authority_binding.get("source_scope", "")).startswith("ONLY frozen96TRAIN/sourceP0/seed42/S5/H50/4h")):
        raise RuntimeError("human authority binding scope does not match this source release")
    human_path, human_sha = HUMAN_AUTHORITY_EVIDENCE
    human_raw = human_path.read_bytes()
    if sha(human_raw) != human_sha or authority_binding["original_human_message_evidence"] != {"path": str(human_path), "sha256": human_sha}:
        raise RuntimeError("original human authority evidence binding mismatch")
    human_json = json.loads(human_raw)
    quote_text = " ".join(str(q.get("text", q.get("exact_excerpt", ""))) for q in human_json.get("quotes", []))
    if "行，你来持续进行这个任务，直到开始实验" not in quote_text or "恢复后你继续核验并推进实验" not in quote_text:
        raise RuntimeError("original human task delegation quotes were not found")
    if clearance["binding"]["authorization_sha256"] != authorization_sha or clearance["binding"]["proposal_sha256"] != pinned_hashes["SOURCE_PRODUCTION_PROPOSAL.json"]:
        raise RuntimeError("clearance authorization/proposal binding mismatch")
    if clearance["binding"]["ceilings"] != handoff["ceilings"] or clearance["binding"]["evidence_class"] != "live_source_only":
        raise RuntimeError("live source evidence class or budget binding mismatch")
    if handoff["teacher_recovery_training_evaluation_heldout"] != "NOT_AUTHORIZED":
        raise RuntimeError("handoff unexpectedly authorizes out-of-scope activity")
    if clearance["binding"]["plan_sha256"] != preflight_execution["binding"]["plan_sha256"]:
        raise RuntimeError("clearance/preflight plan binding mismatch")
    if preflight_review.get("all8runtime_science_counters_zero") is not True or preflight_review.get("all96input_and_plan_bindings_validated_by_real_production_preflight") is not True:
        raise RuntimeError("independent preflight review did not attest required bindings")
    if preflight_execution.get("authentic_returncode") != 0:
        raise RuntimeError("independent execution record does not bind authentic preflight rc0")
    if preflight_execution.get("authentic_returncode") != 0 or preflight_execution.get("preflight_receipt_sha256") != sha(PRE_FLIGHT_RECEIPT.read_bytes()):
        raise RuntimeError("authentic preflight execution receipt mismatch")
    if proposal.get("schema") is None or authorization.get("source_sha") != handoff["source_sha"]:
        raise RuntimeError("proposal or authorization source binding missing")

    # The actual engineering acceptance is a separately pinned, immutable prerequisite.
    engineering_path, engineering_sha = ENGINEERING_ACCEPTANCE
    if sha(engineering_path.read_bytes()) != engineering_sha:
        raise RuntimeError("independent engineering acceptance hash mismatch")

    not_before = dt.datetime.fromisoformat(clearance["not_before_utc"].replace("Z", "+00:00"))
    expiry = dt.datetime.fromisoformat(clearance["expires_utc"].replace("Z", "+00:00"))
    now = dt.datetime.now(dt.timezone.utc)
    if not (not_before <= now < expiry):
        raise RuntimeError("live clearance outside validity window")

    repo = Path(handoff["cwd"])
    head = git(repo, "rev-parse", "HEAD")
    branch = git(repo, "branch", "--show-current")
    dirty = git(repo, "status", "--porcelain=v1")
    remote_line = subprocess.run(["git", "-C", str(repo), "ls-remote", "origin", "refs/heads/" + branch], check=True, capture_output=True, text=True).stdout.strip()
    remote_sha = remote_line.split("\t", 1)[0] if remote_line else ""
    if head != handoff["source_sha"] or remote_sha != head or dirty:
        raise RuntimeError(f"checkout drift: head={head}, remote={remote_sha}, dirty={bool(dirty)}")

    out = Path(handoff["storage"]["output"])
    parent = Path(handoff["storage"]["private_parent"])
    if out.exists():
        raise RuntimeError("scientific output path already exists")
    if not parent.is_dir() or parent.stat().st_uid != 2000 or (parent.stat().st_mode & 0o777) != 0o700:
        raise RuntimeError("private output parent ownership/mode mismatch")
    if shutil.disk_usage(parent).free < 160 * 1024**3:
        raise RuntimeError("less than 160 GiB free on authorized output filesystem")
    preflight = Path(clearance["preflight"]["path"])
    if not preflight.is_file() or sha(preflight.read_bytes()) != clearance["preflight"]["sha256"]:
        raise RuntimeError("preflight receipt changed after independent review")
    if ROOT_RECORD.joinpath("FILE_HASHES.sha256").is_file():
        for line in ROOT_RECORD.joinpath("FILE_HASHES.sha256").read_text().splitlines():
            digest, rel = line.split(None, 1)
            rel = rel.strip()
            if sha((ROOT_RECORD / rel).read_bytes()) != digest:
                raise RuntimeError(f"preserved preflight evidence changed: {rel}")

    # Detect only the exact source CLI process; do not probe CUDA/NVML/GPU state.
    script = argv[2]
    active = []
    for proc in Path("/proc").iterdir():
        if not proc.name.isdigit():
            continue
        try:
            args = [part.decode(errors="replace") for part in (proc / "cmdline").read_bytes().split(b"\0") if part]
        except OSError:
            continue
        if script in args and ("--live" in args or "--preflight-only" in args):
            active.append(proc.name)
    if active:
        raise RuntimeError(f"same source CLI already active: {active}")

    # Preserve exact release records as byte copies in the separate live evidence subdir.
    copy_names = list(PINNED)
    for name in copy_names:
        source_bytes = (TASK / name).read_bytes()
        target = OWN / name
        if target.exists():
            if target.read_bytes() != source_bytes:
                raise RuntimeError(f"existing live evidence copy differs: {name}")
        else:
            with target.open("xb") as stream:
                stream.write(source_bytes); stream.flush(); os.fsync(stream.fileno())
    for name, source_bytes in (("ACTUAL_ENGINEERING_INDEPENDENT_ACCEPTANCE.json", engineering_path.read_bytes()),
                               ("HUMAN_AUTHORITY_EVIDENCE.json", human_raw)):
        target = OWN / name
        if target.exists():
            if target.read_bytes() != source_bytes:
                raise RuntimeError(f"existing live evidence copy differs: {name}")
        else:
            with target.open("xb") as stream:
                stream.write(source_bytes); stream.flush(); os.fsync(stream.fileno())

    prelaunch = {
        "checked_utc": utcnow(),
        "run_id": handoff["run_id"],
        "source_sha": head,
        "source_branch": branch,
        "origin_branch_sha": remote_sha,
        "worktree_clean": True,
        "handoff_sha256": PINNED["SOURCE_EXECUTION_HANDOFF.json"],
        "clearance_sha256": clearance_sha,
        "authorization_sha256": authorization_sha,
        "preflight_verification_sha256": PINNED["SOURCE_PREFLIGHT_INDEPENDENT_VERIFICATION.json"],
        "clearance_rendering_proof_sha256": PINNED["CLEARANCE_RENDERING_VERIFICATION.json"],
        "human_authority_binding_sha256": PINNED["HUMAN_TASK_AUTHORITY_BINDING.json"],
        "original_human_authority_evidence_sha256": human_sha,
        "preflight_receipt_sha256": clearance["preflight"]["sha256"],
        "argv_sha256_canonical": argv_sha,
        "environment_sha256_canonical": env_sha,
        "environment_key_count": len(env),
        "inherit_environment": False,
        "shell": False,
        "clearance_within_validity_window": True,
        "output_absent": True,
        "private_parent_uid_mode": {"uid": parent.stat().st_uid, "mode": oct(parent.stat().st_mode & 0o777)},
        "free_bytes_before_launch": shutil.disk_usage(parent).free,
        "source_cli_process_absent": True,
        "preflight_original_hash_manifest_verified": True,
        "launcher_script_sha256": sha_file(Path(__file__).resolve()),
        "no_cuda_nvml_probe": True,
        "mode": "one_formal_source_only_execution",
        "user_authority_preexisting_and_bound": True,
        "science_caps": handoff["ceilings"],
    }
    durable_json(OWN / "LIVE_PRELAUNCH_CHECKS.json", prelaunch)

    consumed = {
        "consumed_utc": utcnow(),
        "clearance_id": clearance["clearance_id"],
        "clearance_sha256": clearance_sha,
        "run_id": handoff["run_id"],
        "source_sha": handoff["source_sha"],
        "maximum_launches": 1,
        "argv": argv,
        "argv_sha256_canonical": argv_sha,
        "cwd": str(cwd),
        "environment": env,
        "environment_sha256_canonical": env_sha,
        "inherit_environment": False,
        "shell": False,
        "state": "CONSUMED_BEFORE_CHILD_START",
        "automatic_retry": False,
    }
    durable_json(OWN / "LIVE_LAUNCH_CONSUMED.json", consumed)

    stdout_path = OWN / "live.stdout.bin"
    stderr_path = OWN / "live.stderr.bin"
    started = utcnow()
    monotonic_started = time.monotonic()
    with stdout_path.open("xb") as stdout, stderr_path.open("xb") as stderr:
        child = subprocess.Popen(argv, cwd=str(cwd), env=dict(env), stdin=subprocess.DEVNULL,
                                 stdout=stdout, stderr=stderr, shell=False, close_fds=True)
        durable_json(OWN / "LIVE_CHILD_START.json", {
            "started_utc": started,
            "pid": child.pid,
            "argv": argv,
            "argv_sha256_canonical": argv_sha,
            "cwd": str(cwd),
            "environment_sha256_canonical": env_sha,
            "environment_key_count": len(env),
            "inherit_environment": False,
            "shell": False,
            "run_id": handoff["run_id"],
        })
        returncode = child.wait()
        stdout.flush(); os.fsync(stdout.fileno())
        stderr.flush(); os.fsync(stderr.fileno())
    elapsed = time.monotonic() - monotonic_started
    ended = utcnow()

    files = []
    if out.is_dir():
        for path in sorted(out.rglob("*")):
            if path.is_file():
                files.append({"relative_path": str(path.relative_to(out)), "bytes": path.stat().st_size, "sha256": sha_file(path)})
    durable_json(OWN / "LIVE_SUBPROCESS_RECEIPT.json", {
        "started_utc": started,
        "ended_utc": ended,
        "child_pid": child.pid,
        "returncode": returncode,
        "elapsed_seconds_monotonic": elapsed,
        "argv_sha256_canonical": argv_sha,
        "environment_sha256_canonical": env_sha,
        "stdout_bytes": stdout_path.stat().st_size,
        "stdout_sha256": sha(stdout_path.read_bytes()),
        "stderr_bytes": stderr_path.stat().st_size,
        "stderr_sha256": sha(stderr_path.read_bytes()),
        "output_path": str(out),
        "output_path_exists_after": out.exists(),
        "output_files_at_exit": files,
        "automatic_retry": False,
    })
    print(json.dumps({"run_id": handoff["run_id"], "supervisor_pid": child.pid,
                      "returncode": returncode, "started_utc": started,
                      "own_live_record": str(OWN / "LIVE_CHILD_START.json")}, sort_keys=True))
    return 0 if returncode == 0 else returncode


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        abort_path = OWN / "LIVE_PRELAUNCH_ABORT.json"
        suffix = 2
        while abort_path.exists():
            abort_path = OWN / f"LIVE_PRELAUNCH_ABORT_{suffix:02d}.json"
            suffix += 1
        try:
            durable_json(abort_path, {
                "recorded_utc": utcnow(),
                "exception_type": type(exc).__name__,
                "message": str(exc),
                "launch_consumed_marker_exists": (OWN / "LIVE_LAUNCH_CONSUMED.json").exists(),
                "child_started_record_exists": (OWN / "LIVE_CHILD_START.json").exists(),
            })
        except Exception:
            pass
        print(f"LIVE_PRELAUNCH_ABORT: {type(exc).__name__}: {exc}", file=sys.stderr)
        raise
