# Independent read-only audit: third shared GPU admission observation

Raw JSONL SHA256 `09ca9a634cd71cd50bf4718adcc9040ad322bf7ac39ec19ba9086632813ec5e8`; script SHA256 `25ee5f2aae9b12c8708bee368291cf857712249992012a3017124ca593de1e70`. The script differs from the first independently reviewed script SHA `7d3b9bf223ce8beef8cba7feab90d0193593923f5057f06aa3fab7a0d14481fb` only in its output filename. This auditor did not invoke a GPU query, model, training or environment.

Sequence comprises STARTED, 16 samples indexed 0–15, RETURNED. All UUID values agree with authorization and CUDA visibility binding; all samples report 45,390 MiB free and 0% utilization. Query-start span is 60.000111496s, largest start gap 4.003959917s, longest query duration 0.067304055s. This meets the stated admission start-cadence and per-sample 30 GiB/20% thresholds. Terminal row records `PASS_SHARED_DEVICE_OBSERVATION` and no exclusivity. Coordinator reports observing outer exit 0; this is not an independently signed receipt and was not reproduced by the auditor.

These records establish only the bounded historical device-wide observation, not ongoing availability, exclusivity or a scientific execution clearance. Exact GPU hardware measurement instants, activity between queries and subsequent drift remain unknown.
