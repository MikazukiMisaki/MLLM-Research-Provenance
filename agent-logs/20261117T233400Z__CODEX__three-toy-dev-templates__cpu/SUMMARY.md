# Three synthetic DEV templates: text-environment engineering evidence

**Observed: all three manually authored plans completed on the existing TextWorld/PDDL stack.** These are artificial DEV engineering fixtures. No model, tokenizer, GPU, training or scientific evaluation was used. This result does not establish real-model success rate, full ALFWorld adapter/evaluator compatibility, independent evaluation parents or an independent test set.

| Synthetic structure | Fixed manual plan | Native observation |
| --- | --- | --- |
| Closed receptacle, held object | Open the receptacle; move the object into it | Initial won=false; first step nonterminal; second step won=true, done=true, reward=1 |
| Object initially in source, empty hands | Take the object; move it to the destination | Initial won=false; first step nonterminal; second step won=true, done=true, reward=1 |
| Held object, destination at another location | Navigate to the destination; move the object to it | Initial won=false; first step nonterminal; second step won=true, done=true, reward=1 |

The plans and initial predicates were fixed before execution; their three action-precondition structures are distinct. This is not evidence that changing names or seeds creates independent parents, or that the three examples form independent task samples. The precise fictional fixtures remain in the private source evidence, identified by original-byte SHA256 in `ORIGINAL_HASHES.json`. They use pinned source PDDL-domain and grammar bytes, also recorded there.

A single supervised worker completed with authentic return code 0 and no retry or stop. Recorded cost: 3 fixture constructions, 3 native initializations, 3 game loads, 3 resets, 6 environment steps and 12 calls to the original PDDL-to-SAS translator. Recorded wall time 2.035877412 seconds; direct-child user/system CPU 1.548920/0.132808 seconds. Actual aggregate physical disk I/O and unobserved descendant effects remain UNKNOWN. The per-file cap and sampled free space were not an aggregate physical-write limit.

The frozen stop rule required stopping the whole run on the first failed initialization, unexpected conversion, inadmissible predeclared command, unexpected intermediate terminal, final predicate mismatch or resource/technical exception; no alternate command or retry was allowed. None occurred in this three-template run. Earlier separate engineering attempts include two failed native initializations; they were not repaired or retried as part of this run. Including the five earlier native/adapter attempts yields 8 fixture constructions, 8 native initialization attempts (2 failed), 6 game loads, 24 observed conversions, 6 resets and 9 steps; total recorded wall time 8.211138008 seconds. Earlier first-attempt CPU and aggregate physical I/O remain UNKNOWN. These engineering attempts are not independent success-rate observations.

A future confirmation route would need a separate prospective source, canonical structural and parent boundaries, and a frozen train/DEV/confirmation split. No particular future confirmation task was generated, viewed or included here. The placeholder idea of reserving different action families does not prove that a confirmation pool exists.

`SANITIZED_EVENTS.json` is an allowlisted derived projection and is not the original event ledger. Its source hash and all original-file digests/lengths are in `ORIGINAL_HASHES.json`; original bytes remain privately preserved and are required for a full audit. Hash equality identifies bytes, not truth or independent provenance. This package is prepared locally; it has not been published or pushed.
