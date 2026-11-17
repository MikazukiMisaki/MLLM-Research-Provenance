# Synthetic one-game adapter: engineering evidence

Status: observed positive synthetic adapter reset and terminal step; earlier synthetic step failed. Both are bounded engineering checks, not scientific evaluations. The successful fixture differs from the failed fixture and is not a retry of its run identity. No model, tokenizer, GPU, or real task was used. No successful model behavior or generalization is implied.

| Observation | Prior fixture | New fixture |
| --- | --- | --- |
| Worker exit | 1 | 0 |
| Fixture / adapter / native initialization | 1 / 1 / 1 | 1 / 1 / 1 |
| Native game load / conversion / reset / step | 1 / 4 / 1 / 1 | 1 / 4 / 1 / 1 |
| Adapter reset | Returned; won=[false] | Returned; won=[false] |
| Adapter step | Native step returned; wrapper raised KeyError for instance-style object metadata | Returned; reward=1.0, done=true, truncated=false, won=[true] |
| Elapsed seconds | 1.528369733132422 | 1.5295984232798219 |

The failed native step incurred cost: its native returned reward, done, and won were not recorded and remain UNKNOWN. The later fixture supplied a recognized category to the expert and a synthetically constructed object identity. The observations concern only these fixtures. The narrow factory intentionally bypasses normal full-pool discovery; this does not verify upstream solvability metadata, a full evaluator, multiple tasks, or population performance.

In the positive fixture, reset included a non-null game-file identity while the step field was [null]. A consumer must carry and bind the reset/task identity rather than assume the step repeats it. The journal contains selected fields and is not the complete original observation or action set.

Across the five related, distinct engineering attempts recorded locally: five fixture constructions, five native initializations (two failed, three returned), three game loads, 12 conversions, three resets and three native steps; recorded wall time 6.175260595977306 seconds. The first attempt CPU time, aggregate physical disk writes, complete descendant accounting, and system-wide resource exclusivity remain UNKNOWN. The five attempts are not five independent research observations.

Each `*_events_sanitized.json` is a derived allowlisted projection, not the original journal: it preserves event kind, native counters and selected outcome fields and replaces the original game-file field with a coarse presence marker. It omits paths, IDs, commands, full metadata, and process information. `ORIGINAL_SHA256.json` records the SHA256 and byte length of original private artifacts; it contains digests, not those artifacts. Original bytes, including the source journals and exit receipts, remain preserved privately and are necessary for a full independent audit. The hashes establish byte identity when checked against those originals, not the truth of claims by themselves.

The candidate package is prepared locally only; no index modification, upload, or publication is claimed.
