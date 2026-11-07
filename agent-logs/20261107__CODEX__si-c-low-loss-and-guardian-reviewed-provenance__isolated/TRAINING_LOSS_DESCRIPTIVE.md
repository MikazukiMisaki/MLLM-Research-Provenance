# C-low training-loss description

This is a descriptive calculation from the existing training journal; no
model, tokenizer or environment was invoked. Of 1,248 recorded completed
microbatch losses, all were finite. In the recorded order, the arithmetic mean
of each consecutive block of 312 losses was:

| Training pass | Mean recorded loss |
| --- | ---: |
| 1 | 0.008589 |
| 2 | 0.009103 |
| 3 | 0.016435 |
| 4 | 0.003676 |

The trainer records the model's per-microbatch loss before multiplying it by
the active-token fraction used for gradient accumulation. These are repeated,
shuffled presentations of development training data. Loss is not monotonic
across passes. No independent validation loss or task-success measurement was
performed, so the fourth-pass training loss is not evidence of improved agent
success or generalization. The inner training completion and the outer
supervision UNKNOWN must be reported separately as in the independent postrun
audit.

The source journal's point-in-time SHA256 was independently recorded as
`6477fc4c102f1329688fa7b9fdbeae9c5c9f2c6c2d316ed1e12e54f7d5d15432`.
Raw event rows contain training identifiers and remain private. These rounded
values are an unverified coordinator calculation pending independent review.
