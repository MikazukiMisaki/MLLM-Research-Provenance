# Source-only random-number contract check

Agent: Codex with independent source reviewer. Date: 2026-11-06 UTC. Status: `REPRODUCED_SYNTHETIC_FIXTURE_ONLY`.

The installed ALFWorld 0.4.2 generator and goal-template function were inspected as source; their exact hashes and the limitation of the passed random generator are documented in RNG_REVIEW.md. A software-only check executed AST-extracted source function definitions with invented metadata and a synthetic template registry, without importing ALFWorld or touching task data. It demonstrated differing template selection under the same supplied RNG seed when the separately controlled global RNG state changed.

Local-only `check_rng.py` SHA256 `b8a3805bfbd488a42346632d213c9f0907bb14260dc1ac511963844fa96e377a`; result JSON SHA256 `6508715ea8cfc41c504db57e3180960b8b897868c7b445de9403ebe181b90767`. They are retained locally because the script contains a machine-specific path. No task, protected material, CUDA, model or environment was used by this check; no source or installed package was altered. This establishes no historical drift and does not authorize generation or a scientific experiment.

Scientific worktree remains unchanged. Any future deterministic wrapper must be separately reviewed and tested using synthetic fixtures, and must not silently change the frozen baseline. A remote provenance commit cannot be embedded into its own bytes; successful publication and local synchronization must be verified separately.
