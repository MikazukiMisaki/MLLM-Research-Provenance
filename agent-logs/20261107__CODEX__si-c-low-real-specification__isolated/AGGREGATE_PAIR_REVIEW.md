# C-low protocol and training-manifest aggregate review

Status: **conditional data and schedule consistency review only**. This is not a protocol-and-pair gate decision, an approval of any unreviewed source revision, a preflight, a training authorization or an evaluation decision. It does not establish provenance correctness, target-action semantic quality, evaluation isolation or generalization. The candidate receipt continues to report an unreviewed status.

The review privately parsed only the two expressly permitted historical development-training datasets, the two historical data-review documents referenced by the candidate manifests, the old and new training manifests and the old and new protocols. The old learning-rate and schedule-binding implementations were inspected from the named historical Git object without importing the training package. It did not inspect held-out or protected evaluation inputs, or invoke a model, tokenizer, environment or preflight. No row content, sample identifier, task identifier or input path is reproduced below.

## Aggregate checks

| Check | B | C |
|---|---:|---:|
| Dataset SHA256 matches candidate manifest and original data-only review | yes | yes |
| Original review SHA256 matches candidate manifest | yes | yes |
| Original and candidate manifest SHA256 match their candidate receipt bindings | yes | yes |
| Unique rows | 312 | 312 |
| Parent groups | 78 | 78 |
| Rows per parent | 4 | 4 |
| Original review counts: rows / parent groups / exposures | 312 / 78 / 1,248 | 312 / 78 / 1,248 |
| Four 312-row epochs each contain every row once | yes | yes |
| Reconstructed frozen shuffle matches all 1,248 candidate exposures | yes | yes |
| Schedule row/group bindings and per-row/per-group exposure counts match actual rows | yes | yes |
| Parent-family aggregate counts match protocol | yes | yes |
| Recomputed full five-field schedule SHA256 matches historical data review | yes | yes |

The earlier data reviews are scoped to `PASS_DATA_ONLY`. Their exact bytes still bind the same dataset and complete schedule under the candidate manifests. That supports carrying forward their prior **data-only** decisions for these unchanged inputs; it does not enlarge their original scope, establish a new pair/protocol approval, or independently re-adjudicate source lineage and labels.

Candidate dataset SHA256s: B `5ae321d250a5607337af8c7cbba6a4372f60805c20811ad76f0617a50ec93350`; C `0735422fbeb3285256290ef0ec81923d5954b370b341b6a76a293c205804628d`. The recomputed schedule hashes are B `e6c899a2640d382886c4feb622a048604839bcafa68b6b8714cc01f307a98266` and C `5a5d919fa6ba7fc3f24b7572a91735874af0de44fa335341c48a3b94e034076c`. These reproduce the historical production serialization of the five bound schedule fields; they are integrity evidence, not proof of statistical or semantic independence.

## Exact differences and rate values

The old protocol SHA256 is `f72e1de1b27659f0c0cb187c276c7c60483af089d4a756fbe3c3d7819dcc5698`; the candidate is `96e4ac83f9188678a4c820e4f50c9b6b5e74e7caf5a2bbe9ca272ee93614a07e`. In a type-sensitive comparison, the protocol top-level changes are the protocol identifier, training configuration and LR-definition array; all other top-level fields and LR-definition metadata are identical. Within training configuration the sole changed field is the rate, from `1e-4` to `5e-5`. In each manifest the only changed top-level field is training configuration, and it exactly matches the new protocol with types preserved; old manifests each exactly match old protocol training configuration. Historical and candidate base/P0 digest bindings are identical within each arm and between arms; actual weights were not rehashed in this review.

The 78 candidate LR values match the historical production function exactly for the candidate config; maximum absolute discrepancy was zero. Compared to half of the *stored historical* LR vector, 16 values differ in floating-point representation, with largest absolute discrepancy `2.710505431213761e-20` and largest relative discrepancy `8.775328569551876e-16`; all pass `rel_tol=1e-12`, and the historical gate's `rel_tol=1e-14, abs_tol=1e-16` tolerances. This records the observed numerical distinction rather than describing the two stored vectors as bit-exact scalar multiples.

Candidate B/C manifest hashes are respectively `a80a6a540963dd84bf3c006a7bf61b4e5f4a5c1ea9fdc0050b3bce55ef7152bf` and `a04283f822cb0bb008200d2d0551d38e0bf4de1b6113682c176a0788f089a785`. All comparisons above are against historical bytes and the candidate output receipt; a future exact source revision, runtime, actual input availability and full resource and evaluation controls still require independent review. In particular this document sets neither `PASS_PROTOCOL_AND_PAIR` nor any launch/preflight decision.

## Scope deviation

During initial manifest-structure inspection for this review, a recursive schema printer emitted the keys of one grouping dictionary. Those keys were identifiers from the expressly permitted development-training parents. This violated the requirement to output only aggregates and hashes; the identifiers are not repeated in this record. It is not evidence that held-out or protected evaluation data were accessed. The tool transcript containing those keys is private and must not be uploaded; later output was restricted to aggregate booleans, counts, hashes and non-identifying configuration differences. No additional files containing those keys were created by this reviewer.
