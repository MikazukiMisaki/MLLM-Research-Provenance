# SI-E2 runtime adaptation and resource verification

Created 2026-10-25T12:41:18Z by Sol Designer, reviewer thread 01a0994c-a209-7600-8a3e-5ff3096ed346. User explicitly requested real-runtime adaptation and GPU resource verification, using Sol Research and Luna. This phase supersedes the earlier ban on doing that engineering work; it does not authorize acquisition96, student training/evaluation, or historical experiment reruns.

Starting scientific exact SHA: a995d4c3c5f7d31a2cf1fd0afc4bfa4bd72ee3a3. Prior independent engineering review SHA256: 7bd6f4a6e24ea017e98814ec4c7a252c5d68a695816041243e1c5fa0dabb85ed. Provenance starting remote main: aa925dd0ba4a44121e1a9eeaddb36a13eec974a4.

## Dependency and authority

Sol Research isolated implementation/software tests -> frozen exact SHA -> root independent review -> Luna's concrete immutable probe argv/environment/input/resource proposal -> root bounded engineering release -> one supervised engineering probe -> independent evidence review. Developers have no independent acceptance or execution authority. Luna may inspect hardware/config/cache metadata read-only now, but must not load a model, construct/reset/step ALFWorld, or launch the real probe before root releases that concrete frozen proposal.

Scientific acquisition, training, evaluation and launch clearance remain NOT_GRANTED. Old R19 clearance and 8999 restart headroom have no authority here. Keep the 96 acquisition/48 reserve/600 evaluation task bodies closed. No original artifact mutation. All new expenses are engineering expenses, separately counted; historical cumulative science remains 5142 generations / 7949 reset-inclusive operations.

## Minimum deliverable

Actual cached Qwen3-8B + exact P0 LoRA inference backend; prepared input/token equality before generation reservation; local/offline-only loading; no sampling/thinking; frozen generation semantics and v2 parsers; active adapter-on/off evidence from actual PEFT state before/during/after each call, including restoration on exceptions. No reliance solely on caller-supplied adapter labels. No quantization/model/prompt/decoding change. Reuse proven base backend where possible without modifying historical methods.

Bind one visible A40 by UUID, ownership/process checks, real elapsed device allocation, hard subprocess deadline, honest partial/open reservations on failure, no retry, unique output and authentic exit. Keep existing Collector synthetic-only gate unless a separately reviewed tightly scoped engineering bridge is essential. No general scientific collection or training driver is required or released. A distinct engineering probe may exercise real producer and normalized environment boundaries separately, while the full collector remains covered by production synthetic tests. Clearly disclose that boundary.

## Proposed ceiling for later engineering release (not a launch release)

One probe, <=1800 seconds and <=0.5 allocated device-hour, exactly one GPU UUID. <=4 real generation calls, phases source(16), stage_one(40), stage_two(16), suffix(16), <=88 total generated tokens, <=8192 input tokens per call and <=32768 total. Use a fixed synthetic public state/prompt (explicit engineering evidence), not a fresh task. No model-produced command is executed in ALFWorld. Preserve raw tokens, prompts, actual adapter state, timing/memory, parse statuses including invalid output; semantic success is not an acceptance target.

ALFWorld boundary verification: at most 2 resets and 100 physical action steps, using only an already completed, hash-bound R19 TRAIN source trajectory and its saved commands (<=50 per replay). The exact task/seed/trajectory and command count must be selected and bound before release. Compare repeated reset/state/action maps/replay transitions/terminal-map availability; do not inspect or sample any reserved new task. Model and environment probes can fail independently but failure stops the supervisor, with no retry. Environment construction/close and incomplete external calls are recorded separately. No optimizer step, gradient-training run, adapter save, heldout outcome, G2/G3/G4 rerun or acquisition pool artifact.

Resource readiness is conditional on observed memory/latency/ownership, not a claim of training fit or a 96-task completion forecast. Read-only feasibility estimates for future bf16 continuation must distinguish static lower bounds from unmeasured activations/optimizer peaks.

## Preservation and publication

Each agent writes only its own new task directory. Do not edit/stage/commit/push provenance INDEX, inventories or other agent records. Root alone coordinates publication. Sol may push its own new scientific branch non-force. Do not publish any weights, adapters, caches, input datasets or token-array fixtures. Preserve compact commands/receipts/hashes and genuine failure evidence. Historical failures remain baseline, not fixes for this task.
