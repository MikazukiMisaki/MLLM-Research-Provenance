# C-low exploratory preparation: independently reviewed provenance

This record is a sanitized snapshot of a preparation and review stage. It is not a launch clearance, evidence of completed training, a scientific result, or a claim of model improvement. At this review checkpoint, no new production preflight or live training had been run. This statement does not assert the state of future work.

## Scientific scope

The proposed C-low continuation changes the learning rate from 1e-4 to 5e-5 and the derived schedule, maintaining the previously reviewed development data and remaining training recipe. It trains only a new C candidate. The existing C product and P0 are descriptive anchors; the new B manifest is a gate binding, not a trained B-low product. Reused development data are not an independent test set; a future success-rate comparison requires separately reviewed task isolation, evaluation, and uncertainty. The proposed self-authored development cases are not held-out evidence. The accompanying declaration specifies the exploratory limits and does not authorize evaluation.

## Independently reviewed materials

The separately issued software and pair review decisions are `PASS_SOFTWARE_ONLY` and `PASS_PROTOCOL_AND_PAIR`, respectively, limited to the declared source and exact input bindings. They are not production execution acceptance. The source reviewed as a local Git object was `9bbaa12c2d8177a60ec5a74ed2f970ef29a57bce`; a GitHub fetch for this commit returned HTTP 422, so remote availability is not asserted. A complete local Git archive was retained privately without upload or archive-wide content review: SHA256 `818fbacba5c437be77fc267da288a2a6508c196778726b99a7d8da3fe040038e`, 13,198,060 bytes. A digest is an integrity identifier, not independent proof that all archive contents are safe or reproducible.

Private inputs and original review artifacts remain private. Their recorded byte hashes are listed to make later controlled verification possible, not to reveal sample identities, paths or contents:

- New C manifest: `a04283f822cb0bb008200d2d0551d38e0bf4de1b6113682c176a0788f089a785`.
- New B manifest: `a80a6a540963dd84bf3c006a7bf61b4e5f4a5c1ea9fdc0050b3bce55ef7152bf`.
- New protocol: `96e4ac83f9188678a4c820e4f50c9b6b5e74e7caf5a2bbe9ca272ee93614a07e`.
- Independently issued C software review: `3c9d581f25be6d11e5d0b513d749228b11cdcb6beb55e1da935442317961347c`.
- Independently issued pair review: `7af7e6bae8177e21d2cd8baef0e4ba2bad86ac347e0d9b84317e5d1e9ca70fa3`.
- Full independent review narrative: `7f7369f12964c576e05be977bf125580e8445e99a7a7ce245536e48d07acd24b`.
- Independently reviewed private authorization builder: `49c80df2a4f6605a407344bd72d883f2915ae72972da562a712c30753881ea21`.
- Private full gate and resource review narrative: `0cbb61e14bdf5e2f20f0fe9dc7b06414485fa9b7c49923a4a8c3a9c20c66183c`.

The software/pair review used isolated pure source helpers and reviewed actual input bindings; it did not run the production gate or train a model. The independent gate review was source-only; no production preflight, training, model, tokenizer, CUDA or environment was run. A draft builder was corrected to use Z-terminated UTC timestamps and bind the exact independent review hashes. Its reviewed bytes construct fresh run identity and paths; this static review is not a test of any subsequently created authorization.

## Operational conditions and limitations

The protocol retains its original 5,400-second inner limit. The proposal uses a separately supervised 1,800-second outer operational limit which can stop an otherwise valid run. The gate requires an exact fresh authorization and a separate clearance bound to an actual preflight; historical launch clearance is consumed and cannot be reused. Monitoring and process cleanup, including CLI work before the inner supervisor and descendants in separate sessions, must be independently reviewed before use. A draft external guardian had a demonstrated synthetic failure in direct-child cleanup; its real entry was disabled and the failure requires repair and review. Incomplete operations, actual process-cleanup uncertainty, sampling gaps, concurrent storage writes, and unmeasured physical I/O must remain UNKNOWN.

The exploratory resource declaration replaces a previously unestablished complete native/mmap I/O meter and hard quota prerequisite with documented source-based planning and sampled stop conditions. These are not hard physical disk-read or filesystem-quota guarantees. The roughly 76.3 GiB known-shard live-stage sizing reference is not total I/O; actual physical I/O and all unobserved tails remain UNKNOWN. Shared-device observations are not exclusive reservations and device-wide activity must not be attributed to this experiment without evidence.

The repository publication contains only this sanitized review, the path-free exploratory declaration, and their checksums. It excludes private authorization, manifests, datasets, original code, source archive, execution transcripts, and machine-specific paths.
