# SI-P2 — same-pool identity and capacity audit

Status: `READ_ONLY_HISTORICAL_EVIDENCE_AUDIT__NOT_TRAINING_AUTHORIZATION`.
Scope was the frozen 171 parent rows only (R4 24, R10_OSR 48, R16_OSR 60,
R19_K1 39). No new task, schedule, model, environment, tokenizer, replay,
training, project validator, or test suite was run. R19 contributes K=1 only.

## Result under the frozen common rules

| Fixed stage | Rows / distinct task identities | B_pool | C_student | B\C neutral success | Recovery failure/nonrescue |
|---|---:|---:|---:|---:|---:|
| RAW | 171 / 169 | 99 | 11 | 88 | 72 |
| Q_hist | 81 / 80 | 52 | 6 | 46 | 29 |
| Physical-alias dedup | 81 / 80 | 52 | 6 | 46 | 29 |
| Predeclared task anchor | 80 / 80 | 51 | 5 | 46 | 29 |
| Exact public-input/first-target dedup | 80 / 80 | 51 | 5 | 46 | 29 |

The last stage contains 80 distinct public projections, 53 distinct first
target-command hashes, and 80 exact input-target pairs. These are historical
candidate counts, not verified SFT rows/tokens or an approved training pool.
Q_hist retains only R10_OSR (46 rows) and R19_K1 (35); all retained rows are
already in the known-use union. No legacy physical reuse was inferred from
similarity. No shared R19 recovery-generation ID groups were found, so the
physical-dedup stage removed zero rows.

By source, RAW rows / B / C / neutral are R4 24/12/1/11, R10_OSR
48/25/5/20, R16_OSR 60/31/4/27, and R19_K1 39/31/1/30. After Q_hist,
R10_OSR is 46/24/5/19 and R19_K1 is 35/28/1/27. After fixed task anchoring
and exact dedup, R10_OSR is 45/23/4/19 and R19_K1 is 35/28/1/27. The complete
family-by-source and every intermediate-stage table is in
`pool_identity_audit.json`.

Across the 80 Q_hist task anchors, no identical public projection had
different first-target commands (zero ambiguity groups). The machine audit
retains the explicit comparison; no target was repaired or excluded on this
basis.

## Quality holds and identity limits

- R4: 24/24 HOLD because the legacy row contains replay/equality hashes but
  not the complete independently recoverable source public prefix.
- R10_OSR: 46/48 PASS; two HOLDs include one incomplete full-source projection
  and one source-stage legality/target-transition evidence gap.
- R16_OSR: 0/60 PASS. Full independent source-prefix values are absent from
  these rows; three also lack complete/legal stage evidence. Correct `r_osr`
  and `r_continue` labels and their recorded stop traces were used.
- R19_K1: 35/39 PASS; three HOLD for missing replay/transition binding and
  one for incomplete stage-one evidence. The event join uses the original
  ledger, source trajectory, prompt, transition, and continuation references.
  It checks source action-before snapshot, public goal/observation/H4/ordered
  map, exact frozen prompt-instruction prefixes, stage completion, selected
  bare ID to executed command, and stop/label references.

There are two same-task/multiple-prefix groups and no cross-stage task groups
inside these 171 identities. The pre-Q anchor list assigns a label-blind hash
key to every parent candidate before selection. Its labels are descriptive
only and never affect order. The fixed 11 historical target dispositions
were: six Q_hist-pass records, of which five survive the task anchor/exact
pair stage; five are Q_hist HOLD. The sixth passing record is not selected
because its same-task peer has the smaller frozen anchor. Full case-level
dispositions are preserved in the machine JSON.

Explicitly, retained: R8-F02/F20/F21/F22 and R19 failure
`b3ab21b8e193f6adf6ff`; Q_hist-pass but not anchored: R8-F23; Q_hist HOLD:
R4 R2-F01 and R16 R15-F01/F22/F23/F25.

All 171/171 row identities occur in the prior 2,612-identity known-use union.
The fixed rows have zero direct overlap with the registered `expert_train`,
`expert_offline_validation`, or `online_development` lists; they do overlap
prior recovery/source and completed R19 identities. The registered split
presence differences (train 1,141; valid_seen 0; valid_unseen 74) are
presence/difference metadata only and explicitly do **not** certify clean or
held-out data. No full historical prompt/target corpus hash proves that a
candidate has never been trained on. Semantic near-duplicate exclusion was
not inferred.

## Q_pin sensitivity and sufficiency

Q_pin is a strict subset: 35 rows pass (all R19 rows already passing Q_hist),
four R19 rows remain held, and all 132 legacy rows are held because exact
historical weights/tokenizer and loaded adapter-role receipts are not jointly
bound. Applying the same frozen dedup sequence to Q_pin gives 35 task/input
pairs, B=28, C=1, neutral B\C=27, and recovery failure/nonrescue=7. This
does not replace Q_hist or make the candidate source clean.

The largest observed Q_hist task-anchored, exact-pair pool is 80 distinct
task/input-target pairs; 51 are B successes and only five are C successes
(recover success with CONTINUE failure). This demonstrates mechanical label
separability, not that an equal-source/equal-token comparison is feasible or
causal. C is concentrated in R10 (four) and R19 (one); Q_pin has one C. The
unknown independently sourced clean pool, exact training serialization,
target-token counts, duplicate-history coverage, and budget remain decisive
unknowns. No minimum-N rule was invented; current training feasibility
remains unestablished.

## Frozen inputs and side effects

The task/rules/manifest hashes were verified against their supplied values.
Input file sizes and SHA256s before and after are recorded in the JSON; all
checked inputs remained unchanged. The R19 event ledger before/after SHA256
is retained there as well. The raw event journal was indexed only by the
event IDs referenced by the fixed K=1 rows. Historical P1 expert-repeat
occurrence count 127 is preserved as a prior audit finding; no row was
reconstructed or regenerated here.

No science calls occurred: model=0, environment=0, training=0, tokenizer=0,
policy replay=0, project validator=0, pytest=0.
