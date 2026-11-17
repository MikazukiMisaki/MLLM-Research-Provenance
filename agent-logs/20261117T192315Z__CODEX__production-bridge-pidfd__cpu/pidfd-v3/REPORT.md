# Owner directory entry sync: isolated CPU revision, HOLD

Responds only to `/home/lizening/research-notes/agent-logs/20261118__REVIEW__pidfd_owner_v2__iqj8Cw/REVIEW.md`. In a new directory, `owner.py` adds an fsync of the existing parent directory immediately after creating the owner directory, before creating its journal or launching a subprocess. The existing fsync of the owner directory after journal creation and fsync of journal records remain. Parent-directory open, sync or close errors propagate from construction; the caller receives no usable owner and no process is launched. The created directory may remain; it is not silently reused. Parent ancestors must themselves already be durable and the filesystem must honor the relevant fsync semantics. Tests do not simulate power loss and do not establish storage-hardware guarantees.

Pinned Python run: two fake filesystem tests passed (exit 0). One records actual fsync calls in parent-directory, owner-directory, journal order. One injects EIO at parent fsync and confirms error propagation, retained directory, absent journal, and zero Popen calls. No child, model, GPU, environment or task was run. This tiny delta did not rerun the separate direct-child suite; the six-test v2 evidence and its limitations remain in the prior report.

```
/home/lizening/miniconda3/envs/alfworld-self-improve/bin/python -I -B -c 'import sys,unittest;sys.path.insert(0,".");unittest.main(module="test_directory_sync",verbosity=2)'
```

`owner.py` SHA256 `22490ccecf712a1dd1242381852ab688da046516e737f839c6029d32c8280828`; `owner.diff` SHA256 `ae6127c1ba1e85aa36e7b810ba86c9fe4ffb0a5157119af2d5f8af6fa9d2772a`; `test_directory_sync.py` SHA256 `a7f3a46dc795952ed8df0acb150426b4fef1ec070d8b4a40be092bc3df846e8f`; `test.log` SHA256 `6f62f41d154d9d9f1e949624f8e2e14ca3f1334ab21631065627f0e9bf9ff140`.

The process-identity and interruption assumptions, Popen-internal-failure and SIGKILL gaps, unknown descendants, storage failures and absent GPU proof still apply. This is not a supervisor or permission to start another arm. HOLD remains in force.
