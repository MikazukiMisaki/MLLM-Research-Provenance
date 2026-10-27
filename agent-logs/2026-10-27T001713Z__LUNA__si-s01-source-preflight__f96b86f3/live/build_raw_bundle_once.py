#!/usr/bin/env python3
"""Build and round-trip a deterministic archive of the completed source run evidence."""
from __future__ import annotations

import datetime as dt
import gzip
import hashlib
import json
import os
from pathlib import Path
import shutil
import stat
import tarfile


LIVE = Path("/home/lizening/research-notes/agent-logs/2026-10-27T001713Z__LUNA__si-s01-source-preflight__f96b86f3/live")
OWN = LIVE
TASK = Path("/home/lizening/research-notes/agent-logs/2026-10-27T001612Z__SOL__si-s01-A96-source-authority__f1e0d56_f96b86f3")
HUMAN_DIR = Path("/home/lizening/research-notes/agent-logs/2026-10-26T231851Z__ASTRA__preworker-restart-review__cdec2e72")
ENG_DIR = Path("/home/lizening/research-notes/agent-logs/2026-10-27T000517Z__SOL__si-s01-framework-default-amendment__f1e0d56_bf6d2eb7")
PARENT = Path("/tmp/si_s01_source_uid-2000_run-f96b86f3391940eaa9d75040c444a8e4_oxwwsyg4")
PUBLICATION = PARENT / "publication" / "luna_source_bundle_f96b86f3"
ARCHIVE = PUBLICATION / "si_s01_source_f96b86f3_evidence.tar.gz"
ROUNDTRIP = PUBLICATION / "roundtrip"
MEMBERS_JSON = PUBLICATION / "RAW_ARCHIVE_MEMBERS.json"
VERIFY_JSON = PUBLICATION / "RAW_ARCHIVE_VERIFICATION.json"
PREFLIGHT_RECEIPT = PARENT / "control" / "source_preflight_receipt.json"
SOURCE_RUN_ID = "f96b86f3391940eaa9d75040c444a8e4"
SUPERVISOR_PID = 882767
WORKER_PID = 882823
PINNED_CONTROL_SHA256 = {
    "/home/lizening/research-notes/agent-logs/2026-10-27T001612Z__SOL__si-s01-A96-source-authority__f1e0d56_f96b86f3/SOURCE_EXECUTION_HANDOFF.json": "d2ee23838417dd37e8c4743bfc9b3c39f07c38c1a3fa7182f849fe6ea5538e26",
    "/home/lizening/research-notes/agent-logs/2026-10-27T001612Z__SOL__si-s01-A96-source-authority__f1e0d56_f96b86f3/SOURCE_LAUNCH_CLEARANCE_V2.json": "3defb7052665b5ad365093880912f4be8c667d0d3c65979e15373afe014e7524",
    "/home/lizening/research-notes/agent-logs/2026-10-27T001612Z__SOL__si-s01-A96-source-authority__f1e0d56_f96b86f3/ROOT_SOURCE_AUTHORIZATION_V2.json": "cf25576d5bf019a925cb1cd1d878046921162f136de173dad870ce8365e40a05",
    "/home/lizening/research-notes/agent-logs/2026-10-27T001612Z__SOL__si-s01-A96-source-authority__f1e0d56_f96b86f3/SOURCE_PRODUCTION_PROPOSAL.json": "227eef584d8d8bd991e4e783eebb1203f249f9e64835282ba5b4e69328e02580",
    "/home/lizening/research-notes/agent-logs/2026-10-27T001612Z__SOL__si-s01-A96-source-authority__f1e0d56_f96b86f3/SOURCE_EXACT_COMMANDS.json": "149953aab65001c79f5838c03c1c401867459ccf5976854c58e854cf2133e19a",
    "/home/lizening/research-notes/agent-logs/2026-10-27T001612Z__SOL__si-s01-A96-source-authority__f1e0d56_f96b86f3/SOURCE_PREFLIGHT_ONLY_RELEASE.json": "56fce9fccf33e33f624f97e156bebcf1ad7c32a7ac6eba6c26a13f4507543e4a",
    "/home/lizening/research-notes/agent-logs/2026-10-27T001612Z__SOL__si-s01-A96-source-authority__f1e0d56_f96b86f3/SOURCE_CONCRETE_RELEASE_REVIEW.json": "93acff00d94a5dbf632c4460ab88aceb70dc51fe1a25a820aed60830f3588b82",
    "/home/lizening/research-notes/agent-logs/2026-10-27T001612Z__SOL__si-s01-A96-source-authority__f1e0d56_f96b86f3/SOURCE_PREFLIGHT_INDEPENDENT_VERIFICATION.json": "6a305a810c54f3cb5757222143f0564885c418287b4dad249b51ba8a09a89ad1",
    "/home/lizening/research-notes/agent-logs/2026-10-27T001612Z__SOL__si-s01-A96-source-authority__f1e0d56_f96b86f3/SOURCE_PREFLIGHT_EXECUTION_V2.json": "6251263dbdb80298e3c8b896de5f316455d8a25a550c37929c5e4383813aff87",
    "/home/lizening/research-notes/agent-logs/2026-10-27T001612Z__SOL__si-s01-A96-source-authority__f1e0d56_f96b86f3/CLEARANCE_RENDERING_VERIFICATION.json": "5df732a9f562900f478325168f8f17f116a234b03215caf9c11c6e0309e64c59",
    "/home/lizening/research-notes/agent-logs/2026-10-27T001612Z__SOL__si-s01-A96-source-authority__f1e0d56_f96b86f3/HUMAN_TASK_AUTHORITY_BINDING.json": "b924dafe49d645d0ab80fbf7c205c77688bbe6df7f5a8f795c40f7a70aefdcbe",
    "/home/lizening/research-notes/agent-logs/2026-10-26T231851Z__ASTRA__preworker-restart-review__cdec2e72/HUMAN_AUTHORITY_EVIDENCE.json": "b990191410ddb53bce4477b76a37273f325473b4b2fa97aabf06ca81e4bba0e8",
    "/home/lizening/research-notes/agent-logs/2026-10-27T000517Z__SOL__si-s01-framework-default-amendment__f1e0d56_bf6d2eb7/ACTUAL_ENGINEERING_INDEPENDENT_ACCEPTANCE.json": "dfa1f3e89ff1a654a0329109d960b2775dc99841bb98a2c6dc4c7e4e6545cef9",
    "/tmp/si_s01_source_uid-2000_run-f96b86f3391940eaa9d75040c444a8e4_oxwwsyg4/control/source_preflight_receipt.json": "c35dd9bda121aab54901ae5f9057a568330e9e11487f2238ae4c392279853c69",
    "/home/lizening/research-notes/agent-logs/2026-10-27T001713Z__LUNA__si-s01-source-preflight__f96b86f3/SOURCE_PREFLIGHT_RESULT.json": "cf776c4d4142314fe3a5bed5582bd72d795ca6378840f7df2380c4051608780f",
    "/home/lizening/research-notes/agent-logs/2026-10-27T001713Z__LUNA__si-s01-source-preflight__f96b86f3/SOURCE_PREFLIGHT_SUBPROCESS_RECEIPT.json": "c5f8fef69f0cfd84bf549b7fdef3b5829a4b3764ecbde80597d6ffb12c9d21ee",
    "/home/lizening/research-notes/agent-logs/2026-10-27T001713Z__LUNA__si-s01-source-preflight__f96b86f3/FILE_HASHES.sha256": "4c9ca891d1da4211c3485b1913b37f1f1aaac9228db48f06c575ce12ce6e51dc",
}


