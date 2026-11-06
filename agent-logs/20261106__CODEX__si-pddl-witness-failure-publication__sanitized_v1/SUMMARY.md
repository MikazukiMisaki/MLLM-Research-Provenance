# Synthetic PDDL witness: failure and parent-identity fixture

Status: one bounded engineering attempt failed before the worker initialized the environment. The supervisor command exited 2, and its child exited 1 with `UNEXPECTED_SUPERVISOR_PROCESS`. No automatic retry took place. The exception occurs before the worker creates its run directory or ledger and before it imports, constructs, resets, or steps the PDDL environment. Source inspection supports zero model calls and zero environment operations for this attempt; a missing ledger alone would not establish those counts. The original supervisor stderr contains the same traceback twice. Input hashes were unchanged and the supervised process group had exited.

The coordinator used a relative script argument, while the worker compares against an absolute expected spelling. The retained supervisor summary constructs a normalized argument representation and does not prove the parent's actual command line. Because the exception combines executable and argument checks and the actual parent process values were not captured, the exact failing comparison remains unproven. An interpreter spelling difference is another possibility. The observed failure is not a successful engine verification.

## Separate model-free fixture

An independently authored, bounded fixture extracted the unchanged identity-comparison function body and replaced its expected paths with fixture-owned values. It did not invoke the candidate worker, a model, PddlEnv, or historical research data. Four cases each ran once:

| Fixture case | Result |
| --- | --- |
| Expected absolute command | Accepted |
| Relative script spelling | Rejected |
| Equivalent interpreter symlink spelling | Rejected |
| Additional unexpected argument | Rejected |

All rejected cases reported the same identity-check error. The observed executable resolved to the same interpreter in all four cases, and the rejections arose from complete argument comparison in this fixture. These observations do not independently establish which comparison failed during the engineering attempt. The fixture does not validate the actual supervision workflow, environment, or scientific outcomes.

## Provenance and limitations

The original seven reviewed records remain local-only and unchanged. `ORIGINAL_HASHES.json` lists their complete SHA-256 hashes using descriptive labels; this package contains sanitized derivatives, not the original bytes. Local path names, process identifiers, raw process arguments, encoded process data, and environment values have been omitted. No model or PddlEnv call was made in either the failed attempt or the fixture; no efficacy, training, held-out evaluation, or successful environment-run result follows from these records. This package does not authorize a further attempt.
