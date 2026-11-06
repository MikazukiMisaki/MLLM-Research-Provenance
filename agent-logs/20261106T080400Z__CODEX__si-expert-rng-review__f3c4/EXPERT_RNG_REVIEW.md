# ALFWorld expert-check random stream: corrected independent finding

Status: source review and synthetic software check only; no scientific execution or task generation.

In the installed ALFWorld 0.4.2 generator, `is_solvable` has a PLANNER branch that returns before the expert loop. In the non-PLANNER branch, an iteration that reaches the call to module-global `random.choice` consumes a random draw even when `random_perturb=False`; the expert action is still used when perturbation is disabled. The installed CLI defaults to the handcoded expert. Errors before that line do not necessarily consume a draw. The inspected script SHA256 is `2db4f66bb007e9901f046fa2e805bebb7239dd73886fc6ef665e84b6549e8639`.

A synthetic software test AST-extracted only that function, with a made-up edge stub and no ALFWorld environment, model or actual task. Under one non-PLANNER, one-step, nonempty-action case, it observed one global choice and the expert-selected action. The local-only test script SHA256 is `b5c9666c511bd7a381e3d79ea5b1c29c3c8c99e771f5e32837a38124dedc822c`; the result SHA256 is `0470329ddeb4a85a5818149f17d99a31a87fa34b582d7c62c5899add879729cc`.

A preceding source review documented that the template branch uses the same process-global RNG independently of the caller-supplied seeded RNG. Accordingly, if a non-PLANNER solvability check actually reaches the choice, its number of draws can influence a later template selection. That possibility depends on real global state, execution order, skip conditions, exceptions and the applicable library version. There is no evidence here that a historical run drifted or that every future output would be nonreproducible. Earlier published template review: provenance commit `6a34fb9598dab7301faca88d09b597a9ebb50e08`.

A future reviewed design can separate template, branch and expert streams and test actual entrypoint integration, skips and fresh-process behavior, without altering the frozen baseline. A template-only fix would not prove full-generator reproducibility, task solvability, independent parent tasks or scientific efficacy. No such fix or scientific action is authorized or performed by this review.
