# SI-U1 evaluation engineering: observed successful check

Status: **OBSERVED_ENGINEERING_SUCCESS_AWAIT_INDEPENDENT_REVIEW**. The separately cleared engineering run `12558b4c8f23489b88cab1f9198a405f` used source `8532275932dabddc498c23a2b6d9a045647542f0`. Launcher PID 933894 and worker PID 933924 returned 0. The supervisor recorded no timeout or error and established process cleanup. The report is `COMPLETED`; this is an engineering result, not scientific evaluation.

The isolated engineering task completed one physical reset, one model generation of 831 input and 5 output tokens, and one valid mapped environment step. The event ledger contains each raw and normalized reset/step boundary and the generation return boundaries; its 24-event hash chain was independently checked. No recovery suffix, retry or scientific training was run.

The real supervisor device allocation was 104.42523151170462 seconds, or 0.029007008753251285 device-hours. Adding the prior failed evaluation engineering run gives 205.1257505407557 seconds, below the 600-second evaluation engineering ceiling. Across the two attempts the physical totals are two resets, one generation and one step, or three environment operations, matching the amended ceilings. Training engineering expenditure remains separately 250.73030943144113 seconds; the combined engineering time is 455.8560599721968 seconds.

Seven resource entries were recorded with zero allocator OOMs and zero allocator retries. At the recorded `model_closed` point, the worker still reported 8,519,680 bytes allocated and 20,971,520 bytes reserved. The subsequent worker and supervisor exited and process cleanup was established; the device-wide reading returned to the 14 MiB baseline. No claim is made that the in-process allocator was zero at `model_closed`, or that device-wide measurements establish process ownership.

The 36-member `RAW_EVIDENCE_PRIVATE.tar.gz` contains private engineering task evidence and all members were verified byte-for-byte against their original files; original pre/post hashes matched. Its SHA256 is `cf8167fc3775b0b403b2501017b172535ec3e7096b4f33046be0f3c97c137d61`. `INDEPENDENT_RUN_AUDIT.json` SHA256 is `b441df5598e6bdec21c3cc3e6f073e2ec1c6715fab89a66d5c02e429b6656590`. Independently recalculated model and P0 tree hashes were unchanged.

The raw record is local pending coordinated private provenance publication and independent audit. This result does not authorize or establish success of the scientific B/C training or evaluation.
