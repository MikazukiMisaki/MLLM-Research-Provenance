# Fictional final-only safetensors callback — HOLD

Isolated CPU engineering candidate, **not a real LoRA, model checkpoint, training run or scientific result**. The fixed interpreter has `safetensors 0.8.0` and PyTorch `2.6.0+cu124`; CUDA was hidden and all explicitly constructed tensors were on CPU. No real model, data, ALFWorld or GPU was accessed. This module has not been integrated into the synthetic optimizer kernel or independently reviewed. Its input labels and scope strings are not a security sandbox or proof that another caller is fictional.

The one-use callback accepts only exact final step 16 and a nonempty mapping of finite, explicitly `fictional.`-named CPU tensors; it rejects any existing target, including an empty directory, and rejects all subsequent calls even when the first was rejected or interrupted. It writes a new same-parent private temporary directory, writes `fictional.safetensors`, changes it to mode 0400 and fsyncs it and the temporary directory. It computes SHA-256 and independently opens it read-only through `safe_open`, compares metadata, names, dtype, shape and every tensor's bytes. Linux `renameat2(RENAME_NOREPLACE)` atomically publishes the whole directory only if the target remains absent; no overwrite fallback exists. It fsyncs the parent and repeats hash and read-only tensor comparisons after publication. The callback writes/fsyncs a mode-0400 receipt, fsyncs final and parent directories and returns `CONFIRMED_FICTIONAL_ONLY` only after those operations succeed.

Any exception or interruption after writes begin leaves the callback status UNKNOWN; no retry or cleanup is automatic, and a pending temporary directory or published target is preserved. The on-disk receipt deliberately says `RELOAD_CHECKED_CALLBACK_RETURN_REQUIRED` rather than claiming durable completion: a later fsync can fail or the process can die before returning. The demo's `callback_return.json` and stdout record the observed callback return, but are not themselves a crash-proof supervisor receipt. A missing return or incomplete evidence remains UNKNOWN, even if a file is visible. No general power-failure, malicious same-UID modification, platform portability or production checkpoint compatibility claim is made.

`test_final.log` records 5 tests passed with actual exit 0: final save/reload and duplicate refusal; nonfinal/existing target refusal; interruption leaving pending UNKNOWN; race-created nonempty target not overwritten; final directory-sync failure leaving UNKNOWN and a non-confirmatory receipt. `test_initial.log` retains the earlier 4-test version. A separate once-only fictional demo returned exit 0 and created `demo-output/final/fictional.safetensors` SHA256 `5976a9b8984f7f5bca626ac7fe56f76a11dd4c7f6c4de2033fb0c44a41e0f477`; its two tensors are invented toy values. Both demo files have mode 0400.

Test reproduction from this directory:

```
CUDA_VISIBLE_DEVICES='' OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 /home/lizening/miniconda3/envs/alfworld-self-improve/bin/python -I -B -c 'import sys,unittest;sys.path.insert(0,".");unittest.main(module="test_final_checkpoint",verbosity=2)'
```

This reruns tests only; do not rerun the once-only demo into its existing target. Exact hashes for code, logs and fictional output are in `FILE_HASHES.sha256`.
