# Record: latest Parallel Research package synchronization

- Status: `PUBLISHED_DEVELOPMENT_ONLY; ALLOWLIST_HASH_VERIFIED`
- Created: 2026-11-17T14:39:14Z
- Operator: Luna
- Scope: synchronize the latest completed Terra Designer and Parallel Research materials to the two private GitHub repositories. No scientific execution was authorized or performed by this publication task.

## Terra Designer

The existing curated Terra exploratory summary is already present in the project repository under `research_packages/terra_designer/exploratory_self_improvement_20261116/` (introduced by commit `36facd0f5efe04f4d633ab077fe4b640b82fd3e0`; current main before this publication was `730078305e8c09c2d86d3898b5d561cf27cd00e1`). The latest Terra thread contained a coordination status explanation, not a new output file. The project package index was updated in this publication to state that a formal comparison remains blocked pending independently sourced task/history evidence and a verified evaluation path; it does not claim a new experiment.

## Parallel Research packages

Copied only the 48 files enumerated by the three package manifests (45 payload files plus three manifests; 604,379 payload bytes and 7,312 manifest bytes). Their exact manifest SHA-256 values are:

- `progress_rule_probe_development_v1`: `2ea7ebeabf74948f5c597e24af316b8bffbfc07c04b851120ba0d24bc2b77167`
- `action_id_format_factorial_dev_v1`: `41e9c075b30baf30a33c1fde3758d81ad2267f0ba3a888d7ce99255294faae53`
- `execution_contract_factorial_dev_v1`: `f2dce25cca1a67df2fb3fd3e90e16d7e1888640daf67d043d63341f175fbdc58`

The progress probe's 16 fictional outputs yielded zero valid bare actions; bracketed relationships remain post-hoc. The action-ID/output-format factorial has 32 fictional outputs across eight authored cases. Its counts are tied to its frozen reference rules: the historical H4 parser expects `Action-ID: Axyz`, the current two-stage parser expects a bare ID, and the probes use a custom bare-reference rule. The packaged same-tokenizer unstripped audit reports no leading/trailing whitespace among 48 saved outputs, but this is not a production-parser simulation. The independent recompute uses saved decoded text and the standard library; it is not independent tokenizer decoding or model attestation.

The execution-contract package records a startup failure before model load: 32 planned calls, zero started, zero generations, and zero environment operations. Its `PRE_RUN_PROTOCOL_SNAPSHOT.md` is included and has SHA-256 `a7e44048bf7863107445b1160c859b93d0981ee4c16cd7a137d814466f5aa9c1`. A separate external protocol source referenced by the freeze was not in the allowlist and was not copied.

## Scope and exclusions

The Parallel worktree was at branch `codex/parallel-research-pilots-isolated`, HEAD `e537f441010077123a307e9d50ea40cf8dad8547`, with 2611 untracked status entries. Only the three manifest allowlists were read for payload transfer and published; unrelated worktree material was not staged or uploaded. Unlisted draft/cache file names were inventoried only; their contents were not read or included. The allowlisted content scan found no machine-local absolute paths, credential-pattern matches, or GPU UUID-pattern matches.

This publication invoked no model, tokenizer, ALFWorld environment, analyzer, validator, or pytest. Previously captured CPU-only analysis receipts are listed in `commands.log`; they were not rerun. These development packages are not held-out evaluation evidence and do not establish ALFWorld task success or generalization.

## Destinations

- Project repository: `MikazukiMisaki/Alfworld-Self-Improvement-Project`, main advanced from `730078305e8c09c2d86d3898b5d561cf27cd00e1` to `1fbad4721ed2c68bbeaedf7364995c7348035e48`; 48 package files were added and `research_packages/README.md` was updated.
- Provenance repository: `MikazukiMisaki/MLLM-Research-Provenance`, append-only task path `agent-logs/20261117T143914Z__LUNA__parallel-latest-research-github-sync__q7w3/`; parent main at preparation was `346648570e2883f50ed23c0ff95ea8dfb06c8881`.

See `PUBLICATION_MANIFEST.json`, `commands.log`, and `FILE_HASHES.sha256` for per-file bindings.
