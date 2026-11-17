# State-selection CPU prototype v2: duplicate references, HOLD

This isolated revision responds to `/home/lizening/research-notes/agent-logs/20261118__REVIEW__si_selector__QsHhjQ/reproduce_alias.py`. The previous selector, evidence and reproduction remain unchanged. Schema `SI_STATE_SELECTION_DEMO_V2` adds a caller-declared `source_decision_id`; the existing `episode_id` is treated as the declared source episode ID. Both must be unique throughout the selected source cohort. For each parent, the terminal receipt is tracked by opened file device/inode; using the same file, including via a hard link, across parents rejects the entire cohort. The complete decision source-reference tuple `(prompt, action, label, mask)` is similarly tracked by opened file identities, and duplicate tuples across parents reject the cohort. A shared individual label file or coincidentally equal text/bytes is not sufficient for rejection. Input file hashes and source references are still checked as in v1; no duplicate is repaired or replaced.

**These are consistency checks on declared identities, not authenticated source identity.** An author can copy bytes to different inodes and invent distinct IDs; source metadata, record origin, actual parent lineage, native terminal and action/label provenance, execution identity, tokenizer and real trainer transformation remain UNKNOWN. The terminal and decision records are not proven to be real source journal events. `scientific_use` remains HOLD. No real tasks, models, environment or GPU were read or run. No scientific data were generated; this is not a production adapter or research result. Same-UID mutation races and atomic/durable output are still unproved.

Pinned Python final run: 12 synthetic tests passed, exit 0 (`test_final_v3.log`). The suite rejects duplicate episode IDs, duplicate decision IDs, identical full decision reference tuples, repeated terminal file references and terminal hardlinks across declared parents. It also shows an individual shared label artifact is accepted, and retains original checks on lineage overlap, token mismatch, first episode failure, byte drift and manifest hash. Only fictional input files were used; fixture trees in temporary directories were removed. `test_final.log` and `test_final_v2.log` retain intermediate v2 test runs.

Reproduce from this directory:

```
/home/lizening/miniconda3/envs/alfworld-self-improve/bin/python -I -B -c 'import sys,unittest;sys.path.insert(0,".");unittest.main(module="test_selector",verbosity=2)'
```

The v1 README gives the surrounding provisional manifest/selection semantics and other known limitations. Schema v2 requires the new per-decision field and is not backward compatible with v1 fixtures. Review `FILE_HASHES.sha256` for exact bytes.
