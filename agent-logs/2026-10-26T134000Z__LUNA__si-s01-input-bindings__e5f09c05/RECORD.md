# SI-S01 read-only proposal input binding record

- Status: `READ_ONLY_PREPARATION / NOT_RELEASE / NOT_RUNTIME_READY`.
- Start: 2026-10-26T13:40:20Z (own task directory creation). Finish: 2026-10-26T13:47:22Z.
- Unique Luna-owned task directory: `/home/lizening/research-notes/agent-logs/2026-10-26T134000Z__LUNA__si-s01-input-bindings__e5f09c05`.
- Governing scope: the three root documents and adopted protocol listed in `PROPOSAL_INPUT_BINDINGS.json`; no launch release.
- Current development checkout observed: clean at candidate `e5f09c05824cb61cb35ccbbf4e189b04e8829cea`, but the candidate is not frozen/independently reviewed and is not accepted as execution source.

## Frozen input results

1. All 12 cached snapshot files at revision `b968826d9c46dd6066d109eabc6255188de91218` were fully hashed in the current container and match the frozen identity-manifest values. No files were copied or loaded as a model/tokenizer.
2. The P0 adapter directory was hashed using the original `directory_sha256` byte algorithm reimplemented with Python standard library only: 11 files, 365,138,109 bytes, SHA-256 `6e403d85b150a74dfcc176f1f180ce4baf6fdacd922d2f96b3ceef0a21100f11`. This matches the frozen code constant and historic execution manifest; no adapter contents were exported.
3. Historical R19 protocol/config/logic and code inputs plus the actual old supervisor/runtime receipts are path/hash bound in the machine-readable inventory. The original root is `/home/lizening/alfworld_data`; `json_2.1.1/train` is the YAML's nested dataset path, not `ALFWORLD_DATA`.
4. The previous bounded first-source nine-slice event binding is referenced by exact path/SHA. Whole trajectory and journal were not rescanned; the certified whole trajectory digest remains reference-only.
5. Historical runtime package versions are recorded from the old manifest only. Current package origins, host runtime, host cache visibility, UID-to-host mapping, GPU UUID/process ownership, and new raw argv/environment remain unobserved or not created.

## Constraints and stop status

Future scope, if separately released, remains one historical source identity/index 0, one P0 load/tokenizer, one explicit one-byte probe, one generation (<=16 output, <=8192 input), one environment construction, reset 30000 plus the six saved commands (7 operations total), one close, and 600 seconds allocated including cleanup. Pool seed 42 is a new setting and does not reconstruct the unrecorded historical internal RNG. Joined reset→prompt→prepared/sent→generation/parser/map→saved-first-command→six-transition comparison is mandatory; any discrepancy stops with no retry. Historical science totals remain 5,142 generations / 7,949 environment operations; future engineering cost is separate.

Root checkpoint 4 records the forwarded SSH agent socket as absent (`ENOENT`); this task did not recheck it and made no SSH attempt. Old authorizations are consumed. No new gate, authorization, executable argv, output path, or launch was created.

No model/tokenizer/CUDA/environment, project validator/test, preflight, supervisor, SSH, or scientific call occurred. No source checkout, prior record, shared index/inventory, or remote provenance state was changed. No stage/commit/push.
