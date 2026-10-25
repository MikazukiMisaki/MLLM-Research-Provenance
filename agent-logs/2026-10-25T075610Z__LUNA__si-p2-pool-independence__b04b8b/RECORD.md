# SI-P2 Luna task record

## Frozen task and scope

Read and SHA-verified the unique assignment, common rules, and fixed parent
cohort manifest. The audit covers exactly the 171 frozen rows (24 R4, 48
R10_OSR, 60 R16_OSR, 39 R19_K1). R19 is K=1 only. It uses Python standard
library parsing and writes only in this unique Luna directory. No model,
ALFWorld, training, tokenizer, replay, project analyzer/validator, pytest,
G2/G3/G4, preflight, schedule generation, other agent, shared INDEX, commit,
or push was used.

## Frozen inputs

- Task: `LUNA_TASK.md`, SHA256 `76e8880f83dffe40857eb78457dc48766c8ca74bedea46d5f985e4bc7e94cbe7`.
- Rules: `COMMON_AUDIT_RULES.md`, SHA256 `ab5e3afe8bb1e65ae1473254810ba56dfa769cefbd0952d0b2a0bdb32368ea69`.
- Manifest: `PARENT_COHORT_MANIFEST.json`, SHA256 `a3e2548e89280d150cbe83cceca632f9f91275ede0a4a9d89133e53691826078`.
- All four source branch files were full-file hashed against the manifest and
  every selected JSONL row was checked against its exact source line and raw
  row hash, including the line terminator.
- The R19 event ledger was SHA-pinned before and after its referenced-event
  scan. Runtime, known-use, P1 cost, and the previously audited fixed-eleven
  evidence were also byte-hashed before/after.

## Outcome

`POOL_IDENTITY_AND_CAPACITY.md` and `pool_identity_audit.json` preserve the
row-level dispositions, pre-Q label-blind anchor plan, source/family counts,
fixed-eleven destinations, physical alias evidence, Q_hist/Q_pin capacity,
and all source hashes. Primary Q_hist has 81 passing rows / 80 unique tasks;
after the fixed task anchor and exact pair dedup, 80 task/input-target pairs
remain (B=51, C=5, B\C=46). Strict Q_pin sensitivity retains 35 task pairs
(B=28, C=1). All 171 fixed identities are already present in the known-use
union; this is not a clean/held-out certification and does not establish
training eligibility.

Historical cost is carried forward without recomputation: R19 cumulative
5,142 generations and 7,949 environment operations including resets (the
predecessor 177/342 is already included). Historical SFT costs and unknown
units, plus the hypothetical 150E/153E formula, are separated in
`COST_LIMITS_NOT_EXECUTABLE.md`; no budget or execution is authorized.

## Real command receipts and final integrity

The final direct invocation `python audit_pool.py` returned 0. Four earlier
read-only development-command/check failures (bad manifest locator, newline
omission in row hashing, a diagnostic path typo, and missing R19 target-hash
projection in an output consistency check) are explicitly retained
with real return codes and failure descriptions in `commands.log` and
`execution_receipts.json`; no old source row was edited to work around them.
The authoritative output reports 171 rows, 169 task identities, Q_hist
81 PASS / 90 HOLD, Q_pin 35 PASS / 4 HOLD / 132 legacy strict-pin HOLD, and
2,167 referenced event IDs. The machine audit records its full before/after
input and ledger hashes.

Final file hashes are in `FILE_HASHES.sha256` (manifest excludes itself).
This is a frozen read-only audit handoff, not an independent review PASS,
training approval, clean-data claim, new schedule, or scientific execution
authorization.
