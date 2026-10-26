# Luna SI-E2 / SI-P3 v2 read-only design delivery

- Status: `DESIGN_EVIDENCE_READY / COLLECTION_NO_GO_NOW / NO_NEW_RUNTIME_RELEASE`.
- Task: `/home/lizening/research-notes/agent-logs/2026-10-26T084826Z__SOL__si-e2-astra-plan-iteration__cec2ce5a/NEXT_STAGE_DESIGN_TASKS.md` (current SHA256 `12e312be741343e9998f331bad5a9a3b5ddb09df4444a0e47fd0cf869214fdd5`); coordinator decision SHA256 `91c95ff6d73944dc53425c31abcb512c422c1412e4743cff9f34b4dd930881ef`.
- Start/finish UTC: approximately `2026-10-26T09:41Z` (directory creation minute; first command timestamp not separately captured) / `2026-10-26T09:46:14Z`.
- Scope: identity-manifest joins, static paper budget and stop notes, and prior read-only execution-capability evidence only.
- No unused task bodies or scientific outputs opened; no model/tokenizer, CUDA/GPU/NVML, environment, SSH, project validator, test, preflight, launch, replay, acquisition, training, evaluation, or shared INDEX/inventory operation.

## Findings

1. Historical R19 127 and adopted A96 are exactly task/trial disjoint in the registered manifests; R19 also has zero exact identity overlap with S120 and registered expert-train. A96 is 35/26/16/9/10 over five non-light families; old R19 is 30/30/30/30 plus seven light and no pick-two. S120 has 44/32/20/11/13, all 120 identities in expert_train, and zero overlap with A96. These are task/trial metadata claims only—not proof of no semantic/scene leakage or unregistered historical viewing.
2. Old source failures are 7/127 (6/120 non-light) in the selected historical queue. This cannot forecast A96's yield, especially pick-two, absent from old R19.
3. The v2 paper ceilings are 4,800 source-only generations / 4,896 environment operations / 76,800 output tokens; full source-first ceiling 9,216 / 9,792 / 149,760. The 16M input-token and 4 device-hour limits are hard caps, not completion estimates. Training and 600-task evaluation are separate and unauthorized.
4. Trusted execution remains blocked. The prior single permitted `sdxsrv03` SSH attempt authentically failed with exit 255; no remote host/PID/NVML mapping was observed. Local `/proc/1/ns/pid` access was denied. No retry or guard waiver was made.
5. The current task file SHA differs from the historical digest embedded in the related v2 draft. This is disclosed in the cohort report and bindings; current task bytes were followed, not rewritten.

## Frozen files

- `COHORT_COMPARABILITY.md`
- `V2_PAPER_BUDGET_AND_STOPS.md`
- `INPUT_BINDINGS.json`
- `READ_ONLY_AUDIT_RECEIPT.json`
- `FILE_HASHES.sha256` (generated after content freeze; excludes itself)

All listed source-input hashes were rechecked after the audit and matched their initial values. No files outside this unique Luna-owned directory were changed. No commit/push was performed. No execution release is requested or inferred.
