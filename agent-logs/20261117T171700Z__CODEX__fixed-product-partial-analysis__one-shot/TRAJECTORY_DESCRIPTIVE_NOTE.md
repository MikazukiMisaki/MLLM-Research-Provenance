# Descriptive trajectory observation, not a causal conclusion

On completed case a, both arms produced exactly the same 50 committed actions, alternating `look` and `examine twopairatarget 1` 25 times each. Every one of these 100 parser results was `selected`; both episodes ended without success. This is evidence of an observed behavioral loop in this particular exposed DEV case, not evidence of a parser-format failure or proof of why the models looped.

On case b, both arms succeeded; P0 completed in 9 steps and the candidate in 11. On case c, P0 failed after 50 steps and repeatedly moved/took the same item between locations. The candidate's trajectory is incomplete: its 28 committed actions include repeated movement of the same item, but no final outcome may be assigned. More targeted training or diagnostics might address repeated progress failures, but these observations alone do not establish that a proposed intervention will improve success, and do not justify changing the frozen protocol or introducing a new selector.

These counts come from `dev_decision_committed` and `dev_parser_returned` entries in the archived worker journals. Cases are previously exposed and related; no generalization claim follows. Full cost, roster and uncertainty are in RUN_REPORT.md, INDEPENDENT_COST_RECOUNT.json and ROSTER_BOUNDS.md.
