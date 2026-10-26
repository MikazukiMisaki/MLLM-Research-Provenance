PREPARED ONLY — NOT EXECUTED; no runtime result or acceptance is claimed.

Wait for root's explicitly frozen exact SHA. Use a NEW independent clean detached
worktree at that SHA; do not run in the developer/root checkout. Keep this original
script immutable. If the frozen public API differs, make a separately hashed small
revision rather than editing production or requesting a test-only API.

One invocation with the pinned Python, replacing the three angle-bracket values:

env -u PYTHONPATH -u PYTHONHOME -u VIRTUAL_ENV \
  CUDA_VISIBLE_DEVICES='' PYTHONDONTWRITEBYTECODE=1 \
  HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 TOKENIZERS_PARALLELISM=false \
  /home/lizening/miniconda3/envs/alfworld-self-improve/bin/python -I \
  /tmp/si-s01-eng-independent-closure-ZcfUhzvC/independent_closure_probe.py \
  --repository <NEW_DETACHED_WORKTREE> --expected-sha <FROZEN_40_HEX_SHA> \
  --output <NEW_ABSOLUTE_OUTPUT_DIRECTORY>

Root should capture the authentic subprocess rc, raw stdout/stderr and interpreter,
script, fixture and source hashes. The script writes probe_observations.json plus
its synthetic raw journals in the fresh output. It does not invoke pytest or a CLI
preflight, replay old inputs, contact SSH, or use real tokenizer/model/CUDA/ALFWorld.
Production reader, EngineeringPermit/Ledger/Producer/shared core/parser/audit run
against the fixture's explicit raw I/O edges. No acceptance guard is mocked.

Six observations only:
1. Same reserved unit, second producer call: fake raw-model count remains 1.
2. Caller mutates the prepared dictionary and nested lists after reservation:
   raw-model count remains 0 and durable prepared/input debit remain original.
3–4. Fake time crosses 600 after resource observation or CUDA synchronization:
   raw-model count remains 0; no new close edge after exhaustion.
5–6. From one complete successful synthetic joined run, alter only saved returned
   raw latency or observed sequence prefix. Independently recompute the full chain
   and all forward completion-start references. Real read_events must accept it;
   real audit must reject the semantic conflict without adding external calls.

These are software closure observations for ENG-PC01/PC02/A01 only. No scientific
acceptance, exact internal RNG claim, real release, or launch clearance follows.
