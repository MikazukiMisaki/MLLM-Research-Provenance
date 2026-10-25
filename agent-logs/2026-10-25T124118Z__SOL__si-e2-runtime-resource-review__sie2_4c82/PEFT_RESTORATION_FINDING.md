# SI-E2 draft inference restoration defect

Independent CPU-only reproduction with installed PEFT0.17.1 and a1144-parameter GPT2 LoRA toy (no8B model, generation, optimizer, environment or saved weights): all parameters frozen before the context; get_model_status before={enabled:true,trainable_params:0}; inside disable_adapter={enabled:false,trainable_params:0}; after normal context exit={enabled:true,trainable_params:64}. Actual script exit0 and raw stdout/stderr/receipt retained in independent_software/installed_peft_restoration_cpu.*.

Cause: PEFT BaseTunerLayer.enable_adapters calls set_adapter, whose documented behavior enables gradients for active adapter parameters. peft_model.disable_adapter finally enables adapter layers. Active adapter names stay default throughout.

Impact in draft runtime_backend: BASE generation after-state verification correctly requires inference0trainable and exact restoration, so the unamended default context will reject. This is a draft finding, not a frozen-candidate verdict; no real probe was run.

Required minimal correction within existing scope: retain and restore original requires_grad flags on normal and exception context exit BEFORE asserting exact after-state equality; preserve no-grad/inference checks. Do not relax trainability checks or change weights. Genuine installed tinyPEFT tests must exercise both successful P0→BASE→BASE→P0 and exception restoration. Sent to Sol Research before freeze.
