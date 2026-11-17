# Independent review: pidfd owner v3 directory synchronization

Scoped decision: **single filesystem durability fix matches its stated intent; HOLD and all other v2 restrictions remain.** This is not an integrated supervisor or scientific execution approval.

Exact v3 `owner.py` SHA256 `22490ccecf712a1dd1242381852ab688da046516e737f839c6029d32c8280828`; independently diffed against v2 owner SHA256 `d3f4805d35d451b533b73831236e32ecfdea3e4177701d64b04756f0de887fbe`. The sole delta immediately after `root.mkdir` opens its existing parent directory with `O_DIRECTORY|O_NOFOLLOW`, fsyncs it, and closes it before journal creation or any child start. The copied pidfd prior source SHA256 remains `4ba5ac6e9926f2d2c0fd20e3164e140fe28833773d46a5a00c9f896e6689f40a`. No other owner logic changed.

Independent pinned-Python run of `test_directory_sync.py` SHA256 `a7f3a46dc795952ed8df0acb150426b4fef1ec070d8b4a40be092bc3df846e8f` passed 2/2, exit 0; raw `tests.log` SHA256 `6f62f41d154d9d9f1e949624f8e2e14ca3f1334ab21631065627f0e9bf9ff140`. It observed parent-directory -> owner-directory -> journal fsync order and injected parent fsync EIO, which propagated before journal or spawn; failed directory remains and is not reused. No actual process, model, GPU, environment, or task was run in these tests.

This tests the system-call path, not real power failure or storage hardware behavior. Parent ancestors' durability, filesystem semantics, exception windows, no-reaper requirements, Popen-internal failure, SIGKILL, untrusted or escaped descendants, host/GPU ownership, actual physical budget and integration remain unproved. See independent v2 review `/home/lizening/research-notes/agent-logs/20261118__REVIEW__pidfd_owner_v2__iqj8Cw/REVIEW.md`. No experiment clearance.
