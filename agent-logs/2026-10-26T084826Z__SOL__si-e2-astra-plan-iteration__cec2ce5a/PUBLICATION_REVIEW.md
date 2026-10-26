# Independent publication and design review

Verdict: **PASS for design review and compact provenance publication; no material blocker found. No runtime authorization.**

Scope: reviewed the coordinator decision, next-stage design tasks, historical reachability method/exported metadata, source-outcome summary, Astra plan/decision and supporting provenance in these two task directories. This audit did not recount raw trajectories or inspect unused task bodies. No tests, SSH, GPU/CUDA, tokenizer, model or environment calls were made. Only this review file was added; Astra's frozen handoff and shared records were not changed.

Independent arithmetic on the exported historical metadata reproduces 111/75/41/22 reachable nonlight sources at d=5/10/15/20 and 249/480 = 51.875%. This is descriptive evidence from the selected old cohort, not a forecast or deterministic bound for new96. The source-outcome summary is internally consistent: 6/120 nonlight failures, family counts 0/2/2/2, and 7/127 including light. Astra explicitly distinguishes reading these results from independently recounting raw sources.

The paper budgets recompute correctly: v1 8,496 generations / 9,792 reset-inclusive operations / 138,240 output tokens; candidate v2 9,216 / 9,792 / 149,760. Source-only remains a separately justified investment, capped at 4,800 generations. Input/device caps do not promise completion.

The source-first design correctly requires all96 sources to be complete before structural futility adjudication, a conservative E that covers every potentially Q-valid anchor, unknown evidence to cause integrity STOP, and global plus family necessary-count gates. Unmeasured teacher outcomes remain NA. Passing these gates does not establish recipe constructibility or learning efficacy, and cannot authorize runtime. No overstated joint acceptance was found.

**Pool/arm wording clarification:** the intended rule is that **B_pool contains C**. Sampled **B24 need not contain all C24**; it is drawn once from that pool under the fixed matching and neutral-example requirements. Astra's shorthand “B包含C” must be read as candidate-pool inclusion, not set containment of the sampled training arms. Its surrounding text specifies this pool interpretation. This clarification preserves the immutable Astra artifact rather than editing it.

At the audit snapshot, the 26 files in the two directories were UTF-8 text without NUL bytes, targeted credential-pattern matches, weights, token-array payloads or new task bodies. Receipt fields named prompt contain agent coordination messages, not scientific model prompts. Astra's existing inventory verified **12/12** entries. Root's final manifest/hashes remain the coordinator's finalization step; this review does not claim remote publication.
