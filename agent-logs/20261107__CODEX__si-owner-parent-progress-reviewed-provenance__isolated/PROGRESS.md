# Self-improvement research: execution checkpoint

## Long-term objective

Test whether a small ALFWorld agent can improve task success through self-imitation. Preserve the frozen P0 and training provenance; separate development observations from defensibly independent confirmation. Establish task isolation, statistical precision and complete resource accounting before claiming generalization.

## Real work completed

One exploratory C-low continuation was run from the existing P0 product with learning rate 5e-5, compared with the historical C-high learning rate 1e-4. It used 312 development rows, four passes, 1,248 completed microbatches and 78 optimizer updates. The training result and inner supervisor report completion and worker return 0. The independently computed final adapter tree SHA-256 is `1cc6c153138e58ca1bda44c0682757d68649c11190258854e7ee2454df816669`.

The outer guardian recorded an observation error and `STOP_FAILED_OR_UNKNOWN`; the coordinator observed exit 1. The correct overall classification is **INNER_COMPLETED_OUTER_UNKNOWN_NO_RETRY**. The observed outer failure cause and any unseen process tail are unknown. The result is not an overall supervised PASS, and the original attempt was not repeated. Inner elapsed allocated-device-clock time was about 0.2583 hours, not exclusive device time or energy. No success-rate evaluation or held-out test has been performed for this adapter.

Original private logs and the model product remain local. A 17-file private raw evidence archive, excluding model weights, has SHA-256 `324ae788cf55ef971093c382ffca5ccd5a215e48a258526063868828af5be596`. Curated records were uploaded to the private provenance repository, whose remote main was independently observed at `93e9b947b4c24f366c501c2fee2f9d7fde120127`; the raw archive and weights are not represented as remotely uploaded. Independent postrun audit SHA-256: `3f505e64f9413492b9492ee9c43b4c8f30d1db37925790f46a0d0ab564b5e0f7`.

## Next experiment and unresolved work

The proposed B/C × P0/C-high/C-low run contains only six development episodes and would test feasibility, not establish task-success improvement. The two exposed cases yield a 50-percentage-point paired resolution, and the fixed order puts C-high second on both cases. A unit-level repair at commit `c90878eda6f131f96149bde8a546b0bb538637dd` passed limited independent review, including a read-only check of the original outer evidence; this is not six-unit approval. The prior commit `1bf7a19bcd9894eb9e1bffdd864bec7ddfba7432` failed real Markdown evidence binding and is superseded. Existing reservation accounting is not connected to the real unit worker and can admit generation before initialization in a synthetic reproduction. A separately reviewed owner, actual lifecycle accounting, common prompt filter, resource boundaries and documented handling of the C-low outer UNKNOWN remain required before real comparison.

Currently no sufficient independently held task pool or independent custodian has been established. Under hypothetical independent paired-task probabilities of 0.15 improved and 0.05 worsened, about 168 independent parents are needed for 80% power using a two-sided exact conditional test at 5%; this is a planning assumption, not an observed effect. A proposed finite task-supply pilot and graph/lineage tests are preparatory designs, not an existing independent evaluation set.

## Evidence

- `INDEPENDENT_POSTRUN_AUDIT.md`: SHA-256 `3f505e64f9413492b9492ee9c43b4c8f30d1db37925790f46a0d0ab564b5e0f7`.
- Exact-commit unit review: SHA-256 `0064938968fa21dc4a0e278bfdc1d8c2d01aa4b778bcb2cd6918bf28ba5fb3fb`.
- Independent task-supply design: SHA-256 `53f9e064bc7e7ce339c17a92c7bc803d70a0f98b5bd65840672263e51ef33c30`.
- Guardian diagnostic candidate is software-only; its limited synthetic review does not fix the historic UNKNOWN or approve another run.
