# Conditional late-anchor arithmetic addendum

Status: arithmetic-only design note; not a selected sample, validated opportunity set, protocol amendment, or execution authorization.

This calculation uses only the five identities and replay depths supplied for coordination: `C088/C091/C093/C094/C095`, with `d = [11, 8, 16, 12, 8]`. Their semantic validity, family interpretation, exact-state eligibility, and inclusion as a complete subset remain for Sol Research to review. No task body, result, or additional metadata was inspected for this addendum.

## Conditional upper bound

Assumptions for each of the five cases: one reset; exactly `d` recorded actions replayed; two teacher generations (Stage 1 capped at 40 output tokens and Stage 2 at 16); one legal teacher-selected action; then at most `49-d` P0 suffix generations/actions, each capped at 16 output tokens, for total horizon `H=50`. Candidate input ceiling is 8,192 tokens per generation. These are arithmetic assumptions only and require prospective adoption before any future execution.

| Quantity | Calculation | Upper bound |
|---|---:|---:|
| Sum of replay depths | `11+8+16+12+8` | 55 actions |
| Generations | `sum(2 + 49 - d_i) = 5*51 - 55` | 200 |
| Stage 1 generations | `5*1` | 5 |
| Stage 2 generations | `5*1` | 5 |
| P0 suffix generations | `sum(49-d_i) = 245-55` | 190 |
| Output tokens | `5*(40+16) + 190*16` | 3,320 |
| Input tokens | `200*8,192` | 1,638,400 |
| Physical action steps | `sum(d_i + 1 + 49-d_i) = 5*50` | 250 |
| Resets | `5*1` | 5 |
| Reset-inclusive environment operations | `250+5` | 255 |
| Environment constructions / closes | one per case | 5 / 5 |

Per-case generations are `51-d_i`, yielding `[40, 43, 35, 39, 43]`; each case has 50 action steps and 51 reset-inclusive operations. The teacher-selected action is counted as one physical environment action, not an extra generation beyond the two teacher generations.

This five-case late-anchor arithmetic is separate from, and does not replace or revise, the fixed-S5 17-failure comparison scenarios in `BUDGET_CANDIDATES.json`. The prior fixed-S5 intervention-only ceiling remains 782 generations / 12,920 output tokens / 6,406,144 input tokens / 867 reset-inclusive operations. The late-anchor estimate does not include source acquisition cost, any additional matched control arm, retries, model-load cost, or unlisted accounting overhead. It does not establish that 49-d suffix actions are valid or that the five cases are suitable for a scientific contrast.

No experiment, environment call, model call, sample selection, or budget authorization follows from this calculation.
