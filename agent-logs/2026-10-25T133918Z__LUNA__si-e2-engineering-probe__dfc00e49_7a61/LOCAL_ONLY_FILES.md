# Local-only files

These files are retained for reproducibility but excluded from the proposed publication allowlist because they contain machine-specific paths, operational environment details, or executable local helpers:

- `SAFE_ENVIRONMENT_VALUES.json` — captured values from the explicitly allowed environment-key list; contains local paths/runtime settings.
- `capture_prompt_digest.py`
- `capture_safe_environment.py`
- `verify_proposal_inputs.py`
- `capture_final_proposal_state.py`
- `finalize_proposal_hashes.py`
- `capture_finalize_proposal.py`
- `build_file_hashes.py`
- `check_final_consistency.py`
- `capture_final_consistency.py`

No model weights, adapter payloads, cache contents, tokenizer payloads, raw prompts, task rows, training rows, or token arrays exist in this directory. Compact task bindings contain local paths and input digests for audit and require disclosure review before external publication.
