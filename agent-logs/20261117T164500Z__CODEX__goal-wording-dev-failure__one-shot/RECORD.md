# Goal-wording DEV: first attempt stopped during first pair

This record describes a real, incomplete development attempt, not a completed paired comparison. The user had authorized bounded research. The fixed study compared the same P0 product with an original public goal and the same goal plus a fixed redundant two-object clarification, over four previously exposed authored DEV tasks. No claim of self-training improvement, an intervention effect, independent test performance, or statistical significance follows from the partial run.

The exact candidate config was `batch-config-claimed.json`, SHA256 `9b570fa0ed10bc982cc84915f5223670073d5cf02b6b51bfdf6f66ef72489438`. Its isolated supervisor was SHA256 `4cb0da4653e010a83c7813bdaac52341c80e25fdb51300e44297e06ae287f8f5`; the prior fixed task manifest SHA256 was `bba3dff9afdfb08943ec17dc9c8bace3105a4a61f9873a0510efaa3f0b0713e3`. It used the shared original one-shot output identity and shared GPU lock. `launch_metadata.json` SHA256 `71e0c01293ee9221c117e46757ed979cc9d849cc3a6a00d72c782ee815612db6` is a prelaunch record; its PREPARED status is not a final run status.

The actual supervisor process PID 1672366 and first worker PID 1672371 were observed running. The execution session returned **exit code 1**. The captured supervisor traceback reports `RuntimeError: GPU unavailable before model load`. The owner event at the second arm's model-load admission recorded 45,042 MiB free, 0% utilization, and `other_gpu_pids=1`; the event did not preserve the PID or enough information to determine ownership. It is therefore not established whether that process was the worker's own context or another workload. The gate stopped before reserving or starting the second model load.

## Observed outcomes and physical cost

- First pair, original-goal arm: one recorded completed episode, 50 decisions / 50 action steps, native `won=false`, `termination=TERMINAL`. This is one development outcome, not a paired treatment effect.
- First pair, clarified-goal arm: environment construction, initialization and reset returned; no model load or decision was started. Its outcome is UNKNOWN. The other six planned episodes were not executed.
- Owner journal counts, separately recounted as both reserved and returned: materialization 1, environment construction 2, environment initialization 2, reset 2, model load 1, generation 50, step 50. This gives 52 completed environment reset/step operations. The 50 generation records contain 13,175 input and 250 output tokens, including generated EOS; token count is calculated as recorded complete sequence length minus recorded output-ID length.
- No reserved operation lacked a matching owner-return event. That does not establish complete cleanup: the first arm logged environment, producer and resource closure; no closure for the second environment is recorded after the supervisor stopped the worker. Final supervisor event reports `no_remaining_children=true`, and both observed PIDs were absent afterwards; external-process delegation remains UNKNOWN. GPU snapshot after stop: 14 MiB used, 0% utilization, empty visible compute-app table.
- The observed owner event interval was approximately 61.93 seconds. It is a measured process interval, not total preparation time, total project cost or proof of exclusive GPU ownership.

The current evidence does not establish the missing clarified outcome, three other pairs, a successful statistical analysis, or a complete comparison. No retry, later pair, new training, mainline comparison, or other model/environment operation was performed after this failure. The original output is retained at `/home/lizening/research-notes/agent-logs/20261118__PARALLEL__goal-wording-experiment__private/fixed-p0-goal-wording-01/`; it must not be overwritten or relabeled as completed.

## Evidence digests

- Owner journal SHA256 `7e94e1c2efbcaa62be2ce4b55714f3a1a461a836f9cf77e023e8bc5a68e562be`.
- Worker journal SHA256 `1a3a71e0dd4cde91fca0df0f0da37181fbb2730720537553be368df651ab3d47`.
- First load's resource journal SHA256 `0c4aa8c88d7f7f50d9f2cd11e1c2e954b1ebb74469f1ed39361a38fb75cbf9cb`.
- Worker stderr SHA256 `9d600cb5d37dced87b09996aac39942a7fd51559eb1c1e2f5e35215358a836df`.
- Captured supervisor stderr SHA256 `7426dd404957f8e6cd0678e9fab79f7a2ab37219ba2047a55f3f444d0d6f903e`; stdout is empty, SHA256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

The supervisor's exit code was observed through the process-session API rather than from a supervisor-emitted `runner_exit.json`; this distinction is retained. The owner event `operation_returned` entries explicitly state `child_claim_only=true`; totals are journal recounts, not an independent measurement of external physical effects.
