# Append-only correction: root hash inventory index entry

- Applies to publication commit: `3390d7c34c5b0fa655e57e5f3eb2f2852558080d`.
- Correction commit is additive; prior commits and payload files remain unchanged.

Post-publication validation found the root `FILE_HASHES.sha256` contained two entries for `INDEX.md`: it appended the new digest instead of replacing the previous mutable index entry. This addendum records the defect and the next commit corrects the inventory to contain exactly one current `INDEX.md` digest. The task payload, `RECORD.md`, commands receipt, and source package bytes are unchanged.

The first post-publish checksum comparison also used a locally transcribed SHA-256 implementation with a mis-transcribed round-constant table (one constant repeated and another omitted), so it emitted incorrect comparison digests. No mismatching-byte claim was published from that comparison. The corrected implementation was checked against the standard empty-string and `hello` vectors, and the original remote strings were then hashed and compared byte-for-byte to the prepared content. The package, metadata, and Git blob IDs matched; this was a verifier-code issue, not remote content corruption.

No source files, scientific inputs, or package contents were modified. The correction is limited to the task metadata inventory, its index pointer, and the root checksum inventory.