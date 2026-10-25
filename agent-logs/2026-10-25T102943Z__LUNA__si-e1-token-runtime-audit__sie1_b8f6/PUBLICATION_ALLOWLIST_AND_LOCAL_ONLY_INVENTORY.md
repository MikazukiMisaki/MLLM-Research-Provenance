# SI-E1 publication allowlist and local-only inventory

Status: inventory/planning only. Nothing in this directory was uploaded or published; no INDEX or provenance Git operation was performed. The hash authority is `FILE_HASHES.sha256`. Sizes below are exact bytes at inventory time. Raw binary stdout/stderr was checked: no rendered prompts, full dataset/training rows, or token-ID arrays are present. The S manifest contains compact metadata rows (identity/hash/length/quality fields), not full training rows; token sequence digests are hashes, not token arrays.

## Publication candidates (allowlist; exact bytes)

These files are the proposed shareable evidence set, subject to the destination's normal review. Raw aggregate worker output is included by exact size/hash. This allowlist does not authorize publication by itself.

| Path | Bytes | SHA256 | Content/scope |
|---|---:|---|---|
| `S_BACKGROUND_MANIFEST.json` | 392466 | `6d4e8a937d05f91a2d49f76af2fc812d2b566e93e6a8acf38c56fe7ff832aec4` | Compact S120 identities and hashes/lengths/quality metadata; no prompts/full rows/token arrays |
| `TOKENIZER_MASK_AUDIT.json` | 9596 | `3c89d08979f72bf5c0dd4bbc7de7ead1c1c71d733c0be2df38c0d33424415ea5` | Aggregate tokenizer/mask counts and hashes; no prompt/full row/token arrays |
| `TOKENIZER_MASK_AUDIT.md` | 6950 | `df859cc1ec61637f5adbabdbbf49de50ebab4a89be0376fdbcbef7d68943a26e` | Human-readable bounded findings and corrected cap formula |
| `READ_ONLY_READINESS.md` | 5490 | `ad2c8bacd6a56b401c6a9b7f323c68cbd2933631bd4abed1c2aa7336e78a240a` | Readiness limitations; no runtime/pass claim |
| `raw/audit_worker_001.stdout.bin` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | Empty raw stdout from failed pre-tokenizer attempt |
| `raw/audit_worker_002.stdout.bin` | 448 | `8e060308c3fb265c4db297f897f651e673adbc7e6e1d9b06f51771e29771d2c2` | Aggregate counts/status only |
| `raw/audit_worker_003.stdout.bin` | 448 | `655dbbc98509f7141c52f4f9db95d892f162eb265693a3a762bd5b9f818e9412` | Aggregate counts/status only |
| `raw/audit_worker_002.stderr.bin` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | Empty raw stderr |
| `raw/audit_worker_003.stderr.bin` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | Empty raw stderr |

## LOCAL_ONLY inventory

Keep the following exact files local. Reasons include absolute machine paths/runtime origins, raw traceback path disclosure, subprocess argv/environment details, or implementation helpers. Their hashes are in `FILE_HASHES.sha256`; raw files also have exact size/hash listed here.

| Path | Bytes | SHA256 | Reason |
|---|---:|---|---|
| `BINDINGS_SOURCE_SCOPE_ADDENDUM.json` | 3684 | `936aee8f2e2ee9e494bd26979b1c2fa51531a319ec5667c39a54b004449b467d` | Absolute local checkout and evidence paths |
| `S120_INDEPENDENT_CLOSURE_ADDENDUM.json` | 2046 | `711289224c5e7ffd6ad4dcc824d03a78154de83f41578cc433f9cc6bbe7114dc` | Absolute local evidence paths |
| `RECORD.md` | 4548 | `06c4a8fc04d40048bae3ada0637a04b6e2017c06d00a56e49c23d2c40f839143` | Local audit provenance/context and paths |
| `input_bindings.json` | 66632 | `30f6facfb11850a13f4fa0233f9a837addd5b187bcefd9c67ad475d81dea2a05` | Absolute source/cache/runtime paths and package origins |
| `audit_worker_001.receipt.json` | 1503 | `f6227c73ba0a9bd14626d357c401485f0c3e15898f9c89892eff510bc2e48acd` | Absolute argv/cwd/raw paths and environment policy |
| `audit_worker_002.receipt.json` | 1503 | `4e2855039a107675da0ba7d1f61f334fbfc20d999b3e22851376687351ab5c06` | Absolute argv/cwd/raw paths and environment policy |
| `audit_worker_003.receipt.json` | 1503 | `3b8460034b1108eec61bf178b8cb6527ba5b1fc2188a24f9754d15d4a77c8676` | Absolute argv/cwd/raw paths and environment policy |
| `dependency_probe.receipt.json` | 3196 | `b99d700f118862d00dd8ae2bd7e43d8fd579a22c6a30d4a8a033718ddd624de8` | Absolute command and package-origin paths |
| `finalize_audit.receipt.json` | 2058 | `46aca8cdaacbd4cfc7786c5bc7a2e9153daaaab6d7db17905bf34211a1d4b088` | Absolute command/cwd and captured process summary |
| `raw/audit_worker_001.stderr.bin` | 645 | `60a060be5ba7c72238cb197a5ff45d6b5d89d02edd64e7885f16afc1e6caf11c` | Authentic traceback includes local absolute helper path; no prompt/row/token array |
| `raw/dependency_probe.stdout.bin` | 1876 | `cd1a20a5f4655b452712f0e2188cad6f0e37b434f7a2c48594267191fb9db50a` | Package versions plus absolute site-package origins |
| `raw/dependency_probe.stderr.bin` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | Empty; retained alongside probe receipt |
| `audit_worker.py` | 38156 | `00b39a34c74cbb8e139c4575e7f9fe077cff511ee5d650b7b344c91ce67c69c0` | Luna-local audit implementation, not project source |
| `run_capture.py` | 3372 | `9cc7bc9cca158b6715876e9b28ad226eeeb74fe1d12196b26ad5bcbd9494480c` | Luna-local command runner with machine paths |
| `finalize_audit.py` | 7449 | `85fdbb8581960cd2d305604bb60b09f698d39661f8b97b5c3085f3b1804a2b59` | Luna-local receipt aggregator |
| `capture_finalize.py` | 1087 | `fd6afbee97bf35faafad0aa92cbea819d41c9eda1729e11e16a1b606872508c1` | Luna-local receipt wrapper with machine paths |
| `FILE_HASHES.sha256` | 2444 | Not self-reported here; its hash is returned after freeze | Root hash manifest lists this inventory and other artifacts; its own hash is intentionally excluded to avoid a self-reference |

`PUBLICATION_ALLOWLIST_AND_LOCAL_ONLY_INVENTORY.md` is itself recorded in `FILE_HASHES.sha256`; that manifest intentionally does not hash itself. No science payload, dataset copy, weights, adapter, model cache, prompts, full training rows, or token-ID arrays are included in this task directory.
