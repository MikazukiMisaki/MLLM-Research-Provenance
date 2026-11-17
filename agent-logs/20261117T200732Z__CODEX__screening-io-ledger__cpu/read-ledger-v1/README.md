# Fictional selector read-reservation ledger — HOLD

Isolated response to `/home/lizening/research-notes/agent-logs/20261118__REVIEW__si_selector_v7__3BFT6z/reproduce_partial_read.py`. Original selector and review evidence are unchanged. Only fabricated local files were read; no real source/task, model, CUDA or environment was accessed. Source, execution and lineage authenticity remain UNKNOWN; CPU, wall, memory and output-byte budgets remain NOT_IMPLEMENTED; full scan budget remains UNKNOWN and scientific use HOLD.

Before every actual file-content read, the selector records and fsyncs a hash-chained `RESERVE` with fstat size and file number, charging the full size against caller limits. Each `os.read` request is at most the remaining reserved bytes. Successfully returned chunks increment a user-space **lower bound**; a complete stable and hash-matching file gets a `RETURNED` receipt. Any exception or mismatch after reservation is `UNKNOWN` and the full reservation stays charged without refund. File/byte caps are checked against reservations, not the reported returned lower bound. This is not an estimate of physical disk I/O: caching, short reads, operating-system buffering and errors can make that quantity different or unknowable.

The append-only `read_journal.jsonl` is fsynced per event; the newly created output entry and journal directory entry are also fsynced. `read_journal.recover(path)` checks event sequence/hash chain and recomputes reservations, known returned lower bound, incomplete reservations and explicitly UNKNOWN reads. A torn/malformed log, unclosed reservation, failed scan or missing `READ_PHASE_COMPLETE` reports UNKNOWN. `COMPLETE_LOGGED_READS_ONLY` applies only to recorded read operations and does **not** certify dataset selection, output atomicity, source truth or scientific execution. A process crash can leave partial/torn records or no final selection/status files; recovery retains UNKNOWN in that case, not an assertion of reliable crash-proof continuation. Power failure, unsupported fsync semantics, malicious same-UID tampering and partial journal-write failure remain unproved. A failed journal write itself prevents subsequent source reads and leaves the ledger unresolved. There is no resumed scan.

`test_final.log` records 19 synthetic tests passed, observed exit 0. These retain the preceding 16 selector checks and add: a five-byte returned fragment followed by injected OSError, where the complete episode fstat size remains reserved and both parent and read are UNKNOWN; a byte ceiling that refuses the next read before its reservation; and an unclosed then torn synthetic journal that recovers as UNKNOWN. The normal fabricated 16-parent path checks that fully returned read events recover as `COMPLETE_LOGGED_READS_ONLY`. Tests exercise no actual power loss or real task data.

Reproduction from this directory:

```
/home/lizening/miniconda3/envs/alfworld-self-improve/bin/python -I -B -c 'import sys,unittest;sys.path.insert(0,".");unittest.main(module=None,argv=["test","-v","test_selector","test_read_journal"])'
```

`test_initial.log` retains the earlier passing run. See `FILE_HASHES.sha256` for exact code and test evidence. The preceding selector README remains applicable for candidate ordering, REJECT/UNKNOWN/INSUFFICIENT, parent/decision ledger and non-authentication limitations.
