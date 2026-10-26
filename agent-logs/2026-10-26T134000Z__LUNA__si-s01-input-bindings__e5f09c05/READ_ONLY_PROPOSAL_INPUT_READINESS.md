# SI-S01 engineering proposal input readiness

Status: `READ_ONLY_PREPARATION / NOT_RELEASE / NOT_RUNTIME_READY`. This is an input checklist and evidence summary only; it is not an executable proposal, gate, authorization, argv, or scientific output path.

## Scope and candidate identity

Verified the task (`ENGINEERING_ADAPTER_IMPLEMENTATION_TASK.md`, SHA-256 `525d271b38a8ecd2248c653291679a1c8fd37ceaec05b4dbf3b575932a7e103b`), proposal revision 2 (`fe974f732ca03d96718c679facaf1201aa78a364c2f3251690c461f28acf189f`), coupled-path addendum (`2c03660bf71a08cfdad524ba1215abc9aff1c957552412f87d019947a39f6ded`), and adopted protocol (`daa1d787f9ef13f5927dcf696a2be4c6328dc159b3eb39b5f0f5f520582ebb72`). The exact independent d7 source-only software review is `0e878105b523afef4af18d130f6a60dacccd127c27e6f580723cf625ce2e385d`; it does not review or authorize engineering runtime.

The current implementation checkout observed at HEAD `e5f09c05824cb61cb35ccbbf4e189b04e8829cea`, branch `codex/si-s01-engineering-adapter`, was clean at observation. This is an unaccepted development candidate only: no final independent engineering review or release is inferred, and this SHA is not represented as frozen/reviewed.

## Frozen local input bytes

The 12 files in the exact cached Qwen3-8B snapshot `b968826d9c46dd6066d109eabc6255188de91218` were fully SHA-256 read in the current container and all matched the R19 model identity manifest. Their names, byte lengths, and observed digests are enumerated in `PROPOSAL_INPUT_BINDINGS.json`. No weight/tokenizer content was copied into this directory. This establishes only container-visible byte identity; it does not establish that a later designated host sees the same cache.

The P0 adapter directory was hashed using a standard-library reproduction of the original `sft.training.directory_sha256` algorithm (sorted recursive files; relative-path bytes then file bytes in 1 MiB chunks). It contains 11 files / 365,138,109 bytes and computes to `6e403d85b150a74dfcc176f1f180ce4baf6fdacd922d2f96b3ceef0a21100f11`, matching the frozen d7 constant and historical G3 execution manifest. Adapter contents were not copied or printed.

Historical configuration/logic references and hashes are in the JSON binding. The actual old launch used `ALFWORLD_DATA=/home/lizening/alfworld_data`; the local YAML's `dataset.data_path` is the nested `/home/lizening/alfworld_data/json_2.1.1/train`. These are different path roles. The two frozen logic file hashes match the recorded runtime environment identity. No task dataset body was traversed.

## Historical evidence bound by reference

The historical execution identity is source SHA `2da980f631badc25086d12db60d128ff507d3ae6`, run `260422ac02bd42a8b2929d7ef240526b`, first source index 0, nominal seed 30000. The certified whole trajectory SHA `c6f37a7da28e326c70818524c79c17bbd85a286754c111f17db07cbe151a4f1c` is referenced, not recomputed. The prior Luna bounded binding JSON (`FIRST_SOURCE_EVENT_BINDINGS_V2.json`, SHA-256 `c361ba0c9d9276eb7dc20c31d0428f51db3f1a9fdd7fccfa23db5edc4f64eb38`) identifies the raw first row and exactly nine required event slices (reset, six transitions, source completion, first generation); no whole-journal rescan was performed.

The historical raw supervisor launch context, runner exit, supervisor status, runner log, runtime manifests, environment manifest, G3 gate receipt, source restart comparison, and execution manifest have exact paths, byte lengths where observed, and raw SHA-256s listed in `PROPOSAL_INPUT_BINDINGS.json`. Raw file hashes are kept distinct from canonical/preload digests. The historical runtime manifest records Python 3.10.20 and package versions; it does not bind module origins, and these historical versions are not evidence of present host packages.

Historical science totals remain 5,142 generations / 7,949 environment operations including resets. Any authorized engineering calls must be separately charged. No engineering call was made here.

## Required coupled-path contract for a later proposal

Any later implementation/authorization must bind the single original first-source identity and preserve the exact limits: one P0 load/tokenizer load, one explicit one-byte context probe, one generation (maximum 16 output tokens / 8,192 input tokens), one construction, reset at nominal seed 30000 plus six saved commands (seven reset-inclusive environment operations), one close, and 600 total allocated seconds including cleanup. Pool seed 42 is a new engineering choice and must be labelled as not reconstructing historical internal RNG.

Before action 1, the joined evidence must compare the actual reset state/map, reconstructed original public prompt, prepared-versus-sent tensor identity, new raw output/parser/Action-ID mapping, and first saved command. Then execute only the six saved commands and bind each current public transition/map to its historical receipt. Any mismatch or uncertainty stops immediately: no retry, alternate prompt/seed, second reset, seventh operation, or different action. This contract is preparation context, not an invocation instruction.

## Remaining conditions

- Final engineering implementation candidate, exact-SHA independent review, and source/software acceptance: `PENDING`.
- New root-issued one-shot engineering authorization and separate independent launch clearance: `NOT_GRANTED`. Prior clearances are consumed and cannot be reused.
- Forwarded SSH-agent socket: root checkpoint 4 reports `ENOENT` (checkpoint SHA `4aad481852493fbc3358d5409f29bed90bb9c8579231f6b2c0a397194819b093`); not rechecked and no SSH attempt made.
- Designated-host UID mapping, trusted GPU UUID ownership/process mapping, host-visible model/adapter bytes, current package versions/module origins, and future raw argv/environment: `NOT_OBSERVED` / `NOT_CREATED`.
- A future concrete proposal still needs a unique absent output/record identity and exact immutable source/runtime/input bindings. None was created here.

No model/tokenizer import or load, CUDA query/context, environment construction/reset/step, SSH, project validator/test, preflight, supervisor, or scientific action occurred. No shared INDEX/inventory, source tree, or existing evidence was changed; nothing was staged or pushed.
