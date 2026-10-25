# SI-E2 revision 2 source-binding addendum

**Status:** proposal-only; root review pending; no engineering release or execution authorization.  
**Scientific source:** unchanged at `dfc00e49d1ef4d48453d2331507429f8a0c7bbc5`.

This addendum supersedes the earlier source-replay binding draft only. The earlier proposal, environment proposal, argv proposal, and `FIRST_SOURCE_REPLAY_BINDINGS.json` remain preserved byte-for-byte as historical drafts. The corrected data-root proposal is `SI_E2_PROPOSAL_REVISION_2.json`; its companion replay metadata is `FIRST_SOURCE_REPLAY_BINDINGS_REVISION_2.json`. The source repair is metadata-only; no source change is required.

## Raw first-line hash correction

Root finding `proposal_auxiliary_line_hash_finding.json` SHA256 `b56d34796e51274714fb5bfc789f099a3603c1b8add352a0ac8c17b1fc0dfccf` identified a 63-character copied value. This task independently opened the original trajectory JSONL in binary mode, read only the first raw line, and hashed those bytes without printing or copying the record contents:

- Original source path: `/home/lizening/wt-r19-recovery-duration-v1/artifacts/runtime/r19_b1_g3_successor_after_3d1ccea7_20261023T002200Z/source_trajectories.jsonl`
- First raw line length: `35,486` bytes.
- Computed SHA256: `465bff755ba34c18acca299470cd7c3a40455cb395df3e6fe43eee99119a7c73` (64 hex characters).
- The result matches root `independent_first_trace_metadata.json` (SHA256 `caf17db9bcc89c06103ee5b42aecd824e4a570b47e949044ad0f5c8b7ad280ff`).
- Whole trajectory-file hash remains the existing frozen binding `c6f37a7da28e326c70818524c79c17bbd85a286754c111f17db07cbe151a4f1c`; the line-level correction does not alter it.

The revised replay binding also corrects `path_bindings.data_root_original` to `/home/lizening/alfworld_data`, consistent with the authentic original G3 context. YAML `dataset.data_path` remains `/home/lizening/alfworld_data/json_2.1.1/train`; only the new factory's effective task discovery would narrow to this single historical task before constructor entry. No replay was run.

Exact corrected binding SHA256: `b2fdaa6db55572d0eca4d92dd865497a2caac7f0f82b437e8f79fa58d3c75944`. Machine-readable evidence and the captured builder receipt are `SOURCE_BINDING_REVISION_2_EVIDENCE.json` and `SOURCE_BINDING_REVISION_2_BUILD_RECEIPT.json`; checksums are in `SOURCE_BINDING_REVISION_2_FILE_HASHES.sha256`.

## Scope and calls

This is a raw-byte metadata correction only. No source/config/input/runtime files were modified. No model, CUDA, environment, ALFWorld, supervisor, preflight, test suite, or scientific execution was invoked; no training occurred. No launch is authorized by this addendum.
