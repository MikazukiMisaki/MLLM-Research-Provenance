# SI-E2 proposal revision 2 — binding correction only

**Status:** `PROPOSAL_REVISION_2_PREPARED / ROOT_REVIEW_PENDING`; no authorization or launch release.  
**Scientific source:** unchanged; candidate remains `dfc00e49d1ef4d48453d2331507429f8a0c7bbc5`.  
**Execution:** none. No model, CUDA, ALFWorld, environment, supervisor, preflight, or science call.
**Revision-2 completion UTC:** `2026-10-25T13:51:22Z`; the revision-specific inventory was generated and every listed SHA256 verified immediately afterward.

## Correction and evidence

The root finding `proposal_data_root_finding.json` is bound by SHA256 `02cabec3c16693c3f924ef4b45bf1771f3a39a96d0170bda54abdb0e784af96c`. It identifies the conflation between the original ALFWorld root and the YAML's TRAIN dataset path.

The authentic original G3 launch context is `/home/lizening/research-notes/agent-logs/2026-10-23T005510Z__SOL__r19-authorized-g3-monitor__2da980f_eea6b8/launch_context_observed.json`, SHA256 `399137330d5dfaccdd8734f7c39b219cfd7040808649e6090af8c9b733af39ac`. It binds completed live run `260422ac02bd42a8b2929d7ef240526b`; the recorded `effective_environment.ALFWORLD_DATA` and `--data-root` are both `/home/lizening/alfworld_data`.

Revision 2 changes only these proposal bindings:

- `environment.data_root` → `/home/lizening/alfworld_data`.
- Proposed environment `set.ALFWORLD_DATA` → `/home/lizening/alfworld_data`.
- The environment rationale now explicitly distinguishes this original root from YAML `dataset.data_path=/home/lizening/alfworld_data/json_2.1.1/train`.
- The proposed new factory restriction remains limited to effective discovery of the single historical task, before constructor entry; it is a design constraint, not executed behavior.
- The argv revision points to the new proposal path and pins its raw SHA256. Its authorization hash remains null/pending and `launch_allowed=false`.

No source repair is required. The initial proposal, environment, and argv bytes remain untouched and are identified as a superseded draft in `REVISION_2_BINDINGS.json`. Revision 2 raw/canonical hashes and authentic build/verification receipts are in that binding file and `REVISION_2_BUILD_RECEIPT.json` / `REVISION_2_VERIFY_RECEIPT.json`.

## Boundary and accounting

No authorization was authored; no runnable command was constructed. No model/environment/scientific invocation occurred. Existing output and authorization absence evidence remains in the prior `final_proposal_state_receipt.json`; this correction did not create either path. No code, YAML, source data, old proposal, old receipt, or shared provenance/index was changed. No commit/push.

During patch authoring, two newly created helper files briefly landed at an adjacent path missing the `agent-logs` segment. They were moved into this task's own directory; the duplicate receipt index at that exact sibling path and the now-empty sibling directory were removed. No pre-existing file was touched; the final own-directory inventory covers all retained files.
