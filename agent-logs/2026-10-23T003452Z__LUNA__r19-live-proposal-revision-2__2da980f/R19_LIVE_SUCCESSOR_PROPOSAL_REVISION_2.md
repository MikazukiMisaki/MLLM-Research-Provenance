# R19-B1 live successor proposal — revision 2

Status: `PREPARATION_ONLY`; **not ready to launch**. This immutable revision supersedes, but does not edit or erase, the prior Luna proposal and bindings identified below. It corrects three metadata/evidence-domain defects identified in Sol's exact-proposal review. It does not change scientific code, tests, protocol, gate, inputs, argv, environment, output identity, record identity, quotas, budget, or authorization state.

## Supersession and review basis

- Prior proposal SHA256: `c7b1a59fcb1ec2d968ac691efe4d3a3a6ddf523beb9df24d89cc902bca204967`.
- Prior bindings SHA256: `9f10793c0e73ac70c861c0ef8a8d2babbbe878f5aba167a5b4c61f26d2e05aa2`.
- Exact-proposal review: `/home/lizening/research-notes/agent-logs/2026-10-23T002952Z__SOL__r19-exact-live-proposal-review__2da980f_5a72b1/exact_proposal_review.json`, SHA256 `afe215c3785b128f4d9c1a3be4840cf524b7712a6cd7eb3cfca2b060ab142916`.
- This revision's complete correction task: SHA256 `c331829bb2ecf98c7d829a893a1d715ad72cb89199948a0d54f49a28f05f0f84`; corrected requirement values: `4082394774d072e8c7f7d5f75097856ca6fe64298d7e58efd0f5aa2308ea6bf9`.

## Corrected bindings

The new [bindings.json](bindings.json) fixes only the three reviewed metadata defects:

1. **Predecessor identity:** the four raw artifacts now bind to actual run `3d1ccea7e97f4727abf8e216ac6ec498`, implementation `bf31f3da430ffc35bd17fc380e1752adce6d1467`, exit 1, and the restart authorization. The older `45eda8…`, `7e1fc0…`, `e71147…` trio is not reused as 3d1 evidence: read-only comparison confirms those bytes identify separate run `a0de515d7e104101bf8157175ea3d995` on source `ef2328f06256054a6b71c6dc4bdc74dab3a1d3d9`, with no event ledger. The authentic 3d1 event/manifest/registry/branch and cost evidence remains unchanged.
2. **Quota semantics:** frozen eligible quotas are `failure=30`, `success_control=15`, `random_control=15`, matching both protocol and restart authorization. Candidate queue targets (`60/30/30`) are separately identified as queue sizes, not eligible quotas.
3. **Runtime digest domains:** historical `runtime_manifest.json` and `runtime_manifest_preload.json` each have explicit path, raw-file SHA256, and canonical-object SHA256. The frozen pure preload expectation `64ebf466…` is a distinct identity. Future live post-load runtime is explicitly `NOT_OBSERVED`.

`correction_evidence.json` contains actual-path raw hashes and parsed identity/value comparisons, not only PASS labels. It also binds the model aggregate specifically to the actual preflight receipt's `model_files_sha256` field. The original proposal, original binding JSON, Sol review, review inputs, and scientific artifacts remain untouched.

## Invocation and authorization state

The prior exact child argv, supervisor argv, and environment plan are byte-identical copies in this revision. Their previously reviewed absent future output/record paths remain unchanged; they were rechecked absent and not created. Canonical/raw hashes are in [RECORD.md](RECORD.md). No new live UUID is present. There are still zero supervisor, preflight, model, ALFWorld, G2, G3, or G4 invocations for this task.

- Independent exact-proposal re-review: **PENDING**.
- Separate independent live-launch clearance: **PENDING / NOT GRANTED**.
- Fresh explicit user scientific authorization: **PENDING / NOT GRANTED**.

The consumed Phase1 preflight release and any historical `APPROVED_BY_USER` markers are not reusable authorization. This revision does not permit execution or a repeat preflight.
