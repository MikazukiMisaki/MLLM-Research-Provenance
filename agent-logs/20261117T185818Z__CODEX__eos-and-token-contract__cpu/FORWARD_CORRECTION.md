# Proposed prospective EOS/PAD metadata correction

**Candidate for integration and independent review; not execution clearance.**
The original Luna plan is preserved byte for byte at SHA256
`3df73994bc2aba5912959ab7c0970241cba071466f85a8ef440c4b57c5ca03ec`.
This artifact does not alter the original plan, past records, actor rules,
already consumed budgets, or any stopped run. A prospective protocol must
explicitly adopt and bind this correction rather than silently overwrite the
old plan.

The original plan's `inference_contract.tokenizer_eos_id` is `151643` and
equals its PAD. The hash-bound base's static `tokenizer_config.json` instead
maps its primary EOS `<|im_end|>` to **151645** and PAD `<|endoftext|>` to
**151643**. Its `generation_config.json` lists model stopping IDs
`[151645, 151643]` and PAD `151643`. These terms have different roles: the
model generation stop set includes an ID that is PAD; the current actor does
not therefore treat that PAD as an acceptable final output.

Prospectively correct only the primary tokenizer EOS metadata to `151645`;
retain the existing ordered generation stop list, PAD value and frozen actor
logic. For the bound producer, its `eos_ids` are derived from the tokenizer
primary EOS (`live_runtime.py:74–79`). The existing episode rejects primary
EOS equal to PAD (`episode.py:50–55`). Existing `_generation` requires its
producer EOS to agree with tokenizer primary, checks the model stop list and
PAD, and requires a final acceptable primary EOS to be non-PAD. A final PAD
is classified `OUTPUT_PADDING`/policy failure; a model stop occurring earlier
in the output is classified `EARLIER_EOS`/policy failure. This correction
does not accept PAD as a successful terminator.

## Machine-checkable candidate and evidence

`eos_binding_candidate.json`, SHA256
`d1acf6f80086576dcfc4cbad257e47e9e7eef3a79672bd047221f28b46e4fec1`,
binds the original plan, tokenizer and generation static metadata, exact
producer/episode/generation source files and controlled test source; it
separately records primary EOS, model stop IDs, PAD and actor disposition.
`verify_binding.py`, SHA256
`e2f71a5db8c8f745fe97c7760b4b27906263d6ccbc0339acebe03f78c31d59ae`,
verifies those hashes and static fields without loading a tokenizer or model.
It exited 0 and produced `static-verification.log`, SHA256
`24383fac4ce369229aa236be78fe40f82f73fce4be11de4bf3070040b5a37386`.

The existing real episode/_generation CPU tests, with entirely fictional
tokenizer/model/environment edges, were independently rerun in isolated Python:
**4 passed, exit 0**. `cpu-test.log` SHA256
`feabb4add9e2ca3374e538560634d1ec97dc4f4ce89aab12f3d726e36ea9b2f6`.
They cover distinct primary EOS/PAD reaching generation/parser, equal
primary/PAD rejected before generation, final PAD classified output-padding
failure, and intermediate PAD/model stop classified earlier-EOS failure.
They do not load the real tokenizer, model, CUDA or ALFWorld.

## Still required

The candidate's source and configuration hashes and correction need
independent review and explicit prospective protocol integration. A future
runtime must compare the actual loaded tokenizer primary EOS and PAD,
producer EOS tuple, effective generation config/stop IDs and forced-EOS value
against the accepted binding before scientific use; this static review did
not observe an actual loaded runtime. Notably the static `generation_config`
file omits `forced_eos_token_id`; the runtime's effective configuration must
still supply the expected null value to pass the existing actor check.
Token-budget enforcement, genuine task/actor binding, process supervision,
scientific provenance and resource limits remain separate conditions.
