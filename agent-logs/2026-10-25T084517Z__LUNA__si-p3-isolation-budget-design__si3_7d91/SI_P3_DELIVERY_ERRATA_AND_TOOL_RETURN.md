# SI-P3 delivery errata and tool-return attachment

Append-only correction record. No frozen SI-P3 design, metadata, partition, receipt, or hash-list file was edited.

## Path audit

The review reported three `input_bindings.json` paths missing `agent-logs/`. I re-read the frozen file and compared its entries with `metadata_audit.json` `inputs_before`/`inputs_after`. The reported omission is **not present in the current frozen bytes**: all four metadata input paths already contain `/research-notes/agent-logs/`, and each exact path/hash below matches the audit's actual path/hash. Thus this erratum does not invent a shortened prior path or claim that the frozen file was repaired; it records the verified path→SHA binding as requested.

Frozen `input_bindings.json` SHA-256: `88e1d3bb0df3887423533c3038f61c6da4ef84e415a5f1fb73cd91c5739bf553`.
Frozen `metadata_audit.json` SHA-256: `d34e70ec5056b82ca24f3b303861b61f7ab0f587bbeb17149008533802a83b3c`.

| Input | Actual path | SHA-256 |
|---|---|---|
| Known-use registry | `/home/lizening/research-notes/agent-logs/2026-10-25T065200Z__LUNA__si-p1-isolation-budget__caae4c/KNOWN_USE_IDENTITIES.json` | `98580db9a8322c52c87d6f30dcb75858b00f3b0ec6d3494a4a87923504ddca60` |
| Supported identity candidates | `/home/lizening/research-notes/agent-logs/2026-10-25T065200Z__SOL__si-p1-protocol-review__caae4c/P0_SCOPE_INCIDENT_SNAPSHOT/SUPPORTED_IDENTITY_CANDIDATES.json` | `a47101a6e2413695208a256b3174b4723c9c6fc1aef67bb08bb74b1c1b08b48d` |
| Identity file-presence metadata | `/home/lizening/research-notes/agent-logs/2026-10-25T054106Z__SOL__self-improvement-phase0__b1c48c/independent_identity_file_presence.json` | `5c386b5ad43192582ee7d77041e6551fb9fb55192dbfdfe2d79cf0ff164d5b11` |
| Corrected isolation-budget metadata | `/home/lizening/research-notes/agent-logs/2026-10-25T065200Z__LUNA__si-p1-isolation-budget__caae4c/corrected_isolation_budget_v2.json` | `17b8124496e402b98a5e2411cff704c926a40c0338b8ea5f8d804e20764fd6f7` |
| Common design constraints | `/home/lizening/research-notes/agent-logs/2026-10-25T084517Z__SOL__si-p3-controlled-experience-design__si3_7d91/COMMON_DESIGN_CONSTRAINTS.md` | `33e090877817c47a8fd4f046a3567fe06bc4498e52f343a3e3ca61dc21168647` |

## Receipt correction and returned text

The frozen `SI_P3_FAMILY_CAPACITY_ADDENDUM_RECEIPT.json` (SHA-256 `c5d100d5a8e1a0aa2f65682bab4f4630fc15b38dd9a892e6ad8dd7e82c42360c`) contains a **manual transcription**, not raw stdout. Its transcription has the family-key typo `pick_two_obj_and_place_in_recep` and does not preserve the actual `json.dumps(..., sort_keys=True)` output ordering. Do not use that `command.stdout` field as raw execution evidence.

Below is the stdout text returned by the actual `functions.exec` tool call that ran `python3 family_capacity_addendum_build.py` in `/home/lizening/research-notes/agent-logs/2026-10-25T084517Z__LUNA__si-p3-isolation-budget-design__si3_7d91`. It is copied from that tool response in this conversation, not reconstructed from the JSON receipt. The tool wrapper separately reported `exit_code=0`. There is no separate signed or independently persisted process transcript; this conversation tool return is the provenance source for the excerpt.

```text
{"candidate_counts": {"pick_and_place_simple": 419, "pick_clean_then_place_in_recep": 301, "pick_cool_then_place_in_recep": 194, "pick_heat_then_place_in_recep": 106, "pick_two_obj_and_place": 119}, "excluded_light": 2, "family_quotas": {"acquisition_train": {"pick_and_place_simple": 176, "pick_clean_then_place_in_recep": 127, "pick_cool_then_place_in_recep": 82, "pick_heat_then_place_in_recep": 45, "pick_two_obj_and_place": 50}, "engineering_development_train": {"pick_and_place_simple": 18, "pick_clean_then_place_in_recep": 13, "pick_cool_then_place_in_recep": 8, "pick_heat_then_place_in_recep": 4, "pick_two_obj_and_place": 5}, "final_evaluation_train": {"pick_and_place_simple": 221, "pick_clean_then_place_in_recep": 158, "pick_cool_then_place_in_recep": 102, "pick_heat_then_place_in_recep": 56, "pick_two_obj_and_place": 63}, "unallocated_nonlight_reserve": {"pick_and_place_simple": 4, "pick_clean_then_place_in_recep": 3, "pick_cool_then_place_in_recep": 2, "pick_heat_then_place_in_recep": 1, "pick_two_obj_and_place": 1}}, "output": "/home/lizening/research-notes/agent-logs/2026-10-25T084517Z__LUNA__si-p3-isolation-budget-design__si3_7d91/partition_proposal_family_capacity_addendum.json", "output_sha256": "be8710b348b4c90ad90171ea6a691d5bffc67d27c5ff74ac2869be2965929817", "partition_counts": {"acquisition_train": 480, "engineering_development_train": 48, "final_evaluation_train": 600, "unallocated_nonlight_reserve": 11}, "source_sha256": "fd145fe6abee849b44231e1d0c816aa65813be2b67c48715f7ce7d2635e98d23"}
```

Related frozen artifact bindings: builder `family_capacity_addendum_build.py` SHA-256 `8cee618729b3c74c5281b32fbf441a39119710d6316d0c44ed8cbe2b5c1fc305`; produced partition proposal SHA-256 `be8710b348b4c90ad90171ea6a691d5bffc67d27c5ff74ac2869be2965929817`. No writer script was rerun for this erratum. No scientific/model/environment/tokenizer/training call was made.
