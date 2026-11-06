# Independent review correction

The first version accepted all-false and all-true target labels. Although its weights algebraically collapsed to one, the specification requires an informative contrast before use, so that behavior was incorrect. The previous files and their original checksums and passing test output are preserved in `review_v1_snapshot/`; that earlier pass does not establish acceptance.

The revised fixture rejects K=0 and K=M in both C1 and C4 before constructing a loss. Tests cover both multi-record endpoints and both single-record endpoints, through both the weights and window entry points. The new test run and exact file hashes are recorded separately in `TEST_OUTPUT.txt` and `SHA256SUMS`. This remains an isolated synthetic fixture pending independent review, not a production implementation.
