# Excluded runtime inputs

No model weights, tokenizer cache, SFT adapter weights, ALFWorld dataset files, or credentials were copied into the provenance repository. These are pre-existing runtime inputs, not generated G3 outputs. Their immutable identities are referenced by the frozen R19-B1 baseline manifest (SHA-256 `d503f35ae913b137dfff091263bf29c38aa0ade2eea648dc45d7e6cf80da0973`), the successful production preflight receipt, and the frozen source-schedule/exclusion hashes. The preflight source-file manifest SHA-256 is `3b8674f8b2c529195652ad07022a67bfd511b61eff95c375a4c9edadb7b98930`.

All task-owned failure outputs and supervisor evidence are small text/JSON records and are included byte-preservingly in `g3_failure_bundle.tar.gz`, with individual original-file SHA-256 values listed in `g3_raw_evidence_hashes.sha256`. The independent review directory was separately authorized for inclusion and is included unmodified; its hashes are in `review_directory_hashes.sha256`.
