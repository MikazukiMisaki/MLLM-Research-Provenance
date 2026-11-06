# ALFWorld generated-goal RNG contract: source and synthetic check

Decision: **reproducibility gap for a possible future generator; not a demonstrated historical run failure, task-set result, or experiment launch.** The examined installed package reports ALFWorld version 0.4.2. This investigation did not read real task data, generate tasks, instantiate ALFWorld, initialize CUDA, or call a model.

## Observed exact code

The installed `alfworld-generate` script has SHA256 `2db4f66bb007e9901f046fa2e805bebb7239dd73886fc6ef665e84b6549e8639`. It creates an independent `random.Random(args.seed)` and supplies that object to `add_task_to_grammar`. The separately installed `alfworld.agents.utils.misc` source file has SHA256 `28972caffbf77c3ab2cfad9789a91cc02ace472f4a90769937c11024e18f5e44`: `add_task_to_grammar` uses the supplied object for the probability branch and passes it to the human-annotation picker, but calls `get_templated_task_desc` without an RNG argument. That function uses module-global Python `random.choice` for the template. Thus the independent supplied seed is not by itself a binding on the template choice. Global seeding or a single-template case could still make output repeatable; this review has not determined whether a particular historical process did so or which templates were available in any actual task.

The installed generator also discovers trajectory inputs recursively; it should not be pointed at a mixed or protected root. Any future bounded generation invocation must use an independently authorized isolated source whose membership and file behavior are reviewed in advance. The official upstream implementation documents source trajectories, initial-state PDDL and environment/expert solvability checking rather than demonstrating a generator of independent new parents: https://github.com/alfworld/alfworld/blob/master/scripts/alfworld-generate .

## Isolated check

`check_rng.py` extracts only the two relevant function definitions via AST, executes them with an invented metadata dictionary and synthetic two-template registry, and does not import ALFWorld. The same supplied RNG seed with two different controlled global random states gave different template outputs. This proves the source-level dependency in the fixture; it does not claim real CLI end-to-end reproducibility, a change to historical data, successful task generation, or non-overlap with existing/protected tasks. The exact test and result are retained locally.

## Future design implication

A reviewed source/generator contract should identify every independent random stream and its source, bind a generator version and template source, and make output reproducible across fresh processes with a non-sensitive synthetic fixture. One possible approach is a separate reviewed wrapper or patch that explicitly carries an RNG through template selection, or that seeds global state at a precise, tested point per source identity; neither approach is applied here and a global seed set once may be perturbed by unrelated random calls. Any actual compatibility, distribution, PDDL solvability, task provenance, licensing, isolation and scientific claim remain separate validation questions. Do not alter the frozen scientific baseline or installed upstream library based on this note.
