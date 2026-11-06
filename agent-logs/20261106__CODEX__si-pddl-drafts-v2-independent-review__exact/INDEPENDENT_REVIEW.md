# Independent review of v2 development-only symbolic PDDL drafts

Decision: **PASS for static draft and byte binding only**. No parser/planner/translator, environment, model, tokenizer, GPU, protected tasks or scientific execution were used. This review does not establish syntax acceptance, runtime solvability, independent task groups, data non-exposure, or eligibility for training/evaluation. Original candidate remains unmodified.

## Frozen inputs and corrections

- Source SHA `4ee5d9267c3004dbecf8c22c4a8d50f5ec18fe3a3b8e85a8cbc42befd955306b`; static checker `82dcb4374707ea39bf0803f0fece51b8e2d2297397cdc3a6dce1d21c43d44211`; manifest `b1bea1c4784916daf07595eca19e9d58d513498359fe61117ce9ea4f3fd52abd`; 13/13 candidate `SHA256SUMS` rows independently verified (inventory SHA `7320e9d629b07dd12cfc6c9012f42be0890d5f1e5ba0141d16ddc3761be407d4`).
- Toggle PDDL `b6528ad2b840d57b4e4e50bf40e9986e9a62ce40708fc5d2c317743d93292d30` and slice PDDL `b0a3626194f21587113bb926c86650572fe51d8b41bdc5379212d8856cd95318` are unchanged versus v1. Slice grammar is unchanged (`de2e9b4a1c3346e62c1a1cefcb650ff5f0faafbc123316c02ccf9c2726428f7f`). Toggle grammar `397c44e31e6daae3eb0aa7565252c03f068863035218671d8fb328361b456456` now says toggle without asserting exactly once. Problem goal means “has been toggled”; it does not encode an exact number of operations. A future one-step witness still requires trace-level action counting.
- Both grammar files independently equal the pinned public grammar plus their respective unique instruction replacement. `check_grammar` verifies public SHA and exact derived bytes; seven independently generated cross-case, byte tamper, type and unsupported-kind cases are rejected. This checker is byte-level, not a grammar parser. Its API is separate from `check(kind,text)`; a future consumer must explicitly run both checks on the exact files it will use and bind the public domain separately.

## Domain interpretation and constraints

The earlier review of unchanged PDDL remains applicable: under closed-world assumptions both goals are initially false; all stated toggle and slice action preconditions match the pinned public symbolic domain; the knife is initially held; the target and actor share a location, and target/tool are distinct. Required domain identifiers are declared in the problem object sections; actual parser treatment remains UNKNOWN. Public domain hash `f1473041ed01da514de1f87adfd7ef0804862361f83ccf63c75e43633b0eb280`; grammar hash `c5b22f0f73309a7fd7c8e5b71de42ad4803b60766ab4a51cc2feb34162be036b`.

A toggle from initial `isOn=true` symbolically sets `isOn=false`, while `isToggled=true`. The pinned feedback condition tracks `isToggled` and may say “turn on”; it is not evidence of the actual final power state. Display names and command availability are not established. The common previously self-authored clean template is disclosed, as are unknown prior exposure and complete ancestry: these drafts cannot be counted as separate concrete ancestry components without applying existing lineage rules.

## Tests and evidence

Pinned Python with `PYTHONPATH`, `PYTHONHOME`, `VIRTUAL_ENV` removed: candidate's 12 static/binding tests passed (`developer_suite_rerun.log`). Independent tests: 3 passed, including ten malformed PDDL mutations rejected and a two-toggle symbolic counterexample (`independent_test.log`); a further independent grammar test accepted both correct byte sets and rejected seven adversarial cases (`grammar_adversarial.log`). All are static/synthetic; no inference from them to runtime behavior.

## Next step

Retain development-only status. Any real parser or single-action environment witness requires its own reviewed concrete invocation, exact input/path binding, resource accounting, action-count logging and stop rules. Do not claim meaningful independent evaluation or success-rate evidence from these symbolic drafts.
