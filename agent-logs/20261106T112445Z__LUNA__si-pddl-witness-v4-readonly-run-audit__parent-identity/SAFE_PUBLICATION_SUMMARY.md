# Safe publication summary — v4 synthetic CPU witness

- Run identity: `3430b0fe54214aaeb504d10836b9cecc`.
- Status: `PASS_SYNTHETIC_ENGINE_ONLY`; the coordinating operator reports the one supervisor invocation exited 0, and the persisted child result reports return code 0. No separate outer launcher exit receipt is present in the v4 evidence directory.
- The run used the exact previously reviewed v4 candidate hashes: supervisor `291a6bc3e9c1aaa2d312beb74ee583e4feba77c518d980dd4a95dd88d23ecd4e`, worker `5c3d6bac12b367c7452013dac42fabd5d7a02ce848190cbb8658f77f9ce60381`.
- Physical work: 1 environment construction, 1 load, 1 reset, 3 fixed action steps (4 reset/action operations total). All 36 ledger rows reconciled; 0 failed or incomplete started operations.
- The fixed three-action sequence completed its synthetic goal. No model call or generation occurred. This is an engineering witness, not research evidence or a policy evaluation.
- Duration `1.635s`; sampled peak process-tree CPU `1.43s`; sampled peak RSS `105070592 bytes`; peak watched disk `27738 bytes`.
- All 18 preclaim inputs matched expected SHA-256 before and after execution and were directly rehashed to the same values during this audit.
- Cleanup: process group gone; TERM/KILL not needed. The supervisor explicitly records escaped-session-descendant detection as `NOT_PROVEN`; do not interpret group cleanup as proof that no escaped descendant could exist.
- Raw SHA-256: operations ledger `7fcc08648008827e157bcbcbf09e59cfbb126b8c775441fcb6915b554f1a62d8`; preclaim `0383fdae15d3dcb08d98c29e333e0f0ab40d3bc9c3e43c14aef08e336ed70c88`; result `db6d1a8229337f0baa3e4935addef81ccb5a988ef818ca1f3a543760b3842613`; worker parent identity `377699b8a2a637c719f334bcef8501e94c7b3f3fb219d437675e6f3a8804a80a`. Empty stdout/stderr each hash to the standard empty SHA-256.

This summary omits machine paths, executable targets, PIDs, raw `/proc` bytes, and environment values. The detailed local originals inventory is not a public artifact.
