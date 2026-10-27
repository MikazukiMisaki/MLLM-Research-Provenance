# 追加意见：封住已消耗旧授权的程序入口

结论：接受所提追加撤销guard。它是事后行政判定，不是伪造原始supervisor执行证据。本轮未创建该guard，也未执行旧/新CLI。

exact f1e0d56 的 engineering_gate.py:100 对preflight/live均要求claim不存在；supervisor_core.py:26及evidence.py:12–14还通过exclusive-create拒绝已有claim。因此，在旧output旁建立该标记会封住未修改入口对旧授权的再用；即使先前已越过gate，后续原子排他的claim创建仍拒绝已有文件。这不是针对有文件删除权限者的不可绕过撤销系统，标记必须保留。

必要条件：

- 使用ROOT_REVOKED_CONSUMED_ENGINEERING_AUTHORITY_GUARD_V1等明确独立schema，标明POST_FAILURE_REVOCATION、issuer ROOT、实际新建UTC、旧run/auth/clearance/source身份、原失败receipt路径及哈希、撤销理由；worker_created=false，不冒充supervisor schema、时间、worker或结果。
- 只在旧output+'.launch_claim.json'排他创建普通文件，不覆盖、不跟随符号链接；遇到任何既存条目即停，不删除以重建。完成后持久化并独立记录哈希与路径，再进行新的放行流程。
- 旧output继续不存在；原8份失败文件、旧auth及clearance字节不变。原absence快照明确是失败当时观察，不能回写。新guard单独归入事后撤销记录，不纳入原失败时的原始证据清单。
- 不运行旧CLI来证明拒绝；源码条件加文件存在性/哈希足够。新auth/run/output必须独立，每份maximum_launches=1；Root明确family总数2（已用1、余1），费用与单元限制沿用主审查意见，先新预检与独立exact放行。

不需要为本项撤销修改源代码、旧授权或旧证据。此前主审查REVIEW.md及其SHA256SUMS保持原字节；本追加意见单独封存。

静态源码绑定：
- src/self_improvement/si_s01/engineering_gate.py SHA256 ff62ec4d6db94be5c09c5a2e89cb3599fd851805fbdb01729c07de263128d0c0
- src/self_improvement/si_s01/supervisor_core.py SHA256 2a7dc2e601788b4556452f0d10b85fbaa33117715deac10617d4a7becb8f81ba
- src/self_improvement/si_s01/evidence.py SHA256 4048468a1666d23547f0d48cfcd42d20edd526893498a0d91e7434ad3cb5a1f0

完成UTC：2026-10-26T23:21:41.642378+00:00
