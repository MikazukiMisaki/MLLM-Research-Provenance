#!/usr/bin/env python3
"""Mechanically hash and inventory only this Luna-owned evidence directory."""
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent
HASH_FILE = ROOT / "FILE_HASHES.sha256"
INVENTORY = ROOT / "LOCAL_ONLY_FILES.md"

def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()

files = sorted(p for p in ROOT.rglob("*") if p.is_file() and p not in (HASH_FILE, INVENTORY))
rows = [(p.relative_to(ROOT).as_posix(), p.stat().st_size, sha(p)) for p in files]
inventory = [
    "# SI-E2 Luna local-only file inventory",
    "",
    "This directory has not been staged, committed, or pushed. All listed artifacts remain local pending root review. The inventory contains paths, byte sizes, SHA256s, and coarse file class only; it does not print prompts, task bodies, trajectory action text, model weights, token IDs, or raw payload content.",
    "",
    "`FILE_HASHES.sha256` covers every task artifact except itself. `LOCAL_ONLY_FILES.md` is excluded from its own rows to avoid self-reference but is covered by `FILE_HASHES.sha256`.",
    "",
    "| Path | Bytes | SHA256 | Class / note |",
    "|---|---:|---|---|",
]
for name, size, digest in rows:
    if name.startswith("raw/"):
        note = "raw captured stdout/stderr; local host paths/status only"
    elif name.endswith(".receipt.json") or name.endswith("_receipts.json"):
        note = "actual command receipt with argv/cwd/timing/return code/hash"
    elif name.endswith(".py"):
        note = "local read-only capture/inspection helper"
    elif name.endswith(".json"):
        note = "bound metadata/evidence; may contain machine-local paths"
    elif name.endswith(".md"):
        note = "local readiness/record/clarification"
    else:
        note = "task evidence"
    inventory.append(f"| `{name}` | {size} | `{digest}` | {note} |")
INVENTORY.write_text("\n".join(inventory) + "\n")

files = sorted(p for p in ROOT.rglob("*") if p.is_file() and p != HASH_FILE)
HASH_FILE.write_text("".join(f"{sha(p)}  {p.relative_to(ROOT).as_posix()}\n" for p in files))
print(f"inventory_rows={len(rows)} hash_entries={len(files)}")
