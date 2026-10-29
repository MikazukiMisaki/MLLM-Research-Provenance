# SI-M1 exact source preservation

This is a source-preservation checkpoint only. It is not an independent review, preflight, launch clearance, or scientific result.

The bundle contains the exact candidate Git commit `dfa382ad0ab604746690e96537dc4009cfeeefd0`, based on `f1e0d56a1be2a65876bbec5b8950fb76cda3eace`. The base commit was already available in the scientific repository. The candidate branch was not pushed to that repository.

The bundle was verified in a fresh Git repository seeded with the base; fetching bundle HEAD produced the exact candidate commit. The added-source diff was checked for common private-key, GitHub-token, and AWS-key patterns, with zero matches. The checkpoint does not include model files, datasets, or credentials.

To recover after obtaining the base commit in a Git repository: `git bundle verify si-m1-dfa382-source.bundle`, then `git fetch si-m1-dfa382-source.bundle HEAD`, and check `git rev-parse FETCH_HEAD` against the candidate SHA above.
