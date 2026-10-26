# SI-P3 v2 cohort comparability — read-only identity audit

**Status: metadata-only; no new partition or execution authority.** No unused task body, trajectory payload, model, environment, CUDA, SSH, validator, test, or schedule was opened or invoked. Task identity means the registered canonical task/trial string only; this does not establish scene/layout or semantic independence.

## Verified roster and family shape

| Roster | N | pick-place | clean | cool | heat | pick-two | light |
|---|---:|---:|---:|---:|---:|---:|---:|
| Historical R19 source | 127 | 30 | 30 | 30 | 30 | 0 | 7 |
| Adopted A96 reservation | 96 | 35 | 26 | 16 | 9 | 10 | 0 |
| Historical S120 background | 120 | 44 | 32 | 20 | 11 | 13 | 0 |

The old R19 family counts and success summary come from the preserved P0 inventory: 120 source successes and 7 non-successes, with 127 distinct canonical identities. Its success-index list has 120 identities; the separate known-use registry has all 127 R19 source identities. The new A96 is the already adopted `acquisition_feasibility_96` partition, not a new draw. Its five-family quotas match the adopted metadata reservation. No light tasks occur in A96; pick-two has no historical R19 source rows. Therefore the old queue is not family-balanced against A96, and old outcomes cannot be treated as a yield estimate for A96.

## Exact identity intersections from registered metadata

The following are exact task/trial string joins among the listed, already frozen identity manifests:

| Intersection | Count | Interpretation |
|---|---:|---|
| Historical R19 127 ∩ adopted A96 | 0 | Exact task/trial disjointness is supported by the full registered R19 identity list and the A96 manifest. |
| Historical R19 127 ∩ registered `expert_train` | 0 | Direct join against all 1,074 registered expert-train identities; agrees with the old P0 split-overlap summary. |
| Historical R19 127 ∩ S120 | 0 | Direct join; all 120 S120 tasks are members of `expert_train`. |
| A96 ∩ S120 | 0 | Direct join; also consistent with E1's recorded A96 cross-overlap count of zero. |
| A96 ∩ registered known-use union | 0 | The union has 2,612 identities; the adopted roster is excluded from that registered union. |
| S120 ∩ `expert_train` | 120 | All selected S120 identities are in the registered expert-train set. |
| R19 K1 branch identities (39) ∩ A96 / S120 | 0 / 0 | Direct join from the P2 parent manifest. |
| P2 parent union (169 unique task/trials) ∩ A96 / S120 | 0 / 0 | Direct join from the P2 parent manifest. |

These counts describe only exact registered task/trial identity. They do not certify that all historical viewing/consumption was registered, nor rule out shared scene/layout/object, near-duplicate prompt, or other semantic leakage. The registry itself marks historical-viewing absence as not proven and earlier global prefix mappings as partially unresolved. Do not strengthen the claim to “never seen” or “held out.” The 600-task reservation is task-disjoint TRAIN evaluation metadata, not an external held-out set.

The old 6/120 non-light source failure count (or 7/127 including light) is descriptive only. It is not an iid estimate, prospective failure rate, or power/yield forecast for A96. In particular, old R19 contains zero pick-two tasks; there is no old pick-two outcome evidence.

## Evidence scope and input discrepancy

The live `NEXT_STAGE_DESIGN_TASKS.md` bytes hashed to `12e312be741343e9998f331bad5a9a3b5ddb09df4444a0e47fd0cf869214fdd5`. A related v2 draft contains a historical task-hash reference `51143107131e15b1771882461bd77200de14c726819a909de701b9f19fe3b188`; these are not equal. This audit follows the current task file's inspected contents and records the discrepancy rather than asserting the stale digest authenticates the current bytes. The coordinator-decision file matched its supplied SHA.

