# Synthetic read-journal recovery v3 — HOLD

This isolated revision addresses Luna's independently generated duplicate-HEADER and boolean/float-sequence examples, `/home/lizening/research-notes/agent-handoff/grok-codex/2026-11-18_051350_JST__LUNA__v2_readjournal_synthetic_counterexamples.md`. Prior candidates and evidence are unchanged. Recovery now requires exact row keys, exactly one first HEADER, `seq` with exact `int` type and contiguous value, no duplicate JSON fields, and the event-specific fields/types and sequential single-read order emitted by the current synthetic selector. Header bounds must be exact positive integers; read IDs are nonnegative sequential integers; a returned/unknown read must match an open reservation; and completion/unknown events must have the exact emitted payload shape. A complete read phase requires a prior read and no pending reservation; no events may follow completion or scan-unknown. Partial, conflicting or otherwise invalid logs are UNKNOWN. Prior short-read, over-reservation and post-completion guards remain.

Pinned Python run in `test_final_v3.log`: 24 synthetic tests passed, exit 0, including separate duplicate HEADER and boolean/float sequence counterexamples and all 22 preceding tests. No real journal, task, model, CUDA, environment or trainer was read or run. Earlier `test_final.log` and `test_final_v2.log` retain intermediate runs. `read_journal.diff` is the exact delta against recovery v2; code/evidence SHA-256s are in `FILE_HASHES.sha256`.

```
/home/lizening/miniconda3/envs/alfworld-self-improve/bin/python -I -B -c 'import sys,unittest;sys.path.insert(0,".");unittest.main(module=None,argv=["test","-v","test_selector","test_read_journal"])'
```

This is a finite consistency check on the current provisional event schema, not exhaustive adversarial security validation. It does not authenticate source, lineage, tokenization or physical effects; does not measure physical disk traffic; and does not prove crash-resumability, atomic output, CPU/wall/memory/output budgets or model/trainer readiness. The selector's real-use and complete-budget statuses remain UNKNOWN; scientific use remains HOLD.
