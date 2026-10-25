#!/usr/bin/env python3
"""Read-only stdlib verification of SFT protocol canonical manifest hashes."""

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path


ROOT = Path("/home/lizening/wt-codex-r18c2")
OUT = Path(__file__).with_name("protocol_canonical_binding_check.json")


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_digest(value: object, *, ensure_ascii: bool) -> str:
    payload = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=ensure_ascii,
    ).encode("utf-8")
    return digest(payload)


def main() -> int:
    protocol_path = ROOT / "configs/sft/sft_training_protocol.json"
    protocol_bytes = protocol_path.read_bytes()
    protocol = json.loads(protocol_bytes)
    paths = {
        "split": ROOT / "configs/sft/sft_task_splits.json",
        "exclusion": ROOT / "configs/sft/sft_task_exclusions.json",
    }
    declared = {
        "split": protocol["dataset"]["split_manifest_sha256"],
        "exclusion": protocol["dataset"]["exclusion_manifest_sha256"],
    }
    results = {}
    for key, path in paths.items():
        raw = path.read_bytes()
        obj = json.loads(raw)
        ascii_hash = canonical_digest(obj, ensure_ascii=True)
        unicode_hash = canonical_digest(obj, ensure_ascii=False)
        results[key] = {
            "path": str(path),
            "raw_sha256": digest(raw),
            "canonical_sha256_ensure_ascii_true": ascii_hash,
            "canonical_sha256_ensure_ascii_false": unicode_hash,
            "protocol_declared_canonical_sha256": declared[key],
            "both_canonical_forms_match_protocol": (
                ascii_hash == declared[key] and unicode_hash == declared[key]
            ),
            "canonical_forms_equal": ascii_hash == unicode_hash,
        }

    code_paths = {
        "canonical_hash_definition": ROOT / "src/sft/protocol.py",
        "asset_builder": ROOT / "scripts/build_sft_protocol_assets.py",
    }
    code = {key: {"path": str(path), "raw_sha256": digest(path.read_bytes())}
            for key, path in code_paths.items()}
    result = {
        "audit_kind": "read-only stdlib canonical-JSON binding verification; no project imports or execution",
        "observed_utc": datetime.now(timezone.utc).isoformat(),
        "protocol": {
            "path": str(protocol_path),
            "raw_sha256": digest(protocol_bytes),
            "canonicalization": "json.dumps(value, sort_keys=True, separators=(\",\", \":\"), ensure_ascii=True).encode(utf-8), then SHA-256",
        },
        "manifests": results,
        "relevant_code": code,
        "overall_match": all(item["both_canonical_forms_match_protocol"] for item in results.values()),
        "interpretation": "Raw file hashes differ from protocol declarations because the files are pretty-printed; both canonical serializations produce the protocol-declared values. The saved-record mismatch claim based on comparing raw file SHA to canonical object SHA is withdrawn.",
        "limits": [
            "This verifies current saved objects against the saved protocol's canonical digest fields.",
            "It does not itself prove which file bytes a historical training process loaded; historical runtime and launch evidence must be assessed separately.",
            "No project analyzer/validator, model, tokenizer, environment, training, replay, or tests were run.",
        ],
        "scientific_execution": False,
    }
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["overall_match"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
