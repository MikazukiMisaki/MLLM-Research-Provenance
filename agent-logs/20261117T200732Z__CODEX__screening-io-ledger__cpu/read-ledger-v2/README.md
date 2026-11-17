# Synthetic read-journal recovery v2 — HOLD

This isolated change responds to `/home/lizening/research-notes/agent-logs/20261118__REVIEW__si_readledger__4vs6UI/replay_recovery_semantics.py`. The earlier candidate and independent reproduction remain unmodified. The recovery reader now rejects three logically invalid, hash-chained journal cases: a `RETURNED` count different from its full reservation; any event following `READ_PHASE_COMPLETE`; and file or byte reservation totals above the positive limits in the header. These cases remain UNKNOWN even if their hash chain is syntactically valid. `UNKNOWN` read receipts may retain a lower bound below the full reserved amount and are not converted to success. The selector's physical operations and research policy are unchanged.

Pinned Python run `test_final.log`: **22 synthetic tests passed, exit 0**. This includes three new, independently constructed hash-chained negative cases, the prior partial-read/OSError and torn-log tests, and the original fictional selector tests. No real task, model, CUDA or environment was accessed. Reproduce from this directory:

```
/home/lizening/miniconda3/envs/alfworld-self-improve/bin/python -I -B -c 'import sys,unittest;sys.path.insert(0,".");unittest.main(module=None,argv=["test","-v","test_selector","test_read_journal"])'
```

`read_journal.diff` is the exact local change from the previous candidate. Hashes are in `FILE_HASHES.sha256`. This limited correction does not prove arbitrary corruption or adversarial tampering detection, crash-resumability, physical-disk byte accounting, actual source/lineage, atomic output, CPU/wall/memory/output budgets, real trainer format, or any scientific result. Full scan budget remains UNKNOWN, source identity remains UNKNOWN, and scientific use remains HOLD.
