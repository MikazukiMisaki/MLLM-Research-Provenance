# Research evidence: self-generated experience and bounded recovery

*Aggregate evidence from completed studies; exploratory results, not a new experiment. The original records are access-controlled.*

### SI-U1: continuation from an expert-trained policy

A is the original expert-supervised P0 policy; B continues training on expert examples; C continues separately from the same P0 on selected actions from P0's successful episodes. Each continuation was trained once with one training seed. On the same fixed set of **82 TRAIN tasks**, A completed **65**, B **68**, and C **67**. These tasks are not certified held out or scene-independent.

| Prespecified paired contrast | C wins / losses / ties | Net difference | Holm-adjusted p |
|---|---:|---:|---:|
| C − A | 3 / 1 / 78 | +2/82 (+2.44 percentage points) | 1.00 |
| C − B | 3 / 4 / 75 | −1/82 (−1.22 percentage points) | 1.00 |

A win means C succeeded where its comparator failed; a loss means the reverse. The analysis is **inconclusive**: a non-significant result does not establish equivalence or harmlessness. B and C differed in source tasks, states, actions and selection, so the result does not isolate the causal effect of data origin. Confidence intervals and population inferences require assumptions about task sampling; one training seed does not establish across-seed reliability.

### R19: a separate exploratory recovery study

R19 studied the original P0 actor, **not** the B or C trained policies. It recorded **127 TRAIN source episodes**, **39 recovery attempts** and **36 eligible prefixes**; the 39 attempt-level branch records contain 183 K-labelled result entries, including aliases and entries for ineligible attempts; these entries are not independent samples. Of the 36 eligible prefixes, 6 were failure-stratum cases and 30 were controls.

**CONTINUE** means the original actor's recorded no-intervention source suffix, reused after identity and replay checks; it is **not** a newly generated rollout. For a recovery branch, the actor resumes only if the branch is nonterminal, and the original total horizon of 50 environment actions is preserved.

| Recorded comparator | Successes among 36 eligible prefixes |
|---|---:|
| CONTINUE | 30/36 |
| Best fixed tested duration, K2, selected retrospectively on these same 36 prefixes | 30/36 |
| Hindsight choice among K1–K5 | 32/36 |

The 2/36 difference between the hindsight envelope and K2 is **5.56 percentage points** on this same development sample. Both extra hindsight successes were already successes under CONTINUE; they are not additional rescues over the no-intervention baseline. The hindsight choice uses outcomes unavailable to a live controller. No adaptive stopping policy or held-out success gain was demonstrated.

K2 and CONTINUE averaged approximately **9,854** and **7,470 logical tokens per branch**, respectively; this is a per-policy accounting estimate, not the physical research bill. The completed G3 run physically spent **4,965 generations and 7,607 environment operations**, including resets. With earlier charged work, the R19 campaign total was **5,142 generations and 7,949 operations**. Offline G4 added no model or environment calls.

### How to check the results

Execution IDs, commits and hashes below can be linked to internal records; share them only with an authorized recipient. Actual execution identities: SI-U1 evaluation `c2356bbda2b44159a333e7c9d24fc2d4`, evaluator commit `8532275932dabddc498c23a2b6d9a045647542f0`; R19 G3 `260422ac02bd42a8b2929d7ef240526b`, producer commit `2da980f631badc25086d12db60d128ff507d3ae6`; offline G4 used analyzer commit `85cbb92395e5e2420c2adeb1fa0634653e742910`.

| Preserved record | SHA-256 |
|---|---|
| `FINAL_PILOT82_PAIRED_ANALYSIS_C2356.json` | `4a3ea016d4c06022980482ac9dbc58155a68bbe20fbc723a68ce49c7c345ea9b` |
| `C2356_SCIENTIFIC_RESULT_INDEPENDENT_ACCEPTANCE.json` | `6530145ac3ac579d00cdb57c28f3fa9bb07b27b990cfe0fba6e93b7fcca5eacd` |
| `R19_OPPORTUNITY_REPORT.md` | `92c066ad1c9c7f187430db82ad6285800e4f31005a1fd2933231d30d695df4bc` |
| `independent_G4_acceptance.json` | `7331b865778481ab4e1b10943eac0e4090ea004e214dbdfff283cfbe042833e6` |

**Chronology and technical corrections.** R19 G3 completed first; a later offline-consumer contract repair enabled G4 to validate the original evidence without changing G3's records. SI-U1 was a separate subsequent training/evaluation study. After SI-U1 evaluation, the first offline extraction failed on tokenizer-snapshot binding; a reviewed technical supplement enabled the corrected extraction while preserving the registered analysis and observed outcomes. Hashes identify the retained records, not public availability, complete historical exposure, or full end-to-end reproducibility. Underlying task-level data, trajectories and some records require controlled access; no public-download link is implied.
