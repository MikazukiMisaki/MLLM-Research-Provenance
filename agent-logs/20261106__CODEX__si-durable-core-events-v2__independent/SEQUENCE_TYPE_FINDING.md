# Synthetic counterexample: Boolean sequence number

After the v2 fake-edge suite, a separate temporary-file probe changed the first event's sequence from integer zero to JSON `false`, recomputed that event's canonical digest and invoked the verifier without an external anchor. Python compares `False == 0`, so v2 accepted the malformed event as `CHAIN_UNANCHORED`. This is a schema-validation defect; no real model, GPU or environment was used, and it does not imply any actual ledger was corrupted.

The v2 candidate should not be used as a complete event-schema validator. A new version should require `type(sequence) is int` in addition to value and order checks, retaining the earlier formatting and raw-file hash checks. A trustworthy external head and raw-byte digest remain essential and cannot be supplied by the event file itself.
