# Pair interface candidate: independent CPU review

Reviewed `candidate.py` SHA256
`4cc7aff6ae06972d0d1170c14e75bf7c8dd1b88ffb3806ce309d0f22dfd78c0b`.
The candidate explicitly has no production materializer, actor, resource owner,
or environment integration and these tests do not establish readiness.

1. `candidate.py:193–202` accepts a child `done` once its reset has been
   counted, initial has been supplied and `won` is boolean. It does not require
   construction, initialization, model load, generation, or evidence of a
   native outcome. `Owner.complete`, lines 107–110, checks setup and arm
   **starts**, not their completed validated effects. An isolated synthetic
   test ran all four pairs with reset, initial and `won=true` only. The owner
   accepted eight results and `complete` with `model_load=0, generation=0,
   step=0, env_construct=0, env_init=0`. The minimum allowed completed
   operations and legitimate no-step policy outcomes need an explicit contract.
2. If a pair raises, `candidate.py:207–215` does not permanently stop the
   owner. After three fake completed pairs and a fourth with second-arm initial
   mismatch, catching `Stop('initial mismatch')` left 8 arm starts and no
   open reservation. `Owner.complete()` succeeded despite only 7 arm results
   and 7 model loads. Future integration needs fail-stop owner state and
   completion checks that include successful per-arm post-verification.
3. `candidate.py:124–132,144–147` uses lexical `Path.is_relative_to` without
   rejecting `..`; a syntactically contained absolute path can resolve outside
   the root without a symlink. This is a static boundary defect; the actual
   injected production materializer is not connected and no escape was run.

The two observed reproductions use only invented files and fictional child
processes. The equivalent repeatable script is `reproduce.py`. Original code,
run evidence, scientific data, models and environments were not modified.
No launch authorization is implied.
