> Redacted publication copy: owner-private Drive object identifiers removed. Original SHA-256: `91aa8530d2e6fb3f1b4feddd0d092768c6a434cb066538941acaa57aa0130019`.

# Private raw evidence backup receipt

The original C-low training outcome remains `INNER_COMPLETED_OUTER_UNKNOWN_NO_RETRY`; this backup changes no execution status or evidence bytes.

The 17-file original private evidence archive excluding model weights was uploaded to the owner's My Drive root as `SI-C-low-raw-evidence-324ae788.tar.gz`. Drive returned file ID `[OWNER_PRIVATE_ID_REDACTED]`, size 153,646 bytes, `shared=false` and an owner-only permission. The raw uploaded file was fetched back through the authenticated connector; its independently computed SHA-256 is `324ae788cf55ef971093c382ffca5ccd5a215e48a258526063868828af5be596`, identical to the local archive. The archive contains 17 regular entries, 1,459,967 uncompressed bytes, with no absolute or parent-traversal archive paths. It includes sensitive runtime details and should remain private. No model adapter or base weights are included.

Before upload, a bounded scan found no private-key headers, common GitHub/Hugging Face/cloud access-key patterns, or bearer-token patterns. Pattern scanning is not a guarantee that an archive contains no sensitive information; private owner-only handling remains necessary. Raw training evidence is now both local and owner-private in Drive; curated audit records remain separately in the private provenance repository. The locally stored model product is not claimed backed up by this receipt.
