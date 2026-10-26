# SI-S01 engineering runtime static review

Target: `87f46d731f1575731bd7ea1fa7dfb2e982da4c33`. Direct parent/base: `d7a82acb510157ab7ba5439d790816c5c948439f`.

Decision: no new concrete static findings in the assigned runtime/source-parity, once-only and timeout scope. This is not final implementation acceptance, hardware proof, preflight release or launch clearance. Final developer freeze handoff remains pending; a changed final SHA requires changed-object re-review.

`AST_COMPARISON.json` retains every complete normalized base AST, candidate equality/digest, and precise normalization allowances. Source-mode loader/generation, source identity prefix, resource guard, LiveEnvironment, run_worker, source supervisor, and RuntimeSink bodies compare equal. Source-only load additionally tightens the Permit type guard.

PC01 is statically closed at EngineeringLedger.begin58-59, require_generation94-98, claim_generation99-105 and before_generate106-111: the persisted prepared reservation is deeply copied, actual input must match, and invocation/model-boundary claims are consumed once. EngineeringProducer.generate39-43 and _raw36-38 reach those guards.

PC02 is statically closed at runtime_core61-67 and EngineeringLedger.before_generate106-111: the engineering deadline is checked after resource inspection/CUDA synchronization and again after boundary evidence fsync before model.generate. Source does not pass this optional hook, preserving d7 source behavior.

The source supervisor body is unchanged after exact SOURCE_PROFILE substitution. The engineering profile limits this mechanism to600 seconds with science=false; fresh claim/output, atomic worker marker, absolute wait/cleanup deadlines and authentic final result/report checks remain. Final device-hour authority remains the supervisor receipt rather than a worker report.

Eight exact target file SHA256s were captured twice from immutable Git objects and are equal; method source-span/AST hashes and target tree are in METHOD_AND_FILE_HASHES.json. This records committed bytes rather than mutable checkout contents.

Only Git reads and Python standard-library AST/hash/record serialization were used. No project imports, tests, production helper/old reader execution, CUDA/NVML, tokenizer/model/environment, SSH, preflight or science calls occurred. Only this new review directory was written. No scientific source, existing evidence, shared INDEX/inventory, stage or push was changed. Other full-suite, gate, history-reader and evidence-consumer work belongs to the root's independent review and is not claimed here.
