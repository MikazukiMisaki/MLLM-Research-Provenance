# Append-only clarification: toy LoRA checkpoint metadata

The original on-disk safetensors metadata and receipts use the unchanged callback string `FICTIONAL_CPU_ONLY_NOT_LORA_NOT_SCIENCE`. **That string is inaccurate about the architecture of the tensors in this integration.** The saved 14 values are fictional PEFT LoRA adapter tensors from a tiny, randomly initialized, one-layer Qwen3 configuration. They are not a real P0, Qwen3-8B, production model or a scientific training result. The written file is a custom single `fictional.`-prefixed state dictionary, not a PEFT `save_pretrained` adapter export or a production LoRA format. The callback's existing scope string cannot by itself describe the tensor architecture correctly.

The wrapper's positive fixture strips the prefix and puts the 14 tensors into a toy PEFT model on a deep copy of the same initial random base; that toy check does not establish production artifact compatibility. In the interrupted fixture, the inner saver wrote the files but the outer callback did not return and the parent state is UNKNOWN; the disk receipt requiring callback return is not a completion receipt.

Original immutable evidence, SHA256:

- Normal `synthetic_evidence/normal/fake_final/receipt.json`: `4d0dfc32544488a0a5713082df9e3641444b5d06bbbda4303f85e9298397d06c`; its `fictional.safetensors`: `e45c56ea37f05c5b5679cb8fa6f7184e54d6a79b61fadee6f8a15d07e5f99c78`.
- Interrupted `synthetic_evidence/interrupt_after_checkpoint/fake_final/receipt.json`: `392aea6e94f30bb5a0dc32cd1afa7acc94ea097204d473406aaececc7d168b71`; its `fictional.safetensors`: `0c0d34d25eeadca18a8ccc92c76a23e0fc7255d1c53e375a81dd931accbe6e01`.
- Integration `fake_child.py`: `cbaea4cb2dbe9cefe6af415423168117d358b2404e0f14e4e3626479f292f69c`; unchanged original `final_checkpoint.py`: `6444205fbf05e0a2f6b39097a4a1841fd175e0e34877e039857b83136b990509`; integration `REPORT.md`: `a672dea2a4c2cd0d8f4ac3175df7a9750a411c3f6d12417684ffafca1874d4b1`.

The relative evidence paths above are under `/home/lizening/research-notes/agent-logs/20261118__CODEX__tiny-qwen-peft-ipc-atomic__private/`. Independent review: `/home/lizening/research-notes/agent-logs/20261118__REVIEW__tiny_qwen_ipc_atomic__private/REVIEW.md`, SHA256 `f9f16de8807e3c2c541e186fa75ea54a12b6e022fb32220bacd7fffec58c3b4e`.

Any future reuse requires a separately reviewed, unambiguous metadata and receipt schema that identifies toy LoRA content and custom format correctly; do not silently reinterpret, rewrite or replace the original receipt. This record adds clarification only: original artifacts and receipts were not changed, no test was rerun, and scientific execution remains HOLD.
