# MLLM Research Provenance

Private provenance and reproducibility records for the MLLM self-improvement research project.

This repository stores agent task records, experiment execution logs, implementation/review provenance, exact commit SHAs, test summaries, artifact hashes, operational incident reports, launcher/environment diagnostics, and raw result field summaries.

It does not replace the [scientific repository](https://github.com/MikazukiMisaki/Alfworld-Self-Improvement-Project). Model weights, adapters, datasets, caches, credentials, private keys, large runtime artifacts, and unredacted secrets do not belong here. Scientific execution remains subject to separate explicit authorization.

## Provenance chain

Research decision → implementation commit → independent execution → immutable outputs/hashes → scientific interpretation.

## Agent roles

Astra owns authorized implementation, scientific engineering, bug fixes, protocol/runtime hardening, and final technical acceptance.

Gemini is execution-only by default: authorized execution, tests, monitoring, result collection, hashes, task records, and provenance uploads. Gemini must not edit scientific source or tests, or repair unexpected scientific failures; it must stop and return evidence to Astra.

## Reading the records

Start with [INDEX.md](INDEX.md), [the task-record protocol](AGENT_TASK_RECORD_PROTOCOL.md), and [historical corrections](notes/HISTORICAL_CORRECTIONS.md). Original status labels are preserved; a later audit may contradict an earlier claim. Read corrections before interpreting execution evidence.

[FILE_HASHES.sha256](FILE_HASHES.sha256) describes the committed, sanitized provenance files. Historical inventories remain historical evidence and may refer to original bytes before documented redaction or to ignored local transient files. See [redaction notes](notes/REDACTIONS.md) for the explicit mapping. Local paths in logs identify the original research machine and are not portable commands to execute automatically.

Task directories are single-use records. Do not execute archived launchers, test helpers, or historical commands merely because they appear here. This repository does not authorize scientific work.
