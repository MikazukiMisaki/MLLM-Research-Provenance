# v1 to v2 changes

- Arm state is tracked as started, outcome, verified, closed; a completed setup and pre-verification are required before arm start. Global complete requires the exact 4 pairs / 8 closed arms.
- Model load and generation must return before an arm outcome; no step is required. Reserve and return counts remain separate and ordered.
- Pair failure latches the owner in a non-continuable, non-completable state even if the caller catches the exception; an open reservation is retained.
- Path checks reject lexical `..` components explicitly. This does not establish resistance to filesystem races.
- Synthetic regression tests reproduce premature success and the fourth-pair mismatch, validate failure latch, zero-step support and traversal rejection. No production runtime was executed.
