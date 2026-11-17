# Independent review of interrupted DEV trajectory summary

The reviewed report is
`/home/lizening/research-notes/agent-logs/20261118__CODEX__independent_trajectory_comparison__private/REPORT.md`,
SHA256 `7e450e953119b70186c7f506b7a78791d2c6057a7cc4921495ce869c94a30858`.
Its aggregate is `aggregate_v2.json`, SHA256
`141f4526e37ea1d97e653fb9361c6719cec72dd8aa7b1e2e7ee573fa82ab0472`.
Recount sources were the six worker `worker_events.jsonl` files and six owner
`supervisor_events.jsonl` files under
`/home/lizening/research-notes/agent-logs/20261118__CODEX__fixed_product_per_arm__private/live-output`.
No private task text or action strings are copied into this record.

| Anonymized arm | Worker SHA256 | Owner SHA256 |
|---|---|---|
| A P0 | `b1ad9e4c26b90a9f0ff9fde0b0d553753a2ee499d318d60fca47c374094a333e` | `87a504af1b214134f21ada69ba1809a377ef52265fc093131985574b02925833` |
| A candidate | `91da6d5cd4e4f7348db4005fd0e1320177ee1cb95b97d3f2d3835d680afe0543` | `b4e1f0312c205df553c52ab3111533720565ede9d5f83aa884c9997ec5c54e77` |
| B candidate | `2292259d1eed9ea07e6777cfa692a08dfcdd11ab68b3775bdc0ff2bf398fcd14` | `9892f6c2c6c0f2def2400e8478c6a21f428b4a7049944b3bce04b390741686b2` |
| B P0 | `437827414e4bb5b530d5abd9cfc2eb91c9386f193903d4ea98b566f8884e67ab` | `d23bb512e7db4abc5c5d23bf9df14e593f3050b5f9eabf0ea107fef3122045b8` |
| C P0 | `82d4ffd48060b6294dd7f854dc0b8d5081ca76eebd2642959f7f80a60d748731` | `3485457bb94e7a8d633204aab68e9ffeb5ced86ae6421381640426046c42f447` |
| C candidate | `a4b9063ef537271d7e03e7857051b57c11903cd39ef3c999501ef3a26cebaf13` | `a022e03445082dc272e4cac154dc638037d944662b1d976efca647391766c367` |

Independent recount supports the report: in A both arms' 50 action strings
match position by position and alternate 25 each of two reported action
categories; all 100 parser statuses are selected and both outcome records are
false. In B the first divergence is at step 3; P0 and candidate record success
in 9 and 11 steps respectively, with 2,936/45 and 3,546/55 input/output
tokens. A and B's recorded public initial states match, which does not prove
matching hidden state.

C candidate lacks a completed outcome: 29 generations and 28 steps returned;
one further step is reserved but unreturned. D did not start. Across the six
started arms, logs record 199 returned generations, 198 returned steps, six
resets, six model loads and six materializations; 61,223 input and 995 output
tokens. An unclosed reservation is retained as unknown in the accounting and
not turned into a success/failure. Report's two complete pairs yield an
observed difference of zero in that selected, completed subset only.

The report properly limits causal and generalization claims given exposed,
related tasks, small selected sample, interruption, earlier setup-budget
deviation and the stop-token contract. This review examines only current
run logs: it does not independently establish historical exposure or the
candidate's training lineage. Recorded `won`/native capture is a worker
claim, not separate physical authentication. Interruption is not known to be
random, so the two complete pairs do not form an unbiased estimate. C lacks
an initial state in a completed arm-result record, but it does have a reset
receipt; lack of the former must not be stated as lack of all reset evidence.

No model, environment, GPU or task execution was performed and original
records were not modified. This is descriptive checking, not a research
efficacy claim or permission to run a successor.
