# Pair lifecycle v2: independent CPU re-review

Reviewed candidate SHA256 `e6f40baa588ac8e3d308588870375b255b5e3dc2ee732f5db3441f70a1efa4af`;
test SHA256 `70a443b537ac2c49d521514d0bf20deab1d3679747d8aca511ac20d25517fe64`;
fake-arm SHA256 `6c2724936b89c3f855316c27c295d1b4e7f266e323d3305515cadbfaa1959b77`.

Independent execution of the 11 fictional unittest cases passed. Separate
replays of the earlier observations produced:

- A child that reports done after reset without a model was stopped with
  `required completed lifecycle missing`, owner failed and batch completion
  refused; model-load count remained zero.
- After three complete fake pairs, the fourth pair's second initial mismatch
  failed the owner with seven arms closed and eight started; batch completion
  was refused even after catching the exception.
- A fictional `/contained/../outside` path was refused as `unbound path`.

New concrete sequencing finding: `_pair`, candidate line 212, allows any
known case and either arm order without checking a fixed ordered roster.
An independent fictional run supplied `four,three,two,one`, each ordered
`B,A`; `owner.complete()` accepted it and the log recorded this order.
If a future protocol preassigns order, the owning runtime must bind and
enforce it before effects, including fail-stop on mismatch. This is not proof
that any real experiment was run in the wrong order.

The candidate remains test-only. It has not connected production actor,
materializer, verifier, resource supervisor, native success evidence,
process-group cleanup, wall-clock/token budget, or immutable task inputs.
All tests used fake setup and fake child subprocesses; no real task, model,
GPU or environment was invoked. This review does not grant launch approval.
