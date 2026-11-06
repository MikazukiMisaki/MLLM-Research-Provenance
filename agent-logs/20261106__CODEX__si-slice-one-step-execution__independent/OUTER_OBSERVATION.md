# Outer process observation

The coordinator invoked a shell through the execution tool in the fixed candidate directory. `set -o noclobber` was set. The child used an empty inherited environment apart from PATH=/usr/bin:/bin, LANG=C.UTF-8, LC_ALL=C.UTF-8, CUDA_VISIBLE_DEVICES empty, OMP_NUM_THREADS=1 and OPENBLAS_NUM_THREADS=1; argv was the pinned interpreter, `-I`, `-B`, fixed launcher and `--run-once`. Fresh outer stdout and stderr files captured the process; shell status was written to outer.exit and returned.

The original tool call yielded session 93829; the subsequent tool poll reported completed exit_code=0 and empty output. This is a coordinator transcription, not a separately signed external receipt. The saved outer.exit also reports 0. Detailed paths are retained in local invocation/source bindings. No retry was invoked.
