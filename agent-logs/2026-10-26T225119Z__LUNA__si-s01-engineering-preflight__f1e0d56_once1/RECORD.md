# SI-S01 engineering preflight — single released attempt

Status: `ENGINEERING_REJECTED_OR_STOPPED`. The one preflight-only release was consumed by a single authentic child invocation. No live engineering launch was released, and no retry is permitted under that release.

The release and its exact command directory were hash-verified before the attempt. The child ran with the approved pinned Python, `-I`, exact `preflight_argv`, `shell=False`, exact cwd, and the exact `inherit_environment=false` map. Child PID was 878318. It returned exit code 1 after 0.171004903 seconds.

Authentic stderr was: `{"status": "ENGINEERING_REJECTED_OR_STOPPED", "science_authorized": false, "exception": "ContractError", "message": "UTC timestamp must end in Z", "resource_evidence": null}`. Stdout was empty. The command was rejected on authorization timestamp syntax; this is not a successful static preflight and does not establish runtime readiness.

The child has exited. The proposed scientific output path and launch claim remain absent. The frozen source remains `f1e0d56a1be2a65876bbec5b8950fb76cda3eace` and clean. Release, command, authorization, proposal, and corrected-review hashes remained unchanged. No model generation or ALFWorld invocation was observed; the failure output has `resource_evidence:null`, so this record does not claim a successful zero-counter preflight receipt.

The release is consumed. No authorization timestamp was edited, no source or scientific input was changed, no second preflight/live command was run, and no automatic follow-on is permitted. Root must issue a distinct new preflight release after correcting the authorization if another attempt is wanted.

Raw child streams and the subprocess receipt are preserved next to this record. No shared provenance, index, source tree, or push was changed.
