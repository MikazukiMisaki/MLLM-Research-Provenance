# SI-E2 narrow environment read-isolation ruling

Observed concrete trigger: installed alfworld/agents/environment/alfred_tw_env.py118–128 calls collect_game_files from AlfredTWEnv.__init__. Its lines153–181 walk dataset.data_path and open every traj_data.json and game.tw-pddl before filtering. Existing src/sft/environment.py ExactTaskPoolEnvironment._get_environment constructs that factory BEFORE overwriting game_files with the exact task. With the old global TRAIN data_path this would open reserved new-task bodies despite a one-task final game list.

Severity: BLOCKING for this engineering probe if unchanged, because new96/48/600 bodies must remain closed. No actual ALFWorld constructor has been invoked in this phase.

Narrow authorized implementation: in the NEW engineering exact-task factory, restrict effective dataset.data_path to the authenticated historical target task directory BEFORE AlfredTWEnv construction, or use an explicit subclass whose collect_game_files directly admits only the authenticated target without scanning other task bodies. Keep original config bytes and old helper unchanged. Preserve config semantics, game bytes, original canonical path, pool_seed, wrappers, reset/step normalization and closed public-field projection. Record the one intentional effective pool-discovery-path restriction separately from the immutable source YAML hash. No change to domain_randomization, expert_type, training_method, horizon or action semantics.

Required software check: factory construction must never open a sibling/new task body; use a fake boundary/trapped reader with a sentinel outside the exact task, and assert discovery restriction exists before factory __init__. Hash bound selected game/traj_data and logic inputs, no copies or arbitrary directory staging. This is engineering isolation, not an amendment to scientific selection or a release to read the new pool.

Root's read-only code inspection, exact installed-source location and trigger provide evidence for this scope addition; no speculative wider environment repair is authorized.
