# Luna record — R19 live proposal metadata correction, revision 2

- Scope: correct only LIVE-P01/02/03 metadata defects in a new immutable proposal revision. Preserve the previous proposal/bindings bytes unchanged.
- Status: `PREPARATION_ONLY`; independent exact-proposal re-review pending; no clearance or user science authorization.
- Source: `/home/lizening/wt-r19-recovery-duration-v1`, detached clean at `2da980f631badc25086d12db60d128ff507d3ae6`; review-bound gate remains SHA256 `c285692615eaaf1c7cb7139b0417528022db6ee03c510de13f881d126f14415e`.
- No supervisor/preflight/live/model/ALFWorld/G2/G3/G4 invocation occurred. No scientific source, test, gate, config, frozen input, old evidence, output path, or future record path was modified/created.
- Read-only correction evidence is in `correction_evidence.json`; actual paths and raw bytes were hashed and parsed. The 3d1 supervisor files match the versioned restart authorization and run identity. Quotas match both protocol and authorization. Historical runtime raw/canonical digest domains were independently recomputed. Model aggregate is linked to the true preflight receipt field.
- Cumulative cost remains 177 model generations / 342 environment operations. The original failed source unit remains incomplete; its raw records and append-only adjudication were not rewritten.
- Supersedes prior proposal `c7b1a59fcb1ec2d968ac691efe4d3a3a6ddf523beb9df24d89cc902bca204967` and bindings `9f10793c0e73ac70c861c0ef8a8d2babbbe878f5aba167a5b4c61f26d2e05aa2` only. The prior files remain preserved byte-for-byte.

## Revision content hashes

- `R19_LIVE_SUCCESSOR_PROPOSAL_REVISION_2.md`: raw SHA256 `d6b4ebb9f77c434411e39f9ef13aea1bc42f86580bdaadf43c529e267202f754`.
- `bindings.json`: raw SHA256 `a6fd21f10c0acd28740c153521b3d0027e1445c51ce2600089eb73fd56cc82d9`; canonical SHA256 `33d10f0ccc5831a1fa782a61360b3aacab6fc04a48afe560e655c83eb0bb2eaa`.
- `correction_evidence.json`: raw SHA256 `77e01ef93a9b5a0ed97858b1eff0ff06b83ee0b458764a6596f383ac596c7410`; canonical SHA256 `cb000c9be53e8195455e7417e435dba52d036a3319956561ab28482293948cc7`.
- Copied argv/environment raw and canonical values are recorded above and are unchanged from revision 1.
- `correction_evidence.json` includes the observed raw/canonical values and parsed identity/quota comparisons from actual files. Reconciliation subprocess re-read all four predecessor supervisor artifacts, both quota sources, both runtime JSON artifacts, the frozen preload field, the authentic preflight receipt's model aggregate, and checked the copied argv/env bytes and preserved old binding digest; all comparisons returned true.
- `correction_evidence.json` raw SHA256: `77e01ef93a9b5a0ed97858b1eff0ff06b83ee0b458764a6596f383ac596c7410`; canonical SHA256 `cb000c9be53e8195455e7417e435dba52d036a3319956561ab28482293948cc7`.
- `secret_scan.json` SHA256 `5d8dc3081b2b13be4aff86bc2731d5e4765c065e3074a3dddb5b1fc1a9212c98`; the scoped credential-pattern scan found no matches.
- The revision's own `FILE_HASHES.sha256` and the provenance root inventory are the authoritative final file checks.

## Copied invocation artifacts

These files were copied byte-for-byte from proposal revision 1; canonicalization is UTF-8 compact JSON (`(',', ':')`, sorted keys, `ensure_ascii=false`; argv arrays contain no object keys):

- `child_argv.json`: raw `af84459ed7a90bb59f90b4965e959d4e80a24d6c3c563f443b4cb8f4433781fe`; canonical `93aa3a833fbb65241fcab6b7e68d3863fa83985084d9c1b27875c730285f55ef`.
- `supervisor_argv.json`: raw `c9f57d2735d95250b8a12d34c68f6ea7e8bd644e9a5c194bad55d42a81b4024b`; canonical `c2270f4e43d88d53022b38bc4bc0e1890bc49b738387f99485045fd9020e450a`.
- `environment_plan.json`: raw `24af21a3db2ae89abc56f81e5fb8e457ed3a801ca9fc21ef40a472b4c02703c9`; canonical whole-plan `d0bd5721913a6316affcbd4918befe65f2f9400a9d6e14536b88df5627e62189`; static `{set,unset}` canonical `4c1e7ef497ccdcc288e8e79c844705842ad15697c574108b9f146f3d64c148dc`.

No generated live run ID. Existing proposed output and record destinations remain absent. Sol's publication window is complete; publish this Luna-owned revision plus only Luna's INDEX/root inventory delta. Stage no other-agent files.
