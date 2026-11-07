# Independent audit: completed one-shot C-low offline specification preparation

Verdict: **PASS for the observed offline artifact construction and the limited checks below; reviews NOT_OBTAINED and no training, preflight, model or scientific effectiveness clearance is implied.** The coordinator reports the actual outer tool/process exit as zero; this audit independently checked the persisted journals, not the coordinator's tool stream. No gate, tokenizer, model, CUDA, environment or training was invoked here.

## Verified observations

- All seven original input files' current bytes match the exact prior pins, including both actual data files. They were read as opaque bytes for SHA-256 only, never parsed as rows or printed. This auditor performed two hash-check passes (the second added a pure-function LR check); these are logical reads, not measured physical disk I/O. Each checked read had matching start/end file identity, size and timestamps. This does not prove continuous immutability before/after those read windows.
- The outer persisted journal is exactly STARTED followed by RETURNED exit 0; the inner journal is exactly STARTED followed by RETURNED_UNREVIEWED. SHA256 outer `13b7db3cee20b7e40d2633bb761fc51c21d67e4d8a7912481e9c305373a1444f`, inner `684a73316fb43f6700df4221f7a002e10eec0f42243590f5c648127265d7a9b6`. Journal content and paths remain private locally.
- The output directory is owned and private, contains exactly the four expected regular output files, each mode 0600. All four raw file hashes match the inner journal. The receipt binds the seven original pins and three other output hashes and states source/pair review `NOT_OBTAINED`, status `C_LOW_UNREVIEWED`, data rows not parsed.
- Comparing parsed documents with **type-sensitive canonical full reversal** against originals confirms B and C changed only LR 0.0001→0.00005. Protocol changed only LR, the ordered 78 values and protocol ID. All 78 low-rate values are bit-identical as Python floats to the frozen production pure helper from Git SHA `9bbaa12c2d8177a60ec5a74ed2f970ef29a57bce`; no production gate was run.

| Output | SHA-256 |
| --- | --- |
| B manifest | `a80a6a540963dd84bf3c006a7bf61b4e5f4a5c1ea9fdc0050b3bce55ef7152bf` |
| C manifest | `a04283f822cb0bb008200d2d0551d38e0bf4de1b6113682c176a0788f089a785` |
| Protocol | `96e4ac83f9188678a4c820e4f50c9b6b5e74e7caf5a2bbe9ca272ee93614a07e` |
| Receipt | `ef135c993bb6af8d906573c0041de27e12b62c3f06a62b45ffecfe8c60e61cc3` |

## Scientific and operational boundaries

The original protocol's status, existing budget and resource metadata are historical fields preserved by the full-document comparison; they do **not** authorize a new run or prove present-day resource fit or task independence. New derived B-low and C-low manifest documents are not B-low or C-low model products. A genuine, independently authenticated source/pair review, admissible frozen data, current supervised budget and runtime checks, safe output custody, an independently reviewed immutable input snapshot/rebinding design, and compatibility with the complete production gate are still outstanding. The sequential prepare/audit hashes are not a simultaneous snapshot and do not prove future path stability. The prior review's other outer-process, crash durability and descendant limits remain in force.

Audit program SHA256 `388dc0ef6acee9d2e3227ad1d31aeb9fbea600cba9c0907096105131888aeb57`; raw path-free summary `audit.log` `84050adfda95df5d63177cd248dfbf4c67cffced43ddecf3a22438c4152ddccf`. Sample IDs, input paths, original data, and new manifest contents were not printed in these records; the four outputs remain sensitive and private.