def sha_stream(stream) -> str:
    digest = hashlib.sha256()
    for chunk in iter(lambda: stream.read(4 * 1024 * 1024), b""):
        digest.update(chunk)
    return digest.hexdigest()


def sha_file(path: Path) -> str:
    with path.open("rb") as stream:
        return sha_stream(stream)


def utcnow() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat().replace("+00:00", "Z")


def write_json_exclusive(path: Path, data: object) -> None:
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, "wb") as stream:
        stream.write((json.dumps(data, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode())
        stream.flush(); os.fsync(stream.fileno())
    dfd = os.open(path.parent, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0))
    try: os.fsync(dfd)
    finally: os.close(dfd)


def main() -> int:
    if not PUBLICATION.is_dir() or PUBLICATION.stat().st_uid != 2000 or (PUBLICATION.stat().st_mode & 0o777) != 0o700:
        raise RuntimeError("private Luna publication directory missing or permissions differ")
    if ARCHIVE.exists() or ROUNDTRIP.exists() or MEMBERS_JSON.exists() or VERIFY_JSON.exists():
        raise RuntimeError("bundle target already exists; refusing overwrite/rebuild")
    if pathlib_exists_proc(SUPERVISOR_PID) or pathlib_exists_proc(WORKER_PID):
        raise RuntimeError("writers are not quiescent")

    handoff = json.loads((TASK / "SOURCE_EXECUTION_HANDOFF.json").read_text())
    output = Path(handoff["storage"]["output"])
    parent = Path(handoff["storage"]["private_parent"])
    if output != PARENT / "raw" or not output.is_dir():
        raise RuntimeError("actual output path missing or differs from handoff")

    live_receipt = json.loads((LIVE / "LIVE_SUBPROCESS_RECEIPT.json").read_text())
    if live_receipt.get("returncode") != 0 or live_receipt.get("output_path_exists_after") is not True:
        raise RuntimeError("authentic outer subprocess receipt is not completed rc0")
    supervisor = json.loads((output / "supervisor_exit.json").read_text())
    if supervisor.get("authentic_returncode") != 0 or supervisor.get("cleanup_established") is not True or supervisor.get("within_time_cap") is not True:
        raise RuntimeError("production supervisor exit/cleanup receipt did not pass")
    if supervisor.get("deadline_triggered") is not False or supervisor.get("reaping_error") is not None:
        raise RuntimeError("production supervisor deadline/reaping state is unresolved")

    # Exact file selection: all raw output members and the supervisor's launch claim,
    # plus only execution authorization/control/receipt records (never input payloads).
    sources: list[tuple[str, Path, str]] = []
    for entry in live_receipt["output_files_at_exit"]:
        rel = entry["relative_path"]
        source = output / rel
        if not source.is_file() or source.is_symlink():
            raise RuntimeError(f"raw output member missing or non-regular: {rel}")
        if source.stat().st_size != entry["bytes"] or sha_file(source) != entry["sha256"]:
            raise RuntimeError(f"raw output differs from authentic exit-time hash: {rel}")
        sources.append((f"run/raw/{rel}", source, "original-production-output"))

    claim = parent / "raw.launch_claim.json"
    if not claim.is_file() or claim.is_symlink():
        raise RuntimeError("original launch claim absent or non-regular")
    if sha_file(claim) != "2b835c5f0dee1d30b170ed70a7a4144a5d711a13570fd006dbbc4a5520e3254e":
        raise RuntimeError("original live launch claim SHA mismatch")
    sources.append(("run/raw.launch_claim.json", claim, "original-supervisor-claim"))

    control_files = [
        ("control/source_preflight_receipt.json", PREFLIGHT_RECEIPT),
        ("control/source_execution_handoff.json", TASK / "SOURCE_EXECUTION_HANDOFF.json"),
        ("control/source_launch_clearance.json", TASK / "SOURCE_LAUNCH_CLEARANCE_V2.json"),
        ("control/root_source_authorization_v2.json", TASK / "ROOT_SOURCE_AUTHORIZATION_V2.json"),
        ("control/source_production_proposal.json", TASK / "SOURCE_PRODUCTION_PROPOSAL.json"),
        ("control/source_exact_commands.json", TASK / "SOURCE_EXACT_COMMANDS.json"),
        ("control/source_preflight_release.json", TASK / "SOURCE_PREFLIGHT_ONLY_RELEASE.json"),
        ("control/source_concrete_release_review.json", TASK / "SOURCE_CONCRETE_RELEASE_REVIEW.json"),
        ("control/source_preflight_independent_verification.json", TASK / "SOURCE_PREFLIGHT_INDEPENDENT_VERIFICATION.json"),
        ("control/source_preflight_execution.json", TASK / "SOURCE_PREFLIGHT_EXECUTION_V2.json"),
        ("control/clearance_rendering_verification.json", TASK / "CLEARANCE_RENDERING_VERIFICATION.json"),
        ("control/human_task_authority_binding.json", TASK / "HUMAN_TASK_AUTHORITY_BINDING.json"),
        ("control/human_authority_evidence.json", HUMAN_DIR / "HUMAN_AUTHORITY_EVIDENCE.json"),
        ("control/engineering_independent_acceptance.json", ENG_DIR / "ACTUAL_ENGINEERING_INDEPENDENT_ACCEPTANCE.json"),
        ("control/luna_preflight_result.json", LIVE.parent / "SOURCE_PREFLIGHT_RESULT.json"),
        ("control/luna_preflight_subprocess_receipt.json", LIVE.parent / "SOURCE_PREFLIGHT_SUBPROCESS_RECEIPT.json"),
        ("control/luna_preflight_file_hashes.sha256", LIVE.parent / "FILE_HASHES.sha256"),
        ("control/luna_source_preflight_receipt_copy.json", LIVE.parent / "source_preflight_receipt.json"),
    ]
    for arcname, source in control_files:
        if not source.is_file() or source.is_symlink():
            raise RuntimeError(f"control record absent or non-regular: {source}")
        pinned = PINNED_CONTROL_SHA256.get(str(source))
        if pinned is not None and sha_file(source) != pinned:
            raise RuntimeError(f"pinned control file drifted: {source}")
        sources.append((f"run/{arcname}", source, "authorization-review-or-preflight-control"))

    launcher_files = [
        ("launcher/live_launch_consumed.json", LIVE / "LIVE_LAUNCH_CONSUMED.json"),
        ("launcher/live_prelaunch_checks.json", LIVE / "LIVE_PRELAUNCH_CHECKS.json"),
        ("launcher/live_child_start.json", LIVE / "LIVE_CHILD_START.json"),
        ("launcher/live_subprocess_receipt.json", LIVE / "LIVE_SUBPROCESS_RECEIPT.json"),
        ("launcher/live_stdout.bin", LIVE / "live.stdout.bin"),
        ("launcher/live_stderr.bin", LIVE / "live.stderr.bin"),
        ("launcher/launch_source_live_once.py", LIVE / "launch_source_live_once.py"),
        ("launcher/prelaunch_abort_1.json", LIVE / "LIVE_PRELAUNCH_ABORT.json"),
        ("launcher/prelaunch_abort_2.json", LIVE / "LIVE_PRELAUNCH_ABORT_02.json"),
        ("launcher/prelaunch_abort_3.json", LIVE / "LIVE_PRELAUNCH_ABORT_03.json"),
        ("launcher/monitor_incidents.md", LIVE / "LIVE_MONITOR_INCIDENTS.md"),
        ("launcher/preflight_wrapper_abort_1.json", LIVE.parent / "PRELAUNCH_ABORT.json"),
        ("launcher/preflight_wrapper_abort_2_summary.json", LIVE.parent / "PRELAUNCH_ABORT_02_SUMMARY.json"),
        ("launcher/preflight_wrapper_issues.md", LIVE.parent / "PRELAUNCH_CHECKER_ISSUES.md"),
    ]
    for arcname, source in launcher_files:
        if source.exists():
            if not source.is_file() or source.is_symlink():
                raise RuntimeError(f"launcher evidence is not a regular file: {source}")
            sources.append((f"run/{arcname}", source, "operator-launch-or-monitor-receipt"))

    # Verify no duplicate archive names and no payload paths outside explicit allowlists.
    names = [name for name, _, _ in sources]
    if len(names) != len(set(names)):
        raise RuntimeError("duplicate archive member path")
    forbidden = ("/model", "weights", "adapter", "cache", "alfworld_data", "json_2.1.1", "dataset")
    for name, source, _ in sources:
        if any(token in name.lower() for token in forbidden):
            raise RuntimeError(f"forbidden archive path: {name}")
        st = source.lstat()
        if not stat.S_ISREG(st.st_mode):
            raise RuntimeError(f"archive source is not a regular file: {source}")

    # The production report and ledger are from the same fully sealed run; this is only
    # a completion/cost snapshot, not an additional project validator or analysis.
    report = json.loads((output / "source_report.json").read_text())
    if report.get("normal_sources") != 96 or report.get("source_phase_sealed") is not True:
        raise RuntimeError("the authentic production report does not show all 96 source records sealed")
    ledger_counts = {"source_closed": 0, "run_closed": 0, "generation_returned": 0}
    ledger = output / "source_events.jsonl"
    line_count = 0
    sequence_contiguous = True
    last_sequence = -1
    with ledger.open("rb") as stream:
        for line in stream:
            event = json.loads(line)
            line_count += 1
            seq = event.get("sequence")
            sequence_contiguous = sequence_contiguous and seq == line_count - 1
            last_sequence = seq if isinstance(seq, int) else last_sequence
            if event.get("kind") == "source_closed": ledger_counts["source_closed"] += 1
            elif event.get("kind") == "run_closed": ledger_counts["run_closed"] += 1
            elif event.get("kind") == "runtime_evidence" and event.get("payload", {}).get("kind") == "generation_returned":
                ledger_counts["generation_returned"] += 1
    trajectory_rows = sum(1 for _ in (output / "source_trajectories.jsonl").open("rb"))
    if not sequence_contiguous or ledger_counts["source_closed"] != 96 or ledger_counts["run_closed"] != 1 or trajectory_rows != 96:
        raise RuntimeError("post-exit raw completion snapshot is not internally sealed")

    member_records = []
    for arcname, source, classification in sorted(sources):
        member_records.append({
            "archive_path": arcname,
            "original_path": str(source),
            "bytes": source.stat().st_size,
            "sha256_before": sha_file(source),
            "classification": classification,
        })
    inventory = {
        "schema": "luna.si_s01_lossless_raw_archive_members.v1",
        "created_utc": utcnow(),
        "run_id": SOURCE_RUN_ID,
        "source_sha": handoff["source_sha"],
        "archive_path": str(ARCHIVE),
        "archive_format": "ustar+gzip-mtime0",
        "tar_member_metadata": "normalized uid=0,gid=0,mtime=0,mode=0600; member file bytes preserved losslessly",
        "input_dataset_payload_included": False,
        "model_weights_adapters_or_cache_included": False,
        "members": member_records,
        "member_count": len(member_records),
    }
    write_json_exclusive(MEMBERS_JSON, inventory)

    # Deterministic tar/gzip stream. Archive members are explicit regular files only.
    with ARCHIVE.open("xb") as raw_archive:
        with gzip.GzipFile(filename="", mode="wb", compresslevel=6, fileobj=raw_archive, mtime=0) as gz:
            with tarfile.open(fileobj=gz, mode="w|", format=tarfile.USTAR_FORMAT) as tar:
                for row in member_records:
                    info = tarfile.TarInfo(row["archive_path"])
                    info.size = row["bytes"]
                    info.mtime = 0
                    info.uid = 0; info.gid = 0
                    info.uname = ""; info.gname = ""
                    info.mode = 0o600
                    info.type = tarfile.REGTYPE
                    with Path(row["original_path"]).open("rb") as source_stream:
                        tar.addfile(info, source_stream)
        raw_archive.flush(); os.fsync(raw_archive.fileno())

    # Round-trip every member to a separate private location and hash the reconstructed bytes.
    ROUNDTRIP.mkdir(mode=0o700, parents=False, exist_ok=False)
    expected_by_name = {row["archive_path"]: row for row in member_records}
    roundtrip_records = []
    with tarfile.open(ARCHIVE, mode="r:gz") as tar:
        found = set()
        for member in tar:
            if not member.isfile() or member.name not in expected_by_name or member.name in found:
                raise RuntimeError(f"unexpected archive member: {member.name}")
            found.add(member.name)
            row = expected_by_name[member.name]
            dest = ROUNDTRIP / member.name
            dest.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
            src = tar.extractfile(member)
            if src is None:
                raise RuntimeError(f"archive member unreadable: {member.name}")
            fd = os.open(dest, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
            digest = hashlib.sha256(); count = 0
            with os.fdopen(fd, "wb") as target:
                for chunk in iter(lambda: src.read(4 * 1024 * 1024), b""):
                    target.write(chunk); digest.update(chunk); count += len(chunk)
                target.flush(); os.fsync(target.fileno())
            expected = row["sha256_before"]
            if count != row["bytes"] or digest.hexdigest() != expected:
                raise RuntimeError(f"round-trip bytes differ: {member.name}")
            roundtrip_records.append({"archive_path": member.name, "bytes": count, "sha256": digest.hexdigest(), "match": True})
    if found != set(expected_by_name):
        raise RuntimeError("archive member set differs from explicit inventory")

    # Verify original inputs/output remained byte-identical after packaging.
    for row in member_records:
        if row["bytes"] != Path(row["original_path"]).stat().st_size or row["sha256_before"] != sha_file(Path(row["original_path"])):
            raise RuntimeError(f"original evidence changed during archive: {row['original_path']}")

    archive_sha = sha_file(ARCHIVE)
    parts = []
    if ARCHIVE.stat().st_size > 100 * 1024 * 1024:
        chunk_bytes = 32 * 1024 * 1024
        with ARCHIVE.open("rb") as src:
            index = 0
            while True:
                chunk = src.read(chunk_bytes)
                if not chunk: break
                part = PUBLICATION / f"si_s01_source_f96b86f3.part{index:03d}"
                with part.open("xb") as dest:
                    dest.write(chunk); dest.flush(); os.fsync(dest.fileno())
                parts.append({"path": str(part), "bytes": len(chunk), "sha256": sha_file(part)})
                index += 1
        reassembled = PUBLICATION / "si_s01_source_f96b86f3.reassembled.tar.gz"
        with reassembled.open("xb") as dest:
            for part in parts:
                with Path(part["path"]).open("rb") as src:
                    shutil.copyfileobj(src, dest, length=4 * 1024 * 1024)
            dest.flush(); os.fsync(dest.fileno())
        if sha_file(reassembled) != archive_sha:
            raise RuntimeError("numbered-part reassembly does not match whole archive SHA")

    verification = {
        "schema": "luna.si_s01_lossless_raw_archive_verification.v1",
        "verified_utc": utcnow(),
        "run_id": SOURCE_RUN_ID,
        "archive_path": str(ARCHIVE),
        "archive_bytes": ARCHIVE.stat().st_size,
        "archive_sha256": archive_sha,
        "members_manifest_path": str(MEMBERS_JSON),
        "members_manifest_sha256": sha_file(MEMBERS_JSON),
        "member_count": len(member_records),
        "roundtrip_path": str(ROUNDTRIP),
        "roundtrip_member_count": len(roundtrip_records),
        "all_member_bytes_match_original": all(r["match"] for r in roundtrip_records),
        "original_files_pre_post_hashes_equal": True,
        "parts": parts,
        "reassembled_archive_sha256": sha_file(PUBLICATION / "si_s01_source_f96b86f3.reassembled.tar.gz") if parts else None,
        "output_raw_bytes": sum(x["bytes"] for x in member_records if x["classification"] == "original-production-output"),
        "output_file_count": sum(1 for x in member_records if x["classification"] == "original-production-output"),
        "input_dataset_payload_included": False,
        "model_weights_adapters_or_cache_included": False,
        "completion_snapshot": {
            "source_closed": ledger_counts["source_closed"],
            "run_closed": ledger_counts["run_closed"],
            "trajectory_rows": trajectory_rows,
            "ledger_lines": line_count,
            "last_sequence": last_sequence,
            "sequence_contiguous": sequence_contiguous,
            "production_status": report["status"],
            "supervisor_returncode": supervisor["authentic_returncode"],
            "supervisor_cleanup_established": supervisor["cleanup_established"],
        },
        "roundtrip_members": roundtrip_records,
    }
    write_json_exclusive(VERIFY_JSON, verification)
    print(json.dumps({"archive": str(ARCHIVE), "archive_bytes": ARCHIVE.stat().st_size,
                      "archive_sha256": archive_sha, "member_count": len(member_records),
                      "roundtrip_verified": len(roundtrip_records), "output_file_count": verification["output_file_count"],
                      "output_raw_bytes": verification["output_raw_bytes"], "parts": parts,
                      "members_manifest": str(MEMBERS_JSON), "verification": str(VERIFY_JSON)}, sort_keys=True))
    return 0


def pathlib_exists_proc(pid: int) -> bool:
    return Path("/proc") .joinpath(str(pid)).exists()


if __name__ == "__main__":
    raise SystemExit(main())
