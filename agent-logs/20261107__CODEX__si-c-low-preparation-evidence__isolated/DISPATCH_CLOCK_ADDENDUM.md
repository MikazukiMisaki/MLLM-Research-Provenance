# Dispatch clock boundary addendum

Before any live launch, clarify the earlier statement that the proposed
1,800-second outer live ceiling begins at the launch of the CLI. The reviewed
candidate starts its monotonic deadline no later than entry to the dispatch
function. Its main CLI path starts earlier, immediately after importing the
time module. Both occur before checking the external pin, reading inputs,
creating its one-use claim, or starting the production training CLI. The
production CLI's gate, worker and training are charged to that deadline;
cleanup is also timed but may continue beyond the threshold. Time spent
starting the outer Python interpreter and importing the time module occurs
earlier and is **not** covered by this clock; the main CLI path does include
subsequent imports and argument parsing. No model,
CUDA, environment or production training CLI is intended during that earlier
bootstrap, but an interpreter/import stall or its CPU and I/O cost are not
strictly bounded by this in-process deadline and remain UNKNOWN on failure.

This narrower, explicit clock boundary supersedes only the earlier ambiguous
start-of-CLI description. It is an operational exploratory bound, not a claim
that execution ends within 1,800 seconds under an uninterruptible system call,
process escape, monitoring failure or kernel stall. Such tails are UNKNOWN.
Record the externally observed outer process start and exit as additional
evidence; that observation is not an additional enforceable watchdog. The
inner 5,400-second protocol, one attempt, no-retry rule, token limits and
other reviewed controls are unchanged. If pin validation or preparation
already exhausts the available dispatch budget, no live child may start.
