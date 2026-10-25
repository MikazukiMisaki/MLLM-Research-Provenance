from pathlib import Path
OWN=Path(__file__).resolve().parent
assert OWN==Path('/home/lizening/research-notes/agent-logs/2026-10-25T102943Z__CODEX__si-e1-contract-implementation__sie1_b8f6')
ROOT=Path('/home/lizening/wt-si-p3-engineering-contracts')
p=ROOT/'src/self_improvement/si_p3/continuation.py'
assert not p.exists()
p.write_text(r'''"""P0 adapter continuation loader/controller; CPU toy software gate only.

There is no base-model constructor, live training driver, automatic release,
validation selection, optimizer-resume path, or get_peft_model replacement.
Future real training requires separate authorization and implementation review.
"""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path
from typing import Any, Sequence

from sft.training import directory_sha256

from .contract import P0_SHA256, digest, require
from .data import CompletionCollator, Example, audit_exposure, fixed_schedule

RECIPE = {
    "warm_start": "PeftModel.from_pretrained(base, P0, is_trainable=True)",
    "P0_directory_sha256": P0_SHA256, "LoRA_r": 32, "LoRA_alpha": 64, "LoRA_dropout": 0.05,
    "target_modules": "all-linear", "bias": "none", "epochs": 2, "examples": 144,
    "microbatch": 2, "accumulation": 8, "effective_batch": 16, "updates": 18,
    "learning_rate": 1e-4, "optimizer": "adamw_torch_fused", "weight_decay": 0.0,
    "scheduler": "cosine", "warmup_ratio": 0.03, "clip": 1.0, "bf16": True,
    "gradient_checkpointing": True, "packing": False, "completion_only": True, "max_length": 2048,
    "seed": 42, "data_seed": 42, "checkpoint": "final_update18_only", "fresh_optimizer": True,
    "drop_last": False, "independent_arm_shuffle": False, "best_validation": False,
    "execution_authorized": False,
}


def validate_recipe(value: dict[str, Any]) -> None:
    require(value == RECIPE and type(value.get("epochs")) is int and type(value.get("updates")) is int,
            "fixed continuation recipe; no fresh LoRA/best checkpoint/extra epoch/batch/search")


def require_cpu_toy(base: Any, evidence_class: str) -> None:
    require(evidence_class == "cpu_toy_software", "real P0 training NOT_GRANTED")
    parameters = list(base.parameters())
    require(bool(parameters) and sum(p.numel() for p in parameters) <= 1000000,
            "CPU toy parameter bound; actual Qwen/P0 forbidden")
    require(all(p.device.type == "cpu" for p in parameters), "CPU toy only, no GPU")
    require(getattr(base.config, "model_type", "") != "qwen3" and
            "Qwen3-8B" not in str(getattr(base.config, "_name_or_path", "")), "actual model forbidden")


def parameter_fingerprint(model: Any, *, lora: bool) -> str:
    import torch
    h = hashlib.sha256()
    for name, tensor in sorted(model.named_parameters()):
        if ("lora_" in name) != lora:
            continue
        h.update(name.encode())
        h.update(str(tuple(tensor.shape)).encode())
        h.update(str(tensor.dtype).encode())
        h.update(tensor.detach().cpu().contiguous().view(torch.uint8).numpy().tobytes())
    return h.hexdigest()


def lora_only(model: Any) -> list[Any]:
    trainable = []
    for name, parameter in model.named_parameters():
        require(not parameter.requires_grad or "lora_" in name, "non-LoRA trainable: " + name)
        if parameter.requires_grad:
            trainable.append(parameter)
    require(bool(trainable), "no trainable LoRA")
    return trainable


def load_p0_continuation(base: Any, adapter_path: Path, *, evidence_class: str,
                         expected_adapter_sha256: str = P0_SHA256) -> tuple[Any, dict[str, Any]]:
    require_cpu_toy(base, evidence_class)  # before PEFT loading, never builds an 8B base
    require(directory_sha256(Path(adapter_path)) == expected_adapter_sha256, "warm-start adapter file identity")
    from peft import PeftModel
    model = PeftModel.from_pretrained(base, str(adapter_path), is_trainable=True, local_files_only=True)
    config = model.peft_config["default"]
    require(config.r == 32 and config.lora_alpha == 64 and config.lora_dropout == 0.05 and config.bias == "none",
            "original LoRA recipe")
    require(not config.modules_to_save and not getattr(config, "use_dora", False), "LoRA-only continuation")
    # all-linear excludes the final output head, as in the original PEFT recipe.
    linear_names = {name for name, module in model.named_modules() if hasattr(module, "lora_A")}
    require(bool(linear_names), "missing loaded LoRA modules")
    lora_only(model)
    report = {"evidence_class": evidence_class, "actual_P0_verified": False,
              "loaded_adapter_sha256": expected_adapter_sha256,
              "loader": "PeftModel.from_pretrained", "is_trainable": True,
              "initial_lora_parameters_sha256": parameter_fingerprint(model, lora=True),
              "initial_frozen_parameters_sha256": parameter_fingerprint(model, lora=False)}
    return model, report


class Final18Controller:
    """Execute the fixed paired schedule on a tiny CPU fixture, not real science.

    Loss is a sum divided by the entire update's actual shifted target count;
    gradient accumulation therefore does not accidentally average unequal
    microbatch denominators. Padding and prompt never enter the objective.
    """
    def __init__(self, model: Any, pairs: Sequence[tuple[Example, Example]], collator: CompletionCollator,
                 output_dir: Path, *, arm: str, evidence_class: str, recipe: dict[str, Any] | None = None) -> None:
        require_cpu_toy(model, evidence_class)
        validate_recipe(RECIPE if recipe is None else recipe)
        require(arm in ("B", "C"), "arm identity")
        self.exposure = audit_exposure(pairs, collator)
        self.pairs, self.collator = tuple(pairs), collator
        self.arm, self.arm_index, self.model = arm, 0 if arm == "B" else 1, model
        self.output = Path(output_dir)
        self.output.mkdir(parents=True, exist_ok=False)  # no overwrite/resume
        import torch
        torch.manual_seed(42)
        self.parameters = lora_only(model)
        # CPU software exception: fp32 and non-fused AdamW, never advertised as real bf16/fused evidence.
        self.optimizer = torch.optim.AdamW(self.parameters, lr=1e-4, weight_decay=0.0, fused=False)
        require(not self.optimizer.state, "fresh optimizer required")
        warmup = math.ceil(18 * 0.03)

        def multiplier(step: int) -> float:
            if step < warmup:
                return step / warmup
            return 0.5 * (1 + math.cos(math.pi * (step - warmup) / (18 - warmup)))

        self.scheduler = torch.optim.lr_scheduler.LambdaLR(self.optimizer, multiplier)
        self.schedule = fixed_schedule()
        self.microbatches = [tuple(epoch[i:i + 2]) for epoch in self.schedule for i in range(0, 144, 2)]
        self.cursor = self.updates = 0
        self.log: list[dict[str, Any]] = []
        self.frozen_before = parameter_fingerprint(model, lora=False)
        self.lora_before = parameter_fingerprint(model, lora=True)
        self.optimizer.zero_grad(set_to_none=True)
        model.config.use_cache = False
        model.train()

    def consume(self, slot_indices: Sequence[int]) -> dict[str, Any]:
        import torch
        import torch.nn.functional as F
        require(self.cursor < 144 and tuple(slot_indices) == self.microbatches[self.cursor],
                "fixed paired slot order/batch boundary; extra step/drop-last/shuffle forbidden")
        examples = [self.pairs[i][self.arm_index] for i in slot_indices]
        batch = self.collator(examples)
        require(int(batch["input_ids"].max()) < self.model.config.vocab_size, "toy vocabulary bound")
        update_start = (self.cursor // 8) * 8
        denominator = sum(self.pairs[i][self.arm_index].loss_tokens
                          for micro in self.microbatches[update_start:update_start + 8] for i in micro)
        logits = self.model(input_ids=batch["input_ids"], attention_mask=batch["attention_mask"]).logits
        shifted_labels = batch["labels"][:, 1:].contiguous()
        loss_sum = F.cross_entropy(logits[:, :-1, :].contiguous().float().view(-1, logits.shape[-1]),
                                  shifted_labels.view(-1), ignore_index=-100, reduction="sum")
        require(bool(torch.isfinite(loss_sum)), "nonfinite software loss")
        (loss_sum / denominator).backward()
        self.cursor += 1
        if self.cursor % 8 == 0:
            torch.nn.utils.clip_grad_norm_(self.parameters, 1.0)
            self.optimizer.step()
            self.scheduler.step()
            self.optimizer.zero_grad(set_to_none=True)
            self.updates += 1
        row = {"microbatch": self.cursor, "optimizer_updates": self.updates, "slots": list(slot_indices),
               "loss_sum": float(loss_sum.detach()), "update_loss_token_denominator": denominator,
               "actual_shifted_tokens": int((shifted_labels != -100).sum())}
        self.log.append(row)
        return row

    def finish(self) -> dict[str, Any]:
        require(self.cursor == 144 and self.updates == 18, "only final18 can be saved; no partial/best checkpoint")
        require(parameter_fingerprint(self.model, lora=False) == self.frozen_before, "frozen base changed")
        lora_only(self.model)
        final = self.output / "final_update18_adapter"
        require(not final.exists(), "final output already exists")
        self.model.save_pretrained(str(final), safe_serialization=True)
        result = {"evidence_class": "cpu_toy_software", "real_training_performed": False,
                  "real_P0_warm_start_verified": False, "arm": self.arm, "updates": 18, "epochs": 2,
                  "initial_lora_sha256": self.lora_before, "final_lora_sha256": parameter_fingerprint(self.model, lora=True),
                  "frozen_base_sha256": self.frozen_before, "adapter_sha256": directory_sha256(final),
                  "schedule_sha256": self.exposure["schedule_sha256"], "actual_microbatches": self.log,
                  "CPU_exceptions": ["fp32 tiny model", "non-fused CPU AdamW", "no actual P0 weights"],
                  "scientific_execution_authorized": False}
        (self.output / "software_receipt.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
        return result
''')
print(p.relative_to(ROOT))
