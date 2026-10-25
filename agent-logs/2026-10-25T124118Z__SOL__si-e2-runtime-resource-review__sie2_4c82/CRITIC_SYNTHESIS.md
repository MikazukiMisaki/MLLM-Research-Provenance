# Independent runtime contract critique

Internal independent critic si_e2_runtime_critic read a995 source and installed PEFT interfaces. Review guidance was delivered to both Sol Research and Luna; this is engineering guidance, not a frozen-candidate PASS.

- Equal input-token lengths do not bind full tensor identity. Compare rendering, full IDs and attention mask before generation. Test same-length substitution.
- PEFT active adapter names remain populated while layers are disabled. Read actual model/layer enabled, active and merged state before/during/after P0→BASE→BASE→P0; restoration on exceptions mandatory.
- ExactTaskPoolEnvironment seeds the underlying environment at construction; reset(seed) does not reseed that same TextWorld instance. Use two fresh, single-file instances with identical pool_seed. Do not change old environment methods.
- Full ordered maps and transitions must compare. Missing terminal maps are an unresolved interface, never repaired by replacing None with (). Predetermine the historical episode without outcome selection.
- Bind physical UUID before CUDA import; require single-device placement and no offload. Free VRAM alone is not a scheduler/exclusivity guarantee. Preserve BF16 base / default F32 LoRA behavior, no quantization change.
- Parent supervisor must terminate its own process group on hard deadline, save authentic child returncode, preserve incomplete reservations, and never kill unrelated processes or retry.
- Real evidence is engineering, never synthetic. Keep strict frozen generation wire format; place auxiliary state proof alongside it. This phase does not generate an acquisition pool or establish learning efficacy.
- Static storage is observed: 8,190,735,360 BF16 base parameters (16,381,470,720 tensor bytes); 87,293,952 F32 P0 parameters (349,175,808 bytes). Unmeasured activations/optimizer/workspace/throughput prevent a training-fit claim.
