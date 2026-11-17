# Independent reconciliation — distinct exposed-DEV three-arm study

**Result: all 36 episodes are complete, and the exploratory screen is not met.** P0, C-old and C-quarter each succeeded on 10 of 12 parents. Outcomes were matched for every parent: all three succeeded on the same 10 and failed on the same 2. C-quarter versus either comparator has gain 0, loss 0, and net difference 0/12 (0 percentage points). The frozen resource screen required C-quarter to beat P0 by at least 2/12 and C-old by at least 1/12; neither condition is met.

This is a previously exposed, adaptively selected development cohort, after a technical stop in another run, with a single trained seed. The result reports no observed success-rate difference in these 12 cases; it does not establish population-level equivalence, disprove a benefit elsewhere, establish independent generalization, or show that the three policies' trajectories were identical. The earlier stopped study remains UNKNOWN and is not pooled into these counts.

I independently parsed the actual start, exit, full event journal and summary; confirmed the frozen one-shot release/manifest hashes, command argv, candidate source hashes, current clean source checkout, schedule/order and per-episode task/product identity bindings; reconstructed all 36 outcomes from native transition evidence or policy failure; compared pair initial-state hashes; checked returned operation identities and step sequences, decision/action mapping and token accounting; and confirmed every outcome matches the summary. Input hashes were verified again after reading. This supports record attribution and the aggregate calculations, not cryptographic proof of execution or external process ownership. I did not rehash large model trees in this check or re-run the environment/model.

| Quantity | Observed |
| --- | ---: |
| P0 / C-old / C-quarter successes | 10 / 10 / 10 |
| Model-generation / environment-step starts | 601 / 601 |
| Environment reset starts | 36 |
| Completed-generation input / output tokens | 320,009 / 3,005 |
| Supervisor elapsed allocation | 1,202.348 seconds |

The allocation is conservative supervisor wall time, not measured exclusive GPU utilization. Supervisor exit code is 0 with `EXIT_ZERO_REQUIRES_RESULT_AUDIT`; its own descendant-cleanup field remains `NOT_PROVEN`. No hidden/unobserved work is inferred to be zero.

Key immutable input hashes: manifest `cf978725c718e89b96d80ed56b468d9c8e00a6e22fafc43acaa38dd65181d71f`; release `aa11db0aaa6e5d390a500edbbf4905f1055f637607d79c6428890a8a76d369fc`; raw journal `a1ab34fb287372be582648295eb7a506a8ed70174b1689e0f7c2cfd7d4e4a799`; summary `ca0ec8f64db8257a9fcb9a7d02a5a0355391acad90813c2ff6c2bdf5a409dfc1`; supervisor exit `babec3be088f6211ed37d8e129745b7e21eb6914a349dc3144ea6231e4d5a1cb`. The aggregate-only machine record and independent script are beside this report. No model, GPU or ALFWorld process was started, and no original input file was edited.
