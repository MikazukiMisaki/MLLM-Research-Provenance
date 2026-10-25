# SI-P2 scope clarification — cap semantics and local mask

Additive clarification to the already frozen Luna SI-P2 handoff. This note
does not rewrite or rehash the original audit outputs and does not perform a
new source scan.

## Independent interpretation adopted

The coordinator interpretation
`CAP_AND_ROLE_INTERPRETATION.md` (SHA256
`964b5a31dcb78516c16c61780a91be677c55964a6c4e044c505b3d360349ee0c`)
controls the cap semantics for case
`R19_K1:R19-random-control-47bcdcad9c56a38ac146`: `token_cap_reached=true`
at EOS is not itself truncation when the authentic record says
`output_complete=true` and `status=valid`. The frozen production behavior
uses `output_complete=false` to classify truncation. This row has
CONTINUE=1 and K1=1, so it is a neutral success (`B_pool=1`, `C_student=0`),
not a rescue example. No rule is relaxed to preserve a rescue.

## Scope of Luna's frozen mask

The existing Luna JSON row records a local `stage1_legal_complete=HOLD` for
this case because Luna's branch-locator extraction did not recover a complete
Stage-1 record (`stage1_output_complete_and_nonempty=false`). That is a
limitation of this assigned identity/label and pre-Q-anchor audit's local
evidence join; it is **not** evidence that the authentic Stage-1 output was
truncated, that the case is scientifically invalid, or that `cap=true`
disqualifies it. The coordinator's exact original-record interpretation
supersedes that narrow local inference for this field.

Accordingly, all Luna-local `q_hist` and `q_pin` dispositions/counts—including
81 PASS / 90 HOLD—are preserved as a **local branch-index/available-evidence
mask only**, not as the final common Q_hist mask or a finding of data defects.
The final common quality mask is pending Sol Research's complete source/replay
audit and the coordinator's independent original-record review, then will be
joined onto Luna's unchanged 171-row parent index. No source expansion,
reparse, old script, validator, model, environment, training, or scientific
execution was performed for this clarification.

The original audit files and `FILE_HASHES.sha256` remain byte-for-byte
unchanged. This addendum is outside that already frozen hash list by design.
