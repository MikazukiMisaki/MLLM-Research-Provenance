# Independent read-only audit: fourth shared GPU admission observation

Raw JSONL SHA256 `b3f5d4b5f08039efe5003c0d7f372da0463b1dbadbc3bce8deed3b89748725b4`; sampler SHA256 `10610eab52367c29308688ae24d2ffa718def1121594055319d49e98f5c031ac`. The sampler differs from the first independently reviewed script only in its output filename. This auditor did not invoke a GPU query, model, training or environment.

Sequence comprises STARTED, 16 samples indexed 0–15, RETURNED. All UUID values agree with authorization and CUDA visibility binding; all samples report 45,390 MiB free and 0% utilization. Query-start span is 60.000118748s, largest start gap 4.003953314s, largest completion gap 4.004922587s, and longest query duration 0.068961908s. This meets the stated admission cadence and per-sample 30 GiB/20% thresholds. Terminal row records `PASS_SHARED_DEVICE_OBSERVATION` and no exclusivity. Coordinator reports observing outer exit 0; this is not an independently signed receipt and was not reproduced by the auditor.

These records establish only the bounded historical device-wide observation, not ongoing availability, exclusivity or a scientific execution clearance. Exact GPU measurement instants, activity between queries and subsequent drift remain unknown. Freshness has to be independently rechecked at the actual authorized dispatch.
